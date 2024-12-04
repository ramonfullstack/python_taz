from datetime import datetime
from decimal import Decimal

import pytest

from taz.constants import (
    MAGAZINE_LUIZA_SELLER_DESCRIPTION,
    MAGAZINE_LUIZA_SELLER_ID
)
from taz.pollers.product.converter import (
    ProductConverter,
    ProductSpecification,
    ProductType
)


class TestProductConverter:

    @pytest.fixture
    def batch_key(self):
        return 21650

    @pytest.fixture
    def sku(self):
        return '216501900'

    @pytest.fixture
    def converter(self):
        return ProductConverter()

    @pytest.fixture
    def product_db_row(self, batch_key, sku):
        return {
            'batch_key': batch_key,
            'ean': '0841667100531',
            'sku': sku,
            'parent_sku': sku,
            'main_variation': 1,
            'product_type': ProductType.product.value,
            'title': 'Kindle Paperwhite Wi-Fi 4GB Tela 6',
            'description': 'Especialmente feito para os amantes da leitura',
            'reference': 'Amazon',
            'brand': 'amazon',
            'sold_count': 35,
            'review_count': 12,
            'review_score': Decimal(4.5),
            'category_id': 'TB',
            'subcategory_id': 'KIND',
            'width': Decimal(1.0),
            'height': Decimal(1.8399999999999999),
            'depth': Decimal(0.1477777777),
            'weight': Decimal(0.44),
            'voltage': 'Bivolt',
            'color': 'Azul',
            'specification_id': 5,
            'specification_description': '16 GB',
            'release_date': datetime.now(),
            'updated_at': datetime.now(),
            'created_at': datetime.now(),
            'extra_categories': 'EL;LEDD|TB;TAA1|TB;TBB2|TB;TCC3|EL;WIFI',
            'selections': '0;13358|0;13400|24;13401|69;13414',
            'bundles': '1766084;00;179.00;1|2017461;00;95.00;1',
            'gift_product': '150658700',
            'active': True
        }

    @pytest.fixture
    def product_db_row_with_voltage(self, batch_key):
        return {
            'batch_key': batch_key,
            'ean': '7891129195448',
            'parent_sku': '2029572',
            'main_variation': '1',
            'sku': '202957200',
            'product_type': 1,
            'title': 'Geladeira/Refrigerador Consul Cycle Defrost Duplex',
            'description': 'Refrigerador Consul com mais espaço interno',
            'reference': 'Branca 334L CRD37 EBANA',
            'brand': 'consul',
            'sold_count': '0',
            'review_count': '0',
            'review_score': '0',
            'category_id': 'ED',
            'subcategory_id': 'REF2',
            'width': Decimal(1.0),
            'height': Decimal(1.0),
            'depth': Decimal(1.0),
            'weight': Decimal(1.0),
            'voltage': '110 Volts',
            'color': None,
            'specification_id': None,
            'specification_description': None,
            'release_date': datetime.now(),
            'updated_at': datetime.now(),
            'created_at': datetime.now(),
            'extra_categories': None,
            'bundles': '1766084;00;179.00;1|2017461;00;95.00;1',
            'gift_product': '',
            'active': 1,
            'strMestre': '2029572',
            'strCodigo': '2029572',
            'strMarca': 'Consul',
            'strlinha': 'ED',
            'strSetor': 'REF2'
        }

    @pytest.fixture
    def expected_result(
        self,
        product_db_row,
        sku
    ):
        return {
            sku: {
                'ean': product_db_row['ean'],
                'seller_id': MAGAZINE_LUIZA_SELLER_ID,
                'main_variation': bool(product_db_row['main_variation']),
                'seller_description': MAGAZINE_LUIZA_SELLER_DESCRIPTION,
                'sku': product_db_row['sku'],
                'parent_sku': product_db_row['parent_sku'],
                'type': ProductType(product_db_row['product_type']).name,
                'title': product_db_row['title'],
                'description': product_db_row['description'],
                'reference': product_db_row['reference'],
                'brand': product_db_row['brand'],
                'sold_count': product_db_row['sold_count'],
                'review_count': product_db_row['review_count'],
                'review_score': Decimal(product_db_row['review_score']),
                'main_category': {
                    'id': product_db_row['category_id'],
                    'subcategory': {'id': product_db_row['subcategory_id']}
                },
                'categories': [
                    {
                        'id': 'TB',
                        'subcategories': [
                            {'id': 'KIND'},
                            {'id': 'TAA1'},
                            {'id': 'TBB2'},
                            {'id': 'TCC3'},
                        ]
                    },
                    {
                        'id': 'EL',
                        'subcategories': [
                            {'id': 'LEDD'},
                            {'id': 'WIFI'}
                        ]
                    }
                ],
                'selections': {
                    '0': ['13358', '13400'],
                    '24': ['13401'],
                    '69': ['13414']
                },
                'dimensions': {
                    'depth': 0.148,
                    'height': 1.84,
                    'weight': 0.44,
                    'width': 1.0
                },
                'attributes': [
                    {
                        'type': (
                            ProductSpecification.get_by_id(
                                product_db_row['specification_id']
                            ).name
                        ),
                        'value': product_db_row['specification_description']
                    },
                    {
                        'type': ProductSpecification.color.name,
                        'value': product_db_row['color']
                    },
                    {
                        'type': ProductSpecification.voltage.name,
                        'value': product_db_row['voltage']
                    }
                ],
                'release_date': product_db_row['release_date'].isoformat(),
                'updated_at': product_db_row['updated_at'].isoformat(),
                'created_at': product_db_row['created_at'].isoformat(),
                'bundles': {
                    '176608400': {'price': '179.00', 'quantity': 1},
                    '201746100': {'price': '95.00', 'quantity': 1}
                },
                'gift_product': '150658700',
                'active': True
            }
        }

    @pytest.fixture
    def expected_result_voltage(
        self,
        product_db_row_with_voltage
    ):
        return {
            '202957200': {
                'ean': product_db_row_with_voltage['ean'],
                'seller_id': MAGAZINE_LUIZA_SELLER_ID,
                'main_variation': bool(
                    product_db_row_with_voltage['main_variation']
                ),
                'seller_description': MAGAZINE_LUIZA_SELLER_DESCRIPTION,
                'sku': product_db_row_with_voltage['sku'],
                'parent_sku': product_db_row_with_voltage['parent_sku'],
                'type': ProductType(
                    product_db_row_with_voltage['product_type']
                ).name,
                'title': product_db_row_with_voltage['title'],
                'description': product_db_row_with_voltage['description'],
                'reference': product_db_row_with_voltage['reference'],
                'brand': product_db_row_with_voltage['brand'],
                'sold_count': 0,
                'review_count': 0,
                'review_score': 0.0,
                'main_category': {
                    'id': product_db_row_with_voltage['category_id'],
                    'subcategory': {
                        'id': product_db_row_with_voltage['subcategory_id']
                    }
                },
                'categories': [
                    {'id': 'ED', 'subcategories': [{'id': 'REF2'}]}
                ],
                'dimensions': {
                    'depth': 1.0,
                    'height': 1.0,
                    'weight': 1.0,
                    'width': 1.0
                },
                'attributes': [{'type': 'voltage', 'value': '110 Volts'}],
                'release_date': product_db_row_with_voltage['release_date'].isoformat(), # noqa
                'updated_at': product_db_row_with_voltage['updated_at'].isoformat(), # noqa
                'created_at': product_db_row_with_voltage['created_at'].isoformat(), # noqa
                'bundles': {
                    '176608400': {'price': '179.00', 'quantity': 1},
                    '201746100': {'price': '95.00', 'quantity': 1}
                },
                'active': 1
            }
        }

    @pytest.mark.parametrize('payload_input,expected', [
        (
            'product_db_row',
            'expected_result'
        ),
        (
            'product_db_row_with_voltage',
            'expected_result_voltage'
        )
    ])
    def test_convert_product_successfully(
        self,
        converter,
        batch_key,
        payload_input,
        expected,
        request
    ):
        payload = request.getfixturevalue(payload_input)
        expected = request.getfixturevalue(expected)

        converter.from_source([payload])

        items = converter.get_items()
        assert len(items) == 1
        assert items[batch_key] == expected

    @pytest.mark.parametrize('attribute, expected_type, expected_value', [
        (
            {'color': 'Azul'},
            ProductSpecification.color.name,
            'Azul'
        ),
        (
            {'voltage': 'Bivolt'},
            ProductSpecification.voltage.name,
            'Bivolt'
        ),
        (
            {'specification_id': 14, 'specification_description': 'Esquerdo'},
            ProductSpecification.side.name,
            'Esquerdo'
        )
    ])
    def test_different_attributes_on_convert_product(
        self, converter, product_db_row, batch_key, sku, attribute,
        expected_type, expected_value
    ):
        product_db_row.update({
            'voltage': None,
            'color': None,
            'specification_id': None,
            'specification_description': None
        })
        product_db_row.update(attribute)

        converter.from_source([product_db_row])

        items = converter.get_items()
        assert len(items) == 1

        item = items[batch_key][sku]
        attributes = item['attributes']
        assert len(attributes) == 1

        attribute = attributes[0]
        assert attribute['type'] == expected_type
        assert attribute['value'] == expected_value

    def test_product_without_attributes_on_convert(
        self, converter, product_db_row, batch_key, sku, expected_result
    ):
        product_db_row.update({
            'voltage': None,
            'color': None,
            'specification_id': None,
            'specification_description': None
        })

        del expected_result[sku]['attributes']

        converter.from_source([product_db_row])

        items = converter.get_items()
        assert len(items) == 1
        assert items[batch_key] == expected_result

    @pytest.mark.parametrize('field_name', ['release_date', 'updated_at'])
    def test_product_without_field_date_on_convert(
        self, converter, product_db_row, batch_key, sku,
        expected_result, field_name
    ):
        product_db_row[field_name] = None

        del expected_result[sku][field_name]

        converter.from_source([product_db_row])

        items = converter.get_items()
        assert len(items) == 1
        assert items[batch_key] == expected_result

    def test_product_without_bundles(
        self, converter, product_db_row, batch_key, sku, expected_result
    ):
        del product_db_row['bundles']
        del expected_result[sku]['bundles']

        converter.from_source([product_db_row])

        items = converter.get_items()
        assert len(items) == 1
        assert items[batch_key] == expected_result

    def test_product_without_gift_product(
        self, converter, product_db_row, batch_key, sku, expected_result
    ):
        del product_db_row['gift_product']
        del expected_result[sku]['gift_product']

        converter.from_source([product_db_row])

        items = converter.get_items()
        assert len(items) == 1
        assert items[batch_key] == expected_result

    def test_product_return_empty_ean_when_it_not_provided(
        self, converter, product_db_row, batch_key, sku
    ):
        product_db_row['ean'] = None

        converter.from_source([product_db_row])

        items = converter.get_items()
        assert len(items) == 1
        assert items[batch_key][sku]['ean'] == ''

    def test_return_ean_successfully(self, converter, product_db_row):
        expected = '7899838819983'

        product_db_row['ean'] = expected
        response = converter.get_ean_from_response(product_db_row)

        assert response == expected

    def test_return_ean_completing_with_zero(self, converter, product_db_row):
        expected = '0000078998388'

        product_db_row['ean'] = expected[-8:]
        response = converter.get_ean_from_response(product_db_row)

        assert response == expected

    def test_return_empty_ean_when_it_not_provided(
        self, converter, product_db_row
    ):
        expected = ''

        product_db_row['ean'] = expected
        response = converter.get_ean_from_response(product_db_row)

        assert response == expected

    def test_return_empty_ean_when_is_invalid(self, converter, product_db_row):
        product_db_row['ean'] = 'ABCDEFG'
        response = converter.get_ean_from_response(product_db_row)

        assert response == ''

    def test_return_ean_successfully_when_is_numeric(
        self, converter, product_db_row
    ):
        product_db_row['ean'] = 1234
        response = converter.get_ean_from_response(product_db_row)

        assert response == '0000000001234'

    def test_equal_attributes_on_convert_product(
        self, converter, product_db_row, batch_key, sku
    ):
        product_db_row.update({
            'voltage': None,
            'color': 'Azul',
            'specification_id': 13,
            'specification_description': 'Azul'
        })

        converter.from_source([product_db_row])

        items = converter.get_items()
        assert len(items) == 1

        item = items[batch_key][sku]
        attributes = item['attributes']
        assert len(attributes) == 1

        attribute = attributes[0]
        assert attribute['type'] == ProductSpecification.color.name
        assert attribute['value'] == 'Azul'
