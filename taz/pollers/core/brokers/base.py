import abc


class BaseBroker(metaclass=abc.ABCMeta):
    """
    Every message broker must inherit from this class
    """

    @abc.abstractmethod
    def put_many(self, action, dataset):  # pragma: no cover
        return

    @abc.abstractmethod
    def shutdown(self):  # pragma: no cover
        return
