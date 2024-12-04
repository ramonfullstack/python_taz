import pytest


@pytest.fixture
def isbn():
    return '9788582604663'


@pytest.fixture
def product(isbn):
    return {
        'sells_to_company': True,
        'ean': '',
        'isbn': isbn,
        'seller_id': 'magazineluiza',
        'seller_description': 'Rocket Box',
        'sku': '1515489',
        'parent_sku': '1515489',
        'type': 'product',
        'main_variation': True,
        'title': 'Dragon Ball Super - Edição 3',
        'description': '<p> Dragon Ball Super - Edição 3 </p>  <p> </p>  <p>Trunks do Futuro surge novamente! Em seu mundo, um homem muito parecido com Goku, chamado de Goku Black está tentando acabar com a humanidade. Para ajudar Trunks, Goku e Vegeta vão ao futuro.</p>  <p> </p>  <p> Especificações </p>  <p> </p>  <p>- Editora: Panini<br /> - I.S.B.N.: 978-8542612608<br /> - Número de Páginas: 208<br /> - Gênero do Livro: Mangá<br /> - Acabamento: Brochura<br /> - Autor: Akira Toriyama<br /> - Ilustrador: Toyotarou<br /> - Ano da Edição: 2018</p>',  # noqa
        'reference': 'Panini',
        'brand': 'Panini',
        'sold_count': 0,
        'review_count': 0,
        'review_score': 0,
        'main_category': {
            'subcategory': {
                'id': 'FREL'
            },
            'id': 'EP'
        },
        'categories': [{
            'id': 'TM',
            'description': 'Livros',
            'subcategories': [{
                'id': 'HQRC',
                'description': 'História em Quadrinhos'
            }]
        }],
        'dimensions': {
            'width': 0.14,
            'depth': 0.01,
            'weight': 0.21,
            'height': 0.2
        },
        'release_date': '2019-01-21T17:05:56.062752+00:00',
        'updated_at': '2019-01-21T17:04:56.632197+00:00',
        'created_at': '2019-01-21T17:04:56.612093+00:00',
        'attributes': [],
        'disable_on_matching': False,
        'offer_title': 'Dragon Ball Super - Edição 3 - Panini',
        'grade': 10,
        'matching_strategy': 'SINGLE_SELLER',
        'navigation_id': 'hb15hfef3d',
        'md5': '49d526e14f6515f2b5c8bd62b44d7da5',
        'last_updated_at': '2019-01-21T17:06:00.622895'
    }


@pytest.fixture
def sku():
    return '123456789'


@pytest.fixture
def seller_id():
    return 'murcho'


@pytest.fixture
def navigation():
    return 'hb15hfef3d'


@pytest.fixture
def metabooks_save_categories(mongo_database):
    categories = [{
        'category_id': 'LI',
        'subcategory_ids': [
            'LGTA',
            'LDSO'
        ],
        'metabook_id': 'COM046050'
    }, {
        'category_id': 'LI',
        'subcategory_ids': [
            'LGTA',
            'LVDW'
        ],
        'metabook_id': 'COM051330'
    }, {
        'category_id': 'LI',
        'subcategory_ids': [
            'LGTA',
            'LCCO'
        ],
        'metabook_id': 'COM014000'
    }]

    mongo_database.metabooks_categories.insert_many(categories)


@pytest.fixture
def metadata():
    return {
        'audiences': [{
            'audienceDescription': 'Estudantes e profissionais da área de TI candidatos à certificação Microsoft.'  # noqa
        }, {
            'audienceCodeValue': '06',
            'audienceCodeType': '01'
        }],
        'titles': [{
            'titleType': '01',
            'title': 'Exam Ref 70-740',
            'subtitle': 'Instalação, Armazenamento e Computação com Windows Server 2016'  # noqa
        }],
        'salesRights': [{
            'countriesIncluded': ['BR'],
            'salesRightsType': '01'
        }, {
            'regionsIncluded': 'WORLD',
            'salesRightsType': '01'
        }],
        'edition': {
            'editionNumber': 1
        },
        'creationDate': '17.04.2018',
        'collections': [{
            'title': 'Microsoft',
            'subtitle': 'Exam Ref'
        }],
        'prices': [{
            'countriesIncluded': 'BR',
            'currencyCode': 'BRL',
            'priceAmount': 112,
            'priceType': '02',
            'taxes': [{
                'taxRateCode': 'Z',
                'taxRatePercent': 0
            }],
            'calculated': False,
            'priceTypeDescription': '0% MwSt.-Angabe vom Verlag',
            'priceStatus': '02'
        }],
        'publishers': [{
            'publisherIdType': '05',
            'adbName': 'BOOKMAN COMPANHIA EDITORA LTDA.',
            'publishingRole': '01',
            'publisherName': 'Bookman',
            'imprint': False,
            'idValue': 'BR0089739'
        }],
        'relatedProducts': [{
            'productIdValue': '9788582604649',
            'productIdType': '15',
            'productForm': 'BC',
            'productRelationCode': '23'
        }, {
            'productIdValue': '9788582604724',
            'productIdType': '15',
            'productForm': 'BC',
            'productRelationCode': '23'
        }, {
            'productIdValue': '9788582604670',
            'productIdType': '15',
            'productForm': 'EA',
            'productRelationCode': '27'
        }],
        'bitNo': 63436,
        'languages': [{
            'languageCode': 'por',
            'languageRole': '01'
        }],
        'form': {
            'thickness': 21,
            'productForm': 'BC',
            'productFormDetail': ['B304', 'B504'],
            'height': 175,
            'width': 250,
            'weight': 690
        },
        'publicationDate': '06.04.2018',
        'splitVat': False,
        'lastModificationDate': '04.02.2019',
        'supportingResources': [{
            'sha256Hash': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',  # noqa
            'imageHeight': 2953,
            'resourceMode': '03',
            'imageWidth': 2067,
            'resourceForm': '02',
            'contentAudience': ['00'],
            'lastUpdated': '20190201',
            'exportedLink': 'https://api.metabooks.com/api/v1/cover/9788582604663/m',  # noqa
            'md5Hash': '162d4792325b7912bd2b1a0cf5c9603d',
            'filesizeExact': 950142,
            'resourceContentType': '01',
            'fileFormat': 'D502',
            'filename': '9788582604663.jpg'
        }, {
            'sha256Hash': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',  # noqa
            'imageHeight': 2950,
            'resourceMode': '03',
            'imageWidth': 2066,
            'resourceForm': '02',
            'contentAudience': ['00'],
            'lastUpdated': '20190117',
            'exportedLink': 'https://api.metabooks.com/api/v1/asset/mmo/file/3794ebc4c5924f9da2c42a342412ac2f',  # noqa
            'md5Hash': '637717496923ffbcd165e2ee2b91d8c4',
            'filesizeExact': 1959588,
            'resourceContentType': '02',
            'fileFormat': 'D502',
            'filename': '9788582604663_contracapa.jpg'
        }, {
            'sha256Hash': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',  # noqa
            'imageHeight': 1534,
            'resourceMode': '03',
            'imageWidth': 1092,
            'resourceForm': '02',
            'contentAudience': ['00'],
            'lastUpdated': '20190117',
            'exportedLink': 'https://api.metabooks.com/api/v1/asset/mmo/file/74a4340630c247a4b9c7bdab864e7750',  # noqa
            'md5Hash': 'ec637ee9fd719382e30c276c331edc75',
            'filesizeExact': 396052,
            'resourceContentType': '15',
            'fileFormat': 'D502',
            'filename': '9788582604663_vi_04.jpg'
        }, {
            'sha256Hash': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',  # noqa
            'imageHeight': 1534,
            'resourceMode': '03',
            'imageWidth': 1092,
            'resourceForm': '02',
            'contentAudience': ['00'],
            'lastUpdated': '20190117',
            'exportedLink': 'https://api.metabooks.com/api/v1/asset/mmo/file/a202a509abfa4dca8c2c02a20fe8b332',  # noqa
            'md5Hash': 'd98093cfc32cecd1423fc1620252df03',
            'filesizeExact': 278617,
            'resourceContentType': '15',
            'fileFormat': 'D502',
            'filename': '9788582604663_vi_01.jpg'
        }, {
            'sha256Hash': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',  # noqa
            'imageHeight': 1534,
            'resourceMode': '03',
            'imageWidth': 1092,
            'resourceForm': '02',
            'contentAudience': ['00'],
            'lastUpdated': '20190117',
            'exportedLink': 'https://api.metabooks.com/api/v1/asset/mmo/file/62da306622a74d3c93a691cc72a00675',  # noqa
            'md5Hash': '67802836c6fab801121a2ac87433620e',
            'filesizeExact': 408188,
            'resourceContentType': '15',
            'fileFormat': 'D502',
            'filename': '9788582604663_vi_03.jpg'
        }, {
            'sha256Hash': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',  # noqa
            'imageHeight': 1534,
            'resourceMode': '03',
            'imageWidth': 1092,
            'resourceForm': '02',
            'contentAudience': ['00'],
            'lastUpdated': '20190117',
            'exportedLink': 'https://api.metabooks.com/api/v1/asset/mmo/file/bf64840758b14c01a3837d8b3975714d',  # noqa
            'md5Hash': 'af67d32873c9974f7db02eff9ebec0d6',
            'filesizeExact': 398765,
            'resourceContentType': '15',
            'fileFormat': 'D502',
            'filename': '9788582604663_vi_02.jpg'
        }, {
            'resourceMode': '04',
            'sha256Hash': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',  # noqa
            'md5Hash': 'b9ac3bf789542e526013fe3c7fc73aa6',
            'filesizeExact': 3937993,
            'resourceContentType': '15',
            'contentAudience': ['00'],
            'resourceForm': '02',
            'fileFormat': 'E107',
            'filename': '9788582604663_1_capitulo.pdf',
            'lastUpdated': '20180703',
            'exportedLink': 'https://api.metabooks.com/api/v1/asset/mmo/file/48d4de12f3264fc680961a5d1a979b16'  # noqa
        }],
        'contributors': [{
            'sequenceNumber': 1,
            'firstName': 'Craig',
            'biographicalNote': 'Autor e coautor de vários livros, manuais, artigos e sites sobre tópicos referentes a computadores e redes.',  # noqa
            'contributorRole': 'A01',
            'lastName': 'Zacker'
        }, {
            'sequenceNumber': 2,
            'firstName': 'Luciana Monteiro',
            'contributorRole': 'B02',
            'lastName': 'Michel'
        }, {
            'sequenceNumber': 3,
            'firstName': 'Aldir José Coelho Corrêa da',
            'contributorRole': 'B06',
            'lastName': 'Silva'
        }],
        'formFeatures': [{
            'productFormFeatureType': '01',
            'productFormFeatureDescription': '7%',
            'productFormFeatureValue': 'GLD'
        }, {
            'productFormFeatureType': '01',
            'productFormFeatureDescription': '87%',
            'productFormFeatureValue': 'GRN'
        }, {
            'productFormFeatureType': '01',
            'productFormFeatureDescription': '7%',
            'productFormFeatureValue': 'GRY'
        }],
        'textContents': [{
            'text': 'Livro preparatório para o exame de entrada da certificação MCSA, que comprova o domínio das habilidades essenciais do Windows Server 2016 para reduzir custos de TI e agregar mais valor ao negócio. Os exames 70-741 (Redes com Windows Server 2016) e o Exame 70-742 (Identidade com Windows Server 2016) também são necessários para a obtenção do MCSA Windows Server 2016.',  # noqa
            'textFormat': '06',
            'language': 'por',
            'textType': '02'
        }, {
            'text': 'Livro preparatório para o exame 70-740 da Microsoft, que foca nos recursos e nas funcionalidades de instalação, armazenamento e computação com Windows Server 2016. O texto está organizado por objetivos do exame e apresenta cenários estratégicos desafiadores. Parte do princípio de que o leitor já tem experiência com Windows Server em um ambiente corporativo e está familiarizado com a infraestrutura básica de redes, suas topologias, arquitetura e protocolos, bem como com clientes Windows e virtualização.',  # noqa
            'textContentAudience': ['00'],
            'textFormat': '06',
            'textType': '03'
        }],
        'productType': 'pbook',
        'productId': '67a4b9d63c974a578d59756fc9340821',
        'identifiers': [{
            'productIdentifierType': '02',
            'idValue': '8582604661'
        }, {
            'productIdentifierType': '03',
            'idValue': '9788582604663'
        }, {
            'productIdentifierType': '15',
            'idValue': '9788582604663'
        }],
        'subjects': [{
            'subjectSchemeVersion': '1.1',
            'sourceName': 'Publisher',
            'subjectHeadingText': 'Sistemas operativos Microsoft (Windows)',
            'subjectSchemeIdentifier': '93',
            'subjectCode': 'ULD',
            'mainSubject': True
        }, {
            'subjectSchemeVersion': '1.1',
            'sourceName': 'Publisher',
            'subjectHeadingText': 'Testagem e verificação de programas',
            'subjectSchemeIdentifier': '93',
            'subjectCode': 'UMZT',
            'mainSubject': False
        }, {
            'subjectSchemeVersion': '1.1',
            'sourceName': 'Publisher',
            'subjectHeadingText': 'Ciência informática',
            'subjectSchemeIdentifier': '93',
            'subjectCode': 'UY',
            'mainSubject': False
        }, {
            'subjectSchemeIdentifier': '10',
            'subjectSchemeName': 'MainSubject',
            'subjectCode': 'COM046050',
            'mainSubject': True
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'Bookman'
        }, {
            'subjectSchemeIdentifier': '10',
            'subjectSchemeName': 'BISACSubject',
            'subjectCode': 'COM051330',
            'mainSubject': False
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'Zacker, Craig'
        }, {
            'subjectSchemeIdentifier': '10',
            'subjectSchemeName': 'BISACSubject',
            'subjectCode': 'COM014000',
            'mainSubject': False
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'Exam Ref 70-740'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'Microsoft'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'tabela de partição GUID (GPT)'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'recuperação de desastre no Hyper-V'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'implantações de Linux e FreeBSD'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'arquivos VHD e VHDX'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'movimentação de VMs em nós de um cluster'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'servidores'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'Network Load Balancing (NLB)'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'cargas de trabalho'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'Microsoft Assessment and Planning (MAP) Toolkit'  # noqa
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'cluster de failover'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'desduplicação de dados'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'configurações de máquina virtual (VM)'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'manutenção e monitoramento de ambientes de servidor'  # noqa
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'implementação da alta disponibilidade'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'Windows Server Update Services'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'arquivos NTFS e ReFS'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'configurações de compartilhamento'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'Nano Server'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'migração'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'rede do Hyper-V'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'upgrade'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'virtualização'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'soluções de armazenamento'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'ambientes de host e de computação'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'discos rígidos virtuais'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'armazenamento no servidor'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'Storage Spaces Direct'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'contêineres de Windows'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'configurações de servidor e cliente'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'Windows Servers'
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'criar, gerenciar e fazer a manutenção de imagens para implantação'  # noqa
        }, {
            'subjectSchemeIdentifier': '20',
            'mainSubject': False,
            'subjectHeadingText': 'implementação do Hyper-V'
        }],
        'providerId': 'vpereira',
        'productClassifications': [{
            'productClassificationType': '10',
            'productClassificationCode': '4901.99.00'
        }],
        'publicationCity': ['Porto Alegre'],
        'productAvailability': '20',
        'extent': {
            'mainContentPageCount': 464
        },
        'active': True,
        'noContributor': False
    }


@pytest.fixture
def expected_metadata(sku, seller_id):
    return {
        'seller_id': seller_id,
        'sku': sku,
        'items': [{
            'slug': 'apresentacao',
            'display_name': 'Apresentação',
            'position': 1,
            'elements': [{
                'key_name': 'Sinopse',
                'position': 2,
                'elements': [{
                    'value': 'Livro preparatório para o exame de entrada da certificação MCSA, que comprova o domínio das habilidades essenciais do Windows Server 2016 para reduzir custos de TI e agregar mais valor ao negócio. Os exames 70-741 (Redes com Windows Server 2016) e o Exame 70-742 (Identidade com Windows Server 2016) também são necessários para a obtenção do MCSA Windows Server 2016.',  # noqa
                    'is_html': False
                }],
                'slug': 'sinopse'
            }]
        }, {
            'slug': 'ficha-tecnica',
            'display_name': 'Ficha-Técnica',
            'position': 6,
            'elements': [{
                'key_name': 'Informações técnicas',
                'position': 7,
                'elements': [{
                    'value': 'Bookman',
                    'key_name': 'Editora',
                    'position': 8,
                    'is_html': False,
                    'slug': 'editora'
                }, {
                    'value': 'Exam Ref 70-740',
                    'key_name': 'Título',
                    'position': 10,
                    'is_html': False,
                    'slug': 'titulo'
                }, {
                    'value': 'Instalação, Armazenamento e Computação com Windows Server 2016',  # noqa
                    'key_name': 'Subtítulo',
                    'position': 10,
                    'is_html': False,
                    'slug': 'subtitulo'
                }],
                'slug': 'informacoes-tecnicas'
            }, {
                'key_name': 'Autor',
                'position': 14,
                'elements': [{
                    'value': 'Zacker, Craig, Michel, Luciana Monteiro, Silva, Aldir José Coelho Corrêa da',  # noqa
                    'is_html': False
                }],
                'slug': 'autor'
            }, {
                'key_name': 'Ficha técnica',
                'position': 18,
                'elements': [{
                    'value': '464',
                    'key_name': 'Número de páginas',
                    'position': 21,
                    'is_html': False,
                    'slug': 'numero-de-paginas'
                }, {
                    'value': '1',
                    'key_name': 'Edição',
                    'position': 23,
                    'is_html': False,
                    'slug': 'edicao'
                }, {
                    'value': '06.04.2018',
                    'key_name': 'Data de publicação',
                    'position': 24,
                    'is_html': False,
                    'slug': 'data-de-publicacao'
                }, {
                    'value': 'Português',
                    'key_name': 'Idioma',
                    'position': 25,
                    'is_html': False,
                    'slug': 'idioma'
                }],
                'slug': 'ficha-tecnica'
            }, {
                'key_name': 'Código do produto',
                'position': 32,
                'elements': [{
                    'value': 'ISBN-10 - 8582604661\nGTIN-13 - 9788582604663\nISBN-13 - 9788582604663',  # noqa
                    'is_html': False
                }],
                'slug': 'codigo-do-produto'
            }, {
                'key_name': 'Peso aproximado',
                'position': 36,
                'elements': [{
                    'value': '690 gramas.',
                    'key_name': 'Peso do produto',
                    'position': 37,
                    'is_html': False,
                    'slug': 'peso-do-produto'
                }],
                'slug': 'peso-aproximado'
            }, {
                'key_name': 'Dimensões do produto',
                'position': 39,
                'elements': [{
                    'value': '(L x A x P): 25.0 x 17.5 x 21 cm.',
                    'key_name': 'Produto',
                    'position': 40,
                    'is_html': False,
                    'slug': 'produto'
                }],
                'slug': 'dimensoes-do-produto'
            }]
        }]
    }


@pytest.fixture
def product_smartcontent(mock_product_videos_message_data):
    return {
        'title': 'Freezer Vertical Consul 246L - CVU30EBANA',
        'entity': 'Freezer',
        'description': 'O Freezer Consul Vertical',
        'brand': 'Consul',
        'factsheet': {
            'display_name': 'Ficha-Técnica',
            'slug': 'ficha-tecnica',
            'elements': [
                {
                    'key_name': 'Marca',
                    'slug': 'marca',
                    'elements': [
                        {
                            'value': 'Consul'
                        }
                    ]
                },
                {
                    'key_name': 'Referência',
                    'slug': 'referencia',
                    'elements': [
                        {
                            'value': 'CVU30EBANA'
                        }
                    ]
                },
                {
                    'key_name': 'Modelo',
                    'slug': 'modelo',
                    'elements': [
                        {
                            'value': 'CVU30 EBANA'
                        }
                    ]
                }
            ]
        },
        'dimensions': {
            'weight': 58,
            'width': 0.62,
            'height': 1.7,
            'depth': 0.69
        },
        'special_content': '<center>Conteúdo especial</center>',
        'medias': {
            'images': [
                'https://img-tweety-sandbox.mlcdn.com.br/7891129208711/image/afd838ce163f09075da0567f6d3a1c98.JPEG' # noqa
            ],
            'videos': mock_product_videos_message_data,
            'podcasts': [],
            'manuals': []
        },
        'attributes': [{
            'slug': 'cor',
            'display_name': 'Cor',
            'value': 'Preto'
        }, {
            'slug': 'tamanho',
            'display_name': 'Tamanho',
            'value': '20 metros'
        }],
        'reference': '',
        'ean': '7891129208711'
    }


@pytest.fixture
def mock_expected_smartcontent_scope_payload(
    product,
    mock_product_videos_message_data
):
    seller_id = product['seller_id']
    sku = product['sku']
    navigation_id = product['navigation_id']
    return {
        'factsheet': {
            'seller_id': seller_id,
            'sku': sku,
            'items': [
                {
                    'display_name': 'Destaques',
                    'slug': 'destaques',
                    'elements': [
                        {
                            'key_name': 'Destaques',
                            'slug': 'destaques',
                            'elements': [
                                {
                                    'value': '<center>Conteúdo especial</center>' # noqa
                                }
                            ]
                        }
                    ]
                },
                {
                    'display_name': 'Apresentação',
                    'slug': 'apresentacao',
                    'elements': [
                        {
                            'key_name': 'Apresentação do produto',
                            'slug': 'apresentacao-do-produto',
                            'elements': [
                                {
                                    'value': 'O Freezer Consul Vertical' # noqa
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
                                    'value': 'Consul'
                                }
                            ]
                        },
                        {
                            'key_name': 'Referência',
                            'slug': 'referencia',
                            'elements': [
                                {
                                    'value': 'CVU30EBANA'
                                }
                            ]
                        },
                        {
                            'key_name': 'Modelo',
                            'slug': 'modelo',
                            'elements': [
                                {
                                    'value': 'CVU30 EBANA'
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        'media': {
            'seller_id': seller_id,
            'sku': sku,
            'images': {
                'images': [
                    'https://img-tweety-sandbox.mlcdn.com.br/7891129208711/image/afd838ce163f09075da0567f6d3a1c98.JPEG' # noqa
                ],
                'videos': mock_product_videos_message_data,
                'podcasts': []
            }
        },
        'enriched_product': {
            'seller_id': seller_id,
            'sku': sku,
            'navigation_id': navigation_id,
            'metadata': {
                'Cor': 'Preto',
                'Tamanho': '20 metros'
            },
            'title': 'Freezer Vertical Consul 246L - CVU30EBANA',
            'description': 'O Freezer Consul Vertical',
            'source': 'smartcontent',
            'entity': 'Freezer',
            'brand': 'Consul'
        }
    }


@pytest.fixture
def product_consumer_smartcontent(seller):
    return {
        'sells_to_company': True,
        'ean': '87654321',
        'isbn': '',
        'seller_id': seller,
        'seller_description': 'Rocket Box',
        'sku': '1515489',
        'parent_sku': '1515489',
        'type': 'product',
        'main_variation': True,
        'title': 'Dragon Ball Super - Edição 3',
        'description': '<p> Dragon Ball Super - Edição 3 </p>  <p> </p>  <p>Trunks do Futuro surge novamente! Em seu mundo, um homem muito parecido com Goku, chamado de Goku Black está tentando acabar com a humanidade. Para ajudar Trunks, Goku e Vegeta vão ao futuro.</p>  <p> </p>  <p> Especificações </p>  <p> </p>  <p>- Editora: Panini<br /> - I.S.B.N.: 978-8542612608<br /> - Número de Páginas: 208<br /> - Gênero do Livro: Mangá<br /> - Acabamento: Brochura<br /> - Autor: Akira Toriyama<br /> - Ilustrador: Toyotarou<br /> - Ano da Edição: 2018</p>',  # noqa
        'reference': 'Panini',
        'brand': 'Panini',
        'sold_count': 0,
        'review_count': 0,
        'review_score': 0,
        'categories': [{
            'id': 'AF',
            'description': 'Livros',
            'subcategories': [{
                'id': 'HQRC',
                'description': 'História em Quadrinhos'
            }]
        }],
        'dimensions': {
            'width': 0.14,
            'depth': 0.01,
            'weight': 0.21,
            'height': 0.2
        },
        'release_date': '2019-01-21T17:05:56.062752+00:00',
        'updated_at': '2019-01-21T17:04:56.632197+00:00',
        'created_at': '2019-01-21T17:04:56.612093+00:00',
        'attributes': [],
        'disable_on_matching': False,
        'offer_title': 'Dragon Ball Super - Edição 3 - Panini',
        'grade': 10,
        'matching_strategy': 'SINGLE_SELLER',
        'navigation_id': 'hb15hfef3d',
        'md5': '49d526e14f6515f2b5c8bd62b44d7da5',
        'last_updated_at': '2019-01-21T17:06:00.622895'
    }


@pytest.fixture
def mock_metabooks_images():
    return [{
        'hash': '7d7a3bc8a0a231a647e32489fafad827',
        'url': 'https://taz-metadata-images-sandbox.storage.googleapis.com/metabooks/9788542615524/9788542615524.jpg'  # noqa
    }]


@pytest.fixture
def mock_expected_metabooks_images(mock_metabooks_images, sku, seller_id):
    return {
        'images': mock_metabooks_images,
        'seller_id': seller_id,
        'sku': sku
    }


@pytest.fixture
def mock_expected_metabooks_enriched_product(sku, seller_id, navigation):
    return {
        'description': 'Livro preparatório para o exame de entrada da certificação MCSA, que comprova o domínio das habilidades essenciais do Windows Server 2016 para reduzir custos de TI e agregar mais valor ao negócio. Os exames 70-741 (Redes com Windows Server 2016) e o Exame 70-742 (Identidade com Windows Server 2016) também são necessários para a obtenção do MCSA Windows Server 2016.',  # noqa
        'navigation_id': navigation,
        'seller_id': seller_id,
        'sku': sku,
        'metadata': {
            'Editora': 'Bookman',
            'Edição': '1ª edição',
            'Autor': 'Zacker, Craig, Michel, Luciana Monteiro, Silva, Aldir José Coelho Corrêa da',  # noqa
            'Data de publicação': '06.04.2018',
            'Tipo de produto': 'pbook',
            'Número de páginas': '464',
            'Idiomas do produto': 'Português'
        },
        'title': 'Exam Ref 70-740',
        'subtitle': 'Instalação, Armazenamento e Computação com Windows Server 2016',  # noqa
        'source': 'metabooks',
        'entity': 'Livro',
        'category_id': 'LI'
    }
