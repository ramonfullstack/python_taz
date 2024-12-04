import abc


class DataStorageBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def fetch(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def is_batch(self):  # pragma: no cover
        pass

    def shutdown(self):  # pragma: no cover
        pass
