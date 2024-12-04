import uuid
from typing import Dict, List

from simple_settings import settings

from taz.constants import SOURCE_METABOOKS


def _get_token(resource_content_type: str) -> str:
    token = settings.METABOOKS_COVER_TOKEN
    if resource_content_type != '01':
        token = settings.METABOOKS_MMO_TOKEN
    return token


def _get_url(
    resource_content_type: str,
    url: str,
    token: str
) -> str:
    if resource_content_type == '01':
        url = url.replace('/m', '')

    return f'{url}?access_token={token}'


def _get_metabooks_images(payload: Dict) -> List:
    images = []

    resources = payload.get('supportingResources') or []
    for resource in sorted(
        resources,
        key=lambda r:
        int(r['resourceContentType'])
    ):
        if resource['resourceMode'] != '03':
            continue

        resource_content_type = resource['resourceContentType']

        token = _get_token(resource_content_type)

        url = _get_url(
            resource_content_type,
            resource['exportedLink'],
            token
        )

        _hash = resource.get('md5Hash') or str(uuid.uuid4())

        images.append({
            'filename': (
                resource.get('filename') or '{}.jpg'.format(_hash)
            ),
            'url': url,
            'hash': _hash.replace('-', '')
        })

    return images


def _get_taz_payload_images(payload: Dict) -> List:
    images = payload.get('medias', {}).get('images', [])

    formatted_images = []

    for image in images:
        filename = image.strip().split('/')[-1]
        splitted_filename = filename.split('.')

        _hash = (
            filename
            if len(splitted_filename) < 2
            else splitted_filename[0]
        )

        formatted_images.append({
            'filename': filename,
            'url': image,
            'hash': _hash
        })

    return formatted_images


def _get_images(
    payload: Dict,
    source: str
) -> List:
    return (
        _get_metabooks_images(payload)
        if source == SOURCE_METABOOKS
        else _get_taz_payload_images(payload)
    )


def _create_image_payload(
    images: List,
    identified: str,
    source: str
) -> List[Dict]:
    payload = []
    for image in images:
        image_url = settings.METADATA_IMAGE_URL.format(
            bucket=settings.METADATA_IMAGE_BUCKET,
            source=source,
            identified=identified,
            filename=image['filename']
        )

        payload.append({
            'hash': image['hash'],
            'url': image_url
        })

    return payload
