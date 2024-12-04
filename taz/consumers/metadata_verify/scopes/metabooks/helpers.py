from taz import constants


def create_factsheet_payload(sku, seller_id, metadata):
    payload = {
        'seller_id': seller_id,
        'sku': sku,
        'items': [
            _create_factsheet_presentation(metadata),
            _create_factsheet_techsheet(metadata)
        ]
    }

    return payload


def _create_factsheet_presentation(metadata):
    return {
        'display_name': 'Apresentação',
        'elements': [{
            'key_name': 'Sinopse',
            'position': 2,
            'elements': [{
                'value': _get_description(metadata),
                'is_html': False
            }],
            'slug': 'sinopse'
        }],
        'slug': 'apresentacao',
        'position': 1
    }


def _create_factsheet_techsheet(metadata):
    return {
        'display_name': 'Ficha-Técnica',
        'elements': [
            _create_factsheet_informations(metadata),
            _create_factsheet_authors(metadata),
            _create_factsheet_more_informations(metadata),
            _create_factsheet_codes(metadata),
            _create_factsheet_product_weight(metadata),
            _create_factsheet_product_dimensions(metadata)
        ],
        'slug': 'ficha-tecnica',
        'position': 6
    }


def _create_factsheet_informations(metadata):
    payload = {
        'key_name': 'Informações técnicas',
        'position': 7,
        'elements': [{
            'slug': 'editora',
            'is_html': False,
            'key_name': 'Editora',
            'position': 8,
            'value': _get_publishers(metadata)
        }, {
            'slug': 'titulo',
            'is_html': False,
            'key_name': 'Título',
            'position': 10,
            'value': metadata['titles'][0]['title']
        }],
        'slug': 'informacoes-tecnicas'
    }

    subtitle = metadata['titles'][0].get('subtitle')
    if subtitle:
        payload['elements'].append({
            'slug': 'subtitulo',
            'is_html': False,
            'key_name': 'Subtítulo',
            'position': 10,
            'value': subtitle
        })

    return payload


def _create_factsheet_authors(metadata):
    return {
        'key_name': 'Autor',
        'position': 14,
        'elements': [{
            'value': _get_authors(metadata),
            'is_html': False
        }],
        'slug': 'autor'
    }


def _create_factsheet_more_informations(metadata):
    main_content_page_count = metadata.get(
        'extent', {}).get('mainContentPageCount')
    content_page_count = metadata.get(
        'extent', {}).get('contentPageCount')

    elements = [
        {
            'slug': 'edicao',
            'is_html': False,
            'key_name': 'Edição',
            'position': 23,
            'value': str(metadata.get('edition', {}).get('editionNumber'))
        },
        {
            'slug': 'data-de-publicacao',
            'is_html': False,
            'key_name': 'Data de publicação',
            'position': 24,
            'value': str(metadata.get('publicationDate'))
        },
        {
            'slug': 'idioma',
            'is_html': False,
            'key_name': 'Idioma',
            'position': 25,
            'value': _get_languages(metadata)
        }
    ]

    page_count = main_content_page_count or content_page_count

    if page_count is not None:

        elements.insert(0, {
            'slug': 'numero-de-paginas',
            'is_html': False,
            'key_name': 'Número de páginas',
            'position': 21,
            'value': str(page_count)
        })

    return {
        'key_name': 'Ficha técnica',
        'position': 18,
        'elements': elements,
        'slug': 'ficha-tecnica'
    }


def _create_factsheet_codes(metadata):
    return {
        'key_name': 'Código do produto',
        'position': 32,
        'elements': [{
            'value': '\n'.join([
                '{description} - {value}'.format(
                    description=code['description'],
                    value=code['value']
                )
                for code in _get_product_codes(metadata)
            ]),
            'is_html': False
        }],
        'slug': 'codigo-do-produto'
    }


def _create_factsheet_product_weight(metadata):
    return {
        'key_name': 'Peso aproximado',
        'position': 36,
        'elements': [{
            'slug': 'peso-do-produto',
            'is_html': False,
            'key_name': 'Peso do produto',
            'position': 37,
            'value': '{} gramas.'.format(metadata.get('form', {}).get('weight'))  # noqa
        }],
        'slug': 'peso-aproximado'
    }


def _create_factsheet_product_dimensions(metadata):
    return {
        'key_name': 'Dimensões do produto',
        'position': 39,
        'elements': [{
            'slug': 'produto',
            'is_html': False,
            'key_name': 'Produto',
            'position': 40,
            'value': '(L x A x P): {width} x {height} x {thickness} cm.'.format(  # noqa
                width=((metadata.get('form', {}).get('width') or 0) / 10),
                height=((metadata.get('form', {}).get('height') or 0) / 10),
                thickness=((metadata.get('form', {}).get('thickness')) or 0 / 10)  # noqa
            )
        }],
        'slug': 'dimensoes-do-produto'
    }


def create_media_payload(sku, seller_id, payload):
    payload = {
        'seller_id': seller_id,
        'sku': sku,
        'images': payload
    }

    return payload


def create_enriched_product_payload(sku, seller_id, navigation_id, metadata):
    return {
        'sku': sku,
        'seller_id': seller_id,
        'navigation_id': navigation_id,
        'metadata': {
            'Editora': _get_publishers(metadata),
            'Edição': '{}ª edição'.format(
                str(metadata.get('edition', {}).get('editionNumber'))
            ),
            'Autor': _get_authors(metadata),
            'Data de publicação': metadata.get('publicationDate'),
            'Tipo de produto': metadata.get('productType'),
            'Número de páginas': str(metadata.get('extent', {}).get('mainContentPageCount')),  # noqa
            'Idiomas do produto': _get_languages(metadata)
        },
        'title': metadata['titles'][0]['title'],
        'subtitle': metadata['titles'][0].get('subtitle'),
        'description': _get_description(metadata),
        'source': constants.SOURCE_METABOOKS,
        'entity': 'Livro',
        'category_id': 'LI'
    }


def _get_description(metadata):
    description = ''
    if metadata.get('textContents'):
        description = metadata['textContents'][0]['text']

    return description


def _get_publishers(metadata):
    publishers = []
    if metadata.get('publishers'):
        publishers = [
            publisher['publisherName']
            for publisher in metadata.get('publishers') or []
        ]

    return ', '.join(publishers)


def _get_authors(metadata):
    authors = []
    if metadata.get('contributors'):
        for contributor in metadata.get('contributors') or []:
            if contributor.get('lastName'):
                authors.append(
                    '{last_name}, {first_name}'.format(
                        last_name=contributor['lastName'],
                        first_name=contributor.get('firstName') or ''
                    )
                )
            else:
                authors.append(contributor['corporateName'])

    return ', '.join(authors)


def _get_languages(metadata):
    languages = []
    if metadata.get('languages'):
        languages = [
            _get_language_code(language['languageCode'])
            for language in metadata.get('languages') or []
        ]

    return ', '.join(languages)


def _get_product_codes(metadata):
    codes = []
    if metadata.get('identifiers'):
        codes = [
            {
                'value': identifier['idValue'],
                'description': _get_product_identifier_type(
                    identifier['productIdentifierType']
                )
            }
            for identifier in metadata.get('identifiers')
        ]

    return codes


def _get_product_identifier_type(_id):
    values = {
        '02': 'ISBN-10',
        '03': 'GTIN-13',
        '15': 'ISBN-13'
    }

    return values.get(_id) or _id


def _get_language_code(code):
    values = {
        'por': 'Português',
        'eng': 'Inglês'
    }

    return values.get(code) or code


def get_subject_codes(metadata):
    codes = []

    for subject in (
        metadata.get('subjects') or
        metadata.get('classifications') or
        []
    ):
        if (
            subject['subjectSchemeIdentifier'] != '10' or
            not subject.get('subjectCode')
        ):
            continue

        codes.append(subject['subjectCode'])

    return codes
