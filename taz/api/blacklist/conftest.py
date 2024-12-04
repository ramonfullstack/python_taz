import pytest


@pytest.fixture
def blacklist_dict():
    return {'term': 'apple', 'field': 'brand'}
