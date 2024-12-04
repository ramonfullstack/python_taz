from functools import cached_property
from typing import Dict

from confluent_kafka import Producer
from maaslogger import base_logger

from taz.consumers.core.kafka.config import KafkaConfig
from taz.helpers.json import json_dumps

logger = base_logger.get_logger(__name__)


class KafkaProducer:

    def __init__(self, cluster_name: str):
        try:
            self.__config = KafkaConfig.load(cluster_name)
        except Exception as e:
            raise Exception(f'Error to load kafka config, error:{e}')

    @cached_property
    def producer(self) -> Producer:
        config = self.__config.to_dict_config(producer=True)
        logger.debug(f'Create producer Kafka with config:{config}')
        return Producer(config)

    def publish(
        self,
        topic: str,
        message: Dict,
        key: str = None
    ):
        try:
            payload = json_dumps(message).encode('utf-8')
            self.producer.produce(topic=topic, value=payload, key=key)
            logger.debug(f'Successfully sent message to Kafka topic:{topic}')
            self.producer.poll(0)
        except Exception as e:
            logger.error(
                f'Error to publish message on Kafka topic:{topic} '
                f'with error:{e}'
            )
            raise
