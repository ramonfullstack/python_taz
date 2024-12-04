from typing import Dict

from marshmallow import ValidationError

from taz.api.common.exceptions import BadRequest


def convert_fields_to_list(fields):
    if isinstance(fields, str):
        return [field.strip() for field in fields.split(',')]
    return fields or []


def format_fields_filtered(fields=None):
    fields = fields or []
    fields_formatted = {'_id': 0}

    for field in fields:
        fields_formatted.update({field.strip(): 1})

    return fields_formatted


def format_response_with_fields(fields, results):
    results_with_fields = [
        {
            field: result.get(field)
            for field in fields
        }
        for result in results['results']
    ]
    results.update({'results': results_with_fields})
    return results


def validate_schema(data: Dict, schema):
    try:
        return schema().load(data)
    except ValidationError as e:
        raise BadRequest(
            message=f'Invalid payload: {e}'
        )
