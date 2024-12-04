import pytest


@pytest.fixture
def smartcontent_identified():
    return '8806098430031'


@pytest.fixture
def smartcontent_payload():
    return {
        'factsheet': {
            'display_name': 'Ficha-Técnica',
            'slug': 'ficha-tecnica',
            'elements': [
                {
                    'key_name': 'Marca',
                    'slug': 'marca',
                    'elements': [
                        {
                            'value': 'LG'
                        }
                    ]
                },
                {
                    'key_name': 'Referência',
                    'slug': 'referencia',
                    'elements': [
                        {
                            'value': '20M37AA-B.ASP'
                        }
                    ]
                },
                {
                    'key_name': 'Modelo',
                    'slug': 'modelo',
                    'elements': [
                        {
                            'value': '20M37AA'
                        }
                    ]
                },
                {
                    'key_name': 'Tipo de monitor',
                    'slug': 'tipo-de-monitor',
                    'elements': [
                        {
                            'value': 'LCD'
                        }
                    ]
                },
                {
                    'key_name': 'Resolução',
                    'slug': 'resolucao',
                    'elements': [
                        {
                            'value': '1366x768p'
                        }
                    ]
                },
                {
                    'key_name': 'Tipo de tela',
                    'slug': 'tipo-de-tela',
                    'elements': [
                        {
                            'value': 'LCD iluminada por LED'
                        }
                    ]
                },
                {
                    'key_name': 'Formato da tela',
                    'slug': 'formato-da-tela',
                    'elements': [
                        {
                            'value': '16:9 Widescreen'
                        }
                    ]
                },
                {
                    'key_name': 'Tamanho da tela',
                    'slug': 'tamanho-da-tela',
                    'elements': [
                        {
                            'value': '19,5\''
                        }
                    ]
                },
                {
                    'key_name': 'Tecnologia',
                    'slug': 'tecnologia',
                    'elements': [
                        {
                            'value': '- Flicker Safe\n- Reader Mode'
                        }
                    ]
                },
                {
                    'key_name': 'Recursos',
                    'slug': 'recursos',
                    'elements': [
                        {
                            'value': '- Super Energy Saving\n- Entrada RGB\n- Dual Smart Solution'  # noqa
                        }
                    ]
                },
                {
                    'key_name': 'Conexões',
                    'slug': 'conexoes',
                    'elements': [
                        {
                            'value': 'D-SUB (RGB).'
                        }
                    ]
                },
                {
                    'key_name': 'Ângulo de visão',
                    'slug': 'angulo-de-visao',
                    'elements': [
                        {
                            'value': '90º/65º'
                        }
                    ]
                },
                {
                    'key_name': 'Brilho',
                    'slug': 'brilho',
                    'elements': [
                        {
                            'value': '200cd/m²'
                        }
                    ]
                },
                {
                    'key_name': 'Contraste',
                    'slug': 'contraste',
                    'elements': [
                        {
                            'value': '5.000.000:1 (DFC)'
                        }
                    ]
                },
                {
                    'key_name': 'Tempo de resposta',
                    'slug': 'tempo-de-resposta',
                    'elements': [
                        {
                            'value': '5ms'
                        }
                    ]
                },
                {
                    'key_name': 'Número de cores',
                    'slug': 'numero-de-cores',
                    'elements': [
                        {
                            'value': '16,7M'
                        }
                    ]
                },
                {
                    'key_name': 'Pixel Pitch',
                    'slug': 'pixel-pitch',
                    'elements': [
                        {
                            'value': '0.3177 x 0.307 (mm)'
                        }
                    ]
                },
                {
                    'key_name': 'Horizontal',
                    'slug': 'horizontal',
                    'elements': [
                        {
                            'value': '30 ~ 61 KHz'
                        }
                    ]
                },
                {
                    'key_name': 'Vertical',
                    'slug': 'vertical',
                    'elements': [
                        {
                            'value': '56 ~ 75Hz'
                        }
                    ]
                },
                {
                    'key_name': 'Voltagem',
                    'slug': 'voltagem',
                    'elements': [
                        {
                            'value': 'Bivolt'
                        }
                    ]
                },
                {
                    'key_name': 'Consumo aproximado de energia',
                    'slug': 'consumo-aproximado-de-energia',
                    'elements': [
                        {
                            'value': '20W (Típico)'
                        }
                    ]
                },
                {
                    'key_name': 'Cor',
                    'slug': 'cor',
                    'elements': [
                        {
                            'value': 'Preto Fosco'
                        }
                    ]
                },
                {
                    'key_name': 'Conector de entrada',
                    'slug': 'conector-de-entrada',
                    'elements': [
                        {
                            'value': 'D-SUB'
                        }
                    ]
                },
                {
                    'key_name': 'Peso do produto',
                    'slug': 'peso-do-produto',
                    'elements': [
                        {
                            'value': '2,2kg'
                        }
                    ]
                },
                {
                    'key_name': 'Peso do produto com embalagem',
                    'slug': 'peso-do-produto-com-embalagem',
                    'elements': [
                        {
                            'value': '3,1kg'
                        }
                    ]
                },
                {
                    'key_name': 'Largura',
                    'slug': 'largura',
                    'elements': [
                        {
                            'value': '- Com base: 46,3cm\n- Sem base: 46,3cm'  # noqa
                        }
                    ]
                },
                {
                    'key_name': 'Altura',
                    'slug': 'altura',
                    'elements': [
                        {
                            'value': '- Com base: 35,7cm\n- Sem base: 28,7cm'  # noqa
                        }
                    ]
                },
                {
                    'key_name': 'Profundidade',
                    'slug': 'profundidade',
                    'elements': [
                        {
                            'value': '- Com base: 16,8cm\n- Sem base: 5,7cm'  # noqa
                        }
                    ]
                },
                {
                    'key_name': 'Largura',
                    'slug': 'largura',
                    'elements': [
                        {
                            'value': '53,4cm'
                        }
                    ]
                },
                {
                    'key_name': 'Altura',
                    'slug': 'altura',
                    'elements': [
                        {
                            'value': '35,3cm'
                        }
                    ]
                },
                {
                    'key_name': 'Profundidade',
                    'slug': 'profundidade',
                    'elements': [
                        {
                            'value': '11,1cm'
                        }
                    ]
                },
                {
                    'key_name': 'Prazo de Garantia',
                    'slug': 'prazo-de-garantia',
                    'elements': [
                        {
                            'value': '01 ano (3 meses de garantia legal e mais 9 meses de garantia especial concedida pelo fabricante).'  # noqa
                        }
                    ]
                },
                {
                    'key_name': 'Conteúdo da embalagem',
                    'slug': 'conteudo-da-embalagem',
                    'elements': [
                        {
                            'value': '- 01 Monitor\n- 01 Cabo D-SUB\n- 01 Adaptador AC\n- Manual do usuário'  # noqa
                        }
                    ]
                }
            ]
        },
        'description': 'O Monitor para PC 20M37AA da LG apresenta uma tela de 19,5\' 16:09 widescreen, painel LCD com iluminação de LED em uma resolução de 1366x768. ele conta com a função Dual Smart Solution trazendo mais facilidade e agilidade para realizar tarefas, e a função Super Energy Saving proporcionando maior economia de energia. Ainda conta com tecnologias Flicker Safe e Reader Mode, tudo pensado na saúde visual do usuário. O efeito flicker (piscadas imperceptíveis) são efeitos da variação de brilho nas imagens. No monitor LG esse efeito é quase zero, ou seja, menos cansaço visual,logo,usa-se o monitor por muito mais tempo.No Reader Mode a tela é personalizada de forma a ficar similar uma folha de papel ou um jornal. Diminui-se o tom azul, agredindo mesmo os olhos, e a consequência disso são leituras textuais de forma mais confortável.',  # noqa
        'dimensions': {
            'weight': 3.1,
            'width': 0.534,
            'height': 0.353,
            'depth': 0.111
        },
        'title': 'Monitor para PC LG 20M37AA 19,5” LCD - Widescreen HD',
        'brand': 'LG',
        'entity': 'Monitor',
        'medias': {
            'images': [
                'https://img-tweety-sandbox.mlcdn.com.br/8806098430031/image/044af14b50ea8110d1911d6aaba1dbad.JPEG'  # noqa
            ],
            'videos': [],
            'podcasts': [],
            'manuals': []
        },
        'attributes': [],
        'reference': '',
        'ean': '8806098430031'
    }


@pytest.fixture
def datasheet_identified():
    return '9917109541142'


@pytest.fixture
def datasheet_payload():
    return {
        'factsheet': {
            'display_name': 'Ficha-Técnica',
            'slug': 'ficha-tecnica',
            'elements': [
                {
                    'key_name': 'Marca',
                    'slug': 'marca',
                    'elements': [
                        {
                            'value': 'LG'
                        }
                    ]
                },
                {
                    'key_name': 'Referência',
                    'slug': 'referencia',
                    'elements': [
                        {
                            'value': '20M37AA-B.ASP'
                        }
                    ]
                },
                {
                    'key_name': 'Modelo',
                    'slug': 'modelo',
                    'elements': [
                        {
                            'value': '20M37AA'
                        }
                    ]
                },
                {
                    'key_name': 'Tipo de monitor',
                    'slug': 'tipo-de-monitor',
                    'elements': [
                        {
                            'value': 'LCD'
                        }
                    ]
                },
                {
                    'key_name': 'Resolução',
                    'slug': 'resolucao',
                    'elements': [
                        {
                            'value': '1366x768p'
                        }
                    ]
                },
                {
                    'key_name': 'Tipo de tela',
                    'slug': 'tipo-de-tela',
                    'elements': [
                        {
                            'value': 'LCD iluminada por LED'
                        }
                    ]
                },
                {
                    'key_name': 'Formato da tela',
                    'slug': 'formato-da-tela',
                    'elements': [
                        {
                            'value': '16:9 Widescreen'
                        }
                    ]
                },
                {
                    'key_name': 'Tamanho da tela',
                    'slug': 'tamanho-da-tela',
                    'elements': [
                        {
                            'value': '19,5\''
                        }
                    ]
                },
                {
                    'key_name': 'Tecnologia',
                    'slug': 'tecnologia',
                    'elements': [
                        {
                            'value': '- Flicker Safe\n- Reader Mode'
                        }
                    ]
                },
                {
                    'key_name': 'Recursos',
                    'slug': 'recursos',
                    'elements': [
                        {
                            'value': '- Super Energy Saving\n- Entrada RGB\n- Dual Smart Solution'  # noqa
                        }
                    ]
                },
                {
                    'key_name': 'Conexões',
                    'slug': 'conexoes',
                    'elements': [
                        {
                            'value': 'D-SUB (RGB).'
                        }
                    ]
                },
                {
                    'key_name': 'Ângulo de visão',
                    'slug': 'angulo-de-visao',
                    'elements': [
                        {
                            'value': '90º/65º'
                        }
                    ]
                },
                {
                    'key_name': 'Brilho',
                    'slug': 'brilho',
                    'elements': [
                        {
                            'value': '200cd/m²'
                        }
                    ]
                },
                {
                    'key_name': 'Contraste',
                    'slug': 'contraste',
                    'elements': [
                        {
                            'value': '5.000.000:1 (DFC)'
                        }
                    ]
                },
                {
                    'key_name': 'Tempo de resposta',
                    'slug': 'tempo-de-resposta',
                    'elements': [
                        {
                            'value': '5ms'
                        }
                    ]
                },
                {
                    'key_name': 'Número de cores',
                    'slug': 'numero-de-cores',
                    'elements': [
                        {
                            'value': '16,7M'
                        }
                    ]
                },
                {
                    'key_name': 'Pixel Pitch',
                    'slug': 'pixel-pitch',
                    'elements': [
                        {
                            'value': '0.3177 x 0.307 (mm)'
                        }
                    ]
                },
                {
                    'key_name': 'Horizontal',
                    'slug': 'horizontal',
                    'elements': [
                        {
                            'value': '30 ~ 61 KHz'
                        }
                    ]
                },
                {
                    'key_name': 'Vertical',
                    'slug': 'vertical',
                    'elements': [
                        {
                            'value': '56 ~ 75Hz'
                        }
                    ]
                },
                {
                    'key_name': 'Voltagem',
                    'slug': 'voltagem',
                    'elements': [
                        {
                            'value': 'Bivolt'
                        }
                    ]
                },
                {
                    'key_name': 'Consumo aproximado de energia',
                    'slug': 'consumo-aproximado-de-energia',
                    'elements': [
                        {
                            'value': '20W (Típico)'
                        }
                    ]
                },
                {
                    'key_name': 'Cor',
                    'slug': 'cor',
                    'elements': [
                        {
                            'value': 'Preto Fosco'
                        }
                    ]
                },
                {
                    'key_name': 'Conector de entrada',
                    'slug': 'conector-de-entrada',
                    'elements': [
                        {
                            'value': 'D-SUB'
                        }
                    ]
                },
                {
                    'key_name': 'Peso do produto',
                    'slug': 'peso-do-produto',
                    'elements': [
                        {
                            'value': '2,2kg'
                        }
                    ]
                },
                {
                    'key_name': 'Peso do produto com embalagem',
                    'slug': 'peso-do-produto-com-embalagem',
                    'elements': [
                        {
                            'value': '3,1kg'
                        }
                    ]
                },
                {
                    'key_name': 'Largura',
                    'slug': 'largura',
                    'elements': [
                        {
                            'value': '- Com base: 46,3cm\n- Sem base: 46,3cm'  # noqa
                        }
                    ]
                },
                {
                    'key_name': 'Altura',
                    'slug': 'altura',
                    'elements': [
                        {
                            'value': '- Com base: 35,7cm\n- Sem base: 28,7cm'  # noqa
                        }
                    ]
                },
                {
                    'key_name': 'Profundidade',
                    'slug': 'profundidade',
                    'elements': [
                        {
                            'value': '- Com base: 16,8cm\n- Sem base: 5,7cm'  # noqa
                        }
                    ]
                },
                {
                    'key_name': 'Largura',
                    'slug': 'largura',
                    'elements': [
                        {
                            'value': '53,4cm'
                        }
                    ]
                },
                {
                    'key_name': 'Altura',
                    'slug': 'altura',
                    'elements': [
                        {
                            'value': '35,3cm'
                        }
                    ]
                },
                {
                    'key_name': 'Profundidade',
                    'slug': 'profundidade',
                    'elements': [
                        {
                            'value': '11,1cm'
                        }
                    ]
                },
                {
                    'key_name': 'Prazo de Garantia',
                    'slug': 'prazo-de-garantia',
                    'elements': [
                        {
                            'value': '01 ano (3 meses de garantia legal e mais 9 meses de garantia especial concedida pelo fabricante).'  # noqa
                        }
                    ]
                },
                {
                    'key_name': 'Conteúdo da embalagem',
                    'slug': 'conteudo-da-embalagem',
                    'elements': [
                        {
                            'value': '- 01 Monitor\n- 01 Cabo D-SUB\n- 01 Adaptador AC\n- Manual do usuário'  # noqa
                        }
                    ]
                }
            ]
        },
        'description': 'O Monitor para PC 20M37AA da LG apresenta uma tela de 19,5\' 16:09 widescreen, painel LCD com iluminação de LED em uma resolução de 1366x768. ele conta com a função Dual Smart Solution trazendo mais facilidade e agilidade para realizar tarefas, e a função Super Energy Saving proporcionando maior economia de energia. Ainda conta com tecnologias Flicker Safe e Reader Mode, tudo pensado na saúde visual do usuário. O efeito flicker (piscadas imperceptíveis) são efeitos da variação de brilho nas imagens. No monitor LG esse efeito é quase zero, ou seja, menos cansaço visual,logo,usa-se o monitor por muito mais tempo.No Reader Mode a tela é personalizada de forma a ficar similar uma folha de papel ou um jornal. Diminui-se o tom azul, agredindo mesmo os olhos, e a consequência disso são leituras textuais de forma mais confortável.',  # noqa
        'dimensions': {
            'weight': 3.1,
            'width': 0.534,
            'height': 0.353,
            'depth': 0.111
        },
        'title': 'Monitor para PC LG 20M37AA 19,5” LCD - Widescreen HD',
        'brand': 'LG',
        'entity': 'Monitor',
        'medias': {
            'images': [
                'https://img-tweety-sandbox.mlcdn.com.br/8806098430031/image/044af14b50ea8110d1911d6aaba1dbad.JPEG'  # noqa
            ],
            'videos': [],
            'podcasts': [],
            'manuals': []
        },
        'attributes': [],
        'reference': '',
        'ean': '8806098430031'
    }


@pytest.fixture
def metabooks_identified():
    return '9788542615524'


@pytest.fixture
def metabooks_payload():
    return {
        'productId': '022d72e9d57640ceb5c7633be94993ac',
        'providerId': 'jpicorelli',
        'publicationDate': '05.02.2019',
        'titles': [{
            'title': 'Dragon Ball Super Vol. 4',
            'titleType': '01'
        }],
        'publishingStatus': '04',
        'noContributor': False,
        'edition': {'editionNumber': 4},
        'form': {
            'height': 200.0,
            'width': 137.0,
            'weight': 203.0,
            'thickness': 12.0,
            'productForm': 'BC'
        },
        'extent': {'mainContentPageCount': 200},
        'contributors': [{
            'firstName': 'Akira',
            'lastName': 'Toriyama',
            'webSites': [],
            'sequenceNumber': 1,
            'contributorRole': 'A01'
        }],
        'identifiers': [
            {
                'productIdentifierType': '02',
                'idValue': '8542615522'
            },
            {
                'productIdentifierType': '03',
                'idValue': '9788542615524'
            },
            {
                'productIdentifierType': '15',
                'idValue': '9788542615524'
            }
        ],
        'languages': [{
            'languageRole': '01',
            'languageCode': 'por'
        }],
        'prices': [{
            'priceType': '02',
            'countriesIncluded': 'BR',
            'currencyCode': 'BRL',
            'priceAmount': 21.9,
            'priceTypeDescription': '0% MwSt.-Angabe vom Verlag',
            'priceStatus': '02',
            'calculated': False,
            'taxes': [{
                'taxRatePercent': 0.0,
                'taxRateCode': 'Z'
            }]
        }],
        'publishers': [{
            'adbName': 'Panini Brasil LTDA',
            'imprint': False, 'webSites': [],
            'publishingRole': '01',
            'publisherName': 'Panini',
            'publisherIdType': '05',
            'idValue': 'BR0089650'
        }],
        'textContents': [{
            'textType': '03',
            'textFormat': '06',
            'text': (
                'O Goku Black que está destruindo '
                'o mundo paralelo do futuro '
                'é na verdade Zamasu, que '
                'planeja acabar com a '
                'humanidade por conta '
                'de seu senso de justiça '
                'distorcido. Depois de conseguir '
                'executar o mafuba, a única '
                'forma de derrotar o imortal '
                'Zamasu, Goku parte para encontrar '
                'o Trunks do futuro junto com Vegeta, '
                'sem saber o que os aguarda…'
            ),
            'textContentAudience': ['00']
        }],
        'formFeatures': [
            {
                'productFormFeatureType': '01',
                'productFormFeatureValue': 'GRN',
                'productFormFeatureDescription': '17%'
            },
            {
                'productFormFeatureType': '01',
                'productFormFeatureValue': 'GRY',
                'productFormFeatureDescription': '32%'
            },
            {
                'productFormFeatureType': '01',
                'productFormFeatureValue': 'SLV',
                'productFormFeatureDescription': '10%'
            },
            {
                'productFormFeatureType': '01',
                'productFormFeatureValue': 'WHI',
                'productFormFeatureDescription': '42%'
            }],
        'supportingResources': [{
            'resourceMode': '03',
            'resourceForm': '02',
            'fileFormat': 'D502',
            'imageHeight': 2480,
            'imageWidth': 1676,
            'filename': '9788542615524.jpg',
            'filesizeExact': 1472604,
            'md5Hash': '7d7a3bc8a0a231a647e32489fafad827',
            'sha256Hash': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',  # noqa
            'exportedLink': 'https://api.metabooks.com/api/v1/cover/9788542615524/m',  # noqa
            'assetUploadSource': 'VLB',
            'lastUpdated': '20190129',
            'resourceContentType': '01',
            'contentAudience': ['00']
        }],
        'active': True,
        'bitNo': 94381,
        'productType': 'pbook',
        'productAvailability': '20',
        'subjects': [
            {
                'sourceName': 'BISACMapping',
                'subjectSchemeIdentifier': '93',
                'subjectSchemeVersion': '1.1',
                'subjectCode': 'XAK',
                'subjectHeadingText': (
                    'Histórias em quadradinhos '
                    'e romances gráficos ao estilo '
                    'americano/britânico'
                ),
                'mainSubject': True
            },
            {
                'subjectSchemeIdentifier': '10',
                'subjectCode': 'CGN000000',
                'subjectSchemeName': 'MainSubject',
                'mainSubject': True
            }
        ],
        'productClassifications': [{
            'productClassificationType': '10',
            'productClassificationCode': '4901.99.00'
        }],
        'creationDate': '29.01.2019',
        'lastModificationDate': '05.02.2019',
        'splitVat': False
    }
