from decimal import Decimal


def decode_body(data):
    decoded_body = {}
    for k, v in _unpack(data):
        if isinstance(v, Decimal):
            decoded_body[k] = str(v)
        else:
            decoded_body[k] = v
    return decoded_body


def _unpack(data):
    if isinstance(data, dict):
        return data.items()
    return data
