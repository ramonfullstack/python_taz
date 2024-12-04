import pytest

from taz.consumers.stock.helpers import get_availability, get_type


class TestGetType:

    @pytest.mark.parametrize('value, excepted', [
        ('distribution center', 'DC'),
        ('store', 'STORE'),
        ('other', 'OTHER'),
    ])
    def test_shoud_return_type_for_value(self, value, excepted):
        resp = get_type(value)
        assert resp == excepted

    def test_should_return_value_error_for_invalid_value(self):
        with pytest.raises(ValueError) as e:
            get_type('murcho')

        assert e.value.args[0] == 'Invalid value'


class TestGetAvailabilty:

    @pytest.mark.parametrize('value, excepted', [
        (300, 'nationwide'),
        (995, 'regional'),
        ('300', 'nationwide'),
    ])
    def test_should_return_availability_for_branch_id(self, value, excepted):
        resp = get_availability(value)

        assert resp == excepted
