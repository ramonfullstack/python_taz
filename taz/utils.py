import hashlib
import logging
import math
import random
import re
import unicodedata
from collections.abc import Sequence
from datetime import date, datetime
from decimal import Decimal
from uuid import uuid4

from simple_settings import settings

from taz import constants
from taz.helpers.json import json_dumps

logger = logging.getLogger(__name__)


def date_to_timestamp(d):
    if not isinstance(d, datetime):
        raise ValueError('Parameter provided is not a datetime')
    return int(date.strftime(d, '%s'))


def clean_invalid_characters(text):
    return ''.join(
        c for c in text
        if c.isalnum() or c in settings.ALLOWED_NON_ALPHANUMERIC_CHARACTERES
    )


def clean_invalid_characters_from_dict(d):
    for key, value in d.items():
        if isinstance(value, str):
            d[key] = clean_invalid_characters(value)
        elif isinstance(value, dict):
            d[key] = clean_invalid_characters_from_dict(value)
        elif isinstance(value, Sequence):
            d[key] = clean_invalid_characters_from_sequence(value)
    return d


def clean_invalid_characters_from_sequence(sequence):
    result = []
    for i in sequence:
        if isinstance(i, str):
            result.append(clean_invalid_characters(i))
        elif isinstance(i, dict):
            result.append(clean_invalid_characters_from_dict(i))
        elif isinstance(i, Sequence):
            result.append(clean_invalid_characters_from_sequence(i))
        else:
            result.append(i)
    return result


def tryint(text):
    return int(text) if text.isdigit() else text


def alphanum_key(text):
    return [tryint(c) for c in re.split('(\\d+)', text)]


def sort_nicely(_list):
    return sorted(_list, key=alphanum_key)


def md5(payload: dict, old_md5=None):
    new_payload = payload.copy()

    fields = (
        'updated_at',
        'created_at',
        'last_updated_at',
        'md5',
        '_id',
        'release_date',
        'tracking_id',
        'timestamp'
    )

    for f in fields:
        new_payload.pop(f, None)

    new_md5 = hashlib.md5(
        json_dumps(
            sorted(new_payload.items()),
            sort_keys=True
        ).encode('utf-8')
    ).hexdigest()

    logger.debug(f'old_md5:{old_md5} new_md5:{new_md5} payload={payload}')
    return new_md5


def spaceless(text):
    if not isinstance(text, str):
        return text

    spaceless = text.strip()
    return spaceless.replace(' ', '_')


def diacriticless(text, preserve_case=False):
    if not isinstance(text, str):
        return text

    diacriticless = unicodedata.normalize(
        'NFKD', text
    ).encode('ASCII', 'ignore').decode('ASCII')

    if not preserve_case:
        diacriticless = diacriticless.lower()

    return diacriticless


def decode_body(data):
    decoded_body = {}
    for k, v in _unpack(data):
        if isinstance(v, Decimal):
            decoded_body[k] = float(v)
        elif isinstance(v, dict):
            decoded_body[k] = decode_body(v)
        else:
            decoded_body[k] = v
    return decoded_body


def _unpack(data):
    if isinstance(data, dict):
        return data.items()
    return data


def generate_random_id():
    return str(random.randint(0, 9))


def cut_product_id(_id):
    return _id[:7] if _id.isdigit() else _id


def convert_id_to_nine_digits(_id):
    if _id.isdigit():
        return _id.ljust(9, '0')
    return _id


def valid_ean(ean):
    if not ean or not str(ean).isdigit() or int(ean) == 0:
        return False

    return extract_validation_digit(ean[0:-1]) == ean[-1]


def format_ean(ean: str) -> str:
    return ean.rjust(13, '0')


def extract_validation_digit(b):
    s = 0
    for x, c in enumerate(b[::-1]):
        if (x + 1) % 2:
            s += int(c) * 3
        else:
            s += int(c)
    return str(int(math.ceil(s / 10.0) * 10) - s)


def normalize_voltage(value):
    return constants.VOLTAGE_VALUES.get(value.lower()) or value


def get_identifier(raw_product: dict) -> str:
    return raw_product.get('isbn') or raw_product['ean']


def generate_uuid() -> str:
    return str(uuid4())
