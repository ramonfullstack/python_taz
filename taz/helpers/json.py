import json
import logging
from datetime import datetime
from decimal import Decimal

from bson import ObjectId

logger = logging.getLogger(__name__)


class JsonEncoder(json.JSONEncoder):
    """
    Default JSON encoder to be used in the whole project.
    """
    def default(self, o):
        if isinstance(o, Decimal):
            f = float(o)
            logger.debug(
                'Encoding Decimal:{} to float:{}'.format(o, f)
            )
            return f
        elif isinstance(o, ObjectId):
            return str(o)
        return super().default(o)


class JsonDecoder(json.JSONDecoder):
    """
    Default JSON encoder to be used in the whole project.
    """

    def __init__(self, *args, **kwargs):
        kwargs.update({'parse_float': self.parse_float})
        super().__init__(*args, **kwargs)

    def parse_float(self, o):
        d = Decimal(str(o))
        logger.debug(
            'Decoding float:{} to Decimal:{}'.format(o, d)
        )
        return d


def json_dumps(buf, ensure_ascii=True, sort_keys=False):
    return json.dumps(
        buf,
        cls=JsonEncoder,
        ensure_ascii=ensure_ascii,
        sort_keys=sort_keys
    )


def json_loads(buf):
    _buf = buf
    if isinstance(buf, bytes):
        _buf = buf.decode('utf-8')
    return json.loads(
        _buf,
        cls=JsonDecoder
    )


def strip_decimals(o):
    if isinstance(o, Decimal):
        return float(o)
    elif isinstance(o, (list, tuple)):
        return [strip_decimals(i) for i in o]
    elif isinstance(o, dict):
        return {k: strip_decimals(v) for k, v in o.items()}
    elif isinstance(o, datetime):
        return o.isoformat()
    else:
        return o
