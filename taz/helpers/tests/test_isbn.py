import pytest

from taz.helpers.isbn import validate_isbn


class TestValidateIsbn:

    @pytest.mark.parametrize('value, expected', [
        (None, False),
        ('', False),
        ('1234567890', False),
        ('7898166657366', False),
        ('9786610326266', True),
        ('9788542615524', True),
    ])
    def test_validate_isbn(self, value, expected):
        assert validate_isbn(value) == expected
