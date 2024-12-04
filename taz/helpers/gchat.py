import json
import logging

import requests
from simple_settings import settings

logger = logging.getLogger(__name__)


class GchatNotification:
    def __init__(self, skip_notifications=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.skip_notifications = skip_notifications
        self.url = settings.CHANNEL_GCHAT

    def send(self, text):
        if self.skip_notifications:
            logger.warning('Notification turned off for gchat')
            return

        logger.info('Send gchat notification with url {}'.format(self.url))
        if self.url:
            headers = {"Content-Type": "application/json; charset=UTF-8"}
            app_message = {"text": "{}".format(text)}
            response = requests.post(
                url=self.url,
                headers=headers,
                data=json.dumps(app_message),
            )
            response.raise_for_status()
            logger.info('Send gchat notification with payload:{}'.format(text))
