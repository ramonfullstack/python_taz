import hashlib
import logging
import time
import zlib
from concurrent.futures import ThreadPoolExecutor, as_completed, wait

from boto import kinesis
from simple_settings import settings

from taz import constants
from taz.helpers.json import json_dumps
from taz.pollers.core.exceptions import SendRecordsException

from .base import BaseBroker
from .exceptions import MissingPollerSettingException

logger = logging.getLogger(__name__)


class KinesisBroker(BaseBroker):

    def __init__(self, scope):
        if scope not in settings.POLLERS.keys():
            raise MissingPollerSettingException(
                'Poller {} is not properly set on settings file'.format(scope)
            )

        super().__init__()
        self.scope = scope
        self.waits = {}
        self.halt_requested = False
        self.executor = ThreadPoolExecutor(
            max_workers=settings.SENDER_MAX_WORKERS
        )

        self.__connect(
            settings.POLLERS[scope]['stream_name'],
            settings.POLLERS[scope]['aws_settings']['region']
        )

    def __connect(self, stream_name, region):
        self.stream_name = stream_name
        self.region = region
        logger.debug('Connecting to stream: {} in {}'.format(
            self.stream_name,
            self.region,
        ))
        self.conn = kinesis.connect_to_region(
            region_name=self.region,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

    def put_many(self, action, dataset):
        if self.halt_requested:
            return

        start_time = time.time()

        self.waits = {
            self.executor.submit(
                self._process_record,
                self._md5(item),
                action,
                item
            ): item
            for item in dataset if not self.halt_requested
        }

        process_fail = False
        completed, _ = wait(self.waits)
        for future in completed:
            item = self.waits[future]
            try:
                for future in completed:
                    future.result()
            except Exception:
                logger.exception(
                    'Encountered an exception while send many records to '
                    'Scope "{}" with action "{}": {}'.format(
                        self.scope, action, item
                    )
                )
                process_fail = True

        if process_fail:
            raise SendRecordsException()

        logger.debug('Sent all records in {}s'.format(
            time.time() - start_time
        ))

    def shutdown(self):
        if not self.waits:
            return

        logger.warning('Requesting executor shutdown...')
        self.executor.shutdown(wait=True)
        self.halt_requested = True
        for future in as_completed(self.waits):
            logger.warning(
                'Thread with item {} was completed'.format(
                    self.waits[future]
                )
            )
            try:
                future.result()
            except Exception as e:
                logger.error(e)

    def _wrap(self, action, item):
        return json_dumps({
            'action': action,
            'data': item,
        }, ensure_ascii=False)

    def _md5(self, item):
        return hashlib.md5(str(item).encode('utf-8')).hexdigest()

    def _process_record(self, partition_key, action, item):
        if self.halt_requested:
            return

        record = self._wrap(action, item)
        if settings.ENABLE_KINESIS_COMPRESS:
            record = zlib.compress(record.encode())

        logger.debug('Sending record {} to stream {} in {}'.format(
            item,
            self.stream_name,
            self.region,
        ))

        start_time = time.time()
        self.conn.put_record(
            self.stream_name,
            record,
            partition_key,
        )

        record_msg = (
            'sku:{i[sku]}, seller:{i[seller_id]}'.format(i=item)
            if 'sku' in item else record
        )

        logger.info(
            'Sent to scope:{} with action:{} and record {} '
            'sent in {}s'.format(
                self.scope, action, record_msg, time.time() - start_time
            )
        )


class SendKinesisMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.writer = KinesisBroker(self.poller_scope)

    def send(self, rows, batch):
        counter = rows.count()
        while counter > 0:
            range_count = batch if counter >= batch else counter

            products = []
            for _ in range(range_count):
                raw_product = rows.next()
                del raw_product['_id']

                raw_product['origin'] = constants.REBUILD_ORIGIN
                products.append(raw_product)

            self.writer.put_many('update', products)
            counter -= range_count

        self.writer.shutdown()
