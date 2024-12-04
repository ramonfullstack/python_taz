from datetime import datetime

from dateutil.parser import parse
from pytz import UTC


def convert_str_to_datetime(value):
    if not value:
        return datetime.now(UTC)
    if isinstance(value, str):
        value = parse(value)

    if value.tzinfo is None:
        value = UTC.localize(value)
    return value.astimezone(UTC)
