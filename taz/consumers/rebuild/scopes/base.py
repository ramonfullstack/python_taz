import abc
import logging

from taz.consumers.core.google.stream import StreamPublisherManager

logger = logging.getLogger(__name__)


class BaseRebuild(metaclass=abc.ABCMeta):
    """
    Every rebuild consumer must inherit from this class
    """

    schema_class = None
    schema_data_many = False
    pubsub_manager = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema_instance = self.get_schema_instance()
        self.pubsub_manager = StreamPublisherManager()

    def rebuild(self, action, data):
        if self.schema_instance:
            errors = self.schema_instance.validate(
                data, many=self.schema_data_many
            )
            if errors:
                logger.error(
                    'Invalid data "{}" in rebuild. Errors: {}'
                    .format(data, errors)
                )
                return True

        return self._rebuild(action, data)

    def get_schema_instance(self):
        if self.schema_class:
            return self.schema_class()

    @abc.abstractmethod
    def _rebuild(self, action, data):
        """
        This method must contain the process of rebuild
        """


class BaseRebuildWithRawMessage(BaseRebuild):
    def rebuild(self, message, action, data):
        if self.schema_instance:
            errors = self.schema_instance.validate(
                data, many=self.schema_data_many
            )
            if errors:
                logger.error(
                    'Invalid data "{}" in rebuild. Errors: {}'
                    .format(data, errors)
                )
                return True

        return self._rebuild(message, action, data)
