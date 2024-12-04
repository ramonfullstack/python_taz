from typing import Dict
from unittest.mock import patch

import pytest
from pymongo import MongoClient
from redis.client import Redis
from simple_settings.utils import settings_stub

from taz.constants import (
    AVAILABILITY_IN_STOCK,
    AVAILABILITY_OUT_OF_STOCK,
    MAGAZINE_LUIZA_SELLER_ID
)
from taz.consumers.product_exporter.scopes.simple_product import Scope
from taz.consumers.product_writer.tests.helpers import _save_badges_cache
from taz.core.matching.common.enriched_products import EnrichedProductSamples


class TestSimpleProductScope:

    @pytest.fixture
    def scope(self, product_dict: Dict) -> Scope:
        return Scope(
            seller_id=product_dict['seller_id'],
            sku=product_dict['sku']
        )

    @pytest.fixture
    def matching_uuid(self) -> Dict:
        return {
            'matching_uuid': 'd6b129fb-4a84-4642-adf0-872c91f37c23'
        }

    @pytest.fixture
    def save_price(
        self,
        mongo_database: MongoClient,
        price_dict: Dict
    ):
        mongo_database.prices.insert_one(price_dict)

    @pytest.fixture
    def price_dict(
        self,
        mongo_database: MongoClient,
        product_dict: Dict
    ) -> Dict:
        return {
            'sku': product_dict['sku'],
            'seller_id': product_dict['seller_id'],
            'list_price': 234.56,
            'price': 123.45,
            'delivery_availability': 'nationwide',
            'stock_count': 321,
            'stock_type': 'on_seller',
            'checkout_price': 234.56,
        }

    @pytest.fixture
    def save_product(
        self,
        mongo_database: MongoClient,
        product_dict: Dict,
        enriched_product: Dict,
        badge_dict: Dict,
        cache: Redis,
        matching_uuid: Dict
    ) -> None:
        self._store_media(mongo_database, product_dict)

        product_dict['selections'] = {
            '12966': ['16734', '16737'],
            '0': ['19108', '21168', '7291']
        }

        product_dict.update(matching_uuid)

        mongo_database.raw_products.insert_one(product_dict)
        mongo_database.enriched_products.insert_one(enriched_product)

        badge_dict['products'] = [{
            'sku': product_dict['sku'],
            'seller_id': product_dict['seller_id']
        }]
        mongo_database.badges.insert_one(badge_dict)

        stock = {
            'sku': product_dict['sku'],
            'seller_id': product_dict['seller_id'],
            'navigation_id': product_dict['navigation_id'],
            'type': 'DC',
            'branch_id': 300,
            'position': {
                'physic': {'amount': 10, 'reserved': 0, 'available': 10},
                'logic': {'amount': 0, 'reserved': 0, 'available': 0}
            },
            'delivery_availability': 'regional'
        }
        mongo_database.stocks.insert_one(stock)

        _save_badges_cache(cache, badge_dict)

    @pytest.fixture
    def save_product_with_media_data(
        self,
        mongo_database: MongoClient,
        product_dict: Dict,
        enriched_product: Dict,
        badge_dict: Dict,
        cache: Redis,
        matching_uuid: Dict
    ) -> None:
        self._store_media_with_media_data(mongo_database, product_dict)

        product_dict['selections'] = {
            '12966': ['16734', '16737'],
            '0': ['19108', '21168', '7291']
        }

        product_dict.update(matching_uuid)

        mongo_database.raw_products.insert_one(product_dict)
        mongo_database.enriched_products.insert_one(enriched_product)

        badge_dict['products'] = [{
            'sku': product_dict['sku'],
            'seller_id': product_dict['seller_id']
        }]
        mongo_database.badges.insert_one(badge_dict)

        stock = {
            'sku': product_dict['sku'],
            'seller_id': product_dict['seller_id'],
            'navigation_id': product_dict['navigation_id'],
            'type': 'DC',
            'branch_id': 300,
            'position': {
                'physic': {'amount': 10, 'reserved': 0, 'available': 10},
                'logic': {'amount': 0, 'reserved': 0, 'available': 0}
            },
            'delivery_availability': 'regional'
        }
        mongo_database.stocks.insert_one(stock)

        _save_badges_cache(cache, badge_dict)

    @pytest.fixture
    def patch_get_product(self):
        return patch.object(Scope, '_get_product')

    @pytest.fixture
    def patch_get_prices(self):
        return patch.object(Scope, '_get_prices')

    @pytest.fixture
    def patch_get_stocks(self):
        return patch.object(Scope, '_get_stocks')

    @pytest.fixture
    def patch_get_bundles(self):
        return patch.object(Scope, '_get_bundles')

    @pytest.fixture
    def patch_get_availability_stock(self):
        return patch.object(Scope, '_get_availability_stock')

    def _store_media(
        self,
        mongo_database: MongoClient,
        product_dict: Dict
    ) -> None:
        mongo_database.medias.insert_many([
            {
                'seller_id': product_dict['seller_id'],
                'sku': product_dict['sku'],
                'images': [
                    {
                        'url': 'http://img.magazineluiza.com.br/1500x1500/x-213445900.jpg',  # noqa
                        'hash': 'd4b4755b9ee658406f6e40f1d6e6129c'
                    },
                    {
                        'url': 'http://img.magazineluiza.com.br/1500x1500/x-213445900a.jpg',  # noqa
                        'hash': 'ce86964b8543828d1433cb1e029770e5'
                    },
                    '213445900.jpg',
                    '213445900-A.jpg'
                ]
            }
        ])

    def _store_media_with_media_data(
        self,
        mongo_database: MongoClient,
        product_dict: Dict
    ) -> None:
        mongo_database.medias.insert_many([
            {
                'seller_id': product_dict['seller_id'],
                'sku': product_dict['sku'],
                'images': ['130d7fbea7867ac3c31c28101a0344c2.jpg'],
                'audios': ['82c7d703f81ea086b927e192c0f99477.mp3'],
                'videos': ['https://video.com/1'],
                'podcasts': ['4b47ef5201ccdc08725ffa85815e18fb.mp3'],
            }
        ])

    def expected_payload(
        self,
        price,
        list_price,
        images=[],
        audios=[],
        videos=[],
        podcasts=[],
        entity=None,
        currency='BRL'
    ):
        images = (
            images
            if images
            else [
                'https://x.xx.xxx/{w}x{h}/lavadora-de-roupas-electrolux-addmix-13kg/magazineluiza/213445900/d4b4755b9ee658406f6e40f1d6e6129c.jpg', # noqa
                'https://x.xx.xxx/{w}x{h}/lavadora-de-roupas-electrolux-addmix-13kg/magazineluiza/213445900/ce86964b8543828d1433cb1e029770e5.jpg', # noqa
                'https://x.xx.xxx/{w}x{h}/lavadora-de-roupas-electrolux-addmix-13kg/magazineluiza/213445900/213445900.jpg', # noqa
                'https://x.xx.xxx/{w}x{h}/lavadora-de-roupas-electrolux-addmix-13kg/magazineluiza/213445900/213445900-A.jpg' # noqa
            ]
        )
        return {
            'scope': 'simple_product',
            'sku': '213445900',
            'seller_id': 'magazineluiza',
            'seller_name': 'Magazine Luiza',
            'type': 'product',
            'sells_to_company': True,
            'matching_uuid': 'd6b129fb-4a84-4642-adf0-872c91f37c23',
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
            'medias': images,
            'factsheet_url': 'http://pis.static-tst.magazineluiza.com.br/magazineluiza/factsheet/213445900.json',  # noqa
            'created_at': '2015-07-15T06:37:07.747000',
            'parent_sku': '2134458',
            'navigation_id': '213445900',
            'price': price,
            'list_price': list_price,
            'currency': currency,
            'availability': AVAILABILITY_IN_STOCK,
            'path': 'https://www.magazineluiza.com.br/lavadora-de-roupas-electrolux-addmix-13kg/p/213445900/ed/lava/',  # noqa
            'metadata': {
                'descriptive': {
                    'Tipo': ['Sem óleo'],
                    'Cor': ['Inox Vermelho'],
                    'Capacidade': ['3,2L'],
                    'Modelo Nominal': ['Family'],
                    'Voltagem': ['110 volts'],
                    'Modelo': ['AF-14'],
                    'Produto': ['Fritadeira Elétrica'],
                    'Marca': ['Mondial']
                },
                'delivery': {},
                'classified': {},
                'normalized_filters': {}
            },
            'filters_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade', 'Voltagem', 'Tipo', 'Potência'],  # noqa
            'entity': entity or 'Fritadeira Elétrica',
            'badges': [{
                'tooltip': 'Black Fraude',
                'text': 'Melhores oferta é na BLACK FRAUDE da Magazine Luiza - Procure este selo e compre tranquilo que garantimos o melhor preço.',  # noqa
                'image_url': 'https://a-static.mlcdn.com.br/{w}x{h}/black_fraude.jpg',  # noqa
                'position': 'bottom',
                'container': 'information',
                'name': 'Black Fraude',
                'active': True,
                'priority': 1,
                'slug': 'black-fraude'
            }],
            'selections': {
                '12966': ['16734', '16737'],
                '0': ['19108', '21168', '7291']
            },
            'review_count': 0,
            'review_rating': 0.0,
            'stock_count': 10,
            'audios': audios,
            'videos': videos,
            'podcasts': podcasts
        }

    def test_consumer_product_not_exists_in_raw_products(
        self,
        scope: Scope,
        product_dict: Dict,
        logger_stream
    ):
        ret = scope.get_data()

        assert ret is None
        assert (
            'Product not found for sku:{sku} seller_id:{seller_id}'.format(
                sku=product_dict['sku'],
                seller_id=product_dict['seller_id']
            )
        ) in logger_stream.getvalue()

    def test_consumer_product_with_tm_category(
        self,
        scope: Scope,
        logger_stream,
        mongo_database: MongoClient,
        product_dict: Dict
    ):
        product_dict['main_category'] = {'id': 'TM'}
        mongo_database.raw_products.insert_one(product_dict)

        ret = scope.get_data()

        assert ret is None
        assert (
            'Discarding the product because not categorized'
        ) in logger_stream.getvalue()

    def test_consumer_product_not_get_product_url(
        self,
        scope: Scope,
        logger_stream,
        mongo_database: MongoClient,
        product_dict: Dict
    ):
        del product_dict['categories']
        mongo_database.raw_products.insert_one(product_dict)

        ret = scope.get_data()

        assert ret is None
        assert (
            'Discarding the product {navigation_id} because it was '
            'not possible to generate the url'.format(
                navigation_id=product_dict['navigation_id']
            )
        ) in logger_stream.getvalue()

    def test_consumer_returned_payload_without_price_and_medias(
        self,
        scope: Scope,
        mongo_database: MongoClient,
        product_dict: Dict,
        rating_dict,
        review_dict,
        categories_dicts,
        matching_uuid
    ):
        product_dict['navigation_id'] = product_dict['navigation_id'][:7]
        product_dict.update(matching_uuid)
        mongo_database.raw_products.insert_one(product_dict)
        payload = scope.get_data()

        assert payload == {
            'scope': 'simple_product',
            'sku': '213445900',
            'seller_id': 'magazineluiza',
            'seller_name': 'Magazine Luiza',
            'type': 'product',
            'sells_to_company': True,
            'matching_uuid': 'd6b129fb-4a84-4642-adf0-872c91f37c23',
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
            'medias': [],
            'factsheet_url': 'http://pis.static-tst.magazineluiza.com.br/magazineluiza/factsheet/213445900.json',  # noqa
            'created_at': '2015-07-15T06:37:07.747000',
            'parent_sku': '2134458',
            'navigation_id': '213445900',
            'price': '0.00',
            'list_price': '0.00',
            'currency': 'BRL',
            'availability': AVAILABILITY_OUT_OF_STOCK,
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
            'review_rating': 4.3,
            'stock_count': 0,
            'audios': [],
            'videos': [],
            'podcasts': [],
        }

    def test_when_get_data_in_simple_product_scope_then_return_payload(
        self,
        scope: Scope,
        mongo_database: MongoClient,
        product_dict: Dict,
        save_price,
        enriched_product,
        badge_dict,
        cache,
        categories_dicts,
        save_product
    ):
        payload = scope.get_data()
        assert payload == self.expected_payload(
            price='123.45',
            list_price='234.56'
        )

    def test_when_reclassification_price_rule_exists_then_should_return_entity_with_success( # noqa
        self,
        scope: Scope,
        mongo_database: MongoClient,
        product_dict: Dict,
        save_price,
        enriched_product: Dict,
        badge_dict,
        cache: Redis,
        categories_dicts,
        save_product
    ):
        mongo_database.enriched_products.insert_one(
            EnrichedProductSamples.magazineluiza_sku_213445900_reclassification_price_rule()  # noqa
        )

        payload = scope.get_data()
        assert payload == self.expected_payload(
            price='123.45',
            list_price='234.56',
            entity='Peças para Refrigerador'
        )

    def test_consumer_price_collection_only_stock_should_return_ok(
        self,
        scope: Scope,
        mongo_database: MongoClient,
        product_dict: Dict,
        enriched_product: Dict,
        badge_dict,
        cache: Redis,
        categories_dicts,
        save_product
    ):
        price = {
            'sku': product_dict['sku'],
            'seller_id': product_dict['seller_id'],
            'delivery_availability': 'nationwide',
            'stock_count': 321,
            'stock_type': 'on_seller',
            'checkout_price': 234.56,
        }

        mongo_database.prices.insert_one(price)

        payload = scope.get_data()

        assert payload == self.expected_payload(
            price='0.00',
            list_price='0.00'
        )

    def test_consumer_return_seller_name_from_sellers_collection(
        self,
        scope: Scope,
        mongo_database: MongoClient,
        product_dict: Dict,
        save_price,
        enriched_product: Dict,
        badge_dict,
        cache: Redis,
        categories_dicts
    ):
        self._store_media(mongo_database, product_dict)

        product_dict['selections'] = {
            '12966': ['16734', '16737'],
            '0': ['19108', '21168', '7291']
        }
        del product_dict['seller_description']

        mongo_database.raw_products.insert_one(product_dict)
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

        payload = scope.get_data()
        assert payload['seller_name'] == seller_name

    def test_consumer_returned_payload_with_offer_id(
        self,
        scope: Scope,
        mongo_database: MongoClient,
        product_dict: Dict,
        enriched_product: Dict,
        cache: Redis,
        id_correlation_dict,
        save_price,
        unified_objects_dict
    ):
        self._store_media(mongo_database, product_dict)
        product_dict['selections'] = {
            '12966': ['16734', '16737'],
            '0': ['19108', '21168', '7291']
        }

        del product_dict['seller_description']
        product_dict['navigation_id'] = 'dfd5ck1fc0'
        mongo_database.raw_products.insert_one(product_dict)

        unified_objects_dict['id'] = '1234567'
        mongo_database.unified_objects.save(unified_objects_dict)

        payload = scope.get_data()

        assert payload['offer_id'] == '1234567'
        assert 'dfd5ck1fc0' in payload['id_correlations']
        assert len(payload['id_correlations']) == 6

    def test_consumer_returned_payload_with_bundles(
        self,
        scope: Scope,
        mongo_database: MongoClient,
        product_dict: Dict,
        enriched_product: Dict,
        id_correlation_dict,
        cache,
    ):
        product_dict['bundles'] = {
            '215587100': {
                'price': '299.99',
                'quantity': 1
            },
            '215589500': {
                'price': '800.00',
                'quantity': 1
            }
        }
        product_dict['type'] = 'bundle'

        self._store_media(mongo_database, product_dict)
        product_dict['selections'] = {
            '12966': ['16734', '16737'],
            '0': ['19108', '21168', '7291']
        }
        del product_dict['seller_description']

        mongo_database.raw_products.insert_one(product_dict)

        mongo_database.raw_products.insert_one({
            'brand': 'Plumatex',
            'reference': '37cm de Altura Ópus',
            'sku': '215587100',
            'title': 'Base Cama Box Queen Size Plumatex Bipartido',
            'seller_id': 'magazineluiza'
        })

        mongo_database.raw_products.insert_one({
            'brand': 'Plumatex',
            'reference': '28cm de Alt. Ópus',
            'sku': '215589500',
            'title': 'Colchão Queen Size Plumatex Molas Ensacadas',
            'seller_id': 'magazineluiza'
        })

        payload = scope.get_data()

        assert payload['type'] == 'bundle'
        assert payload['bundles'] == [{
            'brand': 'Plumatex',
            'price': '299.99',
            'quantity': 1,
            'reference': '37cm de Altura Ópus',
            'sku': '215587100',
            'title': 'Base Cama Box Queen Size Plumatex Bipartido'
        }, {
            'brand': 'Plumatex',
            'price': '800.00',
            'quantity': 1,
            'reference': '28cm de Alt. Ópus',
            'sku': '215589500',
            'title': 'Colchão Queen Size Plumatex Molas Ensacadas'
        }]

    def test_consumer_returned_payload_with_media_data(
        self,
        scope: Scope,
        mongo_database: MongoClient,
        product_dict: Dict,
        enriched_product: Dict,
        save_price,
        badge_dict,
        cache,
        categories_dicts,
        save_product_with_media_data
    ):
        payload = scope.get_data()
        expected_payload = self.expected_payload(
            price='123.45',
            list_price='234.56',
            audios=['https://x.xx.xxx/magazineluiza/audios/213445900/82c7d703f81ea086b927e192c0f99477.mp3'], # noqa
            podcasts=['https://x.xx.xxx/magazineluiza/podcasts/213445900/4b47ef5201ccdc08725ffa85815e18fb.mp3'], # noqa
            videos=['https://video.com/1'],
            images=['https://x.xx.xxx/{w}x{h}/lavadora-de-roupas-electrolux-addmix-13kg/magazineluiza/213445900/130d7fbea7867ac3c31c28101a0344c2.jpg'] # noqa
        )
        assert payload == expected_payload

    def test_bundle_without_children_return_discard_message(
        self,
        scope: Scope,
        mongo_database: MongoClient,
        product_dict: Dict,
        logger_stream
    ):
        product_dict['type'] = 'bundle'
        mongo_database.raw_products.insert_one(product_dict)

        payload = scope.get_data()
        assert not payload

        assert (
            'It is a bundle product, but does not have children'
        ) in logger_stream.getvalue()

    def test_product_with_pickupstore_return_metadata_delivery(
        self,
        scope: Scope,
        mongo_database: MongoClient,
        product_dict: Dict,
        enriched_pickupstore
    ):
        mongo_database.raw_products.insert_one(product_dict)
        mongo_database.enriched_products.insert_one(enriched_pickupstore)

        payload = scope.get_data()

        assert payload['metadata']['delivery'] == {'Retira loja': ['true']}

    def test_consumer_should_return_out_of_stock(
        self,
        scope: Scope,
        mongo_database: MongoClient,
        product_dict: Dict,
        save_price,
        cache,
    ):
        mongo_database.stocks.delete_one({
            'sku': product_dict['sku'],
            'seller_id': product_dict['seller_id']
        })

        del product_dict['seller_description']

        mongo_database.raw_products.insert_one(product_dict)

        payload = scope.get_data()

        assert payload['availability'] == AVAILABILITY_OUT_OF_STOCK
        assert payload['stock_count'] == 0

    def test_consumer_returned_payload_with_empty_string_in_description(
        self,
        scope: Scope,
        mongo_database: MongoClient,
        product_dict: Dict,
    ):
        product_dict['description'] = None
        mongo_database.raw_products.insert_one(product_dict)

        payload = scope.get_data()

        assert payload['description'] == ''

    def test_consumer_should_return_stock_from_price_collection(
        self,
        mongo_database: MongoClient,
        product_dict: Dict,
    ):
        seller_id = 'murcho'
        product_dict['seller_id'] = seller_id
        mongo_database.raw_products.insert_one(product_dict)

        price_dict = {
            'sku': product_dict['sku'],
            'seller_id': product_dict['seller_id'],
            'list_price': 234.56,
            'price': 123.45,
            'delivery_availability': 'nationwide',
            'stock_count': 10,
            'stock_type': 'on_seller',
            'checkout_price': 234.56,
        }

        mongo_database.prices.insert_one(price_dict)

        payload = Scope(
            seller_id=product_dict['seller_id'],
            sku=product_dict['sku']
        ).get_data()

        assert mongo_database.stocks.count_documents({}) == 0

        assert payload['stock_count'] == 10
        assert payload['availability'] == AVAILABILITY_IN_STOCK

    def test_return_empty_stock_and_product_unavailable_when_unpublished(
        self,
        scope: Scope,
        mongo_database: MongoClient,
        product_dict: Dict,
        enriched_product: Dict,
        save_price,
        badge_dict,
        cache,
        categories_dicts,
        save_product,
        save_unpublished_product
    ):
        expected_payload = self.expected_payload(
            price='123.45',
            list_price='234.56'
        )

        expected_payload['stock_count'] = 0
        expected_payload['availability'] = 'out of stock'
        expected_payload['active'] = False

        payload = scope.get_data()

        assert payload == expected_payload

    def test_product_should_use_all_source_to_build_descriptive(
        self,
        scope: Scope,
        mongo_database: MongoClient,
        product_dict: Dict,
        enriched_product: Dict,
        enriched_wakko,
        patch_storage_manager_get_json: patch
    ):
        mongo_database.raw_products.insert_one(product_dict)
        mongo_database.enriched_products.insert_many(
            [enriched_product, enriched_wakko]
        )

        payload = scope.get_data()

        assert payload['metadata']['descriptive'] == {
            'Capacidade': ['3,2L'],
            'Cor': ['Inox Vermelho'],
            'Marca': ['Mondial'],
            'Modelo': ['AF-14'],
            'Modelo Nominal': ['Family'],
            'Produto': ['Fritadeira Elétrica'],
            'Tipo': ['Sem óleo'],
            'Voltagem': ['110 volts'],
            'Volume': ['90g']
        }

    @settings_stub(ENABLE_FULFILLMENT=True)
    def test_when_fulfillment_enabled_and_product_with_fulfillment_then_return_fulfillment_in_payload( # noqa
        self,
        scope: Scope,
        product_dict: Dict,
        patch_get_product: patch,
        patch_get_prices: patch,
        patch_get_stocks: patch,
        patch_get_bundles: patch,
        patch_get_availability_stock: patch
    ):
        product_dict.update({'fulfillment': True})
        with patch_get_product as mock_get_product:
            with patch_get_stocks, patch_get_bundles:
                with patch_get_prices, patch_get_availability_stock:
                    mock_get_product.return_value = product_dict
                    payload = scope.get_data()

        assert payload['fulfillment']

    @settings_stub(ENABLE_FULFILLMENT=False)
    def test_when_fulfillment_disabled_and_product_with_fulfillment_then_not_include_fulfillment_in_payload( # noqa
        self,
        scope: Scope,
        product_dict: Dict,
        patch_get_product: patch,
        patch_get_prices: patch,
        patch_get_stocks: patch,
        patch_get_bundles: patch,
        patch_get_availability_stock: patch
    ):
        product_dict.update({'fulfillment': True})
        with patch_get_product as mock_get_product:
            with patch_get_stocks, patch_get_bundles:
                with patch_get_prices, patch_get_availability_stock:
                    mock_get_product.return_value = product_dict
                    payload = scope.get_data()

        assert 'fulfillment' not in payload

    @settings_stub(ENABLE_FULFILLMENT=True)
    def test_when_fulfillment_enabled_and_product_without_fulfillment_then_not_include_fulfillment_in_payload( # noqa
        self,
        scope: Scope,
        product_dict: Dict,
        patch_get_product: patch,
        patch_get_prices: patch,
        patch_get_stocks: patch,
        patch_get_bundles: patch,
        patch_get_availability_stock: patch
    ):
        with patch_get_product as mock_get_product:
            with patch_get_stocks, patch_get_bundles:
                with patch_get_prices, patch_get_availability_stock:
                    mock_get_product.return_value = product_dict
                    payload = scope.get_data()

        assert 'fulfillment' not in payload

    def test_when_matching_uuid_not_exists_in_database_then_include_none_in_payload( # noqa
        self,
        scope: Scope,
        product_dict: Dict,
        patch_get_product: patch,
        patch_get_prices: patch,
        patch_get_stocks: patch,
        patch_get_bundles: patch,
        patch_get_availability_stock: patch
    ):
        with patch_get_product as mock_get_product:
            with patch_get_stocks, patch_get_bundles:
                with patch_get_prices, patch_get_availability_stock:
                    mock_get_product.return_value = product_dict
                    payload = scope.get_data()

        assert payload['matching_uuid'] is None

    @settings_stub(ENABLE_EXTRA_DATA=True)
    def test_when_enabled_extra_data_and_product_has_no_extra_data_then_include_none_in_payload( # noqa
        self,
        scope: Scope,
        product_dict: Dict,
        patch_get_product: patch,
        patch_get_prices: patch,
        patch_get_stocks: patch,
        patch_get_bundles: patch,
        patch_get_availability_stock: patch
    ):
        with patch_get_product as mock_get_product:
            with patch_get_stocks, patch_get_bundles:
                with patch_get_prices, patch_get_availability_stock:
                    mock_get_product.return_value = product_dict
                    payload = scope.get_data()

        assert 'extra_data' in payload

    @settings_stub(ENABLE_EXTRA_DATA=True)
    def test_when_enabled_extra_data_and_product_has_extra_data_then_include_in_payload( # noqa
        self,
        scope: Scope,
        product_dict: Dict,
        patch_get_product: patch,
        patch_get_prices: patch,
        patch_get_stocks: patch,
        patch_get_bundles: patch,
        mock_extra_data: Dict,
        patch_get_availability_stock: patch
    ):
        extra_data = mock_extra_data['extra_data']
        product_dict.update({'extra_data': extra_data})
        with patch_get_product as mock_get_product:
            with patch_get_stocks, patch_get_bundles:
                with patch_get_prices, patch_get_availability_stock:
                    mock_get_product.return_value = product_dict
                    payload = scope.get_data()

        assert payload['extra_data'] == extra_data

    @pytest.mark.parametrize(
        'enable_parent_matching,parent_matching,assert_value', [
            (
                True,
                {'parent_matching_uuid': '27006db39089436fb52c5c00c8464034'},
                '27006db39089436fb52c5c00c8464034'
            ),
            (True, {}, None),
            (
                False,
                {'parent_matching_uuid': '27006db39089436fb52c5c00c8464034'},
                None
            )
        ]
    )
    def test_when_enabled_parent_matching_uuid_then_include_in_payload(
        self,
        scope: Scope,
        product_dict: Dict,
        patch_get_product: patch,
        patch_get_prices: patch,
        patch_get_stocks: patch,
        patch_get_bundles: patch,
        enable_parent_matching: bool,
        parent_matching: Dict,
        assert_value: str,
        patch_get_availability_stock: patch
    ):
        product_dict.update(parent_matching)
        with settings_stub(ENABLE_PARENT_MATCHING=enable_parent_matching):
            with patch_get_product as mock_get_product:
                with patch_get_stocks, patch_get_bundles:
                    with patch_get_prices, patch_get_availability_stock:
                        mock_get_product.return_value = product_dict
                        payload = scope.get_data()

        assert payload.get('parent_matching_uuid') == assert_value

    @pytest.mark.parametrize('minimum_order_quantity,stock_count', [
        (50, 100),
        (100, 100)
    ])
    def test_when_product_1p_with_minimum_order_quantity_less_than_or_equal_to_stock_then_should_return_stock_available( # noqa
        self,
        scope: Scope,
        product_dict: Dict,
        price_dict: Dict,
        mongo_database: MongoClient,
        patch_get_product: patch,
        patch_get_stocks: patch,
        patch_get_bundles: patch,
        minimum_order_quantity: int,
        stock_count: int
    ):
        price_dict['minimum_order_quantity'] = minimum_order_quantity
        mongo_database.prices.insert_one(price_dict)

        with patch_get_stocks as mock_stock:
            mock_stock.return_value = {'stock_count': stock_count}
            with patch_get_bundles, patch_get_product as mock_get_product:
                mock_get_product.return_value = product_dict
                payload = scope.get_data()

        assert payload['availability'] == AVAILABILITY_IN_STOCK
        assert payload['stock_count'] == stock_count
        assert payload['minimum_order_quantity'] == minimum_order_quantity

    def test_when_product_1p_with_minimum_order_quantity_greater_than_stock_then_should_return_out_of_stock( # noqa
        self,
        scope: Scope,
        product_dict: Dict,
        price_dict: Dict,
        mongo_database: MongoClient,
        patch_get_product: patch,
        patch_get_stocks: patch,
        patch_get_bundles: patch
    ):
        minimum_order_quantity = 10
        stock_count = 5

        price_dict['minimum_order_quantity'] = minimum_order_quantity
        mongo_database.prices.insert_one(price_dict)

        with patch_get_stocks as mock_stock:
            mock_stock.return_value = {'stock_count': stock_count}
            with patch_get_bundles, patch_get_product as mock_get_product:
                mock_get_product.return_value = product_dict
                payload = scope.get_data()

        assert payload['availability'] == AVAILABILITY_OUT_OF_STOCK
        assert payload['stock_count'] == 0
        assert payload['minimum_order_quantity'] == minimum_order_quantity

    @pytest.mark.parametrize('seller_id', [
        MAGAZINE_LUIZA_SELLER_ID,
        'luizalabs'
    ])
    def test_when_product_without_minimum_order_quantity_but_with_stock_should_return_stock_available( # noqa
        self,
        scope: Scope,
        product_dict: Dict,
        price_dict: Dict,
        save_price,
        mongo_database: MongoClient,
        patch_get_product: patch,
        patch_get_stocks: patch,
        patch_get_bundles: patch,
        seller_id: str
    ):
        stock_count = 10
        product_dict['seller_id'] = seller_id
        with patch_get_stocks as mock_stock:
            mock_stock.return_value = {'stock_count': stock_count}
            with patch_get_bundles, patch_get_product as mock_get_product:
                mock_get_product.return_value = product_dict
                payload = scope.get_data()

        assert payload['availability'] == AVAILABILITY_IN_STOCK
        assert payload['stock_count'] == stock_count
        assert payload.get('minimum_order_quantity') is None

    @pytest.mark.parametrize('seller_id', [
        MAGAZINE_LUIZA_SELLER_ID,
        'luizalabs'
    ])
    def test_when_product_without_minimum_order_quantity_and_without_stock_should_return_out_of_stock(  # noqa
        self,
        scope: Scope,
        product_dict: Dict,
        price_dict: Dict,
        save_price,
        mongo_database: MongoClient,
        patch_get_product: patch,
        patch_get_stocks: patch,
        patch_get_bundles: patch,
        seller_id: str
    ):
        stock_count = 0
        product_dict['seller_id'] = seller_id
        with patch_get_stocks as mock_stock:
            mock_stock.return_value = {'stock_count': stock_count}
            with patch_get_bundles, patch_get_product as mock_get_product:
                mock_get_product.return_value = product_dict
                payload = scope.get_data()

        assert payload['availability'] == AVAILABILITY_OUT_OF_STOCK
        assert payload['stock_count'] == stock_count
        assert payload.get('minimum_order_quantity') is None
