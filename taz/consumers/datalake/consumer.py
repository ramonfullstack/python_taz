import importlib
import time

from maaslogger import base_logger
from simple_settings import settings

from taz.constants import NIAGARA, TETRIX
from taz.consumers.core.brokers.stream import (
    PubSubBroker,
    PubSubRecordProcessor
)
from taz.consumers.core.exceptions import InvalidScope
from taz.consumers.datalake.publish_datalake_context import (
    KafkaTetrix,
    PublishDatalakeContext,
    PubsubNiagara
)

logger = base_logger.get_logger(__name__)

SCOPE = 'datalake'


class DataLakeProcessor(PubSubRecordProcessor):

    scope = SCOPE
    max_process_workers = settings.DATALAKE_PROCESS_WORKERS
    disable_cache_lock = True
    STREAMS = [NIAGARA, TETRIX]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__niagara = PublishDatalakeContext(PubsubNiagara())
        self.__tetrix = PublishDatalakeContext(KafkaTetrix())
        self.__context_stream = {
            NIAGARA: self.__niagara,
            TETRIX: self.__tetrix
        }

    def process_message(self, message):
        sku, seller_id, navigation_id, scope_name, action, source = (
            message['sku'],
            message['seller_id'],
            message['navigation_id'],
            message['type'],
            message.get('action'),
            message.get('source')
        )

        try:
            scope = self._get_scope(scope_name).Scope(
                seller_id=seller_id,
                sku=sku,
                navigation_id=navigation_id,
                action=action,
                source=source
            )

            payload = scope.get_data()

            payloads = (
                [payload]
                if not isinstance(payload, list)
                else payload
            )

            for payload in payloads:
                if not payload:
                    continue

                scope_name = payload.get('scope_name') or scope.name
                start = time.time()

                for stream in self.STREAMS:
                    stream_config = settings.DATALAKE[scope_name].get(stream)

                    if stream_config and stream_config['enabled']:
                        context_stream = self.__context_stream.get(stream)
                        data = context_stream.format_payload(
                            message=payload,
                            scope_name=scope_name
                        )
                        context_stream.send_message(data, stream_config)
                        message = (
                            f'Successfully sent sku:{sku} '
                            f'seller_id:{seller_id} '
                            f'navigation_id:{navigation_id}'
                            f'with scope {scope_name} '
                            f'to Datalake stream:{stream} in '
                            f'{time.time() - start} seconds'
                        )
                        logger.info(
                            message,
                            detail={
                                "sku": sku,
                                "seller_id": seller_id,
                                "navigation_id": navigation_id,
                                "scope_name": scope_name,
                                "stream": stream
                            }
                        )
        except Exception as error:
            logger.error(
                f'Error sending data to datalake '
                f'sku:{sku} seller_id:{seller_id} with scope:{scope_name} '
                f'error:{error} message:{message}',
                detail={
                    "sku": sku,
                    "seller_id": seller_id,
                    "scope_name": scope_name,
                    "message": message
                }
            )
            return False

        return True

    @staticmethod
    def _get_scope(scope_name):
        try:
            scope = f'taz.consumers.datalake.scopes.{scope_name}'
            return importlib.import_module(scope)
        except Exception:
            raise InvalidScope(scope_name=scope_name)


class DataLakeConsumer(PubSubBroker):
    scope = SCOPE
    record_processor_class = DataLakeProcessor
    project_name = settings.GOOGLE_PROJECT_ID
