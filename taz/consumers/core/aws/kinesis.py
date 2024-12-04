import hashlib
import time

from boto import kinesis
from boto.exception import JSONResponseError
from maaslogger import base_logger
from simple_settings import settings

from taz.consumers.core.exceptions import BadRequest
from taz.helpers.json import json_dumps

logger = base_logger.get_logger(__name__)


class KinesisManager:

    def __init__(
        self,
        stream_name,
        region=settings.KINESIS_REGION
    ):
        self.stream_name = stream_name
        self.kinesis = kinesis.connect_to_region(
            region_name=region,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

    def put(self, action, payload):
        partition_key = self._md5(payload)
        record = self._wrap(action, payload)

        start_time = time.time()

        try:
            self.kinesis.put_record(
                self.stream_name,
                record,
                partition_key
            )
        except JSONResponseError as e:
            logger.error('Kinesis JSON response error {}'.format(e))
            raise BadRequest()

        logger.debug(
            'Sent to stream_name:{stream_name} with action:{action} '
            'and record {record} sent in {duration}s'.format(
                stream_name=self.stream_name,
                action=action,
                record=record,
                duration=time.time() - start_time
            )
        )

    def _md5(self, item):
        return hashlib.md5(str(item).encode('utf-8')).hexdigest()

    def _wrap(self, action, item):
        return json_dumps({
            'action': action,
            'data': item,
        }, ensure_ascii=False)
