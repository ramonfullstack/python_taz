from taz.constants import (
    SOURCE_GENERIC_CONTENT,
    SOURCE_RECLASSIFICATION_PRICE_RULE
)


class EnrichedProductSamples:

    @classmethod
    def shoploko_sku_74471(cls):
        return {
            'product_name': 'Fritadeira Elétrica Family AF-14 Mondial Inox Vermelho 3,2L',  # noqa
            'product_hash': '2ea47dcc52af6f1d3f19c35ad8b8ba30',
            'seller_id': 'shoploko',
            'navigation_id': '6242299',
            'sku': '74471',
            'sku_metadata': ['Voltagem'],
            'metadata': {
                'Modelo Nominal': 'Family',
                'Cor': 'Inox Vermelho',
                'Marca': 'Mondial',
                'Modelo': 'AF-14',
                'Produto': 'Fritadeira Elétrica',
                'Voltagem': '110 volts',
                'Tipo': 'Sem óleo',
                'Capacidade': '3,2L'
            },
            'filters_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade', 'Voltagem', 'Tipo', 'Potência'],  # noqa
            'source': 'magalu',
            'timestamp': 1525354056.712081,
            'product_name_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'entity': 'Fritadeira Elétrica',
            'subcategory_ids': ['FREL'],
            'category_id': 'EP',
            'product_matching_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Marca', 'Cor', 'Capacidade']  # noqa
        }

    @classmethod
    def shoploko_sku_155536300_with_technical_specification(cls):
        return {
            'sku': '155536300',
            'entity': 'Celular',
            'metadata': {
                'Sistema Operacional': 'Android Nougat',
                'Quantidade de Chips': 'Dual Chip',
                'Tamanho da Tela': '5.5 polegadas',
                'Tecnologia': '4G,Bluetooth,WiFi',
                'Memória RAM': '3GB',
                'Marca': 'Motorola',
                'Cor': 'Platinum',
                'Resolução da Câmera Traseira': '13MP',
                'Capacidade da Memória': '32GB',
                'Produto': 'Smartphone'
            },
            'seller_id': 'shoploko',
            'navigation_id': '155536300',
            'category_id': 'TE',
            'subcategory_ids': [
                'TCSP',
                'SRMT',
                'MGSP'
            ],
            'product_matching_metadata': [

            ],
            'product_name_metadata': [

            ],
            'sku_metadata': [

            ],
            'navigation_filter': [
                'Produto',
                'Marca',
                'Capacidade da Memória',
                'Cor',
                'Quantidade de Chips',
                'Resolução da Câmera Traseira',
                'Memória RAM',
                'Tamanho da Tela',
                'Sistema Operacional'
            ],
            'technical_specification': [
                'Marca',
                'Capacidade da Memória',
                'Cor',
                'Quantidade de Chips',
                'Resolução da Câmera Traseira',
                'Memória RAM',
                'Tamanho da Tela',
                'Sistema Operacional'
            ]
        }

    @classmethod
    def magazineluiza_sku_0233847(cls):
        return {
            'sku': '023384700',
            'seller_id': 'magazineluiza',
            'filters_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade', 'Voltagem', 'Tipo', 'Potência'],  # noqa
            'entity': 'Fritadeira Elétrica',
            'metadata': {
                'Tipo': 'Sem óleo',
                'Cor': 'Inox Vermelho',
                'Capacidade': '3,2L',
                'Modelo Nominal': 'Family',
                'Voltagem': '110 volts',
                'Modelo': 'AF-14',
                'Produto': 'Fritadeira Elétrica',
                'Marca': 'Mondial'
            },
            'navigation_id': '023384800',
            'timestamp': 1525354062.0433378,
            'product_name': 'Fritadeira Elétrica Family AF-14 Mondial Inox Vermelho 3,2L',  # noqa
            'product_matching_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'product_name_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'source': 'magalu',
            'sku_metadata': ['Voltagem'],
            'subcategory_ids': ['FREL'],
            'category_id': 'EP',
            'product_hash': '2ea47dcc52af6f1d3f19c35ad8b8ba30'
        }

    @classmethod
    def magazineluiza_sku_0233847_smartcontent(cls):
        return {
            'seller_id': 'magazineluiza',
            'sku': '023384700',
            'navigation_id': '023384700',
            'metadata': {
                'Voltagem': '220 volts'
            },
            'title': 'Fritadeira Elétrica Air Fryer/Sem Óleo Mondial - 110 volts',  # noqa
            'description': 'O que era inimaginável agora é real. Fritar comidas sem óleo.',  # noqa
            'source': 'smartcontent',
            'entity': 'Freezer',
            'brand': 'Mondial'
        }

    @classmethod
    def topbrinquedos_sku_2898(cls):
        return {
            'source': 'magalu',
            'sku': '2898',
            'entity': 'Fritadeira Elétrica',
            'subcategory_ids': ['FREL'],
            'product_name': 'Fritadeira Elétrica Family AF-14 Mondial Inox Vermelho 3,2L',  # noqa
            'metadata': {
                'Voltagem': '110 volts',
                'Modelo Nominal': 'Family',
                'Modelo': 'AF-14',
                'Capacidade': '3,2L',
                'Cor': 'Inox Vermelho',
                'Potência': '1500 W',
                'Marca': 'Mondial',
                'Produto': 'Fritadeira Elétrica'
            },
            'product_name_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'category_id': 'EP',
            'sku_metadata': ['Voltagem'],
            'product_matching_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'filters_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade', 'Voltagem', 'Tipo', 'Potência'],  # noqa
            'navigation_id': '6520581',
            'timestamp': 1525354141.062616,
            'product_hash': '2ea47dcc52af6f1d3f19c35ad8b8ba30',
            'seller_id': 'topbrinquedos'
        }

    @classmethod
    def amplocomercial_sku_230(cls):
        return {
            'metadata': {
                'Voltagem': '110 volts',
                'Cor': 'Inox Vermelho',
                'Potência': '1500 W',
                'Modelo Nominal': 'Family',
                'Produto': 'Fritadeira Elétrica',
                'Capacidade': '3,2L',
                'Marca': 'Mondial',
                'Modelo': 'AF-14'
            },
            'category_id': 'EP',
            'entity': 'Fritadeira Elétrica',
            'subcategory_ids': ['FREL'],
            'product_hash': '2ea47dcc52af6f1d3f19c35ad8b8ba30',
            'sku_metadata': ['Voltagem'],
            'seller_id': 'amplocomercial',
            'filters_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade', 'Voltagem', 'Tipo', 'Potência'],  # noqa
            'product_name': 'Fritadeira Elétrica Family AF-14 Mondial Inox Vermelho 3,2L',  # noqa
            'sku': '230',
            'product_matching_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'navigation_id': '6699102',
            'source': 'magalu',
            'product_name_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'timestamp': 1525354142.1856334
        }

    @classmethod
    def efacil_sku_200298(cls):
        return {
            'seller_id': 'efacil',
            'product_hash': '2ea47dcc52af6f1d3f19c35ad8b8ba30',
            'entity': 'Fritadeira Elétrica',
            'product_matching_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'timestamp': 1525354297.0842378,
            'filters_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade', 'Voltagem', 'Tipo', 'Potência'],  # noqa
            'product_name': 'Fritadeira Elétrica Family AF-14 Mondial Inox Vermelho 3,2L',  # noqa
            'metadata': {
                'Marca': 'Mondial',
                'Modelo': 'AF-14',
                'Cor': 'Inox Vermelho',
                'Produto': 'Fritadeira Elétrica',
                'Tipo': 'Sem óleo',
                'Potência': '1500 W',
                'Modelo Nominal': 'Family',
                'Voltagem': '110 volts',
                'Capacidade': '3,2L'
            },
            'sku': '200298-102',
            'sku_metadata': ['Voltagem'],
            'category_id': 'EP',
            'subcategory_ids': ['FREL'],
            'navigation_id': '6836352',
            'source': 'magalu',
            'product_name_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade']  # noqa
        }

    @classmethod
    def mainshop_sku_5643126(cls):
        return {
            'filters_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade', 'Voltagem', 'Tipo', 'Potência'],  # noqa
            'metadata': {
                'Capacidade': '3,2L',
                'Modelo': 'AF-14',
                'Marca': 'Mondial',
                'Voltagem': '110 volts',
                'Potência': '1500 W',
                'Cor': 'Inox Vermelho',
                'Produto': 'Fritadeira Elétrica',
                'Modelo Nominal': 'Family'
            },
            'product_matching_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'subcategory_ids': ['FREL'],
            'sku_metadata': ['Voltagem'],
            'seller_id': 'mainshop',
            'category_id': 'EP',
            'source': 'magalu',
            'product_name': 'Fritadeira Elétrica Family AF-14 Mondial Inox Vermelho 3,2L',  # noqa
            'navigation_id': '6189785',
            'timestamp': 1525354318.7075264,
            'entity': 'Fritadeira Elétrica',
            'product_name_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'product_hash': '2ea47dcc52af6f1d3f19c35ad8b8ba30',
            'sku': '346914'
        }

    @classmethod
    def mainshop_sku_5643123(cls):
        return {
            'product_name_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'timestamp': 1525354327.5888195,
            'product_name': 'Fritadeira Elétrica Family AF-14 Mondial Inox Vermelho 3,2L',  # noqa
            'category_id': 'EP',
            'filters_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade', 'Voltagem', 'Tipo', 'Potência'],  # noqa
            'entity': 'Fritadeira Elétrica',
            'product_matching_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'source': 'magalu',
            'sku_metadata': ['Voltagem'],
            'product_hash': '2ea47dcc52af6f1d3f19c35ad8b8ba30',
            'subcategory_ids': ['FREL'],
            'sku': '346913',
            'navigation_id': '6188565',
            'metadata': {
                'Capacidade': '3,2L',
                'Potência': '1500 W',
                'Marca': 'Mondial',
                'Modelo Nominal': 'Family',
                'Modelo': 'AF-14',
                'Voltagem': '220 volts',
                'Cor': 'Inox Vermelho',
                'Produto': 'Fritadeira Elétrica'
            },
            'seller_id': 'mainshop'
        }

    @classmethod
    def gynshop_sku_5643188(cls):
        return {
            'product_name_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'timestamp': 1525354370.798667,
            'product_name': 'Fritadeira Elétrica Family AF-14 Mondial Inox Vermelho 3,2L',  # noqa
            'category_id': 'EP',
            'filters_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade', 'Voltagem', 'Tipo', 'Potência'],  # noqa
            'entity': 'Fritadeira Elétrica',
            'product_matching_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'source': 'magalu',
            'sku_metadata': ['Voltagem'],
            'product_hash': '2ea47dcc52af6f1d3f19c35ad8b8ba30',
            'subcategory_ids': ['FREL'],
            'sku': '346914',
            'navigation_id': '6524992',
            'metadata': {
                'Capacidade': '3,2L',
                'Potência': '1500 W',
                'Marca': 'Mondial',
                'Modelo Nominal': 'Family',
                'Modelo': 'AF-14',
                'Voltagem': '110 volts',
                'Cor': 'Inox Vermelho',
                'Produto': 'Fritadeira Elétrica'
            },
            'seller_id': 'gynshop'
        }

    @classmethod
    def gynshop_sku_5643191(cls):
        return {
            'navigation_id': '6663080',
            'source': 'magalu',
            'sku_metadata': ['Voltagem'],
            'filters_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade', 'Voltagem', 'Tipo', 'Potência'],  # noqa
            'timestamp': 1525354378.0414371,
            'category_id': 'EP',
            'product_name': 'Fritadeira Elétrica Family AF-14 Mondial Inox Vermelho 3,2L',  # noqa
            'sku': '346913',
            'product_hash': '2ea47dcc52af6f1d3f19c35ad8b8ba30',
            'metadata': {
                'Cor': 'Inox Vermelho',
                'Capacidade': '3,2L',
                'Produto': 'Fritadeira Elétrica',
                'Marca': 'Mondial',
                'Modelo Nominal': 'Family',
                'Modelo': 'AF-14',
                'Potência': '1500 W',
                'Voltagem': '220 volts'
            },
            'product_name_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'seller_id': 'gynshop',
            'subcategory_ids': ['FREL'],
            'entity': 'Fritadeira Elétrica',
            'product_matching_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Marca', 'Cor', 'Capacidade']  # noqa
        }

    @classmethod
    def efacil_sku_185402(cls):
        return {
            'product_hash': '2ea47dcc52af6f1d3f19c35ad8b8ba30',
            'seller_id': 'efacil',
            'filters_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade', 'Voltagem', 'Tipo', 'Potência'],  # noqa
            'subcategory_ids': ['FREL'],
            'timestamp': 1525354623.1587853,
            'product_name': 'Fritadeira Elétrica Family AF-14 Mondial Inox Vermelho 3,2L',  # noqa
            'metadata': {
                'Produto': 'Fritadeira Elétrica',
                'Modelo': 'AF-14',
                'Cor': 'Inox Vermelho',
                'Marca': 'Mondial',
                'Potência': '1500 W',
                'Modelo Nominal': 'Family',
                'Voltagem': '220 volts',
                'Capacidade': '3,2L'
            },
            'sku': '185402',
            'entity': 'Fritadeira Elétrica',
            'sku_metadata': ['Voltagem'],
            'category_id': 'EP',
            'product_matching_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'navigation_id': '6841431',
            'source': 'magalu',
            'product_name_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade']  # noqa
        }

    @classmethod
    def casa_e_video_sku_10359(cls):
        return {
            'metadata': {
                'Voltagem': '110 volts',
                'Tipo': 'Sem óleo',
                'Cor': 'Inox Vermelho',
                'Potência': '1500 W',
                'Modelo Nominal': 'Family',
                'Produto': 'Fritadeira Elétrica',
                'Capacidade': '3,2L',
                'Marca': 'Mondial',
                'Modelo': 'AF-14'
            },
            'category_id': 'EP',
            'product_hash': '2ea47dcc52af6f1d3f19c35ad8b8ba30',
            'subcategory_ids': ['FREL'],
            'entity': 'Fritadeira Elétrica',
            'sku_metadata': ['Voltagem'],
            'product_name': 'Fritadeira Elétrica Family AF-14 Mondial Inox Vermelho 3,2L',  # noqa
            'filters_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade', 'Voltagem', 'Tipo', 'Potência'],  # noqa
            'seller_id': 'casa-e-video',
            'sku': '10099',
            'product_matching_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'navigation_id': '7486857',
            'product_name_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'source': 'magalu',
            'timestamp': 1525354626.9445732
        }

    @classmethod
    def topbrinquedos_sku_1964(cls):
        return {
            'product_matching_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'timestamp': 1525354633.5891047,
            'sku_metadata': ['Voltagem'],
            'product_name_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'navigation_id': '6686757',
            'source': 'magalu',
            'product_hash': '2ea47dcc52af6f1d3f19c35ad8b8ba30',
            'seller_id': 'topbrinquedos',
            'sku': '1964',
            'metadata': {
                'Potência': '1500 W',
                'Marca': 'Mondial',
                'Cor': 'Inox Vermelho',
                'Voltagem': '220 volts',
                'Capacidade': '3,2L',
                'Modelo Nominal': 'Family',
                'Modelo': 'AF-14',
                'Produto': 'Fritadeira Elétrica'
            },
            'category_id': 'EP',
            'product_name': 'Fritadeira Elétrica Family AF-14 Mondial Inox Vermelho 3,2L',  # noqa
            'filters_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade', 'Voltagem', 'Tipo', 'Potência'],  # noqa
            'entity': 'Fritadeira Elétrica',
            'subcategory_ids': ['FREL']
        }

    @classmethod
    def amplocomercial_sku_232(cls):
        return {
            'source': 'magalu',
            'sku': '232',
            'entity': 'Fritadeira Elétrica',
            'subcategory_ids': ['FREL'],
            'product_name': 'Fritadeira Elétrica Family AF-14 Mondial Inox Vermelho 3,2L',  # noqa
            'metadata': {
                'Voltagem': '220 volts',
                'Modelo Nominal': 'Family',
                'Modelo': 'AF-14',
                'Capacidade': '3,2L',
                'Cor': 'Inox Vermelho',
                'Potência': '1500 W',
                'Marca': 'Mondial',
                'Produto': 'Fritadeira Elétrica'
            },
            'product_name_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'category_id': 'EP',
            'sku_metadata': ['Voltagem'],
            'product_matching_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'filters_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade', 'Voltagem', 'Tipo', 'Potência'],  # noqa
            'navigation_id': '6168966',
            'timestamp': 1525354753.8386488,
            'product_hash': '2ea47dcc52af6f1d3f19c35ad8b8ba30',
            'seller_id': 'amplocomercial'
        }

    @classmethod
    def lojasmel_openapi_45035(cls):
        return {
            'source': 'magalu',
            'category_id': 'EP',
            'subcategory_ids': ['FREL'],
            'product_hash': None,
            'sku': '45035',
            'product_matching_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'entity': 'Fritadeira Elétrica',
            'metadata': {
                'Marca': 'Zeex',
                'Produto': 'Fritadeira Elétrica',
                'Voltagem': '110 volts',
                'Cor': 'Inox',
                'Modelo': 'FT235',
                'Capacidade': '1L',
                'Modelo Nominal': 'Frit Fast'
            },
            'timestamp': 1525900168.4950786,
            'seller_id': 'lojasmel-openapi',
            'product_name_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'sku_metadata': ['Voltagem'],
            'filters_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade', 'Voltagem', 'Tipo', 'Potência'],  # noqa
            'product_name': 'Fritadeira Elétrica Frit Fast FT235 Zeex Inox 1L',
            'navigation_id': '7908856'
        }

    @classmethod
    def gazinshop_4470(cls):
        return {
            'product_name': None,
            'timestamp': 1525900824.7776477,
            'sku': '4470',
            'category_id': 'EP',
            'product_name_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'sku_metadata': ['Voltagem'],
            'product_hash': None,
            'source': 'magalu',
            'product_matching_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'seller_id': 'gazinshop',
            'entity': 'Fritadeira Elétrica',
            'metadata': {
                'Potência': '1270 W',
                'Voltagem': '220 volts',
                'Tipo': 'Sem óleo',
                'Capacidade': '2,4L',
                'Marca': 'Mondial',
                'Produto': 'Fritadeira Elétrica'
            },
            'navigation_id': '6652228',
            'filters_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade', 'Voltagem', 'Tipo', 'Potência'],  # noqa
            'subcategory_ids': ['FREL']
        }

    @classmethod
    def colormaq_sku_1408001_1(cls):
        return {
            'product_name_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'source': 'magalu',
            'navigation_id': '6712039',
            'sku_metadata': ['Voltagem'],
            'metadata': {
                'Voltagem': '110 Volts',
                'Potência': '1500 W',
                'Tipo': 'Sem óleo',
                'Marca': 'Colormaq',
                'Cor': 'Preto',
                'Capacidade': '3,6L',
                'Produto': 'Fritadeira Elétrica',
                'Modelo Nominal': 'Air Fryer'
            },
            'filters_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade', 'Voltagem', 'Tipo', 'Potência'],  # noqa
            'category_id': 'EP',
            'entity': 'Fritadeira Elétrica',
            'seller_id': 'colormaq',
            'subcategory_ids': ['FREL'],
            'sku': '1408001-1',
            'timestamp': 1527190341.3066921,
            'product_matching_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'product_name': 'Fritadeira Elétrica Air Fryer Colormaq Preto 3,6L',  # noqa
            'product_hash': 'e6abef7cec153ad43188394b6cf9c008'
        }

    @classmethod
    def colormaq_sku_1408002(cls):
        return {
            'product_name_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'source': 'magalu',
            'navigation_id': '6158329',
            'sku_metadata': ['Voltagem'],
            'metadata': {
                'Voltagem': '220 Volts',
                'Potência': '1500 W',
                'Tipo': 'Sem óleo',
                'Marca': 'Colormaq',
                'Cor': 'Preto',
                'Capacidade': '3,6L',
                'Produto': 'Fritadeira Elétrica',
                'Modelo Nominal': 'Air Fryer'
            },
            'filters_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Linha', 'Marca', 'Cor', 'Capacidade', 'Voltagem', 'Tipo', 'Potência'],  # noqa
            'category_id': 'EP',
            'entity': 'Fritadeira Elétrica',
            'seller_id': 'colormaq',
            'subcategory_ids': ['FREL'],
            'sku': '1408002',
            'timestamp': 1527190152.7638397,
            'product_matching_metadata': ['Produto', 'Modelo Nominal', 'Modelo', 'Marca', 'Cor', 'Capacidade'],  # noqa
            'product_name': 'Fritadeira Elétrica Air Fryer Colormaq Preto 3,6L',  # noqa
            'product_hash': 'e6abef7cec153ad43188394b6cf9c008'
        }

    @classmethod
    def maniavirtual_sku_9022086_01(cls):
        return {
            'entity': 'Torradeira',
            'product_hash': '0d9a74a782ae7f4141befd08915d2cab',
            'product_name_metadata': ['Produto', 'Marca', 'Cor', 'Material', 'Linha', 'Modelo Nominal', 'Modelo', 'Fatias', 'Painel', 'Níveis de Tostagem'],  # noqa
            'source': 'magalu',
            'category_id': 'EP',
            'navigation_id': '6933227',
            'metadata': {
                'Cor': 'Vermelha',
                'Modelo Nominal': 'Tosta Pane',
                'Marca': 'Britânia',
                'Fatias': '2 Fatias',
                'Produto': 'Torradeira',
                'Voltagem': '220 Volts',
                'Material': 'Metal Plástico',
                'Níveis de Tostagem': '7 Níveis de Tostagem',
                'Tipo': 'Elétrica'
            },
            'subcategory_ids': ['TOST'],
            'product_matching_metadata': ['Produto', 'Marca', 'Cor', 'Modelo Nominal', 'Modelo'],  # noqa
            'product_name': 'Torradeira Britânia Vermelha Tosta Pane 7 Níveis de Tostagem',  # noqa
            'seller_id': 'maniavirtual',
            'timestamp': 1531338226.9365623,
            'filters_metadata': ['Produto', 'Marca', 'Cor', 'Material', 'Linha', 'Modelo Nominal', 'Modelo', 'Fatias', 'Painel', 'Níveis de Tostagem', 'Voltagem', 'Tipo'],  # noqa
            'sku_metadata': ['Voltagem'],
            'sku': '9022086-01'
        }

    @classmethod
    def maniavirtual_sku_9022085_01(cls):
        return {
            'entity': 'Torradeira',
            'source': 'magalu',
            'sku': '9022085-01',
            'sku_metadata': ['Voltagem'],
            'product_name_metadata': ['Produto', 'Marca', 'Cor', 'Material', 'Linha', 'Modelo Nominal', 'Modelo', 'Fatias', 'Painel', 'Níveis de Tostagem'],  # noqa
            'product_hash': '0d9a74a782ae7f4141befd08915d2cab',
            'metadata': {
                'Cor': 'Vermelha',
                'Níveis de Tostagem': '7 Níveis de Tostagem',
                'Modelo Nominal': 'Tosta Pane',
                'Tipo': 'Elétrica',
                'Fatias': '2 Fatias',
                'Voltagem': '110 Volts',
                'Material': 'Metal Plástico',
                'Produto': 'Torradeira',
                'Marca': 'Britânia'
            },
            'timestamp': 1531338336.3085113,
            'subcategory_ids': ['TOST'],
            'navigation_id': '6923118',
            'product_name': 'Torradeira Britânia Vermelha Tosta Pane 7 Níveis de Tostagem',  # noqa
            'seller_id': 'maniavirtual',
            'product_matching_metadata': ['Produto', 'Marca', 'Cor', 'Modelo Nominal', 'Modelo'],  # noqa
            'category_id': 'EP',
            'filters_metadata': ['Produto', 'Marca', 'Cor', 'Material', 'Linha', 'Modelo Nominal', 'Modelo', 'Fatias', 'Painel', 'Níveis de Tostagem', 'Voltagem', 'Tipo']  # noqa
        }

    @classmethod
    def casa_e_video_sku_8186(cls):
        return {
            'category_id': 'EP',
            'source': 'magalu',
            'sku': '8186',
            'filters_metadata': ['Produto', 'Marca', 'Cor', 'Material', 'Linha', 'Modelo Nominal', 'Modelo', 'Fatias', 'Painel', 'Níveis de Tostagem', 'Voltagem', 'Tipo'],  # noqa
            'timestamp': 1531338327.9613247,
            'seller_id': 'casa-e-video',
            'entity': 'Torradeira',
            'subcategory_ids': ['TOST'],
            'product_hash': '0d9a74a782ae7f4141befd08915d2cab',
            'product_name_metadata': ['Produto', 'Marca', 'Cor', 'Material', 'Linha', 'Modelo Nominal', 'Modelo', 'Fatias', 'Painel', 'Níveis de Tostagem'],  # noqa
            'product_matching_metadata': ['Produto', 'Marca', 'Cor', 'Modelo Nominal', 'Modelo'],  # noqa
            'sku_metadata': ['Voltagem'],
            'metadata': {
                'Voltagem': '110 Volts',
                'Marca': 'Britânia',
                'Produto': 'Torradeira',
                'Modelo Nominal': 'Tosta Pane',
                'Cor': 'Vermelha',
                'Tipo': 'Elétrica',
                'Níveis de Tostagem': '7 Níveis de Tostagem'
            },
            'navigation_id': '7539762',
            'product_name': 'Torradeira Britânia Vermelha Tosta Pane 7 Níveis de Tostagem'  # noqa
        }

    @classmethod
    def magazineluiza_sku_217148200(cls):
        return {
            'metadata': {
                'Material': 'Metal Plástico',
                'Voltagem': '220 Volts',
                'Marca': 'Britânia',
                'Produto': 'Torradeira',
                'Tipo': 'Elétrica',
                'Níveis de Tostagem': '7 Níveis de Tostagem',
                'Modelo Nominal': 'Tosta Pane',
                'Cor': 'Vermelha'
            },
            'subcategory_ids': ['TOST'],
            'sku_metadata': ['Voltagem'],
            'category_id': 'EP',
            'product_hash': '0d9a74a782ae7f4141befd08915d2cab',
            'product_matching_metadata': ['Produto', 'Marca', 'Cor', 'Modelo Nominal', 'Modelo'],  # noqa
            'entity': 'Torradeira',
            'source': 'magalu',
            'product_name_metadata': ['Produto', 'Marca', 'Cor', 'Material', 'Linha', 'Modelo Nominal', 'Modelo', 'Fatias', 'Painel', 'Níveis de Tostagem'],  # noqa
            'sku': '217148200',
            'seller_id': 'magazineluiza',
            'navigation_id': '217148200',
            'product_name': 'Torradeira Britânia Vermelha Tosta Pane 7 Níveis de Tostagem',  # noqa
            'filters_metadata': ['Produto', 'Marca', 'Cor', 'Material', 'Linha', 'Modelo Nominal', 'Modelo', 'Fatias', 'Painel', 'Níveis de Tostagem', 'Voltagem', 'Tipo'],  # noqa
            'timestamp': 1531338196.2738166
        }

    @classmethod
    def madeiramadeira_openapi_sku_302110(cls):
        return {
            'timestamp': 1531339152.856294,
            'seller_id': 'madeiramadeira-openapi',
            'navigation_id': '5794086',
            'sku_metadata': ['Voltagem'],
            'source': 'magalu',
            'metadata': {
                'Cor': 'Vermelha',
                'Tipo': 'Elétrica',
                'Produto': 'Torradeira',
                'Voltagem': '110 Volts',
                'Modelo Nominal': 'Tosta Pane',
                'Níveis de Tostagem': '7 Níveis de Tostagem',
                'Marca': 'Britânia'
            },
            'product_name': 'Torradeira Britânia Vermelha Tosta Pane 7 Níveis de Tostagem',  # noqa
            'filters_metadata': ['Produto', 'Marca', 'Cor', 'Material', 'Linha', 'Modelo Nominal', 'Modelo', 'Fatias', 'Painel', 'Níveis de Tostagem', 'Voltagem', 'Tipo'],  # noqa
            'subcategory_ids': ['TOST'],
            'sku': '302110',
            'product_matching_metadata': ['Produto', 'Marca', 'Cor', 'Modelo Nominal', 'Modelo'],  # noqa
            'product_hash': '0d9a74a782ae7f4141befd08915d2cab',
            'category_id': 'EP',
            'product_name_metadata': ['Produto', 'Marca', 'Cor', 'Material', 'Linha', 'Modelo Nominal', 'Modelo', 'Fatias', 'Painel', 'Níveis de Tostagem'],  # noqa
            'entity': 'Torradeira'
        }

    @classmethod
    def madeiramadeira_openapi_sku_302117(cls):
        return {
            'subcategory_ids': ['TOST'],
            'product_name_metadata': ['Produto', 'Marca', 'Cor', 'Material', 'Linha', 'Modelo Nominal', 'Modelo', 'Fatias', 'Painel', 'Níveis de Tostagem'],  # noqa
            'metadata': {
                'Produto': 'Torradeira',
                'Marca': 'Britânia',
                'Níveis de Tostagem': '7 Níveis de Tostagem',
                'Modelo Nominal': 'Tosta Pane',
                'Tipo': 'Elétrica',
                'Cor': 'Vermelha',
                'Voltagem': '220 Volts'
            },
            'sku': '302117',
            'seller_id': 'madeiramadeira-openapi',
            'sku_metadata': ['Voltagem'],
            'navigation_id': '5914495',
            'product_matching_metadata': ['Produto', 'Marca', 'Cor', 'Modelo Nominal', 'Modelo'],  # noqa
            'product_name': 'Torradeira Britânia Vermelha Tosta Pane 7 Níveis de Tostagem',  # noqa
            'product_hash': '0d9a74a782ae7f4141befd08915d2cab',
            'source': 'magalu',
            'timestamp': 1531339172.597289,
            'category_id': 'EP',
            'entity': 'Torradeira',
            'filters_metadata': ['Produto', 'Marca', 'Cor', 'Material', 'Linha', 'Modelo Nominal', 'Modelo', 'Fatias', 'Painel', 'Níveis de Tostagem', 'Voltagem', 'Tipo']  # noqa
        }

    @classmethod
    def magazineluiza_sku_217148100(cls):
        return {
            'entity': 'Torradeira',
            'product_hash': '0d9a74a782ae7f4141befd08915d2cab',
            'product_matching_metadata': ['Produto', 'Marca', 'Cor', 'Modelo Nominal', 'Modelo'],  # noqa
            'metadata': {
                'Cor': 'Vermelha',
                'Modelo Nominal': 'Tosta Pane',
                'Tipo': 'Elétrica',
                'Material': 'Metal Plástico',
                'Voltagem': '110 Volts',
                'Produto': 'Torradeira',
                'Níveis de Tostagem': '7 Níveis de Tostagem',
                'Marca': 'Britânia'
            },
            'product_name_metadata': ['Produto', 'Marca', 'Cor', 'Material', 'Linha', 'Modelo Nominal', 'Modelo', 'Fatias', 'Painel', 'Níveis de Tostagem'],  # noqa
            'timestamp': 1531338194.264335,
            'subcategory_ids': ['TOST'],
            'sku_metadata': ['Voltagem'],
            'source': 'magalu',
            'seller_id': 'magazineluiza',
            'product_name': 'Torradeira Britânia Vermelha Tosta Pane 7 Níveis de Tostagem',  # noqa
            'sku': '217148100',
            'navigation_id': '217148100',
            'category_id': 'EP',
            'filters_metadata': ['Produto', 'Marca', 'Cor', 'Material', 'Linha', 'Modelo Nominal', 'Modelo', 'Fatias', 'Painel', 'Níveis de Tostagem', 'Voltagem', 'Tipo']  # noqa
        }

    @classmethod
    def havan_sku_2078836(cls):
        return {
            'seller_id': 'havan',
            'entity': 'Torradeira',
            'product_name_metadata': ['Produto', 'Marca', 'Cor', 'Material', 'Linha', 'Modelo Nominal', 'Modelo', 'Fatias', 'Painel', 'Níveis de Tostagem'],  # noqa
            'sku': '2078836',
            'filters_metadata': ['Produto', 'Marca', 'Cor', 'Material', 'Linha', 'Modelo Nominal', 'Modelo', 'Fatias', 'Painel', 'Níveis de Tostagem', 'Voltagem', 'Tipo'],  # noqa
            'subcategory_ids': ['TOST'],
            'product_matching_metadata': ['Produto', 'Marca', 'Cor', 'Modelo Nominal', 'Modelo'],  # noqa
            'metadata': {
                'Material': 'Metal Plástico',
                'Tipo': 'Elétrica',
                'Voltagem': '220 Volts',
                'Modelo Nominal': 'Tosta Pane',
                'Produto': 'Torradeira',
                'Níveis de Tostagem': '7 Níveis de Tostagem',
                'Cor': 'Vermelha',
                'Marca': 'Britânia'
            },
            'product_name': 'Torradeira Britânia Vermelha Tosta Pane 7 Níveis de Tostagem',  # noqa
            'sku_metadata': ['Voltagem'],
            'product_hash': '0d9a74a782ae7f4141befd08915d2cab',
            'timestamp': 1531339334.3052583,
            'navigation_id': '8355943',
            'source': 'magalu',
            'category_id': 'EP'
        }

    @classmethod
    def havan_sku_2078835(cls):
        return {
            'sku': '2078835',
            'navigation_id': '8283924',
            'sku_metadata': ['Voltagem'],
            'subcategory_ids': ['TOST'],
            'category_id': 'EP',
            'source': 'magalu',
            'seller_id': 'havan',
            'product_name': 'Torradeira Britânia Vermelha Tosta Pane 7 Níveis de Tostagem',  # noqa
            'product_matching_metadata': ['Produto', 'Marca', 'Cor', 'Modelo Nominal', 'Modelo'],  # noqa
            'entity': 'Torradeira',
            'filters_metadata': ['Produto', 'Marca', 'Cor', 'Material', 'Linha', 'Modelo Nominal', 'Modelo', 'Fatias', 'Painel', 'Níveis de Tostagem', 'Voltagem', 'Tipo'],  # noqa
            'product_hash': '0d9a74a782ae7f4141befd08915d2cab',
            'timestamp': 1531339253.576543,
            'metadata': {
                'Marca': 'Britânia',
                'Cor': 'Vermelha',
                'Tipo': 'Elétrica',
                'Produto': 'Torradeira',
                'Modelo Nominal': 'Tosta Pane',
                'Voltagem': '110 Volts',
                'Níveis de Tostagem': '7 Níveis de Tostagem',
                'Material': 'Metal Plástico'
            },
            'product_name_metadata': ['Produto', 'Marca', 'Cor', 'Material', 'Linha', 'Modelo Nominal', 'Modelo', 'Fatias', 'Painel', 'Níveis de Tostagem']  # noqa
        }

    @classmethod
    def mundoautomacao_sku_320_257(cls):
        return {
            'subcategory_ids': ['TOST'],
            'timestamp': 1531338233.794502,
            'sku': '320-257',
            'metadata': {
                'Tipo': 'Elétrica',
                'Produto': 'Torradeira',
                'Marca': 'Britânia',
                'Cor': 'Vermelha',
                'Voltagem': '110 Volts',
                'Modelo Nominal': 'Tosta Pane',
                'Níveis de Tostagem': '7 Níveis de Tostagem'
            },
            'seller_id': 'mundoautomacao',
            'entity': 'Torradeira',
            'sku_metadata': ['Voltagem'],
            'product_hash': '0d9a74a782ae7f4141befd08915d2cab',
            'filters_metadata': ['Produto', 'Marca', 'Cor', 'Material', 'Linha', 'Modelo Nominal', 'Modelo', 'Fatias', 'Painel', 'Níveis de Tostagem', 'Voltagem', 'Tipo'],  # noqa
            'product_matching_metadata': ['Produto', 'Marca', 'Cor', 'Modelo Nominal', 'Modelo'],  # noqa
            'product_name_metadata': ['Produto', 'Marca', 'Cor', 'Material', 'Linha', 'Modelo Nominal', 'Modelo', 'Fatias', 'Painel', 'Níveis de Tostagem'],  # noqa
            'source': 'magalu',
            'navigation_id': '6921135',
            'product_name': 'Torradeira Britânia Vermelha Tosta Pane 7 Níveis de Tostagem',  # noqa
            'category_id': 'EP'
        }

    @classmethod
    def mundoautomacao_sku_320_258(cls):
        return {
            'entity': 'Torradeira',
            'navigation_id': '6150755',
            'timestamp': 1531339228.59462,
            'product_hash': '0d9a74a782ae7f4141befd08915d2cab',
            'sku': '320-258',
            'filters_metadata': ['Produto', 'Marca', 'Cor', 'Material', 'Linha', 'Modelo Nominal', 'Modelo', 'Fatias', 'Painel', 'Níveis de Tostagem', 'Voltagem', 'Tipo'],  # noqa
            'subcategory_ids': ['TOST'],
            'seller_id': 'mundoautomacao',
            'product_name': 'Torradeira Britânia Vermelha Tosta Pane 7 Níveis de Tostagem',  # noqa
            'category_id': 'EP',
            'product_matching_metadata': ['Produto', 'Marca', 'Cor', 'Modelo Nominal', 'Modelo'],  # noqa
            'product_name_metadata': ['Produto', 'Marca', 'Cor', 'Material', 'Linha', 'Modelo Nominal', 'Modelo', 'Fatias', 'Painel', 'Níveis de Tostagem'],  # noqa
            'metadata': {
                'Marca': 'Britânia',
                'Tipo': 'Elétrica',
                'Cor': 'Vermelha',
                'Modelo Nominal': 'Tosta Pane',
                'Voltagem': '220 Volts',
                'Produto': 'Torradeira',
                'Níveis de Tostagem': '7 Níveis de Tostagem'
            },
            'source': 'magalu',
            'sku_metadata': ['Voltagem']
        }

    @classmethod
    def webfones_sku_14366(cls):
        return {
            'product_name_metadata': ['Produto', 'Tipo', 'Marca', 'Linha', 'Modelo Nominal', 'Modelo', 'Cor', 'Material', 'Capacidade', 'Recursos'],  # noqa
            'source': 'magalu',
            'timestamp': 1531858612.9370344,
            'category_id': 'EP',
            'sku': '14366',
            'metadata': {
                'Marca': 'Agratto',
                'Potência': '1200 W',
                'Modelo Nominal': 'Fryer',
                'Produto': 'Fritadeira Elétrica',
                'Modelo': 'AF-01',
                'Cor': 'Preta',
                'Voltagem': '110 Volts',
                'Tipo': 'Sem Óleo/Air Fryer',
                'Recursos': 'Timer'
            },
            'seller_id': 'webfones',
            'entity': 'Fritadeira Elétrica',
            'filters_metadata': ['Produto', 'Tipo', 'Marca', 'Linha', 'Modelo Nominal', 'Modelo', 'Cor', 'Material', 'Capacidade', 'Recursos', 'Voltagem', 'Potência'],  # noqa
            'navigation_id': '6225646',
            'sku_metadata': ['Voltagem'],
            'subcategory_ids': ['FREL'],
            'product_name': None,
            'product_matching_metadata': ['Produto', 'Marca', 'Modelo Nominal', 'Modelo', 'Cor', 'Capacidade'],  # noqa
            'product_hash': None
        }

    @classmethod
    def magazineluiza_sku_216131400(cls):
        return {
            'product_name': None,
            'subcategory_ids': [
                'MATQ',
                'IPMF'
            ],
            'product_hash': None,
            'filters_metadata': [
                'Produto',
                'Marca',
                'Linha',
                'Modelo',
                'Cor da Impressora',
                'Tecnologia de Impressão',
                'Voltagem',
                'Tipo'
            ],
            'source': 'magalu',
            'navigation_id': '216131400',
            'product_name_metadata': [
                'Produto',
                'Marca',
                'Linha',
                'Modelo',
                'Cor da Impressora',
                'Tecnologia de Impressão'
            ],
            'sku': '216131400',
            'entity': 'Impressora',
            'timestamp': 1535760562.7555583,
            'seller_id': 'magazineluiza',
            'sku_metadata': [
                'Voltagem'
            ],
            'product_matching_metadata': [
                'Produto',
                'Marca',
                'Modelo',
                'Cor da Impressora',
                'Tecnologia de Impressão'
            ],
            'category_id': 'IN',
            'metadata': {
                'Linha': 'EcoTank',
                'Cor da Impressora': 'Preta',
                'Voltagem': 'Bivolt',
                'Produto': 'Impressora Multifuncional',
                'Tecnologia de Impressão': 'Tanque de Tinta',
                'Marca': 'Epson',
                'Modelo': 'L575'
            }
        }

    @classmethod
    def magazineluiza_sku_193419700(cls):
        return {
            'product_name': None,
            'product_name_metadata': [],
            'metadata': {
                'Tipo de Tela': 'LED',
                'Marca': 'Philips',
                'Formato da Tela': 'Plana',
                'Tamanho da Tela': '32\'',
                'Resolução': 'HD',
                'Produto': 'TV',
                'Recursos': 'Smart'
            },
            'product_hash': None,
            'entity': 'TV',
            'navigation_id': '193419700',
            'seller_id': 'magazineluiza',
            'sku_metadata': [],
            'sku': '193419700',
            'category_id': 'ET',
            'timestamp': 1536862345.4680047,
            'filters_metadata': [
                'Produto',
                'Marca',
                'Linha',
                'Modelo',
                'Tamanho da Tela',
                'Tipo de Tela',
                'Formato da Tela',
                'Recursos',
                'Resolução',
                'Cor',
                'Tipo'
            ],
            'subcategory_ids': [
                'ELIT',
                'TLED'
            ],
            'product_matching_metadata': []
        }

    @classmethod
    def magazineluiza_sku_155536300_with_technical_specification(cls):
        return {
            'sku': '155536300',
            'entity': 'Celular',
            'metadata': {
                'Sistema Operacional': 'Android Nougat',
                'Quantidade de Chips': 'Dual Chip',
                'Tamanho da Tela': '5.5 polegadas',
                'Tecnologia': '4G,Bluetooth,WiFi',
                'Memória RAM': '3GB',
                'Marca': 'Motorola',
                'Cor': 'Platinum',
                'Resolução da Câmera Traseira': '13MP',
                'Capacidade da Memória': '32GB',
                'Produto': 'Smartphone'
            },
            'seller_id': 'magazineluiza',
            'navigation_id': '155536300',
            'category_id': 'TE',
            'subcategory_ids': [
                'TCSP',
                'SRMT',
                'MGSP'
            ],
            'product_matching_metadata': [

            ],
            'product_name_metadata': [

            ],
            'sku_metadata': [

            ],
            'navigation_filter': [
                'Produto',
                'Marca',
                'Capacidade da Memória',
                'Cor',
                'Quantidade de Chips',
                'Resolução da Câmera Traseira',
                'Memória RAM',
                'Tamanho da Tela',
                'Sistema Operacional'
            ],
            'technical_specification': [
                'Marca',
                'Capacidade da Memória',
                'Cor',
                'Quantidade de Chips',
                'Resolução da Câmera Traseira',
                'Memória RAM',
                'Tamanho da Tela',
                'Sistema Operacional'
            ]
        }

    @classmethod
    def lt2shop_sku_0000998113(cls):
        return {
            'seller_id': 'lt2shop',
            'navigation_id': 'bh8c1h748a',
            'description': 'Livro preparatório para o exame de entrada da certificação MCSA, que comprova o domínio das habilidades essenciais do Windows Server 2016 para reduzir custos de TI e agregar mais valor ao negócio. Os exames 70-741 (Redes com Windows Server 2016) e o Exame 70-742 (Identidade com Windows Server 2016) também são necessários para a obtenção do MCSA Windows Server 2016.',  # noqa
            'subtitle': 'Instalação, Armazenamento e Computação com Windows Server 2016',  # noqa
            'sku': '0000998113',
            'metadata': {
                'Autores': ['Zacker, Craig', 'Michel, Luciana Monteiro', 'Silva, Aldir José Coelho Corrêa da'],  # noqa
                'Idiomas do produto': ['Português'],
                'Número de páginas': 464,
                'Data de publicação': '06.04.2018',
                'Editora': ['Bookman'],
                'Edição': 1,
                'Tipo de produto': 'pbook'
            },
            'entity': 'Livro',
            'title': 'Exam Ref 70-740',
            'source': 'metabooks',
            'category_id': 'LI',
            'subcategory_ids': ['LLIN', 'LETR']
        }

    @classmethod
    def cliquebooks_sku_5752019(cls):
        return {
            'seller_id': 'cliquebooks',
            'navigation_id': 'jd3d3gdb9e',
            'description': '',
            'subtitle': 'Lidando com a lama, o buraco, o revés e a escassez',
            'sku': '5752019',
            'metadata': {
                'Autores': ['Zacker, Craig', 'Michel, Luciana Monteiro', 'Silva, Aldir José Coelho Corrêa da'],  # noqa
                'Idiomas do produto': ['Português'],
                'Número de páginas': 464,
                'Data de publicação': '06.04.2018',
                'Editora': ['Editora Rocco Ltda'],
                'Edição': 1,
                'Tipo de produto': 'pbook'
            },
            'title': 'Cabala e a arte de manutenção da carroça',
            'source': 'metabooks',
            'category_id': 'LI',
            'subcategory_ids': ['OTLI']
        }

    @classmethod
    def magazineluiza_sku_222764000(cls):
        return {
            'sku': '222764000',
            'entity': 'Livro',
            'metadata': {
                'Editora': 'Intrínseca',
                'ISBN-13': '9788551002490',
                'Autor': 'Manson, Mark, Faro, Joana',
                'ISBN-10': '855100249X',
                'Gênero': 'Autoajuda',
                'Edição': '1ª edição'
            },
            'seller_id': 'magazineluiza',
            'navigation_id': '222764000',
            'category_id': 'LI',
            'subcategory_ids': ['LIAJ'],
            'product_hash': 'c91b7af58441163e29bbadb1cdd52941',
            'product_name': 'A Sutil Arte de Ligar o F*da-se - Uma Estratégia Inusitada Para Uma Vida Melhor',  # noqa
            'product_matching_metadata': ['ISBN-10', 'ISBN-13'],
            'product_name_metadata': ['ISBN-10', 'ISBN-13'],
            'sku_metadata': [],
            'filters_metadata': ['ISBN-10', 'ISBN-13', 'Autor', 'Tipo de Edição', 'Volume', 'Editora', 'Edição', 'Gênero'],  # noqa
            'source': 'magalu',
            'timestamp': 1568316496.8427305
        }

    @classmethod
    def authenticlivros_sku_1073972(cls):
        return {
            'sku': '1073972',
            'entity': 'Livro',
            'metadata': {
                'Editora': '',
                'ISBN-13': '9788551002490',
                'Autor': 'Manson, Mark, Faro, Joana',
                'ISBN-10': '855100249X',
                'Gênero': 'Teoria e Crítica Literária',
                'Edição': '1ª edição'
            },
            'seller_id': 'authenticlivros',
            'navigation_id': 'egjbb8121d',
            'category_id': 'LI',
            'subcategory_ids': ['LLIT'],
            'product_hash': 'c91b7af58441163e29bbadb1cdd52941',
            'product_name': 'Sutil Arte de Ligar O F Da-se, A - Intrinseca - Editora intrinseca',  # noqa
            'product_matching_metadata': ['ISBN-10', 'ISBN-13'],
            'product_name_metadata': ['ISBN-10', 'ISBN-13'],
            'sku_metadata': [],
            'filters_metadata': ['ISBN-10', 'ISBN-13', 'Autor', 'Tipo de Edição', 'Volume', 'Editora', 'Edição', 'Gênero'],  # noqa
            'source': 'magalu',
            'timestamp': 1568316512.098712
        }

    @classmethod
    def meulivromegastore_sku_166271(cls):
        return {
            'sku': '166271',
            'entity': 'Livro',
            'metadata': {
                'Editora': 'Intrínseca',
                'ISBN-13': '9788551002490',
                'Autor': 'Manson, Mark, Faro, Joana',
                'ISBN-10': '855100249X',
                'Gênero': 'Teoria e Crítica Literária',
                'Edição': '1ª edição'
            },
            'seller_id': 'meulivromegastore',
            'navigation_id': 'dbkgh9k336',
            'category_id': 'LI',
            'subcategory_ids': ['LLIT'],
            'product_hash': 'c91b7af58441163e29bbadb1cdd52941',
            'product_name': 'Sutil Arte de Ligar O F Da-se, A - Intrinseca - Editora intrinseca',  # noqa
            'product_matching_metadata': ['ISBN-10', 'ISBN-13'],
            'product_name_metadata': ['ISBN-10', 'ISBN-13'],
            'sku_metadata': [],
            'filters_metadata': ['ISBN-10', 'ISBN-13', 'Autor', 'Tipo de Edição', 'Volume', 'Editora', 'Edição', 'Gênero'],  # noqa
            'source': 'magalu',
            'timestamp': 1568316512.098712
        }

    @classmethod
    def livrariaflorence2_sku_9788543105757(cls):
        return {
            'sku': '9788543105757',
            'entity': 'Livro',
            'metadata': {
                'Editora': 'GMT',
                'ISBN-13': '9788543105758',
                'Autor': 'Bessa, Bráulio, Passos, Elano',
                'ISBN-10': '8543105757',
                'Gênero': 'Teoria e Crítica Literária',
                'Edição': '1ª edição'
            },
            'seller_id': 'livrariaflorence2',
            'navigation_id': 'haadaa83f7',
            'category_id': 'LI',
            'subcategory_ids': ['LLIT'],
            'product_hash': '572a933e7834a6cea0a7d4a2b5f35e92',
            'product_name': 'Poesia que transforma - sextante - Gmt',
            'product_matching_metadata': ['ISBN-10', 'ISBN-13'],
            'product_name_metadata': ['ISBN-10', 'ISBN-13'],
            'sku_metadata': [],
            'filters_metadata': ['ISBN-10', 'ISBN-13', 'Autor', 'Tipo de Edição', 'Volume', 'Editora', 'Edição', 'Gênero'],  # noqa
            'source': 'magalu',
            'timestamp': 1568316038.306882
        }

    @classmethod
    def livrariasebocapricho_sku_23036521(cls):
        return {
            'sku': '23036521',
            'entity': 'Livro',
            'metadata': {
                'Editora': 'Sextante',
                'ISBN-13': '9788543105758',
                'Autor': 'Bessa, Bráulio, Passos, Elano',
                'ISBN-10': '8543105757',
                'Gênero': 'Poesia',
                'Edição': '1ª edição'
            },
            'seller_id': 'livrariasebocapricho',
            'navigation_id': 'dggf9f538g',
            'category_id': 'LI',
            'subcategory_ids': ['LVSP', 'LLIT'],
            'product_hash': '572a933e7834a6cea0a7d4a2b5f35e92',
            'product_name': 'Poesia que Transforma - Sextante',
            'product_matching_metadata': ['ISBN-10', 'ISBN-13'],
            'product_name_metadata': ['ISBN-10', 'ISBN-13'],
            'sku_metadata': [],
            'filters_metadata': ['ISBN-10', 'ISBN-13', 'Autor', 'Tipo de Edição', 'Volume', 'Editora', 'Edição', 'Gênero'],  # noqa
            'source': 'magalu',
            'timestamp': 1568316014.9833503
        }

    @classmethod
    def magazineluiza_sku_221841200(cls):
        return {
            'sku': '221841200',
            'entity': 'Livro',
            'metadata': {
                'Editora': 'Sextante',
                'ISBN-13': '9788543105758',
                'Autor': 'Bessa, Bráulio, Passos, Elano',
                'ISBN-10': '8543105757',
                'Gênero': 'Teoria e Crítica Literária',
                'Edição': '1ª edição'
            },
            'seller_id': 'magazineluiza',
            'navigation_id': '221841200',
            'category_id': 'LI',
            'subcategory_ids': ['LLIT'],
            'product_hash': '572a933e7834a6cea0a7d4a2b5f35e92',
            'product_name': 'Poesia que transforma',
            'product_matching_metadata': ['ISBN-10', 'ISBN-13'],
            'product_name_metadata': ['ISBN-10', 'ISBN-13'],
            'sku_metadata': [],
            'filters_metadata': ['ISBN-10', 'ISBN-13', 'Autor', 'Tipo de Edição', 'Volume', 'Editora', 'Edição', 'Gênero'],  # noqa
            'source': 'magalu',
            'timestamp': 1568316086.6736076
        }

    @classmethod
    def livrariaflorence2_sku_9788543105758(cls):
        return {
            'sku': '9788543105758',
            'entity': 'Livro',
            'metadata': {
                'Editora': 'Sextante',
                'ISBN-13': '9788543105758',
                'Autor': 'Bessa, Bráulio, Passos, Elano',
                'ISBN-10': '8543105757',
                'Gênero': 'Teoria e Crítica Literária',
                'Edição': '1ª edição'
            },
            'seller_id': 'livrariaflorence2',
            'navigation_id': 'ej01hd210g',
            'category_id': 'LI',
            'subcategory_ids': ['LLIT'],
            'product_hash': '572a933e7834a6cea0a7d4a2b5f35e92',
            'product_name': 'Livro - Poesia Que Transforma - Bessa - Sextante',
            'product_matching_metadata': ['ISBN-10', 'ISBN-13'],
            'product_name_metadata': ['ISBN-10', 'ISBN-13'],
            'sku_metadata': [],
            'filters_metadata': ['ISBN-10', 'ISBN-13', 'Autor', 'Tipo de Edição', 'Volume', 'Editora', 'Edição', 'Gênero'],  # noqa
            'source': 'magalu',
            'timestamp': 1568316060.5282717
        }

    @classmethod
    def saraiva_sku_10260263(cls):
        return {
            'sku': '10260263',
            'entity': 'Livro',
            'metadata': {
                'Editora': 'GMT',
                'ISBN-13': '9788543105758',
                'Autor': 'Bessa, Bráulio, Passos, Elano',
                'ISBN-10': '8543105757',
                'Gênero': 'Ficção',
                'Edição': '1ª edição'
            },
            'seller_id': 'saraiva',
            'navigation_id': 'cfjkh8c2hk',
            'category_id': 'LI',
            'subcategory_ids': ['LLIT'],
            'product_hash': '572a933e7834a6cea0a7d4a2b5f35e92',
            'product_name': 'Poesia Que Transforma - Sextante / gmt',
            'product_matching_metadata': ['ISBN-10', 'ISBN-13'],
            'product_name_metadata': ['ISBN-10', 'ISBN-13'],
            'sku_metadata': [],
            'filters_metadata': ['ISBN-10', 'ISBN-13', 'Autor', 'Tipo de Edição', 'Volume', 'Editora', 'Edição', 'Gênero'],  # noqa
            'source': 'magalu',
            'timestamp': 1568316075.1394293
        }

    @classmethod
    def cliquebooks_sku_543242_1(cls):
        return {
            'sku': '543242.1',
            'entity': 'Livro',
            'metadata': {
                'ISBN-13': '9788506082645',
                'ISBN-10': '8506082641',
                'Gênero': 'Infantil,Literatura Infantojuvenil'
            },
            'seller_id': 'cliquebooks',
            'navigation_id': '6453998',
            'category_id': 'LI',
            'subcategory_ids': ['LLJL'],
            'product_hash': '42d22aa9caa539496dbb5cd77a0a270b',
            'product_name': 'Viva - o poder da musica - Melhoramentos',
            'product_matching_metadata': ['ISBN-10', 'ISBN-13'],
            'product_name_metadata': ['ISBN-10', 'ISBN-13', 'Gênero'],
            'sku_metadata': [],
            'filters_metadata': ['ISBN-10', 'ISBN-13', 'Gênero', 'Autor', 'Tipo de Edição', 'Volume', 'Editora', 'Edição'],  # noqa
            'source': 'magalu',
            'timestamp': 1570044165.4530776
        }

    @classmethod
    def magazineluiza_sku_222786900(cls):
        return {
            'sku': '222786900',
            'entity': 'Livro',
            'metadata': {
                'ISBN-13': '9788506082645',
                'ISBN-10': '8506082641',
                'Gênero': 'Infantil,Literatura Infantojuvenil'
            },
            'seller_id': 'magazineluiza',
            'navigation_id': '222786900',
            'category_id': 'LI',
            'subcategory_ids': ['LLJL'],
            'product_hash': '42d22aa9caa539496dbb5cd77a0a270b',
            'product_name': 'O poder da música - Viva, A vida é uma festa',
            'product_matching_metadata': ['ISBN-10', 'ISBN-13'],
            'product_name_metadata': ['ISBN-10', 'ISBN-13', 'Gênero'],
            'sku_metadata': [],
            'filters_metadata': ['ISBN-10', 'ISBN-13', 'Gênero', 'Autor', 'Tipo de Edição', 'Volume', 'Editora', 'Edição'],  # noqa
            'source': 'magalu',
            'timestamp': 1570014809.2451077
        }

    @classmethod
    def book7_sku_9788506082645(cls):
        return {
            'sku': '9788506082645',
            'entity': 'Livro',
            'metadata': {
                'ISBN-13': '9788506082645',
                'ISBN-10': '8506082641',
                'Gênero': 'Infantil,Literatura Infantojuvenil'
            },
            'seller_id': 'book7',
            'navigation_id': 'chk0815383',
            'category_id': 'LI',
            'subcategory_ids': ['LLJL'],
            'product_hash': '42d22aa9caa539496dbb5cd77a0a270b',
            'product_name': 'O poder da música - Melhoramentos',
            'product_matching_metadata': ['ISBN-10', 'ISBN-13'],
            'product_name_metadata': ['ISBN-10', 'ISBN-13', 'Gênero'],
            'sku_metadata': [],
            'filters_metadata': ['ISBN-10', 'ISBN-13', 'Gênero', 'Autor', 'Tipo de Edição', 'Volume', 'Editora', 'Edição'],  # noqa
            'source': 'magalu',
            'timestamp': 1570014822.9667335
        }

    @classmethod
    def decorvida_sku_5489(cls):
        return {
            'sku': '5489',
            'entity': 'Mesa',
            'metadata': None,
            'seller_id': 'decorvida',
            'navigation_id': 'gj461cjeg6',
            'category_id': 'MO',
            'subcategory_ids': ['MSES'],
            'product_hash': None,
            'product_name': None,
            'product_matching_metadata': None,
            'product_name_metadata': None,
            'sku_metadata': None,
            'filters_metadata': None,
            'source': 'magalu',
            'timestamp': 1570555138.1955996
        }

    @classmethod
    def magazineluiza_sku_229221800(cls):
        return {
            'sku': '229221800',
            'seller_id': 'magazineluiza',
            'source': 'api_luiza_express_delivery',
            'delivery_days': 2
        }

    @classmethod
    def ifcat_sku_24ng0002xx(cls):
        return {
            'sku': '24NG0002XX',
            'entity': 'Brinquedo Educativo',
            'metadata': {
                'Idade Recomendada': [
                    '09 Anos',
                    '10 Anos',
                    'A Partir de 11 Anos'
                ],
                'Marca': 'Nig Brinquedos',
                'Gênero': 'Unissex'
            },
            'seller_id': 'ifcat',
            'navigation_id': 'hc5edecj5g',
            'category_id': 'BR',
            'subcategory_ids': [
                'JOMO',
                'BRIA',
                'BRIO',
                'B810',
                'BA11',
                'BPID'
            ],
            'product_hash': None,
            'product_name': None,
            'product_matching_metadata': [],
            'product_name_metadata': [],
            'sku_metadata': [],
            'filters_metadata': [
                'Marca',
                'Gênero',
                'Idade Recomendada',
                'Tema'
            ]
        }

    @classmethod
    def _1000store_sku_55316(cls):
        return {
            'sku': '55316',
            'entity': 'Livro',
            'metadata': {
                'ISBN-13': '9788542620719',
                'ISBN-10': '8542620712',
                'Gênero': 'HQs,Mangás e Graphic Novels,Graphic Novels,Super-heróis'  # noqa
            },
            'seller_id': '1000store',
            'navigation_id': 'dhjb75ck12',
            'category_id': 'LI',
            'subcategory_ids': ['HQLV'],
            'product_hash': 'c6656562539e82123f4622edabeccc98',
            'product_name': 'Batman renascimento 29 - Não informado',
            'product_matching_metadata': ['ISBN-10', 'ISBN-13'],
            'product_name_metadata': ['ISBN-10', 'ISBN-13', 'Gênero'],
            'sku_metadata': [],
            'filters_metadata': ['ISBN-10', 'ISBN-13', 'Gênero', 'Autor', 'Tipo de Edição', 'volume', 'Editora', 'Edição', 'subtitle'],  # noqa
            'source': 'magalu',
            'timestamp': 1585005251.664095
        }

    @classmethod
    def _1000store_sku_55313(cls):
        return {
            'sku': '55313',
            'entity': 'Livro',
            'metadata': {
                'ISBN-13': '9788542620719',
                'ISBN-10': '8542620712',
                'Gênero': 'HQs,Mangás e Graphic Novels,Graphic Novels,Super-heróis'  # noqa
            },
            'seller_id': '1000store',
            'navigation_id': 'bkc899e61c',
            'category_id': 'LI',
            'subcategory_ids': ['HQLV'],
            'product_hash': 'c6656562539e82123f4622edabeccc98',
            'product_name': 'Batman renascimento 29 - Não informado',
            'product_matching_metadata': ['ISBN-10', 'ISBN-13'],
            'product_name_metadata': ['ISBN-10', 'ISBN-13', 'Gênero'],
            'sku_metadata': [],
            'filters_metadata': ['ISBN-10', 'ISBN-13', 'Gênero', 'Autor', 'Tipo de Edição', 'volume', 'Editora', 'Edição', 'subtitle'],  # noqa
            'source': 'magalu',
            'timestamp': 1585005209.2161026
        }

    @classmethod
    def magazineluiza_sku_225300068(cls):
        return {
            'sku': '225300068',
            'entity': 'Livro',
            'metadata': {
                'ISBN-13': '9788542218640',
                'ISBN-10': '8542218647',
                'Gênero': 'Saúde e Família,Ciências Biológicas'
            },
            'seller_id': 'magazineluiza',
            'navigation_id': '225300068',
            'category_id': 'LI',
            'subcategory_ids': ['BEST'],
            'product_hash': 'c663bccfcc3119d3575be2f63de9e6c4',
            'product_name': 'Livro - A sinfonia da vida',
            'product_matching_metadata': ['ISBN-10', 'ISBN-13'],
            'product_name_metadata': ['ISBN-10', 'ISBN-13', 'Gênero'],
            'sku_metadata': [],
            'filters_metadata': ['ISBN-10', 'ISBN-13', 'Gênero', 'Autor', 'Tipo de Edição', 'Volume', 'Editora', 'Edição'],  # noqa
            'source': 'magalu',
            'timestamp': 1585664162.7325902
        }

    @classmethod
    def magazineluiza_sku_225620500(cls):
        return {
            'sku': '225620500',
            'entity': 'Livro',
            'metadata': {
                'ISBN-13': '9788542218640',
                'ISBN-10': '8542218647',
                'Gênero': 'Saúde e Família,Ciências Biológicas'
            },
            'seller_id': 'magazineluiza',
            'navigation_id': '225620500',
            'category_id': 'LI',
            'subcategory_ids': ['BEST'],
            'product_hash': 'c663bccfcc3119d3575be2f63de9e6c4',
            'product_name': 'Livro - A sinfonia da vida',
            'product_matching_metadata': ['ISBN-10', 'ISBN-13'],
            'product_name_metadata': ['ISBN-10', 'ISBN-13', 'Gênero'],
            'sku_metadata': [],
            'filters_metadata': ['ISBN-10', 'ISBN-13', 'Gênero', 'Autor', 'Tipo de Edição', 'Volume', 'Editora', 'Edição'],  # noqa
            'source': 'magalu',
            'timestamp': 1585815144.0681067
        }

    @classmethod
    def livrariabaluarte_sku_7576847209(cls):
        return {
            'sku': '7576847209',
            'entity': 'Livro',
            'metadata': {
                'ISBN-13': '9788542218800',
                'ISBN-10': '8542218809',
                'Gênero': 'Infantil,Religião e Espiritualidade'
            },
            'seller_id': 'livrariabaluarte',
            'navigation_id': 'ce9729d4k0',
            'category_id': 'LI',
            'subcategory_ids': ['LLTJ'],
            'product_hash': 'c663bccfcc3119d3575be2f63de9e6c4',
            'product_name': 'Livro - La casa de papel',
            'product_matching_metadata': ['ISBN-10', 'ISBN-13'],
            'product_name_metadata': ['ISBN-10', 'ISBN-13', 'Gênero'],
            'sku_metadata': [],
            'filters_metadata': ['ISBN-10', 'ISBN-13', 'Gênero', 'Autor', 'Tipo de Edição', 'Volume', 'Editora', 'Edição'],  # noqa
            'source': 'magalu',
            'timestamp': 1584109056.4441528
        }

    @classmethod
    def lojasages_sku_5973(cls):
        return {
            'sku': '5973',
            'entity': 'Barbeador',
            'metadata': {
                'Modelo': 'Prestobarba 3',
                'Marca': 'Gillette'
            },
            'seller_id': 'lojasages',
            'navigation_id': 'kh18566g08',
            'category_id': 'ME',
            'subcategory_ids': [
                'APDB',
                'PRHP',
                'PRHI'
            ],
            'product_hash': None,
            'product_name': None,
            'sku_hash': None,
            'sku_name': None,
            'product_matching_metadata': [
                'Marca',
                'Modelo'
            ],
            'product_name_metadata': [
                'Marca',
                'Modelo',
                'Linha',
                'Quantidade de Lâminas'
            ],
            'sku_metadata': [
                'Quantidade'
            ],
            'filters_metadata': [
                'Marca',
                'Modelo',
                'Linha',
                'Quantidade de Lâminas',
                'Quantidade'
            ],
            'source': 'magalu',
            'timestamp': 1596748734.7921245,
            'md5': '6d6b1edc45f1da9bd4b6067d2f469bcc'
        }

    @classmethod
    def ateliefestaemagia_sku_4795_251(cls):
        return {
            'sku': '4795-251',
            'entity': 'Kit Decoração de Festa',
            'metadata': {
                'Tema': 'Moana',
                'Cor': 'Azul',
                'Personagem': 'Moana',
                'Evento': 'Aniversário'
            },
            'seller_id': 'ateliefestaemagia',
            'navigation_id': 'ebkbbch779',
            'category_id': 'AF',
            'subcategory_ids': ['KDDF', 'DFES'],
            'product_hash': None,
            'product_name': None,
            'sku_hash': None,
            'sku_name': None,
            'product_matching_metadata': [],
            'product_name_metadata': [],
            'sku_metadata': [],
            'filters_metadata': ['Marca', 'Cor', 'Tema', 'Personagem', 'Evento'],  # noqa
            'source': 'magalu',
            'timestamp': 1600396648.9844856,
            'md5': '6924b52241058bdb456738e0d3cb0df0'
        }

    @classmethod
    def magazineluiza_230382400(cls):
        return [
            {
                'sku': '230382400',
                'seller_id': 'magazineluiza',
                'navigation_id': '230382400',
                'metadata': {
                    'Editora': 'Principis',
                    'Edição': '1ª edição',
                    'Autor': 'de Queirós, Eça',
                    'Data de publicação': '17.03.2021',
                    'Tipo de produto': 'pbook',
                    'Número de páginas': '1008',
                    'Idiomas do produto': 'Português, Português'
                },
                'title': 'Eça de Queirós',
                'subtitle': None,
                'description': 'Obras de Eça de Queirós, um dos maiores escritores portugueses mais importantes da literatura: O primo Basílio, O crime do padre Amaro e A relíquia.', # noqa
                'source': 'metabooks',
                'entity': 'Livro',
                'category_id': 'LI',
                'subcategory_ids': [
                    'LLIT'
                ]
            },
            {
                'seller_id': 'magazineluiza',
                'sku': '230382400',
                'navigation_id': '230382400',
                'metadata': {
                    'Editora': 'Principis',
                    'Edição': '1ª edição',
                    'Autor': 'de Queirós, Eça',
                    'Data de publicação': '17.03.2021',
                    'Tipo de produto': 'pbook',
                    'Número de páginas': '1008',
                    'Idiomas do produto': 'Português, Português'
                },
                'title': 'Eça de Queirós',
                'description': 'O box Eça de Queirós Vol. 1, publicado pela Editora Principis, conta com 3 importantes livros clássicos da literatura. As obras de Eça de Queirós, um dos maiores escritores portugueses e mais importantes da literatura estão reunidas nesse box: O primo Basílio, O crime do padre Amaro e A relíquia. O Primo Basílio é uma das obras mais emblemáticas do escritor realista português Eça de Queirós. Publicada em 1878, o romance é um retrato fiel da sociedade portuguesa da época. Publicado pela primeira vez em 1875, O Crime do Padre Amaro denuncia a corrupção dos padres, que manipulam a população em favor da elite, e a questão do celibato clerical. É com esse livro que Eça de Queirós inaugura, na prosa, a estética do realismo-naturalismo em Portugal. A relíquia é uma obra que associa à narrativa de viagem um olhar bem-humorado sobre a condição da adaptação humana, em seus interesses de posse e em suas ilusões sociais e afetivas.', # noqa
                'source': 'smartcontent',
                'entity': 'Livro',
                'brand': 'Principis'
            }
        ]

    @classmethod
    def magazineluiza_hector_230382400(cls):
        return {
            'sku': '230382400',
            'seller_id': 'magazineluiza',
            'navigation_id': '230382400',
            'classifications': [
                {
                    'product_type': 'Livro',
                    'category_id': 'LI',
                    'subcategories': ['LLIT'],
                    'channel': 'magazineluiza'
                }
            ],
            'source': 'hector'
        }

    @classmethod
    def magazineluiza_sku_0233847_datasheet(cls):
        return {
            'sku': '023384700',
            'seller_id': 'magazineluiza',
            'navigation_id': '023384700',
            'identifier': '7899882302516',
            'source': 'datasheet',
            'metadata': {
                'Voltagem': '220 volts'
            },
            'title': 'Fritadeira Elétrica Air Fryer/Sem Óleo Mondial - 110 volts',  # noqa
            'description': 'O que era inimaginável agora é real. Fritar comidas sem óleo.',  # noqa
            'entity': 'Freezer',
            'brand': 'Mondial'
        }

    @classmethod
    def generic_content_sku_fd3e322aab(cls):
        return {
            'sku': 'fd3e322aab',
            'seller_id': 'luizalabs',
            'navigation_id': 'abcdefgh',
            'metadata': {
                'code_anatel': 'HHHHH-AA-FFFFF'
            },
            'active': True,
            'source': SOURCE_GENERIC_CONTENT,
            'timestamp': 1711390785.9739926,
            'md5': '883164e7327cac524a54fef7a69b4eba'
        }

    @classmethod
    def shoploko_sku_74471_generic_content(cls):
        return {
            'seller_id': 'shoploko',
            'navigation_id': '6242299',
            'sku': '74471',
            'metadata': {
                'code_anatel': 'HHHHH-AA-FFFFF'
            },
            'active': True,
            'source': SOURCE_GENERIC_CONTENT
        }

    @classmethod
    def magazineluiza_sku_213445900_reclassification_price_rule(cls):
        return {
            'seller_id': 'magazineluiza',
            'sku': '213445900',
            'navigation_id': '213445900',
            'price': 0.01,
            'rule_id': 'id of classifications_rules',
            'from': {
                'product_type': 'Refrigerador',
                'category_id': 'ED',
                'subcategories': ['REFR'],
                'source': 'magalu'
            },
            'category_id': 'ED',
            'subcategory_ids': ['FAPG', 'REFR', 'ACRF'],
            'product_type': 'Peças para Refrigerador',
            'source': SOURCE_RECLASSIFICATION_PRICE_RULE
        }
