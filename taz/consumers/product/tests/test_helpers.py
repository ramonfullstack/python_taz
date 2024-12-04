from unittest.mock import ANY

import pytest

from taz import constants
from taz.constants import MAGAZINE_LUIZA_SELLER_ID, SINGLE_SELLER_STRATEGY
from taz.consumers.product.helpers import ProductHelpers


class TestProductHelpers:

    @pytest.mark.parametrize('value,expected', [
        ('110 v', constants._110VOLTS_DESCRIPTION),
        ('110v', constants._110VOLTS_DESCRIPTION),
        ('110volts', constants._110VOLTS_DESCRIPTION),
        ('110 volts', constants._110VOLTS_DESCRIPTION),
        ('127 v', constants._110VOLTS_DESCRIPTION),
        ('127v', constants._110VOLTS_DESCRIPTION),
        ('127volts', constants._110VOLTS_DESCRIPTION),
        ('127 volts', constants._110VOLTS_DESCRIPTION),
        ('220 v', constants._220VOLTS_DESCRIPTION),
        ('220v', constants._220VOLTS_DESCRIPTION),
        ('220volts', constants._220VOLTS_DESCRIPTION),
        ('220 volts', constants._220VOLTS_DESCRIPTION),
        ('Preto', 'Preto'),
        ('Azul-Marinho', 'Azul-Marinho'),
    ])
    def test_normalize_voltage(self, value, expected):
        product = {'attributes': [{'type': 'voltage', 'value': value}]}
        ProductHelpers.normalize_voltage(product)

        assert product['attributes'][0]['value'] == expected

    def test_merge_categories_returns_success(self, product):
        response = ProductHelpers.merge_categories(product)
        expected = [
            {
                'id': 'GA',
                'subcategories': [{'id': 'GACO'}, {'id': 'XBOX'}]
            }
        ]
        assert response == expected

    def test_merge_categories_returns_duplicated_remove(self):
        product = {
            'main_category': {
                'id': 'GA',
                'subcategory': {
                    'id': 'GACO'
                }
            },
            'categories': [{
                'subcategories': [
                    {'id': 'XBOX'},
                    {'id': 'GACO'}
                ],
                'id': 'GA',
            }],
        }

        response = ProductHelpers.merge_categories(product)
        expected = [
            {
                'id': 'GA',
                'subcategories': [{'id': 'GACO'}, {'id': 'XBOX'}]
            }
        ]

        assert response == expected

    @pytest.mark.parametrize('product, expected', [
        (
            {'description': '<p><strong>Kit Leve 3 Pague 2&nbsp;</strong><strong>Vanish Oxi Action Crystal White 450g'}, # noqa
            '<p><strong>Kit Leve 3 Pague 2 </strong><strong>Vanish Oxi Action Crystal White 450g</strong></p>' # noqa
        ),
        (
            {'description': '<html><head><body><div> Cafeteira elétrica <a> Programável Oster <strong>220V</body>'}, # noqa
            ' Cafeteira elétrica  Programável Oster <strong>220V</strong>'
        ),
    ])
    def test_clear_html_method_in_descriptions(
        self,
        product,
        expected,
    ):
        description = ProductHelpers.clear_html(product['description'])
        assert description == expected

    @pytest.mark.parametrize('input_title,expected_title,seller_id', [
        (
            'FOGAO 4 BOCAS INOX',
            'Fogao 4 bocas inox',
            'seller_a'
        ),
        (
            'PLAYSTATION 5 MidiA DiGiTaL',
            'PLAYSTATION 5 MidiA DiGiTaL',
            MAGAZINE_LUIZA_SELLER_ID
        ),
        (
            'TV LED 32"AOC LE32M1475 HD com 1 USB 2 HDMI VGA TV Digital',
            'TV LED 32"AOC LE32M1475 HD com 1 USB 2 HDMI VGA TV Digital',
            'seller_a'
        )
    ])
    def test_capitalize_fields(
        self,
        product,
        input_title,
        expected_title,
        seller_id
    ):
        product['title'] = input_title
        product['seller_id'] = seller_id

        ProductHelpers.capitalize_fields(product)

        assert product['title'] == expected_title

    @pytest.mark.parametrize(
        'title,'
        'brand,'
        'reference,'
        'expected_reference,'
        'seller_id', [
            (
                'TV LED 32"AOC LE32M1475 HD com 1 USB 2 HDMI VGA TV Digital',
                'Aoc',
                'reference_field',
                '',
                'seller_a'
            ),
            (
                'TV LED 32"AOC LE32M1475 HD com 1 USB 2 HDMI VGA TV Digital',
                'Aoc',
                'reference_field',
                'reference_field',
                MAGAZINE_LUIZA_SELLER_ID
            ),
            (
                'PLAYSTATION 5 MIDIA DIGITAL',
                'Sony',
                'reference_field',
                'Sony',
                'seller_a'
            )
        ]
    )
    def test_format_reference(
        self,
        product,
        title,
        brand,
        reference,
        expected_reference,
        seller_id
    ):
        product['title'] = title
        product['brand'] = brand
        product['reference'] = reference
        product['seller_id'] = seller_id

        ProductHelpers.format_reference(product)

        assert product['reference'] == expected_reference

    @pytest.mark.parametrize('title,reference,expected_full_title', [
        (
            'TV LED 32" LE32M1475 HD com 1 USB 2 HDMI',
            'REFERENCE',
            'TV LED 32" LE32M1475 HD com 1 USB 2 HDMI - REFERENCE'
        ),
        (
            'TV LED 32" LE32M1475 HD com 1 USB 2 HDMI',
            '',
            'TV LED 32" LE32M1475 HD com 1 USB 2 HDMI'
        )
    ])
    def test_get_full_title(
        self,
        product,
        title,
        reference,
        expected_full_title
    ):
        product['title'] = title
        product['reference'] = reference

        full_title = ProductHelpers.get_full_title(product)

        assert full_title == expected_full_title

    @pytest.mark.parametrize('ean,expected_ean', [
        (' 7892509121323 ', '7892509121323'),
        ('7892509121323  ', '7892509121323'),
        (' 7892509121323', '7892509121323')
    ])
    def test_clean_ean_whitespace(
        self,
        product,
        ean,
        expected_ean
    ):
        product['ean'] = ean

        ProductHelpers.clean_ean_whitespace(product)
        assert product['ean'] == expected_ean

    @pytest.mark.parametrize('ean,expected_isbn', [
        ('9788545200345', '9788545200345'),
        ('22694', None),
        ('', None)
    ])
    def test_normalize_isbn(
        self,
        product,
        ean,
        expected_isbn
    ):
        product['ean'] = ean
        ProductHelpers.normalize_isbn(product)

        assert product.get('isbn') == expected_isbn

    @pytest.mark.parametrize('product,seller_info,expected', [
        ({}, {}, False),
        ({'active': True}, {'id': MAGAZINE_LUIZA_SELLER_ID}, False),
        ({'active': False}, {'id': MAGAZINE_LUIZA_SELLER_ID}, True),
        ({'seller_id': MAGAZINE_LUIZA_SELLER_ID}, {'is_active': False}, True),
        ({'seller_id': MAGAZINE_LUIZA_SELLER_ID}, {'is_active': True}, False),
    ])
    def test_convert_product_active(
        self,
        product,
        seller_info,
        expected
    ):
        result = ProductHelpers.convert_product_active(
            product,
            seller_info
        )

        assert result == expected

    def test_format_payload_product(
        self,
        product,
        seller_info
    ):
        payload = ProductHelpers.format_payload_product(
            decoded_product=product,
            seller_info=seller_info,
            grade=10,
            navigation_id=product['navigation_id'],
            matching_strategy=SINGLE_SELLER_STRATEGY,
            md5='123'
        )

        assert {
            'disable_on_matching': False,
            'categories': [
                {
                    'id': 'GA',
                    'subcategories': [
                        {
                            'id': 'GACO'
                        },
                        {
                            'id': 'XBOX'
                        }
                    ]
                }
            ],
            'grade': 10,
            'last_updated_at': ANY,
            'matching_strategy': SINGLE_SELLER_STRATEGY,
            'md5': '123',
            'navigation_id': product['navigation_id'],
            'offer_title': f"{product['title']} - {product['reference']}",
            'seller_description': seller_info['name']
        } == payload
