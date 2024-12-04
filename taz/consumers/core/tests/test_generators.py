from unittest.mock import patch

import pytest
from simple_settings import settings
from simple_settings.utils import settings_stub

from taz.consumers.core.exceptions import MaxRetriesException
from taz.consumers.core.generators import IdGenerator, id_generator


class TestProductVariationIdGenerator:

    def test_generate_an_id(self):
        generated_id = id_generator.generate_id()
        assert isinstance(generated_id, str)

    def test_generator_using_configurable_length(self):
        expected_len = 5
        with settings_stub(**{'ID_LENGTH': expected_len}):
            generated_id = id_generator.generate_id()
        assert len(generated_id) == expected_len

    def test_generate_an_id_without_backlist_characteres(self):
        generated_id = id_generator.generate_id()
        for blacklist_character in settings.BLACKLIST_CHARACTERS:
            assert blacklist_character not in generated_id

    @settings_stub(ID_GENERATOR_RETRIES=0)
    def test_generation_loop_raises_error_when_hits_limit(self):
        with pytest.raises(MaxRetriesException):
            id_generator.generate_id()

    def test_generate_check_for_an_uniq_id(self):
        with patch.object(id_generator, 'is_uniq') as mock:
            mock.side_effect = (False, False, True)
            generated_id = id_generator.generate_id()
        assert isinstance(generated_id, str)
        assert mock.call_count == 3

    def test_generate_find_for_uniq_id_in_mongo_collection(self):
        fake_acme_id = '12345678'
        good_acme_id = '98765432'

        id_generator.collection.insert_one({'id': fake_acme_id})
        with patch.object(id_generator, '_random_id') as mock:
            mock.side_effect = (fake_acme_id, good_acme_id)
            generated_id = id_generator.generate_id()

        assert generated_id != fake_acme_id
        assert mock.call_count == 2

    def test_generate_save_id_in_database(self):
        generated_id = id_generator.generate_id()
        document = id_generator.collection.find_one({'id': generated_id})
        assert document

    def test_generate_id_only_with_digits(self):
        with settings_stub(ONLY_DIGITS_ID_GENERATOR=True):
            generated_id = IdGenerator().generate_id()
        assert generated_id.isdigit()

    def test_generate_id_with_prefix(self):
        with settings_stub(**{'ID_PREFIX': ('666',)}):
            generated_id = id_generator.generate_id()
        assert generated_id.startswith('666')

    def test_generate_id_with_prefix_and_repect_id_length(self):
        with settings_stub(**{'ID_PREFIX': ('666',), 'ID_LENGTH': 4}):
            generated_id = id_generator.generate_id()
        assert generated_id.startswith('666')
        assert len(generated_id) == 4
