from unittest import mock

import pytest

from taz.pollers.lu_content.converter import LuContentConverter


class TestLuContentConverter:

    @pytest.fixture
    def mock_cursor(self):
        cursor = mock.Mock()
        cursor.fetchall.return_value = ''
        return cursor

    @pytest.fixture
    def mock_data_source(self, mock_cursor):
        data_source = mock.Mock()
        data_source.fetch_details.return_value = mock_cursor
        return data_source

    @pytest.fixture
    def converter(self, mock_data_source):
        return LuContentConverter(mock_data_source)

    @pytest.fixture
    def database_row(self):
        return [{
            'batch_key': '776',
            'caption': 'Ar Continental',
            'category_values': 'ELKA;BB;BBFP|ELKA;BB;BBRO|ELKA;BB;BECH|ELKA;BB;BEHS|ELKA;BB;BETG|ELKA;BB;BETR|ELKA;BB;BRBB|ELKA;BB;MPBO|ELKA;BB;MRDE|ELKA;BB;OTBB|ELKA;BR;BA35|ELKA;BR;BAYY|ELKA;BR;BB12|ELKA;BR;BBPB|ELKA;BR;BCRB|ELKA;BR;BEBE|ELKA;BR;BJDT|ELKA;BR;BLCN|ELKA;BR;BLMO|ELKA;BR;BNCA|ELKA;BR;BNCO|ELKA;BR;BPPG|ELKA;BR;BRAS|ELKA;BR;BRBA|ELKA;BR;BRBL|ELKA;BR;BRBT|ELKA;BR;BRFR|ELKA;BR;BRIA|ELKA;BR;BRIN|ELKA;BR;BRMU|ELKA;BR;BSWS|ELKA;BR;CAON|ELKA;BR;CHCA|ELKA;BR;CORE|ELKA;BR;JOGO|ELKA;BR;JOMO|ELKA;BR;KMIN|ELKA;BR;LADA|ELKA;BR;NOCO|ELKA;BR;OUJG|ELKA;BR;PLSE|ELKA;BR;QUCB|ELKA;TM;TEMP',  # noqa
            'classification': 1,
            'contentTypeId': 2,
            'createdAt': 1592500773,
            'display_sessions': 'HOMESUBDEPTORODAPE',
            'hasPodcast': False,
            'id': 77633,
            'image': '77633.gif',
            'productBrand': 'Continental',
            'productCategory': 'ED',
            'productCode': '0112891',
            'productDescription': 'Depurador de Ar Continental 60cm 4 Bocas',
            'productReference': '3 Velocidades DC60B',
            'productSubSategory': 'DEPU',
            'sku': '7763300',
            'source': '',
            'status': 2,
            'subtitle': '60cm 4 Bocas',
            'title': 'Depurador de',
            'videoUrl': 'https://www.youtube.com/v/DcCQK_Jvf-g?hl=pt&'
        }]

    def test_database_convertion(
        self,
        converter,
        database_row
    ):
        expected_transformed_set = {
            '776': {
                '7763300': {
                    'id': 77633,
                    'image': 'https://c.mlcdn.com.br/{w}x{h}/portaldalu/fotosconteudo/77633.gif',  # noqa
                    'title': 'Depurador de',
                    'subtitle': '60cm 4 Bocas',
                    'caption': 'Ar Continental',
                    'content_type_id': 2,
                    'classification': 1,
                    'product': {
                        'id': '0112891',
                        'category': 'ED',
                        'subcategory': 'DEPU',
                        'title': 'Depurador de Ar Continental 60cm 4 Bocas',
                        'reference': '3 Velocidades DC60B',
                        'webvideo': 'https://www.youtube.com/v/DcCQK_Jvf-g?hl=pt&',  # noqa
                        'brand': 'Continental'
                    },
                    'category_values': ['ELKA', 'BB', 'BBFP', 'ELKA', 'BB', 'BBRO', 'ELKA', 'BB', 'BECH', 'ELKA', 'BB', 'BEHS', 'ELKA', 'BB', 'BETG', 'ELKA', 'BB', 'BETR', 'ELKA', 'BB', 'BRBB', 'ELKA', 'BB', 'MPBO', 'ELKA', 'BB', 'MRDE', 'ELKA', 'BB', 'OTBB', 'ELKA', 'BR', 'BA35', 'ELKA', 'BR', 'BAYY', 'ELKA', 'BR', 'BB12', 'ELKA', 'BR', 'BBPB', 'ELKA', 'BR', 'BCRB', 'ELKA', 'BR', 'BEBE', 'ELKA', 'BR', 'BJDT', 'ELKA', 'BR', 'BLCN', 'ELKA', 'BR', 'BLMO', 'ELKA', 'BR', 'BNCA', 'ELKA', 'BR', 'BNCO', 'ELKA', 'BR', 'BPPG', 'ELKA', 'BR', 'BRAS', 'ELKA', 'BR', 'BRBA', 'ELKA', 'BR', 'BRBL', 'ELKA', 'BR', 'BRBT', 'ELKA', 'BR', 'BRFR', 'ELKA', 'BR', 'BRIA', 'ELKA', 'BR', 'BRIN', 'ELKA', 'BR', 'BRMU', 'ELKA', 'BR', 'BSWS', 'ELKA', 'BR', 'CAON', 'ELKA', 'BR', 'CHCA', 'ELKA', 'BR', 'CORE', 'ELKA', 'BR', 'JOGO', 'ELKA', 'BR', 'JOMO', 'ELKA', 'BR', 'KMIN', 'ELKA', 'BR', 'LADA', 'ELKA', 'BR', 'NOCO', 'ELKA', 'BR', 'OUJG', 'ELKA', 'BR', 'PLSE', 'ELKA', 'BR', 'QUCB', 'ELKA', 'TM', 'TEMP'],  # noqa
                    'display': ['HOMESUBDEPTORODAPE'],
                    'content': ''
                }
            }
        }

        converter.from_source(database_row)

        assert expected_transformed_set == converter.get_items()
