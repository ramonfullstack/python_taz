import pytest

from taz.consumers.core.exceptions import NotFound
from taz.consumers.product_exporter.scopes.source_product import Scope
from taz.consumers.product_writer.tests.helpers import _save_badges_cache


class TestSourceProductScope:

    @pytest.fixture
    def scope(self, product_dict):
        return Scope(
            seller_id=product_dict['seller_id'],
            sku=product_dict['sku']
        )

    @pytest.fixture
    def price_dict(self, mongo_database, product_dict):
        price = {
            'sku': product_dict['sku'],
            'seller_id': product_dict['seller_id'],
            'list_price': 234.56,
            'price': 123.45,
            'delivery_availability': 'nationwide',
            'stock_count': 321,
            'stock_type': 'on_seller',
            'checkout_price': 234.56,
        }

        mongo_database.prices.insert_one(price)

    def test_consumer_product_not_exists_in_storage(
        self,
        scope,
        logger_stream,
        patch_storage_manager_get_json
    ):
        with patch_storage_manager_get_json as mock_storage_json:
            mock_storage_json.side_effect = NotFound()
            ret = scope.get_data()

        log = logger_stream.getvalue()

        assert ret is None
        assert (
            'Product not found in storage when searching'
            ' for sku:213445900 and seller_id:magazineluiza.'
        ) in log

    def test_consumer_product_with_tm_category(
        self,
        scope,
        logger_stream,
        product_dict,
        patch_storage_manager_get_json
    ):
        product_dict['main_category'] = {'id': 'TM'}

        with patch_storage_manager_get_json as mock_storage_json:
            mock_storage_json.return_value = product_dict
            ret = scope.get_data()

        assert ret is None
        assert (
            'Discarding the product because not categorized'
        ) in logger_stream.getvalue()

    def test_consumer_product_not_get_product_url(
        self,
        scope,
        logger_stream,
        patch_storage_manager_get_json,
        product_dict
    ):
        del product_dict['categories']

        with patch_storage_manager_get_json as mock_storage_json:
            mock_storage_json.return_value = product_dict
            ret = scope.get_data()

        assert ret is None
        assert (
            'Discarding sku:213445900 seller_id:magazineluiza '
            'navigation_id:213445900 because it was not possible '
            'to generate the url'
        ) in logger_stream.getvalue()

    def test_consumer_returned_payload_without_price_and_medias(
        self,
        scope,
        patch_storage_manager_get_json,
        product_dict,
        rating_dict,
        review_dict,
        categories_dicts
    ):
        product_dict['navigation_id'] = product_dict['navigation_id'][:7]
        with patch_storage_manager_get_json as mock_storage_json:
            mock_storage_json.return_value = product_dict
            payload = scope.get_data()

        assert payload == {
            'scope': 'source_product',
            'sku': '213445900',
            'seller_id': 'magazineluiza',
            'seller_name': 'Magazine Luiza',
            'type': 'product',
            'dimensions': {
                'height': 1.05,
                'depth': 0.76,
                'weight': 50,
                'width': 0.69
            },
            'ean': '7896584066579',
            'brand': 'electrolux',
            'title': 'Lavadora de Roupas Electrolux Addmix',
            'description': 'Lavadora Electrolux, silenciosa e com capacidade de 13Kg, lava mais roupa em menos tempo e espaço, economizando água, energia e produtos de limpeza. O dispencer automático ADDMix, calcula a dosagem de sabão e amaciante, faz a mistura exata, na hora correta. Tem 5 Níveis de água, incluindo nível automático de água que dosa o nível de água da máquina de acordo com a programação e a quantidade de roupa na máquina. E com a exclusiva função Turbo Secagem você aumenta o tempo de centrifugação permitindo que suas roupas saiam mais secas da lavadora do que numa centrifugação normal.\n',  # noqa
            'categories': [{
                'subcategories': [{
                    'id': 'LAVA',
                    'url': 'maquina-de-lavar/eletrodomesticos/s/ed/lava/',
                    'name': 'Máquina de Lavar'
                }],
                'id': 'ED',
                'url': 'eletrodomesticos/l/ed/',
                'name': 'Eletrodomésticos'
            }],
            'reference': '13kg',
            'active': True,
            'attributes': [{
                'value': '220 Volts',
                'type': 'voltage'
            }],
            'medias': ['https://x.xx.xxx/{w}x{h}/imagem-indisponivel/appmockups/000000000/1bd79dc863d30982501d43e14bccc8f0.jpg'],  # noqa
            'factsheet_url': 'http://pis.static-tst.magazineluiza.com.br/magazineluiza/factsheet/213445900.json',  # noqa
            'created_at': '2015-07-15T06:37:07.747000',
            'parent_sku': '2134458',
            'navigation_id': '213445900',
            'path': 'https://www.magazineluiza.com.br/lavadora-de-roupas-electrolux-addmix-13kg/p/213445900/ed/lava/',  # noqa
            'metadata': {
                'descriptive': {},
                'delivery': {},
                'classified': {},
                'normalized_filters': {}
            },
            'filters_metadata': [],
            'entity': '',
            'selections': {},
            'review_count': 83,
            'review_rating': 4.3
        }

    def test_consumer_return_seller_name_from_sellers_collection(
        self,
        scope,
        patch_storage_manager_get_json,
        mongo_database,
        product_dict,
        enriched_product,
        badge_dict,
        cache,
        categories_dicts,
        store_media
    ):
        product_dict['selections'] = {
            '12966': ['16734', '16737'],
            '0': ['19108', '21168', '7291']
        }
        del product_dict['seller_description']

        mongo_database.enriched_products.insert_one(enriched_product)

        badge_dict['products'] = [{
            'sku': product_dict['sku'],
            'seller_id': product_dict['seller_id']
        }]
        mongo_database.badges.insert_one(badge_dict)

        seller_name = 'Test Murcho'
        mongo_database.sellers.insert_one({
            'name': seller_name,
            'id': product_dict['seller_id']
        })

        _save_badges_cache(cache, badge_dict)

        with patch_storage_manager_get_json as mock_storage_json:
            mock_storage_json.return_value = product_dict
            payload = scope.get_data()

        assert payload['seller_name'] == seller_name

    def test_consumer_returned_payload_with_offer_id(
        self,
        scope,
        mongo_database,
        product_dict,
        patch_storage_manager_get_json,
        id_correlation_dict,
        cache,
        store_media,
        price_dict,
        unified_objects_dict
    ):
        product_dict['selections'] = {
            '12966': ['16734', '16737'],
            '0': ['19108', '21168', '7291']
        }
        del product_dict['seller_description']
        product_dict['navigation_id'] = 'dfd5ck1fc0'
        mongo_database.raw_products.save(product_dict)

        unified_objects_dict['id'] = '1234567'
        mongo_database.unified_objects.save(unified_objects_dict)

        with patch_storage_manager_get_json as mock_storage_json:
            mock_storage_json.return_value = product_dict
            payload = scope.get_data()

        assert payload['offer_id'] == '1234567'
        assert 'dfd5ck1fc0' in payload['id_correlations']
        assert len(payload['id_correlations']) == 6

    def test_product_with_pickupstore_return_metadata_delivery(
        self,
        scope,
        mongo_database,
        product_dict,
        enriched_pickupstore,
        patch_storage_manager_get_json
    ):
        mongo_database.enriched_products.insert_one(enriched_pickupstore)
        with patch_storage_manager_get_json as mock_storage_json:
            mock_storage_json.return_value = product_dict
            payload = scope.get_data()

        assert payload['metadata']['delivery'] == {'Retira loja': ['true']}

    def test_consumer_return_payload_with_category_from_raw_products(
        self,
        scope,
        patch_storage_manager_get_json,
        product_dict,
        mongo_database,
        categories_dicts
    ):
        mongo_database.raw_products.insert_one(product_dict)
        product_dict['categories'] = [
            {
                "id": "RC",
                "subcategories": [
                    {
                        "id": "RCNM",
                        "description": "No Magalu",
                    }
                ],
            }
        ]

        with patch_storage_manager_get_json as mock_storage_json:
            mock_storage_json.return_value = product_dict
            payload = scope.get_data()

        assert payload['categories'] == [{
            'subcategories': [{
                'id': 'LAVA',
                'url': 'maquina-de-lavar/eletrodomesticos/s/ed/lava/',
                'name': 'Máquina de Lavar'
            }],
            'id': 'ED',
            'url': 'eletrodomesticos/l/ed/',
            'name': 'Eletrodomésticos'
        }]

    def test_consumer_returned_payload_with_empty_string_in_description(
        self,
        scope,
        product_dict,
        patch_storage_manager_get_json
    ):
        product_dict['description'] = None
        with patch_storage_manager_get_json as mock_storage_json:
            mock_storage_json.return_value = product_dict
            payload = scope.get_data()

        assert payload['description'] == ''

    def test_return_empty_stock_and_product_unavailable_when_unpublished(
        self,
        scope,
        product_dict,
        patch_storage_manager_get_json,
        id_correlation_dict,
        cache,
        store_media,
        save_unpublished_product
    ):
        product_dict['selections'] = {
            '12966': ['16734', '16737'],
            '0': ['19108', '21168', '7291']
        }
        del product_dict['seller_description']

        with patch_storage_manager_get_json as mock_storage_json:
            mock_storage_json.return_value = product_dict
            payload = scope.get_data()

        assert payload['stock_count'] == 0
        assert payload['availability'] == 'out of stock'
        assert payload['active'] is False

    def test_product_should_not_use_wakko_source_to_build_descriptive(
        self,
        scope,
        mongo_database,
        product_dict,
        enriched_product,
        enriched_wakko,
        patch_storage_manager_get_json
    ):
        mongo_database.enriched_products.insert_many(
            [enriched_product, enriched_wakko]
        )
        with patch_storage_manager_get_json as mock_storage_json:
            mock_storage_json.return_value = product_dict
            payload = scope.get_data()

        assert payload['metadata']['descriptive'] == {
            'Capacidade': ['3,2L'],
            'Cor': ['Inox Vermelho'],
            'Marca': ['Mondial'],
            'Modelo': ['AF-14'],
            'Modelo Nominal': ['Family'],
            'Produto': ['Fritadeira Elétrica'],
            'Tipo': ['Sem óleo'],
            'Voltagem': ['110 volts']
        }
