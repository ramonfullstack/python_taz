import logging

import sentry_sdk
from sentry_sdk.integrations.falcon import FalconIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

logger = logging.getLogger(__name__)


def setup_sentry(dsn):  # pragma: no cover
    sentry_logging = LoggingIntegration(
        level=logging.INFO,
        event_level=logging.ERROR,
    )

    try:
        sentry_sdk.init(
            dsn=dsn,
            integrations=[
                FalconIntegration(),
                sentry_logging
            ]
        )
        logger.info('Sentry started with success')
    except Exception as e:
        logger.error('Error starting sentry: {error}').format(error=e)
