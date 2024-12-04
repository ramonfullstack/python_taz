import abc
import logging

from simple_settings import settings

from taz.helpers.gchat import GchatNotification

logger = logging.getLogger(__name__)


class CronBase:

    @abc.abstractmethod
    def run(self):
        """Run cron"""

    @abc.abstractproperty
    def cron_name(self):
        """Defines the cron name"""

    @abc.abstractproperty
    def skip_notification(self):
        """Defines the cron name"""

    def start(self):
        gchat = GchatNotification(self.skip_notification)

        if bool(settings.CRON_STOP):
            logger.warning('CRON_STOP=True, the cron is stopped')

            text = f'Cron *{self.cron_name}* stopped'
            gchat.send(text)

            return

        try:
            self.run()
        except Exception as e:
            logger.error(
                f'An error occurred to run cron:{self.cron_name} error:{e}'
            )

            text = f'An error occurred to run cron:{self.cron_name} error:{e}'

            gchat.send(text)

            raise
