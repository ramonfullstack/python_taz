from taz.consumers.core.kafka.config import KafkaConfig


class TestKafkaConfig:

    def test_load_config_with_success(self):
        config = KafkaConfig.load(cluster_name='datalake')
        assert config.cluster_name == 'datalake'
        assert config.cluster_config == {'bootstrap.servers': 'localhost:9092'}
        assert config.consumer_extra == {}
        assert config.producer_extra == {}

    def test_process_to_dict_config_scope_producer_with_success(self):
        kafka_config = KafkaConfig.load(
            cluster_name='datalake',
            producer_extra_configs={
                'bootstrap.servers': 'localhost:9999',
                'test': '123'
            }
        )
        result = kafka_config.to_dict_config(producer=True)

        assert result == {
            'bootstrap.servers': 'localhost:9999',
            'test': '123'
        }

    def test_process_to_dict_config_scope_consumer_with_success(self):
        kafka_config = KafkaConfig.load(
            cluster_name='datalake',
            consumer_extra_configs={
                'session_timeout_ms': 10000
            }
        )
        result = kafka_config.to_dict_config(producer=False)

        assert result == {
            'bootstrap.servers': 'localhost:9092',
            'session_timeout_ms': 10000
        }
