import abc
import datetime
import json
import time
import zlib
from collections import deque
from concurrent.futures import ThreadPoolExecutor, wait

import boto3
from botocore.exceptions import ClientError
from maaslogger import base_logger
from simple_retry.decorators import retry
from simple_settings import settings

from taz.constants import RETRY_EXCEPTIONS, MessageStatus
from taz.consumers.core.brokers.base import BaseBroker
from taz.consumers.core.cache.redis import CacheMixin
from taz.consumers.core.exceptions import (
    RequiredFieldException,
    RequiredNonEmptyFieldException
)

logger = base_logger.get_logger(__name__)

KINESIS_SEQUENCE_KEY = 'taz_kinesis_{shard_id}_{app_name}_last_sequence'
KINESIS_LOCK_KEY = 'taz_kinesis_{shard_id}_{app_name}_lock'
KINESIS_AFTER_SEQUENCE_NUMBER = 'AFTER_SEQUENCE_NUMBER'


class BotoKinesisBroker(BaseBroker, CacheMixin):

    def __init__(self, *args, **kwargs):
        self._kinesis = boto3.Session().client(
            'kinesis',
            region_name=settings.KINESIS_REGION
        )
        self._cache = self.get_cache()

        self._record_processor = self.record_processor_class(
            self.scope
        )
        self.kinesis_max_time_process = float(
            settings.KINESIS_MAX_TIME_PROCESS
        )

    @abc.abstractmethod
    def scope(self):
        """
        This property define the scope of consumer
        """

    @abc.abstractmethod
    def app_name(self):
        """
        This property define the app_name of consumer
        """

    @abc.abstractproperty
    def fetch_interval(self):
        """
        This property define the fetch interval of chunks
        """

    @abc.abstractproperty
    def error_retry_interval(self):
        """
        This property define the fetch interval error retries
        """

    @property
    def record_processor_class(self):
        raise NotImplementedError(
            'You need to specify the `KinesisRecordProcessor` class in '
            '`record_process_class` attribute of `KinesisBroker`'
        )

    def stream_name(self):
        return settings.CONSUMERS[self.scope]['stream_name']

    def start(self):
        stream = self._describe_stream()
        shards = stream['StreamDescription']['Shards']

        while True:
            try:
                for shard_data in shards:
                    self.run_processor(shard_data)
            except Exception as e:
                logger.critical(
                    'Critical error in stream processing with '
                    'error:{}'.format(e)
                )

    def run_processor(self, shard_data):
        try:
            if settings.KINESIS_STOP:
                logger.warning(
                    "KINESIS_STOP=True, the consumer is stopped"
                )
                return

            shard_id = shard_data['ShardId']

            if self._verify_shard_lock(shard_id):
                return

            if not shard_id:
                return

            self._process_records(shard_id)
            self._sleep_interval()

        except ClientError as e:
            logger.warning(
                'Encountered client error: {error} scope: {scope}'.format(
                    error=e,
                    scope=self.scope
                )
            )
            self._sleep_error()

        except Exception as e:
            logger.exception(
                'Encountered generic error: {error} scope: {scope}'.format(
                    error=e,
                    scope=self.scope
                )
            )
            self._sleep_error()

    def _process_records(self, shard_id):
        logger.debug(
            'Starting record processor '
            'to {scope} in shard_id:{shard_id}'.format(
                scope=self.scope,
                shard_id=shard_id
            )
        )

        try:
            self._lock_shard(shard_id)
            shard_iterator = self._get_shard_iterator(shard_id)
            record_response = self._get_records(shard_iterator)
            processing_time = 0
            processing_start_time = time.time()

            while (
                (
                    (record_response.get('MillisBehindLatest') or 0) > 0 or
                    len(record_response.get('Records') or []) > 0
                ) and
                processing_time <= self.kinesis_max_time_process
            ):
                self._lock_shard(shard_id)
                queue = deque()
                start = time.time()

                records = record_response['Records']

                logger.debug(
                    'Lag time:{}'.format(
                        datetime.datetime.fromtimestamp(
                            record_response['MillisBehindLatest'] / 1000
                        ).strftime('%H:%M:%S')
                    )
                )

                if not records:
                    logger.debug(
                        'Records in shard_id:{shard_id} is empty'.format(
                            shard_id=shard_id
                        )
                    )

                    self._sleep_interval()
                else:
                    for record in records:
                        queue.append(record)

                    self._multi_process_records(shard_id, queue)
                    self._save_sequence_number(
                        shard_id, record.get('SequenceNumber', 0)
                    )

                    logger.debug(
                        'Processed records from scope:{scope} and '
                        'shard_id:{shard_id} in:{sec} seconds'.format(
                            scope=self.scope,
                            shard_id=shard_id,
                            sec=time.time() - start
                        )
                    )

                record_response = self._get_records(
                    record_response.get('NextShardIterator')
                ) or {}

                if not record_response.get('NextShardIterator'):
                    logger.info(
                        'Our shard_id {} has been closed, exiting'.format(
                            shard_id
                        )
                    )
                    break

                processing_time = time.time() - processing_start_time

        except ClientError as e:
            logger.warning(
                'Encountered an aws error: {code} scope: {scope} '
                'detail: {detail}'.format(
                    code=e.response['Error']['Code'],
                    scope=self.scope,
                    detail=e.response['Error']
                )
            )

            raise e
        finally:
            self._unlock_shard(shard_id)

    def _multi_process_records(self, shard_id, queue):
        with ThreadPoolExecutor(
            max_workers=int(self.max_process_workers)
        ) as executor:
            futures = [
                executor.submit(
                    self._record_processor.process_record,
                    queue.pop(), shard_id
                ) for _ in range(len(queue)) if queue
            ]
        completed, _ = wait(futures)

        try:
            for future in completed:
                future.result()
        except Exception:
            logger.exception(
                'Encountered an exception while create multiprocess to '
                'process records of scope "{}"'.format(self.scope)
            )

    def _save_sequence_number(self, shard_id, sequence_number):
        self._cache.set(
            self._generate_key(shard_id),
            sequence_number
        )

    @retry(
        ClientError, retries=4, delay=5, logger=logger,
        level='warning', multiple=2
    )
    def _get_records(self, shard_iterator):
        """
        get records on shard_iterator. When get_records
        return exception informed in RETRY_EXCEPTIONS, the method will be
        retried, else raise Exception. The retries will be exponential.
        MAX DELAY 40s.
        """
        if shard_iterator:
            try:
                return self._kinesis.get_records(
                    ShardIterator=shard_iterator,
                    Limit=self.chunk_size
                )
            except ClientError as e:
                code = e.response['Error']['Code']
                if code in RETRY_EXCEPTIONS:
                    raise e

                raise Exception(e)

    def _get_shard_iterator(self, shard_id):
        last_sequence_number = self._get_last_sequence_number(shard_id)

        if last_sequence_number:
            try:
                return self._get_after_sequence_iterator(
                    shard_id,
                    last_sequence_number
                )
            except ClientError as e:
                code = e.response['Error']['Code']
                message = e.response['Error']['Message']
                if (
                    'InvalidArgumentException' == code and
                    'StartingSequenceNumber' in message and
                    'is invalid because it did not come from' in message
                ):
                    logger.warning(
                        'the sequence "{seq}" does not exist in the stream, '
                        'getting horizon iterator, scope={scope}'.format(
                            seq=last_sequence_number,
                            scope=self.scope
                        )
                    )
                else:
                    raise e

        return self._get_trim_default_iterator(shard_id)

    def _get_after_sequence_iterator(self, shard_id, sequence_number):
        '''
        return shard iterator with AFTER_SEQUENCE_NUMBER type
        AFTER_SEQUENCE_NUMBER delivery all message after sequence informed
        in StartingSequenceNumber parameter
        '''

        logger.debug(
            'get shard iterator from shard:{shard_id} using '
            'AFTER_SEQUENCE_NUMBER with {seq}'.format(
                shard_id=shard_id,
                seq=sequence_number
            )
        )
        try:
            return self._kinesis.get_shard_iterator(
                StreamName=self.stream_name(),
                ShardId=shard_id,
                ShardIteratorType=KINESIS_AFTER_SEQUENCE_NUMBER,
                StartingSequenceNumber=sequence_number
            )['ShardIterator']
        except Exception as e:
            logger.warning(
                'Error getting shard iterator error: {error} '
                'shard_id: {shard_id} sequence_number:{sequence}'.format(
                    error=e,
                    shard_id=shard_id,
                    sequence=sequence_number
                )
            )
            raise e

    def _get_trim_default_iterator(self, shard_id):
        logger.info(
            'get shard iterator from shard:{shard_id} '
            ' using {iteratorType}'.format(
                shard_id=shard_id,
                iteratorType=settings.KINESIS_ITERATOR_TYPE
            )
        )
        return self._kinesis.get_shard_iterator(
            StreamName=self.stream_name(),
            ShardId=shard_id,
            ShardIteratorType=settings.KINESIS_ITERATOR_TYPE
        )['ShardIterator']

    def _get_kinesis_shards(self):
        stream = self._describe_stream()

        shards = stream['StreamDescription']['Shards']

        return len(shards)

    def _get_available_kinesis_shard(self):

        stream = self._describe_stream()

        shards = stream['StreamDescription']['Shards']
        shard_ids = map(lambda shard: shard['ShardId'], shards)

        for shard_id in shard_ids:
            if not self._verify_shard_lock(shard_id):
                self._lock_shard(shard_id)
                return shard_id

    @retry(ClientError, retries=5, delay=5, logger=logger, level='warning')
    def _describe_stream(self):
        return self._kinesis.describe_stream(
            StreamName=self.stream_name()
        )

    def _verify_shard_lock(self, shard_id):
        key = self._generate_lock_key(shard_id)
        lock = self._cache.get(key)
        return lock is not None

    def _generate_key(self, shard_id):
        return KINESIS_SEQUENCE_KEY.format(
            shard_id=shard_id,
            app_name=self.app_name
        )

    def _generate_lock_key(self, shard_id):
        return KINESIS_LOCK_KEY.format(
            shard_id=shard_id,
            app_name=self.app_name
        )

    def _lock_shard(self, shard_id):
        key = self._generate_lock_key(shard_id)
        self._cache.set(key, True, settings.KINESIS_LOCK_EXPIRE)

    def _unlock_shard(self, shard_id):
        key = self._generate_lock_key(shard_id)
        self._cache.delete(key)

    def _sleep_lock(self):
        logger.info(
            'Sleeping {sec} seconds because dont '
            'have available shard'.format(
                sec=settings.KINESIS_LOCK_EXPIRE
            )
        )
        time.sleep(float(settings.KINESIS_LOCK_EXPIRE))

    def _sleep_interval(self):
        logger.debug(
            'Sleeping {sec} seconds'.format(
                sec=self.fetch_interval
            )
        )

        time.sleep(float(self.fetch_interval))

    def _sleep_error(self):
        logger.info(
            'Sleeping {sec} seconds'.format(sec=self.error_retry_interval)
        )
        time.sleep(float(self.error_retry_interval))

    def _get_last_sequence_number(self, shard_id):
        sequence_number = self._cache.get(
            self._generate_key(shard_id)
        )
        sequence_number = self.normalize_value(sequence_number)
        if not sequence_number:
            return None
        return sequence_number

    def normalize_value(self, value):
        return value.decode('utf-8') if isinstance(value, bytes) else value


class BotoKinesisRecordProcessor:

    required_fields = []
    required_fields_create = []
    required_fields_update = []
    required_fields_delete = []

    required_non_empty_fields = []
    required_non_empty_fields_create = []
    required_non_empty_fields_update = []
    required_non_empty_fields_delete = []

    DEFAULT_ENCODING = 'utf-8'

    def __init__(self, scope, *args, **kwargs):
        self.scope = scope
        super().__init__(*args, **kwargs)

    def initialize(self, shard_id):
        logger.info('Initializing shard {} in scope {}'.format(
            shard_id,
            self.scope
        ))
        self.shard_id = shard_id

    def create(self, data):
        self._validations(data, 'create')
        self._create(data)

    def update(self, data):
        self._validations(data, 'update')
        self._update(data)

    def delete(self, data):
        self._validations(data, 'delete')
        self._delete(data)

    def _before_checkpoint(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _create(self, data):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _update(self, data):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _delete(self, data):  # pragma: no cover
        pass

    def _validations(self, data, action):
        self._validate_required_fields(data, action)
        self._validate_required_non_empty_fields(data, action)

    def _validate_required_non_empty_fields(self, data, action):
        required_non_empty_fields = getattr(
            self, 'required_non_empty_fields_{}'.format(action)
        )
        required_non_empty_fields = (
            required_non_empty_fields or self.required_non_empty_fields
        )
        if not required_non_empty_fields:
            return

        empty_fields = [
            f for f in required_non_empty_fields
            if f not in data or not bool(data[f])
        ]
        if empty_fields:
            raise RequiredNonEmptyFieldException(
                empty_fields, self.scope, action, data
            )

    def _validate_required_fields(self, data, action):
        required_fields = getattr(self, 'required_fields_{}'.format(action))
        required_fields = required_fields or self.required_fields

        if not required_fields:
            return

        missing_fields = [
            field for field in required_fields
            if field not in data
        ]

        if missing_fields:
            logger.warning(
                'Required fields {fields} of scope {scope} is missing for '
                'action {action}'.format(
                    fields=missing_fields,
                    scope=self.scope,
                    action=action
                )
            )

            raise RequiredFieldException(
                missing_fields, self.scope, action, data
            )

    @abc.abstractmethod
    def get_id(self, data):
        """
        This method return unique id from received data
        """

    def process_record(self, record, shard_id=None):
        try:
            if settings.ENABLE_KINESIS_COMPRESS:
                try:
                    decoded_data = json.loads(
                        zlib.decompress(
                            record.get('Data')
                        ).decode(self.DEFAULT_ENCODING)  # noqa
                    )
                except zlib.error:
                    decoded_data = json.loads(
                        record.get('Data').decode(self.DEFAULT_ENCODING)
                    )
            else:
                decoded_data = json.loads(
                    record.get('Data').decode(self.DEFAULT_ENCODING)
                )

            action = decoded_data.get('action')
            data = decoded_data.get('data')
            approximate_arrival = record.get('ApproximateArrivalTimestamp')

            status = MessageStatus.ERROR
        except Exception as e:
            logger.warning(
                'Encountered a generic error: {error} scope: {scope} '
                'parsing data with record: {record}'.format(
                    error=e,
                    scope=self.scope,
                    record=record
                )
            )
            return

        try:
            if not data or not action:
                logger.error(
                    'Invalid data for scope: {scope}: {data}'.format(
                        scope=self.scope,
                        data=data
                    )
                )
                return

            _action = action if not action == 'remove' else 'delete'
            if action in ['create', 'update', 'remove', 'delete']:
                logger.info(
                    'Processing action:{action} for scope:{scope} '
                    'with data:{data}'.format(
                        action=action,
                        scope=self.scope,
                        data=data
                    )
                )
                getattr(self, _action)(data)
            else:
                logger.warning(
                    'Unknow action {action} for scope {scope} '
                    'with data: {data}'.format(
                        action=action,
                        scope=self.scope,
                        data=data
                    )
                )
            status = MessageStatus.SUCCESS
        except RequiredNonEmptyFieldException as e:
            logger.warning(
                'Required non empty field exception with action:{action} '
                'scope:{scope} error:{error}'.format(
                    action=action,
                    scope=self.scope,
                    error=e
                )
            )
        except Exception as e:
            logger.exception(
                'Encountered generic exception for action:{action} '
                'scope: {scope} with id: {id}, error:{error}'.format(
                    action=action,
                    scope=self.scope,
                    id=data.get('id'),
                    error=e
                )
            )
        finally:
            log = (
                logger.info
                if not status == MessageStatus.ERROR else logger.error
            )
            self._before_checkpoint()
            self._log_processing_status(
                log,
                self.scope,
                shard_id,
                status,
                approximate_arrival,
                self.get_id(data)
            )
        return log == logger.info, record

    def _log_processing_status(
        self,
        log,
        scope,
        shard_id,
        status,
        approximate_arrival,
        unique_id
    ):
        log(
            'Processed message from scope:{scope} shard_id:{shard_id} '
            'id:{id} with status:{status} ages '
            'approximate_arrival:{approximate_arrival}'.format(
                scope=scope,
                shard_id=shard_id,
                id=unique_id,
                status=status.value,
                approximate_arrival=approximate_arrival
            )
        )
