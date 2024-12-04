import copy
import datetime
import logging
import time
from io import StringIO
from unittest.mock import Mock, patch
from uuid import UUID

import pytest
import requests
from google.cloud.pubsub import PublisherClient
from pymongo import MongoClient
from redis import Redis
from simple_settings import settings

from taz import constants
from taz.consumers.core.aws.kinesis import KinesisManager
from taz.consumers.core.aws.sqs import SQSManager
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.google.storage import StorageManager
from taz.consumers.core.google.stream import StreamPublisherManager
from taz.consumers.core.kafka.producer import KafkaProducer
from taz.consumers.core.notification import Notification
from taz.consumers.core.notification_enrichment import NotificationEnrichment
from taz.core.matching.common.samples import ProductSamples
from taz.core.merge.factsheet import FactsheetMerger
from taz.core.notification.notification_sender import NotificationSender
from taz.core.storage.base_storage import BaseStorage
from taz.core.storage.factsheet_storage import FactsheetStorage
from taz.core.storage.raw_products_storage import RawProductsStorage
from taz.helpers.pagination import Pagination


@pytest.fixture(scope='session')
def mongo_connection():
    return MongoClient(settings.MONGO_URI)


@pytest.fixture(scope='session')
def mongo_database(mongo_connection):
    return getattr(mongo_connection, settings.MONGO_DATABASE)


@pytest.fixture(autouse=True)
def clean_database(mongo_database):
    [
        mongo_database.drop_collection(c)
        for c in mongo_database.list_collection_names()
        if not c.startswith('system')
    ]


@pytest.fixture
def patch_mongo_collection():
    return patch.object(MongodbMixin, 'get_collection')


@pytest.fixture
def logger_stream(request):
    stream = StringIO()
    handler = logging.StreamHandler(stream)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    def fin():
        logger.removeHandler(handler)

    request.addfinalizer(fin)
    return stream


@pytest.fixture(scope='session')
def cache_connection():
    return Redis(
        host=settings.REDIS_LOCK_SETTINGS['host'],
        port=settings.REDIS_LOCK_SETTINGS['port']
    )


@pytest.fixture(autouse=True)
def flush_cache(cache_connection):
    cache_connection.flushall()


@pytest.fixture
def patch_sqs_manager_put():
    return patch.object(SQSManager, 'put')


@pytest.fixture
def patch_notification():
    return patch.object(Notification, 'put')


@pytest.fixture
def normalized_payload():
    return {
        'entity': 'Celular',
        'product_name_metadata': [
            'Produto', 'Marca', 'Modelo', 'Conectividade'
        ],
        'category_id': 'TE',
        'subcategory_ids': ['TECE'],
        'navigation_id': '215915300',
        'sku_metadata': ['Capacidade', 'Cor'],
        'sku': '215915300',
        'source': 'magalu',
        'product_name': 'Celular Samsung Galaxy S7 4G',
        'product_matching_metadata': ['Produto', 'Marca', 'Modelo'],
        'filters_metadata': [
            'Produto', 'Marca', 'Modelo', 'Capacidade',
            'Cor', 'Conectividade',
            'Resolu\u00e7\u00e3o da C\u00e2mera', 'Tamanho da Tela'
        ],
        'product_hash': '60aaf89b372b083af6a4a7bb8549e0d5',
        'metadata': {
            'Cor': 'Preto',
            'Tamanho da Tela': '5.1 polegadas',
            'Resolu\u00e7\u00e3o da C\u00e2mera': '12MP',
            'Capacidade': '32GB',
            'Conectividade': '4G',
            'Modelo': 'Galaxy S7',
            'Marca': 'Samsung',
            'Produto': 'Celular'
        },
        'seller_id': 'magazineluiza'
    }


@pytest.fixture
def patch_publish_manager():
    return patch.object(StreamPublisherManager, 'publish')


@pytest.fixture
def patch_kafka_producer():
    return patch.object(KafkaProducer, 'producer')


@pytest.fixture
def patch_kinesis_put():
    return patch.object(KinesisManager, 'put')


@pytest.fixture
def patch_storage_manager_upload():
    return patch.object(StorageManager, 'upload')


@pytest.fixture
def patch_storage_manager_get_json():
    return patch.object(StorageManager, 'get_json')


@pytest.fixture
def patch_storage_manager_get_file():
    return patch.object(StorageManager, 'get_file')


@pytest.fixture
def patch_storage_manager_delete():
    return patch.object(StorageManager, 'delete')


@pytest.fixture
def patch_requests_get():
    return patch.object(requests, 'get')


@pytest.fixture
def patch_requests_post():
    return patch.object(requests, 'post')


@pytest.fixture
def patch_requests_put():
    return patch.object(requests, 'put')


@pytest.fixture
def patch_pubsub_client():
    return patch.object(PublisherClient, 'publish')


@pytest.fixture
def patch_bucket_upload_data():
    return patch.object(BaseStorage, 'upload_bucket_data')


@pytest.fixture
def patch_bucket_get_data():
    return patch.object(BaseStorage, 'get_bucket_data')


@pytest.fixture
def score_criteria_factsheet():
    return {
        'name': constants.SCORE_FACTSHEET_CRITERIA,
        'type': constants.RANGE_TYPE,
        'criteria': [
            {
                'name': 'between_1_and_7_attributes',
                'min': 1,
                'max': 7,
                'points': 30
            },
            {
                'name': 'between_8_and_10_attributes',
                'min': 8,
                'max': 10,
                'points': 60
            },
            {
                'name': 'greater_than_10_attributes',
                'min': 10,
                'points': 100
            }
        ]
    }


@pytest.fixture
def score_criteria_title():
    return {
        'name': constants.SCORE_TITLE_CRITERIA,
        'type': constants.RANGE_TYPE,
        'criteria': [
            {
                'name': 'between_1_and_30_characters',
                'min': 1,
                'max': 30,
                'points': 20
            },
            {
                'name': 'between_31_and_60_characters',
                'min': 31,
                'max': 60,
                'points': 30
            },
            {
                'name': 'greater_than_60_characters',
                'min': 60,
                'points': 50
            }
        ]
    }


@pytest.fixture
def score_criteria_description():
    return {
        'name': constants.SCORE_DESCRIPTION_CRITERIA,
        'type': constants.RANGE_TYPE,
        'criteria': [
            {
                'name': 'between_1_and_250_characters',
                'min': 1,
                'max': 250,
                'points': 20
            },
            {
                'name': 'between_251_and_1000_characters',
                'min': 251,
                'max': 1000,
                'points': 20
            },
            {
                'name': 'greater_than_1000_characters',
                'min': 1000,
                'points': 60
            }
        ]
    }


@pytest.fixture
def score_criteria_offer_title():
    return {
        'name': constants.SCORE_OFFER_TITLE_CRITERIA,
        'type': constants.RANGE_TYPE,
        'criteria': [
            {
                'name': 'between_1_and_30_characters',
                'min': 1,
                'max': 30,
                'points': 20
            },
            {
                'name': 'between_31_and_60_characters',
                'min': 31,
                'max': 60,
                'points': 30
            },
            {
                'name': 'greater_than_60_characters',
                'min': 60,
                'points': 50
            }
        ]
    }


@pytest.fixture
def score_criteria_images():
    return {
        'name': constants.SCORE_IMAGES_CRITERIA,
        'type': constants.RANGE_TYPE,
        'criteria': [
            {
                'name': 'equals_1',
                'equals': 1,
                'points': 20
            },
            {
                'name': 'between_2_and_3_images',
                'min': 2,
                'max': 3,
                'points': 30
            },
            {
                'name': 'greater_than_3_images',
                'min': 3,
                'points': 50
            }
        ]
    }


@pytest.fixture
def score_criteria_review_count():
    return {
        'name': constants.SCORE_REVIEW_COUNT_CRITERIA,
        'type': constants.RANGE_TYPE,
        'criteria': [
            {
                'name': 'between_1_and_2_reviews_count',
                'min': 1,
                'max': 2.9,
                'points': 20
            },
            {
                'name': 'between_3_and_6_reviews_count',
                'min': 3,
                'max': 6,
                'points': 30
            },
            {
                'name': 'greater_than_6_reviews_count',
                'min': 6,
                'points': 50
            }
        ]
    }


@pytest.fixture
def score_criteria_review_rating():
    return {
        'name': constants.SCORE_REVIEW_RATING_CRITERIA,
        'type': constants.RANGE_TYPE,
        'criteria': [
            {
                'name': 'between_1_and_2_reviews_rating',
                'min': 1,
                'max': 2.9,
                'points': 20
            },
            {
                'name': 'equals_3_reviews_rating',
                'equals': 3,
                'points': 30
            },
            {
                'name': 'greater_than_4_reviews_rating',
                'min': 3,
                'points': 50
            }
        ]
    }


@pytest.fixture
def save_score_criteria(
    mongo_database,
    score_criteria_title,
    score_criteria_description,
    score_criteria_factsheet,
    score_criteria_offer_title,
    score_criteria_images,
    score_criteria_review_count,
    score_criteria_review_rating
):

    default_v2 = {
        'entity_name': 'default',
        'elements': [
            score_criteria_title,
            score_criteria_description,
            score_criteria_offer_title,
            score_criteria_images,
            score_criteria_review_count,
            score_criteria_review_rating
        ],
        'score_version': '0.2.0'
    }

    murcho_v2 = {
        'entity_name': 'murcho',
        'elements': [
            {
                'name': 'title',
                'type': constants.RANGE_TYPE,
                'criteria': [
                    {
                        'name': 'greater_than_1_characters',
                        'min': 1,
                        'max': 99999,
                        'points': 100
                    }
                ]
            },
            {
                'name': 'description',
                'type': constants.RANGE_TYPE,
                'criteria': [
                    {
                        'name': 'greater_than_1000_characters',
                        'min': 1,
                        'max': 999999999,
                        'points': 100
                    }
                ]
            },
            {
                'name': 'images',
                'type': constants.RANGE_TYPE,
                'criteria': [
                    {
                        'name': 'greater_than_1_image',
                        'min': 1,
                        'max': 99,
                        'points': 100
                    }
                ]
            },
            {
                'name': 'review_count',
                'type': constants.RANGE_TYPE,
                'criteria': [
                    {
                        'name': 'greater_than_1_reviews_count',
                        'min': 1,
                        'max': 99999999999,
                        'points': 100
                    }
                ]
            },
            {
                'name': 'review_rating',
                'type': constants.RANGE_TYPE,
                'criteria': [
                    {
                        'name': 'greater_than_1_reviews_rating',
                        'min': 1,
                        'max': 5,
                        'points': 100
                    }
                ]
            }
        ],
        'score_version': '0.2.0'
    }

    default_v3 = copy.deepcopy(default_v2)
    murcho_v3 = copy.deepcopy(murcho_v2)

    default_v3['elements'].append(score_criteria_factsheet)
    default_v3['score_version'] = '0.3.0'
    murcho_v3['score_version'] = '0.3.0'

    mongo_database.score_criterias.insert_many(
        [default_v2, default_v3, murcho_v2, murcho_v3]
    )


@pytest.fixture
def badge_dict_without_name():
    return {
        'tooltip': 'Black Fraude',
        'text': 'Melhores oferta é na BLACK FRAUDE da Magazine Luiza - Procure este selo e compre tranquilo que garantimos o melhor preço.',  # noqa
        'image_url': 'https://a-static.mlcdn.com.br/{w}x{h}/black_fraude.jpg',  # noqa
        'products': [
            {
                'sku': '123456789',
                'seller_id': 'magazineluiza'
            },
            {
                'sku': 'JDLK765G',
                'seller_id': 'murcho'
            }
        ],
        'position': 'bottom',
        'container': 'information',
        'active': True,
        'priority': 1,
        'start_at': '2017-08-17T06:17:03.503000',
        'end_at': '2018-08-17T06:17:03.503000',
        'slug': 'black-fraude',
    }


@pytest.fixture
def badge_dict():
    return {
        'tooltip': 'Black Fraude',
        'text': 'Melhores oferta é na BLACK FRAUDE da Magazine Luiza - Procure este selo e compre tranquilo que garantimos o melhor preço.',  # noqa
        'image_url': 'https://a-static.mlcdn.com.br/{w}x{h}/black_fraude.jpg',  # noqa
        'products': [
            {
                'sku': '123456789',
                'seller_id': 'magazineluiza'
            },
            {
                'sku': 'JDLK765G',
                'seller_id': 'murcho'
            }
        ],
        'position': 'bottom',
        'container': 'information',
        'name': 'Black Fraude',
        'active': True,
        'priority': 1,
        'start_at': '2017-08-17T06:17:03.503000',
        'end_at': '2018-08-17T06:17:03.503000',
        'slug': 'black-fraude',
    }


@pytest.fixture
def omnilogic_message():
    return {
        'seller_id': 'epocacosmeticos',
        'source': 'omnilogic',
        'sku': '2546',
        'navigation_id': '9452723',
        'category_id': 'CP',
        'product_hash': 'b9efe4e50a2529bbe4176812ac208f8a',
        'metadata': {
            'Produto': 'Perfume',
            'Marca': 'Paco Rabanne',
            'Modelo': '1 Million',
            'concentracao': 'Eau de Toilette',
            'genero': 'Masculino',
            'Ocasião': 'Diurno',
            'Volume': '50ml'
        },
        'product_matching_metadata': ['Produto', 'Marca', 'Modelo'],
        'product_name_metadata': [
            'Produto',
            'Marca',
            'Modelo',
            'concentracao',
            'genero'
        ],
        'sku_metadata': ['Volume'],
        'filters_metadata': [
            'Produto',
            'Marca',
            'Modelo',
            'concentracao',
            'genero',
            'Ocasião',
            'Volume'
        ],
        'timestamp': 1638392769.0682776
    }


@pytest.fixture
def patch_patolino_product_post():
    return patch.object(NotificationSender, '_send_stream')


@pytest.fixture
def patch_notification_sender_send():
    return patch.object(NotificationSender, 'send')


@pytest.fixture
def mock_raw_products_payload():
    return ProductSamples.product_magazineluiza_230382400()


@pytest.fixture
def mock_raw_products_filename(mock_raw_products_payload):
    return '{}/{}.json'.format(
        mock_raw_products_payload['seller_id'],
        mock_raw_products_payload['sku']
    )


@pytest.fixture
def mock_factsheet_filename(
    mock_factsheet_seller_id,
    mock_factsheet_sku
):
    return '{}/factsheet/{}.json'.format(
        mock_factsheet_seller_id,
        mock_factsheet_sku
    )


@pytest.fixture
def mock_factsheet_seller_id():
    return 'epoca'


@pytest.fixture
def mock_factsheet_sku():
    return '123456789'


@pytest.fixture
def mock_factsheet_navigation_id():
    return '123456789'


@pytest.fixture
def patch_factsheet_url():
    return patch.object(FactsheetStorage, 'generate_external_url')


@pytest.fixture
def mock_factsheet_payload_with_empty_dict(mock_factsheet_navigation_id):
    return {
        'seller_id': 'epoca',
        'sku': '123456789',
        'navigation_id': mock_factsheet_navigation_id,
        'items': [
            {
                'slug': 'apresentacao',
                'position': 1,
                'display_name': '<h2>Apresentação</h2>',
                'elements': [
                    {
                        'key_name': 'Apresentação do produto',
                        'position': 2,
                        'value': 'Procurando Nemo está de volta agora'
                    },
                    {
                        'key_name': 'Apresentação do produto',
                        'position': 2,
                        'value': '<h2>Procurando Nemo está de volta</h2>'
                    }
                ]
            },
            {}
        ]
    }


@pytest.fixture
def mock_factsheet_payload(mock_factsheet_navigation_id):
    return {
        'seller_id': 'epoca',
        'sku': '123456789',
        'navigation_id': mock_factsheet_navigation_id,
        'items': [
            {
                'slug': 'apresentacao',
                'position': 1,
                'display_name': '<h2>Apresentação</h2>',
                'elements': [
                    {
                        'key_name': 'Apresentação do produto',
                        'position': 2,
                        'value': 'Procurando Nemo está de volta agora'
                    },
                    {
                        'key_name': 'Apresentação do produto',
                        'position': 2,
                        'value': '<h2>Procurando Nemo está de volta</h2>'
                    }
                ]
            },
            {
                'slug': 'ficha-tecnica',
                'position': 6,
                'display_name': 'Ficha-Técnica',
                'elements': [
                    {
                        'key_name': 'Informações complementares',
                        'slug': 'informacoes-complementares-magazineluiza',
                        'elements': [
                            {
                                'key_name': 'Marca',
                                'position': 10,
                                'value': 'Sunny Brinquedos'
                            },
                            {
                                'key_name': 'Cor',
                                'position': 8,
                                'value': 'Branco'
                            },
                            {
                                'key_name': 'Desenvolvimento',
                                'position': 3,
                                'elements': [
                                    {
                                        'key_name': 'Desenvolvimento',
                                        'value': 'Capacidade visual',
                                        'position': 4,
                                    },
                                    {
                                        'key_name': 'Desenvolvimento',
                                        'value': 'Percepção cromática',
                                        'position': 1,
                                    },
                                    {
                                        'key_name': 'Desenvolvimento',
                                        'value': '<h2>Diversão</h2><p>criança</p>',  # noqa
                                        'position': 8,
                                        'is_html': True
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }


@pytest.fixture
def mock_factsheet_forbidden_terms(mock_factsheet_navigation_id):
    return {
        'seller_id': 'epoca',
        'sku': '123456789',
        'navigation_id': mock_factsheet_navigation_id,
        'items': [
            {
                'slug': 'apresentacao',
                'position': 1,
                'display_name': '<h2>Apresentação</h2>',
                'elements': [
                    {
                        'key_name': 'Apresentação do produto',
                        'position': 2,
                        'value': 'Jaqueta de couro ecológico com Velcro. Com couro original e velcro top, você não se arrependerá de comprar essa linda jaqueta de couro com velcro' # noqa
                    },
                    {
                        'key_name': 'Descrição',
                        'position': 2,
                        'value': '<h2>Jaqueta de couro ecológico com Velcro. Com couro original e velcro top, você não se arrependerá de comprar essa linda jaqueta de couro com velcro</h2>'  # noqa
                    }
                ]
            },
            {
                'slug': 'ficha-tecnica',
                'position': 6,
                'display_name': 'Ficha-Técnica',
                'elements': [
                    {
                        'key_name': 'Informações complementares',
                        'slug': 'informacoes-complementares-magazineluiza',
                        'elements': [
                            {
                                'key_name': 'Marca',
                                'position': 10,
                                'value': 'North Face'
                            },
                            {
                                'key_name': 'Couro (sintético)',
                                'position': 8,
                                'value': 'Legítimo'
                            },
                            {
                                'key_name': 'Desenvolvimento VelCRONNN',
                                'position': 3,
                                'elements': [
                                    {
                                        'key_name': 'Material',
                                        'value': 'Couro ecológico',
                                        'position': 4,
                                    },
                                    {
                                        'key_name': 'Fechamento',
                                        'value': 'Velcro',
                                        'position': 1,
                                    },
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }


@pytest.fixture
def patch_datetime():
    return patch.object(
        datetime, 'datetime', Mock(wraps=datetime.datetime)
    )


@pytest.fixture
def patch_time():
    return patch.object(
        time, 'time', Mock(wraps=time.time, return_value=1502734827.997473)
    )


@pytest.fixture
def mock_product_images(mongo_database):
    medias = {
        'sku': '011704400',
        'seller_id': 'magazineluiza',
        'images': [
            'd4a9dda16aebf1d8fe2bb115669c4155.jpg',
            'd4a9dda16aebf1d8fe2bb115669c4155.jpg',
            'c2d88c66d6d53a082e52787df7790c01.jpg',
            '4ba8da09a782be6a190a79419f4d51a9.jpg'
        ],
        'videos': [],
        'podcasts': [],
        'audios': []
    }

    mongo_database.medias.insert_one(medias)


@pytest.fixture
def mock_product_videos_message_data():
    return ['https://www.youtube.com/v/L76al18mF3Y?hl=pt&']


@pytest.fixture
def mock_product_images_message_data():
    return [
        {
            'url': 'https://img.magazineluiza.com.br/1500x1500/x-213445900.jpg',  # noqa
            'hash': '52de9b80208f08270e62616e42fac68a'
        },
        {
            'url': 'https://img.magazineluiza.com.br/1500x1500/x-088064100.jpg',  # noqa
            'hash': 'bc92c770ad72fc410374a470612b9747'
        }
    ]


@pytest.fixture
def mock_product_medias_message_data(
    mock_product_images_message_data
):
    return {
        'sku': '011704400',
        'seller_id': 'magazineluiza',
        'images': mock_product_images_message_data,
        'videos': [],
        'audios': [],
        'podcasts': []
    }


@pytest.fixture
def mock_product_images_with_details(mock_product_images_message_data):

    return {
        'sku': '011704400',
        'seller_id': 'magazineluiza',
        'image_details': [
            {
                'dimensions': {
                    'width': 1500,
                    'height': 1125
                },
                'hash': '52de9b80208f08270e62616e42fac68a.jpg'
            },
            {
                'dimensions': {
                    'width': 865,
                    'height': 648
                },
                'hash': 'bc92c770ad72fc410374a470612b9747.jpg'
            }
        ],
        'images': [
            '52de9b80208f08270e62616e42fac68a.jpg',
            'bc92c770ad72fc410374a470612b9747.jpg'
        ],
        'original': {
            'images': mock_product_images_message_data
        },
        'original_images': [
            image['url'] for image in mock_product_images_message_data
        ],
        'videos': [],
        'audios': [],
        'podcasts': []
    }


@pytest.fixture
def factsheet_product_227747300():
    return {
        "items": [
            {
                'display_name': 'Apresentação',
                'elements': [
                    {
                        'key_name': 'Sinopse',
                        'position': 2,
                        'elements': [
                            {
                                'value': 'O maior sucesso da Citadel Editora',
                                'is_html': False
                            }
                        ],
                        'slug': 'sinopse'
                    }
                ],
                'slug': 'apresentacao',
                'position': 1
            },
            {
                'display_name': 'Ficha-Técnica',
                'elements': [
                    {
                        'key_name': 'Informações técnicas',
                        'position': 7,
                        'elements': [
                            {
                                'slug': 'editora',
                                'is_html': False,
                                'key_name': 'Editora',
                                'position': 8,
                                'value': 'Citadel'
                            },
                            {
                                'slug': 'titulo',
                                'is_html': False,
                                'key_name': 'Título',
                                'position': 10,
                                'value': 'Mais esperto que o Diabo'
                            },
                            {
                                'slug': 'subtitulo',
                                'is_html': False,
                                'key_name': 'Subtítulo',
                                'position': 10,
                                'value': 'O mistério revelado'
                            }
                        ],
                        'slug': 'informacoes-tecnicas'
                    },
                    {
                        'key_name': 'Autor',
                        'position': 14,
                        'elements': [
                            {
                                'value': 'Hill, Napoleon, Conte Júnior',
                                'is_html': False
                            }
                        ],
                        'slug': 'autor'
                    },
                    {
                        'key_name': 'Ficha técnica',
                        'position': 18,
                        'elements': [
                            {
                                'slug': 'numero-de-paginas',
                                'is_html': False,
                                'key_name': 'Número de páginas',
                                'position': 21,
                                'value': '144'
                            },
                            {
                                "slug": 'edicao',
                                'is_html': False,
                                'key_name': 'Edição',
                                'position': 23,
                                'value': '1'
                            },
                            {
                                'slug': 'data-de-publicacao',
                                'is_html': False,
                                'key_name': 'Data de publicação',
                                'position': 24,
                                'value': '22.07.2019'
                            },
                            {
                                'slug': 'idioma',
                                'is_html': False,
                                'key_name': 'Idioma',
                                'position': 25,
                                'value': 'Português'
                            }
                        ],
                        'slug': 'ficha-tecnica'
                    },
                    {
                        'key_name': 'Código do produto',
                        'position': 32,
                        'elements': [
                            {
                                'value': 'ISBN-10 - 8568014933\nGTIN-13',
                                'is_html': False
                            }
                        ],
                        'slug': 'codigo-do-produto'
                    },
                    {
                        'key_name': 'Peso aproximado',
                        'position': 36,
                        'elements': [
                            {
                                'slug': 'peso-do-produto',
                                'is_html': False,
                                'key_name': 'Peso do produto',
                                'position': 37,
                                'value': '81.0 gramas.'
                            }
                        ],
                        'slug': 'peso-aproximado'
                    },
                    {
                        'key_name': 'Dimensões do produto',
                        'position': 39,
                        'elements': [
                            {
                                'slug': 'produto',
                                'is_html': False,
                                'key_name': 'Produto',
                                'position': 40,
                                'value': '(L x A x P): 10.0 x 14.0 x 10.0 cm.'
                            }
                        ],
                        'slug': 'dimensoes-do-produto'
                    }
                ],
                'slug': 'ficha-tecnica',
                'position': 6
            }
        ],
        'navigation_id': '227747300'
    }


@pytest.fixture
def factsheet_product_227718300():
    return {
        'items': [
            {
                'display_name': 'Apresentação',
                'slug': 'apresentacao',
                'elements': [
                    {
                        'key_name': 'Apresentação do produto',
                        'slug': 'apresentacao-do-produto',
                        'elements': [
                            {
                                'value': 'Com o Limpa Piso Cafuné Flores',
                                'is_html': False
                            }
                        ]
                    }
                ]
            },
            {
                'display_name': 'Ficha-Técnica',
                'slug': 'ficha-tecnica',
                'elements': [
                    {
                        'key_name': 'Marca',
                        'slug': 'marca',
                        'elements': [
                            {
                                'value': 'Cafuné',
                                'is_html': False
                            }
                        ]
                    },
                    {
                        'slug': 'informacoes-complementares-magazineluiza',
                        'position': 1,
                        'key_name': 'Informações complementares',
                        'elements': [
                            {
                                'key_name': 'Capacidade Líquida Total',
                                'slug': 'capacidade-liquida-total',
                                'position': 1,
                                'value': '240 L',
                                'is_html': False
                            }
                        ]
                    },
                    {
                        'key_name': 'Informações técnicas - Referência',
                        'slug': 'informacoes-tecnicas-referencia',
                        'elements': [
                            {
                                'value': '68410113\n',
                                'is_html': False
                            }
                        ]
                    },
                    {
                        'slug': 'informacoes-complementares',
                        'position': 1,
                        'key_name': 'Informações complementares',
                        'elements': [
                            {
                                'key_name': 'Capacidade Líquida Total',
                                'slug': 'capacidade-liquida-total',
                                'position': 1,
                                'value': '240 L',
                                'is_html': False
                            }
                        ]
                    },
                    {
                        'key_name': 'Informações técnicas - Modelo',
                        'elements': [
                            {
                                'value': 'Flores Brancas',
                                'is_html': False
                            }
                        ]
                    },
                    {
                        'key_name': 'Indicado para',
                        'elements': [
                            {
                                'value': 'Limpeza de pisos e superfícies',
                                'is_html': False
                            }
                        ]
                    },
                    {
                        'key_name': 'Características',
                        'slug': 'caracteristicas',
                        'elements': [
                            {
                                'value': '- Concentrado\n- Com tecnologia',
                                'is_html': False
                            }
                        ]
                    },
                    {
                        'key_name': 'Fragrância',
                        'slug': 'fragrancia',
                        'elements': [
                            {
                                'value': 'Flores Brancas\n',
                                'is_html': False
                            }
                        ]
                    },
                    {
                        'key_name': 'Volume',
                        'slug': 'volume',
                        'elements': [
                            {
                                'value': '900ml',
                                'is_html': False
                            }
                        ]
                    },
                    {
                        'key_name': 'Quantidade',
                        'slug': 'quantidade',
                        'elements': [
                            {
                                'value': '1',
                                'is_html': False
                            }
                        ]
                    },
                    {
                        'key_name': 'Rendimento',
                        'slug': 'rendimento',
                        'elements': [
                            {
                                'value': 'Rende até 30L de solução de limpeza',
                                'is_html': False
                            }
                        ]
                    },
                    {
                        'key_name': 'Recomendações de uso',
                        'slug': 'recomendacoes-de-uso',
                        'elements': [
                            {
                                'value': 'Com um alto rendimento, para ',
                                'is_html': False
                            }
                        ]
                    },
                    {
                        'key_name': 'Peso aproximado - Peso do produto ',
                        'slug': 'peso-aproximado-peso-do-produto-com-em',
                        'elements': [
                            {
                                'value': '965g',
                                'is_html': False
                            }
                        ]
                    },
                    {
                        'key_name': 'Dimensões do produto com embalagem',
                        'slug': 'dimensoes-do-produto-com-embalagem',
                        'elements': [
                            {
                                'value': '- Largura: 7,8cm\n- Altura: 27cm\n',
                                'is_html': False
                            }
                        ]
                    },
                    {
                        'key_name': 'Garantia - Prazo de Garantia',
                        'slug': 'garantia-prazo-de-garantia',
                        'elements': [
                            {
                                'value': '30 dias',
                                'is_html': False
                            }
                        ]
                    },
                    {
                        'key_name': 'Conteúdo da embalagem',
                        'slug': 'conteudo-da-embalagem',
                        'elements': [
                            {
                                'value': '- 1 Limpa Piso',
                                'is_html': False
                            }
                        ]
                    }
                ]
            }
        ],
        'navigation_id': '227718300'
    }


@pytest.fixture
def factsheet_product_010015900():
    return {
        'items': [
            {
                'display_name': 'Apresentação',
                'elements': [
                    {
                        'elements': [
                            {
                                'is_html': False,
                                'value': 'Bebidas sempre geladas'
                            }
                        ],
                        'key_name': 'Apresentação do produto',
                        'position': 2,
                        'slug': 'apresentacao-do-produto'
                    }
                ],
                'position': 1,
                'slug': 'apresentacao'
            },
            {
                'display_name': 'Ficha-Técnica',
                'elements': [
                    {
                        'elements': [
                            {
                                'is_html': False,
                                'key_name': 'Marca',
                                'position': 8,
                                'slug': 'marca',
                                'value': 'Metalfrio'
                            },
                            {
                                'is_html': False,
                                'key_name': 'Referência',
                                'position': 9,
                                'slug': 'referencia',
                                'value': 'VB50RB2001 1. '
                            },
                            {
                                'is_html': False,
                                'key_name': 'Cor',
                                'position': 10,
                                'slug': 'cor',
                                'value': 'Branco'
                            },
                            {
                                'is_html': False,
                                'key_name': 'Modelo',
                                'position': 11,
                                'slug': 'modelo',
                                'value': 'VB50RB'
                            },
                            {
                                'is_html': False,
                                'key_name': 'Linha',
                                'position': 12,
                                'slug': 'linha',
                                'value': 'Soft Drinks'
                            }
                        ],
                        'key_name': 'Informações técnicas',
                        'position': 7,
                        'slug': 'informacoes-tecnicas'
                    },
                    {
                        'elements': [
                            {
                                'is_html': False,
                                'value': 'Vertical'
                            }
                        ],
                        'key_name': 'Tipo de expositor',
                        'position': 13,
                        'slug': 'tipo-de-expositor'
                    },
                    {
                        'elements': [
                            {
                                'is_html': False,
                                'value': '1'
                            }
                        ],
                        'key_name': 'Quantidade de portas',
                        'position': 14,
                        'slug': 'quantidade-de-portas'
                    },
                    {
                        'elements': [
                            {
                                'is_html': False,
                                'value': 'sim'
                            }
                        ],
                        'key_name': 'Modelo de embutir',
                        'position': 15,
                        'slug': 'modelo-de-embutir'
                    },
                    {
                        'elements': [
                            {
                                'is_html': False,
                                'value': 'Refrigerador'
                            }
                        ],
                        'key_name': 'Função',
                        'position': 16,
                        'slug': 'funcao'
                    },
                    {
                        'elements': [
                            {
                                'is_html': False,
                                'key_name': 'Bruta',
                                'position': 20,
                                'slug': 'bruta',
                                'value': '572 litros.'
                            },
                            {
                                'is_html': False,
                                'key_name': 'Garrafas',
                                'position': 22,
                                'slug': 'garrafas',
                                'value': '196 garrafas Pet 600ml'
                            },
                            {
                                'is_html': False,
                                'key_name': 'Latas',
                                'position': 23,
                                'slug': 'latas',
                                'value': '576 latas 350ml.'
                            }
                        ],
                        'key_name': 'Capacidade',
                        'position': 18,
                        'slug': 'capacidade'
                    },
                    {
                        'elements': [
                            {
                                'is_html': False,
                                'value': '543W.'
                            }
                        ],
                        'key_name': 'Potência',
                        'position': 24,
                        'slug': 'potencia'
                    },
                    {
                        'elements': [
                            {
                                'is_html': False,
                                'value': 'Frost free'
                            }
                        ],
                        'key_name': 'Tipo de degelo',
                        'position': 25,
                        'slug': 'tipo-de-degelo'
                    },
                    {
                        'elements': [
                            {
                                'is_html': False,
                                'value': 'Aço pré-pintado.'
                            }
                        ],
                        'key_name': 'Material',
                        'position': 27,
                        'slug': 'material'
                    },
                    {
                        'elements': [
                            {
                                'is_html': False,
                                'key_name': 'Quantidade',
                                'position': 30,
                                'slug': 'quantidade',
                                'value': '3.'
                            },
                            {
                                'is_html': False,
                                'key_name': 'Material',
                                'position': 31,
                                'slug': 'material',
                                'value': 'Ferro pré-pintado.'
                            },
                            {
                                'elements': [
                                    {
                                        'is_html': False,
                                        'position': 32,
                                        'slug': 'aramado',
                                        'value': 'Aramado'
                                    },
                                    {
                                        'is_html': False,
                                        'position': 32,
                                        'slug': 'regulaveis',
                                        'value': 'reguláveis'
                                    },
                                    {
                                        'is_html': False,
                                        'position': 32,
                                        'slug': 'suspensas',
                                        'value': 'suspensas'
                                    }
                                ],
                                'key_name': 'Tipo',
                                'position': 32,
                                'slug': 'tipo'
                            }
                        ],
                        'key_name': 'Prateleiras',
                        'position': 29,
                        'slug': 'prateleiras'
                    },
                    {
                        'elements': [
                            {
                                'is_html': False,
                                'key_name': 'Sistema de refrigeração',
                                'position': 45,
                                'slug': 'sistema-de-refrigeracao',
                                'value': 'Evaporador Aletado'
                            },
                            {
                                'is_html': False,
                                'key_name': 'Temperatura',
                                'position': 46,
                                'slug': 'temperatura',
                                'value': '2 a 8°C.'
                            },
                            {
                                'is_html': False,
                                'key_name': 'Iluminação interna',
                                'position': 47,
                                'slug': 'iluminacao-interna',
                                'value': 'sim'
                            },
                            {
                                'is_html': False,
                                'key_name': 'Porta com fechamento automático',
                                'position': 49,
                                'slug': 'porta-com-fechamento-automatico',
                                'value': 'Sim'
                            },
                            {
                                'is_html': False,
                                'key_name': 'Condensador embutido',
                                'position': 51,
                                'slug': 'condensador-embutido',
                                'value': 'sim'
                            },
                            {
                                'is_html': False,
                                'key_name': 'Luz indicadora',
                                'position': 53,
                                'slug': 'luz-indicadora',
                                'value': 'sim'
                            },
                            {
                                'is_html': False,
                                'key_name': 'Dreno de gelo',
                                'position': 55,
                                'slug': 'dreno-de-gelo',
                                'value': 'sim'
                            }
                        ],
                        'key_name': 'Recursos Extras',
                        'position': 37,
                        'slug': 'recursos-extras'
                    },
                    {
                        'elements': [
                            {
                                'is_html': False,
                                'value': 'sim'
                            }
                        ],
                        'key_name': 'Não contém CFC',
                        'position': 58,
                        'slug': 'nao-contem-cfc'
                    },
                    {
                        'elements': [
                            {
                                'is_html': False,
                                'key_name': 'Eficiência energética',
                                'position': 60,
                                'slug': 'eficiencia-energetica',
                                'value': 'não classificada'
                            },
                            {
                                'is_html': False,
                                'key_name': 'Voltagem',
                                'position': 62,
                                'slug': 'voltagem',
                                'value': '110 Volts'
                            }
                        ],
                        'key_name': 'Alimentação',
                        'position': 59,
                        'slug': 'alimentacao'
                    },
                    {
                        'elements': [
                            {
                                'is_html': False,
                                'key_name': 'Peso do produto',
                                'position': 64,
                                'slug': 'peso-do-produto',
                                'value': '132 kg.'
                            },
                            {
                                'is_html': False,
                                'key_name': 'Peso do produto com embalagem',
                                'position': 65,
                                'slug': 'peso-do-produto-com-embalagem',
                                'value': '140 kg.'
                            }
                        ],
                        'key_name': 'Peso aproximado',
                        'position': 63,
                        'slug': 'peso-aproximado'
                    },
                    {
                        'elements': [
                            {
                                'is_html': False,
                                'key_name': 'Largura',
                                'position': 71,
                                'slug': 'largura',
                                'value': '67,5 cm.'
                            },
                            {
                                'is_html': False,
                                'key_name': 'Altura',
                                'position': 72,
                                'slug': 'altura',
                                'value': '202,1 cm.'
                            },
                            {
                                'is_html': False,
                                'key_name': 'Profundidade',
                                'position': 73,
                                'slug': 'profundidade',
                                'value': '85 cm.'
                            }
                        ],
                        'key_name': 'Dimensões do produto',
                        'position': 70,
                        'slug': 'dimensoes-do-produto'
                    },
                    {
                        'elements': [
                            {
                                'is_html': False,
                                'key_name': 'Largura',
                                'position': 75,
                                'slug': 'largura',
                                'value': '71,2 cm.'
                            },
                            {
                                'is_html': False,
                                'key_name': 'Altura',
                                'position': 76,
                                'slug': 'altura',
                                'value': '210 cm.'
                            },
                            {
                                'is_html': False,
                                'key_name': 'Profundidade',
                                'position': 77,
                                'slug': 'profundidade',
                                'value': '89,3 cm.'
                            }
                        ],
                        'key_name': 'Dimensões da embalagem',
                        'position': 74,
                        'slug': 'dimensoes-da-embalagem'
                    },
                    {
                        'elements': [
                            {
                                'is_html': False,
                                'value': '01 ano'
                            }
                        ],
                        'key_name': 'Prazo de garantia',
                        'position': 78,
                        'slug': 'prazo-de-garantia'
                    },
                    {
                        'elements': [
                            {
                                'is_html': False,
                                'value': '0800-702-0052'
                            }
                        ],
                        'key_name': 'SAC do fornecedor (E-mail)',
                        'position': 79,
                        'slug': 'sac-do-fornecedor-e-mail'
                    }
                ],
                'position': 6,
                'slug': 'ficha-tecnica'
            },
            {
                'display_name': 'Itens Inclusos',
                'elements': [
                    {
                        'elements': [
                            {
                                'is_html': False,
                                'value': '- 01 Expositor.'
                            }
                        ],
                        'key_name': 'Itens inclusos',
                        'position': 91,
                        'slug': 'itens-inclusos'
                    }
                ],
                'position': 90,
                'slug': 'itens-inclusos'
            }
        ],
        'navigation_id': '010015900'
    }


@pytest.fixture
def patch_notification_put():
    return patch.object(Notification, 'put')


@pytest.fixture
def patch_notification_raw_products():
    return patch.object(Notification, 'raw_products')


@pytest.fixture
def mock_category_rc_payload():
    return {
        'categories': [
            {
                'id': 'RC',
                'description': 'Recém chegados',
                'subcategories': [
                    {
                        'id': 'RCNM',
                        'description': 'No Magalu'
                    }
                ]
            }
        ],
        'main_category': {'id': 'RC', 'subcategory': {'id': 'RCNM'}}
    }


@pytest.fixture
def mock_de_para_forbidden_terms():
    return {
        'v.e.l.c.r.o': 'Tiras Autocolantes',
        'couro (sintetico)': 'Material Sintético',
        'criado - mudos': 'Mesa de Cabeceira'
    }


@pytest.fixture
def patch_raw_products_storage_get_bucket_data():
    return patch.object(RawProductsStorage, 'get_bucket_data')


@pytest.fixture
def mock_extra_data():
    return {
        'seller_id': 'luizalabs',
        'sku': '123456789',
        'extra_data': [
            {
                'name': 'fulfillment',
                'value': 'true'
            },
            {
                'name': 'is_magalu_indica',
                'value': 'true'
            }
        ]
    }


@pytest.fixture
def patch_factsheet_merge():
    return patch.object(FactsheetMerger, 'merge')


@pytest.fixture
def mock_maas_product_reprocess_payload():
    return {
        'seller_id': 'fake',
        'sku': 'fake',
        'source': 'datasheet'
    }


@pytest.fixture
def patch_notification_enrichment_notify():
    return patch.object(NotificationEnrichment, 'notify')


@pytest.fixture
def mock_input_label_payload(
    mock_raw_products_payload: dict
) -> dict:
    return {
        'navigation_id': mock_raw_products_payload['navigation_id'],
        'seller_id': mock_raw_products_payload['seller_id'],
        'sku': mock_raw_products_payload['sku'],
        'in_out': 'in',
        'rules_version': 'v0',
        'label': 'is_magalu_indica'
    }


@pytest.fixture
def mock_matching_uuid():
    return 'b09db6bca2c34fa6acad6c54647bad98'


@pytest.fixture
def mock_classification_rule_refrigerador_menor_400():
    return {
        '_id': '271b9dea-394b-48ed-a24b-853a7200227b',
        'product_type': 'Refrigerador',
        'operation': 'MENOR_IGUAL',
        'active': True,
        'price': 400.00,
        'to': {
            'product_type': 'Peças para Refrigerador',
            'category_id': 'ED',
            'subcategory_ids': ['FAPG', 'REFR', 'ACRF']
        },
        'user': 'catalogo@luizalabs.com',
        'status': 'applied',
        'created_at': datetime.datetime(2024, 3, 15, 0, 0, 0),
        'updated_at': datetime.datetime(2024, 3, 15, 0, 0, 0)
    }


@pytest.fixture
def patch_paginate_keyset():
    return patch.object(Pagination, '_paginate_keyset')


@pytest.fixture
def mock_uuid():
    return UUID('c77286a0-1a97-4580-a375-5069f5af6431')


@pytest.fixture
def mock_tracking_id(mock_uuid):
    return str(mock_uuid)


@pytest.fixture
def patch_generate_uuid(mock_uuid):
    return patch(
        'taz.utils.uuid4',
        return_value=mock_uuid
    )
