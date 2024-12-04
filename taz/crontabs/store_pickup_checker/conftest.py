import pytest


@pytest.fixture
def apiluiza_response_content():
    return {
        'records': [
            {
                'states': [
                    {
                        'name': 'AL',
                        'cities': [
                            {
                                'name': 'ARAPIRACA',
                                'districts': [
                                    {
                                        'stores': [{
                                            'id': 729,
                                            'tradingName': 'AR729',
                                            'cnpj': '47960950081962',
                                            'ie': '242694195',
                                            'type': {
                                                'id': 1,
                                                'description': 'Convencional' # noqa
                                            },
                                            'region': {
                                                'id': 42,
                                                'description': 'MACEIO'
                                            },
                                            'address': {
                                                'street': 'MANOEL ANDRE',
                                                'number': 105,
                                                'zipCode': '57300005'
                                            },
                                            'phones': {
                                                'areaCode': 82,
                                                'commercial': '35292600'
                                            },
                                            'geoLocation': {
                                                'latitude': -9.750622,
                                                'longitude': -36.659513,
                                                'distance': 0,
                                                'outOfRadius': False
                                            },
                                            'primaryDistributionCenter': 991, # noqa
                                            'pickupAvailability': {
                                                'totalNumberOfDays': 4,
                                                'details': {
                                                    'distributionCenterOperationTime': 2, # noqa
                                                    'supplyTimeInterval': 2, # noqa
                                                    'factorCalculation': 5,
                                                    'additionalOperationTimeFromDc': 0 # noqa
                                                },
                                                'stockType': 'dc'
                                            },
                                            'openingHours': {
                                                'saturday': {
                                                    'opening': '08:00',
                                                    'closing': '15:00'
                                                },
                                                'workingDays': {
                                                    'opening': '08:00',
                                                    'closing': '18:00'
                                                }
                                            },
                                            'shippingRates': {
                                                'operatingCost': '0.00',
                                                'customerCost': '0.00'
                                            },
                                            'distributionCenterSupplyMain': { # noqa
                                                'id': 997
                                            }
                                        }]
                                    }
                                ]
                            },
                            {
                                'name': 'CORURIPE',
                                'districts': [
                                    {
                                        'stores': [{
                                            'id': 1203,
                                            'tradingName': 'CP1203',
                                            'cnpj': '47960950101076',
                                            'ie': '247310255',
                                            'type': {
                                                'id': 1,
                                                'description': 'Convencional' # noqa
                                            },
                                            'region': {
                                                'id': 42,
                                                'description': 'MACEIO'
                                            },
                                            'address': {
                                                'street': 'LINDOLFO SIMOES', # noqa
                                                'number': 436,
                                                'zipCode': '57230000'
                                            },
                                            'phones': {
                                                'areaCode': 82,
                                                'commercial': '32742200'
                                            },
                                            'geoLocation': {
                                                'latitude': -10.127432,
                                                'longitude': -36.175045,
                                                'distance': 0,
                                                'outOfRadius': False
                                            },
                                            'primaryDistributionCenter': 991, # noqa
                                            'pickupAvailability': {
                                                'totalNumberOfDays': 4,
                                                'details': {
                                                    'distributionCenterOperationTime': 2, # noqa
                                                    'supplyTimeInterval': 2, # noqa
                                                    'factorCalculation': 5,
                                                    'additionalOperationTimeFromDc': 0 # noqa
                                                },
                                                'stockType': 'dc'
                                            },
                                            'openingHours': {
                                                'saturday': {
                                                    'opening': '08:00',
                                                    'closing': '15:00'
                                                },
                                                'workingDays': {
                                                    'opening': '08:00',
                                                    'closing': '18:00'
                                                }
                                            },
                                            'shippingRates': {
                                                'operatingCost': '0.00',
                                                'customerCost': '0.00'
                                            },
                                            'distributionCenterSupplyMain': { # noqa
                                                'id': 997
                                            }
                                        }]
                                    }
                                ]
                            },
                        ]
                    },
                    {
                        'name': 'BA',
                        'cities': [
                            {
                                'name': 'ALAGOINHAS',
                                'districts': [
                                    {
                                        'stores': [{
                                            'id': 782,
                                            'tradingName': 'AG782',
                                            'cnpj': '47960950071819',
                                            'ie': '101475101',
                                            'type': {
                                                'id': 1,
                                                'description': 'Convencional' # noqa
                                            },
                                            'region': {
                                                'id': 59,
                                                'description': 'ARACAJÚ'
                                            },
                                            'address': {
                                                'street': 'PADRE ALFREDO',
                                                'number': 10,
                                                'zipCode': '48005105'
                                            },
                                            'phones': {
                                                'areaCode': 75,
                                                'commercial': '31633400'
                                            },
                                            'geoLocation': {
                                                'latitude': -12.13837,
                                                'longitude': -38.423156,
                                                'distance': 0,
                                                'outOfRadius': False
                                            },
                                            'primaryDistributionCenter': 991, # noqa
                                            'pickupAvailability': {
                                                'totalNumberOfDays': 8,
                                                'details': {
                                                    'distributionCenterOperationTime': 1, # noqa
                                                    'supplyTimeInterval': 1, # noqa
                                                    'factorCalculation': 5
                                                },
                                                'stockType': 'dc'
                                            },
                                            'openingHours': {
                                                'saturday': {
                                                    'opening': '08:00',
                                                    'closing': '15:00'
                                                },
                                                'workingDays': {
                                                    'opening': '08:00',
                                                    'closing': '18:00'
                                                }
                                            },
                                            'shippingRates': {
                                                'operatingCost': '0.00',
                                                'customerCost': '0.00'
                                            },
                                            'distributionCenterSupplyMain': { # noqa
                                                'id': 997
                                            }
                                        }]
                                    }
                                ]
                            },
                            {
                                'name': 'BARREIRAS',
                                'districts': [
                                    {
                                        'stores': [{
                                            'id': 853,
                                            'tradingName': 'BR853',
                                            'cnpj': '47960950071908',
                                            'ie': '101475327',
                                            'type': {
                                                'id': 1,
                                                'description': 'Convencional' # noqa
                                            },
                                            'region': {
                                                'id': 45,
                                                'description': 'ITABUNA'
                                            },
                                            'address': {
                                                'street': 'CLERISTON ANDRADE', # noqa
                                                'number': 475,
                                                'zipCode': '47800358'
                                            },
                                            'phones': {
                                                'areaCode': 77,
                                                'commercial': '36143700'
                                            },
                                            'geoLocation': {
                                                'latitude': -12.145477,
                                                'longitude': -44.992059,
                                                'distance': 0,
                                                'outOfRadius': False
                                            },
                                            'primaryDistributionCenter': 991, # noqa
                                            'pickupAvailability': {
                                                'totalNumberOfDays': 4,
                                                'details': {
                                                    'distributionCenterOperationTime': 2, # noqa
                                                    'supplyTimeInterval': 2, # noqa
                                                    'factorCalculation': 5,
                                                    'additionalOperationTimeFromDc': 0 # noqa
                                                },
                                                'stockType': 'dc'
                                            },
                                            'openingHours': {
                                                'saturday': {
                                                    'opening': '08:00',
                                                    'closing': '15:00'
                                                },
                                                'workingDays': {
                                                    'opening': '08:00',
                                                    'closing': '18:00'
                                                }
                                            },
                                            'shippingRates': {
                                                'operatingCost': '0.00',
                                                'customerCost': '0.00'
                                            },
                                            'distributionCenterSupplyMain': { # noqa
                                                'id': 997
                                            }
                                        }]
                                    }
                                ]
                            },
                        ]
                    }
                ]
            }
        ]
    }
