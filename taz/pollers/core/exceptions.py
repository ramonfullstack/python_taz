class ConverterException(Exception):
    pass


class MalformedObjectException(Exception):
    pass


class DatabaseException(Exception):
    pass


class SendRecordsException(Exception):
    pass


class UrlNotProvided(ValueError):
    pass


class PollerCircuitBreaker(Exception):
    pass
