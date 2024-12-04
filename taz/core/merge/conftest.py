import pytest
from simple_settings import settings

from taz.constants import SINGLE_SELLER_STRATEGY


@pytest.fixture
def raw_product():
    return {
        'main_variation': False,
        'title': 'Smartphone Samsung Galaxy S7 32GB Preto 4G',
        'main_category': {
            'subcategory': {
                'id': 'GAS7'
            },
            'id': 'TE'
        },
        'dimensions': {
            'depth': 0.15,
            'width': 0.08,
            'height': 0.05,
            'weight': 0.345
        },
        'description': 'O Samsung Galaxy S7 chegou para deixar uma das famílias de celulares mais famosas do mundo ainda mais completa e elegante! Com design sem igual, ele é uma verdadeira inovação feita em metal e vidro. A beleza deste modelo está na combinação sofisticada entre visual e usabilidade. Tudo elegantemente integrado para você ter em suas mãos as mais avançadas funcionalidades com um design inigualável.\n\nSeu processador Octa-Core oferece desempenho superior para que você gerencie fotos, vídeos, jogos e aplicativos sem se preocupar com a velocidade. \n\nQuando o assunto é imagem, o S7 apresenta uma câmera traseira de 12 Megapixels de resolução para você registrar seus momentos de forma perfeita! Já a câmera frontal também não deixa os fãs de selfies na mão com sua resolução de 5 Megapixels, além de ter suporte para expansão da memória com cartão Micro SD de até 200GB.\n\nSuper moderno, o S7 tem bateria maior que dura muito mais e carrega em menos tempo. E até onde um smartphone pode ir? Em qualquer lugar que você for. Utilizando materiais de alto desempenho, conseguimos selar completamente os componentes internos e manter as portas de USB e conectores auriculares abertos. Assim não é preciso proteção extra contra chuva, piscina ou poeiras.\n\nÉ muita modernidade, não é mesmo? Então não perca mais tempo, confira essas e todas as outras vantagens deste smartphone e descubra porque a linha Galaxy vem se tornando cada vez mais completa!',  # noqa
        'parent_sku': '2159153',
        'sku': '215915300',
        'reference': 'Câm 12MP + Selfie 5MP Tela 5.1” Quad HD Octa Core',
        'disable_on_matching': False,
        'ean': '7892509086998',
        'sells_to_company': True,
        'matching_strategy': SINGLE_SELLER_STRATEGY,
        'categories': [
            {
                'subcategories': [
                    {
                        'id': 'GAS7'
                    },
                ],
                'id': 'TE'
            }
        ],
        'seller_description': 'Magazine Luiza',
        'navigation_id': '215915300',
        'seller_id': 'magazineluiza',
        'brand': 'samsung',
    }


@pytest.fixture
def save_raw_product(mongo_database, raw_product):
    mongo_database.raw_products.insert_one(raw_product)


@pytest.fixture
def config_settings():
    settings.USE_MERGE = True
    return settings
