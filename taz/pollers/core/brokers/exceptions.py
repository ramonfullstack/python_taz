class DataNotSentError(Exception):
    """
    This class must be raised when any exception
    happens inside Broker execution.
    """


class MissingPollerSettingException(Exception):
    """
    This class must be raise whenever a setting is missing
    inside poller context.
    """
