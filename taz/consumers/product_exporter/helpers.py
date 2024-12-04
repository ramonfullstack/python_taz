from typing import Dict

from maaslogger import base_logger
from simple_settings import settings

from taz.constants import (
    SOURCE_API_LUIZA_EXPRESS_DELIVERY,
    SOURCE_API_LUIZA_PICKUPSTORE,
    SOURCE_HECTOR,
    SOURCE_METABOOKS,
    SOURCE_OMNILOGIC,
    SOURCE_RECLASSIFICATION_PRICE_RULE,
    SOURCE_SMARTCONTENT,
    SOURCE_WAKKO
)
from taz.core.common.media import build_media
from taz.helpers.url import generate_product_url
from taz.utils import convert_id_to_nine_digits

logger = base_logger.get_logger(__name__)


def _get_product_url(product):
    try:
        return generate_product_url(
            convert_id_to_nine_digits(product['navigation_id']),
            {
                'title': product['title'],
                'reference': product['reference']
            },
            product['categories']
        )
    except Exception as e:
        logger.error(
            'Error in generate product URL for navigation_id:'
            '{navigation_id} and error:{error}'.format(
                navigation_id=product['navigation_id'],
                error=e
            )
        )


def _generate_factsheet_url(sku: str, seller_id: str):
    return f'{settings.FACTSHEET_DOMAIN}/{seller_id}/factsheet/{sku}.json'


def _create_enriched_payload(enriched_products: Dict):
    descriptives = {}
    deliveries = {}
    classifieds = {}
    normalized_filters = {}
    filters_metadata = []
    entity = ''

    for enriched_product in enriched_products:
        source = enriched_product['source']

        if source == SOURCE_RECLASSIFICATION_PRICE_RULE:
            entity = enriched_product.get('product_type') or entity

        if source == SOURCE_OMNILOGIC:
            metadata = enriched_product.get('metadata')

            if metadata:
                descriptives.update(metadata)

            filters_metadata = enriched_product.get('filters_metadata') or []
            entity = enriched_product.get('entity') or entity

        if source == SOURCE_WAKKO:
            metadata = enriched_product.get('metadata')

            if not metadata:
                continue

            descriptives.update(metadata.get('extracted') or {})
            descriptives.update(metadata.get('normalized') or {})
            classifieds.update(metadata.get('classified') or {})
            normalized_filters.update(metadata.get('normalized_filters') or {})

        if source == SOURCE_METABOOKS or source == SOURCE_SMARTCONTENT:
            metadata = enriched_product.get('metadata')
            if not metadata:
                continue

            descriptives.update(metadata)

        if source == SOURCE_API_LUIZA_EXPRESS_DELIVERY:
            deliveries.update({
                'Entrega rápida': enriched_product['delivery_days']
            })

        if source == SOURCE_API_LUIZA_PICKUPSTORE:
            deliveries.update({'Retira loja': 'true'})

        if source == SOURCE_HECTOR and not entity:
            entity = enriched_product.get(
                'classifications', [{}]
            )[0].get('product_type') or ''

    for key, value in descriptives.items():
        if not isinstance(value, list):
            descriptives[key] = [value]

    for key, value in deliveries.items():
        if not isinstance(value, list):
            deliveries[key] = [value]

    return {
        'metadata': {
            'descriptive': descriptives,
            'delivery': deliveries,
            'classified': classifieds,
            'normalized_filters': normalized_filters
        },
        'filters_metadata': filters_metadata,
        'entity': entity
    }


def build_images(sku, seller_id, title, reference, media):
    if media:
        medias = build_media(
            sku=sku,
            seller_id=seller_id,
            title=title,
            reference=reference,
            media_type='images',
            items=media
        )
    else:
        medias = build_media(
            **settings.UNAVAILABLE_IMAGE_OPTIONS
        )

    images = []
    for image in medias:
        images.append('{url}{image}'.format(
            url=settings.ACME_MEDIA_DOMAIN,
            image=image
        ))

    return images


def contains_fulfillment(payload):
    return isinstance(payload, dict) and payload.get('fulfillment') is not None
