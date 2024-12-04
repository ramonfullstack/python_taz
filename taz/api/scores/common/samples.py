class ScoreSamples:

    title_between_31_and_60_characters = 'title::between_31_and_60_characters'
    description_between_251_and_1000_characters = 'description::between_251_and_1000_characters'  # noqa
    images_greater_than_3_images = 'images::greater_than_3_images'
    title_greater_than_60_characters = 'title::greater_than_60_characters'
    images_between_2_and_3_images = 'images::between_2_and_3_images'
    description_between_1_and_250_characters = 'description::between_1_and_250_characters'  # noqa

    @classmethod
    def score_a(cls):
        return {
            'md5': '40a70a00979631dac768a14369601712',
            'sku': '181160400',
            'seller_id': 'magazineluiza',
            'entity': 'brinquedo',
            'active': True,
            'timestamp': 1555476519.4684415,
            'version': 'v0_0_1',
            'final_score': 100.0,
            'category_id': 'BR',
            'sources': [
                {
                    'value': 'Playset Imaginext DTM81 Fisher-Price - 6 Peças',  # noqa
                    'points': 100.0,
                    'weight': 0.3,
                    'criteria': cls.title_between_31_and_60_characters
                },
                {
                    'value': 'Para estimular a imaginação e garantir a brincadeira da criançada, a Fisher Price lançou o divertido Playset Teen Titans Tower Imaginext DTM81!\n6 peças compõe a torre protegida por Robin que é atacado pelo Mamute. \nDurante a brincadeira pequenos heróis poderão impedir o ataque colocando Robin no elevador para o alto da torre, onde ele vira a plataforma e transforma os sofás em lançadores. \nO brinquedo é certificado pelo INMETRO e é indicado para crianças de 6 a 7 anos. \n\n\n\n\n',  # noqa
                    'points': 100.0,
                    'weight': 0.2,
                    'criteria': cls.description_between_251_and_1000_characters
                },
                {
                    'value': 5,
                    'points': 100.0,
                    'weight': 0.5,
                    'criteria': cls.images_greater_than_3_images
                }
            ]
        }

    @classmethod
    def score_b(cls):
        return {
            'md5': 'dee739c57c6c229f4b9ac77597ac686b',
            'sku': '010059801',
            'seller_id': 'magazineluiza',
            'timestamp': 1557165704.0759985,
            'version': 'v0_0_1',
            'sources': [
                {
                    'weight': 40,
                    'points': 40,
                    'criteria': cls.description_between_251_and_1000_characters,  # noqa
                    'value': 'Refrigerador com design sofisticado e painel Blue Touch com capacidade para 382 litros. Possui prateleiras de vidro resistente e mais fácil de limpar, além de serem 100% removíveis. Conta com gavetão de legumes e frutas com abertura diferenciada para proporcionar melhor organização e visualização, tem compartimento para alimentos frescos que conserva melhor os alimentos. O porta-latas é um acessório 2 em 1: Porta-latas + cesta multi-uso. Porta-latas com 4 unidades e cesta multi-uso, que pode ser utilizada como porta-condimentos ou cesta de frutas, por exemplo, podem ser utilizados juntos facilitando o transporte de latas. Além de todos os diferenciais o refrigerador não possui CFC e não agride a camada de ozônio. '  # noqa
                },
                {
                    'weight': 0,
                    'points': 100,
                    'criteria': cls.images_greater_than_3_images,
                    'value': 17
                },
                {
                    'weight': 60,
                    'points': 100,
                    'criteria': cls.title_greater_than_60_characters,
                    'value': 'Geladeira/Refrigerador Electrolux Frost Free  - Duplex 382L DF42'  # noqa
                }
            ],
            'entity_name': 'Refrigerador',
            'category_id': 'ED',
            'final_score': 76,
            'active': True
        }

    @classmethod
    def score_c(cls):
        return {
            'md5': 'dee739c57c6c229f4b9ac77597ac686b',
            'sku': '0123456789',
            'seller_id': 'magazineluiza',
            'timestamp': 1557165704.0759985,
            'version': 'v0_0_1',
            'sources': [
                {
                    'weight': 40,
                    'points': 40,
                    'criteria': cls.description_between_251_and_1000_characters,  # noqa
                    'value': 'Refrigerador com design sofisticado e painel Blue Touch com capacidade para 382 litros. Possui prateleiras de vidro resistente e mais fácil de limpar, além de serem 100% removíveis. Conta com gavetão de legumes e frutas com abertura diferenciada para proporcionar melhor organização e visualização, tem compartimento para alimentos frescos que conserva melhor os alimentos. O porta-latas é um acessório 2 em 1: Porta-latas + cesta multi-uso. Porta-latas com 4 unidades e cesta multi-uso, que pode ser utilizada como porta-condimentos ou cesta de frutas, por exemplo, podem ser utilizados juntos facilitando o transporte de latas. Além de todos os diferenciais o refrigerador não possui CFC e não agride a camada de ozônio. '  # noqa
                },
                {
                    'weight': 0,
                    'points': 100,
                    'criteria': cls.images_greater_than_3_images,
                    'value': 17
                },
                {
                    'weight': 60,
                    'points': 100,
                    'criteria': cls.title_greater_than_60_characters,
                    'value': 'Geladeira/Refrigerador Electrolux Frost Free  - Duplex 382L DF42'  # noqa
                }
            ],
            'entity_name': 'Refrigerador',
            'category_id': 'ED',
            'final_score': 76,
            'active': True
        }

    @classmethod
    def score_d(cls):
        return {
            'md5': '5e7f898fa0f49014dbf2f818f163c01a',
            'sku': '203631500',
            'seller_id': 'magazineluiza',
            'timestamp': 1557162022.3512895,
            'version': 'v0_0_1',
            'sources': [
                {
                    'weight': 40,
                    'points': 20,
                    'criteria': cls.description_between_1_and_250_characters,
                    'value': 'Jogo com 9 unidades sendo 3 de Aço Rápido para perfuração em metal, 3 de Wídea para perfuração em alvenaria e concreto e 3 de Aço Carbono para perfuração em madeira. Medidas: Aço Rápido (4,5 e 6 mm), Wídea (5,6 e 8 mm) e Madeira (4,5 e 6 mm).'  # noqa
                },
                {
                    'weight': 0,
                    'points': 50,
                    'criteria': cls.images_between_2_and_3_images,
                    'value': 2
                },
                {
                    'weight': 60,
                    'points': 50,
                    'criteria': cls.title_between_31_and_60_characters,
                    'value': 'Jogo de Brocas 9 Peças - BlackDecker BD0110CS'
                }
            ],
            'entity_name': 'Jogo de Brocas',
            'category_id': 'FS',
            'final_score': 38,
            'active': True
        }

    @classmethod
    def score_e(cls):
        return {
            'md5': '5e7f898fa0f49014dbf2f818f163c01a',
            'sku': '555555555',
            'seller_id': 'magazineluiza',
            'timestamp': 0,
            'version': 'v0_0_1',
            'sources': [
                {
                    'weight': 40,
                    'points': 20,
                    'criteria': cls.description_between_1_and_250_characters,
                    'value': 'Jogo com 9 unidades sendo 3 de Aço Rápido para perfuração em metal, 3 de Wídea para perfuração em alvenaria e concreto e 3 de Aço Carbono para perfuração em madeira. Medidas: Aço Rápido (4,5 e 6 mm), Wídea (5,6 e 8 mm) e Madeira (4,5 e 6 mm).'  # noqa
                },
                {
                    'weight': 0,
                    'points': 50,
                    'criteria': cls.images_between_2_and_3_images,
                    'value': 2
                },
                {
                    'weight': 60,
                    'points': 50,
                    'criteria': cls.title_between_31_and_60_characters,
                    'value': 'Jogo de Brocas 9 Peças - BlackDecker BD0110CS'
                }
            ],
            'entity_name': 'Jogo de Brocas',
            'category_id': 'FS',
            'final_score': 38,
            'active': True
        }
