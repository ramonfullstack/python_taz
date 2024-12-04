
from decimal import Decimal


class ProductSamples:

    @classmethod
    def variation_a(cls):
        return {
            'type': 'product',
            'created_at': '2016-08-17T06:17:03.503000',
            'updated_at': '2016-08-17T06:17:03.503000',
            'sku': '1a2b3c4d5e',
            'navigation_id': '1a2b3c4d5e',
            'parent_sku': '1a2b3c4d5e',
            'seller_id': 'seller_a',
            'seller_description': 'Seller A',
            'brand': '+canecas xablau',
            'title': 'caneca branca 200ml',
            'ean': '312312312312',
            'disable_on_matching': False,
            'grade': 10,
            'categories': [
                {
                    'id': 'UD',
                    'subcategories': [
                        {'id': 'UDCA'}
                    ]
                },
                {
                    'id': 'PR',
                    'subcategories': [
                        {'id': 'PRCA'}
                    ]
                }
            ],
            'attributes': [
                {
                    'type': 'capacity',
                    'value': '200ml'
                },
                {
                    'type': 'color',
                    'value': 'Branca'
                }
            ],
            'sells_to_company': False
        }

    @classmethod
    def variation_b(cls):
        return {
            'type': 'product',
            'sku': '123321123321',
            'navigation_id': '123321123321',
            'parent_sku': '123321123321',
            'seller_id': 'seller_b',
            'seller_description': 'Seller B',
            'brand': '+canecas xablau',
            'title': 'Caneca branca show de bola - 200ml',
            'ean': '312312312312',
            'disable_on_matching': False,
            'grade': 10,
            'categories': [
                {
                    'id': 'UD',
                    'subcategories': [
                        {'id': 'UDCA'}
                    ]
                },
                {
                    'id': 'PR',
                    'subcategories': [
                        {'id': 'PRCA'}
                    ]
                }
            ],
            'attributes': [
                {
                    'type': 'capacity',
                    'value': '400ml'
                },
                {
                    'type': 'color',
                    'value': 'Preta'
                }
            ],
            'sells_to_company': False
        }

    @classmethod
    def disabled_variation(cls):
        '''
        This variation should be part of any matching even with
        'disable_on_matching' positively flagged due to 2021 fix
        '''
        return {
            'type': 'product',
            'sku': '456654abccba',
            'navigation_id': '456654abccba',
            'parent_sku': '456654abccba',
            'seller_id': 'seller_c',
            'seller_description': 'Seller C',
            'brand': '+canecas xablau',
            'title': 'caneca branca - 200ml',
            'ean': '312312312312',
            'disable_on_matching': True,
            'grade': 10,
            'categories': [
                {
                    'id': 'UD',
                    'subcategories': [
                        {'id': 'UDCA'}
                    ]
                },
                {
                    'id': 'PR',
                    'subcategories': [
                        {'id': 'PRCA'}
                    ]
                }
            ],
            'sells_to_company': False,
            'attributes': [
                {
                    'type': 'capacity',
                    'value': '400ml'
                },
                {
                    'type': 'color',
                    'value': 'Preta'
                }
            ]
        }

    @classmethod
    def unmatched_ml_variation(cls):
        return {
            'type': 'product',
            'sku': '98765',
            'navigation_id': '98765',
            'parent_sku': '98765',
            'seller_id': 'magazineluiza',
            'seller_description': 'Magazine Luiza',
            'brand': '+Canecas Xablau',
            'title': 'Caneca Xablau Branca - 200ml',
            'ean': '312312312312',
            'disable_on_matching': False,
            'grade': 1000,
            'categories': [
                {
                    'id': 'UD',
                    'subcategories': [
                        {'id': 'UDCA'}
                    ]
                },
                {
                    'id': 'PR',
                    'subcategories': [
                        {'id': 'PRCA'}
                    ]
                }
            ],
            'sells_to_company': False,
            'attributes': [
                {
                    'type': 'capacity',
                    'value': '400ml'
                },
                {
                    'type': 'color',
                    'value': 'Preta'
                }
            ]
        }

    @classmethod
    def variation_without_parent_reference(cls):
        return {
            'type': 'product',
            'created_at': '2016-08-17T06:17:03.503000',
            'updated_at': '2016-08-17T06:17:03.503000',
            'sold_count': 53,
            'review_count': 2,
            'review_score': 4.3,
            'sku': '723uwej2u3',
            'navigation_id': '723uwej2u3',
            'main_variation': False,
            'parent_sku': '723uwej2u3',
            'seller_id': 'casaamerica',
            'seller_description': 'Casa America',
            'brand': '+Canecas Xablau',
            'title': 'Caneca Xablau Branca - 150ml',
            'description': 'Caneca lero opa xa blau yo',
            'reference': 'CXB150ML',
            'ean': '8888887775120',
            'disable_on_matching': False,
            'grade': 10,
            'categories': [
                {
                    'id': 'UD',
                    'subcategories': [
                        {'id': 'UDCA'}
                    ]
                },
                {
                    'id': 'PR',
                    'subcategories': [
                        {'id': 'PRCA'}
                    ]
                }
            ],
            'dimensions': {
                'width': 0.18,
                'depth': 0.13,
                'weight': 0.47,
                'height': 0.44
            },
            'attributes': [
                {
                    'type': 'capacity',
                    'value': '150ml'
                }
            ],
            'sells_to_company': False
        }

    @classmethod
    def variation_a_with_parent(cls):
        return {
            'type': 'product',
            'created_at': '2016-08-17T06:17:03.503000',
            'updated_at': '2016-08-17T06:17:03.503000',
            'sold_count': 82,
            'review_count': 5,
            'review_score': 3.3,
            'sku': '819283iqw',
            'navigation_id': '819283iqw',
            'main_variation': False,
            'parent_sku': '819283iqw',
            'seller_id': 'seuzeh',
            'seller_description': 'Seu Zeh',
            'brand': '+Canecas Xablau',
            'title': 'Caneca Xablau Branca - 200ml',
            'description': 'Caneca xablau xaplex lero lero',
            'reference': 'CXB200ML',
            'ean': '3123123123120',
            'disable_on_matching': False,
            'grade': 10,
            'categories': [
                {
                    'id': 'UD',
                    'subcategories': [
                        {'id': 'UDCA'}
                    ]
                }
            ],
            'dimensions': {
                'width': 0.18,
                'depth': 0.13,
                'weight': 0.47,
                'height': 0.44
            },
            'attributes': [
                {
                    'type': 'capacity',
                    'value': '200ml'
                }
            ],
            'sells_to_company': False
        }

    @classmethod
    def ml_parent_variation(cls):
        return {
            'type': 'product',
            'created_at': '2016-08-17T06:17:03.503000',
            'updated_at': '2016-08-17T06:17:03.503000',
            'sold_count': 12,
            'review_count': 5,
            'review_score': 4.6,
            'sku': '623728900',
            'navigation_id': '623728900',
            'main_variation': False,
            'parent_sku': '623728900',
            'seller_id': 'magazineluiza',
            'seller_description': 'Magazine Luiza',
            'brand': '+Canecas Xablau',
            'title': 'Caneca Xablau Branca - 200ml',
            'description': 'Canequinha branca lindeza total, xaplex xablau',
            'reference': 'CXB200ML',
            'ean': '3123123123120',
            'disable_on_matching': False,
            'grade': 1000,
            'categories': [
                {
                    'id': 'UD',
                    'subcategories': [
                        {'id': 'UDCA'}
                    ]
                }
            ],
            'dimensions': {
                'width': 0.18,
                'depth': 0.13,
                'weight': 0.47,
                'height': 0.44
            },
            'attributes': [
                {
                    'type': 'capacity',
                    'value': '200ml'
                }
            ],
            'sells_to_company': False
        }

    @classmethod
    def ml_variation_a_with_parent(cls):
        return {
            'type': 'product',
            'created_at': '2016-08-17T06:17:03.503000',
            'updated_at': '2016-08-17T06:17:03.503000',
            'sold_count': 31,
            'review_count': 6,
            'review_score': 4.6,
            'main_variation': True,
            'sku': '723829300',
            'navigation_id': '723829300',
            'parent_sku': '623728900',
            'seller_id': 'magazineluiza',
            'seller_description': 'Magazine Luiza',
            'brand': '+Canecas Xablau',
            'title': 'Caneca Xablau Branca - 250ml',
            'description': 'Caneca xablau branca belezinha',
            'reference': 'CXB250ML',
            'ean': '3123123123930',
            'disable_on_matching': False,
            'grade': 1000,
            'categories': [
                {
                    'id': 'UD',
                    'subcategories': [
                        {'id': 'UDCA'}
                    ]
                }
            ],
            'dimensions': {
                'width': 0.18,
                'depth': 0.13,
                'weight': 0.47,
                'height': 0.44
            },
            'attributes': [
                {
                    'type': 'capacity',
                    'value': '250ml'
                }
            ],
            'sells_to_company': False
        }

    @classmethod
    def unmatched_ml_variation_with_parent(cls):
        return {
            'type': 'product',
            'created_at': '2016-08-17T06:17:03.503000',
            'updated_at': '2016-08-17T06:17:03.503000',
            'sold_count': 14,
            'review_count': 8,
            'review_score': 4.6,
            'main_variation': False,
            'sku': '8weuwe88we',
            'navigation_id': '8weuwe88we',
            'parent_sku': '623728900',
            'seller_id': 'magazineluiza',
            'seller_description': 'Magazine Luiza',
            'brand': '+Canecas Xablau',
            'title': 'Caneca Xablau Branca - 350ml',
            'description': 'Caneca xablau joinha',
            'reference': 'CXB350ML',
            'ean': '3123123123990',
            'disable_on_matching': False,
            'grade': 2000,
            'categories': [
                {
                    'id': 'UD',
                    'subcategories': [
                        {'id': 'UDCA'},
                        {'id': 'UDCG'}
                    ]
                }
            ],
            'dimensions': {
                'width': 0.18,
                'depth': 0.13,
                'weight': 0.47,
                'height': 0.44
            },
            'attributes': [
                {
                    'type': 'capacity',
                    'value': '350ml'
                }
            ],
            'sells_to_company': False
        }

    @classmethod
    def seller_a_variation_with_parent(cls):
        return {
            'type': 'product',
            'created_at': '2016-08-17T06:17:03.503000',
            'updated_at': '2016-08-17T06:17:03.503000',
            'sold_count': 14,
            'review_count': 9,
            'review_score': 4.1,
            'main_variation': False,
            'sku': '82323jjjj3',
            'navigation_id': '82323jjjj3',
            'parent_sku': '82323jjjj3',
            'seller_id': 'seller_a',
            'seller_description': 'Seller A',
            'brand': '+Canecas Xablau',
            'title': 'Caneca Xablau Branca - 450ml',
            'description': 'Caneca xablau batuta',
            'reference': 'CXB450ML',
            'ean': '3123123999999',
            'disable_on_matching': False,
            'grade': 500,
            'categories': [
                {
                    'id': 'UD',
                    'subcategories': [
                        {'id': 'UDCA'},
                        {'id': 'UDCG'}
                    ]
                }
            ],
            'dimensions': {
                'width': 0.18,
                'depth': 0.13,
                'weight': 0.47,
                'height': 0.44
            },
            'attributes': [
                {
                    'type': 'capacity',
                    'value': '450ml'
                }
            ],
            'sells_to_company': False,
            'matching_uuid': 'a0069aee16d441cab4030cce086debbc',
            'extra_data': [{'name': 'is_magalu_indica', 'value': 'true'}],
            'active': True
        }

    @classmethod
    def seller_b_variation_with_parent(cls):
        return {
            'type': 'product',
            'created_at': '2016-08-17T06:17:03.503000',
            'updated_at': '2016-08-17T06:17:03.503000',
            'sold_count': 14,
            'review_score': 2.1,
            'main_variation': False,
            'sku': '098asdwe28',
            'navigation_id': '0123456',
            'parent_sku': '098asdwe28',
            'seller_id': 'seller_b',
            'seller_description': 'Seller B GMBH',
            'brand': '+Canecas Xablau',
            'title': 'Caneca Xablau Branca - 450ml',
            'description': 'Caneca xablau bacanuda',
            'reference': 'CXB450ML',
            'ean': '3123123999999',
            'disable_on_matching': False,
            'grade': 500,
            'categories': [
                {
                    'id': 'UD',
                    'subcategories': [
                        {'id': 'UDCA'},
                        {'id': 'UDCG'}
                    ]
                }
            ],
            'dimensions': {
                'width': 0.18,
                'depth': 0.13,
                'weight': 0.47,
                'height': 0.44
            },
            'attributes': [
                {
                    'type': 'capacity',
                    'value': '450ml'
                }
            ],
            'sells_to_company': False,
            'matching_uuid': 'a0069aee16d441cab4030cce086debbc',
            'extra_data': [{'name': 'is_magalu_indica', 'value': 'true'}],
            'active': True
        }

    @classmethod
    def seller_c_variation_with_parent(cls):
        return {
            'type': 'product',
            'created_at': '2016-08-17T06:17:03.503000',
            'updated_at': '2016-08-17T06:17:03.503000',
            'sold_count': 14,
            'review_count': 1,
            'review_score': 5,
            'main_variation': False,
            'sku': 'ou23ou23ou',
            'navigation_id': 'ou23ou23ou',
            'parent_sku': 'ou23ou23ou',
            'seller_id': 'seller_c',
            'seller_description': 'Seller C Ltda',
            'brand': '+Canecas Xablau',
            'title': 'Caneca Xablau Branca - 450ml',
            'description': 'Caneca xablau bacaninha',
            'reference': 'CXB450ML',
            'ean': '3123123999999',
            'disable_on_matching': False,
            'grade': 500,
            'categories': [
                {
                    'id': 'UD',
                    'subcategories': [
                        {'id': 'UDCA'},
                        {'id': 'UDCG'}
                    ]
                }
            ],
            'dimensions': {
                'width': 0.18,
                'depth': 0.13,
                'weight': 0.47,
                'height': 0.44
            },
            'attributes': [
                {
                    'type': 'capacity',
                    'value': '450ml'
                }
            ],
            'sells_to_company': False
        }

    @classmethod
    def seller_d_variation_with_parent(cls):
        return {
            'type': 'product',
            'created_at': '2016-08-17T06:17:03.503000',
            'updated_at': '2016-08-17T06:17:03.503000',
            'sold_count': 14,
            'review_count': 1,
            'review_score': 5,
            'main_variation': False,
            'sku': '0123456',
            'navigation_id': '0123456',
            'parent_sku': '0123456',
            'seller_id': 'seller_d',
            'seller_description': 'Seller D Ltda',
            'brand': '+Canecas Xablau',
            'title': 'Caneca Xablau Branca - 450ml',
            'description': 'Caneca xablau bacaninha',
            'reference': 'CXB450ML',
            'ean': '3123123999999',
            'disable_on_matching': False,
            'grade': 500,
            'categories': [
                {
                    'id': 'UD',
                    'subcategories': [
                        {'id': 'UDCA'},
                        {'id': 'UDCG'}
                    ]
                }
            ],
            'dimensions': {
                'width': 0.18,
                'depth': 0.13,
                'weight': 0.47,
                'height': 0.44
            },
            'attributes': [
                {
                    'type': 'capacity',
                    'value': '450ml'
                }
            ],
            'sells_to_company': False
        }

    @classmethod
    def variation_without_ean(cls):
        return {
            'created_at': '2016-08-17T06:17:03.503000',
            'updated_at': '2016-08-17T06:17:03.503000',
            'sold_count': 53,
            'review_count': 3,
            'review_score': 3.1,
            'sku': '72384uoueg',
            'navigation_id': '72384uoueg',
            'main_variation': False,
            'parent_sku': '72384uoueg',
            'seller_id': 'seujoao',
            'seller_description': 'Seu Joao',
            'brand': '+Canecas Xablau',
            'title': 'Caneca Xablau Branca - 150ml',
            'description': 'Caneca lero opa xa blau yo',
            'reference': 'CXB150ML',
            'disable_on_matching': False,
            'grade': 0,
            'categories': [
                {
                    'id': 'UD',
                    'subcategories': [
                        {'id': 'UDCA'}
                    ]
                },
                {
                    'id': 'PR',
                    'subcategories': [
                        {'id': 'PRCA'}
                    ]
                }
            ],
            'dimensions': {
                'width': 0.18,
                'depth': 0.13,
                'weight': 0.47,
                'height': 0.44
            },
            'attributes': [
                {
                    'type': 'capacity',
                    'value': '150ml'
                }
            ],
            'sells_to_company': False
        }

    @classmethod
    def variation_without_ean_and_attributes(cls):
        return {
            'created_at': '2016-08-17T06:17:03.503000',
            'updated_at': '2016-08-17T06:17:03.503000',
            'sold_count': 53,
            'review_count': 3,
            'review_score': 3.1,
            'sku': '72384uoueg',
            'navigation_id': '72384uoueg',
            'main_variation': False,
            'parent_sku': '72384uoueg',
            'seller_id': 'seujoao',
            'seller_description': 'Seu Joao',
            'brand': '+Canecas Xablau',
            'title': 'Caneca Xablau Branca - 150ml',
            'description': 'Caneca lero opa xa blau yo',
            'reference': 'CXB150ML',
            'disable_on_matching': False,
            'grade': 0,
            'categories': [
                {
                    'id': 'UD',
                    'subcategories': [
                        {'id': 'UDCA'}
                    ]
                },
                {
                    'id': 'PR',
                    'subcategories': [
                        {'id': 'PRCA'}
                    ]
                }
            ],
            'dimensions': {
                'width': 0.18,
                'depth': 0.13,
                'weight': 0.47,
                'height': 0.44
            },
            'sells_to_company': False
        }

    @classmethod
    def variation_without_attributes_but_with_ean_trustable(cls):
        return {
            'created_at': '2016-08-17T06:17:03.503000',
            'updated_at': '2016-08-17T06:17:03.503000',
            'sold_count': 53,
            'review_count': 3,
            'review_score': 3.1,
            'sku': '72384uoueg',
            'navigation_id': '72384uoueg',
            'main_variation': False,
            'parent_sku': '72384uoueg',
            'seller_id': 'seujoao',
            'seller_description': 'Seu Joao',
            'brand': '+Canecas Xablau',
            'title': 'Caneca Xablau Branca - 150ml',
            'description': 'Caneca lero opa xa blau yo',
            'reference': 'CXB150ML',
            'disable_on_matching': False,
            'grade': 0,
            'ean': '3123123123120',
            'categories': [
                {
                    'id': 'UD',
                    'subcategories': [
                        {'id': 'UDCA'}
                    ]
                },
                {
                    'id': 'PR',
                    'subcategories': [
                        {'id': 'PRCA'}
                    ]
                }
            ],
            'dimensions': {
                'width': 0.18,
                'depth': 0.13,
                'weight': 0.47,
                'height': 0.44
            },
            'sells_to_company': False
        }

    @classmethod
    def variation_without_ean_but_with_attributes(cls):
        return {
            'created_at': '2016-08-17T06:17:03.503000',
            'updated_at': '2016-08-17T06:17:03.503000',
            'sold_count': 53,
            'review_count': 3,
            'review_score': 3.1,
            'sku': '72384uoueg',
            'navigation_id': '72384uoueg',
            'main_variation': False,
            'parent_sku': '72384uoueg',
            'seller_id': 'seujoao',
            'seller_description': 'Seu Joao',
            'brand': '+Canecas Xablau',
            'title': 'Caneca Xablau Branca - 150ml',
            'description': 'Caneca lero opa xa blau yo',
            'reference': 'CXB150ML',
            'disable_on_matching': False,
            'grade': 0,
            'ean': '3123123123120',
            'categories': [
                {
                    'id': 'UD',
                    'subcategories': [
                        {'id': 'UDCA'}
                    ]
                },
                {
                    'id': 'PR',
                    'subcategories': [
                        {'id': 'PRCA'}
                    ]
                }
            ],
            'dimensions': {
                'width': 0.18,
                'depth': 0.13,
                'weight': 0.47,
                'height': 0.44
            },
            'attributes': [
                {
                    'type': 'capacity',
                    'value': '450ml'
                }
            ],
            'sells_to_company': False
        }

    @classmethod
    def ml_matching_product_variation_a_110(cls):
        return {
            'sold_count': 0,
            'attributes': [{
                'type': 'voltage',
                'value': '110 Volts',
            }],
            'brand': 'skymsen',
            'title': 'Liquidificador Industrial 1 Velocidade 1, 5L Inox',
            'main_variation': True,
            'dimensions': {
                'depth': 0.46,
                'height': 0.55,
                'weight': 2.5,
                'width': 0.39
            },
            'ean': '7895707474246',
            'categories': [{
                'subcategories': [{
                    'id': 'LIQI',
                    'description': 'Liquidificadores industriais'
                }],
                'id': 'PI',
                'description': 'Linha Industrial'
            }],
            'created_at': '2014-12-20T08:04:00.270000',
            'review_score': 0,
            'review_count': 0,
            'type': 'product',
            'seller_id': 'magazineluiza',
            'seller_description': 'Magazine Luiza',
            'reference': 'Skymsen',
            'sku': '212410700',
            'navigation_id': '212410700',
            'description': 'Liquidificador Industrial 1, 5 litro da Skymsen. Liquidificador com gabinete em inox, com copo plástico e alta rotação, ideal para preparar diversos sucos e vitaminas a base de frutas naturais ou polpas congeladas. Tem ainda chave liga/desliga e função pulsar, além de acoplamento com sistema de auto compensação, facilitando o encaixe e permitindo a intercambiabilidade de copos.',  # noqa
            'updated_at': '2016-08-22T06:17:17.833000',
            'grade': 10,
            'disable_on_matching': False,
            'parent_sku': '2124107',
            'sells_to_company': False
        }

    @classmethod
    def ml_matching_product_variation_a_220(cls):
        return {
            'sold_count': 0,
            'attributes': [{
                'type': 'voltage',
                'value': '220 Volts',
            }],
            'brand': 'skymsen',
            'title': 'Liquidificador Industrial 1 Velocidade 1, 5L Inox',
            'main_variation': False,
            'dimensions': {
                'depth': 0.46,
                'height': 0.55,
                'weight': 2.5,
                'width': 0.39
            },
            'ean': '7895707474253',
            'categories': [{
                'subcategories': [{
                    'id': 'LIQI',
                    'description': 'Liquidificadores industriais'
                }],
                'id': 'PI',
                'description': 'Linha Industrial'
            }],
            'created_at': '2014-12-20T08:04:00.270000',
            'review_score': 0,
            'review_count': 0,
            'type': 'product',
            'seller_id': 'magazineluiza',
            'seller_description': 'Magazine Luiza',
            'reference': 'Skymsen',
            'sku': '212410800',
            'navigation_id': '212410800',
            'description': 'Liquidificador Industrial 1, 5 litro da Skymsen. Liquidificador com gabinete em inox, com copo plástico e alta rotação, ideal para preparar diversos sucos e vitaminas a base de frutas naturais ou polpas congeladas. Tem ainda chave liga/desliga e função pulsar, além de acoplamento com sistema de auto compensação, facilitando o encaixe e permitindo a intercambiabilidade de copos.',  # noqa
            'updated_at': '2016-05-15T16:52:18.770000',
            'grade': 10,
            'disable_on_matching': False,
            'parent_sku': '2124107',
            'sells_to_company': False
        }

    @classmethod
    def ml_matching_product_variation_b_110(cls):
        return {
            'sold_count': 0,
            'attributes': [{
                'type': 'voltage',
                'value': '110 Volts',
            }],
            'brand': 'skymsen',
            'title': 'Liquidificador Industrial 1 Velocidade 1, 5L Inox',
            'main_variation': True,
            'dimensions': {
                'depth': 0.46,
                'height': 0.55,
                'weight': 3.6,
                'width': 0.39
            },
            'ean': '7895707474284',
            'categories': [{
                'subcategories': [{
                    'id': 'LIQI',
                    'description': 'Liquidificadores industriais'
                }],
                'id': 'PI',
                'description': 'Linha Industrial'
            }],
            'created_at': '2014-12-20T08:04:00.270000',
            'review_score': 0,
            'review_count': 0,
            'type': 'product',
            'seller_id': 'magazineluiza',
            'seller_description': 'Magazine Luiza',
            'reference': 'Skymsen',
            'sku': '212410900',
            'navigation_id': '212410900',
            'description': 'Liquidificador Industrial 1, 5 litro da Skymsen. Liquidificador com gabinete em inox, com copo de vidro e alta rotação, ideal para preparar diversos sucos e vitaminas a base de frutas naturais ou polpas congeladas. Tem ainda chave liga/desliga e função pulsar, além de acoplamento com sistema de auto compensação, facilitando o encaixe e permitindo a intercambiabilidade de copos.',  # noqa
            'updated_at': '2016-08-22T06:17:17.833000',
            'grade': 10,
            'disable_on_matching': False,
            'parent_sku': '2124109',
            'sells_to_company': False
        }

    @classmethod
    def ml_matching_product_variation_b_220(cls):
        return {
            'sold_count': 0,
            'attributes': [{
                'type': 'voltage',
                'value': '220 Volts',
            }],
            'brand': 'skymsen',
            'title': 'Liquidificador Industrial 1 Velocidade 1, 5L Inox',
            'main_variation': False,
            'dimensions': {
                'depth': 0.46,
                'height': 0.55,
                'weight': 3.6,
                'width': 0.39
            },
            'ean': '7895707474291',
            'categories': [{
                'subcategories': [{
                    'id': 'LIQI',
                    'description': 'Liquidificadores industriais'
                }],
                'id': 'PI',
                'description': 'Linha Industrial'
            }],
            'created_at': '2014-12-20T08:04:00.270000',
            'review_score': 0,
            'review_count': 0,
            'type': 'product',
            'seller_id': 'magazineluiza',
            'seller_description': 'Magazine Luiza',
            'reference': 'Skymsen',
            'sku': '212411000',
            'navigation_id': '212411000',
            'description': 'Liquidificador Industrial 1, 5 litro da Skymsen. Liquidificador com gabinete em inox, com copo de vidro e alta rotação, ideal para preparar diversos sucos e vitaminas a base de frutas naturais ou polpas congeladas. Tem ainda chave liga/desliga e função pulsar, além de acoplamento com sistema de auto compensação, facilitando o encaixe e permitindo a intercambiabilidade de copos.',  # noqa
            'updated_at': '2015-10-22T17:54:54.050000',
            'grade': 10,
            'disable_on_matching': False,
            'parent_sku': '2124109',
            'sells_to_company': False
        }

    @classmethod
    def ml_matching_product_variation_c_110(cls):
        return {
            'sold_count': 0,
            'attributes': [{
                'type': 'voltage',
                'value': '110 Volts',
            }],
            'brand': 'skymsen',
            'title': 'Liquidificador Industrial 1 Velocidade 1, 5L Inox',
            'main_variation': True,
            'dimensions': {
                'depth': 0.46,
                'height': 0.55,
                'weight': 2.6,
                'width': 0.39
            },
            'ean': '7895707474321',
            'categories': [{
                'subcategories': [{
                    'id': 'LIQI',
                    'description': 'Liquidificadores industriais'
                }],
                'id': 'PI',
                'description': 'Linha Industrial'
            }],
            'created_at': '2014-12-20T08:04:00.270000',
            'review_score': 0,
            'review_count': 0,
            'type': 'product',
            'seller_id': 'magazineluiza',
            'seller_description': 'Magazine Luiza',
            'reference': 'Skymsen',
            'sku': '212411100',
            'navigation_id': '212411100',
            'description': 'Liquidificador Industrial 1, 5 litro da Skymsen. Liquidificador com gabinete e copo em inox, alta rotação, ideal para preparar diversos sucos e vitaminas a base de frutas naturais ou polpas congeladas. Tem ainda chave liga/desliga e função pulsar, além de acoplamento com sistema de auto compensação, facilitando o encaixe e permitindo a intercambiabilidade de copos.',  # noqa
            'updated_at': '2016-08-22T06:17:17.833000',
            'grade': 10,
            'disable_on_matching': False,
            'parent_sku': '2124111',
            'sells_to_company': False
        }

    @classmethod
    def ml_matching_product_variation_c_220(cls):
        return {
            'sold_count': 0,
            'attributes': [{
                'type': 'voltage',
                'value': '220 Volts',
            }],
            'brand': 'skymsen',
            'title': 'Liquidificador Industrial 1 Velocidade 1, 5L Inox',
            'main_variation': False,
            'dimensions': {
                'depth': 0.46,
                'height': 0.55,
                'weight': 2.6,
                'width': 0.39
            },
            'ean': '7895707474338',
            'categories': [{
                'subcategories': [{
                    'id': 'LIQI',
                    'description': 'Liquidificadores industriais'
                }],
                'id': 'PI',
                'description': 'Linha Industrial'
            }],
            'created_at': '2014-12-20T08:04:00.270000',
            'review_score': 0,
            'review_count': 0,
            'type': 'product',
            'seller_id': 'magazineluiza',
            'seller_description': 'Magazine Luiza',
            'reference': 'Skymsen',
            'sku': '212411200',
            'navigation_id': '212411200',
            'description': 'Liquidificador Industrial 1, 5 litro da Skymsen. Liquidificador com gabinete e copo em inox, alta rotação, ideal para preparar diversos sucos e vitaminas a base de frutas naturais ou polpas congeladas. Tem ainda chave liga/desliga e função pulsar, além de acoplamento com sistema de auto compensação, facilitando o encaixe e permitindo a intercambiabilidade de copos.',  # noqa
            'updated_at': '2016-05-15T16:52:18.770000',
            'grade': 10,
            'disable_on_matching': False,
            'parent_sku': '2124111',
            'sells_to_company': False
        }

    @classmethod
    def mkp_matching_product_variation_a_shovel(cls):
        return {
            'main_variation': True,
            'ean': '0047875899999',
            'seller_description': 'Jardineiro do Jardim',
            'title': 'Pa do zezinho',
            'grade': 10,
            'created_at': '2014-10-07T07:13:02.140000',
            'reference': 'PZ',
            'description': 'Pa do zezin',
            'parent_sku': '2104681',
            'disable_on_matching': False,
            'type': 'product',
            'sold_count': 0,
            'seller_id': 'jardineirodojardim',
            'review_count': 0,
            'updated_at': '2015-03-02T10:41:43.470000',
            'dimensions': {
                'width': 0.15,
                'depth': 0.02,
                'height': 0.14,
                'weight': 0.2
            },
            'review_score': 0,
            'brand': 'activision',
            'sku': '623',
            'navigation_id': '623',
            'attributes': [
                {'value': 'Verde', 'type': 'color'}
            ],
            'categories': [
                {
                    'id': 'GA',
                    'subcategories': [
                        {'id': 'GAJP'},
                        {'id': 'GAP3'},
                        {'id': 'GCOD'}
                    ]
                }
            ],
            'sells_to_company': False
        }

    @classmethod
    def ml_matching_product_variation_a_ps3(cls):
        return {
            'main_variation': True,
            'ean': '0047875873667',
            'seller_description': 'Magazine Luiza',
            'title': 'Call of Duty - Advanced Warfare para PS3',
            'grade': 1010,
            'created_at': '2014-10-07T07:13:02.140000',
            'reference': 'Activision',
            'description': 'Activision',
            'parent_sku': '2104681',
            'disable_on_matching': False,
            'type': 'product',
            'sold_count': 0,
            'seller_id': 'magazineluiza',
            'review_count': 0,
            'updated_at': '2015-03-02T10:41:43.470000',
            'dimensions': {
                'width': 0.15,
                'depth': 0.02,
                'height': 0.14,
                'weight': 0.2
            },
            'review_score': 0,
            'brand': 'activision',
            'sku': '210468100',
            'navigation_id': '210468100',
            'attributes': [
                {'value': 'PS3', 'type': 'console'}
            ],
            'categories': [
                {
                    'id': 'GA',
                    'subcategories': [
                        {'id': 'GAJP'},
                        {'id': 'GAP3'},
                        {'id': 'GCOD'}
                    ]
                }
            ],
            'sells_to_company': False
        }

    @classmethod
    def ml_matching_product_variation_b_ps4(cls):
        return {
            'main_variation': False,
            'sku': '210468400',
            'navigation_id': '210468400',
            'seller_description': 'Magazine Luiza',
            'title': 'Call of Duty - Advanced Warfare para PS4',
            'dimensions': {
                'width': 0.15,
                'depth': 0.02,
                'height': 0.14,
                'weight': 0.2
            },
            'reference': 'Activision - Pré-venda',
            'description': 'Activision - Pré-venda',
            'parent_sku': '2104681',
            'updated_at': '2016-05-15T16:52:18.770000',
            'grade': 1010,
            'brand': 'activision',
            'review_score': 0,
            'categories': [
                {
                    'id': 'GA',
                    'subcategories': [
                        {'id': 'GAP4'},
                        {'id': 'GASC'},
                        {'id': 'GJPS'},
                        {'id': 'JPRE'}
                    ]
                }
            ],
            'ean': '0047875873698',
            'attributes': [
                {'value': 'PS4', 'type': 'console'}
            ],
            'release_date': '2014-11-04T00:00:00',
            'created_at': '2014-10-07T07:13:02.140000',
            'sold_count': 0,
            'type': 'product',
            'disable_on_matching': False,
            'seller_id': 'magazineluiza',
            'review_count': 0,
            'sells_to_company': False
        }

    @classmethod
    def ml_matching_product_variation_c_xbox(cls):
        return {
            'main_variation': False,
            'sku': '210468200',
            'navigation_id': '210468200',
            'seller_description': 'Magazine Luiza',
            'title': 'Call of Duty - Advanced Warfare para Xbox 360',
            'dimensions': {
                'width': 0.15,
                'depth': 0.02,
                'height': 0.14,
                'weight': 0.2
            },
            'reference': 'Activision - Pré-venda',
            'description': 'Activision - Pré-venda',
            'parent_sku': '2104681',
            'updated_at': '2016-05-15T16:52:18.770000',
            'grade': 1010,
            'brand': 'activision',
            'review_score': 0,
            'categories': [
                {
                    'id': 'GA',
                    'subcategories': [
                        {'id': 'GAJX'},
                        {'id': 'GAXB'},
                        {'id': 'GCOD'},
                        {'id': 'JPRE'}
                    ]
                }
            ],
            'ean': '0047875873728',
            'attributes': [
                {'value': 'XBOX', 'type': 'console'}
            ],
            'release_date': '2014-11-04T00:00:00',
            'created_at': '2014-10-07T07:13:02.140000',
            'sold_count': 0,
            'type': 'product',
            'disable_on_matching': False,
            'seller_id': 'magazineluiza',
            'review_count': 0,
            'sells_to_company': False
        }

    @classmethod
    def matching_product_variation_a_110(
        cls, seller_id=None, seller_description=None,
        ean=None, parent_sku=None, sku=None
    ):
        return {
            'categories': [{
                'subcategories': [
                    {'id': 'ARVC'},
                    {'id': 'ARVM'},
                    {'id': 'ARVP'}
                ],
                'id': 'AR'
            }],
            'created_at': '2014-08-26T07:24:11.887000',
            'type': 'product',
            'disable_on_matching': False,
            'title': 'Ventilador de Mesa e Parede Mondial NV-15-6P 6 Pás',
            'description': 'Ventilador de mesa e parede da Mondial.',
            'grade': 10,
            'parent_sku': parent_sku,
            'reference': '3 Velocidades Branco e Azul',
            'main_variation': True,
            'seller_description': seller_description,
            'ean': ean,
            'sku': sku,
            'navigation_id': sku,
            'seller_id': seller_id,
            'sold_count': 0,
            'attributes': [{
                'value': '110 Volts',
                'type': 'voltage',
            }],
            'dimensions': {
                'depth': 0.22,
                'height': 0.36,
                'width': 0.35,
                'weight': 2.09
            },
            'review_count': 0,
            'brand': 'mondial',
            'updated_at': '2016-05-15T16:52:18.770000',
            'review_score': 0,
            'sells_to_company': False
        }

    @classmethod
    def matching_product_variation_a_220(
        cls, seller_id=None, seller_description=None,
        ean=None, parent_sku=None, sku=None
    ):
        return {
            'categories': [{
                'subcategories': [
                    {'id': 'ARVC'},
                    {'id': 'ARVM'},
                    {'id': 'ARVP'}
                ],
                'id': 'AR'
            }],
            'created_at': '2014-08-26T07:24:11.887000',
            'type': 'product',
            'disable_on_matching': False,
            'title': 'Ventilador de Mesa e Parede Mondial NV-15-6P 6 Pás',
            'description': 'Ventilador de mesa e parede da Mondial.',
            'grade': 10,
            'reference': '3 Velocidades Branco e Azul',
            'main_variation': False,
            'seller_description': seller_description,
            'ean': ean,
            'parent_sku': parent_sku,
            'sku': sku,
            'navigation_id': sku,
            'seller_id': seller_id,
            'sold_count': 0,
            'attributes': [{
                'value': '220 Volts',
                'type': 'voltage',
            }],
            'dimensions': {
                'depth': 0.22,
                'height': 0.36,
                'width': 0.35,
                'weight': 2.09
            },
            'review_count': 0,
            'brand': 'mondial',
            'updated_at': '2016-05-15T16:52:18.770000',
            'review_score': 0,
            'sells_to_company': False
        }

    @classmethod
    def matching_magoo_product(cls):
        return {
            'type': 'product',
            'sold_count': 0,
            'brand': 'Galzerano',
            'disable_on_matching': False,
            'dimensions': {
                'height': 38,
                'depth': 78,
                'weight': 2770,
                'width': 46
            },
            'categories': [{
                'description': 'Bebê',
                'id': 'BB',
                'subcategories': [{
                    'description': 'Bebê Conforto',
                    'id': 'BECO'
                }]
            }],
            'description': 'Mais que uma marca, nasce o conceito',
            'sku': '74609497',
            'navigation_id': '74609497',
            'grade': 10,
            'created_at': '2016-08-16T14:55:23.352355+00:00',
            'seller_description': 'Magoo Baby',
            'parent_sku': '74605773',
            'review_count': 0,
            'reference': 'Galzerano',
            'title': 'Bebê Conforto Piccolina Cinza Off 0 a 13 KG - Galzerano',
            'main_variation': True,
            'updated_at': '2016-09-14T20:07:00.552522+00:00',
            'release_date': '2016-09-14T20:07:03.614789+00:00',
            'review_score': 5,
            'seller_id': 'magoobaby',
            'ean': '7898089226762',
            'sells_to_company': False
        }

    @classmethod
    def matching_ml_product_with_magoo(cls):
        return {
            'disable_on_matching': False,
            'sold_count': 0,
            'reference': 'para Crianças até 13kg',
            'brand': 'galzerano',
            'ean': '7898089226762',
            'main_variation': True,
            'selections': {
                '7985': ['12669'],
                '0': [
                    '10709', '10811', '12416', '8079',
                    '8162', '9303', '9356', '9972'
                ]
            },
            'seller_description': 'Magazine Luiza',
            'seller_id': 'magazineluiza',
            'grade': 10,
            'categories': [{
                'id': 'BB',
                'subcategories': [
                    {'id': 'BBGL'},
                    {'id': 'CADA'},
                    {'id': 'CD18'}
                ]
            }],
            'review_score': 0,
            'title': 'Cadeira para Auto Galzerano Piccolina',
            'dimensions': {
                'depth': 0.4,
                'height': 0.69,
                'width': 0.31,
                'weight': 3.43
            },
            'created_at': '2014-04-25T06:51:25.310000',
            'parent_sku': '0858030',
            'sku': '085803000',
            'navigation_id': '085803000',
            'type': 'product',
            'updated_at': '2016-09-15T06:17:45.377000',
            'description': 'Cadeira para auto para crianças do grupo',
            'review_count': 0,
            'sells_to_company': False
        }

    @classmethod
    def matching_seller_variation_a(cls):
        return {
            'parent_sku': '8729',
            'updated_at': '2016-09-16T18:35:03.142595+00:00',
            'sku': '8732',
            'navigation_id': '8732',
            'disable_on_matching': False,
            'ean': '7892949094942',
            'categories': [
                {
                    'description': 'Cama, Mesa e Banho',
                    'id': 'CM',
                    'subcategories': [
                        {'id': 'CTAB', 'description': 'Toalha de Banho'}
                    ]
                }
            ],
            'sold_count': 0,
            'seller_description': 'Casa América',
            'description': 'Total conforto e maciez na sua saída de banho',
            'release_date': '2016-09-16T18:35:06.083793+00:00',
            'reference': 'Santista',
            'review_score': 5,
            'title': 'Toalha de Banho Platinum Caroline 510g/m² - Santista',
            'type': 'product',
            'main_variation': False,
            'brand': 'Santista',
            'dimensions': {
                'depth': 5,
                'weight': 573,
                'width': 27,
                'height': 37
            },
            'created_at': '2016-07-21T22:51:41.728549+00:00',
            'seller_id': 'casaamerica',
            'attributes': [
                {'value': 'Azul 4 060', 'type': 'color'}
            ],
            'review_count': 0,
            'grade': 10,
            'sells_to_company': False
        }

    @classmethod
    def matching_seller_variation_b(cls):
        return {
            'dimensions': {
                'height': 37,
                'weight': 573,
                'width': 27,
                'depth': 5
            },
            'description': 'Total conforto e maciez na sua saída de banho',
            'review_count': 0,
            'sold_count': 0,
            'attributes': [{'value': 'Lilás 3 050', 'type': 'color'}],
            'review_score': 5,
            'seller_id': 'casaamerica',
            'main_variation': False,
            'sku': '8731',
            'navigation_id': '8731',
            'created_at': '2016-07-21T22:51:41.728549+00:00',
            'categories': [
                {
                    'description': 'Cama, Mesa e Banho',
                    'subcategories': [
                        {'description': 'Toalha de Banho', 'id': 'CTAB'}
                    ],
                    'id': 'CM'
                }
            ],
            'reference': 'Santista',
            'type': 'product',
            'release_date': '2016-09-16T18:35:33.369766+00:00',
            'brand': 'Santista',
            'updated_at': '2016-09-16T18:35:29.690351+00:00',
            'ean': '7892949094911',
            'disable_on_matching': False,
            'seller_description': 'Casa América',
            'parent_sku': '8729',
            'grade': 10,
            'title': 'Toalha de Banho Platinum Caroline 510g/m² - Santista',
            'sells_to_company': False
        }

    @classmethod
    def matching_seller_different_product_parent_skus_matching_a(cls):
        return {
            'created_at': '2016-08-26T17:08:30.623865+00:00',
            'sku': '1773',
            'navigation_id': '1773',
            'title': 'Suporte de Smartphone para Guidão 5\' Multilaser - AC254',  # noqa
            'ean': '7898506470051',
            'attributes': [
                {'value': 'Neutro', 'type': 'color'}
            ],
            'description': '- Suporte para bicicleta ou moto Multilaser AC254, compatível com smartphones com tela de até 5 polegadas.\r\n- Possui película especial que permite a utilização do touch screen.\r\n- Oferece proteção semi permeável e anti-riscos.\r\n- Dispõe de trava giratória em 360º permitindo ajustar a posição do smartphone.\r\n- Plástico transparente permite a visualização.\r\n- Fechamento através de 2 zíperes.',  # noqa
            'dimensions': {
                'depth': 20,
                'weight': 500,
                'width': 20,
                'height': 20
            },
            'type': 'product',
            'updated_at': '2016-09-16T15:28:13.335240+00:00',
            'disable_on_matching': False,
            'categories': [
                {
                    'subcategories': [
                        {
                            'description': 'Celulares',
                            'id': 'TECE'
                        }
                    ],
                    'id': 'TE',
                    'description': 'Celulares e Telefones'
                }
            ],
            'reference': 'Multilaser',
            'release_date': '2016-09-16T15:28:15.122597+00:00',
            'grade': 10,
            'main_variation': True,
            'seller_id': 'lojamultilaser',
            'seller_description': 'Multilaser',
            'review_score': 5,
            'brand': 'Multilaser',
            'review_count': 0,
            'sold_count': 0,
            'parent_sku': '1787',
            'sells_to_company': False
        }

    @classmethod
    def matching_seller_different_product_parent_skus_matching_b(cls):
        return {
            'sku': '1787',
            'navigation_id': '1787',
            'title': 'Almofada Massageadora MY PILLOW Serene - HC013',
            'reference': 'Serene',
            'review_score': 5,
            'type': 'product',
            'categories': [
                {
                    'subcategories': [
                        {'id': 'MASA', 'description': 'Massageadores'}
                    ],
                    'id': 'CP',
                    'description': 'Beleza e Saúde'
                }
            ],
            'ean': '7898506477173',
            'parent_sku': '1800',
            'created_at': '2016-08-26T17:07:56.393729+00:00',
            'sold_count': 0,
            'release_date': '2016-09-16T18:08:42.561853+00:00',
            'attributes': [],
            'dimensions': {
                'depth': 30,
                'weight': 500,
                'height': 30,
                'width': 35
            },
            'seller_id': 'lojamultilaser',
            'description': 'A Almofada massageadora My Pillow da Serene é sua companheira para os momentos de descanso no sofá, na cama ou em uma cadeira. As massagens vibratórias provocam sensações de relaxamento e bem estar além de ser fabricada em tecido supor suave e confortável.',  # noqa
            'main_variation': True,
            'grade': 10,
            'seller_description': 'Multilaser',
            'review_count': 0,
            'updated_at': '2016-09-16T18:08:40.748677+00:00',
            'brand': 'Serene',
            'disable_on_matching': False,
            'sells_to_company': False
        }

    @classmethod
    def matching_seller_different_product_parent_skus_matching_c(cls):
        return {
            'created_at': '2016-08-26T17:10:36.680238+00:00',
            'sku': '1800',
            'navigation_id': '1800',
            'title': 'Spray de envelopamento liquido Preto Fosco 400ML Multilaser - AU420',  # noqa
            'ean': '7899838802725',
            'attributes': [
                {'value': 'Neutro', 'type': 'color'}
            ],
            'dimensions': {
                'weight': 500,
                'height': 15,
                'width': 15,
                'depth': 15
            },
            'type': 'product',
            'updated_at': '2016-09-16T18:08:28.046294+00:00',
            'description': 'O Spray de envelopamento líquido Multilaser é um tipo de cobertura emborrachada de secagem rápida, que pode ser aplicado em diversos tipos de superfícies, tanto plásticas quanto metálicas, sendo próprio para customização de seu automóvel. Possui tecnologia avançada, que reduz a aderência de sujeiras, sendo resistente à água e a corrosão. Além do mais, o produto ainda protege a pintura do seu carro. - A sua aplicação é bastante simples, permitindo que mesmo os não profissionais consigam atingir ótimos resultados na cobertura de superfícies diversas. A remoção da película é ainda mais fácil, não deixando resíduos que necessitem a utilização de químico, comprometendo a pintura original. Pode ser aplicado em: madeiras, vidros, plásticos, borrachas, paredes, metais entre outros. Características: - Fácil aplicação - Durável - Não danifica - Protege a pintura - Fácil remoção Conteúdo do spray: 400ml',  # noqa
            'release_date': '2016-09-16T18:08:29.795987+00:00',
            'reference': 'Multilaser',
            'categories': [
                {
                    'description': 'Automotivo',
                    'id': 'AU',
                    'subcategories': [
                        {
                            'description': 'Acessórios para carro',
                            'id': 'AEPC'
                        }
                    ]
                }
            ],
            'grade': 10,
            'disable_on_matching': False,
            'main_variation': True,
            'seller_id': 'lojamultilaser',
            'seller_description': 'Multilaser',
            'review_score': 5,
            'brand': 'Multilaser',
            'parent_sku': '1811',
            'sold_count': 0,
            'review_count': 0,
            'sells_to_company': False
        }

    @classmethod
    def matching_same_seller_without_attributes_a(cls):
        return {
            'title': 'Diorskin Airflash Dior - Base Facial',
            'grade': 10,
            'brand': 'Dior',
            'description': 'Diorskin Airflash é uma revolução na forma de se maquiar! \r\n\r\nÉ a primeira base aerada da Dior e promete dar luminosidade e leveza para à pele. Por ser em spray, o acabamento é fino e a tecnologia de microdifusão deixa a cobertura homogênea. \r\n\r\nAgite antes de usar! Mantendo uma distância de 30cm da face, aplique sobre o rosto e espalhe com os dedos ou com a ajuda de um pincel.',  # noqa
            'type': 'product',
            'dimensions': {
                'depth': 10,
                'height': 10,
                'width': 10,
                'weight': 100
            },
            'categories': [{
                'description': 'Perfumaria',
                'id': 'PF',
                'subcategories': [{
                    'description': 'Base',
                    'id': 'PFBQ'
                }]
            }],
            'disable_on_matching': False,
            'parent_sku': '310116653',
            'sku': '310117788',
            'navigation_id': '310117788',
            'seller_id': 'sandboxintegracao',
            'release_date': '2016-09-22T14:35:14.170649+00:00',
            'seller_description': 'VTex (Sandbox Integração)',
            'review_count': 0,
            'attributes': [],
            'updated_at': '2016-09-22T14:35:13+00:00',
            'reference': 'Dior',
            'ean': '3348900782532',
            'created_at': '2016-09-03T07:08:39+00:00',
            'review_score': 5,
            'main_variation': True,
            'sold_count': 0,
            'sells_to_company': False
        }

    @classmethod
    def variation_a_match_main(cls):
        return {
            'type': 'product',
            'sku': 'AmatchMAIN',
            'navigation_id': '111111112',
            'parent_sku': '112358',
            'seller_id': 'seller_a',
            'seller_description': 'Seller A',
            'brand': '+canecas xablau',
            'title': 'caneca 200ml',
            'ean': '111111112',
            'disable_on_matching': False,
            'grade': 10,
            'categories': [
                {
                    'id': 'UD',
                    'subcategories': [
                        {'id': 'UDCA'}
                    ]
                },
                {
                    'id': 'PR',
                    'subcategories': [
                        {'id': 'PRCA'}
                    ]
                }
            ],
            'attributes': [
                {
                    'type': 'color',
                    'value': 'Branca'
                }
            ],
            'sells_to_company': False
        }

    @classmethod
    def variation_b_match_a(cls):
        return {
            'type': 'product',
            'sku': 'BmatchA',
            'navigation_id': '111111112',
            'parent_sku': '112358',
            'seller_id': 'seller_b',
            'seller_description': 'Seller B',
            'brand': '+canecas xablau',
            'title': 'caneca branca 200ml xablalesca',
            'ean': '111111112',
            'disable_on_matching': False,
            'grade': 10,
            'categories': [
                {
                    'id': 'UD',
                    'subcategories': [
                        {'id': 'UDCA'}
                    ]
                },
                {
                    'id': 'PR',
                    'subcategories': [
                        {'id': 'PRCA'}
                    ]
                }
            ],
            'attributes': [
                {
                    'type': 'color',
                    'value': 'Branca'
                }
            ],
            'sells_to_company': False
        }

    @classmethod
    def variation_c_match_d(cls):
        return {
            'type': 'product',
            'sku': 'CmatchD',
            'navigation_id': '111111112',
            'parent_sku': '112358',
            'seller_id': 'seller_c',
            'seller_description': 'Seller C',
            'brand': '+canecas xablau',
            'title': 'caneca 200ml ',
            'ean': '111111113',
            'disable_on_matching': False,
            'grade': 10,
            'categories': [
                {
                    'id': 'UD',
                    'subcategories': [
                        {'id': 'UDCA'}
                    ]
                },
                {
                    'id': 'PR',
                    'subcategories': [
                        {'id': 'PRCA'}
                    ]
                }
            ],
            'attributes': [
                {
                    'type': 'color',
                    'value': 'Verde'
                }
            ],
            'sells_to_company': False
        }

    @classmethod
    def variation_d_match_b(cls):
        return {
            'type': 'product',
            'sku': 'DmatchB',
            'navigation_id': '111111112',
            'parent_sku': '',
            'seller_id': 'seller_d',
            'seller_description': 'Seller D',
            'brand': '+canecas xablau',
            'title': 'caneca branca 200ml xablalesca',
            'ean': '111111113',
            'disable_on_matching': False,
            'grade': 10,
            'categories': [
                {
                    'id': 'UD',
                    'subcategories': [
                        {'id': 'UDCA'}
                    ]
                },
                {
                    'id': 'PR',
                    'subcategories': [
                        {'id': 'PRCA'}
                    ]
                }
            ],
            'attributes': [
                {
                    'type': 'color',
                    'value': 'Verde'
                }
            ],
            'sells_to_company': False
        }

    @classmethod
    def matching_same_seller_without_attributes_b(cls):
        return {
            'title': 'Diorskin Airflash Dior - Base Facial',
            'grade': 10,
            'brand': 'Dior',
            'description': 'Diorskin Airflash é uma revolução na forma de se maquiar! \r\n\r\nÉ a primeira base aerada da Dior e promete dar luminosidade e leveza para à pele. Por ser em spray, o acabamento é fino e a tecnologia de microdifusão deixa a cobertura homogênea. \r\n\r\nAgite antes de usar! Mantendo uma distância de 30cm da face, aplique sobre o rosto e espalhe com os dedos ou com a ajuda de um pincel.',  # noqa
            'type': 'product',
            'dimensions': {
                'depth': 10,
                'height': 10,
                'width': 10,
                'weight': 100
            },
            'categories': [{
                'description': 'Perfumaria',
                'id': 'PF',
                'subcategories': [{
                    'description': 'Base',
                    'id': 'PFBQ'
                }]
            }],
            'disable_on_matching': False,
            'parent_sku': '310116653',
            'sku': '310117796',
            'navigation_id': '310117796',
            'seller_id': 'sandboxintegracao',
            'release_date': '2016-09-22T14:35:21.144523+00:00',
            'seller_description': 'VTex (Sandbox Integração)',
            'review_count': 0,
            'attributes': [],
            'updated_at': '2016-09-22T14:35:20+00:00',
            'reference': 'Dior',
            'ean': '3348900782556',
            'created_at': '2016-09-03T07:08:39+00:00',
            'review_score': 5,
            'main_variation': False,
            'sold_count': 0,
            'sells_to_company': False
        }

    @classmethod
    def matching_same_seller_without_attributes_c(cls):
        return {
            'title': 'Diorskin Airflash Dior - Base Facial',
            'grade': 10,
            'brand': 'Dior',
            'description': 'Diorskin Airflash é uma revolução na forma de se maquiar! \r\n\r\nÉ a primeira base aerada da Dior e promete dar luminosidade e leveza para à pele. Por ser em spray, o acabamento é fino e a tecnologia de microdifusão deixa a cobertura homogênea. \r\n\r\nAgite antes de usar! Mantendo uma distância de 30cm da face, aplique sobre o rosto e espalhe com os dedos ou com a ajuda de um pincel.',  # noqa
            'type': 'product',
            'dimensions': {
                'depth': 10,
                'height': 10,
                'width': 10,
                'weight': 100
            },
            'categories': [{
                'description': 'Perfumaria',
                'id': 'PF',
                'subcategories': [{
                    'description': 'Base',
                    'id': 'PFBQ'
                }]
            }],
            'disable_on_matching': False,
            'parent_sku': '310116653',
            'sku': '310117829',
            'navigation_id': '310117829',
            'seller_id': 'sandboxintegracao',
            'release_date': '2016-09-22T14:35:14.187381+00:00',
            'seller_description': 'VTex (Sandbox Integração)',
            'review_count': 0,
            'attributes': [],
            'updated_at': '2016-09-22T14:35:13+00:00',
            'reference': 'Dior',
            'ean': '3348900782563',
            'created_at': '2016-09-03T07:08:39+00:00',
            'review_score': 5,
            'main_variation': False,
            'sold_count': 0,
            'sells_to_company': False
        }

    @classmethod
    def matching_product_with_attributes_a(cls):
        return {
            'ean': '3605532562551',
            'parent_sku': '310116649',
            'description': 'Teint Miracle Compact é a versão compacta da célebre base Teint Miracle. Pela primeira vez, os laboratórios de Lancôme conseguiram integrar a tecnologia Aura-InsideT em uma fórmula compacta. \r\n\r\nTeint Miracle Compact deixa a pele luminosa e com um efeito super natural. Sua composição garante 18 Horas de hidratação, cobertura e fotoproteção com FPS 15. \r\n\r\nEsta base compacta de Lancôme tem uma textura muito fácil de aplicar, que se funde imediatamente à pele.\r\n\r\nAplique diretamente no rosto com a esponja ou com a ajuda de um pincel. Pode ser utilizado sozinho ou após a base. Ao longo do dia, reaplique o produto para evitar que o rosto fique com aspecto oleoso.',  # noqa
            'type': 'product',
            'release_date': '2016-10-06T21:00:57.997480+00:00',
            'created_at': '2016-09-03T03:00:17+00:00',
            'seller_description': 'VTex (Sandbox Integração)',
            'dimensions': {
                'height': 10,
                'weight': 100,
                'width': 10,
                'depth': 10
            },
            'seller_id': 'sandboxintegracao',
            'attributes': [{
                'value': '045 - Sable Beige',
                'type': 'color'
            }],
            'review_score': 5,
            'main_variation': False,
            'sku': '310117814',
            'navigation_id': '310117814',
            'updated_at': '2016-10-06T21:00:57+00:00',
            'sold_count': 0,
            'categories': [{
                'description': 'Perfumaria',
                'id': 'PF',
                'subcategories': [{
                    'description': 'Base',
                    'id': 'PFBQ'
                }]
            }],
            'grade': 10,
            'brand': 'Lancôme',
            'review_count': 0,
            'title': 'Teint Miracle Compact Lancôme - Base Facial',
            'disable_on_matching': False,
            'reference': 'Lancôme',
            'sells_to_company': False
        }

    @classmethod
    def matching_product_with_attributes_b(cls):
        return {
            'attributes': [{
                'type': 'color',
                'value': '03 - Beige Diaphane'
            }],
            'parent_sku': '310116649',
            'grade': 10,
            'sold_count': 0,
            'brand': 'Lancôme',
            'ean': '3605532562414',
            'review_count': 0,
            'reference': 'Lancôme',
            'title': 'Teint Miracle Compact Lancôme - Base Facial',
            'review_score': 5,
            'sku': '310117817',
            'navigation_id': '310117817',
            'created_at': '2016-09-03T03:00:17+00:00',
            'release_date': '2016-10-06T21:03:28.710113+00:00',
            'type': 'product',
            'disable_on_matching': False,
            'categories': [{
                'subcategories': [{
                    'description': 'Base',
                    'id': 'PFBQ'
                }],
                'description': 'Perfumaria',
                'id': 'PF'
            }],
            'description': 'Teint Miracle Compact é a versão compacta da célebre base Teint Miracle. Pela primeira vez, os laboratórios de Lancôme conseguiram integrar a tecnologia Aura-InsideT em uma fórmula compacta. \r\n\r\nTeint Miracle Compact deixa a pele luminosa e com um efeito super natural. Sua composição garante 18 Horas de hidratação, cobertura e fotoproteção com FPS 15. \r\n\r\nEsta base compacta de Lancôme tem uma textura muito fácil de aplicar, que se funde imediatamente à pele.\r\n\r\nAplique diretamente no rosto com a esponja ou com a ajuda de um pincel. Pode ser utilizado sozinho ou após a base. Ao longo do dia, reaplique o produto para evitar que o rosto fique com aspecto oleoso.',  # noqa
            'seller_id': 'sandboxintegracao',
            'dimensions': {
                'depth': 10,
                'weight': 100,
                'width': 10,
                'height': 10
            },
            'seller_description': 'VTex (Sandbox Integração)',
            'main_variation': False,
            'updated_at': '2016-10-06T21:03:27+00:00',
            'sells_to_company': False
        }

    @classmethod
    def matching_product_without_attributes_a(cls):
        return {
            'ean': '3605532562346',
            'parent_sku': '310116649',
            'description': 'Teint Miracle Compact é a versão compacta da célebre base Teint Miracle. Pela primeira vez, os laboratórios de Lancôme conseguiram integrar a tecnologia Aura-InsideT em uma fórmula compacta. \r\n\r\nTeint Miracle Compact deixa a pele luminosa e com um efeito super natural. Sua composição garante 18 Horas de hidratação, cobertura e fotoproteção com FPS 15. \r\n\r\nEsta base compacta de Lancôme tem uma textura muito fácil de aplicar, que se funde imediatamente à pele.\r\n\r\nAplique diretamente no rosto com a esponja ou com a ajuda de um pincel. Pode ser utilizado sozinho ou após a base. Ao longo do dia, reaplique o produto para evitar que o rosto fique com aspecto oleoso.',  # noqa
            'type': 'product',
            'release_date': '2016-10-06T21:03:31.124728+00:00',
            'created_at': '2016-09-03T03:00:17+00:00',
            'seller_description': 'VTex (Sandbox Integração)',
            'dimensions': {
                'height': 10,
                'weight': 100,
                'width': 10,
                'depth': 10
            },
            'seller_id': 'sandboxintegracao',
            'attributes': [],
            'review_score': 5,
            'main_variation': True,
            'sku': '310117816',
            'navigation_id': '310117816',
            'updated_at': '2016-10-06T21:03:30+00:00',
            'sold_count': 0,
            'categories': [{
                'description': 'Perfumaria',
                'id': 'PF',
                'subcategories': [{
                    'description': 'Base',
                    'id': 'PFBQ'
                }]
            }],
            'grade': 10,
            'brand': 'Lancôme',
            'review_count': 0,
            'title': 'Teint Miracle Compact Lancôme - Base Facial',
            'disable_on_matching': False,
            'reference': 'Lancôme',
            'sells_to_company': False
        }

    @classmethod
    def ml_similar_product_a(cls):
        return {
            'seller_description': 'Magazine Luiza',
            'selections': {
                '0': [
                    '18011',
                    '18691',
                    '18693',
                    '19107',
                    '19657',
                    '7039',
                    '7041',
                    '7291',
                    '8079',
                    '8215',
                    '8218'
                ],
                '12966': [
                    '16734',
                    '16737'
                ]
            },
            'seller_id': 'magazineluiza',
            'sku': '212415700',
            'navigation_id': '212415700',
            'review_count': 0,
            'review_score': 0,
            'updated_at': '2016-12-01T12:46:55.773000',
            'main_variation': True,
            'categories': [
                {
                    'subcategories': [
                        {
                            'id': 'ELCO'
                        },
                        {
                            'id': 'LIQU'
                        }
                    ],
                    'id': 'EP'
                }
            ],
            'grade': 10,
            'disable_on_matching': False,
            'parent_sku': '2124157',
            'type': 'product',
            'created_at': '2014-12-23T07:42:49.660000',
            'ean': '0040094922475',
            'sold_count': 0,
            'description': 'Liquidificador Multifuncional Plus da Hamilton Beach. Possui jarra feita com Tritan, o melhor do vidro e do pl\u00e1stico em um s\u00f3 produto, a base \u00e9 em a\u00e7o inoxid\u00e1vel e tem ainda filtro, jarra de 1,4 litro, 5 velocidades e \u00e9 muito f\u00e1cil de usar. Leve e resistente a estilha\u00e7os e manchas, tem bico na tampa que evita sujeira ao servir, 500W de pot\u00eancia, porta-fio na base e design super moderno que vai combinar com a sua cozinha.',  # noqa
            'dimensions': {
                'depth': 0.2,
                'height': 0.21,
                'width': 0.32,
                'weight': 3.79
            },
            'brand': 'hamilton beach',
            'attributes': [
                {
                    'value': '110 Volts',
                    'type': 'voltage'
                }
            ],
            'reference': '5 Velocidades com Filtro Inox 500W',
            'title': 'Liquidificador Hamilton Beach Multifuncional Plus',
            'matching_strategy': 'AUTO_BUYBOX',
            'sells_to_company': False
        }

    @classmethod
    def ml_similar_product_b(cls):
        return {
            'seller_description': 'Magazine Luiza',
            'selections': {
                '0': [
                    '19107',
                    '7039',
                    '7041',
                    '7291',
                    '8079',
                    '8215',
                    '8218'
                ],
                '12966': [
                    '16734',
                    '16737'
                ]
            },
            'seller_id': 'magazineluiza',
            'sku': '212415800',
            'navigation_id': '212415800',
            'review_count': 0,
            'review_score': 0,
            'updated_at': '2016-12-01T06:09:31.320000',
            'main_variation': False,
            'categories': [
                {
                    'subcategories': [
                        {
                            'id': 'ELCO'
                        },
                        {
                            'id': 'LIQU'
                        }
                    ],
                    'id': 'EP'
                }
            ],
            'grade': 10,
            'disable_on_matching': False,
            'parent_sku': '2124157',
            'type': 'product',
            'created_at': '2014-12-23T07:42:49.660000',
            'ean': '0040094922482',
            'sold_count': 0,
            'description': 'Liquidificador Multifuncional Plus da Hamilton Beach. Possui jarra feita com Tritan, o melhor do vidro e do pl\u00e1stico em um s\u00f3 produto, a base \u00e9 em a\u00e7o inoxid\u00e1vel e tem ainda filtro, jarra de 1,4 litro, 5 velocidades e \u00e9 muito f\u00e1cil de usar. Leve e resistente a estilha\u00e7os e manchas, tem bico na tampa que evita sujeira ao servir, 500W de pot\u00eancia, porta-fio na base e design super moderno que vai combinar com a sua cozinha.',  # noqa
            'dimensions': {
                'depth': 0.2,
                'height': 0.21,
                'width': 0.32,
                'weight': 3.79
            },
            'brand': 'hamilton beach',
            'attributes': [
                {
                    'value': '220 Volts',
                    'type': 'voltage'
                }
            ],
            'reference': '5 Velocidades com Filtro Inox 500W',
            'title': 'Liquidificador Hamilton Beach Multifuncional Plus',
            'matching_strategy': 'AUTO_BUYBOX',
            'sells_to_company': False
        }

    @classmethod
    def seller_similar_product_a(cls):
        return {
            'review_count': 0,
            'sold_count': 0,
            'disable_on_matching': False,
            'created_at': '2016-11-11T13:29:33.111623+00:00',
            'ean': '0040094922475',
            'reference': 'Hamilton Beach',
            'description': 'Prepare diversas bebidas e receitas utilizando o Liquidificador Multifuncional Plus 54229 da Hamilton Beach. Produzido com materiais de alta resist\u00eancia que garantem praticidade e rapidez na hora do uso. Al\u00e9m disso, o produto impede vazamentos ao servir, evitando sujeiras e mantendo sua cozinha organizada e com um toque especial e moderno na decora\u00e7\u00e3o.',  # noqa
            'grade': 10,
            'dimensions': {
                'height': 21,
                'weight': 3790,
                'depth': 20,
                'width': 32
            },
            'sku': '2022250',
            'navigation_id': '2022250',
            'type': 'product',
            'seller_description': 'DBestShop',
            'parent_sku': '2020383',
            'release_date': '2016-12-01T10:42:25.953986+00:00',
            'main_variation': True,
            'updated_at': '2016-12-01T10:42:25.659719+00:00',
            'title': 'Liquidificador Multifuncional Plus 54229 - Hamilton Beach',  # noqa
            'seller_id': 'dbestshop',
            'categories': [
                {
                    'description': 'Eletroport\u00e1teis',
                    'id': 'EP',
                    'subcategories': [
                        {
                            'description': 'Liquidificadores',
                            'id': 'LIQU'
                        },
                        {
                            'description': 'Cozinha',
                            'id': 'ELCO'
                        }
                    ]
                }
            ],
            'attributes': [
                {
                    'value': '110 Volts',
                    'type': 'voltage'
                }
            ],
            'review_score': 5,
            'brand': 'Hamilton Beach',
            'matching_strategy': 'AUTO_BUYBOX',
            'sells_to_company': False
        }

    @classmethod
    def ml_product_without_attributes(cls):
        return {
            'ean': '7898506466009',
            'disable_on_matching': False,
            'release_date': '2016-10-04T15:17:24.656241+00:00',
            'review_count': 0,
            'reference': 'Multilaser',
            'type': 'product',
            'brand': 'Multilaser',
            'dimensions': {
                'width': 20,
                'depth': 20,
                'height': 20,
                'weight': 500
            },
            'main_variation': True,
            'description': 'Caracter\u00edsticas \r\n. Bluetooth \r\n. Entrada para micro SD ( At\u00e9 32 GB) \r\n. MP3 \r\n. Microfone Hands Free ( Atende e encerra chamadas ) \r\n. R\u00e1dio FM com auto busca \r\n. Entrada P2 3.5 mm ( Pode se conectar a celulares, tablets,\r\nnotebooks e qualquer dispositivo com entrada auxiliar ) \r\n. Bateria de l\u00edtio recarreg\u00e1vel \r\n. Display para mostrar frequ\u00eancia de r\u00e1dio e nome da\r\nm\u00fasica MP3 \r\n. Alta qualidade de som \r\n. Haste ajust\u00e1vel \r\n. Controle de volume  \r\nInforma\u00e7\u00f5es T\u00e9cnicas \r\n. Bluetooth: CSR 2.1 \r\n. Frequ\u00eancia de resposta:\r\n20 Hz-20 KHz \r\n ',  # noqa
            'parent_sku': '918',
            'title': 'Fone de Ouvido Multilaser Headphone Bluetooth Micro SD Radio com Microfone Hands - PH095',  # noqa
            'seller_description': 'Multilaser',
            'categories': [
                {
                    'subcategories': [
                        {
                            'id': 'EAFN',
                            'description': 'Fone de Ouvido'
                        }
                    ],
                    'id': 'EA',
                    'description': '\u00c1udio'
                }
            ],
            'updated_at': '2016-10-04T15:17:23.935654+00:00',
            'sold_count': 0,
            'created_at': '2016-08-26T17:03:34.355466+00:00',
            'attributes': [
                {
                    'type': 'color',
                    'value': 'Neutro'
                }
            ],
            'grade': 20,
            'sku': '898',
            'navigation_id': '898',
            'seller_id': 'lojamultilaser',
            'review_score': 5,
            'sells_to_company': False
        }

    @classmethod
    def seller_product_with_attributes(cls):
        return {
            'review_score': 0,
            'reference': 'com Conex\u00e3o USB/Micro SD/P2 - Multilaser PH095',
            'sku': '208073000',
            'navigation_id': '208073000',
            'updated_at': '2016-12-08T06:27:25.697000',
            'review_count': 0,
            'ean': '7898506466009',
            'categories': [
                {
                    'id': 'EA',
                    'subcategories': [
                        {
                            'id': 'EAFN'
                        },
                        {
                            'id': 'FRDF'
                        }
                    ]
                }
            ],
            'type': 'product',
            'dimensions': {
                'depth': 0.05,
                'height': 0.17,
                'weight': 0.27,
                'width': 0.22
            },
            'parent_sku': '2080730',
            'main_variation': True,
            'seller_id': 'magazineluiza',
            'description': 'Fone headphone bluetooth Multilaser, designer super moderno e confort\u00e1vel, com um alcance de funcionamento de at\u00e9 10 metros, possui regulagem de altura, apoio de cabe\u00e7a, redutor de ru\u00eddos e controle de volume.',  # noqa
            'selections': {
                '0': [
                    '10811',
                    '6973',
                    '9303',
                    '9310',
                    '9356'
                ]
            },
            'seller_description': 'Magazine Luiza',
            'md5': 'a1dbf1e4a1ffc1663d1d7e2067b492c7',
            'sold_count': 0,
            'title': 'Fone de Ouvido Headphone Dobr\u00e1vel Bluetooth ',
            'disable_on_matching': False,
            'created_at': '2013-10-02T06:30:57.113000',
            'brand': 'multilaser',
            'grade': 10,
            'sells_to_company': False
        }

    @classmethod
    def matching_product_a(cls):
        return {
            'disable_on_matching': False,
            'categories': [
                {
                    'description': 'Eletroportateis',
                    'id': 'EP',
                    'subcategories': [
                        {
                            'description': 'Cozinha',
                            'id': 'ELCO'
                        },
                        {
                            'description': 'Panelas Eletricas',
                            'id': 'PAEL'
                        }
                    ]
                }
            ],
            'grade': 10,
            'parent_sku': '2002849',
            'ean': '0034264428874',
            'reference': 'Oster',
            'seller_id': 'dbestshop',
            'review_score': 5,
            'main_variation': True,
            'attributes': [
                {
                    'type': 'voltage',
                    'value': '110V'
                }
            ],
            'created_at': '2016-11-11T13:42:23.550858+00:00',
            'seller_description': 'DBestShop',
            'release_date': '2016-12-21T22:23:02.744044+00:00',
            'review_count': 0,
            'updated_at': '2016-12-21T22:23:01.322778+00:00',
            'sku': '2003971',
            'navigation_id': '2003971',
            'dimensions': {
                'width': 38,
                'weight': 6400,
                'depth': 37,
                'height': 35
            },
            'type': 'product',
            'brand': 'Oster',
            'title': 'Panela de Pressao Eletrica Oster com Timer 5 Litros Inox 4801',  # noqa
            'description': 'A Panela de Pressao',
            'sold_count': 0,
            'sells_to_company': False
        }

    @classmethod
    def matching_product_b(cls):
        return {
            'description': 'Panela de Pressao',
            'parent_sku': '2002287',
            'updated_at': '2016-12-26T16:41:07.503000',
            'selections': {
                '0': [
                    '17977',
                    '17980',
                    '18424',
                    '18691',
                    '18695',
                    '19107',
                    '19575',
                    '7039',
                    '7041',
                    '7291',
                    '8079',
                    '8218'
                ],
                '12966': [
                    '16734',
                    '16737'
                ]
            },
            'created_at': '2009-05-09T07:15:39.530000',
            'review_count': 4,
            'dimensions': {
                'depth': 0.35,
                'weight': 6.5,
                'width': 0.36,
                'height': 0.36
            },
            'attributes': [
                {
                    'value': '110 Volts',
                    'type': 'voltage'
                }
            ],
            'review_score': 5,
            'sold_count': 1,
            'sku': '200228700',
            'navigation_id': '200228700',
            'categories': [
                {
                    'subcategories': [
                        {
                            'id': 'ELCO'
                        },
                        {
                            'id': 'EPPE'
                        },
                        {
                            'id': 'PAEL'
                        }
                    ],
                    'id': 'EP'
                }
            ],
            'seller_id': 'magazineluiza',
            'title': 'Panela de Pressao Eletrica Oster Multicooker 4801',
            'brand': 'oster',
            'type': 'product',
            'reference': 'Inox 900W 5L Timer',
            'grade': 10,
            'seller_description': 'Magazine Luiza',
            'ean': '0034264428874',
            'main_variation': True,
            'disable_on_matching': False,
            'sells_to_company': False
        }

    @classmethod
    def matching_product_c(cls):
        return {
            'seller_description': 'Presentes Rodriguez',
            'seller_id': 'presentesrodriguez',
            'created_at': '2016-11-21T22:16:06.353344+00:00',
            'updated_at': '2016-12-11T18:46:43.888381+00:00',
            'disable_on_matching': False,
            'parent_sku': '1000002022',
            'review_score': 5,
            'reference': 'Oster',
            'release_date': '2016-12-11T18:46:45.155065+00:00',
            'ean': '0034264428874',
            'title': 'Panela Eletrica Multiuso 127V Oster',
            'brand': 'Oster',
            'main_variation': True,
            'grade': 10,
            'dimensions': {
                'depth': 53,
                'height': 25,
                'width': 50,
                'weight': 3600
            },
            'sold_count': 0,
            'attributes': [],
            'sku': '1000002022',
            'navigation_id': '1000002022',
            'categories': [
                {
                    'id': 'EP',
                    'subcategories': [
                        {
                            'id': 'ELCO',
                            'description': 'Cozinha'
                        },
                        {
                            'id': 'PAEL',
                            'description': 'Panelas Eletricas'
                        }
                    ],
                    'description': 'Eletroportateis'
                }
            ],
            'type': 'product',
            'description': 'Oster',
            'review_count': 0,
            'sells_to_company': False
        }

    @classmethod
    def stamaco_sku_86(cls):
        return {
            'disable_on_matching': False,
            'review_score': 5,
            'updated_at': '2016-12-20T14:30:10.708794+00:00',
            'ean': '7897371602130',
            'reference': 'STAMACO',
            'categories': [
                {
                    'description': 'Ferramentas e Seguran\u00e7a',
                    'id': 'FS',
                    'subcategories': [
                        {
                            'description': 'Ferramentas',
                            'id': 'FEMT'
                        },
                        {
                            'description': 'Disco de corte',
                            'id': 'DICC'
                        }
                    ]
                }
            ],
            'sold_count': 0,
            'brand': 'STAMACO',
            'review_count': 0,
            'main_variation': False,
            'description': 'As serras circulares da linha Serramax',
            'parent_sku': '32',
            'dimensions': {
                'width': 29,
                'height': 0.5,
                'weight': 620,
                'depth': 33.5
            },
            'release_date': '2016-12-20T14:30:12.017393+00:00',
            'seller_description': 'Stamaco',
            'sku': '86',
            'navigation_id': '86',
            'seller_id': 'stamaco',
            'title': 'Disco de Serra Vdea Serramax',
            'type': 'product',
            'created_at': '2016-12-12T17:56:02.551714+00:00',
            'attributes': [
                {
                    'value': '(10\')250x30mm',
                    'type': 'size'
                }
            ],
            'md5': '05ddfcc6d7cbb662a40f3176a8058bed',
            'grade': 10,
            'sells_to_company': False
        }

    @classmethod
    def stamaco_sku_87(cls):
        return {
            'sku': '87',
            'navigation_id': '87',
            'brand': 'STAMACO',
            'created_at': '2016-12-12T17:56:02.551714+00:00',
            'reference': 'STAMACO',
            'seller_id': 'stamaco',
            'type': 'product',
            'description': 'As serras circulares da linha Serramax',
            'md5': '1a5b5dd4cd8b88c15485b087dbf5fd8a',
            'categories': [
                {
                    'id': 'FS',
                    'description': 'Ferramentas e Segurança',
                    'subcategories': [
                        {
                            'id': 'FEMT',
                            'description': 'Ferramentas'
                        },
                        {
                            'id': 'DICC',
                            'description': 'Disco de corte'
                        }
                    ]
                }
            ],
            'title': 'Disco de Serra Vídea Serramax',
            'attributes': [
                {
                    'type': 'size',
                    'value': '(10\')250x30mm'
                }
            ],
            'disable_on_matching': False,
            'parent_sku': '32',
            'seller_description': 'Stamaco',
            'release_date': '2017-01-05T14:23:40.272493+00:00',
            'main_variation': False,
            'grade': 10,
            'review_score': 5,
            'ean': '7897371602147',
            'sold_count': 0,
            'review_count': 0,
            'dimensions': {
                'weight': 627,
                'depth': 33.5,
                'width': 29,
                'height': 0.5
            },
            'updated_at': '2017-01-05T14:23:38.822125+00:00',
            'sells_to_company': False
        }

    @classmethod
    def stamaco_sku_88(cls):
        return {
            'ean': '7897371602154',
            'attributes': [
                {
                    'value': '(10\')250x30mm',
                    'type': 'size'
                }
            ],
            'seller_description': 'Stamaco',
            'grade': 10,
            'disable_on_matching': False,
            'sku': '88',
            'navigation_id': '88',
            'main_variation': False,
            'seller_id': 'stamaco',
            'parent_sku': '32',
            'reference': 'STAMACO',
            'sold_count': 0,
            'type': 'product',
            'title': 'Disco de Serra Vdea Serramax',
            'created_at': '2016-12-12T17:56:02.551714+00:00',
            'brand': 'STAMACO',
            'md5': 'c286d3df258b9ec2e35a290d6315e164',
            'review_count': 0,
            'dimensions': {
                'width': 29,
                'weight': 648,
                'depth': 33.5,
                'height': 0.5
            },
            'categories': [
                {
                    'description': 'Ferramentas e Seguran\u00e7a',
                    'subcategories': [
                        {
                            'description': 'Ferramentas',
                            'id': 'FEMT'
                        },
                        {
                            'description': 'Disco de corte',
                            'id': 'DICC'
                        }
                    ],
                    'id': 'FS'
                }
            ],
            'review_score': 5,
            'description': 'As serras circulares da linha Serramax',
            'updated_at': '2017-01-12T11:09:53.632891+00:00',
            'release_date': '2017-01-12T11:09:54.234045+00:00',
            'sells_to_company': False
        }

    @classmethod
    def stamaco_sku_85(cls):
        return {
            'main_variation': False,
            'attributes': [
                {
                    'type': 'size',
                    'value': '(10\')250x30mm'
                }
            ],
            'title': 'Disco de Serra Vdea Serramax',
            'categories': [
                {
                    'description': 'Ferramentas e Seguran\u00e7a',
                    'subcategories': [
                        {
                            'description': 'Ferramentas',
                            'id': 'FEMT'
                        },
                        {
                            'description': 'Disco de corte',
                            'id': 'DICC'
                        }
                    ],
                    'id': 'FS'
                }
            ],
            'created_at': '2016-12-12T17:56:02.551714+00:00',
            'brand': 'STAMACO',
            'sold_count': 0,
            'md5': '940789b8e0d23c0b99373724d94c06af',
            'review_count': 0,
            'sku': '85',
            'navigation_id': '85',
            'type': 'product',
            'reference': 'STAMACO',
            'disable_on_matching': False,
            'description': 'As serras circulares da linha Serramax',
            'ean': '7897371602123',
            'dimensions': {
                'depth': 33.5,
                'height': 0.5,
                'weight': 631,
                'width': 29
            },
            'review_score': 5,
            'release_date': '2017-01-12T11:09:55.072530+00:00',
            'updated_at': '2017-01-12T11:09:54.852536+00:00',
            'parent_sku': '32',
            'seller_description': 'Stamaco',
            'grade': 10,
            'seller_id': 'stamaco',
            'sells_to_company': False
        }

    @classmethod
    def magazineluiza_sku_2090111_bundle(cls):
        return {
            'created_at': '2008-10-06T09:21:49.243000',
            'navigation_id': '209011100',
            'sold_count': 0,
            'seller_id': 'magazineluiza',
            'seller_description': 'Magazine Luiza',
            'parent_sku': '2090111',
            'brand': 'burigotto',
            'reference': 'para Crianças até 13Kg + Base de Cadeira para Auto',
            'categories': [
                {
                    'id': 'BB',
                    'subcategories': [
                        {'id': 'BBBU'},
                        {'id': 'BECO'},
                        {'id': 'CADA'},
                        {'id': 'CARR'}
                    ]
                }
            ],
            'title': 'Bebê Conforto Burigotto Touring SE Cinza',
            'sku': '209011100',
            'description': '',
            'dimensions': {
                'depth': 0.46, 'height': 0.39, 'weight': 0, 'width': 0.44
            },
            'grade': 0,
            'ean': '000000000None',
            'main_variation': True,
            'type': 'bundle',
            'review_count': 0,
            'origin': 'taz.consumers.rebuild.consumer',
            'sells_to_company': True,
            'selections': {'0': ['10811', '8162', '9303', '9356', '9972']},
            'matching_strategy': 'SINGLE_SELLER',
            'disable_on_matching': False,
            'review_score': 0,
            'bundles': {
                '176608400': {'price': '179.00', 'quantity': '1'},
                '201746100': {'price': '95.00', 'quantity': '1'}
            }
        }

    @classmethod
    def magazineluiza_sku_155108800_gift_product(cls):
        return {
            'sells_to_company': True,
            'created_at': '2014-07-23T07:16:16.793000',
            'review_count': 0,
            'reference': 'Android 4.2 Câm. 5MP Tela 4.5” Wi-Fi Desbl. TIM',
            'review_score': 0,
            'disable_on_matching': False,
            'origin': 'taz.consumers.rebuild.consumer',
            'navigation_id': '155108800',
            'updated_at': '2015-10-11T00:34:26.753000',
            'sku': '155108800',
            'type': 'gift',
            'description': 'Smartphone Samsung Galaxy S3 Slim Dual Chip com Sistema Operacional Android 4.2.2, tecnologia 3G, câmera digital traseira de 5MP e frontal VGA, e processador Quad-Core 1.2 GHz. Quer estar por dentro de tudo o que acontece em suas redes sociais e sempre disponível para os seus contatos? Agora, você pode! Com este excelente aparelho, você poderá ficar disponível para duas operadoras de sua preferência, ter a velocidade e a memória necessárias para realizar downloads, jogar os jogos mais baixados, ouvir e arquivar músicas e fotos. Além é claro, de ter acesso a todas as suas redes sociais, compartilhar tudo o que quiser e participar de chats, bate papos, Whats App e muito mais.  Não perca mais tempo e adquira já o seu!',  # noqa
            'brand': 'samsung',
            'main_variation': True,
            'parent_sku': '1551088',
            'seller_description': 'Magazine Luiza',
            'dimensions': {
                'weight': 0.45, 'depth': 0.14, 'width': 0.12, 'height': 0.06
            },
            'matching_strategy': 'SINGLE_SELLER',
            'categories': [
                {
                    'id': 'TE',
                    'subcategories': [
                        {'id': 'CT45'},
                        {'id': 'GALX'},
                        {'id': 'TCSP'},
                        {'id': 'TEAN'},
                        {'id': 'TECA'},
                        {'id': 'TECE'},
                        {'id': 'TEDH'},
                        {'id': 'TEQC'}
                    ]
                }
            ],
            'title': 'Smartphone Samsung Galaxy S3 Slim Dual Chip 3G',
            'ean': '2005317397674',
            'grade': 10,
            'selections': {
                '0': ['10811', '18423', '6973', '7040', '9303', '9310']
            },
            'sold_count': 0,
            'seller_id': 'magazineluiza',
            'gift_product': '150658700'
        }

    @classmethod
    def madeiramadeira_sku_173212(cls):
        return {
            'reference': 'Itatiaia',
            'updated_at': '2017-04-10T23:49:02.392764+00:00',
            'parent_sku': '173212',
            'seller_id': 'madeiramadeira-openapi',
            'sold_count': 0,
            'review_count': 0,
            'description': 'Cozinha Compacta Regina Itatiaia I3VG3-155 Branco/Verde Claro',  # noqa
            'categories': [{
                'subcategories': [{
                    'description': 'Móveis para Cozinha',
                    'id': 'MCOZ'
                }],
                'description': 'Móveis e Decoração',
                'id': 'MO'
            }],
            'seller_description': 'Madeira Madeira',
            'review_score': 5.0,
            'brand': 'Itatiaia',
            'attributes': [],
            'ean': '7892946325971',
            'sells_to_company': True,
            'type': 'product',
            'dimensions': {
                'weight': Decimal('73.120'),
                'width': Decimal('0.72'),
                'height': Decimal('0.18'),
                'depth': Decimal('1.61')
            },
            'created_at': '2017-04-05T13:08:37.447320+00:00',
            'sku': '173212',
            'release_date': '2017-04-11T12:02:12.142668+00:00',
            'title': 'Armário para Cozinha Regina Itatiaia I3VG3-155 Branco/Verde Claro',  # noqa
            'main_variation': True
        }

    @classmethod
    def casaamerica_sku_2019285(cls, disable_on_matching=True):
        return {
            'release_date': '2017-06-23T05:00:07.741447+00:00',
            'review_count': 0,
            'title': 'Forno a Gás de Embutir Brastemp',
            'categories': [{
                'id': 'ED',
                'subcategories': [{
                    'id': 'FORN',
                    'description': 'Forno'
                }],
                'description': 'Eletrodomésticos'
            }],
            'review_score': 5,
            'created_at': '2016-11-11T13:47:10.390370+00:00',
            'dimensions': {
                'height': 10,
                'weight': 0.04,
                'width': 10,
                'depth': 10
            },
            'parent_sku': '2018229',
            'attributes': [{
                'value': '220V',
                'type': 'voltage'
            }],
            'disable_on_matching': disable_on_matching,
            'sold_count': 0,
            'sku': '2019285',
            'ean': '7891129243828',
            'seller_id': 'casaamerica',
            'type': 'product',
            'main_variation': True,
            'matching_strategy': 'AUTO_BUYBOX',
            'navigation_id': '7918776',
            'seller_description': 'Casa América',
            'brand': 'Brastemp',
            'sells_to_company': True,
            'grade': 10,
            'reference': 'Brastemp',
            'description': 'Forno a Gás de Embutir Brastemp\r\nO Novo Forno a Gás de Embutir Brastemp possui Touch Timer, Grill, e duas prateleiras ajustáveis em 7 níveis para resultados mais precisos.\r\nO Touch Timer oferece maior precisão no tempo de preparo para garantir o ponto certo de cada receita.\r\nÉ ideal para assar dois pratos ao mesmo tempo sem perder o melhor de cada um. As duas prateleiras podem ser ajustadas aos 7 níveis de altura dentro do forno.\r\nO Grill é ideal para finalizar receitas crocantes de forma precisa.',  # noqa
            'updated_at': '2017-06-22T02:50:53.753537+00:00'
        }

    @classmethod
    def cookeletroraro_sku_2002109(cls, disable_on_matching=True):
        return {
            'ean': '7891129243828',
            'categories': [{
                'description': 'Eletrodomésticos',
                'subcategories': [{
                    'description': 'Forno e Fogão',
                    'id': 'FOFO'
                }],
                'id': 'ED'
            }],
            'title': 'Forno a Gás de Embutir 78 Litros Brastemp BOA84AERNA',
            'sku': '2002109',
            'disable_on_matching': disable_on_matching,
            'seller_description': 'Cook Eletroraro',
            'review_count': 0,
            'grade': 10,
            'seller_id': 'cookeletroraro',
            'dimensions': {
                'depth': 70,
                'width': 70,
                'weight': 30,
                'height': 70
            },
            'main_variation': True,
            'navigation_id': '8514563',
            'matching_strategy': 'AUTO_BUYBOX',
            'parent_sku': '2002096',
            'attributes': [{
                'value': '220V',
                'type': 'voltage'
            }],
            'created_at': '2017-01-19T17:37:06.618111+00:00',
            'sells_to_company': True,
            'description': 'O Forno a Gás de Embutir Brastemp tem alta capacidade de 78 litros e conta com 2 prateleiras que podem ser ajustadas em até 7 níveis, possibilitando assar 2 pratos diferentes ao mesmo tempo. O Touch Timer, além de moderno, avisa quando o assado está pronto, e, com o Grill, você finaliza os pratos com garantindo maior precisão às receitas.',  # noqa
            'reference': 'Brastemp',
            'type': 'product',
            'sold_count': 0,
            'review_score': 5,
            'brand': 'Brastemp',
            'updated_at': '2017-06-29T17:46:35.369750+00:00',
            'release_date': '2017-06-29T17:46:36.705645+00:00'
        }

    @classmethod
    def magazineluiza_sku_216534900(cls, disable_on_matching=False):
        return {
            'main_variation': True,
            'seller_id': 'magazineluiza',
            'reference': '84L Grill Touch Timer',
            'sku': '216534900',
            'categories': [{
                'id': 'ED',
                'subcategories': [{
                    'id': 'EFRE'
                }, {
                    'id': 'FEAG'
                }, {
                    'id': 'FORN'
                }]
            }],
            'brand': 'brastemp',
            'title': 'Forno à Gás de Embutir Brastemp BOA84AE',
            'attributes': [{
                'value': '220 Volts',
                'type': 'voltage'
            }],
            'type': 'product',
            'disable_on_matching': disable_on_matching,
            'created_at': '2016-07-28T07:54:45.320000',
            'ean': '7891129243828',
            'matching_strategy': 'AUTO_BUYBOX',
            'parent_sku': '2165349',
            'seller_description': 'Magazine Luiza',
            'dimensions': {
                'depth': 0.68,
                'weight': 30,
                'width': 0.67,
                'height': 0.7
            },
            'grade': 1010,
            'main_category': {
                'id': 'ED',
                'subcategory': {
                    'id': 'EFRE'
                }
            },
            'sold_count': 430,
            'selections': {
                '12966': ['16734', '16737'],
                '0': ['16879', '17976', '18036', '18789', '18934', '19212', '19512', '19597', '19818', '19969', '19994', '20272', '20334', '20336', '20338', '20342', '20344', '20355', '20362', '20363', '20370', '20448', '20486', '20589', '20592', '20601', '20613', '20616', '20639', '20679', '20704', '20761', '20770', '20795', '20833', '20998', '21017', '21027', '21036', '21039', '21056', '6874']  # noqa
            },
            'sells_to_company': True,
            'review_count': 0,
            'updated_at': '2017-07-05T06:06:22.607000',
            'navigation_id': '216534900',
            'description': 'O Forno à Gás de Embutir Brastemp tem alta capacidade de 84 litros e conta com 2 prateleiras que podem ser ajustadas em até 7 níveis, possibilitando assar dois pratos diferentes ao mesmo tempo, Possui Grill, que é ideal para finalizar receitas com crocância e de forma precisa. Além disso, o Touch Timer avisa quando o assado está pronto dando maior precisão ao tempo de preparo. ',  # noqa
            'review_score': 0
        }

    @classmethod
    def whirlpool_sku_2003610(
        cls, disable_on_matching=False, matching_strategy='SINGLE_SELLER'
    ):
        return {
            'seller_description': 'Brastemp',
            'dimensions': {
                'weight': 0.04,
                'width': 10,
                'height': 10,
                'depth': 10
            },
            'type': 'product',
            'review_score': 5,
            'parent_sku': '2002765',
            'sells_to_company': False,
            'title': 'Forno a Gás de Embutir Brastemp',
            'seller_id': 'whirlpool',
            'reference': 'Brastemp',
            'matching_strategy': matching_strategy,
            'main_variation': True,
            'ean': '7891129243828',
            'review_count': 0,
            'description': 'Dois Pratos no Ponto Certo ao mesmo TempoNovo Forno a Gás de Embutir Brastemp com Touch Timer, Grill, e duas prateleiras ajustáveis em 7 níveis para resultados mais precisos.Touch TimerMaior precisão no tempo de preparo para garantir o ponto certo de cada receita.2 Prateleiras E 7 NíveisIdeal para assar dois pratos ao mesmo tempo sem perder o melhor de cada um. As duas prateleiras podem ser ajustadas aos 7 níveis de altura dentro do forno.GrillIdeal para finalizar receitas com crocância e de forma precisa.',  # noqa
            'navigation_id': '9294879',
            'grade': 10,
            'release_date': '2017-07-06T02:55:36.846307+00:00',
            'sold_count': 0,
            'categories': [{
                'description': 'Eletrodomésticos',
                'id': 'ED',
                'subcategories': [{
                    'description': 'Forno',
                    'id': 'FORN'
                }, {
                    'description': 'Forno Embutir',
                    'id': 'EFRE'
                }]
            }],
            'created_at': '2016-12-05T16:37:37.762727+00:00',
            'updated_at': '2017-07-06T02:55:35.323957+00:00',
            'attributes': [{
                'type': 'voltage',
                'value': '220V'
            }],
            'disable_on_matching': disable_on_matching,
            'brand': 'Brastemp',
            'sku': '2003610'
        }

    @classmethod
    def magazineluiza_sku_193389100(cls):
        return {
            'description': 'Assim como os smartphones, as Smart TVs também chegaram para tornar a vida mais fácil, unindo os recursos de uma TV convencional à uma infinidade de recursos permitidos graças à conexão com a internet. Com design inovador que combina modernidade com funcionalidade. Com áudio frontal, você experimenta muito mais clareza no som para aproveitar muito mais seus programas favoritos. Navegue no novo menu e acesse seus aplicativos e canais favoritos com poucos cliques, inclusive os conteúdos do seu smartphone podem ser acessados na TV e sem a utilização de fios.\n\nCom acesso ao conteúdo smart você ganha muito mais opções na hora de escolher o que assistir e se divertir, são mais de 400 aplicativos disponíveis, de redes sociais, a cursos à distância. O processador QuadCore garante alto desempenho para sua TV. Acesse o menu de navegação Smart rapidamente e execute várias tarefas ao mesmo tempo, com precisão e sem perda de velocidade.\n\n',  # noqa
            'reference': 'Conversor Digital 2 HDMI 1 USB Wi-Fi',
            'grade': 10,
            'type': 'product',
            'title': 'Smart TV LED 40” Samsung Full HD 40K5300',
            'sells_to_company': True,
            'dimensions': {
                'height': 0.64,
                'depth': 1.32,
                'weight': 10,
                'width': 0.97
            },
            'ean': '7892509088077',
            'review_count': 0,
            'matching_strategy': 'SINGLE_SELLER',
            'seller_id': 'magazineluiza',
            'review_score': 0,
            'main_category': {
                'subcategory': {
                    'id': 'ELIT'
                },
                'id': 'ET'
            },
            'parent_sku': '1933891',
            'selections': {
                '0': ['18039', '18423', '19885', '20118', '20231', '20241', '20263', '20265', '20307', '20488', '20545', '20577', '20618', '20622', '20653', '20716', '20833', '20890', '20915', '20989', '6874', '8021', '9310'],  # noqa
                '12966': ['16734', '16737']
            },
            'sku': '193389100',
            'created_at': '2016-08-10T07:38:30.803000',
            'disable_on_matching': False,
            'brand': 'samsung',
            'navigation_id': '193389100',
            'sold_count': 7,
            'updated_at': '2017-07-10T16:35:24.437000',
            'seller_description': 'Magazine Luiza',
            'main_variation': False,
            'categories': [{
                'id': 'ET',
                'subcategories': [{
                    'id': 'ELIT'
                }, {
                    'id': 'LE40'
                }, {
                    'id': 'LE6Z'
                }, {
                    'id': 'LEAI'
                }, {
                    'id': 'LECI'
                }, {
                    'id': 'LEFH'
                }, {
                    'id': 'LESM'
                }, {
                    'id': 'PECO'
                }, {
                    'id': 'S60H'
                }, {
                    'id': 'SM40'
                }, {
                    'id': 'SMAI'
                }, {
                    'id': 'SMCD'
                }, {
                    'id': 'SMFH'
                }, {
                    'id': 'SMLD'
                }, {
                    'id': 'TLED'
                }]
            }]
        }

    @classmethod
    def magazineluiza_sku_193389600(cls):
        return {
            'title': 'Smart TV LED 55” Samsung 55K5300',
            'dimensions': {
                'height': 0.86,
                'weight': 21.2,
                'depth': 0.17,
                'width': 1.33
            },
            'navigation_id': '193389600',
            'parent_sku': '1933891',
            'selections': {
                '12966': ['16734', '16737'],
                '0': ['18039', '18423', '18428', '20231', '20263', '20265', '20273', '20307', '20488', '20545', '20577', '20653', '20716', '20830', '20915', '20989', '21036', '21037', '21070', '21073', '6874', '8021', '9310']  # noqa
            },
            'attributes': [{
                'value': '55\'',
                'type': 'inch'
            }],
            'review_score': 0,
            'type': 'product',
            'ean': '7892509088329',
            'sells_to_company': True,
            'matching_strategy': 'SINGLE_SELLER',
            'seller_id': 'magazineluiza',
            'main_category': {
                'subcategory': {
                    'id': 'ELIT'
                },
                'id': 'ET'
            },
            'review_count': 0,
            'brand': 'samsung',
            'main_variation': True,
            'sold_count': 85,
            'disable_on_matching': False,
            'seller_description': 'Magazine Luiza',
            'updated_at': '2017-07-10T10:55:35.170000',
            'created_at': '2016-08-10T07:38:30.803000',
            'categories': [{
                'subcategories': [{
                    'id': 'ELIT'
                }, {
                    'id': 'LE55'
                }, {
                    'id': 'LE6Z'
                }, {
                    'id': 'LEAI'
                }, {
                    'id': 'LECI'
                }, {
                    'id': 'LESM'
                }, {
                    'id': 'PECO'
                }, {
                    'id': 'S60H'
                }, {
                    'id': 'SM55'
                }, {
                    'id': 'SMAI'
                }, {
                    'id': 'SMCD'
                }, {
                    'id': 'SMLD'
                }, {
                    'id': 'TD55'
                }, {
                    'id': 'TLED'
                }],
                'id': 'ET'
            }],
            'sku': '193389600',
            'grade': 10,
            'description': 'Com a Tv Samsung 55K5300 você vai ter Design inovador que combina modernidade com funcionalidade. Com áudio frontal, você experimenta muito mais clareza no som para aproveitar muito mais seus programas favoritos. Navegue no novo menu e acesse seus aplicativos e canais favoritos com poucos cliques, inclusive os conteúdos do seu smartphone podem ser acessados na TV e sem a utilização de fios. Com acesso ao conteúdo smart você ganha muito mais opções na hora de escolher o que assistir e se divertir, são mais de 400 aplicativos disponíveis, de redes sociais, a cursos à distância.\n\nDesign Inovador: Auto Falantes frontais. Design inovador que combina modernidade com funcionalidade.\nCom áudio frontal, você experimenta muito mais clareza no som para aproveitar muito mais seus\nprogramas favoritos.\n\nConteúdo Smart: Centenas de aplicativos e serviços de entretenimento. Além disso, você encontra a mais completa oferta de serviços de vídeo on demand e Games, sem precisar de um videogame. \n\nPossui processador Quad Core. Sua Smart TV mais rápida e fácil de navegar. Melhor performance com aplicativos mais rápidos e controles mais precisos.\n',  # noqa
            'reference': 'Conversor Digital 2 HDMI 1 USB'
        }

    @classmethod
    def magazineluiza_sku_193389600_from_storage(cls):
        return {
            'active': True,
            'attributes': [
                {
                    'type': 'inch',
                    'value': '55\''
                }
            ],
            'brand': 'samsung',
            'categories': [
                {
                    'id': 'ET',
                    'subcategories': [
                        {
                            'id': 'ELIT'
                        }
                    ]
                }
            ],
            'created_at': '2016-08-10T07:38:30.803000',
            'description': 'Gente com a TV Smart LED Samsung Full HD 55K5300 você vai ter Design inovador que combina modernidade com funcionalidade. Com áudio frontal, você experimenta muito mais clareza no som para aproveitar muito mais seus programas favoritos. Navegue no novo menu e acesse seus aplicativos e canais favoritos com poucos cliques, inclusive os conteúdos do seu smartphone podem ser acessados na TV e sem a utilização de fios. Com acesso ao conteúdo smart você ganha muito mais opções na hora de escolher o que assistir e se divertir, são mais de 400 aplicativos disponíveis, de redes sociais, a cursos à distância. Design Inovador: Auto Falantes frontais. Design inovador que combina modernidade com funcionalidade. Com áudio frontal, você experimenta muito mais clareza no som para aproveitar muito mais seus programas favoritos. Possui processador Quad Core. Contém entradas em HDMI e USB. Sua Smart TV mais rápida e fácil de navegar. Melhor performance com aplicativos mais rápidos e controles mais precisos.',  # noqa
            'dimensions': {
                'depth': 0.17,
                'height': 0.86,
                'weight': 21.2,
                'width': 1.33
            },
            'ean': '7892509088329',
            'main_category': {
                'id': 'ET',
                'subcategory': {
                    'id': 'ELIT'
                }
            },
            'main_variation': True,
            'parent_sku': '1933896',
            'reference': 'Conversor Digital 2 HDMI 1 USB',
            'review_count': 0,
            'review_score': 0,
            'selections': {
                '0': [
                    '17637',
                    '18036'
                ]
            },
            'seller_description': 'Magalu',
            'seller_id': 'magazineluiza',
            'sku': '193389600',
            'sold_count': 0,
            'title': 'Smart TV LED 55” Samsung 55K5300',
            'type': 'product',
            'updated_at': '2018-01-22T06:09:46.340000',
            'disable_on_matching': False,
            'offer_title': 'Smart TV LED 55” Samsung 55K5300 - Conversor Digital 2 HDMI 1 USB',  # noqa
            'grade': 10,
            'navigation_id': '193389600',
            'matching_strategy': 'SINGLE_SELLER',
            'md5': '44dfaee33ce96c4c3fbd9ac517434d48',
            'last_updated_at': '2021-03-03T18:26:29.035995',
            'sells_to_company': True
        }

    @classmethod
    def magazineluiza_sku_193389300(cls):
        return {
            'description': 'Assim como os smartphones, as Smart TVs também chegaram para tornar a vida mais fácil, unindo os recursos de uma TV convencional à uma infinidade de recursos permitidos graças à conexão com a internet. Com design inovador que combina modernidade com funcionalidade. Com áudio frontal, você experimenta muito mais clareza no som para aproveitar muito mais seus programas favoritos. Navegue no novo menu e acesse seus aplicativos e canais favoritos com poucos cliques, inclusive os conteúdos do seu smartphone podem ser acessados na TV e sem a utilização de fios.\n\nCom acesso ao conteúdo smart você ganha muito mais opções na hora de escolher o que assistir e se divertir, são mais de 400 aplicativos disponíveis, de redes sociais, a cursos à distância. O processador QuadCore garante alto desempenho para sua TV. Acesse o menu de navegação Smart rapidamente e execute várias tarefas ao mesmo tempo, com precisão e sem perda de velocidade.\n\n',  # noqa
            'reference': 'Conversor Digital 2 HDMI 1 USB Wi-Fi',
            'grade': 10,
            'type': 'product',
            'title': 'Smart TV LED 49” Samsung Full HD 49K5300',
            'sells_to_company': True,
            'dimensions': {
                'height': 0.77,
                'depth': 0.16,
                'weight': 15.8,
                'width': 1.19
            },
            'ean': '7892509088312',
            'review_count': 0,
            'matching_strategy': 'SINGLE_SELLER',
            'seller_id': 'magazineluiza',
            'review_score': 0,
            'main_category': {
                'subcategory': {
                    'id': 'ELIT'
                },
                'id': 'ET'
            },
            'parent_sku': '1933891',
            'selections': {
                '0': ['18039', '18423', '19597', '19885', '19917', '20008', '20099', '20118', '20120', '20126', '20231', '20241', '20242', '20263', '20265', '20272', '20273', '20293', '20296', '20302', '20307', '20364', '20488', '20545', '20653', '20716', '20814', '20833', '20915', '20989', '21036', '21037', '21039', '21070', '21073', '6874', '8021', '9310'],  # noqa
                '12966': ['16734', '16737']
            },
            'sku': '193389300',
            'created_at': '2016-08-10T07:38:30.803000',
            'disable_on_matching': False,
            'brand': 'samsung',
            'navigation_id': '193389300',
            'sold_count': 300,
            'updated_at': '2017-07-10T06:06:30.377000',
            'seller_description': 'Magazine Luiza',
            'main_variation': True,
            'attributes': [{
                'value': '49\'',
                'type': 'inch'
            }],
            'categories': [{
                'id': 'ET',
                'subcategories': [{
                    'id': 'ELIT'
                }, {
                    'id': 'LE49'
                }, {
                    'id': 'LE6Z'
                }, {
                    'id': 'LEAI'
                }, {
                    'id': 'LECI'
                }, {
                    'id': 'LEFH'
                }, {
                    'id': 'LESM'
                }, {
                    'id': 'PECO'
                }, {
                    'id': 'S60H'
                }, {
                    'id': 'SM49'
                }, {
                    'id': 'SMAI'
                }, {
                    'id': 'SMCD'
                }, {
                    'id': 'SMFH'
                }, {
                    'id': 'SMLD'
                }, {
                    'id': 'TLED'
                }]
            }]
        }

    @classmethod
    def whirlpool_294(cls):
        return {
            'sku': '294',
            'brand': 'Brastemp',
            'seller_id': 'whirlpool',
            'grade': 10,
            'sold_count': 0,
            'created_at': '2016-12-05T16:36:03.122403+00:00',
            'type': 'product',
            'ean': '7891129186248',
            'attributes': [
                {
                    'value': '110V',
                    'type': 'voltage'
                }
            ],
            'description': 'Charme vintageO Frigobar Brastemp',
            'title': 'Frigobar Brastemp Retr\u00f4 76 L Preto',
            'matching_strategy': 'AUTO_BUYBOX',
            'review_score': 5,
            'navigation_id': '9130952',
            'reference': 'Brastemp',
            'disable_on_matching': False,
            'main_variation': True,
            'release_date': '2017-06-30T17:01:29.125334+00:00',
            'categories': [
                {
                    'subcategories': [
                        {
                            'description': 'Frigobar',
                            'id': 'RCOM'
                        },
                        {
                            'description': 'Geladeira/Refrigerador',
                            'id': 'REFR'
                        }
                    ],
                    'id': 'ED',
                    'description': 'Eletrodom\u00e9sticos'
                }
            ],
            'sells_to_company': False,
            'updated_at': '2017-06-30T17:01:27.818416+00:00',
            'parent_sku': '143',
            'seller_description': 'Brastemp',
            'dimensions': {
                'width': 10,
                'weight': 0.023,
                'height': 10,
                'depth': 10
            },
            'review_count': 0
        }

    @classmethod
    def whirlpool_879(cls):
        return {
            'created_at': '2016-12-05T16:36:44.861321+00:00',
            'dimensions': {
                'depth': 10,
                'height': 10,
                'width': 10,
                'weight': 0.014
            },
            'main_variation': False,
            'title': 'Micro-ondas Brastemp Ative! 38 Litros',
            'seller_id': 'whirlpool',
            'review_count': 0,
            'parent_sku': '660',
            'description': 'Micro-ondas Brastemp Ative! com',
            'seller_description': 'Brastemp',
            'type': 'product',
            'updated_at': '2017-06-30T17:01:20.483118+00:00',
            'matching_strategy': 'AUTO_BUYBOX',
            'review_score': 5,
            'release_date': '2017-06-30T17:01:21.820928+00:00',
            'brand': 'Brastemp',
            'sold_count': 0,
            'ean': '7891129220461',
            'reference': 'Brastemp',
            'sells_to_company': False,
            'grade': 10,
            'categories': [
                {
                    'subcategories': [
                        {
                            'id': 'MOND',
                            'description': 'Micro-ondas'
                        }
                    ],
                    'id': 'ED',
                    'description': 'Eletrodom\u00e9sticos'
                }
            ],
            'navigation_id': '9132215',
            'sku': '879',
            'attributes': [
                {
                    'value': '220V',
                    'type': 'voltage'
                }
            ],
            'disable_on_matching': False
        }

    @classmethod
    def whirlpool_125(cls):
        return {
            'sells_to_company': False,
            'matching_strategy': 'AUTO_BUYBOX',
            'seller_id': 'whirlpool',
            'sku': '125',
            'navigation_id': '9113908',
            'sold_count': 0,
            'grade': 10,
            'dimensions': {
                'height': 10,
                'width': 10,
                'depth': 10,
                'weight': 0.046
            },
            'review_score': 5,
            'main_variation': True,
            'seller_description': 'Brastemp',
            'type': 'product',
            'brand': 'Brastemp',
            'title': 'Forno El\u00e9trico de Embutir Brastemp Ative!',
            'ean': '7891129208285',
            'disable_on_matching': False,
            'parent_sku': '125',
            'reference': 'Brastemp',
            'attributes': [
                {
                    'value': '220V',
                    'type': 'voltage'
                }
            ],
            'release_date': '2017-06-30T17:27:20.913603+00:00',
            'updated_at': '2017-06-30T17:27:19.649848+00:00',
            'description': 'Um forno completoO Forno de Embutir',
            'review_count': 0,
            'categories': [
                {
                    'id': 'ED',
                    'subcategories': [
                        {
                            'id': 'FORN',
                            'description': 'Forno'
                        },
                        {
                            'id': 'EFRE',
                            'description': 'Forno Embutir'
                        }
                    ],
                    'description': 'Eletrodom\u00e9sticos'
                }
            ],
            'created_at': '2016-12-06T01:36:48.588169+00:00'
        }

    @classmethod
    def whirlpool_1339(cls):
        return {
            'review_score': 5,
            'release_date': '2017-06-30T17:02:05.707661+00:00',
            'categories': [
                {
                    'id': 'ED',
                    'subcategories': [
                        {
                            'id': 'FOGO',
                            'description': 'Fog\u00e3o'
                        },
                        {
                            'id': 'FOGA',
                            'description': 'Fog\u00e3o de Piso'
                        }
                    ],
                    'description': 'Eletrodom\u00e9sticos'
                }
            ],
            'reference': 'Brastemp',
            'sells_to_company': False,
            'dimensions': {
                'weight': 0.023,
                'width': 10,
                'height': 10,
                'depth': 10
            },
            'grade': 10,
            'ean': '7891129219212',
            'matching_strategy': 'AUTO_BUYBOX',
            'parent_sku': '1039',
            'created_at': '2016-12-05T16:36:55.270632+00:00',
            'sku': '1339',
            'navigation_id': '9190273',
            'seller_id': 'whirlpool',
            'type': 'product',
            'description': 'Descri\u00e7\u00e3o do produto',
            'updated_at': '2017-06-30T17:02:04.411954+00:00',
            'review_count': 0,
            'sold_count': 0,
            'attributes': [
                {
                    'value': '220V',
                    'type': 'voltage'
                }
            ],
            'main_variation': False,
            'disable_on_matching': False,
            'seller_description': 'Brastemp',
            'title': 'Fog\u00e3o 4 Bocas Brastemp Ative! Timer Grill',
            'brand': 'Brastemp'
        }

    @classmethod
    def whirlpool_129(cls):
        return {
            'review_score': 5,
            'release_date': '2017-06-30T17:04:27.980165+00:00',
            'categories': [
                {
                    'id': 'ED',
                    'subcategories': [
                        {
                            'id': 'FORN',
                            'description': 'Forno'
                        },
                        {
                            'id': 'EFRE',
                            'description': 'Forno Embutir'
                        }
                    ],
                    'description': 'Eletrodom\u00e9sticos'
                }
            ],
            'reference': 'Brastemp',
            'sells_to_company': False,
            'dimensions': {
                'weight': 0.046,
                'width': 10,
                'height': 10,
                'depth': 10
            },
            'grade': 10,
            'ean': '7891129204713',
            'matching_strategy': 'AUTO_BUYBOX',
            'parent_sku': '129',
            'created_at': '2016-12-05T16:36:07.457639+00:00',
            'sku': '129',
            'navigation_id': '9216980',
            'seller_id': 'whirlpool',
            'type': 'product',
            'description': 'Completo e exclusivoCom design italiano',
            'updated_at': '2017-06-30T17:04:26.508405+00:00',
            'review_count': 0,
            'sold_count': 0,
            'attributes': [
                {
                    'value': '220V',
                    'type': 'voltage'
                }
            ],
            'main_variation': True,
            'disable_on_matching': False,
            'seller_description': 'Brastemp',
            'title': 'Forno El\u00e9trico de Embutir Brastemp Gourmand',
            'brand': 'Brastemp'
        }

    @classmethod
    def whirlpool_1093(cls):
        return {
            'created_at': '2016-12-05T16:37:04.019287+00:00',
            'attributes': [
                {
                    'type': 'voltage',
                    'value': 'Bivolt'
                }
            ],
            'brand': 'Brastemp',
            'review_count': 0,
            'navigation_id': '9288125',
            'parent_sku': '849',
            'seller_description': 'Brastemp',
            'reference': 'Brastemp',
            'main_variation': True,
            'sold_count': 0,
            'sells_to_company': False,
            'title': 'Cooktop Brastemp Ative! Touch Timer Quadrichama 5 bocas',  # noqa
            'seller_id': 'whirlpool',
            'grade': 10,
            'type': 'product',
            'release_date': '2017-06-30T17:22:03.830558+00:00',
            'updated_at': '2017-06-30T17:22:02.564900+00:00',
            'matching_strategy': 'AUTO_BUYBOX',
            'sku': '1093',
            'review_score': 5,
            'categories': [
                {
                    'id': 'ED',
                    'description': 'Eletrodom\u00e9sticos',
                    'subcategories': [
                        {
                            'id': 'OUCO',
                            'description': 'Outras marcas de cooktop'
                        },
                        {
                            'id': 'COOK',
                            'description': 'Cooktops'
                        }
                    ]
                }
            ],
            'dimensions': {
                'height': 10,
                'width': 10,
                'depth': 10,
                'weight': 0.018
            },
            'ean': '7891129224704',
            'disable_on_matching': False,
            'description': 'Design moderno e funcionalO Cooktop'
        }

    @classmethod
    def whirlpool_2003610(cls):
        return {
            'seller_description': 'Brastemp',
            'main_variation': True,
            'title': 'Forno a G\u00e1s de Embutir Brastemp',
            'matching_strategy': 'AUTO_BUYBOX',
            'navigation_id': '9294879',
            'release_date': '2017-06-30T17:01:34.608643+00:00',
            'dimensions': {
                'weight': 0.04,
                'height': 10,
                'width': 10,
                'depth': 10
            },
            'categories': [
                {
                    'subcategories': [
                        {
                            'description': 'Forno',
                            'id': 'FORN'
                        },
                        {
                            'description': 'Forno Embutir',
                            'id': 'EFRE'
                        }
                    ],
                    'description': 'Eletrodom\u00e9sticos',
                    'id': 'ED'
                }
            ],
            'description': 'Dois Pratos no Ponto Certo ao mesmo',
            'sold_count': 0,
            'sells_to_company': False,
            'ean': '7891129243828',
            'parent_sku': '2002765',
            'sku': '2003610',
            'grade': 10,
            'created_at': '2016-12-05T16:37:37.762727+00:00',
            'updated_at': '2017-06-30T17:01:33.315451+00:00',
            'review_score': 5,
            'disable_on_matching': False,
            'attributes': [
                {
                    'value': '220V',
                    'type': 'voltage'
                }
            ],
            'seller_id': 'whirlpool',
            'review_count': 0,
            'brand': 'Brastemp',
            'type': 'product',
            'reference': 'Brastemp'
        }

    @classmethod
    def whirlpool_1091(cls):
        return {
            'created_at': '2016-12-05T16:37:29.320277+00:00',
            'dimensions': {
                'depth': 10,
                'height': 10,
                'width': 10,
                'weight': 0.018
            },
            'title': 'Cooktop Brastemp Ative! 4 bocas Touch Time',
            'seller_id': 'whirlpool',
            'review_count': 0,
            'parent_sku': '847',
            'description': 'Compacto e potenteO Cooktop',
            'seller_description': 'Brastemp',
            'reference': 'Brastemp',
            'updated_at': '2017-06-30T17:01:09.616839+00:00',
            'matching_strategy': 'AUTO_BUYBOX',
            'type': 'product',
            'brand': 'Brastemp',
            'sold_count': 0,
            'ean': '7891129224384',
            'release_date': '2017-06-30T17:01:10.875563+00:00',
            'sells_to_company': False,
            'grade': 10,
            'categories': [
                {
                    'subcategories': [
                        {
                            'id': 'OUCO',
                            'description': 'Outras marcas de cooktop'
                        },
                        {
                            'id': 'COOK',
                            'description': 'Cooktops'
                        }
                    ],
                    'id': 'ED',
                    'description': 'Eletrodom\u00e9sticos'
                }
            ],
            'review_score': 5,
            'navigation_id': '9296704',
            'attributes': [
                {
                    'value': 'Bivolt',
                    'type': 'voltage'
                }
            ],
            'disable_on_matching': False,
            'main_variation': True,
            'sku': '1091'
        }

    @classmethod
    def magazineluiza_088894700(cls):
        return {
            'ean': '7891129219212',
            'seller_description': 'Magazine Luiza',
            'disable_on_matching': False,
            'sold_count': 4,
            'navigation_id': '088894700',
            'seller_id': 'magazineluiza',
            'main_category': {
                'id': 'ED',
                'subcategory': {
                    'id': 'FOGO'
                }
            },
            'attributes': [
                {
                    'value': '220 Volts',
                    'type': 'voltage'
                }
            ],
            'updated_at': '2017-06-30T17:21:34.263000',
            'categories': [
                {
                    'id': 'ED',
                    'subcategories': [
                        {
                            'id': 'FOGO'
                        },
                        {
                            'id': 'EFP4'
                        },
                        {
                            'id': 'FOGA'
                        }
                    ]
                }
            ],
            'review_count': 0,
            'dimensions': {
                'height': 0.89,
                'depth': 0.67,
                'width': 0.52,
                'weight': 32
            },
            'created_at': '2013-11-02T06:21:26.393000',
            'selections': {
                '0': [
                    '18036',
                    '6874',
                    '7039',
                    '7041'
                ],
                '12966': [
                    '16734',
                    '16737'
                ]
            },
            'sells_to_company': True,
            'brand': 'brastemp',
            'main_variation': False,
            'reference': 'Timer Acendimento Autom\u00e1tico',
            'review_score': 0,
            'type': 'product',
            'sku': '088894700',
            'description': 'Fog\u00e3o Brastemp Ative! 4 bocas de piso.',
            'grade': 10,
            'parent_sku': '0888946',
            'title': 'Fog\u00e3o 4 Bocas Brastemp Ative! BF150AR Inox Grill',  # noqa
            'matching_strategy': 'AUTO_BUYBOX',
        }

    @classmethod
    def whirlpool_1338(cls):
        return {
            'sku': '1338',
            'brand': 'Brastemp',
            'reference': 'Brastemp',
            'review_count': 0,
            'seller_description': 'Brastemp',
            'sold_count': 0,
            'parent_sku': '1039',
            'updated_at': '2017-06-30T22:01:28.666086+00:00',
            'main_variation': True,
            'title': 'Fog\u00e3o 4 Bocas Brastemp Ative! Timer Grill',
            'matching_strategy': 'AUTO_BUYBOX',
            'type': 'product',
            'dimensions': {
                'depth': 10,
                'width': 10,
                'height': 10,
                'weight': 0.023
            },
            'attributes': [
                {
                    'value': '110V',
                    'type': 'voltage'
                }
            ],
            'ean': '7891129219229',
            'release_date': '2017-06-30T22:01:30.237087+00:00',
            'categories': [
                {
                    'description': 'Eletrodom\u00e9sticos',
                    'subcategories': [
                        {
                            'description': 'Fog\u00e3o',
                            'id': 'FOGO'
                        },
                        {
                            'description': 'Fog\u00e3o de Piso',
                            'id': 'FOGA'
                        }
                    ],
                    'id': 'ED'
                }
            ],
            'disable_on_matching': False,
            'review_score': 5,
            'sells_to_company': False,
            'seller_id': 'whirlpool',
            'description': 'Descri\u00e7\u00e3o do produto',
            'grade': 10,
            'created_at': '2016-12-05T16:36:55.270632+00:00',
            'navigation_id': '9275888'
        }

    @classmethod
    def casaamerica_2015463(cls):
        return {
            'ean': '7891129219229',
            'categories': [
                {
                    'id': 'ED',
                    'description': 'Eletrodom\u00e9sticos',
                    'subcategories': [
                        {
                            'id': 'FOGO',
                            'description': 'Fog\u00e3o'
                        }
                    ]
                }
            ],
            'sold_count': 0,
            'navigation_id': '7825475',
            'type': 'product',
            'disable_on_matching': False,
            'created_at': '2016-07-21T20:08:52.153806+00:00',
            'reference': 'Brastemp',
            'review_count': 0,
            'dimensions': {
                'width': 49.9,
                'depth': 65.4,
                'weight': 28.5,
                'height': 93
            },
            'review_score': 5,
            'main_variation': True,
            'release_date': '2017-06-23T04:54:45.554607+00:00',
            'seller_id': 'casaamerica',
            'attributes': [
                {
                    'value': '110V',
                    'type': 'voltage'
                }
            ],
            'sku': '2015463',
            'parent_sku': '2014651',
            'grade': 10,
            'updated_at': '2017-06-22T02:38:20.495196+00:00',
            'seller_description': 'Casa Am\u00e9rica',
            'description': '',
            'title': 'Fog\u00e3o 4 Bocas Brastemp Ative! Timer Grill',
            'sells_to_company': True,
            'brand': 'Brastemp',
            'matching_strategy': 'AUTO_BUYBOX'
        }

    @classmethod
    def casaamerica_2015515(cls):
        return {
            'ean': '',
            'categories': [
                {
                    'id': 'ED',
                    'description': 'Eletrodom\u00e9sticos',
                    'subcategories': [
                        {
                            'id': 'FOGO',
                            'description': 'Fog\u00e3o'
                        }
                    ]
                }
            ],
            'sold_count': 0,
            'navigation_id': '7893304',
            'type': 'product',
            'disable_on_matching': False,
            'created_at': '2016-07-21T20:08:52.153806+00:00',
            'reference': 'Brastemp',
            'review_count': 0,
            'dimensions': {
                'weight': 28.5,
                'width': 49.9,
                'depth': 65.4,
                'height': 93
            },
            'review_score': 5,
            'main_variation': False,
            'release_date': '2017-06-23T04:54:54.844061+00:00',
            'seller_id': 'casaamerica',
            'attributes': [
                {
                    'value': '220V',
                    'type': 'voltage'
                }
            ],
            'sku': '2015515',
            'parent_sku': '2014651',
            'grade': 0,
            'updated_at': '2017-06-22T02:38:20.495196+00:00',
            'seller_description': 'Casa Am\u00e9rica',
            'description': '',
            'title': 'Fog\u00e3o 4 Bocas Brastemp Ative! Timer Grill',
            'sells_to_company': True,
            'brand': 'Brastemp',
            'matching_strategy': 'AUTO_BUYBOX'
        }

    @classmethod
    def pequenostravessos_sku_571743566(cls):
        return {
            'review_count': 0,
            'created_at': '2017-01-19T17:23:15.501642+00:00',
            'main_variation': False,
            'review_score': 5,
            'updated_at': '2017-05-11T06:02:19.533797+00:00',
            'sku': '571743566',
            'release_date': '2017-05-11T06:02:20.851892+00:00',
            'brand': 'Diversão',
            'sells_to_company': True,
            'type': 'product',
            'reference': 'Diversão',
            'sold_count': 0,
            'categories': [{
                'description': 'Bebê',
                'id': 'BB',
                'subcategories': [{
                    'description': 'Calçados para bebê',
                    'id': 'CCPB'
                }]
            }],
            'dimensions': {
                'weight': 0.5,
                'height': 15,
                'depth': 12,
                'width': 30
            },
            'parent_sku': '1000643',
            'matching_strategy': 'SINGLE_SELLER',
            'description': 'Trazendo o universo de Frozen para o dia a dia das baixinhas, esta sapatilha da Disney finaliza os looks no maior charme. Macia e altamente confortável, promove uma pisada mais leve e cercada de conforto, como as princesinhas merecem. \r\r\nEstampado;\r\r\nCabedal em material sintético;\r\r\nForro têxtil;\r\r\nPalmilha estampada em EVA;\r\r\nSolado em borracha antiderrapante.',  # noqa
            'ean': '',
            'seller_description': 'Pequenos Travessos',
            'attributes': [{
                'type': 'size',
                'value': '27'
            }],
            'navigation_id': '8267834',
            'seller_id': 'pequenostravessos',
            'disable_on_matching': False,
            'grade': 0,
            'title': 'Sapatilha Charm Frozen - Diversão'
        }

    @classmethod
    def pequenostravessos_sku_571743563(cls):
        return {
            'review_count': 0,
            'dimensions': {
                'weight': 0.5,
                'height': 15,
                'width': 30,
                'depth': 12
            },
            'categories': [{
                'description': 'Bebê',
                'id': 'BB',
                'subcategories': [{
                    'description': 'Calçados para bebê',
                    'id': 'CCPB'
                }]
            }],
            'seller_description': 'Pequenos Travessos',
            'description': 'Trazendo o universo de Frozen para o dia a dia das baixinhas, esta sapatilha da Disney finaliza os looks no maior charme. Macia e altamente confortável, promove uma pisada mais leve e cercada de conforto, como as princesinhas merecem. \r\r\nEstampado;\r\r\nCabedal em material sintético;\r\r\nForro têxtil;\r\r\nPalmilha estampada em EVA;\r\r\nSolado em borracha antiderrapante.',  # noqa
            'reference': 'Diversão',
            'sku': '571743563',
            'release_date': '2017-05-11T06:02:24.314342+00:00',
            'title': 'Sapatilha Charm Frozen - Diversão',
            'brand': 'Diversão',
            'type': 'product',
            'navigation_id': '8274849',
            'grade': 0,
            'attributes': [{
                'value': '24',
                'type': 'color'
            }],
            'sells_to_company': True,
            'updated_at': '2017-05-11T06:02:23.042473+00:00',
            'ean': '',
            'main_variation': True,
            'review_score': 5,
            'parent_sku': '1000643',
            'sold_count': 0,
            'matching_strategy': 'SINGLE_SELLER',
            'seller_id': 'pequenostravessos',
            'disable_on_matching': False,
            'created_at': '2017-01-19T17:23:15.501642+00:00'
        }

    @classmethod
    def pequenostravessos_sku_571743567(cls):
        return {
            'seller_id': 'pequenostravessos',
            'created_at': '2017-01-19T17:23:15.501642+00:00',
            'release_date': '2017-05-11T06:02:30.011126+00:00',
            'updated_at': '2017-05-11T06:02:28.719675+00:00',
            'title': 'Sapatilha Charm Frozen - Diversão',
            'categories': [{
                'subcategories': [{
                    'description': 'Calçados para bebê',
                    'id': 'CCPB'
                }],
                'description': 'Bebê',
                'id': 'BB'
            }],
            'review_score': 5,
            'disable_on_matching': False,
            'description': 'Trazendo o universo de Frozen para o dia a dia das baixinhas, esta sapatilha da Disney finaliza os looks no maior charme. Macia e altamente confortável, promove uma pisada mais leve e cercada de conforto, como as princesinhas merecem. \r\r\nEstampado;\r\r\nCabedal em material sintético;\r\r\nForro têxtil;\r\r\nPalmilha estampada em EVA;\r\r\nSolado em borracha antiderrapante.',  # noqa
            'review_count': 0,
            'sells_to_company': True,
            'main_variation': False,
            'navigation_id': '8385310',
            'parent_sku': '1000643',
            'type': 'product',
            'matching_strategy': 'SINGLE_SELLER',
            'sku': '571743567',
            'attributes': [{
                'value': '28',
                'type': 'size'
            }],
            'seller_description': 'Pequenos Travessos',
            'sold_count': 0,
            'dimensions': {
                'width': 30,
                'height': 15,
                'depth': 12,
                'weight': 0.5
            },
            'reference': 'Diversão',
            'ean': '',
            'brand': 'Diversão',
            'grade': 0
        }

    @classmethod
    def magazineluiza_sku_088878800(cls):
        return {
            'title': 'Coifa de Parede Brastemp Inox 89,8cm 3 Velocidades',
            'type': 'product',
            'disable_on_matching': False,
            'categories': [{
                'id': 'ED',
                'subcategories': [{
                    'id': 'COFA'
                }, {
                    'id': 'COPA'
                }]
            }],
            'description': 'Coifa de parede 90 cm com vidro temperado plano. Pode ser instalada no modo depurador ou exaustor e tem capacidade de sucção ideal para uma cozinha de até 25m² (considerando um pé direito de 2,5 metros). Possui filtro de carvão ativado de longa duração (uso em modo depurador), que garante o ar da sua cozinha sempre limpo e sem cheiro. Design, praticidade e sofisticação para sua cozinha!',  # noqa
            'attributes': [{
                'type': 'voltage',
                'value': '110 Volts'
            }],
            'main_variation': True,
            'seller_id': 'magazineluiza',
            'sells_to_company': True,
            'created_at': '2013-09-26T06:11:50.630000',
            'matching_strategy': 'SINGLE_SELLER',
            'main_category': {
                'id': 'ED',
                'subcategory': {
                    'id': 'COFA'
                }
            },
            'parent_sku': '0888788',
            'updated_at': '2017-08-19T07:11:35.743000',
            'sold_count': 0,
            'grade': 10,
            'review_count': 0,
            'reference': 'BA190ARANA',
            'ean': '7891129217546',
            'navigation_id': '088878800',
            'brand': 'brastemp',
            'sku': '088878800',
            'seller_description': 'Magazine Luiza',
            'review_score': 0,
            'dimensions': {
                'depth': 0.44,
                'height': 0.58,
                'weight': 22.4,
                'width': 0.98
            }
        }

    @classmethod
    def whirlpool_sku_27(cls):
        return {
            'reference': 'Brastemp',
            'main_variation': True,
            'created_at': '2016-12-06T11:05:58.853967+00:00',
            'type': 'product',
            'updated_at': '2017-08-30T15:39:41.146963+00:00',
            'seller_description': 'Brastemp',
            'parent_sku': '27',
            'grade': 10,
            'attributes': [{
                'value': '110V',
                'type': 'voltage'
            }],
            'matching_strategy': 'SINGLE_SELLER',
            'brand': 'Brastemp',
            'navigation_id': '9260935',
            'review_score': 5,
            'review_count': 0,
            'seller_id': 'whirlpool',
            'ean': '7891129217546',
            'sold_count': 0,
            'categories': [{
                'description': 'Eletrodomésticos',
                'subcategories': [{
                    'description': 'Coifas',
                    'id': 'COFA'
                }],
                'id': 'ED'
            }],
            'dimensions': {
                'width': 10,
                'weight': 0.025,
                'depth': 10,
                'height': 10
            },
            'release_date': '2017-08-30T15:39:42.849691+00:00',
            'sells_to_company': False,
            'description': 'Design e potênciaA Coifa de Parede Brastemp com Vidro Temperado Plano é ideal para quem busca potência aliada a um design moderno. Versátil, pode ser instalada de dois modos, como depurador ou exaustor. Ela também conta com 3 níveis de sucção e filtro carbono longa vida, que dura até 3 anos.Depurador ou exaustorA Coifa Brastemp foi desenvolvida para ser usada de duas maneiras. No modo Exaustão, o ar sugado é direcionado para fora do ambiente sem ser filtrado. Já com o Depurador, o ar absorvido passa por um filtro de carbono ativo e é devolvido para o ambiente.Alta sucçãoCom 3 níveis de velocidade, a coifa garante alto nível de absorção e deixa a sua cozinha livre de gordura e vapores.Filtro longa vidaExclusivo para o uso no modo depurador, o filtro longa vida é lavável e pode ser usado tem vida útil de até 3 anos.',  # noqa
            'title': 'Coifa de Parede Brastemp com Vidro Temperado Plano 90 cm',  # noqa
            'sku': '27',
            'disable_on_matching': False
        }

    @classmethod
    def magazineluiza_sku_088878900(cls):
        return {
            'title': 'Coifa de Parede Brastemp Inox 89,8cm 3 Velocidades',
            'type': 'product',
            'disable_on_matching': False,
            'categories': [{
                'id': 'ED',
                'subcategories': [{
                    'id': 'COFA'
                }, {
                    'id': 'COPA'
                }]
            }],
            'description': 'Coifa de parede 90 cm com vidro temperado plano. Pode ser instalada no modo depurador ou exaustor (o kit de instalação do modo de Exaustão, bem como o tubo de ventilação, são vendidos separadamente) e tem capacidade de sucção ideal para uma cozinha de até 25m² (considerando um pé direito de 2,5 metros). Possui filtro de carvão ativado de longa duração (uso em modo depurador), que garante o ar da sua cozinha sempre limpo e sem cheiro. Design, praticidade e sofisticação para sua cozinha!',  # noqa
            'attributes': [{
                'type': 'voltage',
                'value': '220 Volts'
            }],
            'main_variation': False,
            'seller_id': 'magazineluiza',
            'sells_to_company': True,
            'created_at': '2013-09-26T06:11:50.630000',
            'matching_strategy': 'SINGLE_SELLER',
            'main_category': {
                'id': 'ED',
                'subcategory': {
                    'id': 'COFA'
                }
            },
            'parent_sku': '0888788',
            'updated_at': '2017-08-08T18:16:44.813000',
            'sold_count': 0,
            'grade': 10,
            'review_count': 0,
            'reference': 'BA190ARBNA',
            'ean': '7891129217553',
            'navigation_id': '088878900',
            'brand': 'brastemp',
            'sku': '088878900',
            'seller_description': 'Magazine Luiza',
            'review_score': 0,
            'dimensions': {
                'depth': 0.44,
                'height': 0.58,
                'weight': 22.4,
                'width': 0.98
            }
        }

    @classmethod
    def whirlpool_sku_257(cls):
        return {
            'seller_description': 'Brastemp',
            'seller_id': 'whirlpool',
            'review_count': 0,
            'grade': 10,
            'type': 'product',
            'disable_on_matching': False,
            'review_score': 5,
            'reference': 'Brastemp',
            'title': 'Coifa de Parede Brastemp com Vidro Temperado Plano 90 cm',  # noqa
            'dimensions': {
                'depth': 10,
                'height': 10,
                'width': 10,
                'weight': 0.025
            },
            'created_at': '2016-12-06T11:05:58.853967+00:00',
            'main_variation': False,
            'release_date': '2017-08-30T15:40:04.635340+00:00',
            'parent_sku': '27',
            'description': 'Design e potênciaA Coifa de Parede Brastemp com Vidro Temperado Plano é ideal para quem busca potência aliada a um design moderno. Versátil, pode ser instalada de dois modos, como depurador ou exaustor. Ela também conta com 3 níveis de sucção e filtro carbono longa vida, que dura até 3 anos.Depurador ou exaustorA Coifa Brastemp foi desenvolvida para ser usada de duas maneiras. No modo Exaustão, o ar sugado é direcionado para fora do ambiente sem ser filtrado. Já com o Depurador, o ar absorvido passa por um filtro de carbono ativo e é devolvido para o ambiente.Alta sucçãoCom 3 níveis de velocidade, a coifa garante alto nível de absorção e deixa a sua cozinha livre de gordura e vapores.Filtro longa vidaExclusivo para o uso no modo depurador, o filtro longa vida é lavável e pode ser usado tem vida útil de até 3 anos.',  # noqa
            'navigation_id': '9284379',
            'ean': '7891129217553',
            'matching_strategy': 'SINGLE_SELLER',
            'categories': [{
                'id': 'ED',
                'description': 'Eletrodomésticos',
                'subcategories': [{
                    'id': 'COFA',
                    'description': 'Coifas'
                }]
            }],
            'brand': 'Brastemp',
            'updated_at': '2017-08-30T15:40:02.813814+00:00',
            'sells_to_company': False,
            'attributes': [{
                'type': 'voltage',
                'value': '220V'
            }],
            'sold_count': 0,
            'sku': '257'
        }

    @classmethod
    def surikato_sku_4182(cls):
        return {
            'review_score': 5,
            'disable_on_matching': False,
            'matching_strategy': 'SINGLE_SELLER',
            'navigation_id': '7953986',
            'description': '',  # noqa
            'brand': 'Brastemp',
            'main_variation': True,
            'release_date': '2017-08-20T20:59:59.645160+00:00',
            'seller_id': 'surikato',
            'sku': '4182',
            'updated_at': '2017-08-20T20:59:51.616352+00:00',
            'dimensions': {
                'depth': 0.45,
                'height': 0.69,
                'width': 0.9,
                'weight': 90
            },
            'attributes': [],
            'seller_description': 'Surikato',
            'type': 'product',
            'sells_to_company': True,
            'created_at': '2017-04-11T22:27:00.247398+00:00',
            'review_count': 0,
            'parent_sku': '4182',
            'ean': '7891129417546',
            'reference': 'Brastemp',
            'title': 'Coifa de Parede Brastemp com Vidro Temperado Plano 90 cm 220V - BA190ARBNA',  # noqa
            'sold_count': 0,
            'grade': 10,
            'categories': [{
                'id': 'ED',
                'subcategories': [{
                    'id': 'OTED',
                    'description': 'Outros eletrodomésticos'
                }],
                'description': 'Eletrodomésticos'
            }]
        }

    @classmethod
    def magazineluiza_sku_200513500(cls):
        return {
            'main_category': {
                'subcategory': {
                    'id': 'FOGO'
                },
                'id': 'ED'
            },
            'review_score': 5,
            'ean': '7891129235113',
            'grade': 10,
            'seller_description': 'Magazine Luiza',
            'review_count': 1,
            'selections': {
                '12966': ['16734', '16737'],
                '0': ['17911', '18036', '6874', '7039', '7041']
            },
            'sells_to_company': True,
            'type': 'product',
            'attributes': [{
                'value': '110 Volts',
                'type': 'voltage'
            }],
            'main_variation': True,
            'dimensions': {
                'depth': 0.74,
                'weight': 33,
                'height': 0.98,
                'width': 0.63
            },
            'seller_id': 'magazineluiza',
            'sold_count': 0,
            'title': 'Fogão 4 Bocas Brastemp Ative! BFS4GABRNA Grill',
            'navigation_id': '200513500',
            'reference': 'Timer Acendimento Automático Branco',
            'created_at': '2014-09-03T07:50:17.727000',
            'description': 'Fogão 4 bocas Ative! da Brastemp. Este fogão tem um design moderno com porta de vidro panorâmico e grades individuais. Para facilitar a limpeza, ele possui vidro interno removível e novo revestimento do forno com a tecnologia Cleartec. O forno tem ainda capacidade de 65 litros, prateleira auto deslizante, luz, grill elétrico e timer para facilitar no preparo de suas receitas.',  # noqa
            'parent_sku': '2005135',
            'brand': 'brastemp',
            'updated_at': '2017-09-04T06:06:50.220000',
            'categories': [{
                'subcategories': [{
                    'id': 'FOGO'
                }, {
                    'id': 'EFP4'
                }, {
                    'id': 'FOGA'
                }],
                'id': 'ED'
            }],
            'sku': '200513500',
            'disable_on_matching': False
        }

    @classmethod
    def whirlpool_sku_1157(cls):
        return {
            'updated_at': '2017-09-04T18:22:50.140881+00:00',
            'categories': [{
                'subcategories': [{
                    'description': 'Fogão de Piso',
                    'id': 'FOGA'
                }, {
                    'description': 'Fogão',
                    'id': 'FOGO'
                }],
                'description': 'Eletrodomésticos',
                'id': 'ED'
            }],
            'attributes': [{
                'type': 'voltage',
                'value': '110V'
            }],
            'review_score': 5,
            'sells_to_company': False,
            'description': 'Compacto e potenteO Fogão de Piso Brastemp Ative 4 Bocas Maxi é ideal para quem não abre mão de potência e versatilidade na hora de cozinhar. Equipado com Duplachama, Grill Elétrico, forno com vidro interno removível e tecnologia de limpeza Cleartec, também conta com Timer e vidro panorâmico.DuplachamaPara mais agilidade no preparo das receitas, o fogão conta com um potente Duplachama que libera o calor de dois pontos diferentes do queimador.Doura e gratinaGratine e doure massas, carnes e o que mais desejar com o Grill Elétrico do Fogão Brastemp 4 bocas e deixe suas receitas ainda mais saborosas.Facilidade na limpezaO revestimento esmaltado com tecnologia Cleartec, evita o acúmulo de sujeira no interior do forno que conta, também, com vidro interno removível que facilita a limpeza.TimerO Timer proporciona mais precisão no preparo das receitas. Basta girar o botão, regular o tempo necessário e pronto! Um sinal sonoro é emitido quando o tempo acaba.',  # noqa
            'created_at': '2016-12-05T16:36:20.562220+00:00',
            'reference': 'Brastemp',
            'sold_count': 0,
            'main_variation': True,
            'disable_on_matching': False,
            'parent_sku': '887',
            'release_date': '2017-09-04T18:22:51.967071+00:00',
            'seller_description': 'Brastemp',
            'title': 'Fogão 4 Bocas Brastemp Ative! Grill',
            'grade': 10,
            'review_count': 0,
            'ean': '7891129235113',
            'brand': 'Brastemp',
            'type': 'product',
            'sku': '1157',
            'navigation_id': '9163725',
            'dimensions': {
                'width': 10,
                'weight': 0.028,
                'depth': 10,
                'height': 10
            },
            'seller_id': 'whirlpool'
        }

    @classmethod
    def cookeletroraro_sku_2001305(cls):
        return {
            'reference': 'Brastemp',
            'ean': '7891129235380',
            'dimensions': {
                'weight': 32,
                'height': 80,
                'depth': 70,
                'width': 65
            },
            'release_date': '2017-08-18T18:40:10.106758+00:00',
            'updated_at': '2017-08-18T18:40:08.748954+00:00',
            'description': 'Compacto e Potente\r\n&nbsp;\r\nO Fogão de Embutir Brastemp Ative 4 Bocas Maxi é ideal para quem não abre mão de potência e versatilidade na hora de cozinhar. Equipado com Duplachama, Grill Elétrico, forno com vidro interno removível e tecnologia de limpeza Cleartec, também conta com Timer e vidro panorâmico.\r\n&nbsp;\r\nDupla chama\r\n\r\nPara mais agilidade no preparo das receitas, o fogão inox conta com um potente Duplachama que libera o calor de dois pontos diferentes do queimador.\r\n\r\n\r\nO revestimento esmaltado com tecnologia Cleartec, evita o acúmulo de sujeira no interior do forno que conta, também, com vidro interno removível que facilita a limpeza.\r\n\r\n Timer\r\n\r\nO Timer proporciona mais precisão no preparo das receitas. Basta girar o botão, regular o tempo necessário e pronto! Um sinal sonoro é emitido quando o tempo acaba.\r\n\r\n Doura e Gratina\r\n\r\nGratine e doure massas, carnes e o que mais desejar com o Grill Elétrico do Fogão Brastemp 4 bocas e deixe suas receitas ainda mais saborosas.\r\n\r\n',  # noqa
            'review_count': 0,
            'sku': '2001305',
            'review_score': 5,
            'sells_to_company': True,
            'type': 'product',
            'main_variation': True,
            'title': 'Fogão de Embutir Brastemp Ative Grill 4 Queimadores Inox 110V BYS4GARNNA',  # noqa
            'grade': 20,
            'disable_on_matching': False,
            'navigation_id': '8518314',
            'attributes': [{
                'value': '110V',
                'type': 'voltage'
            }],
            'parent_sku': '2001331',
            'created_at': '2017-01-19T17:36:34.447456+00:00',
            'brand': 'Brastemp',
            'categories': [{
                'description': 'Eletrodomésticos',
                'subcategories': [{
                    'description': 'Fogão',
                    'id': 'FOGO'
                }],
                'id': 'ED'
            }],
            'sold_count': 0,
            'seller_id': 'cookeletroraro',
            'seller_description': 'Cook Eletroraro'
        }

    @classmethod
    def magazineluiza_sku_200513600(cls):
        return {
            'created_at': '2014-09-03T07:50:17.727000',
            'seller_id': 'magazineluiza',
            'updated_at': '2017-09-04T09:24:16.790000',
            'sold_count': 2,
            'sku': '200513600',
            'title': 'Fogão 4 Bocas Brastemp Ative! BFS4GABRNA Grill',
            'review_score': 0,
            'attributes': [{
                'value': '220 Volts',
                'type': 'voltage'
            }],
            'type': 'product',
            'main_variation': False,
            'parent_sku': '2005135',
            'disable_on_matching': False,
            'grade': 10,
            'selections': {
                '12966': ['16734', '16737'],
                '0': ['17911', '18036', '6874', '7039', '7041']
            },
            'sells_to_company': True,
            'ean': '7891129235120',
            'reference': 'Timer Acendimento Automático Branco',
            'brand': 'brastemp',
            'review_count': 0,
            'main_category': {
                'subcategory': {
                    'id': 'FOGO'
                },
                'id': 'ED'
            },
            'navigation_id': '200513600',
            'dimensions': {
                'depth': 0.74,
                'weight': 33,
                'height': 0.98,
                'width': 0.63
            },
            'description': 'Fogão 4 bocas Ative! da Brastemp. Este fogão tem um design moderno com porta de vidro panorâmico e grades individuais. Para facilitar a limpeza, ele possui vidro interno removível e novo revestimento do forno com a tecnologia Cleartec. O forno tem ainda capacidade de 65 litros, prateleira auto deslizante, luz, grill elétrico e timer para facilitar no preparo de suas receitas.',  # noqa
            'categories': [{
                'subcategories': [{
                    'id': 'FOGO'
                }, {
                    'id': 'EFP4'
                }, {
                    'id': 'FOGA'
                }],
                'id': 'ED'
            }],
            'seller_description': 'Magazine Luiza'
        }

    @classmethod
    def whirlpool_sku_1048(cls):
        return {
            'type': 'product',
            'dimensions': {
                'width': 10,
                'height': 10,
                'depth': 10,
                'weight': 0.035
            },
            'attributes': [{
                'type': 'voltage',
                'value': '220V'
            }],
            'reference': 'Brastemp',
            'title': 'Fogão 4 Bocas de Embutir Brastemp Ative! Grill',
            'seller_description': 'Brastemp',
            'brand': 'Brastemp',
            'created_at': '2016-12-05T20:05:49.621431+00:00',
            'navigation_id': '9117182',
            'categories': [{
                'description': 'Eletrodomésticos',
                'subcategories': [{
                    'description': 'Fogão de Embutir',
                    'id': 'FOEM'
                }, {
                    'description': 'Fogão',
                    'id': 'FOGO'
                }],
                'id': 'ED'
            }],
            'sold_count': 0,
            'main_variation': False,
            'sells_to_company': False,
            'review_count': 0,
            'grade': 10,
            'release_date': '2017-09-06T00:41:31.810397+00:00',
            'parent_sku': '809',
            'review_score': 5,
            'updated_at': '2017-09-06T00:41:29.899519+00:00',
            'sku': '1048',
            'description': 'Compacto e potenteO Fogão de Embutir Brastemp Ative 4 Bocas Maxi é ideal para quem não abre mão de potência e versatilidade na hora de cozinhar. Equipado com Duplachama, Grill Elétrico, forno com vidro interno removível e tecnologia de limpeza Cleartec, também conta com Timer e vidro panorâmico.DuplachamaPara mais agilidade no preparo das receitas, o fogão inox conta com um potente Duplachama que libera o calor de dois pontos diferentes do queimador.Doura e gratinaGratine e doure massas, carnes e o que mais desejar com o Grill Elétrico do Fogão Brastemp 4 bocas e deixe suas receitas ainda mais saborosas.Facilidade na limpezaO revestimento esmaltado com tecnologia Cleartec, evita o acúmulo de sujeira no interior do forno que conta, também, com vidro interno removível que facilita a limpeza.TimerO Timer proporciona mais precisão no preparo das receitas. Basta girar o botão, regular o tempo necessário e pronto! Um sinal sonoro é emitido quando o tempo acaba.',  # noqa
            'disable_on_matching': False,
            'ean': '7891129235397',
            'seller_id': 'whirlpool'
        }

    @classmethod
    def whirlpool_sku_1183(cls):
        return {
            'seller_description': 'Brastemp',
            'matching_strategy': 'SINGLE_SELLER',
            'review_score': 5,
            'ean': '7891129217003',
            'review_count': 0,
            'release_date': '2017-09-03T16:44:02.031826+00:00',
            'type': 'product',
            'updated_at': '2017-09-03T16:44:00.328878+00:00',
            'sold_count': 0,
            'attributes': [{
                'value': '220V',
                'type': 'voltage'
            }],
            'sku': '1183',
            'description': 'Praticidade para o seu dia a diaO Fogão Brastemp Ative! com 4 Bocas é perfeito para você que busca praticidade e potência para o dia a dia. Com design moderno, é equipado com Grill, Timer Digital, Duplachama e forno com vidro panorâmico, que facilita a visualização durante o preparo das receitas.SuperpotênciaPara mais agilidade no preparo das receitas, o fogão conta com um potente Duplachama que libera o calor de dois pontos diferentes do queimador.Grill elétricoCom o Grill Elétrico do Fogão Brastemp 4 bocas, você pode dourar e gratinar massas, carnes e o que mais desejar, deixando suas receitas ainda mais saborosas.Timer digitalO Timer Digital proporciona mais precisão no preparo das receitas. Basta ajustar o tempo necessário por meio do painel eletrônico e pronto! Um sinal sonoro será emitido quando o tempo acabar.Vidro panorâmicoPara melhor visualização dos seus pratos durante o preparo, o fogão 4 bocas tem forno com vidro panorâmico.',  # noqa
            'disable_on_matching': False,
            'sells_to_company': False,
            'created_at': '2016-12-05T16:36:28.311966+00:00',
            'brand': 'Brastemp',
            'dimensions': {
                'weight': 0.023,
                'depth': 10,
                'height': 10,
                'width': 10
            },
            'reference': 'Brastemp',
            'title': 'Fogão 4 Bocas Brastemp Ative! Timer Grill',
            'main_variation': False,
            'categories': [{
                'description': 'Eletrodomésticos',
                'id': 'ED',
                'subcategories': [{
                    'description': 'Fogão de Piso',
                    'id': 'FOGA'
                }, {
                    'description': 'Fogão',
                    'id': 'FOGO'
                }]
            }],
            'parent_sku': '901',
            'navigation_id': '9162129',
            'grade': 10,
            'seller_id': 'whirlpool'
        }

    @classmethod
    def whirlpool_sku_1047(cls):
        return {
            'reference': 'Brastemp',
            'disable_on_matching': False,
            'type': 'product',
            'categories': [{
                'id': 'ED',
                'description': 'Eletrodomésticos',
                'subcategories': [{
                    'id': 'FOEM',
                    'description': 'Fogão de Embutir'
                }, {
                    'id': 'FOGO',
                    'description': 'Fogão'
                }]
            }],
            'sold_count': 0,
            'updated_at': '2017-09-03T16:42:47.635230+00:00',
            'main_variation': True,
            'grade': 10,
            'created_at': '2016-12-05T20:05:49.621431+00:00',
            'release_date': '2017-09-03T16:42:49.909725+00:00',
            'navigation_id': '9260005',
            'matching_strategy': 'SINGLE_SELLER',
            'dimensions': {
                'width': 10,
                'weight': 0.035,
                'depth': 10,
                'height': 10
            },
            'title': 'Fogão 4 Bocas de Embutir Brastemp Ative! Grill',
            'description': 'Compacto e potenteO Fogão de Embutir Brastemp Ative 4 Bocas Maxi é ideal para quem não abre mão de potência e versatilidade na hora de cozinhar. Equipado com Duplachama, Grill Elétrico, forno com vidro interno removível e tecnologia de limpeza Cleartec, também conta com Timer e vidro panorâmico.DuplachamaPara mais agilidade no preparo das receitas, o fogão inox conta com um potente Duplachama que libera o calor de dois pontos diferentes do queimador.Doura e gratinaGratine e doure massas, carnes e o que mais desejar com o Grill Elétrico do Fogão Brastemp 4 bocas e deixe suas receitas ainda mais saborosas.Facilidade na limpezaO revestimento esmaltado com tecnologia Cleartec, evita o acúmulo de sujeira no interior do forno que conta, também, com vidro interno removível que facilita a limpeza.TimerO Timer proporciona mais precisão no preparo das receitas. Basta girar o botão, regular o tempo necessário e pronto! Um sinal sonoro é emitido quando o tempo acaba.',  # noqa
            'seller_id': 'whirlpool',
            'ean': '7891129235380',
            'parent_sku': '809',
            'attributes': [{
                'value': '110V',
                'type': 'voltage'
            }],
            'seller_description': 'Brastemp',
            'sells_to_company': False,
            'sku': '1047',
            'brand': 'Brastemp',
            'review_score': 5,
            'review_count': 0
        }

    @classmethod
    def magazineluiza_sku_088894400(cls):
        return {
            'attributes': [{
                'value': '110 Volts',
                'type': 'voltage'
            }],
            'updated_at': '2017-09-02T23:32:45.250000',
            'main_variation': True,
            'sells_to_company': True,
            'brand': 'brastemp',
            'categories': [{
                'id': 'ED',
                'subcategories': [{
                    'id': 'FOGO'
                }, {
                    'id': 'EFP4'
                }, {
                    'id': 'FOGA'
                }]
            }],
            'ean': '7891129217010',
            'review_count': 2,
            'review_score': 5,
            'sold_count': 20,
            'matching_strategy': 'SINGLE_SELLER',
            'seller_id': 'magazineluiza',
            'seller_description': 'Magazine Luiza',
            'dimensions': {
                'depth': 0.67,
                'width': 0.52,
                'weight': 32,
                'height': 0.89
            },
            'type': 'product',
            'description': 'Fogão Brastemp Ative! 4 bocas de piso. Possui timer grill que facilita o seu dia a dia na cozinha para você ter mais \ntempo para fazer o que gosta. Ele vem também com timer, que ajuda a controlar o tempo de preparo dos alimentos e dupla chama, que é maior, mais potente e distribui o calor por igual. Assim, você pode preparar suas receitas bem mais rápido. Além disso, o grill elétrico serve para dourar, gratinar e deixar tudo mais bonito e saboroso. Para facilitar a limpeza, o Forno Smart Clean tem um acabamento interno especial que absorve e elimina 3 vezes mais gordura que os fornos comuns, suas grades são individuais e podem ser lavadas na pia ou na lava-louças e seu design super moderno vai combinar com o seu ambiente.',  # noqa
            'reference': 'Acendimento Automático',
            'grade': 10,
            'parent_sku': '0888944',
            'main_category': {
                'id': 'ED',
                'subcategory': {
                    'id': 'FOGO'
                }
            },
            'navigation_id': '088894400',
            'disable_on_matching': False,
            'selections': {
                '0': ['18036', '20334', '20355', '21375', '6874', '7039', '7041'],  # noqa
                '12966': ['16734', '16737']
            },
            'title': 'Fogão 4 Bocas Brastemp Ative! BF150AB Grill Timer',
            'sku': '088894400',
            'created_at': '2013-11-02T06:21:26.393000'
        }

    @classmethod
    def magazineluiza_sku_088894500(cls):
        return {
            'review_score': 0,
            'matching_strategy': 'SINGLE_SELLER',
            'main_variation': False,
            'updated_at': '2017-09-01T14:05:34.997000',
            'parent_sku': '0888944',
            'grade': 10,
            'disable_on_matching': False,
            'type': 'product',
            'main_category': {
                'subcategory': {
                    'id': 'FOGO'
                },
                'id': 'ED'
            },
            'description': 'Fogão Brastemp Ative! 4 bocas de piso. Possui timer grill que facilita o seu dia a dia na cozinha para você ter mais \ntempo para fazer o que gosta. Ele vem também com timer, que ajuda a controlar o tempo de preparo dos alimentos e dupla chama, que é maior, mais potente e distribui o calor por igual. Assim, você pode preparar suas receitas bem mais rápido. Além disso, o grill elétrico serve para dourar, gratinar e deixar tudo mais bonito e saboroso. Para facilitar a limpeza, o Forno Smart Clean tem um acabamento interno especial que absorve e elimina 3 vezes mais gordura que os fornos comuns, suas grades são individuais e podem ser lavadas na pia ou na lava-louças e seu design super moderno vai combinar com o seu ambiente.',  # noqa
            'ean': '7891129217003',
            'sold_count': 3,
            'brand': 'brastemp',
            'categories': [{
                'subcategories': [{
                    'id': 'FOGO'
                }, {
                    'id': 'EFP4'
                }, {
                    'id': 'FOGA'
                }],
                'id': 'ED'
            }],
            'reference': 'Acendimento Automático Branco',
            'created_at': '2013-11-02T06:21:26.393000',
            'sku': '088894500',
            'sells_to_company': True,
            'seller_id': 'magazineluiza',
            'title': 'Fogão 4 Bocas Brastemp Ative! BF150AB Grill Timer',
            'selections': {
                '12966': ['16734', '16737'],
                '0': ['18036', '20334', '20355', '21375', '6874', '7039', '7041']  # noqa
            },
            'review_count': 0,
            'navigation_id': '088894500',
            'seller_description': 'Magazine Luiza',
            'attributes': [{
                'type': 'voltage',
                'value': '220 Volts'
            }],
            'dimensions': {
                'height': 0.89,
                'width': 0.52,
                'depth': 0.67,
                'weight': 32
            }
        }

    @classmethod
    def magazineluiza_sku_088894600(cls):
        return {
            'attributes': [{
                'value': '110 Volts',
                'type': 'voltage'
            }],
            'updated_at': '2017-09-03T21:23:34.757000',
            'main_variation': True,
            'sells_to_company': True,
            'brand': 'brastemp',
            'categories': [{
                'id': 'ED',
                'subcategories': [{
                    'id': 'FOGO'
                }, {
                    'id': 'EFP4'
                }, {
                    'id': 'FOGA'
                }]
            }],
            'ean': '7891129219229',
            'review_count': 2,
            'review_score': 4.5,
            'sold_count': 27,
            'matching_strategy': 'SINGLE_SELLER',
            'seller_id': 'magazineluiza',
            'seller_description': 'Magazine Luiza',
            'dimensions': {
                'depth': 0.67,
                'width': 0.52,
                'weight': 32,
                'height': 0.89
            },
            'type': 'product',
            'description': 'Fogão Brastemp Ative! 4 bocas de piso. Possui timer grill que facilita o seu dia a dia na cozinha para você ter mais \ntempo para fazer o que gosta. Ele vem também com timer, que ajuda a controlar o tempo de preparo dos alimentos e dupla chama, que é maior, mais potente e distribui o calor por igual. Assim, você pode preparar suas receitas bem mais rápido. Além disso, o grill elétrico serve para dourar, gratinar e deixar tudo mais bonito e saboroso. Para facilitar a limpeza, o Forno Smart Clean tem um acabamento interno especial que absorve e elimina 3 vezes mais gordura que os fornos comuns, suas grades são individuais e podem ser lavadas na pia ou na lava-louças e seu design super moderno vai combinar com o seu ambiente.',  # noqa
            'reference': 'Timer Acendimento Automático',
            'grade': 10,
            'parent_sku': '0888946',
            'main_category': {
                'id': 'ED',
                'subcategory': {
                    'id': 'FOGO'
                }
            },
            'navigation_id': '088894600',
            'disable_on_matching': False,
            'selections': {
                '0': ['13146', '18036', '20334', '20355', '20577', '21427', '21498', '6874', '7039', '7041'],  # noqa
                '12966': ['16734', '16737']
            },
            'title': 'Fogão 4 Bocas Brastemp Ative! BF150AR Inox Grill',
            'sku': '088894600',
            'created_at': '2013-11-02T06:21:26.393000'
        }

    @classmethod
    def magazineluiza_sku_088894700(cls):
        return {
            'reference': 'Timer Acendimento Automático',
            'dimensions': {
                'weight': 32,
                'height': 0.89,
                'width': 0.52,
                'depth': 0.67
            },
            'title': 'Fogão 4 Bocas Brastemp Ative! BF150AR Inox Grill',
            'description': 'Fogão Brastemp Ative! 4 bocas de piso. Possui timer grill que facilita o seu dia a dia na cozinha para você ter mais \ntempo para fazer o que gosta. Ele vem também com timer, que ajuda a controlar o tempo de preparo dos alimentos e dupla chama, que é maior, mais potente e distribui o calor por igual. Assim, você pode preparar suas receitas bem mais rápido. Além disso, o grill elétrico serve para dourar, gratinar e deixar tudo mais bonito e saboroso. Para facilitar a limpeza, o Forno Smart Clean tem um acabamento interno especial que absorve e elimina 3 vezes mais gordura que os fornos comuns, suas grades são individuais e podem ser lavadas na pia ou na lava-louças e seu design super moderno vai combinar com o seu ambiente.',  # noqa
            'main_variation': False,
            'selections': {
                '0': ['13146', '18036', '20334', '20355', '20577', '21427', '21498', '6874', '7039', '7041'],  # noqa
                '12966': ['16734', '16737']
            },
            'brand': 'brastemp',
            'sells_to_company': True,
            'sku': '088894700',
            'grade': 10,
            'ean': '7891129219212',
            'review_score': 0,
            'main_category': {
                'id': 'ED',
                'subcategory': {
                    'id': 'FOGO'
                }
            },
            'navigation_id': '088894700',
            'created_at': '2013-11-02T06:21:26.393000',
            'seller_description': 'Magazine Luiza',
            'disable_on_matching': False,
            'categories': [{
                'id': 'ED',
                'subcategories': [{
                    'id': 'FOGO'
                }, {
                    'id': 'EFP4'
                }, {
                    'id': 'FOGA'
                }]
            }],
            'matching_strategy': 'SINGLE_SELLER',
            'type': 'product',
            'updated_at': '2017-09-03T19:44:05.117000',
            'seller_id': 'magazineluiza',
            'attributes': [{
                'value': '220 Volts',
                'type': 'voltage'
            }],
            'review_count': 0,
            'parent_sku': '0888946',
            'sold_count': 20
        }

    @classmethod
    def magazineluiza_sku_200513300(cls):
        return {
            'attributes': [{
                'type': 'voltage',
                'value': '110 Volts'
            }],
            'description': 'Fogão Ative! de embutir da Brastemp. Com 4 bocas, tem acendimento automático, mega chama e grades individuais. O forno tem capacidade de 65 litros, com luz, timer e grill. Além de eficiente, possui classificação energética A e tem design moderno, que vai combinar com a sua cozinha!',  # noqa
            'reference': 'de Embutir Inox Grill Timer Acendimento Automático',
            'main_category': {
                'id': 'ED',
                'subcategory': {
                    'id': 'FOEM'
                }
            },
            'sku': '200513300',
            'updated_at': '2017-09-02T14:16:54.783000',
            'type': 'product',
            'seller_id': 'magazineluiza',
            'dimensions': {
                'depth': 0.75,
                'height': 0.83,
                'weight': 33,
                'width': 0.69
            },
            'title': 'Fogão 4 Bocas Brastemp Ative! BYS4GARNNA',
            'sells_to_company': True,
            'ean': '7891129235380',
            'categories': [{
                'id': 'ED',
                'subcategories': [{
                    'id': 'FOEM'
                }, {
                    'id': 'EFE4'
                }]
            }],
            'brand': 'brastemp',
            'disable_on_matching': False,
            'review_count': 0,
            'review_score': 0,
            'created_at': '2014-09-03T07:50:17.727000',
            'matching_strategy': 'SINGLE_SELLER',
            'main_variation': True,
            'parent_sku': '2005133',
            'selections': {
                '0': ['17911', '18036', '6874'],
                '12966': ['16734', '16737']
            },
            'grade': 10,
            'navigation_id': '200513300',
            'seller_description': 'Magazine Luiza',
            'sold_count': 1
        }

    @classmethod
    def magazineluiza_sku_200513400(cls):
        return {
            'parent_sku': '2005133',
            'grade': 10,
            'main_variation': False,
            'main_category': {
                'subcategory': {
                    'id': 'FOEM'
                },
                'id': 'ED'
            },
            'seller_id': 'magazineluiza',
            'sells_to_company': True,
            'review_count': 0,
            'dimensions': {
                'depth': 0.75,
                'height': 0.83,
                'width': 0.69,
                'weight': 33
            },
            'ean': '7891129235397',
            'sku': '200513400',
            'reference': 'de Embutir Grill Timer Acendimento Automático',
            'review_score': 0,
            'created_at': '2014-09-03T07:50:17.727000',
            'seller_description': 'Magazine Luiza',
            'sold_count': 3,
            'brand': 'brastemp',
            'selections': {
                '0': ['17911', '18036', '6874'],
                '12966': ['16734', '16737']
            },
            'description': 'Fogão Ative! de embutir da Brastemp. Com 4 bocas, tem acendimento automático, mega chama e grades individuais. O forno tem capacidade de 65 litros, com luz, timer e grill. Além de eficiente, possui classificação energética A e tem design moderno, que vai combinar com a sua cozinha!',  # noqa
            'navigation_id': '200513400',
            'attributes': [{
                'type': 'voltage',
                'value': '220 Volts'
            }],
            'updated_at': '2017-09-02T07:07:15.863000',
            'title': 'Fogão 4 Bocas Brastemp Ative! BYS4GARNNA Inox',
            'disable_on_matching': False,
            'type': 'product',
            'categories': [{
                'subcategories': [{
                    'id': 'FOEM'
                }, {
                    'id': 'EFE4'
                }, {
                    'id': 'FOGO'
                }],
                'id': 'ED'
            }],
            'matching_strategy': 'SINGLE_SELLER'
        }

    @classmethod
    def magazineluiza_sku_011704201(cls):
        return {
            'sku': '011704201',
            'reference': '8 Serviços',
            'created_at': '2011-09-14T05:10:49.357000',
            'main_variation': True,
            'sold_count': 7,
            'review_score': 4.9,
            'disable_on_matching': False,
            'type': 'product',
            'parent_sku': '0117042',
            'seller_id': 'magazineluiza',
            'attributes': [{
                'type': 'color',
                'value': 'Branco'
            }, {
                'type': 'voltage',
                'value': '110 Volts'
            }],
            'description': 'A nova lava-louças Brastemp Ative! 8 serviços traz mais liberdade para você e sua família. São 5 diferentes ciclos pré-programados que lavam louças de até 8 pessoas. Seu cesto superior tem regulagem de altura permitindo acondicionar qualquer tamanho de louça. Conta com indicador de etapas e visor, que permite acompanhar em qual fase a lavagem está. ',  # noqa
            'selections': {
                '12966': ['16734', '16737'],
                '0': ['10121', '10246', '11016', '12969', '18036', '19448', '19597', '20334', '20355', '21532', '6874', '7039']  # noqa
            },
            'seller_description': 'Magazine Luiza',
            'categories': [{
                'id': 'ED',
                'subcategories': [{
                    'id': 'LALO'
                }]
            }],
            'main_category': {
                'subcategory': {
                    'id': 'LALO'
                },
                'id': 'ED'
            },
            'title': 'Lava-Louças Brastemp Ative! BLF08AB',
            'matching_strategy': 'SINGLE_SELLER',
            'sells_to_company': True,
            'grade': 10,
            'ean': '7891129207370',
            'dimensions': {
                'depth': 0.59,
                'height': 0.62,
                'width': 0.51,
                'weight': 31.25
            },
            'review_count': 7,
            'brand': 'brastemp',
            'updated_at': '2017-09-14T14:40:25.123000',
            'navigation_id': '011704201'
        }

    @classmethod
    def whirlpool_sku_192(cls):
        return {
            'sells_to_company': False,
            'seller_id': 'whirlpool',
            'review_count': 0,
            'brand': 'Brastemp',
            'sku': '192',
            'dimensions': {
                'width': 10,
                'weight': 0.029,
                'depth': 10,
                'height': 10
            },
            'grade': 10,
            'categories': [{
                'description': 'Eletrodomésticos',
                'subcategories': [{
                    'description': 'Lava-Louças',
                    'id': 'LALO'
                }],
                'id': 'ED'
            }],
            'title': 'Lava-Louças Brastemp Ative! 8 Serviços',
            'disable_on_matching': False,
            'navigation_id': '9169069',
            'type': 'product',
            'release_date': '2017-09-14T15:22:07.648328+00:00',
            'updated_at': '2017-09-14T15:22:06.027399+00:00',
            'sold_count': 0,
            'attributes': [{
                'value': '110V',
                'type': 'voltage'
            }],
            'ean': '7891129207370',
            'parent_sku': '192',
            'seller_description': 'Brastemp',
            'main_variation': True,
            'description': 'Facilite seu dia a diaA Lava-louças Brastemp Ative! 8 serviços conta com 5 ciclos para a lavagem de louças de até 8 pessoas de uma só vez, mais praticidade para o seu dia a dia. De uso intuitivo, tem com identificador de etapas para o acompanhamento da lavagem, função Acquaspray e cestos ajustáveis.8 serviçosCom capacidade total para 8 serviços, lava até 24 pratos, oito copos, oito xícaras, oito pires e 40 talheres de uma só vez.Ciclos de lavagemSão 5 ciclos pré-programados para diferentes tipos de louças e lavagens, entre eles: Dia a Dia, para peças de uso diário; Pesado, para panelas e tigelas; Delicado, ideal para taças e cristais; Econômico e Rápido.Identificador de etapasPor meio do identificador de etapas é possível saber em qual estágio a o processo está: lavagem, enxágue ou secagem.Cestos ajustáveisPara melhor aproveitamento do espaço, os cestos superiores são reguláveis de acordo com o tamanho da louça.',  # noqa
            'matching_strategy': 'SINGLE_SELLER',
            'review_score': 5,
            'created_at': '2016-12-05T19:35:47.180392+00:00',
            'reference': 'Brastemp'
        }

    @classmethod
    def cookeletroraro_sku_2000160(cls):
        return {
            'updated_at': '2017-08-21T20:01:31.964012+00:00',
            'disable_on_matching': False,
            'seller_description': 'Cook Eletroraro',
            'release_date': '2017-08-21T20:01:33.209594+00:00',
            'type': 'product',
            'brand': 'Brastemp',
            'title': 'Lava-louças Brastemp Ative! 8 Serviços Cor Inox 110V BLF08ASANA',  # noqa
            'attributes': [{
                'type': 'voltage',
                'value': '220V'
            }],
            'dimensions': {
                'weight': 30.65,
                'depth': 59,
                'height': 62.4,
                'width': 50.8
            },
            'reference': 'Brastemp',
            'categories': [{
                'subcategories': [{
                    'description': 'Lava-Louças',
                    'id': 'LALO'
                }],
                'description': 'Eletrodomésticos',
                'id': 'ED'
            }],
            'grade': 10,
            'review_score': 5,
            'sold_count': 0,
            'sells_to_company': True,
            'created_at': '2017-01-19T17:38:19.734825+00:00',
            'navigation_id': '8577101',
            'parent_sku': '2000150',
            'sku': '2000160',
            'main_variation': True,
            'seller_id': 'cookeletroraro',
            'description': ' Facilite seu dia-a-dia! \r\n&nbsp;\r\nA Lava-louças Brastemp Ative! 8 serviços conta com 5 ciclos para a lavagem de louças de até 8 pessoas de uma só vez, mais praticidade para o seu dia a dia. De uso intuitivo, tem com identificador de etapas para o acompanhamento da lavagem, função Acquaspray e cestos ajustáveis.\r\n\r\n &nbsp;\r\n&nbsp;&nbsp;&nbsp;5 ciclos de lavagem&nbsp;8 serviços&nbsp;Função Acquaspray&nbsp;Cestos ajustáveis\r\n\r\n 5 ciclos de lavagem\r\nSão 5 ciclos pré-programados para diferentes tipos de louças e lavagens, entre eles: Dia a Dia, para peças de uso diário; Pesado, para panelas e tigelas; Delicado, ideal para taças e cristais; Econômico e Rápido.\r\n\r\n 8 serviços\r\nCom capacidade total para 8 serviços, lava até 24 pratos, oito copos, oito xícaras, oito pires e 40 talheres de uma só vez.\r\n\r\n Função Acquaspray\r\nPermite acumular a louça por mais tempo e lavá-la em uma única vez. Isso porque ela libera jatos de água esporádicos que removem a sujeira e evitam que os resíduos ressequem enquanto a lavagem e prorrogada.\r\n\r\n Cestos ajustáveis \r\nPara melhor aproveitamento do espaço, os cestos superiores são reguláveis de acordo com o tamanho da louça.\r\n\r\n',  # noqa
            'review_count': 0,
            'ean': '7891129207370',
            'matching_strategy': 'SINGLE_SELLER'
        }

    @classmethod
    def magazineluiza_sku_011704400(cls):
        return {
            'sold_count': 37,
            'navigation_id': '011704400',
            'sells_to_company': True,
            'grade': 10,
            'seller_description': 'Magazine Luiza',
            'title': 'Lava-Louças Brastemp Ative! BLF08AS',
            'attributes': [{
                'type': 'voltage',
                'value': '110 Volts'
            }],
            'brand': 'brastemp',
            'selections': {
                '12966': ['16734', '16737'],
                '0': ['10121', '10246', '11016', '17911', '18036', '19448', '19512', '19597', '20033', '20679', '21532', '6874', '7039', '7091']  # noqa
            },
            'disable_on_matching': False,
            'seller_id': 'magazineluiza',
            'type': 'product',
            'description': 'A nova lava-louças Brastemp Ative! 8 serviços traz mais liberdade para você e sua família. São 5 diferentes ciclos pré-programados que lavam louças de até 8 pessoas. Seu cesto superior tem regulagem de altura permitindo acondicionar qualquer tamanho de louça. Conta com indicador de etapas e visor na porta que permite o acompanhamento de todo processo de lavagem além de permitir acompanhar em qual fase a lavagem está. É, ainda, compacta e flexível e pode ser instalada em bancadas ou nichos.\n',  # noqa
            'dimensions': {
                'depth': 0.59,
                'weight': 31.25,
                'height': 0.62,
                'width': 0.51
            },
            'main_category': {
                'id': 'ED',
                'subcategory': {
                    'id': 'LALO'
                }
            },
            'review_score': 4.9,
            'updated_at': '2017-09-14T15:55:55.177000',
            'matching_strategy': 'SINGLE_SELLER',
            'review_count': 9,
            'parent_sku': '0117044',
            'ean': '7891129204836',
            'main_variation': True,
            'created_at': '2011-09-14T05:10:49.357000',
            'categories': [{
                'id': 'ED',
                'subcategories': [{
                    'id': 'LALO'
                }]
            }],
            'sku': '011704400',
            'reference': '8 Serviços'
        }

    @classmethod
    def cookeletroraro_sku_2000159(cls):
        return {
            'title': 'Lava-louças Brastemp Ative! 8 Serviços Cor Inox 110V BLF08ASANA',  # noqa
            'updated_at': '2017-08-21T20:01:31.964012+00:00',
            'created_at': '2017-01-19T17:38:19.734825+00:00',
            'main_variation': False,
            'dimensions': {
                'depth': 59,
                'weight': 30.65,
                'height': 62.4,
                'width': 50.8
            },
            'review_score': 5,
            'seller_id': 'cookeletroraro',
            'seller_description': 'Cook Eletroraro',
            'grade': 10,
            'review_count': 0,
            'type': 'product',
            'release_date': '2017-09-13T20:16:04.519991+00:00',
            'sells_to_company': True,
            'sku': '2000159',
            'sold_count': 0,
            'matching_strategy': 'SINGLE_SELLER',
            'categories': [{
                'id': 'ED',
                'description': 'Eletrodomésticos',
                'subcategories': [{
                    'id': 'LALO',
                    'description': 'Lava-Louças'
                }]
            }],
            'ean': '7891129204836',
            'attributes': [{
                'type': 'voltage',
                'value': '110V'
            }],
            'parent_sku': '2000150',
            'brand': 'Brastemp',
            'reference': 'Brastemp',
            'navigation_id': '8530173',
            'description': ' Facilite seu dia-a-dia! \r\n&nbsp;\r\nA Lava-louças Brastemp Ative! 8 serviços conta com 5 ciclos para a lavagem de louças de até 8 pessoas de uma só vez, mais praticidade para o seu dia a dia. De uso intuitivo, tem com identificador de etapas para o acompanhamento da lavagem, função Acquaspray e cestos ajustáveis.\r\n\r\n &nbsp;\r\n&nbsp;&nbsp;&nbsp;5 ciclos de lavagem&nbsp;8 serviços&nbsp;Função Acquaspray&nbsp;Cestos ajustáveis\r\n\r\n 5 ciclos de lavagem\r\nSão 5 ciclos pré-programados para diferentes tipos de louças e lavagens, entre eles: Dia a Dia, para peças de uso diário; Pesado, para panelas e tigelas; Delicado, ideal para taças e cristais; Econômico e Rápido.\r\n\r\n 8 serviços\r\nCom capacidade total para 8 serviços, lava até 24 pratos, oito copos, oito xícaras, oito pires e 40 talheres de uma só vez.\r\n\r\n Função Acquaspray\r\nPermite acumular a louça por mais tempo e lavá-la em uma única vez. Isso porque ela libera jatos de água esporádicos que removem a sujeira e evitam que os resíduos ressequem enquanto a lavagem e prorrogada.\r\n\r\n Cestos ajustáveis \r\nPara melhor aproveitamento do espaço, os cestos superiores são reguláveis de acordo com o tamanho da louça.\r\n\r\n',  # noqa
            'disable_on_matching': False
        }

    @classmethod
    def magazineluiza_sku_011704500(cls):
        return {
            'sku': '011704500',
            'reference': '8 Serviços',
            'created_at': '2011-09-14T05:10:49.357000',
            'main_variation': False,
            'sold_count': 19,
            'review_score': 0,
            'disable_on_matching': False,
            'type': 'product',
            'parent_sku': '0117044',
            'seller_id': 'magazineluiza',
            'attributes': [{
                'value': '220 Volts',
                'type': 'voltage'
            }],
            'description': 'A nova lava-louças Brastemp Ative! 8 serviços traz mais liberdade para você e sua família. São 5 diferentes ciclos pré-programados que lavam louças de até 8 pessoas. Seu cesto superior tem regulagem de altura permitindo acondicionar qualquer tamanho de louça. Conta com indicador de etapas e visor na porta que permite o acompanhamento de todo processo de lavagem além de permitir acompanhar em qual fase a lavagem está. É, ainda, compacta e flexível e pode ser instalada em bancadas ou nichos.\n',  # noqa
            'selections': {
                '0': ['10121', '10246', '11016', '17911', '18036', '19448', '19512', '19597', '20033', '20679', '21532', '6874', '7039', '7091'],  # noqa
                '12966': ['16734', '16737']
            },
            'seller_description': 'Magazine Luiza',
            'categories': [{
                'id': 'ED',
                'subcategories': [{
                    'id': 'LALO'
                }]
            }],
            'main_category': {
                'subcategory': {
                    'id': 'LALO'
                },
                'id': 'ED'
            },
            'title': 'Lava-Louças Brastemp Ative! BLF08AS',
            'matching_strategy': 'SINGLE_SELLER',
            'sells_to_company': True,
            'grade': 10,
            'ean': '7891129205741',
            'dimensions': {
                'depth': 0.59,
                'height': 0.62,
                'weight': 31.25,
                'width': 0.51
            },
            'review_count': 0,
            'brand': 'brastemp',
            'updated_at': '2017-09-14T08:14:24.507000',
            'navigation_id': '011704500'
        }

    @classmethod
    def whirlpool_sku_334(cls):
        return {
            'review_score': 5,
            'brand': 'Brastemp',
            'categories': [{
                'description': 'Eletrodomésticos',
                'id': 'ED',
                'subcategories': [{
                    'description': 'Lava-Louças',
                    'id': 'LALO'
                }]
            }],
            'seller_id': 'whirlpool',
            'type': 'product',
            'sold_count': 0,
            'disable_on_matching': False,
            'navigation_id': '9127000',
            'review_count': 0,
            'description': 'Facilite seu dia a diaA Lava-louças Brastemp Ative! 8 serviços conta com 5 ciclos para a lavagem de louças de até 8 pessoas de uma só vez, mais praticidade para o seu dia a dia. De uso intuitivo, tem com identificador de etapas para o acompanhamento da lavagem, função Acquaspray e cestos ajustáveis.8 serviçosCom capacidade total para 8 serviços, lava até 24 pratos, oito copos, oito xícaras, oito pires e 40 talheres de uma só vez.Ciclos de lavagemSão 5 ciclos pré-programados para diferentes tipos de louças e lavagens, entre eles: Dia a Dia, para peças de uso diário; Pesado, para panelas e tigelas; Delicado, ideal para taças e cristais; Econômico e Rápido.Identificador de etapasPor meio do identificador de etapas é possível saber em qual estágio a o processo está: lavagem, enxágue ou secagem.Cestos ajustáveisPara melhor aproveitamento do espaço, os cestos superiores são reguláveis de acordo com o tamanho da louça.',  # noqa
            'sells_to_company': False,
            'title': 'Lava-Louças Brastemp Ative! 8 Serviços',
            'dimensions': {
                'depth': 10,
                'weight': 0.029,
                'width': 10,
                'height': 10
            },
            'parent_sku': '192',
            'matching_strategy': 'SINGLE_SELLER',
            'created_at': '2016-12-05T19:35:47.180392+00:00',
            'seller_description': 'Brastemp',
            'main_variation': False,
            'reference': 'Brastemp',
            'updated_at': '2017-09-14T15:21:39.260336+00:00',
            'attributes': [{
                'value': '220V',
                'type': 'voltage'
            }],
            'grade': 10,
            'release_date': '2017-09-14T15:21:42.767730+00:00',
            'ean': '7891129204829',
            'sku': '334'
        }

    @classmethod
    def cookeletroraro_sku_2000837(cls):
        return {
            'categories': [{
                'description': 'Eletrodomésticos',
                'id': 'ED',
                'subcategories': [{
                    'description': 'Lava-Louças',
                    'id': 'LALO'
                }]
            }],
            'seller_description': 'Cook Eletroraro',
            'grade': 10,
            'type': 'product',
            'title': 'Lava-louças Brastemp Ative! 8 Serviços BLF08ASBNA',
            'reference': 'Brastemp',
            'sold_count': 0,
            'main_variation': True,
            'description': 'Chega de perder tempo com suas louças após aquele delicioso almoço em família. Com design inovador, a nova lava-louças Brastemp Ative! 8 serviços é pequena por fora e gigante por dentro: lava louças de até 8 pessoas (8 copos, 8 xícaras, 8 pratos de sobremesa, 8 pires, 8 pratos rasos, 8 pratos fundos, 8 colheres de sopa, 8 colheres de sobremesa, 8 garfos, 8 facas, 8 colheres de chá). Além de seus 5 diferentes ciclos (Dia-a-dia, Pesado, Delicado, Rápido e Econômico), seu cesto superior flexível conta com regulagem de altura permitindo lavar qualquer tipo de louça. Tudo isso para deixar o seu dia ainda mais livre. Então não perca tempo. Compre já a nova Lava-Louças Brastemp Clean. Porque aproveitar a vida é assiiim, uma Brastemp.',  # noqa
            'updated_at': '2017-08-18T18:38:49.161155+00:00',
            'brand': 'Brastemp',
            'review_score': 5,
            'created_at': '2017-01-19T17:35:50.378612+00:00',
            'dimensions': {
                'weight': 60,
                'depth': 80,
                'height': 80,
                'width': 80
            },
            'attributes': [{
                'type': 'voltage',
                'value': '220V'
            }],
            'seller_id': 'cookeletroraro',
            'matching_strategy': 'SINGLE_SELLER',
            'disable_on_matching': False,
            'sells_to_company': True,
            'review_count': 0,
            'sku': '2000837',
            'ean': '7891129205741',
            'navigation_id': '8575327',
            'release_date': '2017-08-18T18:38:50.398437+00:00',
            'parent_sku': '2000845'
        }

    @classmethod
    def magazineluiza_sku_011704301(cls):
        return {
            'sku': '011704301',
            'reference': '8 Serviços',
            'created_at': '2011-09-14T05:10:49.357000',
            'main_variation': False,
            'sold_count': 1,
            'review_score': 0,
            'disable_on_matching': False,
            'type': 'product',
            'parent_sku': '0117042',
            'seller_id': 'magazineluiza',
            'attributes': [{
                'value': 'Branco',
                'type': 'color'
            }, {
                'value': '220 Volts',
                'type': 'voltage'
            }],
            'description': 'A nova lava-louças Brastemp Ative! 8 serviços traz mais liberdade para você e sua família. São 5 diferentes ciclos pré-programados que lavam louças de até 8 pessoas. Seu cesto superior tem regulagem de altura permitindo acondicionar qualquer tamanho de louça. Conta com indicador de etapas e visor, que permite acompanhar em qual fase a lavagem está. ',  # noqa
            'selections': {
                '0': ['10121', '10246', '11016', '12969', '18036', '19448', '19597', '20334', '20355', '21532', '6874', '7039'],  # noqa
                '12966': ['16734', '16737']
            },
            'seller_description': 'Magazine Luiza',
            'categories': [{
                'id': 'ED',
                'subcategories': [{
                    'id': 'LALO'
                }]
            }],
            'main_category': {
                'subcategory': {
                    'id': 'LALO'
                },
                'id': 'ED'
            },
            'title': 'Lava-Louças Brastemp Ative! BLF08AB',
            'matching_strategy': 'SINGLE_SELLER',
            'sells_to_company': True,
            'grade': 10,
            'ean': '7891129204829',
            'dimensions': {
                'depth': 0.59,
                'height': 0.62,
                'weight': 31.25,
                'width': 0.51
            },
            'review_count': 0,
            'brand': 'brastemp',
            'updated_at': '2017-09-14T10:40:06.557000',
            'navigation_id': '011704301'
        }

    @classmethod
    def whirlpool_sku_335(cls):
        return {
            'sold_count': 0,
            'navigation_id': '9147175',
            'release_date': '2017-09-14T19:28:24.563063+00:00',
            'grade': 10,
            'seller_description': 'Brastemp',
            'title': 'Lava-Louças Brastemp Ative! 8 Serviços',
            'sells_to_company': False,
            'brand': 'Brastemp',
            'disable_on_matching': False,
            'seller_id': 'whirlpool',
            'type': 'product',
            'dimensions': {
                'width': 10,
                'depth': 10,
                'height': 10,
                'weight': 0.029
            },
            'description': 'Facilite seu dia a diaA Lava-louças Brastemp Ative! 8 serviços conta com 5 ciclos para a lavagem de louças de até 8 pessoas de uma só vez, mais praticidade para o seu dia a dia. De uso intuitivo, tem com identificador de etapas para o acompanhamento da lavagem, função Acquaspray e cestos ajustáveis.8 serviçosCom capacidade total para 8 serviços, lava até 24 pratos, oito copos, oito xícaras, oito pires e 40 talheres de uma só vez.Ciclos de lavagemSão 5 ciclos pré-programados para diferentes tipos de louças e lavagens, entre eles: Dia a Dia, para peças de uso diário; Pesado, para panelas e tigelas; Delicado, ideal para taças e cristais; Econômico e Rápido.Identificador de etapasPor meio do identificador de etapas é possível saber em qual estágio a o processo está: lavagem, enxágue ou secagem.Cestos ajustáveisPara melhor aproveitamento do espaço, os cestos superiores são reguláveis de acordo com o tamanho da louça.',  # noqa
            'review_score': 5,
            'updated_at': '2017-09-14T19:28:22.370748+00:00',
            'matching_strategy': 'SINGLE_SELLER',
            'review_count': 0,
            'attributes': [{
                'value': '220V',
                'type': 'voltage'
            }],
            'parent_sku': '193',
            'ean': '7891129205741',
            'main_variation': False,
            'created_at': '2016-12-06T00:10:54.653933+00:00',
            'categories': [{
                'id': 'ED',
                'description': 'Eletrodomésticos',
                'subcategories': [{
                    'id': 'LALO',
                    'description': 'Lava-Louças'
                }]
            }],
            'sku': '335',
            'reference': 'Brastemp'
        }

    @classmethod
    def magazineluiza_sku_193410900(cls):
        return {
            'disable_on_matching': False,
            'type': 'product',
            'attributes': [{
                'value': 'Preto',
                'type': 'color'
            }, {
                'value': '43\'',
                'type': 'inch'
            }],
            'sku': '193410900',
            'created_at': '2017-08-19T08:07:48.747000',
            'selections': {
                '12966': ['16734', '16737'],
                '0': ['18423', '21507', '21508', '21509', '21521', '21541', '21570', '21668', '21680', '21692', '21755', '21768', '21800', '21801', '21804', '21824', '21838', '6874']  # noqa
            },
            'sold_count': 351,
            'title': 'Smart TV LED 43” Philips 4K Ultra HD 43PUG6102/78',
            'description': 'TV LED Smart ultrafina 4K com Pixel Plus Ultra HD. Conectividade exclusiva, versátil e elegante. A TV Philips 6100 proporciona qualidade de imagem HD ultra 4K com riqueza de detalhes. Com a conexão da Smart TV, você terá fácil acesso ao entretenimento.\n\nA TV Ultra HD tem 4 vezes a resolução de uma TV Full HD convencional. Com mais de 8 milhões de pixels e nossa tecnologia de Redimensionamento Ultra Resolution exclusiva, você curtirá a melhor qualidade de imagem. Quanto maior a qualidade de seu conteúdo original, melhor imagem e resolução para você aproveitar. Aproveite melhor nitidez, maior percepção de profundidade, contraste superior, movimentos naturais e detalhes incríveis.\n\nExperimente a nitidez do Ultra HD 4K com o mecanismo Pixel Plus Ultra HD da Philips. Ele otimiza a qualidade da imagem para proporcionar imagens fluidas perfeitas com detalhes e profundidade incríveis. Desfrute de imagens 4K mais nítidas com brancos mais brilhantes e pretos mais intensos, sempre.\n\nDescubra uma experiência mais inteligente que há além da tradicional transmissão e locação de filmes, vídeos ou jogos a partir de lojas de vídeo on-line. Assista ao catch-up TV de seus canais favoritos e desfrute de uma ampla seleção de aplicativos on-line com a Smart TV.\n\n\n\n',  # noqa
            'ean': '7898620270506',
            'grade': 1010,
            'navigation_id': '193410900',
            'main_variation': True,
            'review_score': 0,
            'seller_description': 'Magazine Luiza',
            'parent_sku': '1934109',
            'reference': 'Conversor Digital Wi-Fi 4 HDMI 2 USB DTVi',
            'categories': [{
                'subcategories': [{
                    'id': 'TV4K'
                }, {
                    'id': '4K60'
                }, {
                    'id': '4KAI'
                }, {
                    'id': '4KCD'
                }, {
                    'id': '4KSM'
                }, {
                    'id': '4KUH'
                }, {
                    'id': 'ELIT'
                }, {
                    'id': 'LE43'
                }, {
                    'id': 'LE4K'
                }, {
                    'id': 'LE6Z'
                }, {
                    'id': 'LEAI'
                }, {
                    'id': 'LECI'
                }, {
                    'id': 'LESM'
                }, {
                    'id': 'PECO'
                }, {
                    'id': 'S60H'
                }, {
                    'id': 'SM43'
                }, {
                    'id': 'SMAI'
                }, {
                    'id': 'SMCD'
                }, {
                    'id': 'SMLD'
                }, {
                    'id': 'TLED'
                }],
                'id': 'ET'
            }],
            'matching_strategy': 'SINGLE_SELLER',
            'seller_id': 'magazineluiza',
            'main_category': {
                'subcategory': {
                    'id': 'TV4K'
                },
                'id': 'ET'
            },
            'brand': 'philips',
            'updated_at': '2017-10-08T07:53:53.960000',
            'review_count': 0,
            'dimensions': {
                'height': 0.66,
                'depth': 0.15,
                'width': 1.06,
                'weight': 12
            },
            'sells_to_company': True,
            'md5': '5d4f90f308109d03aeaf72e94091b3e3'
        }

    @classmethod
    def magazineluiza_sku_193411000(cls):
        return {
            'sku': '193411000',
            'reference': 'Conversor Digital Wi-Fi 4 HDMI 2 USB DTVi',
            'created_at': '2017-08-19T08:07:48.747000',
            'main_variation': True,
            'sold_count': 250,
            'review_score': 0,
            'disable_on_matching': False,
            'type': 'product',
            'parent_sku': '1934109',
            'seller_id': 'magazineluiza',
            'attributes': [{
                'value': 'Preto',
                'type': 'color'
            }, {
                'value': '50\'',
                'type': 'inch'
            }],
            'description': 'TV LED Smart ultrafina 4K com Pixel Plus Ultra HD. Conectividade exclusiva, versátil e elegante. A TV Philips 6100 proporciona qualidade de imagem HD ultra 4K com riqueza de detalhes. Com a conexão da Smart TV, você terá fácil acesso ao entretenimento.\n\nA TV Ultra HD tem 4 vezes a resolução de uma TV Full HD convencional. Com mais de 8 milhões de pixels e nossa tecnologia de Redimensionamento Ultra Resolution exclusiva, você curtirá a melhor qualidade de imagem. Quanto maior a qualidade de seu conteúdo original, melhor imagem e resolução para você aproveitar. Aproveite melhor nitidez, maior percepção de profundidade, contraste superior, movimentos naturais e detalhes incríveis.\n\nExperimente a nitidez do Ultra HD 4K com o mecanismo Pixel Plus Ultra HD da Philips. Ele otimiza a qualidade da imagem para proporcionar imagens fluidas perfeitas com detalhes e profundidade incríveis. Desfrute de imagens 4K mais nítidas com brancos mais brilhantes e pretos mais intensos, sempre.\n\nDescubra uma experiência mais inteligente que há além da tradicional transmissão e locação de filmes, vídeos ou jogos a partir de lojas de vídeo on-line. Assista ao catch-up TV de seus canais favoritos e desfrute de uma ampla seleção de aplicativos on-line com a Smart TV.\n\n\n\n',  # noqa
            'selections': {
                '12966': ['16734', '16737'],
                '0': ['18423', '18428', '21755', '21800', '21801', '21824', '21838', '6874']  # noqa
            },
            'seller_description': 'Magazine Luiza',
            'categories': [{
                'id': 'ET',
                'subcategories': [{
                    'id': 'TV4K'
                }, {
                    'id': '4KCD'
                }, {
                    'id': '4KSM'
                }, {
                    'id': '4KUH'
                }, {
                    'id': 'ELIT'
                }, {
                    'id': 'LE4K'
                }, {
                    'id': 'LE50'
                }, {
                    'id': 'LE6Z'
                }, {
                    'id': 'LEAI'
                }, {
                    'id': 'LECI'
                }, {
                    'id': 'PECO'
                }, {
                    'id': 'S60H'
                }, {
                    'id': 'SM4K'
                }, {
                    'id': 'SM50'
                }, {
                    'id': 'SMAI'
                }, {
                    'id': 'SMCD'
                }, {
                    'id': 'SMLD'
                }, {
                    'id': 'TLED'
                }]
            }],
            'main_category': {
                'subcategory': {
                    'id': 'TV4K'
                },
                'id': 'ET'
            },
            'title': 'Smart TV LED 50” Philips 4K Ultra HD 50PUG6102/78',
            'matching_strategy': 'SINGLE_SELLER',
            'sells_to_company': True,
            'grade': 1010,
            'ean': '7898620270490',
            'dimensions': {
                'weight': 17.2,
                'width': 0.16,
                'depth': 1.23,
                'height': 0.8
            },
            'review_count': 0,
            'brand': 'philips',
            'updated_at': '2017-10-08T08:22:25.053000',
            'navigation_id': '193411000',
            'md5': 'd46ac7c633e756943aa2d8efeaf66000'
        }

    @classmethod
    def magazineluiza_sku_193411100(cls):
        return {
            'disable_on_matching': False,
            'review_score': 0,
            'attributes': [{
                'value': 'Preto',
                'type': 'color'
            }, {
                'value': '55\'',
                'type': 'inch'
            }],
            'reference': 'Conversor Digital Wi-Fi 4 HDMI 2 USB DTVi',
            'ean': '7898620270483',
            'title': 'Smart TV LED 55” Philips 4K Ultra HD 55PUG6102/78',
            'sells_to_company': True,
            'grade': 1010,
            'navigation_id': '193411100',
            'created_at': '2017-08-19T08:07:48.747000',
            'type': 'product',
            'parent_sku': '1934109',
            'sku': '193411100',
            'matching_strategy': 'SINGLE_SELLER',
            'sold_count': 4,
            'description': 'TV LED Smart ultrafina 4K com Pixel Plus Ultra HD. Conectividade exclusiva, versátil e elegante. A TV Philips 6100 proporciona qualidade de imagem HD ultra 4K com riqueza de detalhes. Com a conexão da Smart TV, você terá fácil acesso ao entretenimento.\n\nA TV Ultra HD tem 4 vezes a resolução de uma TV Full HD convencional. Com mais de 8 milhões de pixels e nossa tecnologia de Redimensionamento Ultra Resolution exclusiva, você curtirá a melhor qualidade de imagem. Quanto maior a qualidade de seu conteúdo original, melhor imagem e resolução para você aproveitar. Aproveite melhor nitidez, maior percepção de profundidade, contraste superior, movimentos naturais e detalhes incríveis.\n\nExperimente a nitidez do Ultra HD 4K com o mecanismo Pixel Plus Ultra HD da Philips. Ele otimiza a qualidade da imagem para proporcionar imagens fluidas perfeitas com detalhes e profundidade incríveis. Desfrute de imagens 4K mais nítidas com brancos mais brilhantes e pretos mais intensos, sempre.\n\nDescubra uma experiência mais inteligente que há além da tradicional transmissão e locação de filmes, vídeos ou jogos a partir de lojas de vídeo on-line. Assista ao catch-up TV de seus canais favoritos e desfrute de uma ampla seleção de aplicativos on-line com a Smart TV.\n\n\n\n',  # noqa
            'brand': 'philips',
            'seller_description': 'Magazine Luiza',
            'review_count': 0,
            'updated_at': '2017-10-07T12:43:17.070000',
            'dimensions': {
                'depth': 1.35,
                'height': 0.83,
                'width': 0.17,
                'weight': 20.19
            },
            'categories': [{
                'id': 'ET',
                'subcategories': [{
                    'id': 'TV4K'
                }, {
                    'id': '4K60'
                }, {
                    'id': '4KAI'
                }, {
                    'id': '4KCD'
                }, {
                    'id': '4KSM'
                }, {
                    'id': 'LE55'
                }, {
                    'id': 'LE6Z'
                }, {
                    'id': 'LECI'
                }, {
                    'id': 'LESM'
                }, {
                    'id': 'SMCD'
                }]
            }],
            'main_category': {
                'id': 'ET',
                'subcategory': {
                    'id': 'TV4K'
                }
            },
            'main_variation': True,
            'seller_id': 'magazineluiza',
            'selections': {
                '0': ['18423', '18428', '21668', '21755', '6874'],
                '12966': ['16734', '16737']
            },
            'md5': 'a0af0a5a4a33da9a09bbbf49fe03537e'
        }

    @classmethod
    def magazineluiza_sku_213445800(cls):
        return {
            'categories': [{
                'id': 'ED',
                'subcategories': [{
                    'id': 'LAVA'
                }]
            }],
            'seller_description': 'Magazine Luiza',
            'disable_on_matching': False,
            'sku': '213445800',
            'navigation_id': '213445800',
            'parent_sku': '2134458',
            'attributes': [{
                'type': 'voltage',
                'value': '110 Volts'
            }],
            'brand': 'electrolux',
            'description': 'Lavadora Electrolux, silenciosa tem capacidade de 13Kg, lava mais roupa em menos tempo e espaço, economizando água, energia e produtos de limpeza. O dispencer automático ADDMix, calcula a dosagem de sabão e amaciante, faz a mistura exata, na hora correta. Tem 5 Níveis de água, incluindo nível automático de água que dosa o nível de água da máquina de acordo com a programação e a quantidade de roupa na máquina. E com a exclusiva função Turbo Secagem você aumenta o tempo de centrifugação permitindo que suas roupas saiam mais secas da lavadora do que numa centrifugação normal.\n',  # noqa
            'reference': '13kg',
            'sold_count': 29,
            'review_score': 0,
            'seller_id': 'magazineluiza',
            'review_count': 0,
            'ean': '7896584066562',
            'main_category': {
                'id': 'ED',
                'subcategory': {
                    'id': 'LAVA'
                }
            },
            'title': 'Lavadora de Roupas Electrolux Addmix',
            'sells_to_company': True,
            'matching_strategy': 'SINGLE_SELLER',
            'dimensions': {
                'height': 1.05,
                'width': 0.69,
                'weight': 50,
                'depth': 0.76
            },
            'grade': 10,
            'updated_at': '2017-10-21T11:17:36.500000',
            'type': 'product',
            'main_variation': True,
            'created_at': '2015-07-15T06:37:07.747000',
            'md5': 'aaaa4778bbc48ce58566914b3db10842'
        }

    @classmethod
    def magazineluiza_sku_213445900(cls):
        return {
            'dimensions': {
                'height': 1.05,
                'depth': 0.76,
                'weight': 50,
                'width': 0.69
            },
            'sold_count': 3,
            'parent_sku': '2134458',
            'seller_description': 'Magazine Luiza',
            'sells_to_company': True,
            'title': 'Lavadora de Roupas Electrolux Addmix',
            'grade': 10,
            'main_variation': False,
            'type': 'product',
            'disable_on_matching': False,
            'brand': 'electrolux',
            'review_count': 0,
            'updated_at': '2017-08-26T07:03:46.277000',
            'reference': '13kg',
            'sku': '213445900',
            'seller_id': 'magazineluiza',
            'navigation_id': '213445900',
            'created_at': '2015-07-15T06:37:07.747000',
            'ean': '7896584066579',
            'matching_strategy': 'SINGLE_SELLER',
            'review_score': 0,
            'attributes': [{
                'value': '220 Volts',
                'type': 'voltage'
            }],
            'description': 'Lavadora Electrolux, silenciosa e com capacidade de 13Kg, lava mais roupa em menos tempo e espaço, economizando água, energia e produtos de limpeza. O dispencer automático ADDMix, calcula a dosagem de sabão e amaciante, faz a mistura exata, na hora correta. Tem 5 Níveis de água, incluindo nível automático de água que dosa o nível de água da máquina de acordo com a programação e a quantidade de roupa na máquina. E com a exclusiva função Turbo Secagem você aumenta o tempo de centrifugação permitindo que suas roupas saiam mais secas da lavadora do que numa centrifugação normal.\n',  # noqa
            'categories': [{
                'subcategories': [{
                    'id': 'LAVA'
                }],
                'id': 'ED'
            }],
            'main_category': {
                'subcategory': {
                    'id': 'LAVA'
                },
                'id': 'ED'
            }
        }

    @classmethod
    def avalancheshop_sku_768(cls):
        return {
            'seller_id': 'avalancheshop',
            'sku': '768',
            'matching_strategy': 'SINGLE_SELLER',
            'seller_description': 'Avalanche Shop',
            'updated_at': '2017-10-31T10:27:31.094282+00:00',
            'reference': 'Supra',
            'grade': 10,
            'brand': 'Supra',
            'review_score': 0,
            'main_variation': True,
            'description': '<p>   O fone de ouvido supra-auricular Beats EP oferece som da mais alta qualidade. Seu design sem bateria oferece reprodução ilimitada. E sua estrutura elegante e resistente é reforçada com aço inoxidável leve. O Beats EP é ideal para os apaixonados por música em busca de uma experiência dinâmica de áudio.</p>  <p>   <br />   Destaques<br />   A acústica de precisão garante a nitidez e amplitude que você espera da Beats<br />   Design leve e durável, reforçado com aço inoxidável<br />   Sem bateria para reprodução ilimitada<br />   Sistema de deslizamento vertical para ajuste personalizado<br />   Atenda a ligações e controle a música nos seus dispositivos com iOS com o RemoteTalk</p>  <p>   <br />   Características:<br />   Formato: On Ear - No ouvido<br />   Com controle e microfone<br />   Controles de áudio e de chamadas<br />   Controle de volume<br />   Isolamento de ruídos<br />   Conector de áudio de 3,5 mm</p>  <p>   <br />   Conteúdo da Caixa:<br />   Fone de ouvido Beats EP<br />   Estojo dobrável para transporte<br />   Guia de início rápido<br />   Cartão de garantia</p>  <p>   <br />   Dimensões do produto:<br />   Altura: 24.2cm<br />   Largura: 21cm<br />   Profundidade: 11cm<br />   Peso: 0.245kg</p>  <p>   <br />   Garantia do Fornecedor de 12 Meses</p>',  # noqa
            'release_date': '2017-10-31T10:27:31.122801+00:00',
            'created_at': '2017-09-20T20:41:24.160607+00:00',
            'disable_on_matching': False,
            'ean': '0190198212511',
            'review_count': 0,
            'dimensions': {
                'height': 0.21,
                'depth': 0.08,
                'weight': 0.66,
                'width': 0.18
            },
            'sells_to_company': True,
            'title': 'Headphone On Ear Supra Auricular Beats',
            'attributes': [{
                'type': 'voltage',
                'value': 'Bivolt'
            }],
            'sold_count': 0,
            'parent_sku': '561',
            'navigation_id': '7244694',
            'type': 'product',
            'categories': [{
                'subcategories': [{
                    'id': 'FRDF',
                    'description': 'Fone de ouvido headphone'
                }],
                'id': 'EA',
                'description': 'Áudio'
            }],
            'md5': '7c228fa7890d4dba5e71de0af5742e50'
        }

    @classmethod
    def avalancheshop_sku_769(cls):
        return {
            'seller_id': 'avalancheshop',
            'sku': '769',
            'matching_strategy': 'SINGLE_SELLER',
            'seller_description': 'Avalanche Shop',
            'updated_at': '2017-10-31T10:27:40.358174+00:00',
            'reference': 'Supra',
            'grade': 10,
            'brand': 'Supra',
            'review_score': 0,
            'main_variation': False,
            'description': '<p>   O fone de ouvido supra-auricular Beats EP oferece som da mais alta qualidade. Seu design sem bateria oferece reprodução ilimitada. E sua estrutura elegante e resistente é reforçada com aço inoxidável leve. O Beats EP é ideal para os apaixonados por música em busca de uma experiência dinâmica de áudio.</p>  <p>   <br />   Destaques<br />   A acústica de precisão garante a nitidez e amplitude que você espera da Beats<br />   Design leve e durável, reforçado com aço inoxidável<br />   Sem bateria para reprodução ilimitada<br />   Sistema de deslizamento vertical para ajuste personalizado<br />   Atenda a ligações e controle a música nos seus dispositivos com iOS com o RemoteTalk</p>  <p>   <br />   Características:<br />   Formato: On Ear - No ouvido<br />   Com controle e microfone<br />   Controles de áudio e de chamadas<br />   Controle de volume<br />   Isolamento de ruídos<br />   Conector de áudio de 3,5 mm</p>  <p>   <br />   Conteúdo da Caixa:<br />   Fone de ouvido Beats EP<br />   Estojo dobrável para transporte<br />   Guia de início rápido<br />   Cartão de garantia</p>  <p>   <br />   Dimensões do produto:<br />   Altura: 24.2cm<br />   Largura: 21cm<br />   Profundidade: 11cm<br />   Peso: 0.245kg</p>  <p>   <br />   Garantia do Fornecedor de 12 Meses</p>',  # noqa
            'release_date': '2017-10-31T10:27:42.678768+00:00',
            'created_at': '2017-09-20T20:41:24.160607+00:00',
            'disable_on_matching': False,
            'ean': '0190198212498',
            'review_count': 0,
            'dimensions': {
                'height': 0.21,
                'depth': 0.08,
                'weight': 0.66,
                'width': 0.18
            },
            'sells_to_company': True,
            'title': 'Headphone On Ear Supra Auricular Beats',
            'attributes': [{
                'type': 'voltage',
                'value': 'Bivolt'
            }],
            'sold_count': 0,
            'parent_sku': '561',
            'navigation_id': '7086923',
            'type': 'product',
            'categories': [{
                'subcategories': [{
                    'id': 'FRDF',
                    'description': 'Fone de ouvido headphone'
                }],
                'id': 'EA',
                'description': 'Áudio'
            }],
            'md5': '3e062c698559359c2386ec85e200645a'
        }

    @classmethod
    def avalancheshop_sku_770(cls):
        return {
            'seller_id': 'avalancheshop',
            'sku': '770',
            'review_count': 0,
            'reference': 'Supra',
            'disable_on_matching': False,
            'navigation_id': '7235273',
            'brand': 'Supra',
            'attributes': [{
                'value': 'Bivolt',
                'type': 'voltage'
            }],
            'release_date': '2017-10-31T10:27:56.671578+00:00',
            'dimensions': {
                'height': 0.21,
                'width': 0.18,
                'depth': 0.08,
                'weight': 0.66
            },
            'title': 'Headphone On Ear Supra Auricular Beats',
            'description': '<p>   O fone de ouvido supra-auricular Beats EP oferece som da mais alta qualidade. Seu design sem bateria oferece reprodução ilimitada. E sua estrutura elegante e resistente é reforçada com aço inoxidável leve. O Beats EP é ideal para os apaixonados por música em busca de uma experiência dinâmica de áudio.</p>  <p>   <br />   Destaques<br />   A acústica de precisão garante a nitidez e amplitude que você espera da Beats<br />   Design leve e durável, reforçado com aço inoxidável<br />   Sem bateria para reprodução ilimitada<br />   Sistema de deslizamento vertical para ajuste personalizado<br />   Atenda a ligações e controle a música nos seus dispositivos com iOS com o RemoteTalk</p>  <p>   <br />   Características:<br />   Formato: On Ear - No ouvido<br />   Com controle e microfone<br />   Controles de áudio e de chamadas<br />   Controle de volume<br />   Isolamento de ruídos<br />   Conector de áudio de 3,5 mm</p>  <p>   <br />   Conteúdo da Caixa:<br />   Fone de ouvido Beats EP<br />   Estojo dobrável para transporte<br />   Guia de início rápido<br />   Cartão de garantia</p>  <p>   <br />   Dimensões do produto:<br />   Altura: 24.2cm<br />   Largura: 21cm<br />   Profundidade: 11cm<br />   Peso: 0.245kg</p>  <p>   <br />   Garantia do Fornecedor de 12 Meses</p>',  # noqa
            'categories': [{
                'id': 'EA',
                'description': 'Áudio',
                'subcategories': [{
                    'id': 'FRDF',
                    'description': 'Fone de ouvido headphone'
                }]
            }],
            'seller_description': 'Avalanche Shop',
            'sells_to_company': True,
            'matching_strategy': 'SINGLE_SELLER',
            'created_at': '2017-09-20T20:41:24.160607+00:00',
            'review_score': 0,
            'parent_sku': '561',
            'grade': 10,
            'ean': '0190198212504',
            'updated_at': '2017-10-31T10:27:40.358174+00:00',
            'sold_count': 0,
            'type': 'product',
            'main_variation': False,
            'md5': '9a4814ad8922cb2834b35daa3610ba36'
        }

    @classmethod
    def avalancheshop_sku_771(cls):
        return {
            'seller_id': 'avalancheshop',
            'sku': '771',
            'sold_count': 0,
            'updated_at': '2017-09-20T20:41:24.160658+00:00',
            'reference': 'Supra',
            'main_variation': False,
            'grade': 10,
            'matching_strategy': 'SINGLE_SELLER',
            'disable_on_matching': False,
            'sells_to_company': True,
            'parent_sku': '561',
            'navigation_id': '7030066',
            'attributes': [{
                'value': 'Bivolt',
                'type': 'voltage'
            }],
            'title': 'Headphone On Ear Supra Auricular Beats',
            'dimensions': {
                'width': 0.18,
                'depth': 0.08,
                'weight': 0.66,
                'height': 0.21
            },
            'type': 'product',
            'description': '<p>   O fone de ouvido supra-auricular Beats EP oferece som da mais alta qualidade. Seu design sem bateria oferece reprodução ilimitada. E sua estrutura elegante e resistente é reforçada com aço inoxidável leve. O Beats EP é ideal para os apaixonados por música em busca de uma experiência dinâmica de áudio.</p>  <p>   <br />   Destaques<br />   A acústica de precisão garante a nitidez e amplitude que você espera da Beats<br />   Design leve e durável, reforçado com aço inoxidável<br />   Sem bateria para reprodução ilimitada<br />   Sistema de deslizamento vertical para ajuste personalizado<br />   Atenda a ligações e controle a música nos seus dispositivos com iOS com o RemoteTalk</p>  <p>   <br />   Características:<br />   Formato: On Ear - No ouvido<br />   Com controle e microfone<br />   Controles de áudio e de chamadas<br />   Controle de volume<br />   Isolamento de ruídos<br />   Conector de áudio de 3,5 mm</p>  <p>   <br />   Conteúdo da Caixa:<br />   Fone de ouvido Beats EP<br />   Estojo dobrável para transporte<br />   Guia de início rápido<br />   Cartão de garantia</p>  <p>   <br />   Dimensões do produto:<br />   Altura: 24.2cm<br />   Largura: 21cm<br />   Profundidade: 11cm<br />   Peso: 0.245kg</p>  <p>   <br />   Garantia do Fornecedor de 12 Meses</p>',  # noqa
            'categories': [{
                'subcategories': [{
                    'id': 'FRDF',
                    'description': 'Fone de ouvido headphone'
                }],
                'id': 'EA',
                'description': 'Áudio'
            }],
            'brand': 'Supra',
            'ean': '0190198212481',
            'seller_description': 'Avalanche Shop',
            'release_date': '2017-10-31T10:02:50.519366+00:00',
            'created_at': '2017-09-20T20:41:24.160607+00:00',
            'review_score': 0,
            'review_count': 0,
            'md5': '60d6d21a4ff46a157f2d9b8a35d0eca2'
        }

    @classmethod
    def foccusnutricao_sku_4098_6290(cls):
        return {
            'seller_id': 'foccusnutricao',
            'sku': '4098-6290',
            'dimensions': {
                'weight': 1.2,
                'depth': 0.17,
                'height': 0.17,
                'width': 0.27
            },
            'sells_to_company': True,
            'type': 'product',
            'disable_on_matching': False,
            'review_count': 0,
            'attributes': [{
                'type': 'size',
                'value': 'TAM. 39'
            }, {
                'type': 'color',
                'value': 'Prata'
            }],
            'brand': 'Aqurun',
            'reference': '',
            'parent_sku': '4098',
            'sold_count': 0,
            'matching_strategy': 'SINGLE_SELLER',
            'created_at': '2017-12-19T21:48:12.488914+00:00',
            'ean': '8809176681271',
            'updated_at': '2017-12-19T21:48:12.505122+00:00',
            'review_score': 0,
            'release_date': '2018-01-14T22:01:36.451659+00:00',
            'categories': [{
                'subcategories': [{
                    'id': 'SPTL',
                    'description': 'Calçados'
                }],
                'id': 'RE',
                'description': 'Relógios'
            }],
            'description': 'Sapatilha P/ Hidroginástica da Aqurun.<BR>Toda a tecnologia em prol do seu conforto e aderência! Com solado leve e emborrachado, a Sapatilha P/ Hidroginástica - Aqurun é a opção ideal para as atividades aquáticas.',  # noqa
            'grade': 10,
            'navigation_id': '6107667',
            'main_variation': False,
            'title': 'Sapatilha P/ Hidroginástica - Aqurun - Prata',
            'seller_description': 'Foccus Nutrição Esportiva',
            'md5': '5b6da7f79d3d10f629df0aceb8534ae6'
        }

    @classmethod
    def foccusnutricao_sku_4098_6293(cls):
        return {
            'seller_id': 'foccusnutricao',
            'sku': '4098-6293',
            'dimensions': {
                'height': 0.17,
                'width': 0.27,
                'weight': 1.2,
                'depth': 0.17
            },
            'sells_to_company': True,
            'type': 'product',
            'disable_on_matching': False,
            'review_count': 0,
            'attributes': [{
                'type': 'size',
                'value': 'TAM. 42'
            }, {
                'type': 'color',
                'value': 'Prata'
            }],
            'brand': 'Aqurun',
            'reference': 'Aqurun',
            'parent_sku': '4098',
            'sold_count': 0,
            'matching_strategy': 'SINGLE_SELLER',
            'created_at': '2017-12-19T21:48:12.488914+00:00',
            'ean': '8809176681301',
            'updated_at': '2017-12-19T21:48:12.505122+00:00',
            'review_score': 0,
            'release_date': '2017-12-19T21:54:00.932811+00:00',
            'categories': [{
                'description': 'Relógios',
                'subcategories': [{
                    'description': 'Calçados',
                    'id': 'SPTL'
                }],
                'id': 'RE'
            }],
            'description': 'Sapatilha P/ Hidroginástica da Aqurun.<BR>Toda a tecnologia em prol do seu conforto e aderência! Com solado leve e emborrachado, a Sapatilha P/ Hidroginástica - Aqurun é a opção ideal para as atividades aquáticas.',  # noqa
            'grade': 10,
            'navigation_id': '6636300',
            'main_variation': False,
            'title': 'Sapatilha P/ Hidroginástica - Aqurun - Prata',
            'seller_description': 'Foccus Nutrição Esportiva',
            'md5': 'bf9a0efff1f16f812aa35b894d1dd3a3'
        }

    @classmethod
    def foccusnutricao_sku_4098_6295(cls):
        return {
            'seller_id': 'foccusnutricao',
            'sku': '4098-6295',
            'title': 'Sapatilha P/ Hidroginástica - Aqurun - Prata',
            'main_variation': True,
            'disable_on_matching': False,
            'ean': '8809176681240',
            'grade': 10,
            'matching_strategy': 'SINGLE_SELLER',
            'attributes': [{
                'type': 'size',
                'value': 'TAM. 35'
            }, {
                'type': 'color',
                'value': 'Prata'
            }],
            'type': 'product',
            'updated_at': '2017-12-19T21:48:12.505122+00:00',
            'description': 'Sapatilha P/ Hidroginástica da Aqurun.<BR>Toda a tecnologia em prol do seu conforto e aderência! Com solado leve e emborrachado, a Sapatilha P/ Hidroginástica - Aqurun é a opção ideal para as atividades aquáticas.',  # noqa
            'md5': 'da3a88675cdba339220f487586980a7c',
            'navigation_id': '6482822',
            'parent_sku': '4098',
            'review_score': 0,
            'reference': '',
            'categories': [{
                'subcategories': [{
                    'id': 'SPTL',
                    'description': 'Calçados'
                }],
                'id': 'RE',
                'description': 'Relógios'
            }],
            'review_count': 0,
            'release_date': '2018-01-01T17:01:38.503168+00:00',
            'sells_to_company': True,
            'seller_description': 'Foccus Nutrição Esportiva',
            'created_at': '2017-12-19T21:48:12.488914+00:00',
            'dimensions': {
                'weight': 1.2,
                'height': 0.17,
                'depth': 0.17,
                'width': 0.27
            },
            'brand': 'Aqurun',
            'sold_count': 0
        }

    @classmethod
    def foccusnutricao_sku_4098_6297(cls):
        return {
            'seller_id': 'foccusnutricao',
            'sku': '4098-6297',
            'categories': [{
                'id': 'RE',
                'subcategories': [{
                    'id': 'SPTL',
                    'description': 'Calçados'
                }],
                'description': 'Relógios'
            }],
            'description': 'Sapatilha P/ Hidroginástica da Aqurun.<BR>Toda a tecnologia em prol do seu conforto e aderência! Com solado leve e emborrachado, a Sapatilha P/ Hidroginástica - Aqurun é a opção ideal para as atividades aquáticas.',  # noqa
            'sold_count': 0,
            'brand': 'Aqurun',
            'created_at': '2017-12-19T21:48:12.488914+00:00',
            'grade': 10,
            'main_variation': False,
            'attributes': [{
                'type': 'size',
                'value': 'TAM. 32'
            }, {
                'type': 'color',
                'value': 'Prata'
            }],
            'md5': '2281f1a11a292dd3619134cf16a6e637',
            'ean': '8809176681219',
            'review_score': 0,
            'title': 'Sapatilha P/ Hidroginástica - Aqurun - Prata',
            'review_count': 0,
            'dimensions': {
                'width': 0.27,
                'depth': 0.17,
                'weight': 1.2,
                'height': 0.17
            },
            'matching_strategy': 'SINGLE_SELLER',
            'sells_to_company': True,
            'seller_description': 'Foccus Nutrição Esportiva',
            'navigation_id': '6585073',
            'updated_at': '2017-12-19T21:48:12.505122+00:00',
            'type': 'product',
            'parent_sku': '4098',
            'reference': 'Aqurun',
            'release_date': '2017-12-19T21:54:07.432181+00:00',
            'disable_on_matching': False
        }

    @classmethod
    def foccusnutricao_sku_4099_6303(cls):
        return {
            'seller_id': 'foccusnutricao',
            'sku': '4099-6303',
            'type': 'product',
            'dimensions': {
                'width': 0.27,
                'depth': 0.17,
                'height': 0.17,
                'weight': 1.2
            },
            'navigation_id': '6478240',
            'sells_to_company': True,
            'created_at': '2017-12-22T18:02:21.265887+00:00',
            'description': 'Sapatilha P/ Hidroginástica da Aqurun.<BR>Toda a tecnologia em prol do seu conforto e aderência!<BR>Com solado leve e emborrachado, a Sapatilha P/ Hidroginástica - Aqurun é a opção ideal para as atividades aquáticas.',  # noqa
            'reference': '',
            'categories': [{
                'description': 'Esporte e Lazer',
                'subcategories': [{
                    'description': 'Artigos e Acessórios de Natação',
                    'id': 'ELNT'
                }],
                'id': 'ES'
            }],
            'brand': 'Aqurun',
            'sold_count': 0,
            'updated_at': '2017-12-22T18:02:21.284165+00:00',
            'seller_description': 'Foccus Nutrição Esportiva',
            'md5': '18044cb79d44093cc618c20c4336633e',
            'title': 'Sapatilha P/ Hidroginástica - Aqurun - Rosa',
            'review_count': 0,
            'disable_on_matching': False,
            'grade': 10,
            'matching_strategy': 'SINGLE_SELLER',
            'ean': '8809176681141',
            'review_score': 0,
            'attributes': [{
                'type': 'size',
                'value': 'TAM. 34'
            }, {
                'type': 'color',
                'value': 'Rosa'
            }],
            'main_variation': True,
            'release_date': '2018-01-03T23:03:40.050532+00:00',
            'parent_sku': '4099'
        }

    @classmethod
    def foccusnutricao_sku_4100_6306(cls):
        return {
            'seller_id': 'foccusnutricao',
            'sku': '4100-6306',
            'review_count': 0,
            'matching_strategy': 'SINGLE_SELLER',
            'navigation_id': '6649508',
            'seller_description': 'Foccus Nutrição Esportiva',
            'brand': 'Aqurun',
            'created_at': '2017-12-19T21:48:18.774708+00:00',
            'type': 'product',
            'ean': '8809176681400',
            'reference': '',
            'attributes': [{
                'value': 'TAM. 39',
                'type': 'size'
            }, {
                'type': 'color',
                'value': 'Preto'
            }],
            'md5': 'beeb59ec9dd5051fecbcc772b20d2fd6',
            'categories': [{
                'id': 'RE',
                'subcategories': [{
                    'id': 'SPTL',
                    'description': 'Calçados'
                }],
                'description': 'Relógios'
            }],
            'disable_on_matching': False,
            'updated_at': '2017-12-19T21:48:18.786309+00:00',
            'grade': 10,
            'title': 'Sapatilha P/ Hidroginástica - Aqurun - Preto',
            'review_score': 0,
            'parent_sku': '4100',
            'release_date': '2017-12-24T05:00:16.660517+00:00',
            'sells_to_company': True,
            'dimensions': {
                'width': 0.27,
                'height': 0.17,
                'depth': 0.17,
                'weight': 1.2
            },
            'description': 'Sapatilha P/ Hidroginástica da Aqurun.<BR>Toda a tecnologia em prol do seu conforto e aderência! Com solado leve e emborrachado, a Sapatilha P/ Hidroginástica - Aqurun é a opção ideal para as atividades aquáticas.',  # noqa
            'main_variation': True,
            'sold_count': 0
        }

    @classmethod
    def foccusnutricao_sku_4100_6314(cls):
        return {
            'seller_id': 'foccusnutricao',
            'sku': '4100-6314',
            'reference': '',
            'parent_sku': '4100',
            'updated_at': '2017-12-19T21:48:18.786309+00:00',
            'brand': 'Aqurun',
            'md5': '858983c0df504ca7661a1969481265e9',
            'release_date': '2018-01-26T17:22:53.082828+00:00',
            'review_count': 0,
            'main_variation': False,
            'title': 'Sapatilha P/ Hidroginástica - Aqurun - Preto',
            'sells_to_company': True,
            'navigation_id': '6464835',
            'review_score': 0,
            'attributes': [{
                'type': 'size',
                'value': 'TAM. 32'
            }, {
                'type': 'color',
                'value': 'Preto'
            }],
            'dimensions': {
                'width': 0.27,
                'weight': 1.2,
                'height': 0.17,
                'depth': 0.17
            },
            'type': 'product',
            'disable_on_matching': False,
            'matching_strategy': 'SINGLE_SELLER',
            'seller_description': 'Foccus Nutrição Esportiva',
            'created_at': '2017-12-19T21:48:18.774708+00:00',
            'ean': '8809176681349',
            'categories': [{
                'subcategories': [{
                    'id': 'SPTL',
                    'description': 'Calçados'
                }],
                'id': 'RE',
                'description': 'Relógios'
            }],
            'description': 'Sapatilha P/ Hidroginástica da Aqurun.<BR>Toda a tecnologia em prol do seu conforto e aderência! Com solado leve e emborrachado, a Sapatilha P/ Hidroginástica - Aqurun é a opção ideal para as atividades aquáticas.',  # noqa
            'grade': 10,
            'sold_count': 0
        }

    @classmethod
    def foccusnutricao_sku_4101_6319(cls):
        return {
            'seller_id': 'foccusnutricao',
            'sku': '4101-6319',
            'review_count': 0,
            'matching_strategy': 'SINGLE_SELLER',
            'navigation_id': '6276310',
            'seller_description': 'Foccus Nutrição Esportiva',
            'brand': 'Aqurun',
            'created_at': '2017-12-19T21:48:22.923111+00:00',
            'type': 'product',
            'ean': '8809176681080',
            'reference': '',
            'attributes': [{
                'value': 'TAM. 42',
                'type': 'size'
            }, {
                'type': 'color',
                'value': 'Azul'
            }],
            'md5': '917d02ccfdbde7cce070a416714610ae',
            'categories': [{
                'subcategories': [{
                    'description': 'Calçados',
                    'id': 'SPTL'
                }],
                'description': 'Relógios',
                'id': 'RE'
            }],
            'disable_on_matching': False,
            'updated_at': '2017-12-19T21:48:22.938497+00:00',
            'grade': 10,
            'title': 'Sapatilha P/ Hidroginástica - Aqurun - Azul',
            'review_score': 0,
            'parent_sku': '4101',
            'release_date': '2018-01-09T00:21:23.964500+00:00',
            'sells_to_company': True,
            'dimensions': {
                'depth': 0.17,
                'width': 0.27,
                'weight': 1.2,
                'height': 0.17
            },
            'description': 'Sapatilha P/ Hidroginástica da Aqurun.<BR>Toda a tecnologia em prol do seu conforto e aderência! Com solado leve e emborrachado, a Sapatilha P/ Hidroginástica - Aqurun é a opção ideal para as atividades aquáticas.',  # noqa
            'main_variation': False,
            'sold_count': 0
        }

    @classmethod
    def foccusnutricao_sku_4101_6321(cls):
        return {
            'seller_id': 'foccusnutricao',
            'sku': '4101-6321',
            'dimensions': {
                'width': 0.27,
                'depth': 0.17,
                'height': 0.17,
                'weight': 1.2
            },
            'sells_to_company': True,
            'type': 'product',
            'disable_on_matching': False,
            'review_count': 0,
            'attributes': [{
                'type': 'size',
                'value': 'TAM. 35'
            }, {
                'type': 'color',
                'value': 'Azul'
            }],
            'brand': 'Aqurun',
            'reference': '',
            'parent_sku': '4101',
            'sold_count': 0,
            'matching_strategy': 'SINGLE_SELLER',
            'created_at': '2017-12-19T21:48:22.923111+00:00',
            'ean': '8809176681509',
            'updated_at': '2017-12-19T21:48:22.938497+00:00',
            'review_score': 0,
            'release_date': '2018-01-20T14:41:26.351622+00:00',
            'categories': [{
                'subcategories': [{
                    'description': 'Calçados',
                    'id': 'SPTL'
                }],
                'description': 'Relógios',
                'id': 'RE'
            }],
            'description': 'Sapatilha P/ Hidroginástica da Aqurun.<BR>Toda a tecnologia em prol do seu conforto e aderência! Com solado leve e emborrachado, a Sapatilha P/ Hidroginástica - Aqurun é a opção ideal para as atividades aquáticas.',  # noqa
            'grade': 10,
            'navigation_id': '6703463',
            'main_variation': False,
            'title': 'Sapatilha P/ Hidroginástica - Aqurun - Azul',
            'seller_description': 'Foccus Nutrição Esportiva',
            'md5': '7f050c568a4a37d1723b61b920c579bc'
        }

    @classmethod
    def magazineluiza_sku_216218600(cls):
        return {
            'created_at': '2016-04-27T07:18:22.050000',
            'brand': 'golden',
            'sold_count': 0,
            'description': 'A luminária Spot Ultra Led tem cor de luz de 6500K, com potência de 3W e vida útil de 25.000 horas. Indicado para hospital, edifício, lojas, restaurantes, hotéis e shoppings vai garantir uma ótima iluminação para o seu estabelecimento comercial. Leve agora uma luminária com vida longa, alto fluxo luminoso e fecho de luz direcionado. \n\n',  # noqa
            'type': 'product',
            'matching_strategy': 'SINGLE_SELLER',
            'disable_on_matching': False,
            'main_variation': True,
            'reference': 'Golden Ultra LED',
            'attributes': [{
                'value': '1',
                'type': 'quantity'
            }],
            'sells_to_company': True,
            'selections': {
                '12966': ['16734', '16737'],
                '0': ['19108', '21168', '7291']
            },
            'dimensions': {
                'width': 0.06,
                'height': 0.17,
                'depth': 0.21,
                'weight': 0.25
            },
            'navigation_id': '216218600',
            'categories': [{
                'id': 'CJ',
                'subcategories': [{
                    'id': 'LULD'
                }, {
                    'id': 'PILU'
                }]
            }],
            'main_category': {
                'id': 'CJ',
                'subcategory': {
                    'id': 'LULD'
                }
            },
            'sku': '216218600',
            'parent_sku': '2162186',
            'review_score': 0,
            'ean': '7897714351138',
            'title': 'Luminária LED Spot 3W 6500K',
            'grade': 10,
            'seller_id': 'magazineluiza',
            'seller_description': 'Magazine Luiza',
            'updated_at': '2018-02-09T00:15:14.270000',
            'review_count': 0,
            'md5': '201bef18e63efa1f3d182d924f78ac5f'
        }

    @classmethod
    def magazineluiza_sku_216218700(cls):
        return {
            'created_at': '2016-04-27T07:18:22.050000',
            'review_score': 0,
            'sold_count': 0,
            'description': 'A luminária Spot Ultra Led tem cor de luz de 6500K, com potência de 3W e vida útil de 25.000 horas. Indicado para hospital, edifício, lojas, restaurantes, hotéis e shoppings vai garantir uma ótima iluminação para o seu estabelecimento comercial. Leve agora uma luminária com vida longa, alto fluxo luminoso e fecho de luz direcionado. \n\n',  # noqa
            'review_count': 0,
            'type': 'product',
            'matching_strategy': 'SINGLE_SELLER',
            'disable_on_matching': False,
            'main_variation': False,
            'reference': 'Golden Ultra LED',
            'sells_to_company': True,
            'selections': {
                '12966': ['16734', '16737'],
                '0': ['18427', '19108', '19575', '7291']
            },
            'dimensions': {
                'width': 0.06,
                'height': 0.17,
                'depth': 0.21,
                'weight': 0.25
            },
            'navigation_id': '216218700',
            'categories': [{
                'id': 'CJ',
                'subcategories': [{
                    'id': 'LULD'
                }, {
                    'id': 'PILU'
                }]
            }],
            'main_category': {
                'id': 'CJ',
                'subcategory': {
                    'id': 'LULD'
                }
            },
            'sku': '216218700',
            'parent_sku': '2162187',
            'brand': 'golden',
            'ean': '7897714351121',
            'title': 'Luminária LED Spot 3W 6500K',
            'grade': 10,
            'seller_description': 'Magazine Luiza',
            'updated_at': '2018-01-18T15:13:05.307000',
            'seller_id': 'magazineluiza',
            'md5': '348b50a2285f8579284259d692efa24b',
            'attributes': [{
                'value': 'Amarelo',
                'type': 'color'
            }]
        }

    @classmethod
    def magazineluiza_sku_215522200(cls):
        return {
            'type': 'product',
            'main_category': {
                'subcategory': {
                    'id': 'CSOL'
                },
                'id': 'CO'
            },
            'description': 'Colchão de espuma em 100% póliuretano. Confortável, composto por matérias-prima de 1ª qualidade, selado e aferido pelo Inmetro, revestido com tecido com tratamento antiácaros, antifungos e antialergico. Desenvolvido para atender adequadamente pessoas com peso aproximado de 80 kg.\n',  # noqa
            'matching_strategy': 'SINGLE_SELLER',
            'dimensions': {
                'depth': 0.88,
                'width': 1.88,
                'weight': 7.5,
                'height': 0.16
            },
            'sells_to_company': True,
            'review_count': 0,
            'categories': [{
                'id': 'CO',
                'subcategories': [{
                    'id': 'CSOL'
                }, {
                    'id': 'CANL'
                }, {
                    'id': 'COOO'
                }, {
                    'id': 'S80K'
                }, {
                    'id': 'SA13'
                }, {
                    'id': 'SO28'
                }]
            }],
            'main_variation': False,
            'navigation_id': '215522200',
            'seller_description': 'Magazine Luiza',
            'grade': 10,
            'selections': {
                '12966': ['16734', '16737'],
                '0': ['18787', '19576', '20291', '20780', '21875', '22315']
            },
            'sold_count': 0,
            'disable_on_matching': False,
            'ean': '7896988303805',
            'created_at': '2015-12-24T06:48:42.590000',
            'seller_id': 'magazineluiza',
            'sku': '215522200',
            'parent_sku': '2155222',
            'brand': 'ortobom',
            'reference': 'Light',
            'updated_at': '2018-01-07T18:07:57.917000',
            'review_score': 0,
            'title': 'Colchão Solteiro Ortobom Espuma D-28 88x188cm',
            'md5': '85a35afeb9d2c2323e4e317325a5060e',
            'attributes': [{
                'type': 'color',
                'value': 'Estampado'
            }]
        }

    @classmethod
    def magazineluiza_sku_215522700(cls):
        return {
            'type': 'product',
            'main_category': {
                'subcategory': {
                    'id': 'CSOL'
                },
                'id': 'CO'
            },
            'description': 'Colchão de espuma em 100% póliuretano. Confortável, composto por matérias-prima de 1ª qualidade, selado e aferido pelo Inmetro, revestido com tecido com tratamento antiácaros, antifungos e antialergico. Desenvolvido para atender adequadamente pessoas com peso aproximado de 80 kg.\n',  # noqa
            'matching_strategy': 'SINGLE_SELLER',
            'dimensions': {
                'depth': 0.88,
                'width': 1.88,
                'weight': 6.5,
                'height': 0.14
            },
            'sells_to_company': True,
            'review_count': 0,
            'categories': [{
                'id': 'CO',
                'subcategories': [{
                    'id': 'CSOL'
                }, {
                    'id': 'CANL'
                }, {
                    'id': 'COOO'
                }, {
                    'id': 'S80K'
                }, {
                    'id': 'SA13'
                }, {
                    'id': 'SO28'
                }]
            }],
            'main_variation': False,
            'navigation_id': '215522700',
            'seller_description': 'Magazine Luiza',
            'grade': 10,
            'selections': {
                '12966': ['16734', '16737'],
                '0': ['18787', '20780', '21875', '22315', '22720']
            },
            'sold_count': 0,
            'disable_on_matching': False,
            'ean': '7896988303850',
            'created_at': '2015-12-24T06:48:42.590000',
            'seller_id': 'magazineluiza',
            'sku': '215522700',
            'parent_sku': '2155227',
            'brand': 'ortobom',
            'reference': 'Light',
            'updated_at': '2018-02-08T21:24:06.393000',
            'review_score': 0,
            'title': 'Colchão Solteiro Ortobom Espuma D-28 88x188cm',
            'md5': 'ec68134f976279acfa7b76d696a0eb18',
            'attributes': [{
                'type': 'color',
                'value': 'Estampado'
            }]
        }

    @classmethod
    def whirlpool_sku_1225(cls):
        return {
            'attributes': [{
                'type': 'voltage',
                'value': '220 Volts'
            }],
            'disable_on_matching': False,
            'title': 'Lavadora Brastemp 15Kg',
            'updated_at': '2017-12-21T20:13:38.155648+00:00',
            'ean': '7891129234901',
            'matching_strategy': 'SINGLE_SELLER',
            'brand': 'Brastemp',
            'review_score': 0,
            'sku': '1225',
            'seller_description': 'Brastemp',
            'categories': [{
                'subcategories': [{
                    'id': 'LAVA',
                    'description': 'Lavadora de Roupas'
                }],
                'id': 'ED',
                'description': 'Eletrodomésticos'
            }],
            'seller_id': 'whirlpool',
            'parent_sku': '936',
            'description': '<p>Cuidado extra<br>A Lavadora Brastemp Top Load tem capacidade para até 15kg e é perfeita para quem não abre mão de um cuidado extra na hora de lavar as roupas. Ela conta com funções especiais para edredons, roupas brancas e coloridas, além de enxágue antialérgico e 7 programas de lavagem.</p><p>Ciclo Edredom Especial<br>Lava seu edredom com alta performance e cuidado, deixando-o sempre limpo. Com ele é possível lavar edredons de solteiro, casal e até king size com a mesma eficiência.</p><p>Funções e ciclos especiais<br>A Lavadora Top Load conta com 7 ciclos pré-programados para diferentes tipos de roupas para facilitar o seu dia a dia como: Rápido, Roupas Íntimas, Dia a Dia, Branco + Branco, Cores + Vivas, Edredom, Cama e Banho.</p><p>Enxágue Antialérgico<br>Com a função especial Enxágue Antialérgico, a lavadora remove quatro vezes mais sabão que o ciclo normal, deixando as peças livres de resíduos que podem irritar a pele.</p><p>Multidispenser<br>O dispenser da Lavadora Brastemp tem compartimentos para sabão em pó, líquido e amaciante que são distribuídos automaticamente durante as etapas da lavagem.</p>',  # noqa
            'sells_to_company': False,
            'reference': '',
            'navigation_id': '9287621',
            'main_variation': False,
            'release_date': '2018-02-24T01:37:37.943510+00:00',
            'md5': '6d2b57f344f565e4e63b585f401e5574',
            'type': 'product',
            'created_at': '2016-12-06T11:05:55.368207+00:00',
            'grade': 10,
            'sold_count': 0,
            'dimensions': {
                'height': 0.1,
                'width': 0.1,
                'weight': 0.03,
                'depth': 0.1
            },
            'review_count': 0
        }

    @classmethod
    def whirlpool_sku_1224(cls):
        return {
            'attributes': [{
                'type': 'voltage',
                'value': '110 Volts'
            }],
            'disable_on_matching': False,
            'title': 'Lavadora Brastemp 15Kg',
            'updated_at': '2017-12-21T20:13:38.155648+00:00',
            'ean': '7891129234468',
            'matching_strategy': 'SINGLE_SELLER',
            'brand': 'Brastemp',
            'review_score': 0,
            'sku': '1224',
            'seller_description': 'Brastemp',
            'categories': [{
                'id': 'ED',
                'description': 'Eletrodomésticos',
                'subcategories': [{
                    'id': 'LAVA',
                    'description': 'Lavadora de Roupas'
                }]
            }],
            'seller_id': 'whirlpool',
            'parent_sku': '936',
            'description': '<p>Cuidado extra<br>A Lavadora Brastemp Top Load tem capacidade para até 15kg e é perfeita para quem não abre mão de um cuidado extra na hora de lavar as roupas. Ela conta com funções especiais para edredons, roupas brancas e coloridas, além de enxágue antialérgico e 7 programas de lavagem.</p><p>Ciclo Edredom Especial<br>Lava seu edredom com alta performance e cuidado, deixando-o sempre limpo. Com ele é possível lavar edredons de solteiro, casal e até king size com a mesma eficiência.</p><p>Funções e ciclos especiais<br>A Lavadora Top Load conta com 7 ciclos pré-programados para diferentes tipos de roupas para facilitar o seu dia a dia como: Rápido, Roupas Íntimas, Dia a Dia, Branco + Branco, Cores + Vivas, Edredom, Cama e Banho.</p><p>Enxágue Antialérgico<br>Com a função especial Enxágue Antialérgico, a lavadora remove quatro vezes mais sabão que o ciclo normal, deixando as peças livres de resíduos que podem irritar a pele.</p><p>Multidispenser<br>O dispenser da Lavadora Brastemp tem compartimentos para sabão em pó, líquido e amaciante que são distribuídos automaticamente durante as etapas da lavagem.</p>',  # noqa
            'sells_to_company': False,
            'reference': '',
            'navigation_id': '9258118',
            'main_variation': True,
            'release_date': '2018-02-24T01:37:37.853366+00:00',
            'md5': '227c062776c68d078cae6aaa412a6d36',
            'type': 'product',
            'created_at': '2016-12-06T11:05:55.368207+00:00',
            'grade': 10,
            'sold_count': 0,
            'dimensions': {
                'weight': 0.03,
                'width': 0.1,
                'depth': 0.1,
                'height': 0.1
            },
            'review_count': 0
        }

    @classmethod
    def magazineluiza_sku_010554000(cls):
        return {
            'attributes': [{
                'value': '110 Volts',
                'type': 'voltage'
            }],
            'disable_on_matching': False,
            'seller_id': 'magazineluiza',
            'updated_at': '2018-02-24T16:16:34.587000',
            'ean': '7891129234925',
            'matching_strategy': 'AUTO_BUYBOX',
            'brand': 'brastemp',
            'review_score': 5,
            'sku': '010554000',
            'seller_description': 'Magazine Luiza',
            'categories': [{
                'id': 'ED',
                'subcategories': [{
                    'id': 'LAVA'
                }]
            }],
            'title': 'Lavadora de Roupas Brastemp BWS15ABANA',
            'parent_sku': '0105540',
            'description': 'Lavadora Brastemp, com capacidade de 15 kg ela tem ciclos exclusivos como: edredom especial que limpa sem causar danos no edredom, roupas íntimas para peças delicadas e o clico tira odores que lava roupas pouco sujas em menos tempo. Você escolhe a quantidade de enxágue e os níveis de agitação. Seu cesto em inox e o agitador especial evitam maiores danos as suas roupas. \n\n\n\n',  # noqa
            'sells_to_company': True,
            'reference': '15Kg',
            'navigation_id': '010554000',
            'selections': {
                '0': ['17911', '18787', '19843', '20334', '20355', '20448', '20570', '20577', '20679', '20704', '20795', '20998', '21141', '21706', '21773', '21830', '21863', '21868', '21877', '21942', '21954', '21957', '22045', '22276', '22280', '22329', '22337', '22532', '22645', '22651', '22658', '6874', '7039', '8218'],  # noqa
                '12966': ['16734', '16737']
            },
            'main_variation': True,
            'main_category': {
                'id': 'ED',
                'subcategory': {
                    'id': 'LAVA'
                }
            },
            'md5': 'cf8f51136428d6c296d0f97a3f2422f0',
            'type': 'product',
            'created_at': '2015-07-02T06:34:50.563000',
            'grade': 10,
            'sold_count': 10,
            'dimensions': {
                'weight': 47.35,
                'height': 1.09,
                'depth': 0.76,
                'width': 0.71
            },
            'review_count': 1
        }

    @classmethod
    def whirlpool_sku_1226(cls):
        return {
            'attributes': [{
                'value': '110 Volts',
                'type': 'voltage'
            }],
            'disable_on_matching': False,
            'seller_id': 'whirlpool',
            'updated_at': '2017-12-21T20:43:44.870375+00:00',
            'ean': '7891129234925',
            'matching_strategy': 'AUTO_BUYBOX',
            'brand': 'Brastemp',
            'review_score': 0,
            'sku': '1226',
            'seller_description': 'Brastemp',
            'categories': [{
                'description': 'Eletrodomésticos',
                'subcategories': [{
                    'description': 'Lavadora de Roupas',
                    'id': 'LAVA'
                }],
                'id': 'ED'
            }],
            'dimensions': {
                'width': 10,
                'height': 10,
                'weight': 0.035,
                'depth': 10
            },
            'title': 'Lavadora Brastemp 15Kg',
            'parent_sku': '937',
            'description': '<p>Cuidado extra<br>A Lavadora Brastemp Top Load tem capacidade para até 15kg e é perfeita para quem não abre mão de um cuidado extra na hora de lavar as roupas. Ela conta com 7 ciclos de lavagem, incluindo programas especiais para edredons, sujeira pesada e roupas íntimas.</p><p>Ciclo Roupas Íntimas<br>Com este ciclo você poder lavar roupas íntimas e delicadas com cuidado e alta performance.</p><p>Funções e ciclos especiais<br>A Lavadora Top Load conta com 7 ciclos pré-programados para diferentes tipos de roupas para facilitar o seu dia a dia como: Rápido, Roupas Íntimas, Dia a Dia, Tira Odores, Sujeira Pesada, Edredom, Cama e Banho.</p><p>Ciclo Tira Odores<br>Ideal para aquelas peças que não estão muito sujas, mas precisam de um cheirinho de roupa limpa.</p><p>Multidispenser<br>O dispenser da Lavadora Brastemp tem compartimentos para sabão em pó, líquido e amaciante que são distribuídos automaticamente durante as etapas da lavagem.</p>',  # noqa
            'sells_to_company': False,
            'reference': '',
            'sold_count': 0,
            'main_variation': True,
            'release_date': '2018-02-24T18:01:49.498837+00:00',
            'md5': 'f75551a078f5bf05118c986101887704',
            'type': 'product',
            'created_at': '2016-12-05T16:36:55.476268+00:00',
            'navigation_id': '9296177',
            'review_count': 0,
            'grade': 10
        }

    @classmethod
    def magazineluiza_sku_010554100(cls):
        return {
            'attributes': [{
                'value': '220 Volts',
                'type': 'voltage'
            }],
            'disable_on_matching': False,
            'seller_id': 'magazineluiza',
            'updated_at': '2018-02-24T14:11:54.510000',
            'ean': '7891129234956',
            'matching_strategy': 'AUTO_BUYBOX',
            'brand': 'brastemp',
            'review_score': 0,
            'sku': '010554100',
            'seller_description': 'Magazine Luiza',
            'categories': [{
                'id': 'ED',
                'subcategories': [{
                    'id': 'LAVA'
                }]
            }],
            'title': 'Lavadora de Roupas Brastemp BWS15ABBNA',
            'parent_sku': '0105540',
            'description': 'Lavadora Brastemp, com capacidade de 15 kg ela tem ciclos exclusivos como: edredom especial que limpa sem causar danos no edredom, roupas íntimas para peças delicadas e o clico tira odores que lava roupas pouco sujas em menos tempo. Você escolhe a quantidade de enxágue e os níveis de agitação. Seu cesto em inox e o agitador especial evitam maiores danos as suas roupas. \n\n\n\n',  # noqa
            'sells_to_company': True,
            'reference': '15Kg',
            'navigation_id': '010554100',
            'selections': {
                '0': ['17911', '18787', '19843', '20334', '20355', '20448', '20570', '20577', '20679', '20704', '20795', '20998', '21141', '21706', '21773', '21830', '21863', '21868', '21877', '21942', '21954', '21957', '22045', '22276', '22280', '22329', '22337', '22532', '22645', '22651', '22658', '6874', '7039', '8218'],  # noqa
                '12966': ['16734', '16737']
            },
            'main_variation': False,
            'main_category': {
                'id': 'ED',
                'subcategory': {
                    'id': 'LAVA'
                }
            },
            'md5': '1511aa5781f971526ea7bb77a52ebc5f',
            'type': 'product',
            'created_at': '2015-07-02T06:34:50.563000',
            'grade': 10,
            'sold_count': 5,
            'dimensions': {
                'weight': 47.35,
                'height': 1.09,
                'width': 0.71,
                'depth': 0.76
            },
            'review_count': 0
        }

    @classmethod
    def whirlpool_sku_1227(cls):
        return {
            'attributes': [{
                'type': 'voltage',
                'value': '220 Volts'
            }],
            'disable_on_matching': False,
            'title': 'Lavadora Brastemp 15Kg',
            'updated_at': '2017-12-21T20:43:44.870375+00:00',
            'ean': '7891129234956',
            'matching_strategy': 'AUTO_BUYBOX',
            'brand': 'Brastemp',
            'review_score': 0,
            'sku': '1227',
            'seller_description': 'Brastemp',
            'categories': [{
                'description': 'Eletrodomésticos',
                'id': 'ED',
                'subcategories': [{
                    'description': 'Lavadora de Roupas',
                    'id': 'LAVA'
                }]
            }],
            'seller_id': 'whirlpool',
            'parent_sku': '937',
            'description': '<p>Cuidado extra<br>A Lavadora Brastemp Top Load tem capacidade para até 15kg e é perfeita para quem não abre mão de um cuidado extra na hora de lavar as roupas. Ela conta com 7 ciclos de lavagem, incluindo programas especiais para edredons, sujeira pesada e roupas íntimas.</p><p>Ciclo Roupas Íntimas<br>Com este ciclo você poder lavar roupas íntimas e delicadas com cuidado e alta performance.</p><p>Funções e ciclos especiais<br>A Lavadora Top Load conta com 7 ciclos pré-programados para diferentes tipos de roupas para facilitar o seu dia a dia como: Rápido, Roupas Íntimas, Dia a Dia, Tira Odores, Sujeira Pesada, Edredom, Cama e Banho.</p><p>Ciclo Tira Odores<br>Ideal para aquelas peças que não estão muito sujas, mas precisam de um cheirinho de roupa limpa.</p><p>Multidispenser<br>O dispenser da Lavadora Brastemp tem compartimentos para sabão em pó, líquido e amaciante que são distribuídos automaticamente durante as etapas da lavagem.</p>',  # noqa
            'sells_to_company': False,
            'reference': '',
            'navigation_id': '9106668',
            'main_variation': False,
            'release_date': '2018-02-24T19:06:34.145421+00:00',
            'md5': 'cfa29a4d5fe3e0bc3911c33cf1f471a8',
            'type': 'product',
            'created_at': '2016-12-05T16:36:55.476268+00:00',
            'grade': 10,
            'sold_count': 0,
            'dimensions': {
                'width': 10,
                'height': 10,
                'weight': 0.035,
                'depth': 10
            },
            'review_count': 0
        }

    @classmethod
    def magazineluiza_sku_217130800(cls):
        return {
            'attributes': [{
                'value': '110 Volts',
                'type': 'voltage'
            }],
            'disable_on_matching': False,
            'title': 'Liquidificador Philco PH900 12 Velocidades',
            'updated_at': '2018-02-17T10:58:44.870000',
            'ean': '7891356063978',
            'matching_strategy': 'SINGLE_SELLER',
            'brand': 'philco',
            'review_score': 0,
            'sku': '217130800',
            'seller_description': 'Magazine Luiza',
            'categories': [{
                'id': 'EP',
                'subcategories': [{
                    'id': 'LIQU'
                }, {
                    'id': 'ELCO'
                }]
            }],
            'dimensions': {
                'width': 0.33,
                'height': 0.26,
                'weight': 2.1,
                'depth': 0.23
            },
            'seller_id': 'magazineluiza',
            'parent_sku': '2171308',
            'description': 'Com o novo liquidificador PH900 da Philco, você vai ganhar muito mais opções na hora de preparar alguma coisa na cozinha. Suas quatro velocidades te dão um leque de opções que vai de simples sucos a cremes elaborados e muito mais. Sua tampa com orifício possibilita a adição de ingredientes durante o preparo e a função Ice permite que você triture gelo com muita facilidade.\n\nE para deixar sua vida ainda muito mais fácil, ele possui função autolimpante!',  # noqa
            'sells_to_company': True,
            'reference': 'com Filtro 900W',
            'sold_count': 0,
            'selections': {
                '0': ['18426', '19107', '19575', '21468', '22304', '22585', '22674', '7041', '7291'],  # noqa
                '12966': ['16734', '16737']
            },
            'main_variation': True,
            'main_category': {
                'id': 'EP',
                'subcategory': {
                    'id': 'LIQU'
                }
            },
            'md5': 'c8ed40ab0e0a94ecb119e15e4b285e0d',
            'type': 'product',
            'created_at': '2017-01-14T08:00:43.113000',
            'navigation_id': '217130800',
            'review_count': 0,
            'grade': 1010
        }

    @classmethod
    def magazineluiza_sku_218374600(cls):
        return {
            'attributes': [{
                'value': '110 Volts',
                'type': 'voltage'
            }],
            'disable_on_matching': False,
            'title': 'Liquidificador Philco PH900 12 Velocidades',
            'updated_at': '2018-02-26T11:47:14.813000',
            'ean': '7899466422616',
            'matching_strategy': 'SINGLE_SELLER',
            'brand': 'philco',
            'review_score': 0,
            'sku': '218374600',
            'seller_description': 'Magazine Luiza',
            'categories': [{
                'id': 'EP',
                'subcategories': [{
                    'id': 'LIQU'
                }, {
                    'id': 'ELCO'
                }]
            }],
            'seller_id': 'magazineluiza',
            'parent_sku': '2183746',
            'description': 'Esse é o liquidificador pra você. Simples assim. Ele tem 900W de potência, doze velocidades, botão pulsar, e ainda permite que você possa servir à partir dele através da tampa. E pra tudo ficar ainda mais fácil e prático, você ainda pode usar seu modo de auto-limpeza! É ou não é perfeito pra você?',  # noqa
            'sells_to_company': True,
            'reference': 'com Filtro 900W',
            'navigation_id': '218374600',
            'selections': {
                '0': ['17719', '19107', '19108', '21330', '21750', '22189', '22206', '22230', '22242', '22248', '22304', '22330', '22585', '22586', '22674', '22678', '22697', '22718', '22720', '22725', '22734', '22737', '22799', '22804', '7041', '7291'],  # noqa
                '12966': ['16734', '16737']
            },
            'main_variation': True,
            'main_category': {
                'id': 'EP',
                'subcategory': {
                    'id': 'LIQU'
                }
            },
            'md5': '2c45f272cb491d7fc17d18b2f3eb47a0',
            'type': 'product',
            'created_at': '2017-08-30T07:53:03.920000',
            'grade': 1010,
            'sold_count': 814,
            'dimensions': {
                'depth': 0.23,
                'height': 0.26,
                'weight': 2.115,
                'width': 0.33
            },
            'review_count': 0
        }

    @classmethod
    def magazineluiza_sku_217130900(cls):
        return {
            'attributes': [{
                'value': '220 Volts',
                'type': 'voltage'
            }],
            'disable_on_matching': False,
            'title': 'Liquidificador Philco PH900 12 Velocidades',
            'updated_at': '2018-02-25T23:08:44.037000',
            'ean': '7891356063992',
            'matching_strategy': 'SINGLE_SELLER',
            'brand': 'philco',
            'review_score': 0,
            'sku': '217130900',
            'seller_description': 'Magazine Luiza',
            'categories': [{
                'subcategories': [{
                    'id': 'LIQU'
                }, {
                    'id': 'ELCO'
                }],
                'id': 'EP'
            }],
            'dimensions': {
                'width': 0.33,
                'depth': 0.23,
                'weight': 2.1,
                'height': 0.26
            },
            'seller_id': 'magazineluiza',
            'parent_sku': '2171308',
            'description': 'Com o novo liquidificador PH900 da Philco, você vai ganhar muito mais opções na hora de preparar alguma coisa na cozinha. Suas quatro velocidades te dão um leque de opções que vai de simples sucos a cremes elaborados e muito mais. Sua tampa com orifício possibilita a adição de ingredientes durante o preparo e a função Ice permite que você triture gelo com muita facilidade.\n\nE para deixar sua vida ainda muito mais fácil, ele possui função autolimpante!',  # noqa
            'sells_to_company': True,
            'reference': 'com Filtro 900W',
            'sold_count': 4,
            'selections': {
                '0': ['18426', '19107', '19575', '21468', '22304', '22585', '22674', '7041', '7291'],  # noqa
                '12966': ['16734', '16737']
            },
            'main_variation': False,
            'main_category': {
                'subcategory': {
                    'id': 'LIQU'
                },
                'id': 'EP'
            },
            'md5': '965618314162edf7c2713b5b8faa490b',
            'type': 'product',
            'created_at': '2017-01-14T08:00:43.113000',
            'navigation_id': '217130900',
            'review_count': 0,
            'grade': 1010
        }

    @classmethod
    def magazineluiza_sku_218374700(cls):
        return {
            'attributes': [{
                'value': '220 Volts',
                'type': 'voltage'
            }],
            'disable_on_matching': False,
            'title': 'Liquidificador Philco PH900 12 Velocidades',
            'updated_at': '2018-02-26T11:40:26.510000',
            'ean': '7899466422623',
            'matching_strategy': 'SINGLE_SELLER',
            'brand': 'philco',
            'review_score': 0,
            'sku': '218374700',
            'seller_description': 'Magazine Luiza',
            'categories': [{
                'subcategories': [{
                    'id': 'LIQU'
                }, {
                    'id': 'ELCO'
                }],
                'id': 'EP'
            }],
            'dimensions': {
                'weight': 2.115,
                'height': 0.26,
                'depth': 0.23,
                'width': 0.33
            },
            'seller_id': 'magazineluiza',
            'parent_sku': '2183746',
            'description': 'Esse é o liquidificador pra você. Simples assim. Ele tem 900W de potência, doze velocidades, botão pulsar, e ainda permite que você possa servir à partir dele através da tampa. E pra tudo ficar ainda mais fácil e prático, você ainda pode usar seu modo de auto-limpeza! É ou não é perfeito pra você?',  # noqa
            'sells_to_company': True,
            'reference': 'com Filtro 900W',
            'sold_count': 422,
            'selections': {
                '0': ['17719', '19107', '19108', '21330', '21750', '22189', '22206', '22230', '22242', '22248', '22304', '22330', '22585', '22586', '22674', '22678', '22697', '22718', '22720', '22725', '22734', '22737', '22799', '22804', '7041', '7291'],  # noqa
                '12966': ['16734', '16737']
            },
            'main_variation': False,
            'main_category': {
                'id': 'EP',
                'subcategory': {
                    'id': 'LIQU'
                }
            },
            'md5': '23f61b40de7cc8c8db91a41329706572',
            'type': 'product',
            'created_at': '2017-08-30T07:53:03.920000',
            'navigation_id': '218374700',
            'review_count': 0,
            'grade': 1010
        }

    @classmethod
    def bigtires_sku_2027(cls):
        return {
            'parent_sku': '2027',
            'type': 'product',
            'sold_count': 0,
            'sells_to_company': True,
            'created_at': '2017-11-12T06:03:10.400770+00:00',
            'brand': 'PIRELLI',
            'release_date': '2018-02-28T18:32:56.137442+00:00',
            'ean': '8019227220315',
            'updated_at': '2018-02-28T13:39:16.985295+00:00',
            'dimensions': {
                'height': 0.65,
                'depth': 0.65,
                'width': 0.21,
                'weight': 9.76
            },
            'categories': [{
                'subcategories': [{
                    'id': 'OMDP',
                    'description': 'Pneus de outras marcas'
                }],
                'id': 'AU',
                'description': 'Automotivo'
            }],
            'md5': 'c1d08ad842ab6de19177502fcbaae4ba',
            'grade': 10,
            'disable_on_matching': False,
            'seller_id': 'bigtires',
            'matching_strategy': 'SINGLE_SELLER',
            'title': 'Pneu passeio 205/60r16 92h scorpion atr pirelli',
            'review_score': 0,
            'sku': '2027',
            'review_count': 0,
            'seller_description': 'Big Tires',
            'navigation_id': '6770582',
            'attributes': [],
            'reference': '',
            'main_variation': True,
            'description': 'Um pneu de uso misto, para todos os tipos de superficies: versátil em todas as situações com excelente capacidade fora estrada. Off road, ele é robusto e confiável. On road, ele proporciona conforto, excelente tração e resistência ao desgaste.'  # noqa
        }

    @classmethod
    def bigtires_sku_20274(cls):
        return {
            'ean': '8019227220315',
            'seller_description': 'Big Tires',
            'updated_at': '2018-03-02T13:24:57.559927+00:00',
            'sku': '20274',
            'grade': 10,
            'attributes': [],
            'review_score': 0,
            'matching_strategy': 'SINGLE_SELLER',
            'created_at': '2017-11-15T05:28:01.579730+00:00',
            'disable_on_matching': False,
            'md5': 'd8ecf1e7bc8bfd0a6232632f540e1431',
            'title': 'Kit pneu aro 16 pirelli 205/60r16 92h scorpion atr 4 unidades',  # noqa
            'release_date': '2018-03-02T13:25:01.029400+00:00',
            'parent_sku': '20274',
            'sold_count': 0,
            'description': 'Um pneu de uso misto, para todos os tipos de superfÃ­cies: versÃ¡til em todas as situaÃ§Ãµes com excelente capacidade fora estrada. Off road, ele Ã© robusto e confiÃ¡vel. On road, ele proporciona conforto, excelente traÃ§Ã£o e resistÃªncia ao desgaste.',  # noqa
            'reference': '',
            'brand': 'PIRELLI',
            'navigation_id': '6682425',
            'type': 'product',
            'review_count': 0,
            'dimensions': {
                'depth': 0.65,
                'width': 0.82,
                'weight': 39.04,
                'height': 0.65
            },
            'main_variation': True,
            'seller_id': 'bigtires',
            'categories': [{
                'subcategories': [{
                    'id': 'OMDP',
                    'description': 'Pneus de outras marcas'
                }],
                'id': 'AU',
                'description': 'Automotivo'
            }],
            'sells_to_company': True
        }

    @classmethod
    def magazineluiza_sku_218849100(cls):
        return {
            'main_category': {
                'subcategory': {
                    'id': 'GJPS'
                },
                'id': 'GA'
            },
            'sells_to_company': True,
            'review_score': 0,
            'matching_strategy': 'SINGLE_SELLER',
            'attributes': [{
                'type': 'console',
                'value': 'PS4'
            }],
            'main_variation': True,
            'seller_description': 'Magazine Luiza',
            'sku': '218849100',
            'title': 'Burnout Paradise Remastered para PS4',
            'review_count': 0,
            'ean': '7892110217446',
            'selections': {
                '0': ['19108', '22780'],
                '12966': ['16734', '16737']
            },
            'description': 'Com Burnout Paradise Remastered para PS4 você vai acelerar na cidade, desde as avenidas caóticas até estradas distantes nas montanhas. Reviva as manobras de alta octanagem e a destruição desenfreada de um dos maiores jogos de pilotagem da EA no estilo arcade!\n\nO jogo oferece o playground definitivo de veículos para que você e seus amigos possam jogar online. Esta remasterização inclui todo o DLC do Year of Paradise, incluindo a atualização Big Surf Island, cuidadosamente recriado e pronto para destruir no Playstation 4.\n\nExplore Paradise City com seus amigos\nQueime o asfalto e estilhace carrocerias nas ruas e estradas abertas de Paradise City, descobrindo saltos, manobras e atalhos. Abra seu caminho para a glória com eventos únicos, usando o seu conhecimento da cidade para encontrar as rotas mais rápidas e sair na frente dos seus rivais. Destrua seus amigos online e colete as fotos de identificação deles, ou junte suas forças para demolir centenas de desafios online.\n\nQuebre todas as regras e cause acidentes em qualquer lugar a qualquer momento \nJogue fora o manual do motorista e bata recordes de velocidade e destruição por toda a cidade. Acompanhe suas realizações e prove sua superioridade em demolição sobre seus amigos. Faça seu carro levantar voo, girar e tirar fina por toda a cidade, passando por cima do tráfego e deixando um rastro caro de destruição no retrovisor.',  # noqa
            'categories': [{
                'subcategories': [{
                    'id': 'GJPS'
                }, {
                    'id': 'GAP4'
                }, {
                    'id': 'GCEV'
                }],
                'id': 'GA'
            }],
            'seller_id': 'magazineluiza',
            'dimensions': {
                'weight': 0.187,
                'depth': 0.01,
                'height': 0.17,
                'width': 0.13
            },
            'md5': '55e0a846fc4a95911f2676b04ab5bb42',
            'sold_count': 0,
            'reference': 'EA',
            'brand': 'ea',
            'created_at': '2018-02-27T08:12:17.033000',
            'grade': 1010,
            'updated_at': '2018-03-01T10:03:34.927000',
            'type': 'product',
            'navigation_id': '218849100',
            'parent_sku': '2188491',
            'disable_on_matching': False
        }

    @classmethod
    def magazineluiza_sku_218849200(cls):
        return {
            'brand': 'ea',
            'sold_count': 0,
            'parent_sku': '2188492',
            'seller_id': 'magazineluiza',
            'navigation_id': '218849200',
            'ean': '7892110217453',
            'review_count': 0,
            'matching_strategy': 'SINGLE_SELLER',
            'main_category': {
                'subcategory': {
                    'id': 'GJXO'
                },
                'id': 'GA'
            },
            'md5': '3943d08ec329e9fdd782e2b6fbc16081',
            'description': 'Com Burnout Paradise Remastered para XBox One você vai acelerar na cidade, desde as avenidas caóticas até estradas distantes nas montanhas. Reviva as manobras de alta octanagem e a destruição desenfreada de um dos maiores jogos de pilotagem da EA no estilo arcade!\n\nO jogo oferece o playground definitivo de veículos para que você e seus amigos possam jogar online. Esta remasterização inclui todo o DLC do Year of Paradise, incluindo a atualização Big Surf Island, cuidadosamente recriado e pronto para destruir no Xbox One.\n\nExplore Paradise City com seus amigos\nQueime o asfalto e estilhace carrocerias nas ruas e estradas abertas de Paradise City, descobrindo saltos, manobras e atalhos. Abra seu caminho para a glória com eventos únicos, usando o seu conhecimento da cidade para encontrar as rotas mais rápidas e sair na frente dos seus rivais. Destrua seus amigos online e colete as fotos de identificação deles, ou junte suas forças para demolir centenas de desafios online.\n\nQuebre todas as regras e cause acidentes em qualquer lugar a qualquer momento \nJogue fora o manual do motorista e bata recordes de velocidade e destruição por toda a cidade. Acompanhe suas realizações e prove sua superioridade em demolição sobre seus amigos. Faça seu carro levantar voo, girar e tirar fina por toda a cidade, passando por cima do tráfego e deixando um rastro caro de destruição no retrovisor.',  # noqa
            'review_score': 0,
            'title': 'Burnout Paradise Remastered para Xbox One',
            'grade': 1010,
            'dimensions': {
                'width': 0.13,
                'depth': 0.01,
                'weight': 0.136,
                'height': 0.17
            },
            'selections': {
                '0': ['19108', '22780'],
                '12966': ['16734', '16737']
            },
            'main_variation': True,
            'sells_to_company': True,
            'type': 'product',
            'categories': [{
                'subcategories': [{
                    'id': 'GJXO'
                }, {
                    'id': 'GAXO'
                }, {
                    'id': 'GCEV'
                }],
                'id': 'GA'
            }],
            'sku': '218849200',
            'disable_on_matching': False,
            'updated_at': '2018-03-01T10:10:25.343000',
            'attributes': [{
                'value': 'Xbox One',
                'type': 'console'
            }],
            'seller_description': 'Magazine Luiza',
            'created_at': '2018-02-27T08:12:17.033000',
            'reference': 'EA'
        }

    @classmethod
    def magazineluiza_sku_218200700(cls):
        return {
            'sku': '218200700',
            'disable_on_matching': False,
            'categories': [{
                'subcategories': [{
                    'id': 'MALA'
                }],
                'id': 'ES'
            }],
            'review_score': 0,
            'selections': {
                '0': ['22040', '22780', '7291', '7638'],
                '12966': ['16734', '16737']
            },
            'attributes': [{
                'value': 'P',
                'type': 'size'
            }],
            'brand': 'american tourister',
            'updated_at': '2018-01-23T11:00:08.610000',
            'title': 'Mala de Viagem American Tourister Pequena',
            'grade': 1010,
            'seller_description': 'Magazine Luiza',
            'created_at': '2017-06-29T08:22:19.453000',
            'description': 'A supermoderna linha Summer Wave vai garantir muito mais estilo para suas viagens, graças ao desenho único com linhas onduladas e elegantes. Summer Wave é uma opção excelente de bagagem para quem busca mais liberdade para viajar para qualquer destino.',  # noqa
            'dimensions': {
                'height': 0.56,
                'depth': 0.23,
                'weight': 3.36,
                'width': 0.42
            },
            'sold_count': 0,
            'main_category': {
                'id': 'ES',
                'subcategory': {
                    'id': 'MALA'
                }
            },
            'parent_sku': '2182007',
            'matching_strategy': 'SINGLE_SELLER',
            'main_variation': True,
            'type': 'product',
            'ean': '7501068856170',
            'navigation_id': '218200700',
            'sells_to_company': True,
            'md5': '85cefcbfc803187c4bf83413a02b70c3',
            'reference': 'Expansiva Summer Wave Spinner Grafite',
            'seller_id': 'magazineluiza',
            'review_count': 0
        }

    @classmethod
    def magazineluiza_sku_218200800(cls):
        return {
            'sku': '218200800',
            'disable_on_matching': False,
            'categories': [{
                'subcategories': [{
                    'id': 'MALA'
                }],
                'id': 'ES'
            }],
            'review_score': 0,
            'selections': {
                '0': ['22040', '22780', '7291', '7638'],
                '12966': ['16734', '16737']
            },
            'attributes': [{
                'value': 'M',
                'type': 'size'
            }],
            'brand': 'american tourister',
            'updated_at': '2018-03-01T03:48:34.730000',
            'title': 'Mala de Viagem American Tourister Média',
            'grade': 1010,
            'seller_description': 'Magazine Luiza',
            'created_at': '2017-06-29T08:22:19.453000',
            'description': 'A supermoderna linha Summer Wave vai garantir muito mais estilo para suas viagens, graças ao desenho único com linhas onduladas e elegantes. Summer Wave é uma opção excelente de bagagem para quem busca mais liberdade para viajar para qualquer destino.',  # noqa
            'dimensions': {
                'height': 0.68,
                'depth': 0.31,
                'weight': 4.32,
                'width': 0.49
            },
            'sold_count': 0,
            'main_category': {
                'id': 'ES',
                'subcategory': {
                    'id': 'MALA'
                }
            },
            'parent_sku': '2182008',
            'matching_strategy': 'SINGLE_SELLER',
            'main_variation': True,
            'type': 'product',
            'ean': '7501068856187',
            'navigation_id': '218200800',
            'sells_to_company': True,
            'md5': '99615ae78089c4059e1c36192398092f',
            'reference': 'Expansiva Summer Wave Spinner Grafite',
            'seller_id': 'magazineluiza',
            'review_count': 0
        }

    @classmethod
    def magazineluiza_sku_218200900(cls):
        return {
            'reference': 'Expansiva Summer Wave Spinner Grafite',
            'type': 'product',
            'sku': '218200900',
            'sold_count': 0,
            'parent_sku': '2182009',
            'md5': 'bf850124984d6812dd8fc793fae0a7cc',
            'updated_at': '2018-01-14T16:54:35.100000',
            'seller_description': 'Magazine Luiza',
            'matching_strategy': 'SINGLE_SELLER',
            'description': 'A supermoderna linha Summer Wave vai garantir muito mais estilo para suas viagens, graças ao desenho único com linhas onduladas e elegantes. Summer Wave é uma opção excelente de bagagem para quem busca mais liberdade para viajar para qualquer destino.',  # noqa
            'navigation_id': '218200900',
            'title': 'Mala de Viagem American Tourister Grande',
            'disable_on_matching': False,
            'ean': '7501068856194',
            'main_variation': True,
            'seller_id': 'magazineluiza',
            'attributes': [{
                'type': 'size',
                'value': 'G'
            }],
            'review_count': 0,
            'brand': 'american tourister',
            'dimensions': {
                'width': 0.53,
                'depth': 0.34,
                'height': 0.78,
                'weight': 5.22
            },
            'review_score': 0,
            'grade': 1010,
            'created_at': '2017-06-29T08:22:19.453000',
            'selections': {
                '0': ['22040', '22780', '7291', '7638'],
                '12966': ['16734', '16737']
            },
            'categories': [{
                'id': 'ES',
                'subcategories': [{
                    'id': 'MALA'
                }]
            }],
            'sells_to_company': True,
            'main_category': {
                'id': 'ES',
                'subcategory': {
                    'id': 'MALA'
                }
            }
        }

    @classmethod
    def magazineluiza_sku_216868300(cls):
        return {
            'parent_sku': '2168683',
            'navigation_id': '216868300',
            'main_variation': True,
            'md5': 'e31b098d3e81c48cdcbc2b55254a7137',
            'brand': 'toshiba',
            'title': 'Pen Drive 8GB Toshiba Hayabusa',
            'ean': '4547808806220',
            'description': 'O Pen Drive Toshiba TransMemory® USB 2.0 oferece uma maneira conveniente de armazenar e transportar suas fotos, vídeos, músicas e arquivos importantes.  \nO Pen Drive Toshiba TransMemory® USB 2.0 ajuda e torna mais fácil transferir o seu conteúdo digital entre vários dispositivos com segurança de forma intuitiva pode compartilhá-lo com sua família e amigos rapidamente. O Pen Drive Toshiba TransMemory ® é otimizado para dispositivos com porta USB 2.0 ou maior para transferência de dados de alta velocidade. Um software de proteção com senha pode ser baixado no site da Toshiba gratuitamente para manter seus dados protegidos a todo momento e além disso O Pen Drive Toshiba TransMemory® USB 2.0 e Plug & Play, sendo reconhecido pela porta receptora do seu equipamento.\nO Pen Drive Toshiba TransMemory® USB 2.0 é compatível com os sistemas operacionais Windows e Mac.\n',  # noqa
            'dimensions': {
                'depth': 0.36,
                'weight': 0.08,
                'height': 0.11,
                'width': 0.17
            },
            'attributes': [{
                'value': '8GB',
                'type': 'capacity'
            }],
            'categories': [{
                'id': 'IA',
                'subcategories': [{
                    'id': 'IAPD'
                }, {
                    'id': 'IAP8'
                }]
            }],
            'review_score': 0,
            'seller_id': 'magazineluiza',
            'main_category': {
                'id': 'IA',
                'subcategory': {
                    'id': 'IAPD'
                }
            },
            'sold_count': 49,
            'disable_on_matching': False,
            'reference': 'USB 2.0',
            'selections': {
                '0': ['18787', '20364', '20486', '20489', '20559', '20589', '20590', '20591', '20592', '20601', '21198', '21570', '21652', '21671', '21685', '21731', '21767', '21773', '21838', '21864', '21892', '21913', '21942', '22358', '22366', '22412', '22493', '22780'],  # noqa
                '12966': ['16734', '16737']
            },
            'matching_strategy': 'SINGLE_SELLER',
            'created_at': '2016-10-20T07:15:04.033000',
            'grade': 10,
            'updated_at': '2018-03-02T15:30:35.567000',
            'seller_description': 'Magazine Luiza',
            'review_count': 0,
            'sku': '216868300',
            'type': 'product',
            'sells_to_company': True
        }

    @classmethod
    def magazineluiza_sku_216868400(cls):
        return {
            'description': 'O Pen Drive Toshiba TransMemory® USB 2.0 oferece uma maneira conveniente de armazenar e transportar suas fotos, vídeos, músicas e arquivos importantes.  \nO Pen Drive Toshiba TransMemory® USB 2.0 ajuda e torna mais fácil transferir o seu conteúdo digital entre vários dispositivos com segurança de forma intuitiva pode compartilhá-lo com sua família e amigos rapidamente. O Pen Drive Toshiba TransMemory ® é otimizado para dispositivos com porta USB 2.0 ou maior para transferência de dados de alta velocidade. Um software de proteção com senha pode ser baixado no site da Toshiba gratuitamente para manter seus dados protegidos a todo momento e além disso O Pen Drive Toshiba TransMemory® USB 2.0 e Plug & Play, sendo reconhecido pela porta receptora do seu equipamento.\nO Pen Drive Toshiba TransMemory® USB 2.0 é compatível com os sistemas operacionais Windows e Mac.\n',  # noqa
            'review_count': 0,
            'md5': 'd56f4242a0435bba683dca9b114cd8ef',
            'review_score': 0,
            'selections': {
                '12966': ['16734', '16737'],
                '0': ['18787', '20559', '21570', '21652', '21671', '21685', '21731', '21767', '21773', '21838', '21864', '21892', '21913', '22009', '22302', '22358', '22366', '22412', '22493', '22780']  # noqa
            },
            'ean': '4547808806237',
            'title': 'Pen Drive 16GB Toshiba Hayabusa',
            'parent_sku': '2168684',
            'dimensions': {
                'depth': 0.17,
                'height': 0.07,
                'width': 0.11,
                'weight': 0.08
            },
            'updated_at': '2018-03-02T14:29:24.430000',
            'seller_description': 'Magazine Luiza',
            'disable_on_matching': False,
            'main_variation': True,
            'categories': [{
                'subcategories': [{
                    'id': 'IAPD'
                }, {
                    'id': 'IAP6'
                }],
                'id': 'IA'
            }],
            'main_category': {
                'subcategory': {
                    'id': 'IAPD'
                },
                'id': 'IA'
            },
            'sold_count': 35,
            'seller_id': 'magazineluiza',
            'type': 'product',
            'matching_strategy': 'SINGLE_SELLER',
            'created_at': '2016-10-20T07:15:04.033000',
            'navigation_id': '216868400',
            'sku': '216868400',
            'attributes': [{
                'type': 'capacity',
                'value': '16GB'
            }],
            'reference': 'USB 2.0',
            'brand': 'toshiba',
            'grade': 10,
            'sells_to_company': True
        }

    @classmethod
    def magazineluiza_sku_216868500(cls):
        return {
            'description': 'O Pen Drive Toshiba TransMemory® USB 2.0 oferece uma maneira conveniente de armazenar e transportar suas fotos, vídeos, músicas e arquivos importantes.  \nO Pen Drive Toshiba TransMemory® USB 2.0 ajuda e torna mais fácil transferir o seu conteúdo digital entre vários dispositivos com segurança de forma intuitiva pode compartilhá-lo com sua família e amigos rapidamente. O Pen Drive Toshiba TransMemory ® é otimizado para dispositivos com porta USB 2.0 ou maior para transferência de dados de alta velocidade. Um software de proteção com senha pode ser baixado no site da Toshiba gratuitamente para manter seus dados protegidos a todo momento e além disso O Pen Drive Toshiba TransMemory® USB 2.0 e Plug & Play, sendo reconhecido pela porta receptora do seu equipamento.\nO Pen Drive Toshiba TransMemory® USB 2.0 é compatível com os sistemas operacionais Windows e Mac.\n',  # noqa
            'sold_count': 10,
            'title': 'Pen Drive 32GB Toshiba Hayabusa',
            'review_count': 0,
            'main_category': {
                'id': 'IA',
                'subcategory': {
                    'id': 'IAPD'
                }
            },
            'ean': '4547808806244',
            'reference': 'USB 2.0',
            'type': 'product',
            'selections': {
                '12966': ['16734', '16737'],
                '0': ['18787', '20357', '20364', '20486', '20489', '20559', '21570', '21652', '21671', '21685', '21731', '21767', '21773', '21838', '21864', '22020', '22358', '22366', '22412', '22493', '22517', '22527', '22537', '22780']  # noqa
            },
            'brand': 'toshiba',
            'attributes': [{
                'type': 'capacity',
                'value': '32GB'
            }],
            'updated_at': '2018-03-01T16:25:25.407000',
            'created_at': '2016-10-20T07:15:04.033000',
            'review_score': 0,
            'md5': 'b1331a6f08412cf985121cd85dcb4beb',
            'grade': 10,
            'navigation_id': '216868500',
            'seller_id': 'magazineluiza',
            'sells_to_company': True,
            'categories': [{
                'subcategories': [{
                    'id': 'IAPD'
                }, {
                    'id': 'IAP3'
                }],
                'id': 'IA'
            }],
            'parent_sku': '2168685',
            'disable_on_matching': False,
            'matching_strategy': 'SINGLE_SELLER',
            'seller_description': 'Magazine Luiza',
            'dimensions': {
                'height': 0.07,
                'weight': 0.08,
                'depth': 0.17,
                'width': 0.11
            },
            'sku': '216868500',
            'main_variation': True
        }

    @classmethod
    def magazineluiza_sku_217110800(cls):
        return {
            'main_category': {
                'subcategory': {
                    'id': 'CSBL'
                },
                'id': 'EA'
            },
            'grade': 1010,
            'review_score': 0,
            'type': 'product',
            'ean': '6925281914188',
            'sells_to_company': True,
            'disable_on_matching': False,
            'main_variation': True,
            'brand': 'jbl',
            'attributes': [{
                'type': 'color',
                'value': 'Preto'
            }],
            'created_at': '2016-12-01T07:45:36.163000',
            'navigation_id': '217110800',
            'selections': {
                '12966': ['16734', '16737'],
                '0': ['18033', '18787', '18789', '21370', '21574', '21613', '21615', '21618', '21622', '21645', '21646', '21647', '21667', '21675', '21676', '21696', '21733', '21838', '21860', '21925', '22002', '22045', '22132', '22146', '22149', '22150', '22152', '22182', '22283', '22284', '22302', '22338', '22659', '22661', '22730', '22768', '22780', '22794', '22826', '22830', '22854', '22881', '22884', '22885']  # noqa
            },
            'sold_count': 30,
            'parent_sku': '2171108',
            'seller_description': 'Magazine Luiza',
            'description': 'O Charge 3 JBL é um speaker sem fio e carregador de baterias ao mesmo tempo, podendo ser usado como uma poderosa caixa acústica, com a qualidade de áudio JBL, ou como uma bateria portátil.\nA Prova D’agua - Classificação IPX 7 : (Submergir em água até 1 metro de profundidade, por Até 30 minutos). Com dois transdutores de 50mm e 2 X 10 W de potência, Tecnologia de reforço de Graves com duplo radiador passivo, função Viva Voz, bateria de 6.000mAh com duração de até 20 horas e função Social Mode, para pareamento de até 3 dispositivos simultaneamente. \n',  # noqa
            'md5': '7da5ad754b051406e82309a6faeb2566',
            'title': 'Caixa de Som Bluetooth Portatil JBL Charge 3 ',
            'seller_id': 'magazineluiza',
            'sku': '217110800',
            'updated_at': '2018-03-06T06:10:59.590000',
            'categories': [{
                'id': 'EA',
                'subcategories': [{
                    'id': 'CSBL'
                }, {
                    'id': 'AUCX'
                }]
            }],
            'review_count': 0,
            'dimensions': {
                'height': 0.18,
                'width': 0.12,
                'depth': 0.26,
                'weight': 1.55
            },
            'matching_strategy': 'SINGLE_SELLER',
            'reference': '20W USB à Prova de Água'
        }

    @classmethod
    def magazineluiza_sku_217110900(cls):
        return {
            'sells_to_company': True,
            'seller_id': 'magazineluiza',
            'sold_count': 5,
            'grade': 10,
            'ean': '6925281914201',
            'updated_at': '2018-03-06T07:30:45.570000',
            'description': 'O Charge 3 JBL é um speaker sem fio e carregador de baterias ao mesmo tempo, podendo ser usado como uma poderosa caixa acústica, com a qualidade de áudio JBL, ou como uma bateria portátil.\nA Prova D’agua - Classificação IPX 7 : (Submergir em água até 1 metro de profundidade, por Até 30 minutos). Com dois transdutores de 50mm e 2 X 10 W de potência, Tecnologia de reforço de Graves com duplo radiador passivo, função Viva Voz, bateria de 6.000mAh com duração de até 20 horas e função Social Mode, para pareamento de até 3 dispositivos simultaneamente. \n',  # noqa
            'title': 'Caixa de Som Bluetooth Portatil JBL Charge 3 ',
            'dimensions': {
                'height': 0.18,
                'width': 0.12,
                'weight': 1.55,
                'depth': 0.26
            },
            'categories': [{
                'id': 'EA',
                'subcategories': [{
                    'id': 'CSBL'
                }, {
                    'id': 'AUCX'
                }]
            }],
            'main_category': {
                'subcategory': {
                    'id': 'CSBL'
                },
                'id': 'EA'
            },
            'sku': '217110900',
            'md5': 'fa2484d7d8c559fbb384c3f19f5dfc56',
            'attributes': [{
                'type': 'color',
                'value': 'Vermelho'
            }],
            'disable_on_matching': False,
            'navigation_id': '217110900',
            'type': 'product',
            'brand': 'jbl',
            'main_variation': True,
            'review_score': 0,
            'review_count': 0,
            'selections': {
                '0': ['18033', '18787', '18789', '20488', '20509', '20551', '21574', '21613', '21615', '21733', '21925', '22002', '22045', '22121', '22132', '22146', '22149', '22150', '22152', '22190', '22191', '22347', '22352', '22363', '22659', '22728', '22780', '22826', '22830', '22881'],  # noqa
                '12966': ['16734', '16737']
            },
            'matching_strategy': 'SINGLE_SELLER',
            'reference': '20W USB à Prova de Água',
            'seller_description': 'Magazine Luiza',
            'created_at': '2016-12-01T07:45:36.163000',
            'parent_sku': '2171109'
        }

    @classmethod
    def magazineluiza_sku_217111000(cls):
        return {
            'title': 'Caixa de Som Bluetooth Portatil JBL Charge 3',
            'navigation_id': '217111000',
            'disable_on_matching': False,
            'review_score': 0,
            'parent_sku': '2171110',
            'description': 'O Charge 3 JBL é um speaker sem fio e carregador de baterias ao mesmo tempo, podendo ser usado como uma poderosa caixa acústica, com a qualidade de áudio JBL, ou como uma bateria portátil.\nA Prova D’agua - Classificação IPX 7 : (Submergir em água até 1 metro de profundidade, por Até 30 minutos). Com dois transdutores de 50mm e 2 X 10 W de potência, Tecnologia de reforço de Graves com duplo radiador passivo, função Viva Voz, bateria de 6.000mAh com duração de até 20 horas e função Social Mode, para pareamento de até 3 dispositivos simultaneamente. \n',  # noqa
            'attributes': [{
                'value': 'Azul',
                'type': 'color'
            }],
            'categories': [{
                'subcategories': [{
                    'id': 'CSBL'
                }, {
                    'id': 'AUCX'
                }],
                'id': 'EA'
            }],
            'sells_to_company': True,
            'sku': '217111000',
            'created_at': '2016-12-01T07:45:36.163000',
            'reference': '20W USB à Prova de Água',
            'selections': {
                '0': ['18033', '18787', '18789', '20678', '20682', '20703', '20761', '21350', '21351', '21390', '21391', '21574', '21613', '21615', '21618', '21622', '21645', '21646', '21667', '21676', '21696', '21733', '21735', '21755', '21838', '21855', '21860', '21925', '22002', '22011', '22045', '22132', '22146', '22149', '22150', '22152', '22338', '22347', '22659', '22731', '22780', '22826', '22830', '22832', '22854', '22881', '22884', '22885'],  # noqa
                '12966': ['16734', '16737']
            },
            'brand': 'jbl',
            'main_variation': True,
            'sold_count': 15,
            'main_category': {
                'subcategory': {
                    'id': 'CSBL'
                },
                'id': 'EA'
            },
            'matching_strategy': 'SINGLE_SELLER',
            'seller_id': 'magazineluiza',
            'seller_description': 'Magazine Luiza',
            'ean': '6925281914195',
            'review_count': 0,
            'md5': 'f6f29f93a34e10da0ddca7d3bc733a36',
            'type': 'product',
            'dimensions': {
                'width': 0.12,
                'height': 0.18,
                'weight': 1.55,
                'depth': 0.26
            },
            'grade': 10,
            'updated_at': '2018-03-04T12:30:54.723000'
        }

    @classmethod
    def magazineluiza_sku_218828600(cls):
        return {
            'parent_sku': '2188286',
            'created_at': '2017-10-14T08:51:58',
            'grade': 1010,
            'review_count': 0,
            'description': 'A Caixa Bluetooth à prova d´agua Charge 3 agora vem com carregador portátil e deixa o som ainda mais potente. Escute suas músicas sem fios, por muito mais tempo e ainda leve sua festa para todo o lugar. Graças ao seu design à prova dágua, tecido durável e carcaça resistente, ela pode até cair na piscina.\n\nA caixa de som conta com viva-voz que possui cancelamento de ruído e eco, garantindo ligações cristalinas possíveis de serem atendidas com apensa um simples toque.',  # noqa
            'main_category': {
                'id': 'EA',
                'subcategory': {
                    'id': 'CSBL'
                }
            },
            'review_score': 0,
            'sells_to_company': True,
            'brand': 'jbl',
            'updated_at': '2018-03-06T06:10:59.590000',
            'attributes': [{
                'value': 'Verde',
                'type': 'color'
            }],
            'sold_count': 22,
            'navigation_id': '218828600',
            'md5': '39a3a5979ea01b195e6145417665f16f',
            'sku': '218828600',
            'dimensions': {
                'height': 0.18,
                'weight': 1.55,
                'width': 0.12,
                'depth': 0.26
            },
            'selections': {
                '0': ['18033', '18787', '18789', '21370', '21574', '21613', '21615', '21675', '21925', '22002', '22011', '22045', '22121', '22132', '22146', '22149', '22150', '22152', '22659', '22728', '22768', '22780', '22826', '22830'],  # noqa
                '12966': ['16734', '16737']
            },
            'seller_description': 'Magazine Luiza',
            'disable_on_matching': False,
            'main_variation': True,
            'title': 'Caixa de Som Bluetooth Portátil JBL Charge 3 ',
            'reference': '20W USB à Prova de Água',
            'seller_id': 'magazineluiza',
            'ean': '6925281923203',
            'categories': [{
                'id': 'EA',
                'subcategories': [{
                    'id': 'CSBL'
                }, {
                    'id': 'AUCX'
                }]
            }],
            'type': 'product',
            'matching_strategy': 'SINGLE_SELLER'
        }

    @classmethod
    def magazineluiza_sku_218178700(cls):
        return {
            'brand': 'brastemp',
            'selections': {
                '0': ['18787', '21869', '21954', '21998', '22021', '22356', '22645', '22832', '22852', '6874'],  # noqa
                '12966': ['16734', '16737']
            },
            'reference': '500L BRM58AB Branco',
            'main_category': {
                'subcategory': {
                    'id': 'ELGF'
                },
                'id': 'ED'
            },
            'main_variation': True,
            'categories': [{
                'id': 'ED',
                'subcategories': [{
                    'id': 'ELGF'
                }, {
                    'id': 'REF2'
                }, {
                    'id': 'REFR'
                }]
            }],
            'parent_sku': '2181787',
            'matching_strategy': 'SINGLE_SELLER',
            'disable_on_matching': False,
            'md5': '8fa17eac18c64f6d2320851ba61421e5',
            'dimensions': {
                'width': 0.7,
                'depth': 0.73,
                'height': 1.94,
                'weight': 82
            },
            'navigation_id': '218178700',
            'type': 'product',
            'sells_to_company': True,
            'title': 'Geladeira/Refrigerador Brastemp Frost Free Duplex ',
            'seller_description': 'Magazine Luiza',
            'attributes': [{
                'type': 'color',
                'value': 'Branco'
            }, {
                'type': 'voltage',
                'value': '110 Volts'
            }],
            'description': 'Refrigerador BRM58AB da Brastemp. Esse refrigerador  Frost Free Duplex conta com o exclusivo sistema Twist Ice Advanced que permite abastecer as formas de gelo de um jeito inteligente, evitando molhar o chão da cozinha, além de desenformar o gelo facilmente e armazená-lo em um recipiente portátil e prático. Conta também com prateleiras com múltiplas combinações possíveis para armazenar itens de diversos tamanhos na porta de sua geladeira. Compartimento retrátil para armazenar vinhos na posição ideal de conservação, aproveitando ao máximo o espaço do seu refrigerador. E um compartimento especial para gelar rápido suas bebidas. Ele pode ser encaixado tanto no freezer como no refrigerador para gelar a cerveja ou o refrigerante, com um espaço perfeito para 3 garrafas long neck ou 6 latas. Leve agora esse refrigerador e tenha o melhor da Brastemp na sua casa! \n\n\n',  # noqa

            'ean': '7891129251939',
            'created_at': '2017-07-21T08:44:22.543000',
            'sold_count': 14,
            'sku': '218178700',
            'review_count': 0,
            'seller_id': 'magazineluiza',
            'updated_at': '2018-03-05T21:09:34.990000',
            'grade': 1010,
            'review_score': 0
        }

    @classmethod
    def magazineluiza_sku_218178900(cls):
        return {
            'reference': '500L BRM58AK Evox',
            'created_at': '2017-07-21T08:44:22.543000',
            'sku': '218178900',
            'grade': 1010,
            'description': 'Refrigerador BRM58AK da Brastemp. Esse refrigerador  Frost Free Duplex conta com o exclusivo sistema Twist Ice Advanced que permite abastecer as formas de gelo de um jeito inteligente, evitando molhar o chão da cozinha, além de desenformar o gelo facilmente e armazená-lo em um recipiente portátil e prático. Conta também com prateleiras com múltiplas combinações possíveis para armazenar itens de diversos tamanhos na porta de sua geladeira. Compartimento retrátil para armazenar vinhos na posição ideal de conservação, aproveitando ao máximo o espaço do seu refrigerador. E um compartimento especial para gelar rápido suas bebidas. Ele pode ser encaixado tanto no freezer como no refrigerador para gelar a cerveja ou o refrigerante, com um espaço perfeito para 3 garrafas long neck ou 6 latas. Leve agora esse refrigerador e tenha o melhor da Brastemp na sua casa! \n\n\n',  # noqa
            'dimensions': {
                'width': 0.7,
                'height': 1.94,
                'weight': 82,
                'depth': 0.73
            },
            'main_variation': True,
            'ean': '7891129251670',
            'parent_sku': '2181789',
            'sold_count': 30,
            'navigation_id': '218178900',
            'categories': [{
                'subcategories': [{
                    'id': 'ELGF'
                }, {
                    'id': 'REF2'
                }, {
                    'id': 'REFR'
                }],
                'id': 'ED'
            }],
            'type': 'product',
            'md5': '85400e3e8972fcaa4b826ab9af73048b',
            'sells_to_company': True,
            'disable_on_matching': False,
            'matching_strategy': 'SINGLE_SELLER',
            'main_category': {
                'subcategory': {
                    'id': 'ELGF'
                },
                'id': 'ED'
            },
            'review_count': 0,
            'selections': {
                '0': ['18787', '21863', '21869', '22021', '22356', '22373', '22515', '22616', '22645', '22651', '22658', '22678', '22681', '22697', '22778', '22786', '22832', '22852', '6874'],  # noqa
                '12966': ['16734', '16737']
            },
            'seller_id': 'magazineluiza',
            'seller_description': 'Magazine Luiza',
            'updated_at': '2018-03-06T05:51:15.677000',
            'brand': 'brastemp',
            'attributes': [{
                'type': 'color',
                'value': 'Inox'
            }, {
                'type': 'voltage',
                'value': '110 Volts'
            }],
            'title': 'Geladeira/Refrigerador Brastemp Frost Free Duplex ',
            'review_score': 0
        }

    @classmethod
    def magazineluiza_sku_218178800(cls):
        return {
            'review_count': 0,
            'type': 'product',
            'dimensions': {
                'height': 1.94,
                'width': 0.7,
                'weight': 82,
                'depth': 0.73
            },
            'description': 'Refrigerador BRM58AB da Brastemp. Esse refrigerador  Frost Free Duplex conta com o exclusivo sistema Twist Ice Advanced que permite abastecer as formas de gelo de um jeito inteligente, evitando molhar o chão da cozinha, além de desenformar o gelo facilmente e armazená-lo em um recipiente portátil e prático. Conta também com prateleiras com múltiplas combinações possíveis para armazenar itens de diversos tamanhos na porta de sua geladeira. Compartimento retrátil para armazenar vinhos na posição ideal de conservação, aproveitando ao máximo o espaço do seu refrigerador. E um compartimento especial para gelar rápido suas bebidas. Ele pode ser encaixado tanto no freezer como no refrigerador para gelar a cerveja ou o refrigerante, com um espaço perfeito para 3 garrafas long neck ou 6 latas. Leve agora esse refrigerador e tenha o melhor da Brastemp na sua casa! \n\n\n',  # noqa
            'brand': 'brastemp',
            'matching_strategy': 'SINGLE_SELLER',
            'navigation_id': '218178800',
            'review_score': 0,
            'md5': 'e35af4d0b608b3dce2dd0fe14a8c770e',
            'sold_count': 3,
            'updated_at': '2018-03-04T23:07:34.173000',
            'main_category': {
                'id': 'ED',
                'subcategory': {
                    'id': 'ELGF'
                }
            },
            'ean': '7891129251946',
            'sku': '218178800',
            'created_at': '2017-07-21T08:44:22.543000',
            'categories': [{
                'subcategories': [{
                    'id': 'ELGF'
                }, {
                    'id': 'REF2'
                }, {
                    'id': 'REFR'
                }],
                'id': 'ED'
            }],
            'selections': {
                '0': ['18787', '21869', '21954', '21998', '22021', '22356', '22645', '22832', '22852', '6874'],  # noqa
                '12966': ['16734', '16737']
            },
            'title': 'Geladeira/Refrigerador Brastemp Frost Free Duplex ',
            'sells_to_company': True,
            'parent_sku': '2181787',
            'attributes': [{
                'type': 'color',
                'value': 'Branco'
            }, {
                'type': 'voltage',
                'value': '220 Volts'
            }],
            'seller_id': 'magazineluiza',
            'disable_on_matching': False,
            'seller_description': 'Magazine Luiza',
            'grade': 1010,
            'reference': '500L BRM58AB Branco',
            'main_variation': False
        }

    @classmethod
    def magazineluiza_sku_218179000(cls):
        return {
            'parent_sku': '2181789',
            'reference': '500L BRM58AK Evox',
            'sku': '218179000',
            'seller_id': 'magazineluiza',
            'navigation_id': '218179000',
            'main_category': {
                'subcategory': {
                    'id': 'ELGF'
                },
                'id': 'ED'
            },
            'brand': 'brastemp',
            'selections': {
                '12966': ['16734', '16737'],
                '0': ['18787', '21863', '21869', '22021', '22356', '22373', '22515', '22616', '22645', '22651', '22658', '22678', '22681', '22697', '22778', '22786', '22832', '22852', '6874']  # noqa
            },
            'description': 'Refrigerador BRM58AK da Brastemp. Esse refrigerador  Frost Free Duplex conta com o exclusivo sistema Twist Ice Advanced que permite abastecer as formas de gelo de um jeito inteligente, evitando molhar o chão da cozinha, além de desenformar o gelo facilmente e armazená-lo em um recipiente portátil e prático. Conta também com prateleiras com múltiplas combinações possíveis para armazenar itens de diversos tamanhos na porta de sua geladeira. Compartimento retrátil para armazenar vinhos na posição ideal de conservação, aproveitando ao máximo o espaço do seu refrigerador. E um compartimento especial para gelar rápido suas bebidas. Ele pode ser encaixado tanto no freezer como no refrigerador para gelar a cerveja ou o refrigerante, com um espaço perfeito para 3 garrafas long neck ou 6 latas. Leve agora esse refrigerador e tenha o melhor da Brastemp na sua casa! \n\n\n',  # noqa
            'attributes': [{
                'type': 'color',
                'value': 'Inox'
            }, {
                'value': '220 Volts',
                'type': 'voltage'
            }],
            'dimensions': {
                'width': 0.7,
                'weight': 82,
                'depth': 0.73,
                'height': 1.94
            },
            'grade': 1010,
            'review_count': 0,
            'categories': [{
                'subcategories': [{
                    'id': 'ELGF'
                }, {
                    'id': 'REF2'
                }, {
                    'id': 'REFR'
                }],
                'id': 'ED'
            }],
            'ean': '7891129251687',
            'title': 'Geladeira/Refrigerador Brastemp Frost Free Duplex ',
            'review_score': 0,
            'matching_strategy': 'SINGLE_SELLER',
            'type': 'product',
            'seller_description': 'Magazine Luiza',
            'md5': '2328fd7980b9a256119e4b086b8defa4',
            'main_variation': False,
            'sold_count': 12,
            'disable_on_matching': False,
            'sells_to_company': True,
            'created_at': '2017-07-21T08:44:22.543000',
            'updated_at': '2018-03-06T06:10:59.590000'
        }

    @classmethod
    def magazineluiza_sku_214945600(cls):
        return {
            'description': 'JBL Xtreme é a mais nova caixa de som Bluetooth portátil que oferece um som extremamente poderoso com seus quatro transdutores ativos e dois radiadores passivos. Esta caixa de som proporciona 15 horas de som contínuo de alta qualidade de áudio estéreo.\n\nAlém disso, apresenta duas entradas USB para recarregar seus dispositivos móveis e materiais de alta qualidade com laterais emborrachadas e tecido á prova de respingos d’agua.\n\nO Xtreme também possui cancelamento de ruído para chamadas que proporcionam um som limpo e cristalino. Além da mais nova tecnologia JBL CONNECT que permite conectar até dois dispositivos com a mesma tecnologia ou até mesmo que até três usuários diferentes utilizem seus smartphones ou tablets na mesma caixa Bluetooth, de forma alternada.',  # noqa
            'sells_to_company': True,
            'created_at': '2015-12-23T06:53:44.593000',
            'ean': '6925281904578',
            'title': 'Caixa de Som Bluetooth JBL Xtreme 40W ',
            'dimensions': {
                'height': 0.2,
                'weight': 3.5,
                'depth': 0.2,
                'width': 0.33
            },
            'review_score': 0,
            'matching_strategy': 'SINGLE_SELLER',
            'review_count': 0,
            'disable_on_matching': False,
            'updated_at': '2018-03-06T21:05:24.837000',
            'sold_count': 60,
            'grade': 10,
            'brand': 'jbl',
            'navigation_id': '214945600',
            'seller_id': 'magazineluiza',
            'main_category': {
                'id': 'EA',
                'subcategory': {
                    'id': 'CSBL'
                }
            },
            'reference': 'USB À Prova de Respingos dágua',
            'type': 'product',
            'sku': '214945600',
            'parent_sku': '2149456',
            'selections': {
                '12966': ['16734', '16737'],
                '0': ['18033', '18787', '18789', '20488', '20678', '20703', '21155', '21370', '21574', '21615', '21860', '21925', '22002', '22338', '22528', '22556', '22659', '22725', '22734', '22780', '22826', '22885']  # noqa
            },
            'md5': '133cedb16d3f4b271cd1153a82b4e47e',
            'categories': [{
                'subcategories': [{
                    'id': 'CSBL'
                }, {
                    'id': 'AUCX'
                }],
                'id': 'EA'
            }],
            'seller_description': 'Magazine Luiza',
            'main_variation': False
        }

    @classmethod
    def magazineluiza_sku_218557900(cls):
        return {
            'parent_sku': '2149456',
            'reference': 'USB À Prova de Respingos dágua',
            'sku': '218557900',
            'dimensions': {
                'width': 0.25,
                'weight': 2.2,
                'depth': 0.15,
                'height': 0.15
            },
            'navigation_id': '218557900',
            'main_category': {
                'subcategory': {
                    'id': 'CSBL'
                },
                'id': 'EA'
            },
            'brand': 'jbl',
            'selections': {
                '12966': ['16734', '16737'],
                '0': ['18033', '18787', '18789', '20488', '20678', '20703', '21155', '21370', '21574', '21615', '21860', '21925', '22002', '22338', '22528', '22556', '22659', '22725', '22734', '22780', '22826', '22885']  # noqa
            },
            'description': 'Com a caixa de som portátil Xtreme de JBL, a festa nunca acaba! Extremamente poderosa, proporcionando até 15 horas de som contínuo de altíssima qualidade e som estéreo. Conta ainda com bluetooth, potência de 40W, entrada USB, microfone embutido permitindo que você controle suas músicas e atenda chamadas. Além disso, possui laterais emborrachadas, fazendo com que a mesma se torne resistente a respingos de água. A Xtreme possui cancelamento de ruído para chamadas, garantindo um som limpo e cristalino. A tecnologia JBL Connect lhe permite conectar até dois dispositivos com a mesma tecnologia, ou até três usuários diferentes que utilizem seus smatphones ou tablets na mesma caixa bluetooth de forma alternada. Ah, seu tipo ativa e alça para transporte, garante com que o produto supra suas necessidades. Compartilhe a melhor experiência sonora com seus amigos!\n\n\n\n',  # noqa
            'seller_id': 'magazineluiza',
            'grade': 1010,
            'review_count': 0,
            'created_at': '2017-12-30T07:56:57.837000',
            'ean': '6925281904592',
            'title': 'Caixa de Som Bluetooth JBL Xtreme 40W',
            'review_score': 0,
            'matching_strategy': 'SINGLE_SELLER',
            'type': 'product',
            'seller_description': 'Magazine Luiza',
            'md5': 'adca02ffcd2fccee8069f7339c05142e',
            'main_variation': False,
            'sold_count': 7,
            'disable_on_matching': False,
            'sells_to_company': True,
            'categories': [{
                'subcategories': [{
                    'id': 'CSBL'
                }, {
                    'id': 'AUCX'
                }],
                'id': 'EA'
            }],
            'updated_at': '2018-03-04T19:01:35.143000'
        }

    @classmethod
    def magazineluiza_sku_218557800(cls):
        return {
            'sells_to_company': True,
            'sold_count': 12,
            'grade': 1010,
            'ean': '6925281923135',
            'categories': [{
                'id': 'EA',
                'subcategories': [{
                    'id': 'CSBL'
                }, {
                    'id': 'AUCX'
                }]
            }],
            'seller_id': 'magazineluiza',
            'description': 'Com a caixa de som portátil Xtreme de JBL, a festa nunca acaba! Extremamente poderosa, proporcionando até 15 horas de som contínuo de altíssima qualidade e som estéreo. Conta ainda com bluetooth, potência de 40W, entrada USB, microfone embutido permitindo que você controle suas músicas e atenda chamadas. Além disso, possui laterais emborrachadas, fazendo com que a mesma se torne resistente a respingos de água. A Xtreme possui cancelamento de ruído para chamadas, garantindo um som limpo e cristalino. A tecnologia JBL Connect lhe permite conectar até dois dispositivos com a mesma tecnologia, ou até três usuários diferentes que utilizem seus smatphones ou tablets na mesma caixa bluetooth de forma alternada. Ah, seu tipo ativa e alça para transporte, garante com que o produto supra suas necessidades. Compartilhe a melhor experiência sonora com seus amigos!\n\n\n\n',  # noqa
            'title': 'Caixa de Som Bluetooth JBL Xtreme 40W',
            'navigation_id': '218557800',
            'review_count': 0,
            'main_category': {
                'subcategory': {
                    'id': 'CSBL'
                },
                'id': 'EA'
            },
            'updated_at': '2018-03-06T05:50:27.460000',
            'sku': '218557800',
            'md5': 'cd717cc7119c3ba262106e4d4f31912c',
            'disable_on_matching': False,
            'type': 'product',
            'brand': 'jbl',
            'main_variation': False,
            'review_score': 0,
            'dimensions': {
                'height': 0.15,
                'width': 0.25,
                'weight': 2.2,
                'depth': 0.15
            },
            'selections': {
                '0': ['18033', '18787', '18789', '20488', '20678', '20703', '21155', '21370', '21574', '21615', '21860', '21925', '22002', '22338', '22528', '22556', '22659', '22725', '22734', '22780', '22826', '22885'],  # noqa
                '12966': ['16734', '16737']
            },
            'matching_strategy': 'SINGLE_SELLER',
            'reference': 'USB À Prova de Respingos dágua',
            'seller_description': 'Magazine Luiza',
            'created_at': '2017-12-30T07:56:57.837000',
            'parent_sku': '2149456'
        }

    @classmethod
    def efacil_sku_193574_46(cls):
        return {
            'main_variation': True,
            'seller_description': 'eFácil',
            'ean': '7891356069321',
            'grade': 10,
            'attributes': [{
                'value': '220 Volts',
                'type': 'voltage'
            }],
            'sold_count': 0,
            'sku': '193574-46',
            'md5': '861ec5eb03ea3c7e1df5b975f1f35208',
            'review_score': 0,
            'reference': '',
            'parent_sku': '193574',
            'navigation_id': '6996333',
            'created_at': '2018-01-24T05:53:01.011140+00:00',
            'review_count': 0,
            'updated_at': '2018-01-24T05:53:01.023816+00:00',
            'disable_on_matching': False,
            'type': 'product',
            'brand': 'Philco',
            'dimensions': {
                'weight': 18.8,
                'width': 0.46,
                'height': 0.53,
                'depth': 0.95
            },
            'categories': [{
                'id': 'ED',
                'description': 'Eletrodomésticos',
                'subcategories': [{
                    'id': 'COFA',
                    'description': 'Coifa'
                }]
            }],
            'release_date': '2018-03-29T22:45:18.230249+00:00',
            'sells_to_company': True,
            'title': 'Coifa de Parede Philco 90cm Inox',
            'seller_id': 'efacil',
            'matching_strategy': 'SINGLE_SELLER',
            'description': 'Coifa de Parede Philco 90cm Inox<br />Ficha Técnica <br /><br/>Características do produto:<br/>Tipo de Coifa/Depurador: Coifa de Parede<br/>Altura: 55,6 cm<br/>Largura: 90,0 cm<br/>Profundidade:50,0 cm<br/>Indicação: Até 6 Bocas<br/>Tipo de Selo Inmetro: Segurança<br/><br/>Dados Adicionais do produto:<br/>Timer de desligamento Automático;<br/>Dupla Função: pode ser usado com Depurador e Exaustor<br/>Possui três velocidades: Possibilita o ajuste de acordo com a quantidade de fumaça a ser absorvida<br/>Painel Touch: Rápido e prático para utilização<br/>Regulagem de altura: Possibilita o ajuste mais adequado à altura da cozinha<br/>Painel Digital<br/>Relógio Digital<br/>Com 90 cm: Para fogões de até 6 bocas<br/>Filtro de Carvão Ativo e Alumínio: Muito mais absorção de gordura e fumaça<br/>Lâmpadas de LED de baixo consumo: Dois conjuntos de lâmpadas LED práticas para iluminar o fogão<br/>Acompanha Duto<br/>Acompanha kit de instalação<br/>Vazão 900m²/h<br/>Regulado de Altura de acabamento do Duto<br/>Composição Metal<br/> <br/>Embalagem:<br/>Aparelho:<br/>Peso: 19,2 kg<br/>Altura: 55,6 cm<br/>Largura: 90,0 cm<br/>Profundidade: 50,0 cm<br/><br/>Caixa Unitária:<br/>Peso: 22,0 kg<br/>Altura: 52,5 cm<br/>Largura: 93,5 cm<br/>Profundidade: 63,0 cm<br/><br/>Garantia: 1 Ano ( Ofertada pelo Fabricante)<br/><br/>SAC - Fornecedor <br/>Philco<br/>0800 645 8300<br/>Ficha Técnica<br/><br/>Selo Inmetro: Sim<br/>Profundidade(em Cm): 90<br/>Indicação: Até 6 Bocas<br/>Altura(em Cm): 55.6<br/>Tipo Coifa/Depurador: Coifa de Parede<br/>Tipo de Selo Inmetro: Segurança<br/>Garantia: 1 Ano<br/>Largura(em Cm): 50'  # noqa
        }

    @classmethod
    def efacil_sku_193574_123(cls):
        return {
            'title': 'Coifa de Parede Philco 90cm Inox',
            'reference': '',
            'categories': [{
                'subcategories': [{
                    'description': 'Coifa',
                    'id': 'COFA'
                }],
                'description': 'Eletrodomésticos',
                'id': 'ED'
            }],
            'created_at': '2018-01-24T05:53:01.011140+00:00',
            'parent_sku': '193574',
            'navigation_id': '6491292',
            'main_variation': False,
            'seller_description': 'eFácil',
            'grade': 10,
            'review_score': 0,
            'type': 'product',
            'description': 'Coifa de Parede Philco 90cm Inox<br />Ficha Técnica <br /><br/>Características do produto:<br/>Tipo de Coifa/Depurador: Coifa de Parede<br/>Altura: 55,6 cm<br/>Largura: 90,0 cm<br/>Profundidade:50,0 cm<br/>Indicação: Até 6 Bocas<br/>Tipo de Selo Inmetro: Segurança<br/><br/>Dados Adicionais do produto:<br/>Timer de desligamento Automático;<br/>Dupla Função: pode ser usado com Depurador e Exaustor<br/>Possui três velocidades: Possibilita o ajuste de acordo com a quantidade de fumaça a ser absorvida<br/>Painel Touch: Rápido e prático para utilização<br/>Regulagem de altura: Possibilita o ajuste mais adequado à altura da cozinha<br/>Painel Digital<br/>Relógio Digital<br/>Com 90 cm: Para fogões de até 6 bocas<br/>Filtro de Carvão Ativo e Alumínio: Muito mais absorção de gordura e fumaça<br/>Lâmpadas de LED de baixo consumo: Dois conjuntos de lâmpadas LED práticas para iluminar o fogão<br/>Acompanha Duto<br/>Acompanha kit de instalação<br/>Vazão 900m²/h<br/>Regulado de Altura de acabamento do Duto<br/>Composição Metal<br/> <br/>Embalagem:<br/>Aparelho:<br/>Peso: 19,2 kg<br/>Altura: 55,6 cm<br/>Largura: 90,0 cm<br/>Profundidade: 50,0 cm<br/><br/>Caixa Unitária:<br/>Peso: 22,0 kg<br/>Altura: 52,5 cm<br/>Largura: 93,5 cm<br/>Profundidade: 63,0 cm<br/><br/>Garantia: 1 Ano ( Ofertada pelo Fabricante)<br/><br/>SAC - Fornecedor <br/>Philco<br/>0800 645 8300<br/>Ficha Técnica<br/><br/>Selo Inmetro: Sim<br/>Profundidade(em Cm): 90<br/>Indicação: Até 6 Bocas<br/>Altura(em Cm): 55.6<br/>Tipo Coifa/Depurador: Coifa de Parede<br/>Tipo de Selo Inmetro: Segurança<br/>Garantia: 1 Ano<br/>Largura(em Cm): 50',  # noqa
            'dimensions': {
                'height': 0.53,
                'weight': 18.8,
                'depth': 0.95,
                'width': 0.46
            },
            'matching_strategy': 'SINGLE_SELLER',
            'sells_to_company': True,
            'release_date': '2018-03-13T11:04:05.987215+00:00',
            'sold_count': 0,
            'brand': 'Philco',
            'ean': '7891356069314',
            'disable_on_matching': False,
            'attributes': [{
                'type': 'voltage',
                'value': '110 Volts'
            }],
            'seller_id': 'efacil',
            'review_count': 0,
            'sku': '193574-123',
            'updated_at': '2018-01-24T05:53:01.023816+00:00',
            'md5': 'e148f7a39f1b92839d2b6a0ef2e9f7aa'
        }

    @classmethod
    def lojamultilaser_sku_3770(cls):
        return {
            'brand': 'Multilaser',
            'disable_on_matching': False,
            'ean': '7899838833019',
            'sold_count': 0,
            'attributes': [{
                'value': 'Preto',
                'type': 'color'
            }],
            'grade': 20,
            'review_score': 0,
            'parent_sku': '3767',
            'reference': '',
            'description': '<br>MS80 chega com qualidade, desempenho e design premium dentro do estilo multimelhor de ser: inovação com custo-benefício. Desde a tela de 5,7 com bordas finas até o processador Qualcomm Snapdragon, a experiência é incrível, completa e rápida. A inovação fica por conta da câmera Dual Selfie com 20 MP + 8 MP e lente grande-angular de 120 graus. Mais resolução e cobertura para a sua selfie que cabe todo mundo!<br><br><br><br>Imagens Meramente Ilustrativas*',  # noqa
            'seller_id': 'lojamultilaser',
            'sku': '3770',
            'review_count': 0,
            'main_variation': True,
            'md5': 'cdc6b53d0bce4a2dd94e424c9b0da608',
            'created_at': '2018-01-20T18:17:26.718762+00:00',
            'matching_strategy': 'SINGLE_SELLER',
            'dimensions': {
                'weight': 0.2,
                'depth': 0.01,
                'width': 0.07,
                'height': 0.15
            },
            'type': 'product',
            'release_date': '2018-03-22T18:17:41.291555+00:00',
            'seller_description': 'MMPLACE',
            'navigation_id': '6311101',
            'categories': [{
                'id': 'TE',
                'description': 'Celulares e Smartphones',
                'subcategories': [{
                    'id': 'TCSP',
                    'description': 'Smartphone'
                }]
            }],
            'sells_to_company': True,
            'title': 'Smartphone Multilaser MS80 3GB RAM + 32GB Tela 5,7\' HD+ 4G Android 7.1 Qualcomm Dual Câmera 20MP+8MP Preto',  # noqa
            'updated_at': '2018-03-22T18:17:37.693360+00:00'
        }

    @classmethod
    def lojamultilaser_sku_3771(cls):
        return {
            'main_variation': True,
            'seller_id': 'lojamultilaser',
            'grade': 20,
            'attributes': [{
                'type': 'color',
                'value': 'Dourado'
            }],
            'sku': '3771',
            'review_count': 0,
            'reference': '',
            'updated_at': '2018-03-22T18:17:42.738753+00:00',
            'sold_count': 0,
            'ean': '7899838833026',
            'dimensions': {
                'depth': 0.01,
                'width': 0.07,
                'weight': 0.2,
                'height': 0.15
            },
            'title': 'Smartphone Multilaser MS80 3GB RAM + 32GB Tela 5,7\' HD+ Android 7.1 Qualcomm Dual Câmera 20MP+8MP Dourado',   # noqa
            'release_date': '2018-03-22T18:17:49.759843+00:00',
            'md5': '381f525f15c9676373c4a61c3886cdca',
            'parent_sku': '3768',
            'description': '<br>MS80 chega com qualidade, desempenho e design premium dentro do estilo multimelhor de ser: inovação com custo-benefício. Desde a tela de 5,7 com bordas finas até o processador Qualcomm Snapdragon, a experiência é incrível, completa e rápida. A inovação fica por conta da câmera Dual Selfie com 20 MP + 8 MP e lente grande-angular de 120 graus. Mais resolução e cobertura para a sua selfie que cabe todo mundo!<br><br><br><br>Imagens Meramente Ilustrativas*',  # noqa
            'disable_on_matching': False,
            'categories': [{
                'subcategories': [{
                    'description': 'Smartphone',
                    'id': 'TCSP'
                }],
                'description': 'Celulares e Smartphones',
                'id': 'TE'
            }],
            'matching_strategy': 'SINGLE_SELLER',
            'created_at': '2018-01-20T18:17:29.959751+00:00',
            'brand': 'Multilaser',
            'type': 'product',
            'navigation_id': '6614169',
            'review_score': 0,
            'seller_description': 'MMPLACE',
            'sells_to_company': True
        }

    @classmethod
    def epocacosmeticos_sku_2546(cls):
        return {
            'title': '1 Million Paco Rabanne - Perfume Masculino - Eau de Toilette',  # noqa
            'main_variation': False,
            'review_score': 0,
            'review_count': 0,
            'parent_sku': '2546',
            'sold_count': 0,
            'type': 'product',
            'md5': '1cab7e4b0c33796c697be0f2b84c68e8',
            'matching_strategy': 'SINGLE_SELLER',
            'release_date': '2018-05-01T00:17:14.449861+00:00',
            'sells_to_company': True,
            'seller_id': 'epocacosmeticos',
            'ean': '3349666007891',
            'created_at': '2016-03-26T14:55:57.259697+00:00',
            'seller_description': 'Época Cosméticos Perfumaria',
            'attributes': [{
                'type': 'volume',
                'value': '50ml'
            }],
            'navigation_id': '9452723',
            'sku': '2546',
            'brand': 'Paco Rabanne',
            'reference': '',
            'description': 'One Million é o perfume importado que descreve o homem de personalidade forte. Leve e refrescante, o perfume One Million, por Paco Rabanne é um verdadeiro objeto de design e expressões, o que é perceptível logo no primeiro contato visual com o produto. A embalagem dourada, com a gravação de um número de série na parte inferior, remete à barras de ouro, o que confere um toque de sofisticação inigualável ao perfume.\r\n\r\nSe o contato visual com o perfume  é incrível, o contato olfativo com a fragrância é espetacular, pois One Million torna-se ainda mais forte e intuitivo com essa interpretação: uma extravagante nota de topo de tangerina sanguínea e especiarias reforçadas por vibrantes notas de base de íris e sândalo.\r\n\r\nOne Million nos propõe um cruel Dilema: desejamos mais o objeto ou a fragrância?\r\nA resposta parece clara: ambos\r\n\r\nA Fragrância:\r\nOne Million é um perfume masculino, que se abre com notas de Pomelo, Menta Picante, Mandarina. Como notas de coração desta fragrância Amadeirado Especiado, Rosa, Canela, Condimentos. As notas de fundo contam com nuances de Couro Aveludado, Madeira Branca, Âmbar, Patchouli da Indonésia.\r\n\r\nO Frasco:\r\nO frasco deste perfume masculino na forma de um lingote de ouro possui o nome da fragrância impresso com a tipografia dos tempos do Velho Oeste, representando poder, prosperidade, luxo e durabilidade. Segundo seu criador, em todas as civilizações e religiões, o ouro sempre seduziu as pessoas. Objeto do desejo supremo, este lingote abriga um jogo atrevido de notas olfativas, abrindo a fragrância com notas frutadas e picantes.',  # noqa
            'dimensions': {
                'width': 10,
                'depth': 10,
                'weight': 0.1,
                'height': 10
            },
            'last_updated_at': '2018-05-01T00:17:15.011437',
            'updated_at': '2018-05-01T00:17:13.089516+00:00',
            'categories': [{
                'subcategories': [{
                    'id': 'PFPM',
                    'description': 'Perfumes importados masculinos'
                }, {
                    'id': 'PFPI',
                    'description': 'Perfumes Importados'
                }],
                'id': 'PF',
                'description': 'Perfumaria'
            }],
            'disable_on_matching': False,
            'grade': 10
        }

    @classmethod
    def shoploko_sku_74471(cls):
        return {
            'dimensions': {
                'width': 0.32,
                'depth': 0.32,
                'height': 0.37,
                'weight': 4.85
            },
            'review_score': 0,
            'description': 'Fritadeira Family Mondial 3.2L AF-14 110V - Vemelha<BR>Características:<BR>Design moderno em Aço Inox<BR>Controle de temperatura de até 200ºC<BR>Timer de 60 minutos<BR>Peças removíveis para fácil limpeza<BR>Prepara petiscos, massas, carnes, pastéis, pão de queijo, churros, peixes<BR>Capacidade de até 3,2 litros no cesto de alimentos<BR>Espeficicações:<BR>Consumo de energia (kW/h): 1,5<BR>Temperatura máxima (°C): 200<BR>Capacidade (litros): 3,2<BR>Potência (W): 1500<BR>Cor: Vermelho<BR>Tensão/Voltagem: 110V<BR>Cesto removível: Sim<BR>Tipo Sem óleo*<BR>Cor: Inox<BR>Capacidade (litros) Acima de: 2,6L<BR>Voltagem: 127V<BR>Dimensões:<BR>Altura: 33,00<BR>Largura: 35,00<BR>Profundidade: 27,00<BR>Peso: 5,10<BR>Conteúdo da Embalagem:<BR>1 Fritadeira Mondial<BR>1 Manual de Assistência Técnica<BR>1 Manual de Instruções<BR>Ean: 7899882302516<BR>Garantia 12 meses',  # noqa
            'title': 'Fritadeira Family Mondial 3.2L AF-14 110V - Vemelha',
            'created_at': '2018-03-13T19:01:10.774684+00:00',
            'seller_id': 'shoploko',
            'grade': 10,
            'last_updated_at': '2018-05-05T22:18:08.457391',
            'attributes': [],
            'review_count': 0,
            'main_variation': True,
            'sold_count': 0,
            'type': 'product',
            'disable_on_matching': False,
            'categories': [{
                'description': 'Eletroportáteis',
                'subcategories': [{
                    'description': 'Fritadeira Elétrica',
                    'id': 'FREL'
                }],
                'id': 'EP'
            }],
            'reference': '',
            'navigation_id': '6242299',
            'sells_to_company': True,
            'seller_description': 'Shoploko',
            'sku': '74471',
            'parent_sku': '74471',
            'matching_strategy': 'SINGLE_SELLER',
            'ean': '7899882302516',
            'updated_at': '2018-03-13T19:01:10.789532+00:00',
            'release_date': '2018-05-05T22:18:07.745280+00:00',
            'brand': 'MONDIAL',
            'md5': '313b48c2844609b75e0f4079a0163fb8'
        }

    @classmethod
    def magazineluiza_sku_0233847(cls):
        return {
            'seller_description': 'Magazine Luiza',
            'title': 'Fritadeira Elétrica Air Fryer/Sem Óleo Mondial',
            'review_score': 0,
            'grade': 1010,
            'dimensions': {
                'depth': 0.32,
                'weight': 12.33,
                'height': 0.36,
                'width': 0.32
            },
            'seller_id': 'magazineluiza',
            'brand': 'mondial',
            'created_at': '2017-07-21T08:44:22.543000',
            'last_updated_at': '2018-05-07T13:07:52.507805',
            'md5': '305042de772de075df1c2f6891a468d5',
            'disable_on_matching': False,
            'matching_strategy': 'SINGLE_SELLER',
            'description': 'O que era inimaginável agora é real, sim, você pode fritar alimentos sem usar óleo, sem deixar cheiro de gordura ou fumaça pela casa, e tem mais, você também pode preparar alimentos de maneira incrivelmente rápida e deixar tudo crocante, gostoso e mais saudável para a sua família!\nCom a incrível Fritadeira Sem Óleo Inox RED Premium da Mondial tudo isso está ao seu alcance.  Painel em aço inox e design sofisticado, lâmpadas-piloto que indicam o funcionamento do produto e do aquecimento, controle de temperatura até 200 ºC para a escolha da temperatura ideal de acordo com diferentes tipos de alimentos, cesta removível segura e prática para facilitar o manuseio dos alimentos, timer de 60 minutos com sinal sonoro e desligamento automático. Com muita praticidade, você pode prepara batatas crocantes em apenas 12 min, e com o livro de receitas você também pode preparar pão de queijo, carnes, aperitivos, peixes, frango a passarinho, pastéis doces e muito mais. \n',  # noqa
            'main_variation': True,
            'ean': '7899882302516',
            'type': 'product',
            'reference': 'AF-14 3,2L Timer',
            'updated_at': '2018-05-07T09:45:14.827000',
            'main_category': {
                'subcategory': {
                    'id': 'FREL'
                },
                'id': 'EP'
            },
            'review_count': 0,
            'sold_count': 35,
            'selections': {
                '12966': ['16734', '16737'],
                '0': ['17637', '19107', '21750', '22009', '22163', '22330', '7291']  # noqa
            },
            'sku': '023384700',
            'navigation_id': '023384700',
            'sells_to_company': True,
            'attributes': [{
                'type': 'voltage',
                'value': '110 volts'
            }],
            'categories': [{
                'subcategories': [{
                    'id': 'FREL'
                }, {
                    'id': 'EFSO'
                }, {
                    'id': 'ELCO'
                }],
                'id': 'EP'
            }],
            'parent_sku': '0233847',
            'media': {
                'images': [
                    '/{w}x{h}/cama-box-queen-size-box/magazineluiza/023384700/13ee4a66986591c0a586f68b.jpg' # noqa
                ]
            }
        }

    @classmethod
    def topbrinquedos_sku_2898(cls):
        return {
            'last_updated_at': '2018-05-04T20:12:58.714400',
            'brand': 'Mondial',
            'title': 'Air Fryer Inox RED Premium 127V Mondial - AF-14',
            'seller_description': 'Top Brinquedos',
            'disable_on_matching': False,
            'parent_sku': '2898',
            'type': 'product',
            'matching_strategy': 'SINGLE_SELLER',
            'sold_count': 0,
            'navigation_id': '6520581',
            'reference': '',
            'description': '<br/> <br/>       Assa, tosta, cozinha, gratina por convecção a ar  Controle de temperatura até 200ºC  Capacidade de até 2,7 L no cesto de alimentos  Capacidade total de até 4L         Modelo: Air Fryer Inox RED  Potência: 1500W  Consumo: 1,5Kw/h  Origem: Importado  Garantia: 12 meses  Voltagem: 127V<br>        <b>Dados do produto</b> <br /> Garantia: 90(dias) <br />  Marca: Mondial<br />  NCM: 85167920<br />  EAN: 7899882302516<br /><br /> <b>Dados de Embalagem</b> <br /> Peso Total (Produto + Embalagem): 5800.00(gr)  <br />  Altura: 33.00(cm)  <br />  Largura: 35.00(cm)  <br />  Profundidade: 27.00(cm)  <br />  <br>      01 Mondial Air Fryer,   Manual de Assistência Técnica,   Manual de Instruções',  # noqa
            'sku': '2898',
            'review_score': 0,
            'ean': '7899882302516',
            'md5': '61f23f4f5b97d013b26512df8d06195c',
            'updated_at': '2018-03-24T14:36:26.033140+00:00',
            'grade': 10,
            'sells_to_company': True,
            'release_date': '2018-05-04T20:12:57.537355+00:00',
            'dimensions': {
                'depth': 0.27,
                'height': 0.33,
                'width': 0.35,
                'weight': 5.8
            },
            'main_variation': True,
            'created_at': '2018-03-24T14:36:26.019862+00:00',
            'categories': [{
                'id': 'EP',
                'subcategories': [{
                    'id': 'EFAO',
                    'description': 'Fritadera a óleo'
                }],
                'description': 'Eletroportáteis'
            }],
            'attributes': [],
            'review_count': 0,
            'seller_id': 'topbrinquedos'
        }

    @classmethod
    def amplocomercial_sku_230(cls):
        return {
            'attributes': [],
            'main_variation': True,
            'md5': '925822c908a262fa988023640d6dd1e0',
            'updated_at': '2018-03-10T18:21:21.375040+00:00',
            'parent_sku': '230',
            'title': 'Air Fryer Inox RED Premium 127V Mondial - AF-14',
            'matching_strategy': 'SINGLE_SELLER',
            'sells_to_company': True,
            'dimensions': {
                'width': 0.35,
                'depth': 0.27,
                'weight': 5.8,
                'height': 0.33
            },
            'brand': 'Mondial',
            'review_count': 0,
            'release_date': '2018-05-04T20:18:06.320710+00:00',
            'grade': 10,
            'type': 'product',
            'disable_on_matching': False,
            'last_updated_at': '2018-05-04T20:18:07.664889',
            'seller_id': 'amplocomercial',
            'created_at': '2018-03-10T18:21:21.362873+00:00',
            'ean': '7899882302516',
            'seller_description': 'Amplo Comercial',
            'sku': '230',
            'review_score': 0,
            'categories': [{
                'id': 'EP',
                'subcategories': [{
                    'id': 'EFSO',
                    'description': 'Fritadeira sem óleo (air fryer)'
                }],
                'description': 'Eletroportáteis'
            }],
            'navigation_id': '6699102',
            'sold_count': 0,
            'reference': '',
            'description': 'Assa, tosta, cozinha, gratina por convecção a ar  Controle de temperatura até 200ºC  Capacidade de até 2,7 L no cesto de alimentos  Capacidade total de até 4L     <br>  </p><p>  Descrição T&eacutecnica: <br> </p><p>    Modelo: Air Fryer Inox RED  Potência: 1500W  Consumo: 1,5Kw/h  Origem: Importado  Garantia: 12 meses  Voltagem: 127V<br>    </p><p> Itens Inclusos: </p><p>   01 Mondial Air Fryer,   Manual de Assistência Técnica,   Manual de Instruções   </p><p> <b>Dados do produto</b> <br /> Garantia: 90(dias) <br />  Marca: Mondial<br />  NCM: 85167920<br />  EAN: 7899882302516<br /><br /> <b>Dados de Embalagem</b> <br /> Peso Total (Produto + Embalagem): 5800.00(gr)  <br />  Altura: 33.00(cm)  <br />  Largura: 35.00(cm)  <br />  Profundidade: 27.00(cm)  <br />'  # noqa
        }

    @classmethod
    def efacil_sku_200298(cls):
        return {
            'grade': 10,
            'sold_count': 0,
            'description': 'Fritadeira Sem Oleo Air Fryer <br />Ficha Técnica <br />Características do Produto:<br/>Produto: Air Fryer Inox RED Premium<br/>Capacidade: 3,2 Litros<br/>Modelo: AF-14<br/>Potência (em Watts): 1500W<br/>Consumo (em Kilowatts por hora): 1,50Kw/h<br/>Cor: Vermelho/Inox<br/><br/>Dimensões:<br/>Dimensões do produto sem embalagem (AxLxP em cm): 33 x 35 x 27<br/>Dimensões do produto com a embalagem (AxLxP em cm): 35,5 x 32 x 32<br/><br/>Peso:<br/>Peso líquido unitário: 5,1 Kg<br/>Peso Bruto unitário: 5,79 Kg<br/><br/>Garantia: 1 Ano (Ofertada Pelo Fabricante)<br/><br/>SAC - Fornecedor<br/>Mondial<br/>0800 55 03 93<br/><br/>Ficha Técnica<br/><br/>Fritadeira: Sem Óleo<br/>Garantia: 1 Ano<br/>Selo Inmetro: Sim<br/>Tipo de Selo Inmetro: Segurança<br/>Capacidade: 2.7 Litros',  # noqa
            'ean': '7899882302516',
            'matching_strategy': 'SINGLE_SELLER',
            'release_date': '2018-05-06T14:02:47.815328+00:00',
            'brand': 'Mondial',
            'seller_id': 'efacil',
            'review_score': 0,
            'reference': 'Mondial',
            'categories': [{
                'description': 'Eletroportáteis',
                'id': 'EP',
                'subcategories': [{
                    'description': 'Fritadeira sem óleo (air fryer)',
                    'id': 'EFSO'
                }]
            }],
            'dimensions': {
                'height': 0.36,
                'weight': 5.09,
                'width': 0.32,
                'depth': 0.32
            },
            'last_updated_at': '2018-05-06T14:02:48.416603',
            'updated_at': '2018-03-26T23:33:40.138838+00:00',
            'disable_on_matching': False,
            'md5': '427a46e11284b165136b3f3e39486edc',
            'seller_description': 'eFácil',
            'main_variation': True,
            'type': 'product',
            'sells_to_company': True,
            'navigation_id': '6836352',
            'parent_sku': '200298',
            'created_at': '2018-03-26T23:33:40.123548+00:00',
            'review_count': 0,
            'attributes': [{
                'type': 'voltage',
                'value': '110 Volts'
            }],
            'title': 'Fritadeira Sem Oleo Air Fryer',
            'sku': '200298-102'
        }

    @classmethod
    def mainshop_sku_5643126(cls):
        return {
            'seller_id': 'mainshop',
            'attributes': [],
            'disable_on_matching': False,
            'release_date': '2018-05-07T00:46:33.025416+00:00',
            'reference': '',
            'sku': '346914',
            'review_count': 0,
            'title': 'Fritadeira Elétrica Mondial Air Fryer AF-14 Inox, Vermelha - 110V',  # noqa
            'updated_at': '2017-12-16T01:29:43.825043+00:00',
            'parent_sku': '5643126',
            'grade': 10,
            'dimensions': {
                'depth': 0.32,
                'width': 0.32,
                'height': 0.36,
                'weight': 5.79
            },
            'matching_strategy': 'SINGLE_SELLER',
            'ean': '7899882302516',
            'created_at': '2017-12-08T10:22:44.882305+00:00',
            'description': '<p>Fritadeira Elétrica Mondial Air Fryer AF-14 Inox, Vermelha - 110V<br><br> Possui painel em aço inox e design sofisticado, lâmpadas-piloto que indicam o funcionamento do produto e do aquecimento, controle de temperatura até 200 ºC para a escolha da temperatura ideal de acordo com diferentes tipos de alimentos, cesta removível segura e prática para facilitar o manuseio dos alimentos, timer de 60 minutos com sinal sonoro e desligamento automático, separador de alimentos permitindo o preparo de diferentes alimentos ao mesmo tempo sem misturar o sabor. Com muita praticidade, você pode preparar batatas crocantes em apenas 12 minutos e com o livro de receitas você também pode preparar pão de queijo, carnes, aperitivos, peixes, frango a passarinho, pastéis doces e muito mais.<br> <br> Especificações Técnicas:<br> Marca: Mondial<br> Modelo: AF-14<br> Voltagem: 110V<br> Potência (em Watts): 1500W<br> Consumo (em Kilowatts por hora): 1,50Kw/h<br> Cor: Vermelho/Inox<br> <br> Dimensões:<br> Dimensões do produto sem embalagem (AxLxP em cm): 33 x 35 x 27<br> Dimensões do produto com a embalagem (AxLxP em cm): 35,5 x 32 x 32<br> <br> Peso:<br> Peso líquido unitário: 5,1 Kg<br> Peso Bruto unitário: 5,79 Kg<br><br> Garantia: 12 meses pelo fabricante<br> <br> Itens Inclusos: 01 Fritadeira Mondial Air Fryer AF-14</p>',  # noqa
            'review_score': 0,
            'brand': 'Mondial',
            'navigation_id': '6189785',
            'md5': 'f2a89770d62e0167bdcf87ae76c74934',
            'main_variation': True,
            'seller_description': 'MainShop',
            'last_updated_at': '2018-05-07T00:46:33.835662',
            'categories': [{
                'description': 'Eletroportáteis',
                'subcategories': [{
                    'description': 'Fritadeira Elétrica',
                    'id': 'FREL'
                }],
                'id': 'EP'
            }],
            'sold_count': 0,
            'sells_to_company': True,
            'type': 'product'
        }

    @classmethod
    def mainshop_sku_5643123(cls):
        return {
            'created_at': '2017-12-08T10:22:42.912775+00:00',
            'seller_description': 'MainShop',
            'grade': 10,
            'review_score': 0,
            'matching_strategy': 'SINGLE_SELLER',
            'release_date': '2018-05-07T00:49:42.827963+00:00',
            'md5': 'b474cd448a65e6a4e38dfb11869134f0',
            'brand': 'Mondial',
            'parent_sku': '5643123',
            'main_variation': True,
            'seller_id': 'mainshop',
            'description': '<p>Fritadeira Elétrica Mondial Air Fryer AF-14 Inox, Vermelha - 220V<br><br> Possui painel em aço inox e design sofisticado, lâmpadas-piloto que indicam o funcionamento do produto e do aquecimento, controle de temperatura até 200 ºC para a escolha da temperatura ideal de acordo com diferentes tipos de alimentos, cesta removível segura e prática para facilitar o manuseio dos alimentos, timer de 60 minutos com sinal sonoro e desligamento automático, separador de alimentos permitindo o preparo de diferentes alimentos ao mesmo tempo sem misturar o sabor. Com muita praticidade, você pode preparar batatas crocantes em apenas 12 minutos e com o livro de receitas você também pode preparar pão de queijo, carnes, aperitivos, peixes, frango a passarinho, pastéis doces e muito mais.<br> <br> Especificações Técnicas:<br> Marca: Mondial<br> Modelo: AF-14<br> Voltagem: 220V<br> Potência (em Watts): 1500W<br> Consumo (em Kilowatts por hora): 1,50Kw/h<br> Cor: Vermelho/Inox<br> <br> Dimensões:<br> Dimensões do produto sem embalagem (AxLxP em cm): 33 x 35 x 27<br> Dimensões do produto com a embalagem (AxLxP em cm): 35,5 x 32 x 32<br> <br> Peso:<br> Peso líquido unitário: 5,1 Kg<br> Peso Bruto unitário: 5,79 Kg<br><br> Garantia: 12 meses pelo fabricante<br> <br> Itens Inclusos: 01 Fritadeira Mondial Air Fryer AF-14</p>',  # noqa
            'sku': '346913',
            'title': 'Fritadeira Elétrica Mondial Air Fryer AF-14 Inox, Vermelha - 220V',  # noqa
            'dimensions': {
                'weight': 5.79,
                'height': 0.36,
                'width': 0.32,
                'depth': 0.32
            },
            'last_updated_at': '2018-05-07T00:49:43.859588',
            'reference': '',
            'attributes': [],
            'categories': [{
                'subcategories': [{
                    'id': 'FREL',
                    'description': 'Fritadeira Elétrica'
                }],
                'id': 'EP',
                'description': 'Eletroportáteis'
            }],
            'navigation_id': '6188565',
            'updated_at': '2017-12-16T01:29:27.686286+00:00',
            'ean': '7899882302523',
            'sells_to_company': True,
            'disable_on_matching': False,
            'sold_count': 0,
            'review_count': 0,
            'type': 'product'
        }

    @classmethod
    def gynshop_sku_5643188(cls):
        return {
            'seller_id': 'gynshop',
            'attributes': [],
            'disable_on_matching': False,
            'release_date': '2018-05-07T01:04:14.544650+00:00',
            'reference': '',
            'sku': '346914',
            'review_count': 0,
            'title': 'Fritadeira Elétrica Mondial Air Fryer AF-14 Inox, Vermelha - 110V',  # noqa
            'updated_at': '2017-12-16T02:22:40.820469+00:00',
            'parent_sku': '5643188',
            'grade': 10,
            'dimensions': {
                'depth': 0.32,
                'width': 0.32,
                'height': 0.36,
                'weight': 5.79
            },
            'matching_strategy': 'SINGLE_SELLER',
            'ean': '7899882302516',
            'created_at': '2017-12-08T06:01:03.466244+00:00',
            'description': '<p>Fritadeira Elétrica Mondial Air Fryer AF-14 Inox, Vermelha - 110V<br><br> Possui painel em aço inox e design sofisticado, lâmpadas-piloto que indicam o funcionamento do produto e do aquecimento, controle de temperatura até 200 ºC para a escolha da temperatura ideal de acordo com diferentes tipos de alimentos, cesta removível segura e prática para facilitar o manuseio dos alimentos, timer de 60 minutos com sinal sonoro e desligamento automático, separador de alimentos permitindo o preparo de diferentes alimentos ao mesmo tempo sem misturar o sabor. Com muita praticidade, você pode preparar batatas crocantes em apenas 12 minutos e com o livro de receitas você também pode preparar pão de queijo, carnes, aperitivos, peixes, frango a passarinho, pastéis doces e muito mais.<br> <br> Especificações Técnicas:<br> Marca: Mondial<br> Modelo: AF-14<br> Voltagem: 110V<br> Potência (em Watts): 1500W<br> Consumo (em Kilowatts por hora): 1,50Kw/h<br> Cor: Vermelho/Inox<br> <br> Dimensões:<br> Dimensões do produto sem embalagem (AxLxP em cm): 33 x 35 x 27<br> Dimensões do produto com a embalagem (AxLxP em cm): 35,5 x 32 x 32<br> <br> Peso:<br> Peso líquido unitário: 5,1 Kg<br> Peso Bruto unitário: 5,79 Kg<br><br> Garantia: 12 meses pelo fabricante<br> <br> Itens Inclusos: 01 Fritadeira Mondial Air Fryer AF-14</p>',  # noqa
            'review_score': 0,
            'brand': 'Mondial',
            'navigation_id': '6524992',
            'md5': 'bb501ce721ddc426c10d71922ff663bc',
            'main_variation': True,
            'seller_description': 'Gyn Shop',
            'last_updated_at': '2018-05-07T01:04:15.423315',
            'categories': [{
                'description': 'Eletroportáteis',
                'subcategories': [{
                    'description': 'Fritadeira Elétrica',
                    'id': 'FREL'
                }],
                'id': 'EP'
            }],
            'sold_count': 0,
            'sells_to_company': True,
            'type': 'product'
        }

    @classmethod
    def gynshop_sku_5643191(cls):
        return {
            'created_at': '2017-12-08T06:01:01.825632+00:00',
            'seller_description': 'Gyn Shop',
            'grade': 10,
            'review_score': 0,
            'matching_strategy': 'SINGLE_SELLER',
            'release_date': '2018-05-07T01:01:03.743607+00:00',
            'md5': 'e97b6b30faabe5f3ffbcdcc48190e4f3',
            'brand': 'Mondial',
            'parent_sku': '5643191',
            'main_variation': True,
            'seller_id': 'gynshop',
            'description': '<p>Fritadeira Elétrica Mondial Air Fryer AF-14 Inox, Vermelha - 220V<br><br> Possui painel em aço inox e design sofisticado, lâmpadas-piloto que indicam o funcionamento do produto e do aquecimento, controle de temperatura até 200 ºC para a escolha da temperatura ideal de acordo com diferentes tipos de alimentos, cesta removível segura e prática para facilitar o manuseio dos alimentos, timer de 60 minutos com sinal sonoro e desligamento automático, separador de alimentos permitindo o preparo de diferentes alimentos ao mesmo tempo sem misturar o sabor. Com muita praticidade, você pode preparar batatas crocantes em apenas 12 minutos e com o livro de receitas você também pode preparar pão de queijo, carnes, aperitivos, peixes, frango a passarinho, pastéis doces e muito mais.<br> <br> Especificações Técnicas:<br> Marca: Mondial<br> Modelo: AF-14<br> Voltagem: 220V<br> Potência (em Watts): 1500W<br> Consumo (em Kilowatts por hora): 1,50Kw/h<br> Cor: Vermelho/Inox<br> <br> Dimensões:<br> Dimensões do produto sem embalagem (AxLxP em cm): 33 x 35 x 27<br> Dimensões do produto com a embalagem (AxLxP em cm): 35,5 x 32 x 32<br> <br> Peso:<br> Peso líquido unitário: 5,1 Kg<br> Peso Bruto unitário: 5,79 Kg<br><br> Garantia: 12 meses pelo fabricante<br> <br> Itens Inclusos: 01 Fritadeira Mondial Air Fryer AF-14</p>',  # noqa
            'sku': '346913',
            'title': 'Fritadeira Elétrica Mondial Air Fryer AF-14 Inox, Vermelha - 220V',  # noqa
            'dimensions': {
                'weight': 5.79,
                'height': 0.36,
                'width': 0.32,
                'depth': 0.32
            },
            'last_updated_at': '2018-05-07T01:01:04.264677',
            'reference': '',
            'attributes': [],
            'categories': [{
                'subcategories': [{
                    'id': 'FREL',
                    'description': 'Fritadeira Elétrica'
                }],
                'id': 'EP',
                'description': 'Eletroportáteis'
            }],
            'navigation_id': '6663080',
            'updated_at': '2017-12-16T01:16:46.576013+00:00',
            'ean': '7899882302523',
            'sells_to_company': True,
            'disable_on_matching': False,
            'sold_count': 0,
            'review_count': 0,
            'type': 'product'
        }

    @classmethod
    def efacil_sku_185402(cls):
        return {
            'release_date': '2018-04-30T14:01:27.116688+00:00',
            'created_at': '2018-03-26T23:33:36.713044+00:00',
            'attributes': [],
            'sold_count': 0,
            'parent_sku': '185402',
            'review_count': 0,
            'main_variation': True,
            'type': 'product',
            'sku': '185402',
            'seller_description': 'eFácil',
            'ean': '7899882302523',
            'brand': 'Mondial',
            'review_score': 0,
            'seller_id': 'efacil',
            'navigation_id': '6841431',
            'disable_on_matching': False,
            'categories': [{
                'description': 'Eletroportáteis',
                'id': 'EP',
                'subcategories': [{
                    'description': 'Fritadeira Elétrica',
                    'id': 'FREL'
                }]
            }],
            'md5': 'df452d22031fba0d0735d7a8ba5d884d',
            'updated_at': '2018-03-26T23:33:36.732696+00:00',
            'matching_strategy': 'SINGLE_SELLER',
            'sells_to_company': True,
            'dimensions': {
                'height': 0.36,
                'weight': 5.79,
                'width': 0.32,
                'depth': 0.32
            },
            'title': 'Fritadeira Air Fryer AF-14 Inox Vermelha 220V - Mondial',  # noqa
            'description': '<p>  Características do Produto:<br  />  Produto: Air Fryer Inox RED Premium<br  />  Modelo: AF-14<br  />  Potência (em Watts): 1500W<br  />  Consumo (em Kilowatts por hora): 1,50Kw/h<br  />  Cor: Vermelho/Inox<br  />  <br  />  Dimensões:<br  />  Dimensões do produto sem embalagem (AxLxP em cm): 33 x 35 x 27<br  />  Dimensões do produto com a embalagem (AxLxP em cm): 35,5 x 32 x 32<br  />  <br  />  Garantia: 1 Ano (Ofertada Pelo Fabricante)<br  />  <br  />  SAC - Fornecedor<br  />  Mondial<br  />  0800 55 03 93</p> <br />Ficha Técnica <br />Características do Produto:<br/>Produto: Air Fryer Inox RED Premium<br/>Modelo: AF-14<br/>Potência (em Watts): 1500W<br/>Consumo (em Kilowatts por hora): 1,50Kw/h<br/>Cor: Vermelho/Inox<br/><br/>Dimensões:<br/>Dimensões do produto sem embalagem (AxLxP em cm): 33 x 35 x 27<br/>Dimensões do produto com a embalagem (AxLxP em cm): 35,5 x 32 x 32<br/><br/>Peso:<br/>Peso líquido unitário: 5,1 Kg<br/>Peso Bruto unitário: 5,79 Kg<br/><br/>Garantia: 1 Ano (Ofertada Pelo Fabricante)<br/><br/>SAC - Fornecedor<br/>Mondial<br/>0800 55 03 93<br/>',  # noqa
            'grade': 10,
            'reference': '',
            'last_updated_at': '2018-04-30T14:01:27.642976'
        }

    @classmethod
    def casa_e_video_sku_10359(cls):
        return {
            'last_updated_at': '2018-05-05T01:12:08.005088',
            'brand': 'Mondial',
            'title': 'Fritadeira sem Óleo Mondial com Timer Air Fryer Family Inox Vermelha 127V',  # noqa
            'seller_description': 'Casa & Video',
            'disable_on_matching': False,
            'parent_sku': '10359',
            'type': 'product',
            'matching_strategy': 'SINGLE_SELLER',
            'sold_count': 0,
            'navigation_id': '7486857',
            'reference': '',
            'description': 'Saúde em primeiro lugar até na hora das refeições. Esta fritadeira modelo Air Fryer funciona sem óleo, deixando os alimentos sequinhos e saborosos, como você gosta. Tem potência de 1500W , capacidade para 2,7 litros, seletor de temperatura, de acordo com o alimento que será preparado e timer com alarme e desligamento automático. Sua cuba antiaderente evita que os alimentos fiquem grudados, facilitando na hora de servir e ainda é desmontável, facilitando na hora de guardar dentro do armário.',  # noqa
            'sku': '10099',
            'review_score': 0,
            'ean': '7899882302516',
            'md5': 'd9b4b29c79affccba155eca7936a3b74',
            'updated_at': '2018-01-05T00:01:58.098294+00:00',
            'grade': 20,
            'sells_to_company': True,
            'release_date': '2018-05-05T01:12:06.844313+00:00',
            'dimensions': {
                'depth': 0.33,
                'height': 0.36,
                'width': 0.36,
                'weight': 4.98
            },
            'main_variation': True,
            'created_at': '2017-08-11T22:41:54.456603+00:00',
            'categories': [{
                'id': 'EP',
                'subcategories': [{
                    'id': 'FREL',
                    'description': 'Fritadeira Elétrica'
                }],
                'description': 'Eletroportáteis'
            }],
            'attributes': [{
                'value': '110 Volts',
                'type': 'voltage'
            }],
            'review_count': 0,
            'seller_id': 'casa-e-video'
        }

    @classmethod
    def topbrinquedos_sku_1964(cls):
        return {
            'type': 'product',
            'ean': '7899882302523',
            'dimensions': {
                'height': 0.33,
                'depth': 0.27,
                'weight': 5.8,
                'width': 0.35
            },
            'review_score': 0,
            'main_variation': True,
            'review_count': 0,
            'created_at': '2018-03-24T14:36:04.329384+00:00',
            'sold_count': 0,
            'sku': '1964',
            'seller_id': 'topbrinquedos',
            'last_updated_at': '2018-04-30T23:18:16.934319',
            'md5': '6957fef210dd9dac68f687f6a5f93034',
            'matching_strategy': 'SINGLE_SELLER',
            'brand': 'Mondial',
            'categories': [{
                'description': 'Eletroportáteis',
                'id': 'EP',
                'subcategories': [{
                    'description': 'Fritadera a óleo',
                    'id': 'EFAO'
                }]
            }],
            'grade': 10,
            'disable_on_matching': True,
            'title': 'Air Fryer Inox RED Premium 220V - Mondial AF-14',
            'updated_at': '2018-03-24T14:36:04.342843+00:00',
            'description': '<br/> <br/>        Assa, tosta, cozinha, gratina por convecção a ar   Controle de temperatura até 200ºC   Capacidade de até 2,7 L no cesto de alimentos   Capacidade total de até 4L           Modelo: Air Fryer Inox RED   Cor: Preto/Inox   Potência: 1500W   Consumo: 1,5Kw/h   Origem: Importado   Garantia: 12 meses         <b>Dados do produto</b> <br /> Garantia: 90(dias) <br />  Marca: Mondial<br />  NCM: 85167920<br />  EAN: 7899882302523<br /><br /> <b>Dados de Embalagem</b> <br /> Peso Total (Produto + Embalagem): 5800.00(gr)  <br />  Altura: 33.00(cm)  <br />  Largura: 35.00(cm)  <br />  Profundidade: 27.00(cm)  <br />  <br>       01 Mondial Air Fryer,    Manual de Assistência Técnica,    Manual de Instruções',  # noqa
            'navigation_id': '6686757',
            'release_date': '2018-04-30T23:18:16.288050+00:00',
            'reference': '',
            'seller_description': 'Top Brinquedos',
            'parent_sku': '1964',
            'sells_to_company': True,
            'attributes': []
        }

    @classmethod
    def amplocomercial_sku_232(cls):
        return {
            'title': 'Air Fryer Inox RED Premium 220V - Mondial AF-14',
            'sku': '232',
            'dimensions': {
                'depth': 0.27,
                'width': 0.35,
                'height': 0.33,
                'weight': 5.8
            },
            'reference': '',
            'sold_count': 0,
            'last_updated_at': '2018-04-21T15:52:04.375515',
            'navigation_id': '6168966',
            'ean': '7899882302523',
            'seller_description': 'Amplo Comercial',
            'matching_strategy': 'SINGLE_SELLER',
            'release_date': '2018-04-21T15:52:03.504514+00:00',
            'description': 'Assa, tosta, cozinha, gratina por convecção a ar  Controle de temperatura até 200ºC  Capacidade de até 2,7 L no cesto de alimentos  Capacidade total de até 4L     <br>  </p><p>  Descrição T&eacutecnica: <br> </p><p>    Modelo: Air Fryer Inox RED  Potência: 1500W  Consumo: 1,5Kw/h  Origem: Importado  Garantia: 12 meses    </p><p> Itens Inclusos: </p><p>   01 Mondial Air Fryer,   Manual de Assistência Técnica,   Manual de Instruções   </p><p> <b>Dados do produto</b> <br /> Garantia: 90(dias) <br />  Marca: Mondial<br />  NCM: 85167920<br />  EAN: 7899882302523<br /><br /> <b>Dados de Embalagem</b> <br /> Peso Total (Produto + Embalagem): 5800.00(gr)  <br />  Altura: 33.00(cm)  <br />  Largura: 35.00(cm)  <br />  Profundidade: 27.00(cm)  <br />',  # noqa
            'parent_sku': '232',
            'review_score': 0,
            'type': 'product',
            'seller_id': 'amplocomercial',
            'created_at': '2018-03-10T18:21:25.442875+00:00',
            'md5': 'fddb78cc0c184aad413c1ac018361fe1',
            'sells_to_company': True,
            'review_count': 0,
            'disable_on_matching': True,
            'attributes': [],
            'categories': [{
                'subcategories': [{
                    'description': 'Fritadeira sem óleo (air fryer)',
                    'id': 'EFSO'
                }],
                'description': 'Eletroportáteis',
                'id': 'EP'
            }],
            'grade': 10,
            'brand': 'Mondial',
            'main_variation': True,
            'updated_at': '2018-03-10T18:21:25.455087+00:00'
        }

    @classmethod
    def lojasmel_openapi_45035(cls):
        return {
            'type': 'product',
            'reference': '',
            'ean': '6902442351273',
            'seller_description': 'Lojas Mel',
            'sells_to_company': True,
            'brand': 'Zeex',
            'created_at': '2017-04-05T20:53:11.691286+00:00',
            'dimensions': {
                'width': 0.35,
                'height': 0.34,
                'depth': 0.35,
                'weight': 1.19
            },
            'release_date': '2018-03-07T00:12:39.485893+00:00',
            'attributes': [],
            'review_score': 0,
            'parent_sku': '2380',
            'navigation_id': '7908856',
            'grade': 10,
            'description': 'A Fritadeira Elétrica Frit Fast da ZEEX, é compacta com design moderno e prático. É fácil de montar, possui suporte e é perfeita para a sua cozinha, pois frita batatas, frutos do mar, cebolas, aves e ainda faz fondue de carne.<br> Possui cesta removível em aço inox, recipiente para óleo com revestimento antiaderente e capacidade de 1 litro. <br>Permite preparar o alimento com a tampa fechada evitando respingos de gorduras, deixando sua cozinha sempre limpa. Possui indicador luminoso para aquecimento e controle de temperatura com seletor de 80°C a 190°C e quando o óleo atinge a temperatura selecionada, a luz apaga automaticamente.<br>     Dimensões aproximadas do produto (cm) AxLxP  30 x 25 x 28    Peso do produto  1,085 kg    Dimensões aproximadas da embalagem (cm) AxLxP  47 x 24 x 69    Peso da embalagem  1,185 kg    Garantia  90 dias contra defeitos de fabricação    Código do Fornecedor  FT235110    Site      Telefone  0800 644 5005    E-mail',  # noqa
            'title': 'Fritadeira Frit Fast 110v Ref.FT235110 Zeex',
            'sold_count': 0,
            'disable_on_matching': False,
            'categories': [{
                'id': 'EP',
                'subcategories': [{
                    'id': 'OTEP',
                    'description': 'Outros Eletroportáteis'
                }],
                'description': 'Eletroportáteis'
            }],
            'sku': '45035',
            'seller_id': 'lojasmel-openapi',
            'md5': 'd57ad1d86b4172d432cb8552cbcfdd8e',
            'updated_at': '2018-01-05T06:01:16.628951+00:00',
            'matching_strategy': 'SINGLE_SELLER',
            'review_count': 0,
            'main_variation': True
        }

    @classmethod
    def colormaq_sku_1408001_1(cls):
        return {
            'seller_description': 'Colormaq',
            'ean': '7897016826723',
            'review_count': 0,
            'created_at': '2018-04-11T13:01:40.989273+00:00',
            'parent_sku': '550',
            'matching_strategy': 'OMNILOGIC',
            'brand': 'Colormaq',
            'release_date': '2018-05-22T14:38:12.141737+00:00',
            'updated_at': '2018-04-11T13:01:41.002178+00:00',
            'last_updated_at': '2018-05-22T14:38:13.156947',
            'categories': [{
                'id': 'EP',
                'subcategories': [{
                    'id': 'EFSO',
                    'description': 'Fritadeira sem óleo (air fryer)'
                }, {
                    'id': 'FREL'
                }],
                'description': 'Eletroportáteis'
            }],
            'disable_on_matching': False,
            'title': 'Fritadeira Elétrica Air Fryer Colormaq Preto 3,6L',
            'main_variation': True,
            'navigation_id': '6712039',
            'grade': 10,
            'type': 'product',
            'attributes': [{
                'type': 'voltage',
                'value': '110 Volts'
            }],
            'review_score': 0,
            'reference': '',
            'sku': '1408001-1',
            'seller_id': 'colormaq',
            'description': 'A Air Fryer Colormaq pode fazer vários pratos gostosos sem usar óleo. Além de alimentos que normalmente são feitos com fritura, esse modelo também pode preparar comidas assadas e cozidas.             É só escolher a temperatura!    A Air Fryer Colormaq tem ajuste de temperatura até 200º, além de timer de até 60 minutos com desligamento automático, então nada de queimar a comida. As luzes indicadoras do aparelho garantem que você saiba que está tudo da maneira que precisa para fazer cada tipo de alimento.         Vários pratos, sem óleo.    Com ela você prepara vários pratos sem usar óleo e não fica aquele cheiro de gordura e fumaça na cozinha. O cesto removível de 3,6 litros é antiaderente, durável e fácil de limpar. Outro ponto legal deste modelo é o separador de alimentos que abre a possibilidade de preparar mais de um alimento ao mesmo tempo.                 BATATA CONGELADA   200ºC   12 - 16 min.        Peixe   200ºC   15 - 20 min.        Nuggets   200ºC   15 - 20 min.        Frango   180ºC   15 - 22 min.        Carne   180ºC   8 - 14 min.        Pão de queijo   180ºC   5 - 8 min.        Cupcake   200ºC   15 - 18 min.',  # noqa
            'sold_count': 0,
            'dimensions': {
                'height': 0.37,
                'width': 0.32,
                'depth': 0.32,
                'weight': 5.5
            },
            'md5': '49711a805beebe762f57ac599c3a41b6',
            'sells_to_company': True
        }

    @classmethod
    def colormaq_sku_1408002(cls):
        return {
            'seller_description': 'Colormaq',
            'categories': [{
                'id': 'EP',
                'subcategories': [{
                    'id': 'EFSO',
                    'description': 'Fritadeira sem óleo (air fryer)'
                }, {
                    'id': 'FREL'
                }],
                'description': 'Eletroportáteis'
            }],
            'description': 'A Air Fryer Colormaq pode fazer vários pratos gostosos sem usar óleo. Além de alimentos que normalmente são feitos com fritura, esse modelo também pode preparar comidas assadas e cozidas.             É só escolher a temperatura!    A Air Fryer Colormaq tem ajuste de temperatura até 200º, além de timer de até 60 minutos com desligamento automático, então nada de queimar a comida. As luzes indicadoras do aparelho garantem que você saiba que está tudo da maneira que precisa para fazer cada tipo de alimento.         Vários pratos, sem óleo.    Com ela você prepara vários pratos sem usar óleo e não fica aquele cheiro de gordura e fumaça na cozinha. O cesto removível de 3,6 litros é antiaderente, durável e fácil de limpar. Outro ponto legal deste modelo é o separador de alimentos que abre a possibilidade de preparar mais de um alimento ao mesmo tempo.                 BATATA CONGELADA   200ºC   12 - 16 min.        Peixe   200ºC   15 - 20 min.        Nuggets   200ºC   15 - 20 min.        Frango   180ºC   15 - 22 min.        Carne   180ºC   8 - 14 min.        Pão de queijo   180ºC   5 - 8 min.        Cupcake   200ºC   15 - 18 min.',  # noqa
            'matching_strategy': 'OMNILOGIC',
            'parent_sku': '550',
            'brand': 'Colormaq',
            'review_score': 0,
            'updated_at': '2018-04-11T13:01:41.002178+00:00',
            'md5': '8c53ee6b6023cae6c80d0a0585fa4f59',
            'last_updated_at': '2018-05-22T15:01:04.015872',
            'ean': '7897016826723',
            'disable_on_matching': False,
            'title': 'Fritadeira Elétrica Air Fryer Colormaq Preto 3,6L',
            'main_variation': False,
            'navigation_id': '6158329',
            'release_date': '2018-05-22T15:01:02.454218+00:00',
            'grade': 10,
            'type': 'product',
            'created_at': '2018-04-11T13:01:40.989273+00:00',
            'reference': '',
            'sku': '1408002',
            'seller_id': 'colormaq',
            'attributes': [{
                'type': 'voltage',
                'value': '220 Volts'
            }],
            'sold_count': 0,
            'dimensions': {
                'depth': 0.32,
                'width': 0.32,
                'height': 0.37,
                'weight': 5.5
            },
            'review_count': 0,
            'sells_to_company': True
        }

    @classmethod
    def maniavirtual_sku_9022086_01(cls):
        return {
            'seller_id': 'maniavirtual',
            'sold_count': 0,
            'seller_description': 'Mania Virtual',
            'last_updated_at': '2018-07-05T22:36:18.754033',
            'review_count': 0,
            'source': 'magalu',
            'reference': '',
            'offer_title': 'Torradeira Tosta Pane Britânia com 7 Opções de Tostagem - Vermelha - 220V - Philco',  # noqa
            'sells_to_company': True,
            'md5': '59ed985d55490d844ac9d2a4e12cbe66',
            'main_variation': True,
            'created_at': '2018-04-03T15:15:27.042662+00:00',
            'title': 'Torradeira Britânia Vermelha Tosta Pane 7 Níveis de Tostagem',  # noqa
            'parent_sku': '9022086',
            'disable_on_matching': False,
            'grade': 20,
            'release_date': '2018-07-05T22:36:17.858861+00:00',
            'categories': [{
                'id': 'EP',
                'description': 'Eletroportáteis',
                'subcategories': [{
                    'description': 'Torradeira',
                    'id': 'TOST'
                }, {
                    'id': 'TOST'
                }]
            }],
            'product_hash': '0d9a74a782ae7f4141befd08915d2cab',
            'type': 'product',
            'ean': '7891356067143',
            'dimensions': {
                'depth': 0.28,
                'weight': 1,
                'width': 0.17,
                'height': 0.16
            },
            'matching_strategy': 'OMNILOGIC',
            'updated_at': '2018-07-05T22:34:13.220893+00:00',
            'navigation_id': '6933227',
            'description': 'Prepara 2 fatias<br />Características Gerais - Funções: descongelar, reaquecer, cancelar <br />- 7 níveis de Tostagem  <br />- Capacidade para 2 torradas <br />- Pés antiderrapantes <br />- Com porta fio para facilitar o armazenamento <br />- Luz indicadora de funcionamento <br />- Coletor de migalhas removível <br />- Composição plástico e metal <br />- Disponível em 110v e 220v (não é um produto bivolt)<br />Permite ejeção manual sim<br />Aquecedor de pão sim<br />Descongela pão sim<br />Bandeja para resíduos sim<br />Lâmpada piloto sim<br />Porta-fio sim<br />Especificações Técnicas<br /><br />Consumo de energia (kW/h) 0,8 kW/h<br />Níveis de potência 7<br />Cor Vermelho<br />Potência (W) 800W<br />Tensão/Voltagem 220V<br />Conteúdo da Embalagem - 1 Torradeira Tosta Pane Britânia com 7 Opções de Tostagem - Vermelha <br />- Manual de Instruções<br />Garantia 12 meses<br />Observações Imagens meramente ilustrativas.',  # noqa
            'sku': '9022086-01',
            'brand': 'Britânia',
            'attributes': [{
                'value': '220 Volts',
                'type': 'voltage'
            }],
            'review_score': 0
        }

    @classmethod
    def maniavirtual_sku_9022085_01(cls):
        return {
            'grade': 20,
            'created_at': '2018-04-03T15:14:25.243277+00:00',
            'offer_title': 'Torradeira Tosta Pane Britânia com 7 Opções de Tostagem - Vermelha - 110V - Philco',  # noqa
            'title': 'Torradeira Britânia Vermelha Tosta Pane 7 Níveis de Tostagem',  # noqa
            'updated_at': '2018-07-05T22:34:38.614642+00:00',
            'brand': 'Britânia',
            'review_score': 0,
            'main_variation': True,
            'dimensions': {
                'depth': 0.28,
                'height': 0.16,
                'width': 0.17,
                'weight': 1
            },
            'sells_to_company': True,
            'attributes': [{
                'type': 'voltage',
                'value': '110 Volts'
            }],
            'sold_count': 0,
            'source': 'magalu',
            'reference': '',
            'parent_sku': '9022085',
            'sku': '9022085-01',
            'type': 'product',
            'description': 'Prepara 2 fatias<br />Características Gerais - Funções: descongelar, reaquecer, cancelar <br />- 7 níveis de Tostagem <br />- Capacidade para 2 torradas <br />- Pés antiderrapantes <br />- Com porta fio para facilitar o armazenamento <br />- Luz indicadora de funcionamento <br />- Coletor de migalhas removível <br />- Composição plástico e metal <br />- Disponível em 110v e 220v (não é um produto bivolt)<br />Permite ejeção manual sim<br />Aquecedor de pão sim<br />Descongela pão sim<br />Bandeja para resíduos sim<br />Lâmpada piloto sim<br />Porta-fio sim<br />Especificações Técnicas<br /><br />Consumo de energia (kW/h) 0,8 kW/h<br />Níveis de potência 7<br />Cor Vermelho<br />Potência (W) 800W<br />Tensão/Voltagem 110V<br />Conteúdo da Embalagem - 1 Torradeira Tosta Pane Britânia com 7 Opções de Tostagem - Vermelha <br />- Manual de Instruções<br />Garantia 12 meses<br />Observações Imagens meramente ilustrativas.',  # noqa
            'seller_description': 'Mania Virtual',
            'matching_strategy': 'OMNILOGIC',
            'last_updated_at': '2018-07-05T22:37:07.729964',
            'product_hash': '0d9a74a782ae7f4141befd08915d2cab',
            'ean': '7891356067136',
            'release_date': '2018-07-05T22:37:06.746083+00:00',
            'categories': [{
                'id': 'EP',
                'description': 'Eletroportáteis',
                'subcategories': [{
                    'id': 'TOST',
                    'description': 'Torradeira'
                }, {
                    'id': 'TOST'
                }]
            }],
            'seller_id': 'maniavirtual',
            'disable_on_matching': False,
            'review_count': 0,
            'md5': '601b6a44a425c558da25e85cfdd84587',
            'navigation_id': '6923118'
        }

    @classmethod
    def casa_e_video_sku_8186(cls):
        return {
            'release_date': '2018-07-09T17:59:09.068024+00:00',
            'dimensions': {
                'depth': 0.21,
                'width': 0.32,
                'weight': 1.41,
                'height': 0.2
            },
            'attributes': [{
                'type': 'voltage',
                'value': '110 Volts'
            }],
            'matching_strategy': 'OMNILOGIC',
            'created_at': '2017-07-19T21:00:21.306309+00:00',
            'md5': '665481f6badaf0d3a462215beb44ff80',
            'sold_count': 0,
            'source': 'magalu',
            'parent_sku': '7958',
            'main_variation': True,
            'updated_at': '2018-07-05T22:35:19.908848+00:00',
            'ean': '7891356067136',
            'type': 'product',
            'grade': 20,
            'brand': 'Britânia',
            'review_count': 0,
            'review_score': 0,
            'reference': '',
            'offer_title': 'Torradeira com 7 Níveis de Temperatura Britânia Tosta Pane Vermelha 127V',  # noqa
            'categories': [{
                'description': 'Eletroportáteis',
                'id': 'EP',
                'subcategories': [{
                    'description': 'Eletroportáteis para Cozinha',
                    'id': 'ELCO'
                }, {
                    'description': 'Eletroportáteis para Cozinha',
                    'id': 'ELCO'
                }, {
                    'id': 'TOST'
                }]
            }],
            'seller_description': 'Casa & Video',
            'last_updated_at': '2018-07-09T17:59:10.090816',
            'sells_to_company': True,
            'seller_id': 'casa-e-video',
            'title': 'Torradeira Britânia Vermelha Tosta Pane 7 Níveis de Tostagem',  # noqa
            'product_hash': '0d9a74a782ae7f4141befd08915d2cab',
            'description': 'Design aliado a praticidade. Esta bela torradeira vai fazer o seu café da manhã ser mais completo. Apresenta 7 níveis de intensidade, botão para descongelamento do pão e reaquecimento do mesmo, podendo saboreá-lo quentinho. Possui bocal ajustável ao tamanho do pão, botão cancelar e coletor de migalhas removível, deixando o aparelho limpo, conservando-o por mais tempo. Perfeita para quem gosta de deixar seu café da manhã ou lanche da tarde completo.',  # noqa
            'disable_on_matching': False,
            'sku': '8186',
            'navigation_id': '7539762'
        }

    @classmethod
    def magazineluiza_sku_217148200(cls):
        return {
            'categories': [{
                'subcategories': [{
                    'id': 'TOST'
                }, {
                    'id': 'ELCA'
                }],
                'id': 'EP'
            }],
            'matching_strategy': 'OMNILOGIC',
            'product_hash': '0d9a74a782ae7f4141befd08915d2cab',
            'attributes': [{
                'type': 'voltage',
                'value': '220 Volts'
            }],
            'source': 'magalu',
            'sold_count': 0,
            'md5': '8fe287e67d5c97044dc69dbc19397a0c',
            'offer_title': 'Torradeira Britânia Vermelha Tosta Pane - 7 Níves de Tostagem',  # noqa
            'selections': {
                '12966': ['16734', '16737'],
                '0': ['17637', '22013', '22297', '7041', '7291']
            },
            'main_category': {
                'subcategory': {
                    'id': 'TOST'
                },
                'id': 'EP'
            },
            'sells_to_company': True,
            'description': 'Agora seus pães irão ficar ainda mais saborosos com a torradeira Tosta Pane Britânia. Pão quentinho, crocante e sem complicação na hora. Com sete níveis para tostar, você pode escolher o que é melhor para cada pão. A bandeja anti resíduos pode ser lavado mantendo assim seu produto e ambiente limpo. E você tem a opção descongelar e reaquecer. É ou não é uma torradeira multiuso?',  # noqa
            'title': 'Torradeira Britânia Vermelha Tosta Pane',
            'review_count': 0,
            'main_variation': False,
            'reference': '7 Níves de Tostagem',
            'grade': 10,
            'seller_id': 'magazineluiza',
            'type': 'product',
            'updated_at': '2018-06-09T17:49:45.520000',
            'brand': 'Britânia',
            'sku': '217148200',
            'review_score': 0,
            'parent_sku': '2171481',
            'last_updated_at': '2018-07-11T12:06:23.017212',
            'seller_description': 'Magazine Luiza',
            'created_at': '2017-01-25T07:50:32.557000',
            'navigation_id': '217148200',
            'ean': '7891356067143',
            'disable_on_matching': False,
            'dimensions': {
                'height': 0.2,
                'depth': 0.21,
                'weight': 1.25,
                'width': 0.32
            }
        }

    @classmethod
    def madeiramadeira_openapi_sku_302110(cls):
        return {
            'seller_id': 'madeiramadeira-openapi',
            'created_at': '2018-06-01T20:35:50.798658+00:00',
            'grade': 10,
            'offer_title': 'Torradeira Tosta Pane Vermelha 800W Britânia 127V',
            'matching_strategy': 'OMNILOGIC',
            'source': 'magalu',
            'review_score': 0,
            'categories': [{
                'id': 'EP',
                'subcategories': [{
                    'id': 'TOST',
                    'description': 'Torradeira'
                }, {
                    'id': 'TOST'
                }],
                'description': 'Eletroportáteis'
            }],
            'release_date': '2018-07-06T03:36:03.832549+00:00',
            'review_count': 0,
            'sku': '302110',
            'attributes': [{
                'value': '110 Volts',
                'type': 'voltage'
            }],
            'product_hash': '0d9a74a782ae7f4141befd08915d2cab',
            'sells_to_company': True,
            'sold_count': 0,
            'disable_on_matching': False,
            'seller_description': 'Madeira Madeira',
            'title': 'Torradeira Britânia Vermelha Tosta Pane 7 Níveis de Tostagem',  # noqa
            'description': 'Com a Torradeira Tostapane Vermelha Britânia não vão faltar torradas gostosas em suas refeições diárias.Ela é multifunções: Reaquece pães já torrados, descongela pães congelados e possui a função cancelar para desligar a qualquer momento.A Bandeja de resíduos retém migalhas de pão que caem durante o preparo das torradas, facilitando a limpeza.Possui 7 níveis de tostagem, permitindo ajustar a intensidade de acordo com sua preferência.A Torradeira Tostapane Vermelha Britânia garante torradas gostosas, a qualquer momento, com a praticidade e conforto que só sua casa oferece!',  # noqa
            'type': 'product',
            'last_updated_at': '2018-07-06T03:36:04.525296',
            'navigation_id': '5794086',
            'parent_sku': '302110',
            'updated_at': '2018-07-05T22:37:09.267302+00:00',
            'ean': '7891356067136',
            'dimensions': {
                'height': 0.2,
                'width': 0.32,
                'weight': 1.25,
                'depth': 0.21
            },
            'main_variation': True,
            'md5': '6c94f5aee8c5ad3e12ff62c64c758ad4',
            'reference': '',
            'brand': 'Britânia'
        }

    @classmethod
    def madeiramadeira_openapi_sku_302117(cls):
        return {
            'sells_to_company': True,
            'main_variation': True,
            'disable_on_matching': False,
            'seller_description': 'Madeira Madeira',
            'seller_id': 'madeiramadeira-openapi',
            'reference': '',
            'type': 'product',
            'title': 'Torradeira Britânia Vermelha Tosta Pane 7 Níveis de Tostagem',  # noqa
            'product_hash': '0d9a74a782ae7f4141befd08915d2cab',
            'ean': '7891356067143',
            'review_score': 0,
            'parent_sku': '302117',
            'brand': 'Britânia',
            'last_updated_at': '2018-07-05T17:53:30.683789',
            'sold_count': 0,
            'sku': '302117',
            'matching_strategy': 'OMNILOGIC',
            'release_date': '2018-07-05T17:53:29.391297+00:00',
            'categories': [{
                'id': 'EP',
                'description': 'Eletroportáteis',
                'subcategories': [{
                    'id': 'TOST',
                    'description': 'Torradeira'
                }, {
                    'id': 'TOST'
                }]
            }],
            'description': 'Com a Torradeira Tostapane Vermelha Britânia não vão faltar torradas gostosas em suas refeições diárias.Ela é multifunções: Reaquece pães já torrados, descongela pães congelados e possui a função cancelar para desligar a qualquer momento.A Bandeja de resíduos retém migalhas de pão que caem durante o preparo das torradas, facilitando a limpeza.Possui 7 níveis de tostagem, permitindo ajustar a intensidade de acordo com sua preferência.A Torradeira Tostapane Vermelha Britânia garante torradas gostosas, a qualquer momento, com a praticidade e conforto que só sua casa oferece!',  # noqa
            'grade': 10,
            'md5': 'f973ffad722e3bfa2c4cba137b8f751c',
            'attributes': [{
                'value': '220 Volts',
                'type': 'voltage'
            }],
            'navigation_id': '5914495',
            'created_at': '2018-06-01T20:35:54.698426+00:00',
            'review_count': 0,
            'source': 'magalu',
            'offer_title': 'Torradeira Tosta Pane Vermelha 800W Britânia 220V',
            'updated_at': '2018-07-04T21:23:51.307602+00:00',
            'dimensions': {
                'width': 0.32,
                'weight': 1.25,
                'depth': 0.21,
                'height': 0.2
            }
        }

    @classmethod
    def magazineluiza_sku_217148100(cls):
        return {
            'sold_count': 0,
            'dimensions': {
                'weight': 1.25,
                'width': 0.32,
                'height': 0.2,
                'depth': 0.21
            },
            'description': 'Agora seus pães irão ficar ainda mais saborosos com a torradeira Tosta Pane Britânia. Pão quentinho, crocante e sem complicação na hora. Com sete níveis para tostar, você pode escolher o que é melhor para cada pão. A bandeja anti resíduos pode ser lavado mantendo assim seu produto e ambiente limpo. E você tem a opção descongelar e reaquecer. É ou não é uma torradeira multiuso?\n\n\n\n\n',  # noqa
            'matching_strategy': 'OMNILOGIC',
            'title': 'Torradeira Britânia Vermelha Tosta Pane',
            'main_variation': True,
            'offer_title': 'Torradeira Britânia Vermelha Tosta Pane - 7 Níves de Tostagem',  # noqa
            'seller_id': 'magazineluiza',
            'md5': 'ce0f829bdac45fa4f9c98364ea6489b1',
            'reference': '7 Níves de Tostagem',
            'updated_at': '2018-05-20T19:52:05.663000',
            'sells_to_company': True,
            'product_hash': '0d9a74a782ae7f4141befd08915d2cab',
            'disable_on_matching': True,
            'created_at': '2017-01-25T07:50:32.557000',
            'review_score': 0,
            'parent_sku': '2171481',
            'type': 'product',
            'ean': '7891356067136',
            'seller_description': 'Magazine Luiza',
            'review_count': 0,
            'main_category': {
                'subcategory': {
                    'id': 'TOST'
                },
                'id': 'EP'
            },
            'last_updated_at': '2018-07-11T12:06:23.059354',
            'source': 'magalu',
            'selections': {
                '0': ['17637', '22013', '22297', '7041', '7291'],
                '12966': ['16734', '16737']
            },
            'attributes': [{
                'value': '110 Volts',
                'type': 'voltage'
            }],
            'grade': 10,
            'categories': [{
                'subcategories': [{
                    'id': 'TOST'
                }, {
                    'id': 'ELCO'
                }],
                'id': 'EP'
            }],
            'navigation_id': '217148100',
            'sku': '217148100',
            'brand': 'Britânia'
        }

    @classmethod
    def havan_sku_2078836(cls):
        return {
            'main_variation': False,
            'sold_count': 0,
            'parent_sku': '2045284',
            'sku': '2078836',
            'updated_at': '2018-07-06T11:13:13.486672+00:00',
            'type': 'product',
            'grade': 10,
            'sells_to_company': True,
            'description': '<br>  Recursos   <br>Funções diferenciais <br>Descongela, reaquece e cancela <br> <br>Multifunções <br>Função Reaquecer: Permite reaquecer pães já torrados <br>Função Descongelar: Descongela e tosta pães congelados <br>Função Cancelar: Permite desligar a qualquer momento <br> <br>7 níveis de tostagem <br>Permite ajustar a intensidade da tostagem conforme preferência <br> <br>Bandeja de resíduos deslizante <br>Facilita a retirada de migalhas de pão que caem durante o preparo das torradas <br> <br>Porta-Fio <br>Fácil de guardar <br> <br>Funções diferenciais <br>Descongela, reaquece e é ajustável para pães espessos <br> <br>  Informações Adicionais   <br>Funções: descongelar, reaquecer, cancelar <br>7 níveis de Tostagem <br>Capacidade para 2 torradas <br>Pés antiderrapantes <br>Luz indicadora de funcionamento <br>Coletor de migalhas removível <br>Porta fio <br>Composição: Plástico e metal <br> <br>  Informações Técnicas   <br>Voltagem: Vendido em 110V e 220V <br>Frequência (Hz): 60 <br>Potência (W): 800 <br>Consumo (kWh): 0,8 <br> <br>  Dimensões e Pesos   <br>Peso Líquido (Kg): 0,96 <br>Peso Bruto (Kg): 1,25 <br>Dimensões do Produto (LxAxP): 172 x 164 x 276 mm <br>Dimensões da Embalagem (LxAxP): 320 x 200 x 210 mm <br> <br>  Observações   <br>Garantia do Fabricante: 1 Ano <br>SAC: 0800 645 8300 <br>Imagem meramente ilustrativa <br>Informações sujeitas a alterações sem aviso prévio',  # noqa
            'reference': '',
            'product_hash': '0d9a74a782ae7f4141befd08915d2cab',
            'dimensions': {
                'height': 0.2,
                'weight': 1.25,
                'depth': 0.21,
                'width': 0.32
            },
            'created_at': '2017-03-03T18:58:41.163279+00:00',
            'disable_on_matching': False,
            'seller_id': 'havan',
            'ean': '7891356067143',
            'brand': 'Britânia',
            'md5': '5086a69471ba5d15ee5dadc61b46309f',
            'release_date': '2018-07-06T11:41:46.675527+00:00',
            'categories': [{
                'subcategories': [{
                    'description': 'Torradeira',
                    'id': 'TOST'
                }, {
                    'description': 'Eletroportáteis para Cozinha',
                    'id': 'ELCO'
                }, {
                    'description': 'Eletroportáteis para Cozinha',
                    'id': 'ELCO'
                }, {
                    'id': 'TOST'
                }],
                'description': 'Eletroportáteis',
                'id': 'EP'
            }],
            'last_updated_at': '2018-07-06T11:42:33.409292',
            'review_count': 0,
            'offer_title': 'Torradeira Tosta Pane Vermelha Multifunções Britânia',  # noqa
            'review_score': 0,
            'matching_strategy': 'OMNILOGIC',
            'attributes': [{
                'value': '220 Volts',
                'type': 'voltage'
            }],
            'navigation_id': '8355943',
            'title': 'Torradeira Britânia Vermelha Tosta Pane 7 Níveis de Tostagem',  # noqa
            'source': 'magalu',
            'seller_description': 'Havan'
        }

    @classmethod
    def havan_sku_2078835(cls):
        return {
            'matching_strategy': 'OMNILOGIC',
            'sku': '2078835',
            'navigation_id': '8283924',
            'title': 'Torradeira Britânia Vermelha Tosta Pane 7 Níveis de Tostagem',  # noqa
            'created_at': '2017-03-03T18:58:41.163279+00:00',
            'description': '<br>  Recursos   <br>Funções diferenciais <br>Descongela, reaquece e cancela <br> <br>Multifunções <br>Função Reaquecer: Permite reaquecer pães já torrados <br>Função Descongelar: Descongela e tosta pães congelados <br>Função Cancelar: Permite desligar a qualquer momento <br> <br>7 níveis de tostagem <br>Permite ajustar a intensidade da tostagem conforme preferência <br> <br>Bandeja de resíduos deslizante <br>Facilita a retirada de migalhas de pão que caem durante o preparo das torradas <br> <br>Porta-Fio <br>Fácil de guardar <br> <br>Funções diferenciais <br>Descongela, reaquece e é ajustável para pães espessos <br> <br>  Informações Adicionais   <br>Funções: descongelar, reaquecer, cancelar <br>7 níveis de Tostagem <br>Capacidade para 2 torradas <br>Pés antiderrapantes <br>Luz indicadora de funcionamento <br>Coletor de migalhas removível <br>Porta fio <br>Composição: Plástico e metal <br> <br>  Informações Técnicas   <br>Voltagem: Vendido em 110V e 220V <br>Frequência (Hz): 60 <br>Potência (W): 800 <br>Consumo (kWh): 0,8 <br> <br>  Dimensões e Pesos   <br>Peso Líquido (Kg): 0,96 <br>Peso Bruto (Kg): 1,25 <br>Dimensões do Produto (LxAxP): 172 x 164 x 276 mm <br>Dimensões da Embalagem (LxAxP): 320 x 200 x 210 mm <br> <br>  Observações   <br>Garantia do Fabricante: 1 Ano <br>SAC: 0800 645 8300 <br>Imagem meramente ilustrativa <br>Informações sujeitas a alterações sem aviso prévio',  # noqa
            'seller_description': 'Havan',
            'review_score': 0,
            'dimensions': {
                'width': 0.32,
                'height': 0.2,
                'depth': 0.21,
                'weight': 1.25
            },
            'attributes': [{
                'value': '110 Volts',
                'type': 'voltage'
            }],
            'disable_on_matching': False,
            'sells_to_company': True,
            'source': 'magalu',
            'offer_title': 'Torradeira Tosta Pane Vermelha Multifunções Britânia',  # noqa
            'type': 'product',
            'md5': 'c4772cf4ac32a752249acef6658fe07a',
            'grade': 10,
            'updated_at': '2018-07-06T11:13:13.486672+00:00',
            'brand': 'Britânia',
            'seller_id': 'havan',
            'ean': '7891356067136',
            'product_hash': '0d9a74a782ae7f4141befd08915d2cab',
            'reference': '',
            'main_variation': True,
            'last_updated_at': '2018-07-06T11:14:40.007127',
            'sold_count': 0,
            'release_date': '2018-07-06T11:14:39.318542+00:00',
            'categories': [{
                'id': 'EP',
                'subcategories': [{
                    'id': 'TOST',
                    'description': 'Torradeira'
                }, {
                    'id': 'ELCO',
                    'description': 'Eletroportáteis para Cozinha'
                }, {
                    'id': 'ELCO',
                    'description': 'Eletroportáteis para Cozinha'
                }, {
                    'id': 'TOST'
                }],
                'description': 'Eletroportáteis'
            }],
            'parent_sku': '2045284',
            'review_count': 0
        }

    @classmethod
    def mundoautomacao_sku_320_257(cls):
        return {
            'seller_id': 'mundoautomacao',
            'type': 'product',
            'ean': '7891356067136',
            'grade': 10,
            'offer_title': 'Torradeira Britânia Tostapane Vermelha 800W',
            'attributes': [{
                'type': 'voltage',
                'value': '110 Volts'
            }],
            'parent_sku': '320',
            'navigation_id': '6921135',
            'created_at': '2018-02-09T20:30:49.444461+00:00',
            'description': 'Na Tostapane Britânia você vai preparar torradas de um jeito prático e rápido<BR>Com a torradeira Tostapane Preta Britânia suas torradas ficam gostosas a qualquer momento, com praticidade, no conforto da sua casa.<BR>Além de torrar pães, com ela você vai descongelar pães, reaquecer pães já torrados e conta também com a função cancelar para desligar a qualquer momento.<BR>Permite ajustar a intensidade de acordo com sua preferência entre 7 diferentes níveis de tostagem. A Bandeja de resíduos facilita a retirada de migalhas de pão que caem durante o preparo das torradas.<BR>Ao comprar torradeira Britânia Tostpane você terá:<BR>• Função para reaquecer pães já torrados;<BR>• Função para descongelar e tostas pães congelados;<BR>• Função cancelar para desligar a qualquer momento;<BR>• 7 níveis de tostagem para ajustar conforme preferência;<BR>• Bandeja de resíduos deslizante para facilitar a retirada de migalhas de pão no preparo das torradas;<BR>• Porta-fios para facilitar o armazenamento, ocupando menos espaço.',  # noqa
            'disable_on_matching': False,
            'release_date': '2018-07-05T22:36:11.743352+00:00',
            'title': 'Torradeira Britânia Vermelha Tosta Pane 7 Níveis de Tostagem',  # noqa
            'md5': 'e18758260003dc38b0a54770f31d08b7',
            'sells_to_company': True,
            'sold_count': 0,
            'dimensions': {
                'weight': 1.7,
                'height': 0.2,
                'width': 0.32,
                'depth': 0.22
            },
            'matching_strategy': 'OMNILOGIC',
            'sku': '320-257',
            'review_count': 0,
            'main_variation': False,
            'reference': '',
            'updated_at': '2018-07-05T22:34:56.544591+00:00',
            'seller_description': 'Mundo Automacao',
            'product_hash': '0d9a74a782ae7f4141befd08915d2cab',
            'categories': [{
                'id': 'EP',
                'subcategories': [{
                    'id': 'TOST',
                    'description': 'Torradeira'
                }, {
                    'id': 'TOST'
                }],
                'description': 'Eletroportáteis'
            }],
            'source': 'magalu',
            'last_updated_at': '2018-07-05T22:36:12.853138',
            'review_score': 0,
            'brand': 'Britânia'
        }

    @classmethod
    def mundoautomacao_sku_320_258(cls):
        return {
            'review_count': 0,
            'main_variation': True,
            'seller_description': 'Mundo Automacao',
            'sku': '320-258',
            'dimensions': {
                'height': 0.2,
                'depth': 0.22,
                'weight': 1.7,
                'width': 0.32
            },
            'review_score': 0,
            'categories': [{
                'subcategories': [{
                    'id': 'TOST',
                    'description': 'Torradeira'
                }, {
                    'id': 'TOST'
                }],
                'id': 'EP',
                'description': 'Eletroportáteis'
            }],
            'disable_on_matching': False,
            'attributes': [{
                'value': '220 Volts',
                'type': 'voltage'
            }],
            'navigation_id': '6150755',
            'description': 'Na Tostapane Britânia você vai preparar torradas de um jeito prático e rápido<BR>Com a torradeira Tostapane Preta Britânia suas torradas ficam gostosas a qualquer momento, com praticidade, no conforto da sua casa.<BR>Além de torrar pães, com ela você vai descongelar pães, reaquecer pães já torrados e conta também com a função cancelar para desligar a qualquer momento.<BR>Permite ajustar a intensidade de acordo com sua preferência entre 7 diferentes níveis de tostagem. A Bandeja de resíduos facilita a retirada de migalhas de pão que caem durante o preparo das torradas.<BR>Ao comprar torradeira Britânia Tostpane você terá:<BR>• Função para reaquecer pães já torrados;<BR>• Função para descongelar e tostas pães congelados;<BR>• Função cancelar para desligar a qualquer momento;<BR>• 7 níveis de tostagem para ajustar conforme preferência;<BR>• Bandeja de resíduos deslizante para facilitar a retirada de migalhas de pão no preparo das torradas;<BR>• Porta-fios para facilitar o armazenamento, ocupando menos espaço.',  # noqa
            'created_at': '2018-02-09T20:30:49.444461+00:00',
            'reference': '',
            'grade': 10,
            'title': 'Torradeira Britânia Vermelha Tosta Pane 7 Níveis de Tostagem',  # noqa
            'sells_to_company': True,
            'release_date': '2018-07-05T22:36:19.765393+00:00',
            'source': 'magalu',
            'updated_at': '2018-07-05T22:34:56.544591+00:00',
            'last_updated_at': '2018-07-05T22:36:20.852529',
            'brand': 'Britânia',
            'sold_count': 0,
            'product_hash': '0d9a74a782ae7f4141befd08915d2cab',
            'parent_sku': '320',
            'matching_strategy': 'OMNILOGIC',
            'offer_title': 'Torradeira Britânia Tostapane Vermelha 800W',
            'seller_id': 'mundoautomacao',
            'ean': '7891356067143',
            'md5': '99c3f6f18c5acbe2ede2d32f542cecbb',
            'type': 'product'
        }

    @classmethod
    def webfones_sku_14366(cls):
        return {
            'disable_on_matching': False,
            'matching_strategy': 'SINGLE_SELLER',
            'seller_description': 'Webfones',
            'created_at': '2018-04-17T18:03:56.331436+00:00',
            'categories': [{
                'description': 'Eletroportáteis',
                'id': 'EP',
                'subcategories': [{
                    'description': 'Fritadeira sem óleo (air fryer)',
                    'id': 'EFSO'
                }]
            }],
            'release_date': '2018-07-18T01:25:11.753190+00:00',
            'description': 'Fritadeira sem óleo   A Fritadeira Elétrica Agratto é a opção para quem preza pela saúde na hora de se alimentar. Não necessita de óleo e deixa os alimentos frescos e secos.    Benefícios   • Fácil de usar Basta colocar os alimentos, ligar a fritadeira e escolher o tempo e temperatura desejados.  • Controle de tempo Timer para até 30 minutos de fritura.   • Controle de temperatura Temperatura selecionável de 0°C até 200°C.  • Cuba e Grelha Antiaderente Muito mais fácil na hora de limpar, os resíduos de alimento saem com mais facilidade.  • Alça com Trava de Segurança Evita que a bandeja caia da fritadeira.  • Acabamento em Preto Brilhante Acabamento em preto brilhante com detalhes prateados.',  # noqa
            'last_updated_at': '2018-07-18T01:26:49.538231',
            'sells_to_company': True,
            'reference': '',
            'sold_count': 0,
            'offer_title': 'Fritadeira sem óleo Agratto Fryer AF-01',
            'attributes': [],
            'title': 'Fritadeira sem óleo Agratto Fryer AF-01',
            'review_score': 0,
            'seller_id': 'webfones',
            'main_variation': True,
            'dimensions': {
                'depth': 0.32,
                'width': 0.32,
                'weight': 0,
                'height': 0.35
            },
            'brand': 'Agratto',
            'sku': '14366',
            'type': 'product',
            'grade': 10,
            'parent_sku': '14366',
            'navigation_id': '6225646',
            'md5': 'e0730b4692c397ed6ff8b167c39bd52c',
            'review_count': 0,
            'updated_at': '2018-07-06T10:34:00.593389+00:00',
            'ean': '7898461966484'
        }

    @classmethod
    def magazineluiza_sku_216131400(cls):
        return {
            'last_updated_at': '2018-09-12T04:25:03.999166',
            'title': 'Multifuncional Epson EcoTank L575 Tanque de Tinta ',
            'dimensions': {
                'depth': 0.46,
                'height': 0.32,
                'weight': 10,
                'width': 0.62
            },
            'main_variation': False,
            'seller_id': 'magazineluiza',
            'ean': '0010343920637',
            'review_count': 0,
            'parent_sku': '2161314',
            'type': 'product',
            'description': 'A multifuncional Epson Ecotank L575 é ideal para escritórios que buscam produtividade com baixíssimo custo de impressão. Com as conexões Ethernet ou Wireless compartilhe o equipamento com todos do escritório.\n\n• Exclusiva tecnologia Ecotank da Epson - Menor Custo de Impressão da Categoria\nCom o sistema Ecotank da Epson, cada Garrafa de Tinta de 70ml tem rendimento para imprimir até 4.500 páginas em preto e 7.500 páginas em cores com alta qualidade. Isso permite imprimir milhares de trabalhos, documentos, planilhas, páginas da web ou tudo que necessitar sem se preocupar se a tinta irá acabar.\n\n• ADF - Alimentador Automático de Folhas\nUma multifuncional versátil, que além de imprimir muito, também copia e digitaliza através do vidro de originais ou pelo alimentador automático com capacidade para 30 folhas, conveniente para facilitar o manuseio de documentos.\n\n• Epson Connect\nAlém de compartilhar a multifuncional a diversos equipamentos e dispositivos (tablets e smartphones), com o Epson Connect é possível conectar-se a multifuncional de diversas maneiras podendo até digitalizar ou imprimir através da nuvem, o que significa poder estar conectado ao equipamento no escritório ou até do outro lado do mundo* .\n\n• Aplicativo iPrint\nO aplicativo iPrint da Epson permite ter o controle total da multifuncional através do tablet ou Smartphone. Imprima fotos, documentos, acesse suas pastas virtuais e digitalize para seu aparelho por este aplicativo fácil de usar e com diversos recursos. Nunca foi tão fácil unir documentos e mobilidade como na multifuncional Epson L575.\n',  # noqa
            'disable_on_matching': False,
            'review_score': 0,
            'categories': [{
                'subcategories': [
                    {
                        'id': 'IASS'
                    },
                    {
                        'id': 'IMTQ'
                    }
                ],
                'id': 'IA'
            }],
            'created_at': '2016-04-20T07:39:03.877000',
            'offer_title': 'Multifuncional Epson EcoTank L575 Tanque de Tinta  - Colorida LCD 2,2” Wi-Fi',  # noqa
            'attributes': [{
                'type': 'voltage',
                'value': 'Bivolt'
            }],
            'updated_at': '2018-09-12T01:23:34.587000',
            'reference': 'Colorida LCD 2,2” Wi-Fi',
            'brand': 'Epson',
            'matching_strategy': 'OMNILOGIC',
            'main_category': {
                'subcategory': {
                    'id': 'IASS'
                },
                'id': 'IA'
            },
            'seller_description': 'Magazine Luiza',
            'md5': '414d34c09cca9ee02275b6013a395dc7',
            'grade': 10,
            'navigation_id': '216131400',
            'sells_to_company': True,
            'sold_count': 0,
            'sku': '216131400',
            'selections': {}
        }

    @classmethod
    def lt2shop_sku_0000998113(cls):
        return {
            'sells_to_company': True,
            'ean': '',
            'seller_id': 'lt2shop',
            'seller_description': 'LT2 Shop',
            'sku': '0000998113',
            'parent_sku': '0000998113',
            'type': 'product',
            'main_variation': True,
            'title': 'Beira da sepultura, a',
            'description': 'ALGUMAS COISAS NAO FICAM SEPULTADAS... Deveria ser a melhor epoca da vida de Cat Crawfield. Com seu amante morto-vivo Bones a seu lado, ela tem sido bem-sucedida ao defender os mortais de mortos-vivos mal-intencionados. Mas apesar de fazer de tudo para manter sua verdadeira identidade a salvo de insolentes sugadores de sangue, seu disfarce e afinal desmascarado, colocando-a em terrivel perigo. Como se isso nao bastasse, uma mulher do passado de Bones esta determinada a enterra-lo de uma vez por todas. Envolta nas artimanhas de uma vampira vingativa, e ainda assim determinada a ajudar Bones a deter a magia letal que esta para ser liberada, Cat esta prestes a entender o verdadeiro significado de sangue ruim. E os truques que ela aprendeu como agentes especiais nao irao ajuda-la. Cat tera que abracar de uma vez por todas seus instintos de vampira de forma a salvar a si mesma, e Bones, de um destino pior do que a sepultura.<BR>',  # noqa
            'reference': 'Novo seculo',
            'brand': 'Novo seculo',
            'sold_count': 0,
            'review_count': 0,
            'review_score': 0,
            'categories': [{
                'id': 'LI',
                'description': 'Livros',
                'subcategories': [
                    {
                        'id': 'LLIN',
                        'description': 'Livros de Linguística',
                        'subcategories': [{
                            'id': 'LETR',
                            'description': 'Livro de Literatura Estrangeira'
                        }]
                    },
                    {
                        'id': 'LETR',
                        'description': 'Livro de Literatura Estrangeira'
                    }
                ]
            }],
            'dimensions': {
                'width': 0.23,
                'depth': 0.25,
                'weight': 0.34,
                'height': 0.16
            },
            'release_date': '2018-10-15T21:09:58.604226+00:00',
            'updated_at': '2018-10-15T21:05:28.646621+00:00',
            'created_at': '2018-10-15T21:05:28.631725+00:00',
            'attributes': [],
            'disable_on_matching': True,
            'offer_title': 'Beira da sepultura, a - Novo seculo',
            'grade': 10,
            'matching_strategy': 'SINGLE_SELLER',
            'navigation_id': 'bh8c1h748a',
            'md5': 'f50da6a38164aeca3687b75df90448fd',
            'last_updated_at': '2018-10-15T21:10:26.581877',
            'isbn': '9780074500903'
        }

    @classmethod
    def cliquebooks_sku_5752019(cls):
        return {
            'sells_to_company': True,
            'ean': '9788532531438',
            'seller_id': 'cliquebooks',
            'seller_description': 'Clique Books',
            'sku': '5752019',
            'parent_sku': '5752019',
            'type': 'product',
            'main_variation': True,
            'title': 'Livro - Cabala e a arte de manutenção da carroça',
            'description': '',
            'reference': '',
            'brand': 'Rocco',
            'sold_count': 0,
            'review_count': 0,
            'review_score': 0,
            'categories': [{
                'id': 'LI',
                'description': 'Livros',
                'subcategories': [{
                    'id': 'LLIN',
                    'description': 'Livros de Linguística',
                    'subcategories': [{
                        'id': 'LETR',
                        'description': 'Livro de Literatura Estrangeira'
                    }]
                }]
            }],
            'dimensions': {
                'width': 0.14,
                'depth': 0.02,
                'weight': 0.11,
                'height': 0.19
            },
            'release_date': '2018-10-15T21:09:58.604226+00:00',
            'updated_at': '2018-10-15T21:05:28.646621+00:00',
            'created_at': '2018-10-15T21:05:28.631725+00:00',
            'attributes': [
                {'type': 'additional', 'value': '1'}
            ],
            'disable_on_matching': True,
            'offer_title': 'Cabala e a arte de manutenção da carroça',
            'grade': 10,
            'matching_strategy': 'SINGLE_SELLER',
            'navigation_id': 'jd3d3gdb9e',
            'md5': 'f50da6a38164aeca3687b75df90448fd',
            'last_updated_at': '2018-10-15T21:10:26.581877',
            'isbn': '9788532531438'
        }

    @classmethod
    def magazineluizaa_sku_144129900(cls):
        return {
            'active': True,
            'brand': 'Tramontina',
            'categories': [{
                'id': 'UD',
                'subcategories': [{
                    'id': 'PANL'
                }]
            }],
            'created_at': '2018-01-19T07:48:21.980000',
            'description': 'As dez peças do jogo de panelas compacto vermelho',
            'dimensions': {
                'depth': 0.4,
                'height': 0.25,
                'weight': 4.62,
                'width': 0.41
            },
            'ean': '7891112250536',
            'main_category': {
                'id': 'UD',
                'subcategory': {
                    'id': 'PANL'
                }
            },
            'main_variation': False,
            'parent_sku': '1441299',
            'reference': 'de Alumínio Vermelho 10 Peças Turim 20298/722',
            'review_count': 0,
            'review_score': 0,
            'selections': {},
            'seller_description': 'Magazine Luiza',
            'seller_id': 'magazineluiza',
            'sku': '144129900',
            'sold_count': 0,
            'title': 'Jogo de Panelas Tramontina Antiaderente',
            'type': 'product',
            'updated_at': '2019-08-20T18:53:24.647000',
            'disable_on_matching': False,
            'offer_title': 'Jogo de Panelas Tramontina Antiaderente',
            'grade': 1010,
            'navigation_id': '144129900',
            'matching_strategy': 'SINGLE_SELLER',
            'md5': '7f7663a289865efe990694e2dcc30b73',
            'last_updated_at': '2019-08-20T21:56:38.549985',
            'sells_to_company': True,
            'price': {
                'list_price': 399.9,
                'stock_type': 'on_supplier',
                'delivery_availability': 'nationwide',
                'md5': '191e4e164226253f8aa6367601e27bbb',
                'seller_id': 'magazineluiza',
                'campaign_code': 0,
                'stock_count': 1,
                'sku': '144129900',
                'price': 239.9,
                'last_updated_at': '2019-08-19T22:14:37.924495',
                'checkout_price': 0
            },
            'media': {}
        }

    @classmethod
    def authenticlivros_sku_1073972(cls):
        return {
            'sells_to_company': True,
            'ean': '9788551002490',
            'seller_id': 'authenticlivros',
            'seller_description': 'Authentic Livros',
            'sku': '1073972',
            'parent_sku': '1073972',
            'type': 'product',
            'main_variation': True,
            'title': 'Livro - A sutil arte de ligar o f*da-se',
            'description': '<p>Chega de tentar buscar um sucesso que só existe na sua cabeça. Chega de se torturar para pensar positivo enquanto sua vida vai ladeira abaixo. Chega de se sentir inferior por não ver o lado bom de estar no fundo do poço.</p>\n\n<p>Coaching, autoajuda, desenvolvimento pessoal, mentalização positiva - sem querer desprezar o valor de nada disso, a grande verdade é que às vezes nos sentimos quase sufocados diante da pressão infinita por parecermos otimistas o tempo todo. É um pecado social se deixar abater quando as coisas não vão bem. Ninguém pode fracassar simplesmente, sem aprender nada com isso. Não dá mais. É insuportável. E é aí que entra a revolucionária e sutil arte de ligar o foda-se.</p>\n\n<p>Mark Manson usa toda a sua sagacidade de escritor e seu olhar crítico para propor um novo caminho rumo a uma vida melhor, mais coerente com a realidade e consciente dos nossos limites. E ele faz isso da melhor maneira. Como um verdadeiro amigo, Mark se senta ao seu lado e diz, olhando nos seus olhos: você não é tão especial. Ele conta umas piadas aqui, dá uns exemplos inusitados ali, joga umas verdades na sua cara e pronto, você já se sente muito mais alerta e capaz de enfrentar esse mundo cão.</p>\n\n<p>Para os céticos e os descrentes, mas também para os amantes do gênero, enfim uma abordagem franca e inteligente que vai ajudar você a descobrir o que é realmente importante na sua vida, e f*da-se o resto. Livre-se agora da felicidade maquiada e superficial e abrace esta arte verdadeiramente transformadora.</p>',  # noqa
            'reference': '',
            'brand': 'Intrinseca',
            'sold_count': 0,
            'review_count': 0,
            'review_score': 0.0,
            'categories': [
                {
                    'id': 'LI',
                    'subcategories': [
                        {
                            'id': 'LLIT'
                        }
                    ]
                }
            ],
            'dimensions': {
                'width': 0.14,
                'depth': 0.21,
                'weight': 0.28,
                'height': 0.02
            },
            'release_date': '2020-10-26T16:16:33.455517+00:00',
            'updated_at': '2020-09-19T10:53:52.013712+00:00',
            'created_at': '2019-05-10T16:53:35.085043+00:00',
            'attributes': [],
            'disable_on_matching': False,
            'offer_title': 'Livro - A sutil arte de ligar o f*da-se',
            'grade': 10,
            'navigation_id': 'egjbb8121d',
            'matching_strategy': 'OMNILOGIC',
            'md5': '100e77e4e8da77f16c7b84420b2a081a',
            'last_updated_at': '2020-10-26T16:16:40.366885',
            'product': '4a5eab178ba030c793e99f73b0386729',
            'isbn': '9788551002490',
            'product_hash': '4a5eab178ba030c793e99f73b0386729',
            'source': 'magalu',
            'main_category': {
                'id': 'LI',
                'subcategory': {
                    'id': 'LIAJ'
                }
            },
            'price': {
                'sku': '1073972',
                'seller_id': 'authenticlivros',
                'list_price': 39.9,
                'price': 31.92,
                'delivery_availability': 'nationwide',
                'stock_count': 584,
                'stock_type': 'on_seller',
                'last_updated_at': '2021-04-14T14:35:11.249055',
                'md5': 'f24a0e32d7c20d52d4c9cd158d248c77',
                'source': 'price'
            },
            'media': {
                'images': [
                    '/{w}x{h}/livro-a-sutil-arte-de-ligar-o-f-da-se/authenticlivros/1073972/cee8f7d343866ce68fa16f4e228b4a38.jpg',  # noqa
                    '/{w}x{h}/livro-a-sutil-arte-de-ligar-o-f-da-se/authenticlivros/1073972/5c33bb4de12abf91386e033b6bb5f0af.jpg'  # noqa
                ]
            }
        }

    @classmethod
    def magazineluiza_sku_222764000(cls):
        return {
            'active': True,
            'brand': 'Intrínseca',
            'categories': [{
                'id': 'LI',
                'subcategories': [{
                    'id': 'LIAJ'
                }]
            }],
            'created_at': '2019-03-23T08:14:26.573000',
            'description': '<p>Chega de tentar buscar um sucesso que só existe na sua cabeça. Chega de se torturar para pensar positivo enquanto sua vida vai ladeira abaixo. Chega de se sentir inferior por não ver o lado bom de estar no fundo do poço.</p>\n\n<p>Coaching, autoajuda, desenvolvimento pessoal, mentalização positiva - sem querer desprezar o valor de nada disso, a grande verdade é que às vezes nos sentimos quase sufocados diante da pressão infinita por parecermos otimistas o tempo todo. É um pecado social se deixar abater quando as coisas não vão bem. Ninguém pode fracassar simplesmente, sem aprender nada com isso. Não dá mais. É insuportável. E é aí que entra a revolucionária e sutil arte de ligar o foda-se.</p>\n\n<p>Mark Manson usa toda a sua sagacidade de escritor e seu olhar crítico para propor um novo caminho rumo a uma vida melhor, mais coerente com a realidade e consciente dos nossos limites. E ele faz isso da melhor maneira. Como um verdadeiro amigo, Mark se senta ao seu lado e diz, olhando nos seus olhos: você não é tão especial. Ele conta umas piadas aqui, dá uns exemplos inusitados ali, joga umas verdades na sua cara e pronto, você já se sente muito mais alerta e capaz de enfrentar esse mundo cão.</p>\n\n<p>Para os céticos e os descrentes, mas também para os amantes do gênero, enfim uma abordagem franca e inteligente que vai ajudar você a descobrir o que é realmente importante na sua vida, e f*da-se o resto. Livre-se agora da felicidade maquiada e superficial e abrace esta arte verdadeiramente transformadora.</p>',  # noqa
            'dimensions': {
                'depth': 0.21,
                'height': 0.02,
                'weight': 0.276,
                'width': 0.14
            },
            'ean': '9788551002490',
            'main_category': {
                'id': 'LI',
                'subcategory': {
                    'id': 'LIAJ'
                }
            },
            'main_variation': False,
            'parent_sku': '2227640',
            'reference': '',
            'review_count': 0,
            'review_score': 0,
            'selections': {
                '0': ['18426', '22038']
            },
            'seller_description': 'Magazine Luiza',
            'seller_id': 'magazineluiza',
            'sku': '222764000',
            'sold_count': 0,
            'title': 'Livro - A sutil arte de ligar o f*da-se',
            'type': 'product',
            'updated_at': '2019-09-13T08:58:54.097000',
            'disable_on_matching': False,
            'offer_title': 'A Sutil Arte de Ligar o F*da-se - Uma Estratégia Inusitada Para Uma Vida Melhor',  # noqa
            'grade': 1010,
            'navigation_id': '222764000',
            'matching_strategy': 'OMNILOGIC',
            'md5': '308f99c3ee2727641112bbd917fa27b3',
            'last_updated_at': '2019-09-13T12:02:28.465767',
            'sells_to_company': True,
            'isbn': '9788551002490',
            'store_pickup_available': True,
            'delivery_plus_1': True,
            'delivery_plus_2': False
        }

    @classmethod
    def meulivromegastore_sku_166271(cls):
        return {
            'sells_to_company': True,
            'ean': '9788551002490',
            'seller_id': 'meulivromegastore',
            'seller_description': 'Meu Livro Mega Store',
            'sku': '166271',
            'parent_sku': '166271',
            'type': 'product',
            'main_variation': True,
            'title': 'Sutil Arte de Ligar O F Da-se, A - Intrinseca - Editora intrinseca',  # noqa
            'description': '<p>Chega de tentar buscar um sucesso que só existe na sua cabeça. Chega de se torturar para pensar positivo enquanto sua vida vai ladeira abaixo. Chega de se sentir inferior por não ver o lado bom de estar no fundo do poço.</p>\n\n<p>Coaching, autoajuda, desenvolvimento pessoal, mentalização positiva - sem querer desprezar o valor de nada disso, a grande verdade é que às vezes nos sentimos quase sufocados diante da pressão infinita por parecermos otimistas o tempo todo. É um pecado social se deixar abater quando as coisas não vão bem. Ninguém pode fracassar simplesmente, sem aprender nada com isso. Não dá mais. É insuportável. E é aí que entra a revolucionária e sutil arte de ligar o foda-se.</p>\n\n<p>Mark Manson usa toda a sua sagacidade de escritor e seu olhar crítico para propor um novo caminho rumo a uma vida melhor, mais coerente com a realidade e consciente dos nossos limites. E ele faz isso da melhor maneira. Como um verdadeiro amigo, Mark se senta ao seu lado e diz, olhando nos seus olhos: você não é tão especial. Ele conta umas piadas aqui, dá uns exemplos inusitados ali, joga umas verdades na sua cara e pronto, você já se sente muito mais alerta e capaz de enfrentar esse mundo cão.</p>\n\n<p>Para os céticos e os descrentes, mas também para os amantes do gênero, enfim uma abordagem franca e inteligente que vai ajudar você a descobrir o que é realmente importante na sua vida, e f*da-se o resto. Livre-se agora da felicidade maquiada e superficial e abrace esta arte verdadeiramente transformadora.</p>',  # noqa
            'reference': '',
            'brand': 'Intrínseca Editora',
            'sold_count': 0,
            'review_count': 0,
            'review_score': 0,
            'categories': [{
                'id': 'LI',
                'subcategories': [{
                    'id': 'LLIT'
                }]
            }],
            'dimensions': {
                'width': 0.14,
                'depth': 0.02,
                'weight': 0.3,
                'height': 0.21
            },
            'release_date': '2019-08-31T15:00:52.325377+00:00',
            'updated_at': '2019-07-22T22:19:00.314902+00:00',
            'created_at': '2018-11-13T11:03:23.671732+00:00',
            'attributes': [],
            'disable_on_matching': False,
            'offer_title': 'Sutil Arte de Ligar O F Da-se, A - Intrinseca - Editora intrinseca',  # noqa
            'grade': 10,
            'navigation_id': 'dbkgh9k336',
            'matching_strategy': 'OMNILOGIC',
            'md5': 'e520fd75405e22bb79d411de22fad44f',
            'last_updated_at': '2019-08-31T15:00:57.011918',
            'isbn': '9788551002490',
            'main_category': {
                'id': 'LI',
                'subcategory': {
                    'id': 'LLIT'
                }
            },
            'product_hash': 'c91b7af58441163e29bbadb1cdd52941',
            'source': 'magalu'
        }

    @classmethod
    def livrariaflorence2_sku_9788543105757(cls):
        return {
            'sells_to_company': True,
            'ean': '9788543105758',
            'seller_id': 'livrariaflorence2',
            'seller_description': 'Livraria Florence',
            'sku': '9788543105757',
            'parent_sku': '1755703',
            'type': 'product',
            'main_variation': True,
            'title': 'Poesia que transforma - sextante - Gmt',
            'description': 'Bráulio Bessa conquistou o Brasil com seus cordéis no programa Encontro com Fátima Bernardes.\n\nO livro inclui o poema Recomece e ilustrações do artista baiano Elano Passos.\n\n\n“O Bráulio mexe com nossas memórias, nossos sentimentos, faz aflorar o melhor da gente. É poesia que sai do coração. Que alegria tê-lo toda semana no meu programa!” - Fátima Bernardes\n\n\n“Cada palavra que sai da boca do Bráulio Bessa toca minha alma de uma forma raríssima.” - Milton Nascimento\n \n“Bráulio Bessa é um hipnotizador de palavras. Tem o coração rimado. Quando fala, o verbo venta verso.” - Fabrício Carpinejar\n\n\n“Gosto de comparar a poesia a um abraço, que consegue fazer um carinho na alma sem nem saber qual é a dor que você está sentindo. A poesia se adapta à sua dor. É um abraço cego e despretensioso, como quem diz: ‘Venha! Tá doendo? Pois deixe eu dar um arrocho, que vai lhe fazer bem.’” - Bráulio Bessa\n\n\nEste livro é uma homenagem à poesia e a tudo o que ela é capaz de proporcionar. Com mais de 30 de seus emocionantes poemas, alguns deles inéditos, Bráulio Bessa nos conta um pouco das histórias do menino de Alto Santo, no interior do Ceará, que se tornou poeta e ativista cultural.\n \nDesde o primeiro encontro com a obra de Patativa do Assaré, aos 14 anos, até a fama na televisão, ele mostra como a poesia transformou sua vida.\n \nCom ilustrações do artista baiano Elano Passos, o livro traz ainda depoimentos de fãs de todos os cantos do Brasil, revelando como as palavras de Bráulio são capazes de inspirar pequenas e grandes mudanças.',  # noqa
            'reference': '',
            'brand': 'GMT',
            'sold_count': 0,
            'review_count': 0,
            'review_score': 0,
            'categories': [{
                'id': 'LI',
                'subcategories': [{
                    'id': 'LLIT'
                }]
            }],
            'dimensions': {
                'width': 0.11,
                'depth': 0.16,
                'weight': 0.4,
                'height': 0.02
            },
            'release_date': '2019-07-23T10:29:14.381634+00:00',
            'updated_at': '2019-07-23T10:28:33.178729+00:00',
            'created_at': '2019-03-31T05:03:55.495622+00:00',
            'attributes': [],
            'disable_on_matching': False,
            'offer_title': 'Poesia que transforma - sextante - Gmt',
            'grade': 10,
            'matching_strategy': 'OMNILOGIC',
            'navigation_id': 'haadaa83f7',
            'md5': 'cad6d3487031248fc6c6effed3485e88',
            'last_updated_at': '2019-07-23T10:29:25.922676',
            'isbn': '9788543105758',
            'main_category': {
                'id': 'LI',
                'subcategory': {
                    'id': 'LLIT'
                }
            },
            'product_hash': '572a933e7834a6cea0a7d4a2b5f35e92',
            'source': 'magalu'
        }

    @classmethod
    def livrariaflorence2_sku_9788543105758(cls):
        return {
            'sells_to_company': True,
            'ean': '9788543105758',
            'seller_id': 'livrariaflorence2',
            'seller_description': 'Livraria Florence',
            'sku': '9788543105758',
            'parent_sku': '1593474',
            'type': 'product',
            'main_variation': True,
            'title': 'Livro - Poesia Que Transforma - Bessa - Sextante',
            'description': 'Bráulio Bessa conquistou o Brasil com seus cordéis no programa Encontro com Fátima Bernardes.\n\nO livro inclui o poema Recomece e ilustrações do artista baiano Elano Passos.\n\n\n“O Bráulio mexe com nossas memórias, nossos sentimentos, faz aflorar o melhor da gente. É poesia que sai do coração. Que alegria tê-lo toda semana no meu programa!” - Fátima Bernardes\n\n\n“Cada palavra que sai da boca do Bráulio Bessa toca minha alma de uma forma raríssima.” - Milton Nascimento\n \n“Bráulio Bessa é um hipnotizador de palavras. Tem o coração rimado. Quando fala, o verbo venta verso.” - Fabrício Carpinejar\n\n\n“Gosto de comparar a poesia a um abraço, que consegue fazer um carinho na alma sem nem saber qual é a dor que você está sentindo. A poesia se adapta à sua dor. É um abraço cego e despretensioso, como quem diz: ‘Venha! Tá doendo? Pois deixe eu dar um arrocho, que vai lhe fazer bem.’” - Bráulio Bessa\n\n\nEste livro é uma homenagem à poesia e a tudo o que ela é capaz de proporcionar. Com mais de 30 de seus emocionantes poemas, alguns deles inéditos, Bráulio Bessa nos conta um pouco das histórias do menino de Alto Santo, no interior do Ceará, que se tornou poeta e ativista cultural.\n \nDesde o primeiro encontro com a obra de Patativa do Assaré, aos 14 anos, até a fama na televisão, ele mostra como a poesia transformou sua vida.\n \nCom ilustrações do artista baiano Elano Passos, o livro traz ainda depoimentos de fãs de todos os cantos do Brasil, revelando como as palavras de Bráulio são capazes de inspirar pequenas e grandes mudanças.',  # noqa
            'reference': '',
            'brand': 'Sextante',
            'sold_count': 0,
            'review_count': 0,
            'review_score': 0,
            'categories': [{
                'id': 'LI',
                'subcategories': [{
                    'id': 'LLIT'
                }]
            }],
            'dimensions': {
                'width': 0.11,
                'depth': 0.16,
                'weight': 0.33,
                'height': 0.02
            },
            'release_date': '2019-05-04T22:24:12.820394+00:00',
            'updated_at': '2019-05-04T22:22:49.669604+00:00',
            'created_at': '2019-03-26T23:32:25.156630+00:00',
            'attributes': [],
            'disable_on_matching': False,
            'offer_title': 'Livro - Poesia Que Transforma - Bessa - Sextante',
            'grade': 10,
            'navigation_id': 'ej01hd210g',
            'matching_strategy': 'OMNILOGIC',
            'md5': '63150fad8dc5a7be66f8351de762458c',
            'last_updated_at': '2019-05-04T22:24:18.042280',
            'isbn': '9788543105758',
            'main_category': {
                'id': 'LI',
                'subcategory': {
                    'id': 'LLIT'
                }
            },
            'product_hash': '572a933e7834a6cea0a7d4a2b5f35e92',
            'source': 'magalu'
        }

    @classmethod
    def livrariasebocapricho_sku_23036521(cls):
        return {
            'seller_id': 'livrariasebocapricho',
            'sku': '23036521',
            'sells_to_company': True,
            'ean': '9788543105758',
            'seller_description': 'Livraria Sebo Capricho',
            'parent_sku': '23036521',
            'type': 'product',
            'main_variation': True,
            'title': 'Poesia que Transforma - Sextante',
            'description': 'Bráulio Bessa conquistou o Brasil com seus cordéis no programa Encontro com Fátima Bernardes.\n\nO livro inclui o poema Recomece e ilustrações do artista baiano Elano Passos.\n\n\n“O Bráulio mexe com nossas memórias, nossos sentimentos, faz aflorar o melhor da gente. É poesia que sai do coração. Que alegria tê-lo toda semana no meu programa!” - Fátima Bernardes\n\n\n“Cada palavra que sai da boca do Bráulio Bessa toca minha alma de uma forma raríssima.” - Milton Nascimento\n \n“Bráulio Bessa é um hipnotizador de palavras. Tem o coração rimado. Quando fala, o verbo venta verso.” - Fabrício Carpinejar\n\n\n“Gosto de comparar a poesia a um abraço, que consegue fazer um carinho na alma sem nem saber qual é a dor que você está sentindo. A poesia se adapta à sua dor. É um abraço cego e despretensioso, como quem diz: ‘Venha! Tá doendo? Pois deixe eu dar um arrocho, que vai lhe fazer bem.’” - Bráulio Bessa\n\n\nEste livro é uma homenagem à poesia e a tudo o que ela é capaz de proporcionar. Com mais de 30 de seus emocionantes poemas, alguns deles inéditos, Bráulio Bessa nos conta um pouco das histórias do menino de Alto Santo, no interior do Ceará, que se tornou poeta e ativista cultural.\n \nDesde o primeiro encontro com a obra de Patativa do Assaré, aos 14 anos, até a fama na televisão, ele mostra como a poesia transformou sua vida.\n \nCom ilustrações do artista baiano Elano Passos, o livro traz ainda depoimentos de fãs de todos os cantos do Brasil, revelando como as palavras de Bráulio são capazes de inspirar pequenas e grandes mudanças.',  # noqa
            'reference': '',
            'brand': 'Sextante',
            'sold_count': 0,
            'review_count': 0,
            'review_score': 0,
            'categories': [{
                'id': 'LI',
                'subcategories': [{
                    'id': 'LVSP'
                }, {
                    'id': 'LLIT'
                }]
            }],
            'dimensions': {
                'width': 0.15,
                'depth': 0.25,
                'weight': 0.25,
                'height': 0.01
            },
            'release_date': '2019-08-08T16:11:31.179497+00:00',
            'updated_at': '2019-08-08T16:10:49.762718+00:00',
            'created_at': '2019-08-08T16:10:49.748467+00:00',
            'attributes': [],
            'disable_on_matching': False,
            'offer_title': 'Poesia que Transforma - Sextante',
            'grade': 10,
            'matching_strategy': 'OMNILOGIC',
            'navigation_id': 'dggf9f538g',
            'md5': '3c8b998e557b9e15fa6ed969165dc7fd',
            'last_updated_at': '2019-08-08T16:11:37.800482',
            'isbn': '9788543105758',
            'main_category': {
                'id': 'LI',
                'subcategory': {
                    'id': 'LVSP'
                }
            },
            'product_hash': '572a933e7834a6cea0a7d4a2b5f35e92',
            'source': 'magalu'
        }

    @classmethod
    def magazineluiza_sku_221841200(cls):
        return {
            'active': True,
            'brand': 'Editora Sextante',
            'categories': [{
                'id': 'LI',
                'subcategories': [{
                    'id': 'LLIT'
                }, {
                    'id': 'LVSP'
                }]
            }],
            'created_at': '2019-03-23T08:14:26.573000',
            'description': 'Bráulio Bessa conquistou o Brasil com seus cordéis no programa Encontro com Fátima Bernardes.\n\nO livro inclui o poema Recomece e ilustrações do artista baiano Elano Passos.\n\n\n“O Bráulio mexe com nossas memórias, nossos sentimentos, faz aflorar o melhor da gente. É poesia que sai do coração. Que alegria tê-lo toda semana no meu programa!” - Fátima Bernardes\n\n\n“Cada palavra que sai da boca do Bráulio Bessa toca minha alma de uma forma raríssima.” - Milton Nascimento\n \n“Bráulio Bessa é um hipnotizador de palavras. Tem o coração rimado. Quando fala, o verbo venta verso.” - Fabrício Carpinejar\n\n\n“Gosto de comparar a poesia a um abraço, que consegue fazer um carinho na alma sem nem saber qual é a dor que você está sentindo. A poesia se adapta à sua dor. É um abraço cego e despretensioso, como quem diz: ‘Venha! Tá doendo? Pois deixe eu dar um arrocho, que vai lhe fazer bem.’” - Bráulio Bessa\n\n\nEste livro é uma homenagem à poesia e a tudo o que ela é capaz de proporcionar. Com mais de 30 de seus emocionantes poemas, alguns deles inéditos, Bráulio Bessa nos conta um pouco das histórias do menino de Alto Santo, no interior do Ceará, que se tornou poeta e ativista cultural.\n \nDesde o primeiro encontro com a obra de Patativa do Assaré, aos 14 anos, até a fama na televisão, ele mostra como a poesia transformou sua vida.\n \nCom ilustrações do artista baiano Elano Passos, o livro traz ainda depoimentos de fãs de todos os cantos do Brasil, revelando como as palavras de Bráulio são capazes de inspirar pequenas e grandes mudanças.',  # noqa
            'dimensions': {
                'depth': 0.02,
                'height': 0.21,
                'weight': 0.23,
                'width': 0.14
            },
            'ean': '9788543105758',
            'main_category': {
                'id': 'LI',
                'subcategory': {
                    'id': 'LLIT'
                }
            },
            'main_variation': False,
            'parent_sku': '2218412',
            'reference': '',
            'review_count': 0,
            'review_score': 0,
            'selections': {
                '0': ['18426', '22038']
            },
            'seller_description': 'Magazine Luiza',
            'seller_id': 'magazineluiza',
            'sku': '221841200',
            'sold_count': 0,
            'title': 'Livro - Poesia que transforma',
            'type': 'product',
            'updated_at': '2019-09-13T12:57:44.240000',
            'disable_on_matching': False,
            'offer_title': 'Poesia que transforma',
            'grade': 1010,
            'navigation_id': '221841200',
            'matching_strategy': 'OMNILOGIC',
            'md5': 'fe776e7d04684dd27e7f2dad9bd3802d',
            'last_updated_at': '2019-09-13T16:49:10.636410',
            'sells_to_company': True,
            'isbn': '9788543105758',
            'store_pickup_available': True,
            'delivery_plus_1': True,
            'delivery_plus_2': False
        }

    @classmethod
    def saraiva_sku_10260263(cls):
        return {
            'sells_to_company': False,
            'ean': '9788543105758',
            'seller_id': 'saraiva',
            'seller_description': 'Saraiva',
            'sku': '10260263',
            'parent_sku': '10650918',
            'type': 'product',
            'main_variation': False,
            'title': 'Poesia Que Transforma - Sextante / gmt',
            'description': 'Bráulio Bessa conquistou o Brasil com seus cordéis no programa Encontro com Fátima Bernardes.\n\nO livro inclui o poema Recomece e ilustrações do artista baiano Elano Passos.\n\n\n“O Bráulio mexe com nossas memórias, nossos sentimentos, faz aflorar o melhor da gente. É poesia que sai do coração. Que alegria tê-lo toda semana no meu programa!” - Fátima Bernardes\n\n\n“Cada palavra que sai da boca do Bráulio Bessa toca minha alma de uma forma raríssima.” - Milton Nascimento\n \n“Bráulio Bessa é um hipnotizador de palavras. Tem o coração rimado. Quando fala, o verbo venta verso.” - Fabrício Carpinejar\n\n\n“Gosto de comparar a poesia a um abraço, que consegue fazer um carinho na alma sem nem saber qual é a dor que você está sentindo. A poesia se adapta à sua dor. É um abraço cego e despretensioso, como quem diz: ‘Venha! Tá doendo? Pois deixe eu dar um arrocho, que vai lhe fazer bem.’” - Bráulio Bessa\n\n\nEste livro é uma homenagem à poesia e a tudo o que ela é capaz de proporcionar. Com mais de 30 de seus emocionantes poemas, alguns deles inéditos, Bráulio Bessa nos conta um pouco das histórias do menino de Alto Santo, no interior do Ceará, que se tornou poeta e ativista cultural.\n \nDesde o primeiro encontro com a obra de Patativa do Assaré, aos 14 anos, até a fama na televisão, ele mostra como a poesia transformou sua vida.\n \nCom ilustrações do artista baiano Elano Passos, o livro traz ainda depoimentos de fãs de todos os cantos do Brasil, revelando como as palavras de Bráulio são capazes de inspirar pequenas e grandes mudanças.',  # noqa
            'reference': '',
            'brand': 'GMT',
            'sold_count': 0,
            'review_count': 0,
            'review_score': 0,
            'categories': [{
                'id': 'LI',
                'subcategories': [{
                    'id': 'LLIT'
                }]
            }],
            'dimensions': {
                'width': 0.14,
                'depth': 0.02,
                'weight': 0.23,
                'height': 0.21
            },
            'release_date': '2019-09-02T15:21:22.437502+00:00',
            'updated_at': '2019-09-02T15:21:22.381759+00:00',
            'created_at': '2019-06-28T05:02:26.925289+00:00',
            'attributes': [],
            'disable_on_matching': False,
            'offer_title': 'Poesia Que Transforma - Sextante / gmt',
            'grade': 10,
            'navigation_id': 'cfjkh8c2hk',
            'matching_strategy': 'OMNILOGIC',
            'md5': '1842ea6706ea2495a3a48078c5a5e5d6',
            'last_updated_at': '2019-09-02T15:21:51.824657',
            'isbn': '9788543105758',
            'main_category': {
                'id': 'LI',
                'subcategory': {
                    'id': 'LLIT'
                }
            },
            'product_hash': '572a933e7834a6cea0a7d4a2b5f35e92',
            'source': 'magalu'
        }

    @classmethod
    def mundokids_sku_55(cls):
        return {
            'sells_to_company': True,
            'ean': '99999999',
            'seller_id': 'mundokids',
            'seller_description': 'Mundo Kids',
            'sku': '55',
            'parent_sku': '109',
            'type': 'product',
            'main_variation': True,
            'title': 'Triciclo Infantil 3x1 Vira Gangorra Belfix Luzes E Musical cabeça de cachorro',  # noqa
            'description': '<p>Triciclo Infantil 3x1 Vira Gangorra Belfix</p> <p>Triciclo Gangorra Cabeça Cachorro Rosa</p> <p>3 em 1: Triciclo para empurrar + vira balancinho + pedalar</p> <p>Assento macio</p> <p>Duas cestas - frontal e traseira</p> <p>Toca música e acende luzes</p> <p>Possui haste para empurrar</p> <p>Estruturas de proteção e capô removível</p> <p>Transforma-se em balancinho</p> <p>Levanta as orelhas ao pressionar o botão</p> <p>Assento de tecido</p> <p>Brinquedo para crianças acima dos 3 anos</p> <p>Suporta uma criança de até 20 Kg</p> <p>Produzido seguindo criteriosamente as recomendações de segurança do INMETRO</p> <p>Pilhas não inclusas (deve-se usar pilhas comuns, pois pilhas recarregáveis e alcalinas não funcionam nesse aparelho)</p> <p>ATENÇÃO SIGA AS INSTRUÇÕES DE MONTAGEM NO VÍDEO A CIMA</p>',  # noqa
            'reference': '',
            'brand': 'Belfix',
            'sold_count': 0,
            'review_count': 0,
            'review_score': 0,
            'categories': [{
                'id': 'BR',
                'subcategories': [{
                    'id': 'BTRI'
                }]
            }],
            'dimensions': {
                'width': 0.22,
                'depth': 0.42,
                'weight': 6.5,
                'height': 0.69
            },
            'release_date': '2019-09-17T16:44:21.809457+00:00',
            'updated_at': '2019-08-14T22:40:00.982876+00:00',
            'created_at': '2019-07-01T17:43:33.855664+00:00',
            'attributes': [{
                'type': 'color',
                'value': 'Azul'
            }],
            'disable_on_matching': False,
            'offer_title': 'Triciclo Infantil 3x1 Vira Gangorra Belfix Luzes E Musical cabeça de cachorro',  # noqa
            'grade': 20,
            'navigation_id': 'cd1h8ddjg6',
            'matching_strategy': 'SINGLE_SELLER',
            'md5': 'b94d7785e08ac1fa05085576cdfb112c',
            'last_updated_at': '2019-09-17T16:44:26.287621',
            'main_category': {
                'id': 'BR',
                'subcategory': {
                    'id': 'BTRI'
                }
            }
        }

    @classmethod
    def mundokids_sku_57(cls):
        return {
            'sells_to_company': True,
            'ean': '88888888',
            'seller_id': 'mundokids',
            'seller_description': 'Mundo Kids',
            'sku': '57',
            'parent_sku': '109',
            'type': 'product',
            'main_variation': False,
            'title': 'Triciclo Infantil 3x1 Vira Gangorra Belfix Luzes E Musical cabeça de cachorro',  # noqa
            'description': '<p>Triciclo Infantil 3x1 Vira Gangorra Belfix</p> <p>Triciclo Gangorra Cabeça Cachorro Rosa</p> <p>3 em 1: Triciclo para empurrar + vira balancinho + pedalar</p> <p>Assento macio</p> <p>Duas cestas - frontal e traseira</p> <p>Toca música e acende luzes</p> <p>Possui haste para empurrar</p> <p>Estruturas de proteção e capô removível</p> <p>Transforma-se em balancinho</p> <p>Levanta as orelhas ao pressionar o botão</p> <p>Assento de tecido</p> <p>Brinquedo para crianças acima dos 3 anos</p> <p>Suporta uma criança de até 20 Kg</p> <p>Produzido seguindo criteriosamente as recomendações de segurança do INMETRO</p> <p>Pilhas não inclusas (deve-se usar pilhas comuns, pois pilhas recarregáveis e alcalinas não funcionam nesse aparelho)</p> <p>ATENÇÃO SIGA AS INSTRUÇÕES DE MONTAGEM NO VÍDEO A CIMA</p>',  # noqa
            'reference': '',
            'brand': 'Belfix',
            'sold_count': 0,
            'review_count': 0,
            'review_score': 0,
            'categories': [{
                'id': 'BR',
                'subcategories': [{
                    'id': 'BTRI'
                }]
            }],
            'dimensions': {
                'width': 0.22,
                'depth': 0.42,
                'weight': 6.5,
                'height': 0.69
            },
            'release_date': '2019-09-17T16:45:09.809751+00:00',
            'updated_at': '2019-08-14T22:40:00.982876+00:00',
            'created_at': '2019-07-01T17:43:33.855664+00:00',
            'attributes': [{
                'type': 'color',
                'value': 'ROSA'
            }],
            'disable_on_matching': False,
            'offer_title': 'Triciclo Infantil 3x1 Vira Gangorra Belfix Luzes E Musical cabeça de cachorro',  # noqa
            'grade': 10,
            'navigation_id': 'hfbf18cbd6',
            'matching_strategy': 'SINGLE_SELLER',
            'md5': '41a4bd7782e2d0ddc35099796b7ef770',
            'last_updated_at': '2019-09-17T16:45:12.828173',
            'main_category': {
                'id': 'BR',
                'subcategory': {
                    'id': 'BTRI'
                }
            }
        }

    @classmethod
    def cliquebooks_sku_543242_1(cls):
        return {
            'sells_to_company': True,
            'ean': '9788506082645',
            'seller_id': 'cliquebooks',
            'seller_description': 'Clique Books',
            'sku': '543242.1',
            'parent_sku': '543242.1',
            'type': 'product',
            'main_variation': True,
            'title': 'Livro - O poder da música',
            'description': '\'O Poder da Música\' é um livro superdivertido, com lindas ilustrações, um cenário gigante e 12 miniaturas incríveis!',  # noqa
            'reference': '',
            'brand': 'Melhoramentos',
            'sold_count': 0,
            'review_count': 0,
            'review_score': 0,
            'categories': [{
                'id': 'LI',
                'subcategories': [{
                    'id': 'LVEN'
                }, {
                    'id': 'LVIN'
                }, {
                    'id': 'LLTJ'
                }]
            }],
            'dimensions': {
                'width': 0.21,
                'depth': 0.04,
                'weight': 0.7,
                'height': 0.26
            },
            'release_date': '2019-04-11T12:26:12.264137+00:00',
            'updated_at': '2018-02-21T13:07:40.255308+00:00',
            'created_at': '2018-02-21T13:07:40.225153+00:00',
            'attributes': [{
                'type': 'additional',
                'value': '9788506082645'
            }],
            'disable_on_matching': False,
            'offer_title': 'Viva - o poder da musica - Melhoramentos',
            'grade': 10,
            'navigation_id': '6453998',
            'matching_strategy': 'OMNILOGIC',
            'md5': 'a85c6060eddb1238ec54f3eea104bdf6',
            'last_updated_at': '2019-04-11T12:26:23.809380',
            'isbn': '9788506082645',
            'main_category': {
                'id': 'LI',
                'subcategory': {
                    'id': 'LVEN'
                }
            },
            'product_hash': '42d22aa9caa539496dbb5cd77a0a270b',
            'source': 'magalu'
        }

    @classmethod
    def magazineluiza_sku_222786900(cls):
        return {
            'active': True,
            'brand': 'Melhoramentos',
            'categories': [{
                'id': 'LI',
                'subcategories': [{
                    'id': 'LVEN'
                }, {
                    'id': 'LVIN'
                }, {
                    'id': 'LLTJ'
                }]
            }],
            'created_at': '2019-03-23T08:14:26.573000',
            'description': '\'O Poder da Música\' é um livro superdivertido, com lindas ilustrações, um cenário gigante e 12 miniaturas incríveis!',  # noqa
            'dimensions': {
                'depth': 0.26,
                'height': 0.04,
                'weight': 0.7,
                'width': 0.21
            },
            'ean': '9788506082645',
            'main_category': {
                'id': 'LI',
                'subcategory': {
                    'id': 'LVEN'
                }
            },
            'main_variation': False,
            'parent_sku': '2227869',
            'reference': '',
            'review_count': 0,
            'review_score': 0,
            'selections': {
                '0': ['22038']
            },
            'seller_description': 'Magazine Luiza',
            'seller_id': 'magazineluiza',
            'sku': '222786900',
            'sold_count': 0,
            'title': 'Livro - O poder da música',
            'type': 'product',
            'updated_at': '2019-05-05T22:04:34.137000',
            'disable_on_matching': False,
            'offer_title': 'O poder da música - Viva, A vida é uma festa',
            'grade': 1010,
            'navigation_id': '222786900',
            'matching_strategy': 'OMNILOGIC',
            'md5': '132a7d88a76e50e4428cc88bd1ad9d62',
            'last_updated_at': '2019-10-01T18:12:46.613405',
            'sells_to_company': True,
            'isbn': '9788506082645',
            'store_pickup_available': False,
            'delivery_plus_1': True,
            'delivery_plus_2': False,
            'product_hash': '42d22aa9caa539496dbb5cd77a0a270b',
            'source': 'magalu'
        }

    @classmethod
    def book7_sku_9788506082645(cls):
        return {
            'seller_id': 'book7',
            'sku': '9788506082645',
            'sells_to_company': True,
            'ean': '9788506082645',
            'seller_description': 'Book7',
            'parent_sku': '9788506082645',
            'type': 'product',
            'main_variation': True,
            'title': 'Livro - O poder da música',
            'description': '\'O Poder da Música\' é um livro superdivertido, com lindas ilustrações, um cenário gigante e 12 miniaturas incríveis!',  # noqa
            'reference': '',
            'brand': 'Melhoramentos',
            'sold_count': 0,
            'review_count': 0,
            'review_score': 0,
            'categories': [{
                'id': 'LI',
                'subcategories': [{
                    'id': 'LVEN'
                }, {
                    'id': 'LVIN'
                }, {
                    'id': 'LLTJ'
                }]
            }],
            'dimensions': {
                'width': 0.24,
                'depth': 0.28,
                'weight': 0.8,
                'height': 0.05
            },
            'release_date': '2019-09-04T14:56:29.275468+00:00',
            'updated_at': '2019-09-04T14:56:18.084407+00:00',
            'created_at': '2019-09-04T14:56:18.073888+00:00',
            'attributes': [],
            'disable_on_matching': False,
            'offer_title': 'O poder da música - Melhoramentos',
            'grade': 10,
            'matching_strategy': 'OMNILOGIC',
            'navigation_id': 'chk0815383',
            'md5': '92f5f8adb83a4723d8d607963c202f24',
            'last_updated_at': '2019-09-04T14:56:32.188117',
            'isbn': '9788506082645',
            'main_category': {
                'id': 'LI',
                'subcategory': {
                    'id': 'LVEN'
                }
            },
            'product_hash': '42d22aa9caa539496dbb5cd77a0a270b',
            'source': 'magalu'
        }

    @classmethod
    def decorvida_sku_5489(cls):
        return {
            'sells_to_company': True,
            'ean': '7898318007971',
            'seller_id': 'decorvida',
            'seller_description': 'Decor Vida',
            'sku': '5489',
            'parent_sku': '5489',
            'type': 'product',
            'main_variation': True,
            'title': 'Mesa cavalet 2 gavetas retrô Nature MovelBento',
            'description': 'Mesa cavalet 2 gavetas retrô <br>  Design moderno e inovador, combina com qualquer ambiente, mescla o retrô com o atual.<br>  CARACTERÍSTICAS <br>  Garantia: 3 meses contra defeito de fabricação <br> Itens inclusos: 1 mesa e manual de montagem <br> Necessita Montagem <br> Sistema de Montagem: Dificuldade Média - Pode ser montado por 1 ou 2 pessoas <br> Suporta até (kg) 25 Kg <br> Tipo de Madeira Maciça da Base: MDP 15mm caixa <br> Acabamento da Base: Pintura UV <br> Pés: MDP 25 mm pé <br> Puxador: puxador ABS <br> Fundo: 3 mm costas <br> Escala de Brilho: Brilhante <br> Material Principal: MDP 15mm caixa <br>  Limpeza: Utilize pano umedecido com água. <br> MEDIDAS E PESO DO PRODUTO <br> Altura: 78 cm <br> Largura: 50 cm <br> Profundidade: 120 cm <br> Peso: 24 Kg <br>',  # noqa
            'reference': 'Móveis bento',
            'brand': 'Móveis Bento',
            'sold_count': 0,
            'review_count': 0,
            'review_score': 0,
            'categories': [{
                'id': 'MO',
                'subcategories': [{
                    'id': 'MSES'
                }]
            }],
            'dimensions': {
                'width': 0.5,
                'depth': 1.2,
                'weight': 24,
                'height': 0.78
            },
            'release_date': '2019-10-24T21:39:22.174917+00:00',
            'updated_at': '2019-06-26T13:33:05.510189+00:00',
            'created_at': '2019-06-26T13:33:05.499537+00:00',
            'attributes': [],
            'disable_on_matching': False,
            'offer_title': 'Mesa cavalet 2 gavetas retrô Nature MovelBento - Móveis bento',  # noqa
            'grade': 10,
            'navigation_id': 'gj461cjeg6',
            'matching_strategy': 'SINGLE_SELLER',
            'md5': '04c993bf8edc8f3543899241f5182257',
            'last_updated_at': '2019-10-24T21:39:24.801024',
            'main_category': {
                'id': 'MO',
                'subcategory': {
                    'id': 'MSES'
                }
            }
        }

    @classmethod
    def magazineluiza_sku_229221800(cls):
        return {
            'active': True,
            'brand': 'sony',
            'bundles': {
                '043078100': {
                    'price': '2397.60',
                    'quantity': 1
                },
                '043183600': {
                    'price': '1.00',
                    'quantity': 1
                }
            },
            'categories': [
                {
                    'id': 'GA',
                    'subcategories': [
                        {
                            'id': 'GPS4'
                        }
                    ]
                }
            ],
            'created_at': '2019-12-11T14:01:49.503000',
            'description': '',
            'dimensions': {
                'depth': 0.46,
                'height': 0.39,
                'weight': 0.0,
                'width': 0.44
            },
            'ean': '',
            'main_category': {
                'id': 'GA',
                'subcategory': {
                    'id': 'GPS4'
                }
            },
            'main_variation': False,
            'parent_sku': '2292219',
            'reference': 'com 1 Jogo + Controle PS4 Sem Fio Dualshock 4',
            'review_count': 0,
            'review_score': 0.0,
            'selections': {
                '0': [
                    '17637',
                    '18786',
                    '19107',
                    '19108'
                ],
                '12966': [
                    '16734',
                    '16737'
                ]
            },
            'seller_description': 'Magazine Luiza',
            'seller_id': 'magazineluiza',
            'sku': '229221800',
            'sold_count': 0,
            'title': 'Playstation 4 1TB 1 Controle Sony ',
            'type': 'bundle',
            'disable_on_matching': False,
            'offer_title': 'Playstation 4 1TB 1 Controle Sony - com 1 Jogo + '
                           'Controle PS4 Sem Fio Dualshock 4 '
        }

    @classmethod
    def _1000store_sku_55313(cls):
        return {
            'seller_id': '1000store',
            'sku': '55313',
            'sells_to_company': False,
            'ean': '9788542620719',
            'seller_description': '1000 Store',
            'parent_sku': '55313',
            'type': 'product',
            'main_variation': True,
            'title': 'Batman renascimento 29 - Não informado',
            'description': 'Batman: Renascimento - 29 - O retorno da dulpa-dinâmica! - Dc comics',  # noqa
            'reference': '',
            'brand': 'Não informado',
            'sold_count': 0,
            'review_count': 0,
            'review_score': 0,
            'categories': [{
                'id': 'LI',
                'subcategories': [{
                    'id': 'HQLV'
                }]
            }],
            'dimensions': {
                'width': 0.2,
                'depth': 0.3,
                'weight': 1,
                'height': 0.3
            },
            'release_date': '2020-03-23T23:09:37.457638+00:00',
            'updated_at': '2020-03-23T23:09:37.384585+00:00',
            'created_at': '2019-11-15T20:06:12.854881+00:00',
            'attributes': [],
            'disable_on_matching': False,
            'offer_title': 'Batman renascimento 29 - Não informado',
            'grade': 10,
            'matching_strategy': 'OMNILOGIC',
            'navigation_id': 'bkc899e61c',
            'md5': '73d04e20379aa4ddc0e11108d9d5b92e',
            'last_updated_at': '2020-03-23T23:09:42.932654',
            'isbn': '9788542620719',
            'main_category': {
                'id': 'LI',
                'subcategory': {
                    'id': 'HQLV'
                }
            },
            'product_hash': 'c6656562539e82123f4622edabeccc98',
            'source': 'magalu',
            'product': 'c6656562539e82123f4622edabeccc98'
        }

    @classmethod
    def _1000store_sku_55316(cls):
        return {
            'seller_id': '1000store',
            'sku': '55316',
            'sells_to_company': False,
            'ean': '9788542620719',
            'seller_description': '1000 Store',
            'parent_sku': '55316',
            'type': 'product',
            'main_variation': True,
            'title': 'Batman renascimento 29 - Não informado',
            'description': 'Batman: Renascimento - 29 - O retorno da dulpa-dinâmica! - Dc comics',  # noqa
            'reference': '',
            'brand': 'Não informado',
            'sold_count': 0,
            'review_count': 0,
            'review_score': 0,
            'categories': [{
                'id': 'LI',
                'subcategories': [{
                    'id': 'HQLV'
                }]
            }],
            'dimensions': {
                'width': 0.2,
                'depth': 0.3,
                'weight': 1,
                'height': 0.3
            },
            'release_date': '2020-03-23T23:09:27.810415+00:00',
            'updated_at': '2020-03-23T23:09:27.713556+00:00',
            'created_at': '2019-11-15T20:06:16.240484+00:00',
            'attributes': [],
            'disable_on_matching': False,
            'offer_title': 'Batman renascimento 29 - Não informado',
            'grade': 10,
            'matching_strategy': 'OMNILOGIC',
            'navigation_id': 'dhjb75ck12',
            'md5': 'e47a6d1590271cf3a2806706e1ce2fd6',
            'last_updated_at': '2020-03-23T23:09:29.301218',
            'isbn': '9788542620719',
            'main_category': {
                'id': 'LI',
                'subcategory': {
                    'id': 'HQLV'
                }
            },
            'product_hash': 'c6656562539e82123f4622edabeccc98',
            'source': 'magalu',
            'product': 'c6656562539e82123f4622edabeccc98'
        }

    @classmethod
    def magazineluiza_sku_225300068(cls):
        return {
            'active': False,
            'attributes': [{
                'type': 'color',
                'value': 'Branco / Azul'
            }],
            'brand': 'Planeta',
            'categories': [{
                'id': 'LI',
                'subcategories': [{
                    'id': 'LIAJ'
                }, {
                    'id': 'LDSS'
                }]
            }],
            'created_at': '2020-02-06T04:36:17.580000',
            'description': 'A epigenética é uma das descobertas mais importantes no campo da biologia nos últimos anos porque muda o nosso\nentendimento sobre a genética. Até então, os cientistas acreditavam que os homens e os animais eram um produto\nexclusivamente de seus genes. Se o filho herdou os genes de uma determinada doença de seu pai, ele está fadado\na desenvolver tal doença. Nem sempre... A epigenética mostra que o DNA pode também ser influenciado pelo nosso\ncomportamento.\nNeste livro, o cientista francês Joël de Rosnay, um dos expoentes neste ramo da biologia, explica o escopo dessa revolução\ncientífica e ensina o que é possível fazer para ter um equilíbrio físico e mental. Ele oferece conselhos para uma boa\nnutrição, redução do estresse, exercício físico e ressalta a importância das relações familiares e sociais e de termos prazer\ncom o que fazemos.\nA partir da epigenética, nós nos tornamos ainda mais responsáveis pelo que fazemos com nós mesmos – afinal, podemos\n“administrar” o nosso corpo e a nossa saúde. Rosnay nos alerta sobre essa enorme responsabilidade e ensina como\nusufruir dela.',  # noqa
            'dimensions': {
                'depth': 0.33,
                'height': 0.24,
                'weight': 1.27,
                'width': 0.28
            },
            'ean': '9788542218640',
            'main_category': {
                'id': 'LI',
                'subcategory': {
                    'id': 'LIAJ'
                }
            },
            'main_variation': False,
            'parent_sku': '2253000',
            'reference': '',
            'review_count': 0,
            'review_score': 0,
            'selections': {
                '0': ['22038']
            },
            'seller_description': 'Magalu',
            'seller_id': 'magazineluiza',
            'sku': '225300068',
            'sold_count': 0,
            'title': 'Livro - A sinfonia da vida',
            'type': 'product',
            'updated_at': '2020-02-27T15:35:48.923000',
            'disable_on_matching': True,
            'offer_title': 'Livro - A sinfonia da vida',
            'grade': 1010,
            'navigation_id': '225300068',
            'matching_strategy': 'OMNILOGIC',
            'md5': 'c47ca64e0a079b2da4ea4dd186617757',
            'last_updated_at': '2020-04-07T23:50:52.385617',
            'sells_to_company': True,
            'isbn': '9788542218640',
            'store_pickup_available': False
        }

    @classmethod
    def magazineluiza_sku_225620500(cls):
        return {
            'updated_at': '2020-04-03T12:13:34.483000',
            'seller_description': 'Magalu',
            'review_score': 0,
            'description': 'A epigenética é uma das descobertas mais importantes no campo da biologia nos últimos anos porque muda o nosso\nentendimento sobre a genética. Até então, os cientistas acreditavam que os homens e os animais eram um produto\nexclusivamente de seus genes. Se o filho herdou os genes de uma determinada doença de seu pai, ele está fadado\na desenvolver tal doença. Nem sempre... A epigenética mostra que o DNA pode também ser influenciado pelo nosso\ncomportamento.\nNeste livro, o cientista francês Joël de Rosnay, um dos expoentes neste ramo da biologia, explica o escopo dessa revolução\ncientífica e ensina o que é possível fazer para ter um equilíbrio físico e mental. Ele oferece conselhos para uma boa\nnutrição, redução do estresse, exercício físico e ressalta a importância das relações familiares e sociais e de termos prazer\ncom o que fazemos.\nA partir da epigenética, nós nos tornamos ainda mais responsáveis pelo que fazemos com nós mesmos – afinal, podemos\n“administrar” o nosso corpo e a nossa saúde. Rosnay nos alerta sobre essa enorme responsabilidade e ensina como\nusufruir dela.',  # noqa
            'main_variation': False,
            'dimensions': {
                'height': 0.21,
                'width': 0.14,
                'depth': 0.02,
                'weight': 0.26
            },
            'main_category': {
                'id': 'LI',
                'subcategory': {
                    'id': 'LIAJ'
                }
            },
            'ean': '9788542218640',
            'categories': [{
                'id': 'LI',
                'subcategories': [{
                    'id': 'LIAJ'
                }, {
                    'id': 'LDSS'
                }]
            }],
            'selections': {
                '0': ['22038']
            },
            'reference': '',
            'type': 'product',
            'title': 'Livro - A sinfonia da vida',
            'sold_count': 0,
            'review_count': 0,
            'active': True,
            'sku': '225620500',
            'parent_sku': '2256205',
            'seller_id': 'magazineluiza',
            'brand': 'Planeta',
            'created_at': '2020-04-02T04:37:03.127000',
            'disable_on_matching': False,
            'offer_title': 'Livro - A sinfonia da vida',
            'grade': 10,
            'navigation_id': '225620500',
            'matching_strategy': 'OMNILOGIC',
            'md5': '0c90c0cae83632fcdcb4b5a9c5cf4ab1',
            'last_updated_at': '2020-04-07T20:54:30.985895',
            'sells_to_company': True,
            'isbn': '9788542218640',
            'store_pickup_available': False
        }

    @classmethod
    def livrariabaluarte_sku_7576847209(cls):
        return {
            'seller_id': 'livrariabaluarte',
            'sku': '7576847209',
            'sells_to_company': True,
            'ean': '9788542218800',
            'seller_description': 'Livraria Baluarte',
            'parent_sku': '7576847209',
            'type': 'product',
            'main_variation': True,
            'title': 'Livro - La casa de papel',
            'description': 'Escape book baseado na série La casa de papel\nSergio Marquina, mais conhecido como “o Professor”, líder do maior roubo da história da Espanha, passou parte de sua\ninfância e adolescência no hospital de San Juan de Dios de San Sebastián, onde se tornou amigo de Jero Lamarca. Nos\npiores dias de Jero, Sergio, que já revelava ter uma mente privilegiada, criou jogos para manter sua amigo acordado.\nQuando Sergio se perdia nos pensamentos, era Jero que o trazia de volta ensinando-o a fazer dobraduras de papel. Já\nfaz um tempo desde o roubo milionário na Casa da Moeda. Hoje, enquanto junta as poucas coisas restantes na oficina de\nmotocicletas prestes a fechar, Jero recebe um pacote. No interior, uma carta não assinada, um caderno, uma caixa fechada\ncom cadeado, uma foto de uma máscara de Dalí e uma gravata vermelha. Jero não tem dúvidas. Lá fora, Sergio Marquina\no deixou um tesouro escondido, uma nova oportunidade. Ele só precisa desvendar as pistas para encontrá-lo.\nE você?\nSerá capaz de chegar ao final?',  # noqa
            'reference': '',
            'brand': 'Outro Planeta',
            'sold_count': 0,
            'review_count': 0,
            'review_score': 0,
            'categories': [{
                'id': 'LI',
                'subcategories': [{
                    'id': 'LLIT'
                }, {
                    'id': 'LVEN'
                }]
            }],
            'dimensions': {
                'width': 0.16,
                'depth': 0.03,
                'weight': 0.5,
                'height': 0.23
            },
            'release_date': '2020-02-28T13:43:12.067260+00:00',
            'updated_at': '2020-02-28T13:43:11.829988+00:00',
            'created_at': '2020-02-28T13:41:57.212135+00:00',
            'attributes': [],
            'disable_on_matching': False,
            'offer_title': 'Livro - La casa de papel',
            'grade': 10,
            'matching_strategy': 'OMNILOGIC',
            'navigation_id': 'ce9729d4k0',
            'md5': 'b25e154817f6581bf081bc1ed58a2f75',
            'last_updated_at': '2020-02-28T13:43:17.132431',
            'isbn': '9788542218800',
            'main_category': {
                'id': 'LI',
                'subcategory': {
                    'id': 'LLIT'
                }
            },
            'product_hash': 'db5e6707ab242955bfbac9324b0c3640',
            'source': 'magalu'
        }

    @classmethod
    def lojasages_sku_5973(cls):
        return {
            'sells_to_company': True,
            'ean': '7506339384673',
            'seller_id': 'lojasages',
            'seller_description': 'Sages',
            'sku': '5973',
            'parent_sku': '34066812',
            'type': 'product',
            'main_variation': True,
            'title': 'Aparelho de Barbear Gillette Prestobarba 3 Leve 8 Pague 7',  # noqa
            'description': '<br>Aparelho de Barbear Gillette Prestobarba 3 Leve 8 Pague 7<br>',  # noqa
            'reference': '',
            'brand': 'Gillette',
            'sold_count': 0,
            'review_count': 0,
            'review_score': 0,
            'categories': [
                {
                    'id': 'ME',
                    'subcategories': [
                        {
                            'id': 'APDB'
                        },
                        {
                            'id': 'PRHP'
                        },
                        {
                            'id': 'PRHI'
                        }
                    ]
                }
            ],
            'dimensions': {
                'width': 0.11,
                'depth': 0.05,
                'weight': 0.2,
                'height': 0.21
            },
            'release_date': '2020-07-16T17:12:34.403687+00:00',
            'updated_at': '2020-07-16T17:12:34.071718+00:00',
            'created_at': '2019-10-23T07:23:23.451591+00:00',
            'attributes': [
                {
                    'type': 'quantity',
                    'value': '2'
                }
            ],
            'disable_on_matching': False,
            'offer_title': 'Aparelho de Barbear Gillette Prestobarba 3 Leve 8 Pague 7',  # noqa
            'grade': 10,
            'navigation_id': 'kh18566g08',
            'matching_strategy': 'SINGLE_SELLER',
            'md5': '5e91afa8bd37e8bedc669f849af9b56f',
            'last_updated_at': '2020-07-16T17:14:22.882450',
            'main_category': {
                'id': 'ME',
                'subcategory': {
                    'id': 'APDB'
                }
            }
        }

    @classmethod
    def magazineluiza_sku_124383200(cls):
        return {
            'active': True,
            'brand': 'Plumatex',
            'categories': [{
                'id': 'CO',
                'subcategories': [{
                    'id': 'CCBC'
                }, {
                    'id': 'CHCX'
                }]
            }],
            'created_at': '2019-07-23T09:41:21.313000',
            'description': 'O Colchão casal Prime da Plumatex com 25cm de altura apresenta um nível de conforto diferenciado, sendo confeccionado com Sistema de Molas SLHS Superlastic, sistema no qual o Molejo é composto por fios de aço bitemperados contínuos, com o entrelaçamento das molas entre si, o que proporciona uma maior resistência bem como o suporte ideal para o corpo. Este sistema de molejo é o mais utilizado no mercado norte-americano, um dos mais exigentes do mundo. Seu estofamento é composto por espuma D-26 selada de ótima qualidade, e certificada pelo INMETRO. Este colchão possui uma perfeita sustentação para a coluna vertebral, sendo adaptado para todos os Biotipos de usuários. Cuidado, proteção, tecnologia e conforto para um descanso muito mais tranquilo e saudável com o colchão da Plumatex.',  # noqa
            'dimensions': {
                'depth': 1.88,
                'height': 0.25,
                'weight': 16.05,
                'width': 1.38
            },
            'ean': '7899918725777',
            'main_category': {
                'id': 'CO',
                'subcategory': {
                    'id': 'CCBC'
                }
            },
            'main_variation': False,
            'parent_sku': '1243832',
            'reference': 'Prime',
            'review_count': 0,
            'review_score': 0,
            'selections': {
                '0': ['17637', '18787'],
                '12966': ['16734', '16737']
            },
            'seller_description': 'Magalu',
            'seller_id': 'magazineluiza',
            'sku': '124383200',
            'sold_count': 0,
            'title': 'Colchão Casal Plumatex Mola 25cm de Altura',
            'type': 'product',
            'updated_at': '2020-06-08T03:00:03.870000',
            'disable_on_matching': False,
            'offer_title': 'Colchão Casal Plumatex Mola 25cm de Altura - Prime',  # noqa
            'grade': 1010,
            'navigation_id': '124383200',
            'matching_strategy': 'SINGLE_SELLER',
            'md5': 'bb7686621f7c8db3e5330c6c8db981ad',
            'last_updated_at': '2020-06-08T06:07:46.087912',
            'sells_to_company': True,
            'store_pickup_available': False
        }

    @classmethod
    def magazineluiza_sku_124383300(cls):
        return {
            'active': True,
            'brand': 'Plumatex',
            'categories': [{
                'id': 'CO',
                'subcategories': [{
                    'id': 'BTCL'
                }, {
                    'id': 'CBTT'
                }]
            }],
            'created_at': '2019-07-24T10:13:35.493000',
            'description': 'Sabia que é a base pra cama box que garante conforto, segurança e a sustentação ideal pro seu colchão? Além disso, é bom dizer que a base vem apenas com espaço para colocar o colchão. Ou seja, ela é bem diferente da cama tradicional, que vem com estrado, laterais e cabeceiras. A Base Cama Box de casal Prime da Plumatex possui 37cm de altura e deixará seu sono ainda mais seguro, sustentando o colchão com mais firmeza e tudo isso sem deixar de lado a beleza, pois ele vem com design clean e que dá um toque a mais de beleza para o seu quarto.',  # noqa
            'dimensions': {
                'depth': 1.88,
                'height': 0.25,
                'weight': 28.85,
                'width': 1.38
            },
            'ean': '7899918725654',
            'main_category': {
                'id': 'CO',
                'subcategory': {
                    'id': 'BTCL'
                }
            },
            'main_variation': False,
            'parent_sku': '1243833',
            'reference': 'Prime',
            'review_count': 0,
            'review_score': 0,
            'selections': {
                '0': ['17637', '18787'],
                '12966': ['16734', '16737']
            },
            'seller_description': 'Magalu',
            'seller_id': 'magazineluiza',
            'sku': '124383300',
            'sold_count': 0,
            'title': 'Base Cama Box Casal Plumatex 37cm de Altura',
            'type': 'product',
            'updated_at': '2020-06-05T12:17:23.987000',
            'disable_on_matching': False,
            'offer_title': 'Base Cama Box Casal Plumatex 37cm de Altura - Prime',  # noqa
            'grade': 1010,
            'navigation_id': '124383300',
            'matching_strategy': 'SINGLE_SELLER',
            'md5': '3a78e6f64ee6c367bf9c087c303838ee',
            'last_updated_at': '2020-06-05T15:22:14.748677',
            'sells_to_company': True,
            'store_pickup_available': False,
            'delivery_plus_1': True,
            'delivery_plus_2': False
        }

    @classmethod
    def magazineluiza_sku_229219300(cls):
        return {
            'active': True,
            'brand': 'plumatex',
            'bundles': {
                '124383200': {
                    'price': '498.00',
                    'quantity': 1
                },
                '124383300': {
                    'price': '250.00',
                    'quantity': 1
                }
            },
            'categories': [{
                'id': 'MO',
                'subcategories': [{
                    'id': 'CAMO'
                }, {
                    'id': 'MCAM'
                }, {
                    'id': 'MCQA'
                }]
            }],
            'created_at': '2019-11-22T17:52:11.243000',
            'description': '',
            'dimensions': {
                'depth': 0.46,
                'height': 0.39,
                'weight': 0,
                'width': 0.44
            },
            'ean': '',
            'main_category': {
                'id': 'MO',
                'subcategory': {
                    'id': 'CAMO'
                }
            },
            'main_variation': False,
            'parent_sku': '2292193',
            'reference': '25cm de Altura',
            'review_count': 0,
            'review_score': 0,
            'selections': {
                '0': ['17637', '18787'],
                '12966': ['16734', '16737']
            },
            'seller_description': 'Magalu',
            'seller_id': 'magazineluiza',
            'sku': '229219300',
            'sold_count': 0,
            'title': 'Cama Box Casal (Box + Colchão) Plumatex Mola',
            'type': 'bundle',
            'disable_on_matching': False,
            'offer_title': 'Cama Box Casal (Box + Colchão) Plumatex Mola - 25cm de Altura',  # noqa
            'grade': 0,
            'navigation_id': '229219300',
            'matching_strategy': 'SINGLE_SELLER',
            'md5': '314f2c22d30d3ed53e35d3d40e960ec4',
            'last_updated_at': '2020-06-05T13:18:34.341427',
            'sells_to_company': True,
            'store_pickup_available': False
        }

    @classmethod
    def ateliefestaemagia_sku_4795_251(cls):
        return {
            'sells_to_company': True,
            'ean': '',
            'seller_id': 'ateliefestaemagia',
            'seller_description': 'Ateliê Festa e Magia',
            'sku': '4795-251',
            'parent_sku': '4795',
            'type': 'product',
            'main_variation': True,
            'title': 'Kit festa Moana 61 peças + 1 vela de numerada de aniversário',  # noqa
            'description': 'Kit Festa com 6 peças + 1 Vela Numerada . Envio Imediato. <br> Este Kit contém: 1 Vela de aniversário numerada de 8 cm de parafina com glitter ( Por favor selecionar cor e número no momento da compra ) <br> 1 topo de bolo de tamanho aproximado de 18 cm ( impresso a laser em papel offset de 240g ) 5 peças decorativas tamanho aproximado 8 x 8 cm cm ( impresso a laser papel offset 180g ) Este Kit Não acompanha os doces . OBS : O envio é imediato, por esse motivo não personalizamos com nome ou idade. Os nossos produtos possuem imagens impressas com alta definição a laser. Por favor leia com atenção a descrição do anúncio antes de concluir a compra. Caso tenha dúvidas envie a sua pergunta antes de finalizar o pedido . Concluída a compra, não podemos efetuar alterações no pedido. Ele será encaminhado imediatamente conforme o anúncio . Em caso de feriados e finais de semana o seu pedido será encaminhado no próximo dia útil. Fique atento ao prazo de entrega informado. É muito importante que você receba seu produto dentro do prazo.',  # noqa
            'reference': 'Produto Artesanal',
            'brand': 'Produto artesanal',
            'sold_count': 0,
            'review_count': 0,
            'review_score': 0,
            'categories': [{
                'id': 'AF',
                'subcategories': [{
                    'id': 'KDDF'
                }, {
                    'id': 'DFES'
                }]
            }],
            'dimensions': {
                'width': 0.2,
                'depth': 0.2,
                'weight': 0.4,
                'height': 0.2
            },
            'release_date': '2020-09-18T03:14:36.159935+00:00',
            'updated_at': '2020-09-18T03:14:36.084520+00:00',
            'created_at': '2020-09-15T18:27:00.627489+00:00',
            'attributes': [{
                'type': 'color',
                'value': 'azul'
            }, {
                'type': 'size',
                'value': '1'
            }],
            'disable_on_matching': False,
            'offer_title': 'Kit festa Moana 61 peças + 1 vela de numerada de aniversário - Produto Artesanal',  # noqa
            'grade': 0,
            'navigation_id': 'ebkbbch779',
            'matching_strategy': 'SINGLE_SELLER',
            'md5': '48b43addf47a452ed230fd6399b7b8f6',
            'last_updated_at': '2020-09-18T03:14:37.897512',
            'main_category': {
                'id': 'AF',
                'subcategory': {
                    'id': 'KDDF'
                }
            }
        }

    @classmethod
    def kabum_sku_102632(cls):
        return {
            'seller_id': 'kabum',
            'sku': '102632',
            'sells_to_company': False,
            'ean': '7893299917738',
            'seller_description': 'KaBuM!',
            'parent_sku': '102632',
            'type': 'product',
            'main_variation': True,
            'title': 'Monitor Profissional LG 32',
            'description': 'Desfrute de uma incrível qualidade de imagem com o monitor LG e se surpreenda com o HDR10. A alta gama de cores e com resolução 4k é facilmente superior quando comparado a monitores convencionais. Com a tecnologia AMD Radeon FreeSync você aproveitará ainda mais das imagens do Monitor LG, eliminando os cortes e repetições de imagem.',  # noqa
            'reference': '',
            'brand': 'LG',
            'sold_count': 0,
            'review_count': 0,
            'review_score': 0,
            'categories': [
                {
                    'id': 'IN',
                    'subcategories': [
                        {
                            'id': 'MLCD'
                        },
                        {
                            'id': 'MNPC'
                        }
                    ]
                }
            ],
            'dimensions': {
                'width': 0.22,
                'depth': 0.82,
                'weight': 18.792,
                'height': 0.5
            },
            'release_date': '2021-09-21T16:03:32.288919+00:00',
            'updated_at': '2021-09-21T16:03:32.218258+00:00',
            'created_at': '2021-08-16T18:43:31.886669+00:00',
            'attributes': [],
            'disable_on_matching': False,
            'offer_title': 'Monitor Profissional LG 32',
            'grade': 20,
            'matching_strategy': 'SINGLE_SELLER',
            'navigation_id': 'bc77d9gk26',
            'md5': '609d514685ee4fab1c9fa26deafd9956',
            'last_updated_at': '2021-09-21T16:03:34.085247',
            'source': 'wakko',
            'main_category': {
                'id': 'IN',
                'subcategory': {
                    'id': 'MLCD'
                }
            },
            'price': {
                'seller_id': 'kabum',
                'sku': '102632',
                'list_price': 4333.22,
                'price': 4333.22,
                'delivery_availability': 'nationwide',
                'stock_count': 5,
                'stock_type': 'on_seller',
                'last_updated_at': '2021-09-23T21:50:13.933880',
                'md5': '590708c90a6f00aa8b5e79881dc5052a',
                'source': 'price'
            },
            'media': {
                'images': [
                    '/{w}x{h}/monitor-profissional-lg-32-va-led-wide-4k-uhd-hdr-600-95-dci-p3-hdmi-displayport-color-calibrated-som-integrado-32ul750-w/kabum/102632/03d303861a9904560e95d62441082e9b.jpg'  # noqa
                ]
            }
        }

    @classmethod
    def product_magazineluiza_230382400(cls):
        return {
            'active': True,
            'brand': 'principis',
            'categories': [
                {
                    'id': 'LI',
                    'subcategories': [
                        {
                            'id': 'LLIT'
                        }
                    ]
                }
            ],
            'created_at': '2021-05-19T04:33:30.143000',
            'description': '',
            'dimensions': {
                'depth': 0.06,
                'height': 0.23,
                'weight': 1.025,
                'width': 0.16
            },
            'ean': '7908312102418',
            'isbn': '7908312102418',
            'main_category': {
                'id': 'LI',
                'subcategory': {
                    'id': 'LLIT'
                }
            },
            'main_variation': False,
            'parent_sku': '2303824',
            'reference': '',
            'review_count': 0,
            'review_score': 0,
            'selections': {
                '0': [
                    '22038'
                ]
            },
            'seller_description': 'Magalu',
            'seller_id': 'magazineluiza',
            'sku': '230382400',
            'sold_count': 0,
            'title': 'Box Livros Eça de Queirós Vol. 1 ',
            'type': 'product',
            'updated_at': '2022-06-08T15:47:35.137000',
            'disable_on_matching': False,
            'offer_title': 'Box Livros Eça de Queirós Vol. 1 ',
            'grade': 1010,
            'navigation_id': '230382400',
            'matching_strategy': 'SINGLE_SELLER',
            'md5': '41ece4972b93620b1c9fc66e3b048349',
            'last_updated_at': '2022-06-08T19:57:40.816108'
        }
