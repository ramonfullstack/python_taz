from simple_settings import settings
from slugify import slugify


def build_media(
    sku,
    title,
    reference,
    seller_id,
    media_type,
    items,
    force_path=False
):
    built_items = []
    for item in items:
        if media_type == 'images':
            path = settings.IMAGES_PATH.format(
                slug=slugify('{} - {}'.format(title, reference)),
                seller_id=seller_id,
                sku=slugify(sku),
                filename=(
                    item
                    if not isinstance(item, dict)
                    else '{}.jpg'.format(item['hash'])
                )
            )

            if force_path:
                built_items.append('{domain}{path}'.format(
                    domain=settings.ACME_MEDIA_DOMAIN,
                    path=path
                ))
            else:
                built_items.append(path)
        elif media_type == 'videos':
            built_items.append(item)
        else:
            path = settings.AUDIOS_VIDEOS_PODCASTS_PATH.format(
                seller_id=seller_id,
                media_type=media_type,
                sku=slugify(sku),
                filename=item
            )

            if force_path:
                built_items.append('{domain}{path}'.format(
                    domain=settings.ACME_MEDIA_DOMAIN,
                    path=path
                ))
            else:
                built_items.append(path)

    return built_items


def build_url_image(image):
    return '{domain}{path}'.format(
        domain=settings.ACME_MEDIA_DOMAIN,
        path=image.format(
            w=600,
            h=400
        )
    )


def _build_images(
    product,
    medias_collection,
    width=600,
    height=400
):
    medias = medias_collection.find_one(
        {
            'sku': product['sku'],
            'seller_id': product['seller_id']
        },
        {
            'images': 1,
            '_id': 0
        }
    )

    if not medias:
        return []

    images = build_media(
        sku=product['sku'],
        seller_id=product['seller_id'],
        title=product['title'],
        reference=product.get('reference') or '',
        media_type='images',
        items=medias['images']
    )

    return [
        '{domain}{path}'.format(
            domain=settings.ACME_MEDIA_DOMAIN,
            path=image.format(
                w=width,
                h=height
            )
        ) for image in images
    ]
