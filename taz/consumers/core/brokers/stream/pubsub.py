import abc
import time
from threading import Thread

from maaslogger import base_logger
from marshmallow import INCLUDE
from simple_settings import settings

from taz.consumers.core.brokers.base import BaseBroker
from taz.consumers.core.exceptions import (
    RequiredFieldException,
    RequiredNonEmptyFieldException
)
from taz.consumers.core.google.stream import (
    PubSubSubscriber,
    PubSubSubscriberRawEvent
)

logger = base_logger.get_logger(__name__)

ACKNOWLEDGE: bool = True


class PubSubRecordProcessor:

    def __init__(self, scope):
        self.scope = scope

    def run_as_thread(self, message):  # pragma: no cover
        thread = Thread(
            target=self.process_message, args=(message,)
        )
        thread.start()
        thread.join()

    @abc.abstractmethod
    def process_message(self, message):
        return


class PubSubRecordProcessorValidateSchema(PubSubRecordProcessor):
    schema_class = None

    def __init__(self, scope):
        super().__init__(scope)
        self.schema_instance = self.get_schema_instance()

    def get_schema_instance(self):
        if self.schema_class:
            return self.schema_class(unknown=INCLUDE)

    def run_as_thread(self, message):  # pragma: no cover
        thread = Thread(
            target=self.validate_process_message, args=(message,)
        )
        thread.start()
        thread.join()

    def validate_process_message(self, message):
        if self.schema_instance:
            logger.debug('Validating message {}'.format(message))

            errors = self.schema_instance.validate(message)
            if errors:
                logger.error(
                    'Invalid message "{}" received from queue. '
                    'Errors: {}'.format(message, errors)
                )
                return True

        return self.process_message(message)


class PubSubRecordProcessorWithRequiredFields(PubSubRecordProcessor):
    required_fields = []
    required_fields_create = []
    required_fields_update = []
    required_fields_delete = []

    required_non_empty_fields = []
    required_non_empty_fields_create = []
    required_non_empty_fields_update = []
    required_non_empty_fields_delete = []

    def __init__(self, scope, *args, **kwargs):
        super().__init__(scope)

    @abc.abstractmethod
    def _create(self, data):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _update(self, data):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _delete(self, data):  # pragma: no cover
        pass

    def create(self, data):
        self._validations(data, 'create')
        return self._create(data)

    def update(self, data):
        self._validations(data, 'update')
        self._update(data)

    def delete(self, data):
        self._validations(data, 'delete')
        return self._delete(data)

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

    def process_message(self, message):
        try:
            action = message.get('action')
            data = message.get('data')
            if not data or not action:
                logger.error(
                    'Invalid data for scope: {scope}: {data}'.format(
                        scope=self.scope,
                        data=data
                    ),
                    detail={
                        "scope": self.scope,
                        "data": data
                    }
                )
                return

            if action not in ['create', 'update', 'remove', 'delete']:
                logger.warning(
                    'Unknow action {action} for scope {scope} '
                    'with data: {data}'.format(
                        action=action,
                        scope=self.scope,
                        data=data
                    ),
                    detail={
                        "scope": self.scope,
                        "data": data,
                        "action": action
                    }
                )
                return False

            logger.info(
                'Processing action:{action} for scope:{scope} '
                'with data:{data}'.format(
                    action=action,
                    scope=self.scope,
                    data=data
                ),
                detail={
                    "scope": self.scope,
                    "data": data,
                    "action": action
                }
            )
            return getattr(self, action)(data)
        except Exception as e:
            logger.warning(
                'Encountered a generic error: {error} scope: {scope} '
                'parsing data with message: {message}'.format(
                    error=e,
                    scope=self.scope,
                    message=message
                ),
                detail={
                    "scope": self.scope,
                    "message": message,
                    "error": e
                }
            )
            raise e


class PubSubBroker(BaseBroker):
    @abc.abstractmethod
    def project_name(self):  # pragma: no cover
        pass

    def __init__(self):
        processor = self.record_processor_class(self.scope)
        self.subscription_name = getattr(
            self,
            'subscription_name',
            settings.PUBSUB_SUBSCRIPTION_ID
        )
        if not self.subscription_name:
            raise AttributeError('Invalid subscription name')

        self.project_id = getattr(
            self, 'project_id', settings.GOOGLE_PROJECT_ID
        )
        self.subscribe()

        try:
            self.subscriber.subscribe(
                handler_function=processor.process_message,
                max_messages=settings.SUBSCRIBER_MAX_MESSAGES
            )

            logger.info(
                'Listening pubsub on subscription {}'.format(self.scope)
            )
        except Exception as e:
            logger.error(
                'Error listening pubsub on subscription {scope} '
                'error:{error}. Restarting it'.format(
                    scope=self.scope,
                    error=e
                )
            )

            raise

    def subscribe(self):
        self.subscriber = PubSubSubscriber(
            project_id=self.project_id,
            subscription_name=self.subscription_name
        )

    @classmethod
    def start(cls):
        time.sleep(1)

    @property
    def record_processor_class(self):
        raise NotImplementedError(  # pragma: no cover
            'You need to specify the `StreamRecordProcessor` class in '
            '`record_process_class` attribute of `StreamBroker`'
        )


class PubSubBrokerRawEvent(PubSubBroker):
    def subscribe(self):
        self.subscriber = PubSubSubscriberRawEvent(
            project_id=self.project_id,
            subscription_name=self.subscription_name
        )
