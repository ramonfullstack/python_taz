from abc import abstractmethod
from functools import cached_property
from typing import Dict

from maaslogger import base_logger

from taz.consumers.core.google.stream import StreamPublisherManager
from taz.consumers.core.kafka.producer import KafkaProducer

logger = base_logger.get_logger(__name__)


class PublishDatalakeInterface:

    @abstractmethod
    def publish(self, message: Dict, config: Dict):
        ...

    @abstractmethod
    def mount_payload(self, message: Dict, **kwargs):
        ...


class PubsubNiagara(PublishDatalakeInterface):

    @cached_property
    def pubsub(self):
        return StreamPublisherManager()

    def publish(self, message: Dict, config: Dict):
        self.pubsub.publish(
            content=message,
            topic_name=config['topic_name'],
            project_id=config['project_id']
        )

    def mount_payload(self, message: Dict, **kwargs):
        scope = kwargs.get('scope_name')
        return {
            'data': message,
            'schema': scope
        }


class KafkaTetrix(PublishDatalakeInterface):

    @cached_property
    def kafka(self):
        return KafkaProducer('datalake')

    def publish(self, message: Dict, config: Dict):
        self.kafka.publish(
            topic=config['topic_name'],
            message=message
        )

    def mount_payload(self, message: Dict, **kwargs):
        return message


class PublishDatalakeContext:

    def __init__(self, strategy: PublishDatalakeInterface):
        self.__strategy = strategy

    def send_message(self, message: Dict, config: Dict):
        self.__strategy.publish(message, config)

    def format_payload(self, message: Dict, **kwargs):
        return self.__strategy.mount_payload(message, **kwargs)
