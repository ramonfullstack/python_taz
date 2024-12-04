import pytest


@pytest.fixture
def mock_deliveries():
    return {
        'meta': {
            'server': 'magazineluiza-prod.apigee.net',
            'limit': 1,
            'offset': 0,
            'recordCount': 1
        },
        'records': [{
            'zipCode': '02136000',
            'deliveries': [{
                'uuid': '96cb0eaa-60d7-49bc-bf8d-2249c81db982-1',
                'status': {
                    'code': 200,
                    'description': 'Shipping modals available'
                },
                'products': [{
                    'sku': '220907400',
                    'quantity': 1,
                    'stock': {
                        'id': 300,
                        'name': 'Physical',
                        'isRouteY': False
                    },
                    'value': 1099,
                    'availableForStorePickup': True,
                    'rule': {
                        'id': 6,
                        'name': 'Malha Brasil 1000000 a 19999999',
                        'provenance': 'all'
                    },
                    'campaigns': [
                        {
                            'id': 2251,
                            'name': 'PRIME CD300 PRAZO 2 PARA SP RJ PR MG SC'
                        },
                        {
                            'id': 977,
                            'name': 'FS / SP (CAPITAL E INTERIOR) / 13,90'
                        }
                    ]
                }],
                'modals': [
                    {
                        'id': 1,
                        'name': 'Convencional',
                        'branch': {
                            'id': 204,
                            'inventory': 300,
                            'inventoryOrigin': 300,
                            'departurePoint': 'cd'
                        },
                        'shippingTime': {
                            'businessDays': 1
                        },
                        'modality': {
                            'id': 1,
                            'name': 'courrier',
                            'abbreviation': 'SE',
                            'integrationCode': 'SE',
                            'skipIntegration': False
                        },
                        'shippingRates': {
                            'operatingCost': '19.23',
                            'customerCost': '13.90'
                        },
                        'inventoryType': {
                            'id': 1,
                            'name': 'Physical'
                        },
                        'zipcodeRestriction': False,
                        'type': 'conventional',
                        'expressDelivery': True
                    },
                    {
                        'id': 2,
                        'name': 'Retira loja',
                        'outOfRadius': False,
                        'modality': {
                            'id': 3,
                            'name': 'store pickup',
                            'abbreviation': 'RL'
                        },
                        'shippingRates': {
                            'operatingCost': '0.00',
                            'customerCost': '0.00'
                        },
                        'availability': {
                            'workingDays': 0
                        },
                        'stockType': 'store',
                        'type': 'pickupPoint'
                    }
                ]
            }]
        }]
    }
