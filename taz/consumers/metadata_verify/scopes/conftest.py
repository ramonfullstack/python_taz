from unittest.mock import patch

import pytest

from taz.consumers.metadata_verify.scopes.base import BaseScope


@pytest.fixture
def patch_data_storage():
    return patch.object(BaseScope, 'data_storage')


@pytest.fixture
def patch_image_storage():
    return patch.object(BaseScope, 'image_storage')
