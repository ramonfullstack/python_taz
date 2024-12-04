import pytest

from taz.consumers.product_exporter.helpers import (
    _create_enriched_payload,
    _generate_factsheet_url,
    _get_product_url,
    build_images,
    contains_fulfillment
)
from taz.core.matching.common.enriched_products import EnrichedProductSamples


class TestGetProductUrlHelpers:

    @pytest.fixture
    def product(self):
        return {
            'title': 'Lavadora de Roupas Electrolux Addmix',
            'reference': '13kg',
            'navigation_id': '213445900',
            'seller_id': 'magazineluiza',
            'categories': [{
                'subcategories': [{'id': 'LAVA'}],
                'id': 'ED'
            }]
        }

    @pytest.fixture
    def expected_url(self):
        return 'lavadora-de-roupas-electrolux-addmix-13kg/p/213445900/ed/lava/'  # noqa

    def test_should_success_for_get_url(self, product, expected_url):
        url = _get_product_url(product)
        assert url == expected_url

    def test_when_product_without_category_then_error_for_get_url(
        self,
        product
    ):
        del product['categories']
        assert _get_product_url(product) is None

    @pytest.mark.parametrize('seller_id', [('magazineluiza', 'netshoes')])
    def test_when_product_with_navigation_7_digits_then_return_url_with_9_digits(  # noqa
        self,
        product,
        seller_id,
        expected_url
    ):
        product.update({'seller_id': seller_id, 'navigation_id': '2134459'})
        assert _get_product_url(product) == expected_url


class TestGenerateFactsheetUrlHelpers:

    def test_should_success_to_generate_factsheet_url(self):
        url = _generate_factsheet_url('123456789', 'murcho')
        assert url == 'http://pis.static-tst.magazineluiza.com.br/murcho/factsheet/123456789.json'  # noqa


class TestBuildImages:

    def test_build_images_returns_images(
        self,
        mock_product_videos_message_data
    ):
        media = {
            'images': [{
                'url': 'http://img.magazineluiza.com.br/1500x1500/x-ABD412345CF.jpg',  # noqa
                'hash': 'd4b4755b9ee658406f6e40f1d6e6129c'
            }, {
                'url': 'http://img.magazineluiza.com.br/1500x1500/x-ABD412345CF.jpg',  # noqa
                'hash': 'ce86964b8543828d1433cb1e029770e5'
            }],
            'videos': mock_product_videos_message_data
        }

        payload = build_images(
            sku='123456 ABC',
            seller_id='murcho',
            title='Tv Murhcão',
            reference='Smart Tv Fulano',
            media=media['images']
        )

        assert payload == [
            'https://x.xx.xxx/{w}x{h}/tv-murhcao-smart-tv-fulano/murcho/123456-abc/d4b4755b9ee658406f6e40f1d6e6129c.jpg',  # noqa
            'https://x.xx.xxx/{w}x{h}/tv-murhcao-smart-tv-fulano/murcho/123456-abc/ce86964b8543828d1433cb1e029770e5.jpg'  # noqa
        ]

    def test_build_images_returns_unavailable_image(self):
        payload = build_images(
            sku='123456',
            seller_id='murcho',
            title='murchão',
            reference='fulano',
            media=None
        )

        assert payload == [
            'https://x.xx.xxx/{w}x{h}/imagem-indisponivel/appmockups/000000000/1bd79dc863d30982501d43e14bccc8f0.jpg'  # noqa
        ]


class TestCreateEnrichedProducts:

    @pytest.fixture
    def omnilogic_enriched(self):
        metadata = {
            'ISBN-13': '9788551002490',
            'ISBN-10': '855100249X',
            'Autor': 'Manson, Mark, Faro, Joana',
            'Gênero': 'Saúde e Família,Transformação Pessoal,Autoajuda,Administração,Negócios e Economia'  # noqa
        }
        return {
            'sku': '222764000',
            'entity': 'Livro',
            'metadata': metadata,
            'seller_id': 'magazineluiza',
            'navigation_id': '222764000',
            'category_id': 'LI',
            'subcategory_ids': ['ADML'],
            'product_hash': '4a5eab178ba030c793e99f73b0386729',
            'product_name': 'Livro - A sutil arte de ligar o f*da-se',
            'product_matching_metadata': ['ISBN-10', 'ISBN-13'],
            'product_name_metadata': [x for x in metadata],
            'sku_metadata': [],
            'filters_metadata': ['ISBN-10', 'ISBN-13', 'Gênero', 'Autor', 'Tipo de Edição', 'Volume', 'Editora', 'Edição'],  # noqa
            'source': 'magalu',
            'timestamp': 1584614485.1888497,
        }

    @pytest.fixture
    def wakko_enriched(self):
        return {
            'sku': '222764000',
            'metadata': {
                'normalized': {
                    'Volume': ['90g']
                },
                'descriptive': {
                    'Volume': ['90 g']
                },
                'normalized_filters': {
                    'Volume': ['90g'],
                    'Quantidade': ['01 unidades']
                }
            },
            'seller_id': 'magazineluiza',
            'navigation_id': '222764000',
            'source': 'wakko',
            'timestamp': 1584614485.1888497
        }

    @pytest.fixture
    def wakko_enriched_classification_not_normalized(self):
        return {
            'sku': '222764000',
            'metadata': {
                'normalized': {
                    'Volume': ['90g'],
                    'Classificação': ['murcho']
                },
                'descriptive': {
                    'Volume': ['90 g'],
                    'Classificação': ['murcho']
                },
            },
            'seller_id': 'magazineluiza',
            'navigation_id': '222764000',
            'source': 'wakko',
            'timestamp': 1584614485.1888497,
        }

    @pytest.fixture
    def wakko_enriched_classification_with_extracted_key(self):
        return {
            'sku': '222764000',
            'metadata': {
                'normalized': {
                    'Volume': ['90g'],
                    'Classificação': ['murcho']
                },
                'descriptive': {
                    'Volume': ['90 g'],
                    'Classificação': ['murcho']
                },
                'extracted': {
                    'Cor': ['Azul']
                }
            },
            'seller_id': 'magazineluiza',
            'navigation_id': '222764000',
            'source': 'wakko',
            'timestamp': 1584614485.1888497,
        }

    @pytest.fixture
    def wakko_enriched_with_nsfw_classification(self):
        return {
            'sku': '222764000',
            'metadata': {
                'normalized': {
                    'Volume': ['90g']
                },
                'descriptive': {
                    'Volume': ['90 g']
                },
                'classified': {
                    'nsfw': {
                        'safe': 0.5,
                        'illustration': 0.35,
                        'hentai': 0.80,
                        'sensual': 0.82,
                        'porn': 0.85
                    },
                    'category_id': 'IN'
                }
            },
            'seller_id': 'magazineluiza',
            'navigation_id': '222764000',
            'source': 'wakko',
            'timestamp': 1584614485.1888497
        }

    @pytest.fixture
    def reclassification_price_rule_enriched(self):
        enriched_product = EnrichedProductSamples.magazineluiza_sku_213445900_reclassification_price_rule()  # noqa
        enriched_product.update({
            'seller_id': 'magazineluiza',
            'sku': '222764000',
            'navigation_id': '222764000',
        })
        return enriched_product

    @pytest.fixture
    def metabooks_enriched(self):
        return {
            'sku': '222764000',
            'seller_id': 'magazineluiza',
            'navigation_id': '222764000',
            'metadata': {
                'Editora': 'Intrínseca',
                'Edição': '1ª edição',
                'Autor': 'Zacker, Craig, Michel, Luciana Monteiro, Silva, Aldir José Coelho Corrêa da',  # noqa
                'Data de publicação': '06.11.2017',
                'Tipo de produto': 'pbook',
                'Número de páginas': '224',
                'Idiomas do produto': 'Português'
            },
            'title': 'A sutil arte de ligar o f*da-se',
            'subtitle': 'Uma estratégia inusitada para uma vida melhor',
            'description': '<p>Chega de tentar buscar um sucesso que só existe na sua cabeça. Chega de se torturar para pensar positivo enquanto sua vida vai ladeira abaixo. Chega de se sentir inferior por não ver o lado bom de estar no fundo do poço.</p>\n\n<p>Coaching, autoajuda, desenvolvimento pessoal, mentalização positiva - sem querer desprezar o valor de nada disso, a grande verdade é que às vezes nos sentimos quase sufocados diante da pressão infinita por parecermos otimistas o tempo todo. É um pecado social se deixar abater quando as coisas não vão bem. Ninguém pode fracassar simplesmente, sem aprender nada com isso. Não dá mais. É insuportável. E é aí que entra a revolucionária e sutil arte de ligar o foda-se.</p>\n\n<p>Mark Manson usa toda a sua sagacidade de escritor e seu olhar crítico para propor um novo caminho rumo a uma vida melhor, mais coerente com a realidade e consciente dos nossos limites. E ele faz isso da melhor maneira. Como um verdadeiro amigo, Mark se senta ao seu lado e diz, olhando nos seus olhos: você não é tão especial. Ele conta umas piadas aqui, dá uns exemplos inusitados ali, joga umas verdades na sua cara e pronto, você já se sente muito mais alerta e capaz de enfrentar esse mundo cão.</p>\n\n<p>Para os céticos e os descrentes, mas também para os amantes do gênero, enfim uma abordagem franca e inteligente que vai ajudar você a descobrir o que é realmente importante na sua vida, e f*da-se o resto. Livre-se agora da felicidade maquiada e superficial e abrace esta arte verdadeiramente transformadora.</p>',  # noqa
            'source': 'metabooks',
            'entity': 'Livro',
            'category_id': 'LI',
            'subcategory_ids': ['LIAJ']
        }

    @pytest.fixture
    def smartcontent_enriched(self):
        return {
            'seller_id': 'magazineluiza',
            'sku': '222764000',
            'navigation_id': '222764000',
            'metadata': {
                'Voltagem': '110 volts'
            },
            'title': 'A sutil arte de ligar o f*da-se',
            'description': '<p>Chega de tentar buscar um sucesso que só existe na sua cabeça. Chega de se torturar para pensar positivo enquanto sua vida vai ladeira abaixo. Chega de se sentir inferior por não ver o lado bom de estar no fundo do poço.</p>\n\n<p>Coaching, autoajuda, desenvolvimento pessoal, mentalização positiva - sem querer desprezar o valor de nada disso, a grande verdade é que às vezes nos sentimos quase sufocados diante da pressão infinita por parecermos otimistas o tempo todo. É um pecado social se deixar abater quando as coisas não vão bem. Ninguém pode fracassar simplesmente, sem aprender nada com isso. Não dá mais. É insuportável. E é aí que entra a revolucionária e sutil arte de ligar o foda-se.</p>\n\n<p>Mark Manson usa toda a sua sagacidade de escritor e seu olhar crítico para propor um novo caminho rumo a uma vida melhor, mais coerente com a realidade e consciente dos nossos limites. E ele faz isso da melhor maneira. Como um verdadeiro amigo, Mark se senta ao seu lado e diz, olhando nos seus olhos: você não é tão especial. Ele conta umas piadas aqui, dá uns exemplos inusitados ali, joga umas verdades na sua cara e pronto, você já se sente muito mais alerta e capaz de enfrentar esse mundo cão.</p>\n\n<p>Para os céticos e os descrentes, mas também para os amantes do gênero, enfim uma abordagem franca e inteligente que vai ajudar você a descobrir o que é realmente importante na sua vida, e f*da-se o resto. Livre-se agora da felicidade maquiada e superficial e abrace esta arte verdadeiramente transformadora.</p>',  # noqa
            'source': 'smartcontent',
            'entity': 'Livro',
            'brand': 'Sextante'
        }

    @pytest.fixture
    def express_delivery_enriched(self):
        return {
            'sku': '222764000',
            'seller_id': 'magazineluiza',
            'source': 'api_luiza_express_delivery',
            'delivery_days': 2
        }

    @pytest.fixture
    def pickupstore_enriched(self):
        return {
            'seller_id': 'magazineluiza',
            'sku': '222764000',
            'source': 'api_luiza_pickupstore',
            'stores': [
                {
                    'trading_id': 511,
                    'trading_name': 'BR511',
                    'zipcode': '06440180',
                    'type': 'Convencional',
                    'location': {
                        'latitude': -23.5162335,
                        'longitude': -46.855463
                    }
                },
                {
                    'trading_id': 556,
                    'trading_name': 'CA556',
                    'zipcode': '07700170',
                    'type': 'Convencional',
                    'location': {
                        'latitude': -23.361463,
                        'longitude': -46.746177
                    }
                }
            ]
        }

    @pytest.fixture
    def expected_payload_enriched(
        self,
        metabooks_enriched,
        omnilogic_enriched,
        smartcontent_enriched
    ):
        metadata_metabooks = metabooks_enriched['metadata']
        metadata_omnilogic = omnilogic_enriched['metadata']
        metadata_smartcontent = smartcontent_enriched['metadata']
        metadata = {**metadata_omnilogic,
                    **metadata_metabooks,
                    **metadata_smartcontent}
        descriptive = {x: [metadata[x]] for x in metadata}
        filters_metadata = omnilogic_enriched['filters_metadata']

        return {
            'metadata': {
                'descriptive': descriptive,
                'delivery': {
                    'Entrega rápida': [2],
                    'Retira loja': ['true']
                },
                'classified': {},
                'normalized_filters': {}
            },
            'filters_metadata': filters_metadata,
            'entity': 'Livro'
        }

    @pytest.fixture
    def mock_hector_enriched(self):
        hector = EnrichedProductSamples.magazineluiza_hector_230382400()
        hector['classifications'][0]['product_type'] = 'hector'
        return hector

    def test_create_enriched_complete_payload(
        self,
        omnilogic_enriched,
        metabooks_enriched,
        smartcontent_enriched,
        express_delivery_enriched,
        pickupstore_enriched,
        expected_payload_enriched
    ):
        enriched_products = [
            omnilogic_enriched,
            metabooks_enriched,
            smartcontent_enriched,
            express_delivery_enriched,
            pickupstore_enriched
        ]
        enriched_products.sort(key=lambda x: x['source'])

        payload = _create_enriched_payload(enriched_products)

        assert payload == expected_payload_enriched

    def test_create_enriched_partial_payload(
        self,
        metabooks_enriched,
        pickupstore_enriched
    ):
        enriched_products = [metabooks_enriched, pickupstore_enriched]

        enriched_products.sort(key=lambda x: x['source'])

        payload = _create_enriched_payload(enriched_products)

        assert payload == {
            'filters_metadata': [],
            'metadata': {
                'delivery': {
                    'Retira loja': ['true']
                },
                'descriptive': {
                    'Autor': [
                        'Zacker, Craig, Michel, Luciana '
                        'Monteiro, Silva, Aldir José Coelho '
                        'Corrêa da'
                    ],
                    'Data de publicação': ['06.11.2017'],
                    'Editora': ['Intrínseca'],
                    'Edição': ['1ª edição'],
                    'Idiomas do produto': ['Português'],
                    'Número de páginas': ['224'],
                    'Tipo de produto': ['pbook']
                },
                'classified': {},
                'normalized_filters': {}
            },
            'entity': ''
        }

    def test_create_enriched_payload_only_deliveries(
        self,
        express_delivery_enriched,
        pickupstore_enriched
    ):
        enriched_products = [express_delivery_enriched, pickupstore_enriched]

        enriched_products.sort(key=lambda x: x['source'])

        payload = _create_enriched_payload(enriched_products)

        assert payload == {
            'metadata': {
                'descriptive': {},
                'delivery': {
                    'Entrega rápida': [2],
                    'Retira loja': ['true']
                },
                'classified': {},
                'normalized_filters': {}
            },
            'filters_metadata': [],
            'entity': ''
        }

    def test_create_enriched_payload_only_descriptive(
        self,
        omnilogic_enriched,
        metabooks_enriched,
        smartcontent_enriched,
        expected_payload_enriched
    ):
        enriched_products = [omnilogic_enriched,
                             metabooks_enriched,
                             smartcontent_enriched]

        enriched_products.sort(key=lambda x: x['source'])

        payload = _create_enriched_payload(enriched_products)

        expected_payload_enriched['metadata']['delivery'] = {}
        assert payload == expected_payload_enriched

    def test_create_enriched_payload_only_descriptive_without_metadata(
        self,
        omnilogic_enriched,
        metabooks_enriched,
    ):
        del omnilogic_enriched['metadata']
        del metabooks_enriched['metadata']

        enriched_products = [omnilogic_enriched, metabooks_enriched]

        enriched_products.sort(key=lambda x: x['source'])

        payload = _create_enriched_payload(enriched_products)

        assert payload == {
            'metadata': {
                'descriptive': {},
                'delivery': {},
                'classified': {},
                'normalized_filters': {}
            },
            'filters_metadata': [
                'ISBN-10', 'ISBN-13', 'Gênero', 'Autor',
                'Tipo de Edição', 'Volume', 'Editora', 'Edição'
            ],
            'entity': 'Livro'
        }

    def test_create_enriched_payload_without_metadata_in_source_omnilogic(
        self,
        omnilogic_enriched
    ):
        del omnilogic_enriched['metadata']

        enriched_products = [omnilogic_enriched]

        enriched_products.sort(key=lambda x: x['source'])

        payload = _create_enriched_payload(enriched_products)

        assert payload == {
            'metadata': {
                'descriptive': {},
                'delivery': {},
                'classified': {},
                'normalized_filters': {}
            },
            'filters_metadata': [
                'ISBN-10', 'ISBN-13', 'Gênero', 'Autor',
                'Tipo de Edição', 'Volume', 'Editora', 'Edição'
            ],
            'entity': 'Livro'
        }

    def test_create_enriched_payload_without_metadata_in_source_metabooks( # noqa
        self,
        metabooks_enriched
    ):
        del metabooks_enriched['metadata']

        enriched_products = [metabooks_enriched]

        enriched_products.sort(key=lambda x: x['source'])

        payload = _create_enriched_payload(enriched_products)

        assert payload == {
            'metadata': {
                'descriptive': {},
                'delivery': {},
                'classified': {},
                'normalized_filters': {}
            },
            'filters_metadata': [],
            'entity': ''
        }

    def test_create_enriched_wakko_overwrite_omnilogic(
        self,
        omnilogic_enriched,
        metabooks_enriched,
        smartcontent_enriched,
        express_delivery_enriched,
        pickupstore_enriched,
        wakko_enriched,
        expected_payload_enriched
    ):
        enriched_products = [
            omnilogic_enriched,
            wakko_enriched,
            express_delivery_enriched,
            pickupstore_enriched,
            metabooks_enriched,
            smartcontent_enriched,
        ]

        sources = [x['source'] for x in enriched_products]
        enriched_products.sort(key=lambda x: x['source'])
        sorted_sources = [x['source'] for x in enriched_products]

        assert sources != sorted_sources

        payload = _create_enriched_payload(enriched_products)

        expected_payload_enriched['entity'] = 'Livro'
        expected_payload_enriched['filters_metadata'] = omnilogic_enriched['filters_metadata']  # noqa
        expected_payload_enriched['metadata']['descriptive']['Volume'] = ['90g'] # noqa
        expected_payload_enriched['metadata']['normalized_filters'] = {
            'Volume': ['90g'],
            'Quantidade': ['01 unidades']
        }

        assert payload == expected_payload_enriched

    def test_create_enriched_with_wakko_extracted_attributes_should_set_color(
        self,
        omnilogic_enriched,
        metabooks_enriched,
        smartcontent_enriched,
        express_delivery_enriched,
        pickupstore_enriched,
        wakko_enriched_classification_with_extracted_key,
        expected_payload_enriched
    ):
        enriched_products = [
            omnilogic_enriched,
            wakko_enriched_classification_with_extracted_key,
            express_delivery_enriched,
            pickupstore_enriched,
            metabooks_enriched,
            smartcontent_enriched,
        ]

        sources = [x['source'] for x in enriched_products]

        enriched_products.sort(key=lambda x: x['source'])

        sorted_sources = [x['source'] for x in enriched_products]

        assert sources != sorted_sources

        payload = _create_enriched_payload(enriched_products)

        descriptive = expected_payload_enriched['metadata']['descriptive']
        descriptive['Cor'] = ['Azul']
        descriptive['Volume'] = ['90g']
        descriptive['Classificação'] = ['murcho']

        assert payload['metadata']['descriptive'] == descriptive

    def test_create_enriched_wakko_overwrite_omnilogic_classification_not_normalized(  # noqa
        self,
        omnilogic_enriched,
        metabooks_enriched,
        smartcontent_enriched,
        reclassification_price_rule_enriched,
        express_delivery_enriched,
        pickupstore_enriched,
        wakko_enriched_classification_not_normalized,
        expected_payload_enriched
    ):
        enriched_products = [
            reclassification_price_rule_enriched,
            omnilogic_enriched,
            wakko_enriched_classification_not_normalized,
            express_delivery_enriched,
            pickupstore_enriched,
            metabooks_enriched,
            smartcontent_enriched,
        ]

        sources = [x['source'] for x in enriched_products]
        enriched_products.sort(key=lambda x: x['source'])
        sorted_sources = [x['source'] for x in enriched_products]

        assert sources != sorted_sources

        payload = _create_enriched_payload(enriched_products)

        descriptive = expected_payload_enriched['metadata']['descriptive']
        descriptive['Volume'] = ['90g']
        descriptive['Classificação'] = ['murcho']

        expected_payload_enriched.update({'entity': 'Peças para Refrigerador'})
        assert payload == expected_payload_enriched

    def test_create_enriched_wakko_overwrite_omnilogic_with_nsfw_classification(  # noqa
        self,
        omnilogic_enriched,
        metabooks_enriched,
        smartcontent_enriched,
        express_delivery_enriched,
        pickupstore_enriched,
        wakko_enriched_with_nsfw_classification,
        expected_payload_enriched
    ):
        enriched_products = [
            omnilogic_enriched,
            wakko_enriched_with_nsfw_classification,
            express_delivery_enriched,
            pickupstore_enriched,
            metabooks_enriched,
            smartcontent_enriched,
        ]

        sources = [x['source'] for x in enriched_products]

        enriched_products.sort(key=lambda x: x['source'])

        sorted_sources = [x['source'] for x in enriched_products]

        assert sources != sorted_sources

        payload = _create_enriched_payload(enriched_products)

        expected_payload_enriched['entity'] = 'Livro'
        expected_payload_enriched['filters_metadata'] = omnilogic_enriched['filters_metadata']  # noqa
        expected_payload_enriched['metadata']['descriptive']['Volume'] = [
            '90g'
        ]
        expected_payload_enriched['metadata']['classified']['nsfw'] = {'safe': 0.5, 'illustration': 0.35, 'hentai': 0.80, 'sensual': 0.82, 'porn': 0.85}  # noqa
        expected_payload_enriched['metadata']['classified']['category_id'] = 'IN'  # noqa

        assert payload == expected_payload_enriched

    def test_when_have_classification_hector_and_omnilogic_then_return_omnilogic(  # noqa
        self,
        omnilogic_enriched,
        mock_hector_enriched
    ):
        omnilogic_enriched['entity'] = 'omnilogic'
        enriched_products = [
            omnilogic_enriched,
            mock_hector_enriched
        ]
        payload = _create_enriched_payload(enriched_products)
        assert payload['entity'] == 'omnilogic'

    def test_when_have_classification_hector_and_omnilogic_is_none_then_return_hector(  # noqa
        self,
        omnilogic_enriched,
        mock_hector_enriched
    ):
        omnilogic_enriched['entity'] = None
        enriched_products = [
            mock_hector_enriched,
            omnilogic_enriched
        ]
        payload = _create_enriched_payload(enriched_products)
        assert payload['entity'] == 'hector'

    def test_when_have_hector_classification_then_return_hector(
        self,
        mock_hector_enriched
    ):
        payload = _create_enriched_payload([mock_hector_enriched])
        assert payload['entity'] == 'hector'


class TestContainsFulfillmentHelpers:

    @pytest.mark.parametrize('fulfillment,result', [
        (False, True),
        (True, True),
        (None, False)
    ])
    def test_with_fullfilment_field(
        self,
        fulfillment,
        result
    ):
        assert contains_fulfillment({'fulfillment': fulfillment}) == result

    @pytest.mark.parametrize('payload', [
        ({}), (None), ([])
    ])
    def test_without_fulfillment_field(
        self,
        payload
    ):
        assert not contains_fulfillment(payload)
