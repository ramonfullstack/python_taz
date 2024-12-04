from typing import Any, Dict, NamedTuple, Optional

from simple_settings import settings


class KafkaConfig(NamedTuple):

    cluster_name: str
    cluster_config: Dict
    consumer_extra: Optional[Dict[str, Any]] = {}
    producer_extra: Optional[Dict[str, Any]] = {}

    def to_dict_config(self, *, producer: bool) -> Dict[str, Any]:
        if producer:
            node = {**self.producer_extra}
        else:
            node = {**self.consumer_extra}

        return {
            **self.cluster_config,
            **node
        }

    @classmethod
    def load(
        cls,
        cluster_name: str,
        consumer_extra_configs: Dict = None,
        producer_extra_configs: Dict = None
    ):

        cluster_config = settings.KAFKA_CLUSTERS_CONFIG[cluster_name]

        return cls(
            cluster_name=cluster_name,
            cluster_config=cluster_config,
            consumer_extra=consumer_extra_configs or {},
            producer_extra=producer_extra_configs or {}
        )
