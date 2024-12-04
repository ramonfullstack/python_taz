import logging
from collections import OrderedDict
from datetime import datetime
from enum import Enum

from taz.constants import (
    MAGAZINE_LUIZA_SELLER_DESCRIPTION,
    MAGAZINE_LUIZA_SELLER_ID,
    ProductSpecification
)
from taz.pollers.core.data.converter import BaseConverter

logger = logging.getLogger(__name__)


class ProductType(Enum):
    product = 1
    bundle = 2
    gift = 3


class ProductConverter(BaseConverter):
    def _add_item(self, raw):
        item = {
            'ean': self.get_ean_from_response(raw),
            'main_variation': bool(raw['main_variation']),
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'seller_description': MAGAZINE_LUIZA_SELLER_DESCRIPTION,
            'sku': raw['sku'],
            'type': ProductType(raw['product_type']).name,
            'title': raw['title'],
            'description': raw['description'] or '',
            'reference': raw['reference'],
            'brand': raw['brand'],
            'sold_count': int(raw['sold_count']),
            'review_count': int(raw['review_count']),
            'review_score': float(raw['review_score']),
            'categories': self._create_categories(raw),
            'dimensions': {
                'width': float('{:.3f}'.format(raw['width'])),
                'depth': float('{:.3f}'.format(raw['depth'])),
                'weight': float('{:.3f}'.format(raw['weight'])),
                'height': float('{:.3f}'.format(raw['height']))
            },
            'created_at': raw['created_at'].isoformat(),
        }

        main_category = {
            'id': raw['category_id'],
            'subcategory': {'id': raw['subcategory_id']}
        }
        item['main_category'] = main_category

        attributes = self._create_attributes(raw)
        if attributes:
            item['attributes'] = attributes

        selections = self._create_selections(raw)
        if selections:
            item['selections'] = selections

        if raw['parent_sku']:
            item['parent_sku'] = raw['parent_sku']

        release_date = raw['release_date']
        if release_date and isinstance(release_date, datetime):
            item['release_date'] = release_date.isoformat()

        updated_at = raw['updated_at']
        if updated_at and isinstance(updated_at, datetime):
            item['updated_at'] = updated_at.isoformat()

        bundles = self._create_bundles(raw)
        if bundles:
            item['bundles'] = bundles

        if raw.get('gift_product'):
            item['gift_product'] = raw['gift_product']

        item['active'] = (
            str(raw['active']).lower().strip() in ('1', 'true')
        )
        self.items.setdefault(raw['batch_key'], {}).update({item['sku']: item})

    def _create_bundles(self, raw):
        bundles = (
            raw['bundles'].split('|')
            if raw.get('bundles') else []
        )

        results = {}
        for bundle in bundles:
            code, model, price, quantity = bundle.split(';')

            result = {
                'price': price,
                'quantity': int(quantity)
            }

            results[code + model] = result

        return results

    def _create_selections(self, raw):
        selections = (
            raw['selections'].split('|')
            if raw.get('selections') else []
        )

        result = {}
        for selection in selections:
            partner_id, selection_id = selection.split(';')
            if partner_id not in result:
                result[partner_id] = []
            result[partner_id].append(selection_id)

        return result

    def _create_categories(self, raw):
        categories = OrderedDict(
            {raw['category_id']: [raw['subcategory_id']]}
        )

        extra_categories = (
            raw['extra_categories'].split('|')
            if raw.get('extra_categories') else []
        )

        for extra_category in extra_categories:
            cat_id, sub_id = extra_category.split(';')
            if cat_id not in categories:
                categories[cat_id] = []
            categories[cat_id].append(sub_id)

        return [
            {
                'id': category_id,
                'subcategories': [
                    {'id': subcategory_id}
                    for subcategory_id in subcategories
                ]
            }
            for category_id, subcategories in categories.items()
        ]

    def _create_attributes(self, raw):
        attributes = (
            (
                raw['voltage'],
                ProductSpecification.voltage,
            ),
            (
                raw['color'],
                ProductSpecification.color,
            ),
        )

        if raw['specification_id'] and raw['specification_description']:
            attributes += (
                (
                    raw['specification_description'],
                    ProductSpecification.get_by_id(raw['specification_id'])
                ),
            )

        attributes = [
            {
                'type': attribute.name,
                'value': value
            }
            for value, attribute in set(attributes)
            if value and value.strip()
        ]

        return sorted(attributes, key=lambda a: a['type'])

    @staticmethod
    def get_ean_from_response(raw):
        ean = raw.get('ean', '')

        if not ean or not str(ean).isdigit():
            return ''

        return str(ean).zfill(13)

    def from_source(self, data):
        for item in data:
            logger.debug(
                'Converting data for sku:{sku} active:{active} '
                'parent_sku:{parent_sku} attributes:{attributes} '
                'bundles:{bundles} selections:{selections}'.format(
                    sku=item['sku'],
                    active=item['active'],
                    parent_sku=item['parent_sku'],
                    attributes=item.get('attributes'),
                    bundles=item.get('bundles'),
                    selections=item.get('selections')
                )
            )

            self._add_item(item)
