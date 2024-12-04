from datetime import datetime
from decimal import Decimal
from uuid import uuid4

import pytest
from bson import ObjectId

from taz.api.common.json import custom_json_encoder


class TestCustomJsonEncoder:

    def test_encoder_from_decimal_to_string(self):
        encoded = custom_json_encoder(Decimal(1.23))

        assert encoded
        assert isinstance(encoded, str)
        assert encoded == '1.23'

    def test_encoder_from_uuid_to_string(self):
        uuid = uuid4()
        encoded = custom_json_encoder(uuid)

        assert encoded
        assert isinstance(encoded, str)
        assert encoded == str(uuid)

    def test_encoder_from_datetime_to_string(self):
        date = datetime.now()
        encoded = custom_json_encoder(date)

        assert encoded
        assert isinstance(encoded, str)
        assert encoded == date.isoformat()

    def test_encoder_from_object_id_to_string(self):
        object_id = ObjectId()
        encoded = custom_json_encoder(object_id)

        assert encoded
        assert isinstance(encoded, str)
        assert encoded == str(object_id)

    def test_encoder_should_return_type_error(self):
        with pytest.raises(TypeError):
            assert custom_json_encoder(None)
