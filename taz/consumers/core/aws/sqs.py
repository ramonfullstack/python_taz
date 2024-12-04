import boto3
from botocore.exceptions import ClientError
from maaslogger import base_logger
from simple_settings import settings

from taz.constants import APPROXIMATE_RECEIVE_COUNT
from taz.consumers.core.brokers.exceptions import QueueError
from taz.helpers.json import json_dumps

logger = base_logger.get_logger(__name__)


class SQSManager:

    def __init__(
        self, queue_name, region_name=settings.DEFAULT_AWS_SETTINGS['region']
    ):
        self.client = boto3.resource(
            'sqs',
            region_name=region_name,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        self.queue_name = queue_name
        self._queue = None

    @property
    def queue(self):
        if not self._queue:
            try:
                self._queue = self.client.get_queue_by_name(
                    QueueName=self.queue_name
                )
            except ClientError as e:  # pragma: no cover
                logger.error(
                    'Fail to get SQS queue:{}'.format(self.queue_name)
                )
                raise QueueError(e.response['Error']['Code'])

        return self._queue

    def put(self, message):
        if not message:
            raise QueueError('Message cannot be empty')

        logger.debug('Sending message {} to queue:{}'.format(
            message,
            self.queue_name
        ))

        self.queue.send_message(
            MessageBody=json_dumps(message, False)
        )

    def get(self):
        messages = self.queue.receive_messages(
            MaxNumberOfMessages=settings.QUEUE_BATCH_READ_SIZE,
            AttributeNames=[APPROXIMATE_RECEIVE_COUNT]
        )
        logger.debug(
            'Got {} messages from queue:{}'.format(
                len(messages),
                self.queue_name
            )
        )
        return messages
