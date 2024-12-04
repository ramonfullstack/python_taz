import pytest

from taz.consumers.stock.tests.helpers import create_stock_payload


@pytest.fixture
def magazineluiza_sku_044359000_cd_300():
    return {
        'event_date': '2020-05-20T19:55:27+00:00',
        'version': '1.0',
        'operation': 'UPDATE',
        'source': 'EDDIE',
        'entity_type': 'EDDIE_V1',
        'entity_hash': 'a185d18cbbb8b91f592855ea3a0c18a33d484c45d78e8194208bae1a33535e4c',  # noqa
        'entity': {
            'product': {
                'organization': {
                    'id': 'magazineluiza'
                },
                'id': 1797,
                'digit': 8,
                'sku': '044359000',
                'barcode': '7891485077938',
                'line': {
                    'id': 12
                },
                'family': {
                    'id': 3029
                }
            },
            'branch': {
                'organization': {
                    'id': 'magazineluiza'
                },
                'id': 300,
                'type': {
                    'description': 'distribution center'
                },
                'latitude': -23.131369,
                'longitude': -46.95137
            },
            'position': {
                'new': {
                    'levels': [{
                        'physic': {
                            'amount': 33,
                            'reserved': 2,
                            'available': 31
                        }
                    }, {
                        'logic': {
                            'amount': 0,
                            'reserved': 0,
                            'available': 0
                        }
                    }]
                },
                'old': {
                    'levels': [{
                        'physic': {
                            'amount': 32,
                            'reserved': 2,
                            'available': 30
                        }
                    }, {
                        'logic': {
                            'amount': 0,
                            'reserved': 0,
                            'available': 0
                        }
                    }]
                }
            }
        },
        'status': 'SUCCESS'
    }


@pytest.fixture
def magazineluiza_sku_044359000_cd_50():
    return {
        'event_date': '2020-05-20T19:55:27+00:00',
        'version': '1.0',
        'operation': 'UPDATE',
        'source': 'EDDIE',
        'entity_type': 'EDDIE_V1',
        'entity_hash': 'a185d18cbbb8b91f592855ea3a0c18a33d484c45d78e8194208bae1a33535e4c',  # noqa
        'entity': {
            'product': {
                'organization': {
                    'id': 'magazineluiza'
                },
                'id': 1797,
                'digit': 8,
                'sku': '044359000',
                'barcode': '7891485077938',
                'line': {
                    'id': 12
                },
                'family': {
                    'id': 3029
                }
            },
            'branch': {
                'organization': {
                    'id': 'magazineluiza'
                },
                'id': 50,
                'type': {
                    'description': 'distribution center'
                },
                'latitude': -23.131369,
                'longitude': -46.95137
            },
            'position': {
                'new': {
                    'levels': [{
                        'physic': {
                            'amount': 0,
                            'reserved': 2,
                            'available': 0
                        }
                    }, {
                        'logic': {
                            'amount': 0,
                            'reserved': 0,
                            'available': 0
                        }
                    }]
                },
                'old': {
                    'levels': [{
                        'physic': {
                            'amount': 0,
                            'reserved': 2,
                            'available': 0
                        }
                    }, {
                        'logic': {
                            'amount': 0,
                            'reserved': 0,
                            'available': 0
                        }
                    }]
                }
            }
        },
        'status': 'SUCCESS'
    }


@pytest.fixture
def magazineluiza_sku_044359000_cd_350():
    return create_stock_payload('044359000', 350, 'distribution center')


@pytest.fixture
def magazineluiza_sku_044359000_cd_995():
    return create_stock_payload('044359000', 995, 'distribution center')


@pytest.fixture
def magazineluiza_sku_044359000_store_595():
    return create_stock_payload('044359000', 595, 'store')


@pytest.fixture
def magazineluiza_sku_044359000_other_62():
    return create_stock_payload('044359000', 62, 'other')
