import hashlib
import json

from taz import constants
from taz.core.score.weights import ScoreWeight


def create_payload(
    product,
    enriched_product,
    media,
    customer_behaviors,
    factsheet=None
):
    full_title = product['title']

    if product.get('reference'):
        full_title += ' - {}'.format(product['reference'])

    _delete_fields(product)
    payload = product

    payload.update({
        'entity': enriched_product['entity'],
        'full_title': full_title,
        'images_count': len(media.get('images') or []) or 0,
        'category_id': enriched_product['category_id'],
        'reviews_count': 0,
        'review_rating': 0,
        'active': True
    })

    if factsheet:
        attributes_count = 0
        for item in factsheet['items']:
            if item.get('slug') != 'ficha-tecnica':
                continue

            for elements in item['elements']:
                if (
                    elements.get('slug') and
                    'informacoes-complementares' in elements.get('slug')
                ):
                    continue

                attributes_count = __count_attributes(
                    elements,
                    attributes_count
                )

        payload.update({
            'factsheet_attributes_count': attributes_count
        })

    for customer_behavior in customer_behaviors:
        if customer_behavior['type'] == constants.META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT:  # noqa
            payload.update({'reviews_count': customer_behavior['value']})

        if customer_behavior['type'] == constants.META_TYPE_PRODUCT_AVERAGE_RATING:  # noqa
            payload.update({'review_rating': customer_behavior['value']})

    return payload


def _delete_fields(product):
    fields = ['review_count', 'review_score']
    for field in fields:
        if field in product:
            del product[field]


def generate_md5(payload):
    payload = json.dumps(payload, sort_keys=True)
    return hashlib.md5(payload.encode('utf-8')).hexdigest()


def get_weights_and_scores_by_criteria_and_entity(
    criteria_values,
    entity
):
    score_weight = ScoreWeight()
    weight_criterias = {}

    for criteria_value in criteria_values:
        criteria = criteria_value['criteria'].split('::')[0]

        weight = score_weight.get(entity_name=entity, criteria_name=criteria)

        weight_criterias[criteria] = {
            'weight': float(weight),
            'points': float(criteria_value['points']),
            'criteria': criteria_value['criteria'],
            'value': criteria_value['value']
        }

    return weight_criterias


def __count_attributes(elements, count):
    for element in elements.get('elements', []):
        if element.get('elements'):
            count = __count_attributes(element, count)
        else:
            count += 1
    return count
