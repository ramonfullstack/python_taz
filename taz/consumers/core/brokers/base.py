import abc
import time

from maaslogger import base_logger

logger = base_logger.get_logger(__name__)


class BaseBroker(metaclass=abc.ABCMeta):
    """
    Every consumer broker must inherit from this class
    """

    run_in_loop = False
    halt_requested = False

    @property
    @abc.abstractmethod
    def scope(self):
        """
        This property define the scope of consumer
        """

    @abc.abstractmethod
    def start(self):
        """
        This method is usefully to start consumer and
        define your context
        """

    def stop(self):  # pragma: no cover
        self.halt_requested = True


def log_processing_status(
    log,
    scope,
    status,
    global_started_at,
    local_started_at
):
    log(
        'Processed message from scope:{scope} with status:{status} and '
        'ages global_age:{global_age} local_age:{local_age}'.format(
            scope=scope,
            status=status.value,
            global_age=time.time() - float(global_started_at),
            local_age=time.time() - float(local_started_at)
        )
    )
