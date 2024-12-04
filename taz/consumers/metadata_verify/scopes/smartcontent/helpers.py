from taz import constants


def create_factsheet_payload(sku, seller_id, metadata):
    return {
        'seller_id': seller_id,
        'sku': sku,
        'items': [
            item for item in [
                _create_special_content(metadata),
                _create_manual(metadata),
                _create_presentation(metadata),
                metadata.get('factsheet')
            ] if item is not None
        ]
    }


def _create_special_content(metadata):
    return {
        'display_name': 'Destaques',
        'slug': 'destaques',
        'elements': [
            {
                'key_name': 'Destaques',
                'slug': 'destaques',
                'elements': [
                    {
                        'value': metadata.get('special_content')
                    }
                ]
            }
        ]
    } if metadata.get('special_content') else None


def _create_manual(metadata):
    return {
        'display_name': 'Manual',
        'slug': 'manual',
        'elements': [
            {
                'key_name': 'Download do Manual',
                'slug': 'download-do-manual',
                'elements': [
                    {'value': '<p><a style=\"cursor: pointer; no-repeat scroll 0 0 transparent; display: block; height: 21px; width: 143px;\" title=\"Download Manual\" href=\"{manual}\" target=\"_blank\"> <img src=\"http://conteudoproduto.magazineluiza.com.br/manual/botao/botao_downloadmanual.gif\" alt=\"\" /> </a></p>'.format(manual=manual)} # noqa
                    for manual in metadata['medias']['manuals']
                ]
            }
        ]
    } if metadata.get('medias', {}).get('manuals') else None


def _create_presentation(metadata):
    return {
        'display_name': 'Apresentação',
        'slug': 'apresentacao',
        'elements': [
            {
                'key_name': 'Apresentação do produto',
                'slug': 'apresentacao-do-produto',
                'elements': [
                    {
                        'value': metadata.get('description')
                    }
                ]
            }
        ]
    } if metadata.get('description') else None


def create_media_payload(sku, seller_id, metadata):
    return {
        'seller_id': seller_id,
        'sku': sku,
        'images': dict((k, v) for k, v in metadata['medias'].items() if k != 'manuals') # noqa
    }


def create_enriched_product_payload(sku, seller_id, navigation_id, metadata):
    return {
        'seller_id': seller_id,
        'sku': sku,
        'navigation_id': navigation_id,
        'metadata': {
            item.get('display_name'):
            item.get('value')
            for item in metadata.get('attributes') or []
        },
        'title': metadata.get('title'),
        'description': metadata.get('description'),
        'source': constants.SOURCE_SMARTCONTENT,
        'entity': metadata.get('entity'),
        'brand': metadata.get('brand')
    }
