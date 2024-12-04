import logging
import re

from simple_settings import settings
from slugify import slugify

logger = logging.getLogger(__name__)


def generate_product_url(
    product_id,
    variation,
    categories,
    persist_changes=False
):
    if not categories:
        logger.warning(
            'Product without categories for generated url '
            f'product:{product_id} persist_changes:{persist_changes}'
        )
        return ''

    title_slug = slugify(variation['title'])
    reference_slug = slugify(variation.get('reference') or '')
    main_category = categories[0]

    full_title = '{title}-{reference}'.format(
        title=title_slug,
        reference=reference_slug
    ).strip('-')

    subcategories = main_category.get('subcategories', [])
    subcategory = (
        subcategories[0]['id']
        if len(subcategories) > 0
        else settings.FALLBACK_MISSING_SUBCATEGORY
    )

    return '{full_title}/p/{id}/{category}/{subcategory}/'.format(
        full_title=full_title,
        id=product_id,
        category=main_category['id'],
        subcategory=slugify(subcategory),
    ).lower()


def get_variation_url(product, navigation_id) -> str:
    for variation in product.get('variations', []):
        if variation['id'] != navigation_id:
            continue
        return '{host}/{path}'.format(
            host=settings.BASE_DESKTOP_URL,
            path=variation['url']
        )
    return ''


def remove_url_param(url, param_name) -> str:
    regex = r'(?=' + param_name + ')[^&]*'
    removed_param_name = re.sub(regex, '', url)
    removed_concat_symbols = re.sub(r'\?&', '?', removed_param_name)
    removed_duplicated_concat = re.sub(r'&&', '&', removed_concat_symbols)
    removed_tail_symbol = re.sub(r'\?$|&$', '', removed_duplicated_concat)
    return removed_tail_symbol
