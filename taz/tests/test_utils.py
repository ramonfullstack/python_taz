from datetime import datetime

import pytest

from taz import utils


class TestUtils:
    def test_date_to_timestamp_precision(self):
        now = datetime.now()
        timestamp = utils.date_to_timestamp(now)
        expected_date = datetime.fromtimestamp(timestamp)

        assert isinstance(timestamp, int)
        assert expected_date.year == now.year
        assert expected_date.month == now.month
        assert expected_date.day == now.day
        assert expected_date.hour == now.hour
        assert expected_date.minute == now.minute
        assert expected_date.second == now.second

    def test_invalid_date_to_timestamp(self):
        with pytest.raises(ValueError):
            utils.date_to_timestamp('111')

    @pytest.mark.parametrize('text,expected_result', [
        ('Poppy O\u0019 Hair - Mattel', 'Poppy O Hair - Mattel'),
        ('teste \\', 'teste ')
    ])
    def test_clean_invalid_characteres(self, text, expected_result):
        assert utils.clean_invalid_characters(text) == expected_result

    @pytest.mark.parametrize('builder', [list, tuple])
    @pytest.mark.parametrize('text,expected_result', [
        ('Poppy O\u0019 Hair - Mattel', 'Poppy O Hair - Mattel'),
        (
            'Filtro de ar Master - <Hengst E492L - Hengst',
            'Filtro de ar Master - Hengst E492L - Hengst'
        )
    ])
    def test_clean_invalid_characteres_in_sequence(
        self, text, expected_result, builder
    ):
        sequence = builder([text for _ in range(3)] + [1])
        expected_sequence = [expected_result for _ in range(3)] + [1]
        cleaned = utils.clean_invalid_characters_from_sequence(sequence)
        assert cleaned == expected_sequence

    def test_spaceless_str(self):
        assert utils.spaceless(' test ') == 'test'

    def test_spaceless_int(self):
        assert utils.spaceless(1) == 1

    def test_clean_invalid_characteres_in_sequence_dict(
        self
    ):
        sequence = {'test': 'a'}
        expected_sequence = ['test']
        cleaned = utils.clean_invalid_characters_from_sequence(sequence)
        assert cleaned == expected_sequence

    @pytest.mark.parametrize('text,expected_result', [
        ('Poppy O\u0019 Hair - Mattel', 'Poppy O Hair - Mattel')
    ])
    def test_clean_invalid_characteres_in_dict(
        self, text, expected_result
    ):
        expected_dict = {
            'foo': expected_result,
            'bar': [expected_result, expected_result],
            'nested': {'level1': expected_result}
        }
        d = {'foo': text, 'bar': [text, text], 'nested': {'level1': text}}
        cleaned = utils.clean_invalid_characters_from_dict(d)
        assert cleaned == expected_dict

    @pytest.mark.parametrize('text,expected_result', [
        ('9788573263282', True),
        ('37896007513315', True),
    ])
    def test_valid_ean(self, text, expected_result):
        validating_ean = utils.valid_ean(text)
        assert validating_ean == expected_result

    def test_valid_ean_with_wrong_ean(self):
        validating_ean = utils.valid_ean('123456789')
        assert validating_ean is False

    def test_valid_ean_without_ean(self):
        validating_ean = utils.valid_ean(None)
        assert validating_ean is False


class TestSortNicely:

    @pytest.fixture
    def data_dict(self):
        return ['125ml', '200ml', '75ml', '5ml']

    @pytest.fixture
    def expected(self):
        return ['5ml', '75ml', '125ml', '200ml']

    def test_sort_nicely(self, data_dict, expected):
        response = utils.sort_nicely(data_dict)
        assert response == expected


class TestUtilMd5:

    @pytest.fixture
    def payload(self):
        return {
            'title': 'murcho',
            'reference': 'murchão',
            'updated_at': '2017-09-22',
            'timestamp': 00000000000
        }

    @pytest.fixture
    def excepted(self):
        return 'b4330876986bd95d83c2393c44144dcd'

    def test_md5(self, payload, excepted):
        response = utils.md5(payload)
        assert response == excepted

    def test_md5_missing_updated_at(self, payload, excepted):
        del payload['updated_at']
        response = utils.md5(payload)
        assert response == excepted


class TestCutProductId:
    @pytest.mark.parametrize('value, excepted', [
        ('1234567', '1234567'),
        ('123456789', '1234567'),
        ('ABCDEF12345', 'ABCDEF12345'),
        ('ABCD', 'ABCD'),
    ])
    def test_cut_product_id(self, value, excepted):
        payload = utils.cut_product_id(value)
        assert payload == excepted


class TestConvertIdToNineDigits:

    @pytest.mark.parametrize('value, excepted', [
        ('1234567', '123456700'),
        ('ABCDEF12345', 'ABCDEF12345'),
        ('ABCD', 'ABCD'),
    ])
    def test_convert_id_to_nine_digits(self, value, excepted):
        payload = utils.convert_id_to_nine_digits(value)
        assert payload == excepted


class TestGetIdentifier:

    def test_when_product_contains_isbn_then_return_isbn(self):
        assert utils.get_identifier({'isbn': 'fake_isbn'}) == 'fake_isbn'

    def test_when_product_contains_isbn_and_ean_then_return_isbn(self):
        assert utils.get_identifier(
            {'isbn': 'fake_isbn', 'ean': 'fake_ean'}
        ) == 'fake_isbn'

    def test_when_product_not_contains_isbn_then_return_ean(self):
        assert utils.get_identifier({'ean': 'fake_ean'}) == 'fake_ean'


class TestGenerateUUID:

    def test_when_generate_uuid_then_return_uuid_as_string(
        self,
        patch_generate_uuid,
        mock_uuid
    ):
        with patch_generate_uuid:
            assert utils.generate_uuid() == str(mock_uuid)
