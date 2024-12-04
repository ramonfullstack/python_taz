class SmartcontentSamples:
    @classmethod
    def videos_payload(cls):
        return ['https://www.youtube.com/v/L76al18mF3Y?hl=pt&']

    @classmethod
    def payload_smartcontent(cls):
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
            'medias': {
                'images': [
                    'https://img-tweety-sandbox.mlcdn.com.br/7891129208711/image/afd838ce163f09075da0567f6d3a1c98.JPEG' # noqa
                ],
                'videos': cls.videos_payload(),
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
        }, {
            'seller_id': 'murcho',
            'sku': '123456789',
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
                                    'value': 'O Freezer Consul Vertical'
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
        }

    @classmethod
    def payload_smartcontent_with_special_content(cls):
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
                'videos': cls.videos_payload(),
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
        }, {
            'seller_id': 'murcho',
            'sku': '123456789',
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
                                    'value': '<center>Conteúdo especial</center>'  # noqa
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
                                    'value': 'O Freezer Consul Vertical'
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
        }

    @classmethod
    def payload_smartcontent_with_manual(cls):
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
                'videos': cls.videos_payload(),
                'podcasts': [],
                'manuals': [
                    'lava-roupa.pdf'
                ]
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
        }, {
            'seller_id': 'murcho',
            'sku': '123456789',
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
                                    'value': '<center>Conteúdo especial</center>'  # noqa
                                }
                            ]
                        }
                    ]
                },
                {
                    'display_name': 'Manual',
                    'slug': 'manual',
                    'elements': [
                        {
                            'key_name': 'Download do Manual',
                            'slug': 'download-do-manual',
                            'elements': [
                                {
                                    'value': '<p><a style=\"cursor: pointer; no-repeat scroll 0 0 transparent; display: block; height: 21px; width: 143px;\" title=\"Download Manual\" href=\"lava-roupa.pdf\" target=\"_blank\"> <img src=\"http://conteudoproduto.magazineluiza.com.br/manual/botao/botao_downloadmanual.gif\" alt=\"\" /> </a></p>' # noqa
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
                                    'value': 'O Freezer Consul Vertical'
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
        }

    @classmethod
    def payload_smartcontent_media(cls):
        return {
            'title': 'Freezer Vertical Consul 246L - CVU30EBANA',
            'entity': 'Freezer',
            'description': 'O Freezer Consul Vertical',
            'brand': 'Consul',
            'dimensions': {
                'weight': 58,
                'width': 0.62,
                'height': 1.7,
                'depth': 0.69
            },
            'medias': {
                'images': [
                    'https://img-tweety-sandbox.mlcdn.com.br/7891129208711/image/afd838ce163f09075da0567f6d3a1c98.JPEG' # noqa
                ],
                'videos': cls.videos_payload(),
                'podcasts': [],
                'manuals': []
            },
            'attributes': [],
            'reference': '',
            'ean': '7891129208711'
        }, {
            'seller_id': 'murcho',
            'sku': '123456789',
            'images': {
                'images': [
                    'https://img-tweety-sandbox.mlcdn.com.br/7891129208711/image/afd838ce163f09075da0567f6d3a1c98.JPEG' # noqa
                ],
                'videos': cls.videos_payload(),
                'podcasts': []
            }
        }

    @classmethod
    def payload_smartcontent_media_with_manual(cls):
        return {
            'title': 'Freezer Vertical Consul 246L - CVU30EBANA',
            'entity': 'Freezer',
            'description': 'O Freezer Consul Vertical',
            'brand': 'Consul',
            'dimensions': {
                'weight': 58,
                'width': 0.62,
                'height': 1.7,
                'depth': 0.69
            },
            'medias': {
                'images': [
                    'https://img-tweety-sandbox.mlcdn.com.br/7891129208711/image/afd838ce163f09075da0567f6d3a1c98.JPEG' # noqa
                ],
                'videos': cls.videos_payload(),
                'podcasts': [],
                'manuals': [
                    'https://manual.mlcdn.com.br/7891129208711/manual/afd838ce163f09075da0567f6d3a1c98.pdf'  # noqa
                ]
            },
            'attributes': [],
            'reference': '',
            'ean': '7891129208711'
        }, {
            'seller_id': 'murcho',
            'sku': '123456789',
            'images': {
                'images': [
                    'https://img-tweety-sandbox.mlcdn.com.br/7891129208711/image/afd838ce163f09075da0567f6d3a1c98.JPEG' # noqa
                ],
                'videos': cls.videos_payload(),
                'podcasts': []
            }
        }
