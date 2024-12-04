from datetime import datetime

from taz.api.common.models.validations import convert_str_to_datetime


def create_converted_payload(payload):
    if payload.get('created_at'):
        payload['created_at'] = convert_str_to_datetime(
            datetime.fromtimestamp(
                payload['created_at']['$date'] / 1000
            )
        )

    if payload.get('updated_at'):
        payload['updated_at'] = convert_str_to_datetime(
            datetime.fromtimestamp(
                payload['updated_at']['$date'] / 1000
            )
        )

    return payload


def convert_validation_errors(err):
    detail = {}
    errors = dict(err.errors.items())
    keys = errors.keys()
    for key in keys:
        detail[key] = errors[key].message
    return detail
