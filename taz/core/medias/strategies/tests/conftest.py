import pytest


@pytest.fixture
def mock_fake_bucket_name() -> str:
    return 'fake'


@pytest.fixture
def mock_image_internet_url() -> str:
    return 'https://files-product.magalu.com/6425a28b8bf6f1e9b622352b.jpeg'


@pytest.fixture
def mock_image_data() -> bytes:
    return b'image'


@pytest.fixture
def mock_bucket_img_internal_url(mock_fake_bucket_name: str) -> str:
    return f'https://{mock_fake_bucket_name}.googleapis.com/21/213445900.jpg'
