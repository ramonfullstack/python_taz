import pytest

from taz.consumers.metadata_verify.scopes.metabooks.helpers import (
    _create_factsheet_more_informations,
    _get_authors,
    _get_description,
    _get_language_code,
    _get_languages,
    _get_product_codes,
    _get_product_identifier_type,
    _get_publishers,
    create_enriched_product_payload,
    create_factsheet_payload,
    create_media_payload,
    get_subject_codes
)


class TestCreateFactsheetPayload:

    def test_create_factsheet_payload(
        self,
        sku,
        seller_id,
        metadata,
        expected_metadata
    ):
        payload = create_factsheet_payload(sku, seller_id, metadata)
        assert payload == expected_metadata

    def test_when_content_page_count_is_not_none(self, metadata):
        metadata['extent'] = {'contentPageCount': 465}
        metadata['extent']['mainContentPageCount'] = None
        informations = _create_factsheet_more_informations(metadata)

        assert informations['elements'][0]['value'] == '465'

    def test_when_content_page_count_is_none_then_return_main_content_page_count(self, metadata): # noqa
        metadata['extent']['contentPageCount'] = None
        metadata['extent']['mainContentPageCount'] = 464
        informations = _create_factsheet_more_informations(metadata)

        assert informations['elements'][0]['value'] == '464'

    def test_when_main_content_page_count_is_not_none_then_return_main_content_page_count(self, metadata): # noqa
        metadata['extent']['mainContentPageCount'] = 464
        metadata['extent']['contentPageCount'] = 465
        informations = _create_factsheet_more_informations(metadata)

        assert informations['elements'][0]['value'] == '464'

    def test_when_main_content_page_is_not_none(self, metadata):
        metadata['extent']['mainContentPageCount'] = 464
        metadata['extent']['contentPageCount'] = None
        informations = _create_factsheet_more_informations(metadata)

        assert informations['elements'][0]['value'] == '464'

    def test_when_main_content_page_count_and_content_page_count_is_none(self, metadata):  # noqa
        metadata['extent']['mainContentPageCount'] = None
        metadata['extent']['contentPageCount'] = None
        informations = _create_factsheet_more_informations(metadata)

        assert 'numero-de-paginas' not in [
            info['slug'] for info in informations['elements']
        ]


class TestCreateMediaPayload:

    def test_create_media_payload(
        self,
        sku,
        seller_id,
        mock_metabooks_images,
        mock_expected_metabooks_images
    ):
        payload = create_media_payload(sku, seller_id, mock_metabooks_images)

        assert payload == mock_expected_metabooks_images

    def test_create_media_payload_returns_empty_list(self, sku, seller_id):
        payload = create_media_payload(sku, seller_id, [])

        assert payload == {
            'images': [],
            'sku': '123456789',
            'seller_id': 'murcho'
        }


class TestCreateEnrichedProductPayload:

    def test_create_enriched_product_payload(
        self,
        sku,
        seller_id,
        navigation,
        metadata,
        mock_expected_metabooks_enriched_product
    ):
        payload = create_enriched_product_payload(
            sku,
            seller_id,
            navigation,
            metadata
        )

        assert (
            payload == mock_expected_metabooks_enriched_product
        )

    def test_create_enriched_product_payload_without_fields(
        self,
        sku,
        seller_id,
        navigation,
        metadata,
        mock_expected_metabooks_enriched_product
    ):
        for field in ['publishers', 'contributors', 'languages']:
            del metadata[field]

        mock_expected_metabooks_enriched_product['metadata'].update({
            'Editora': '',
            'Autor': '',
            'Idiomas do produto': ''
        })

        payload = create_enriched_product_payload(
            sku,
            seller_id,
            navigation,
            metadata
        )

        assert payload == mock_expected_metabooks_enriched_product


class TestGetLanguageCode:

    @pytest.mark.parametrize('code, expected', [
        ('por', 'Português'),
        ('eng', 'Inglês'),
        ('aaa', 'aaa'),
    ])
    def test_get_language_code(self, code, expected):
        payload = _get_language_code(code)
        assert payload == expected


class TestGetProductIdentifierType:

    @pytest.mark.parametrize('code, expected', [
        ('02', 'ISBN-10'),
        ('03', 'GTIN-13'),
        ('15', 'ISBN-13'),
        ('20', '20'),
    ])
    def test_get_product_identifier_type(self, code, expected):
        payload = _get_product_identifier_type(code)
        assert payload == expected


class TestGetProductCodes:

    def test_get_product_codes(self, metadata):
        payload = _get_product_codes(metadata)
        assert payload == [
            {'description': 'ISBN-10', 'value': '8582604661'},
            {'description': 'GTIN-13', 'value': '9788582604663'},
            {'description': 'ISBN-13', 'value': '9788582604663'}
        ]

    def test_get_product_codes_returns_empty_list(self, metadata):
        del metadata['identifiers']

        payload = _get_product_codes(metadata)
        assert payload == []


class TestGetLanguages:

    def test_get_languages(self, metadata):
        payload = _get_languages(metadata)
        assert payload == 'Português'

    def test_get_languages_returns_empty_list(self, metadata):
        del metadata['languages']

        payload = _get_languages(metadata)
        assert payload == ''


class TestGetAuthors:

    def test_get_authors(self, metadata):
        payload = _get_authors(metadata)
        assert payload == (
            'Zacker, Craig, Michel, Luciana Monteiro, '
            'Silva, Aldir José Coelho Corrêa da'
        )

    def test_get_authors_returns_empty_list(self, metadata):
        del metadata['contributors']

        payload = _get_authors(metadata)
        assert payload == ''


class TestGetPublishers:

    def test_get_publishers(self, metadata):
        payload = _get_publishers(metadata)
        assert payload == 'Bookman'

    def test_get_publishers_returns_empty_list(self, metadata):
        del metadata['publishers']

        payload = _get_publishers(metadata)
        assert payload == ''


class TestGetDescription:

    def test_get_description(self, metadata):
        payload = _get_description(metadata)
        assert payload == (
            'Livro preparatório para o exame de entrada da certificação '
            'MCSA, que comprova o domínio das habilidades essenciais do '
            'Windows Server 2016 para reduzir custos de TI e agregar mais '
            'valor ao negócio. Os exames 70-741 (Redes com Windows Server '
            '2016) e o Exame 70-742 (Identidade com Windows Server 2016) '
            'também são necessários para a obtenção do MCSA Windows Server '
            '2016.'
        )

    def test_get_description_returns_empty(self, metadata):
        del metadata['textContents']

        payload = _get_description(metadata)
        assert payload == ''


class TestGetSubjectCodes:

    def test_get_subject_codes(self, metadata):
        codes = get_subject_codes(metadata)
        assert codes == ['COM046050', 'COM051330', 'COM014000']

    def test_get_classifications_codes(self, metadata):
        metadata['classifications'] = metadata['subjects']
        del metadata['subjects']

        codes = get_subject_codes(metadata)
        assert codes == ['COM046050', 'COM051330', 'COM014000']

    def test_get_empty_list(self):
        codes = get_subject_codes({})
        assert codes == []
