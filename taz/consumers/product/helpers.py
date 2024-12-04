from collections import OrderedDict
from datetime import datetime
from typing import Dict, List, Optional

from taz.constants import (
    MAGAZINE_LUIZA_SELLER_ID,
    UPDATE_ACTION,
    VOLTAGE_VALUES
)
from taz.helpers.html import clean_html_string, fix_broken_tags
from taz.helpers.isbn import validate_isbn


class ProductHelpers:

    @staticmethod
    def normalize_voltage(product: Dict) -> None:
        for attribute in product.get('attributes') or []:
            if attribute['type'] != 'voltage':
                continue

            attribute['value'] = (
                VOLTAGE_VALUES.get(attribute['value'].lower()) or
                attribute['value']
            )

    @staticmethod
    def capitalize_fields(product: Dict) -> None:
        if (
            product['seller_id'] != MAGAZINE_LUIZA_SELLER_ID and
            product['title'].isupper()
        ):
            product['title'] = product['title'].capitalize()

    @staticmethod
    def format_reference(product: Dict) -> None:
        if product['seller_id'] == MAGAZINE_LUIZA_SELLER_ID:
            return

        if product['brand'].lower() not in product['title'].lower():
            product['reference'] = product['brand']
        else:
            product['reference'] = ''

    @staticmethod
    def clean_ean_whitespace(product: Dict) -> None:
        product['ean'] = product.get('ean', '').replace(' ', '')

    @staticmethod
    def merge_categories(product: Dict) -> List:
        if 'main_category' not in product:
            return product['categories']

        main_category = product['main_category']

        categories = OrderedDict({
            main_category['id']: [main_category['subcategory']['id']]
        })

        for category in product['categories']:
            for subcategory in category['subcategories']:
                if category['id'] not in categories:
                    categories[category['id']] = []

                if subcategory['id'] in categories[category['id']]:
                    continue

                categories[category['id']].append(subcategory['id'])

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

    @staticmethod
    def get_full_title(product: Dict) -> str:
        full_title = product['title']

        if product.get('reference'):
            full_title += ' - {}'.format(product['reference'])

        return full_title

    @staticmethod
    def convert_product_active(product: Dict, seller_info: Dict) -> bool:
        if not product or not seller_info:
            return False

        if 'active' in product:
            return not product.get('active')

        return not seller_info['is_active']

    @staticmethod
    def normalize_isbn(product: Dict) -> None:
        value = product.get('ean')

        if validate_isbn(value):
            product['isbn'] = value

    @staticmethod
    def clear_html(text: str, tags=None, empty=None) -> str:
        text = fix_broken_tags(text)
        text = clean_html_string(text, tags, empty)
        return text

    @staticmethod
    def get_seller_description(
        seller_id: str,
        seller_info: Dict
    ) -> str:
        return (
            seller_info.get('name') or
            seller_id
        )

    @staticmethod
    def extract_categorization(
        product: dict,
        action: str
    ) -> Optional[dict]:
        if (
            action == UPDATE_ACTION and
            product['seller_id'] != MAGAZINE_LUIZA_SELLER_ID and
            'categories' in product
        ):
            return {
                'categories': product.pop('categories', None),
                'main_category': product.pop('main_category', None)
            }

        return None

    @staticmethod
    def format_payload_product(
        decoded_product: Dict,
        seller_info: Dict,
        grade: int,
        navigation_id: str,
        matching_strategy: str,
        md5: str
    ) -> Dict:
        return {
            'disable_on_matching': ProductHelpers.convert_product_active(
                product=decoded_product,
                seller_info=seller_info
            ),
            'categories': ProductHelpers.merge_categories(decoded_product),
            'offer_title': ProductHelpers.get_full_title(decoded_product),
            'grade': grade,
            'navigation_id': navigation_id,
            'matching_strategy': matching_strategy,
            'md5': md5,
            'last_updated_at': datetime.utcnow().isoformat(),
            'seller_description': ProductHelpers.get_seller_description(
                seller_id=decoded_product['seller_id'],
                seller_info=seller_info
            )
        }
