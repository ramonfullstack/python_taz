import logging

import requests

from .json import json_dumps

logger = logging.getLogger(__name__)


class SlackNotification:
    def __init__(self, skip_notifications=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.skip_notifications = skip_notifications

    def send(self, channel, text, webhook, icon_url=None, username=None):
        if self.skip_notifications:
            logger.warning('Notification turned off for slack')
            return

        payload = {'channel': channel, 'text': text}

        if icon_url:
            payload.update({'icon_url': icon_url})

        if username:
            payload.update({'username': username})

        response = requests.post(webhook, data=json_dumps(payload))
        response.raise_for_status()

        logger.info('Send slack notification with payload:{}'.format(payload))
