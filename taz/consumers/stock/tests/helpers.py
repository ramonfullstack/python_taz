
def create_stock_payload(sku, cd, description):
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
                'sku': sku,
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
                'id': int(cd),
                'type': {
                    'description': description
                },
                'latitude': -23.131369,
                'longitude': -46.95137
            },
            'position': {
                'new': {
                    'levels': [{
                        'physic': {
                            'amount': 6,
                            'reserved': 2,
                            'available': 5
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
                            'amount': 4,
                            'reserved': 2,
                            'available': 4
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
