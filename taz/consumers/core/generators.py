import random
import string

from pymongo import MongoClient
from simple_settings import settings

from .exceptions import MaxRetriesException


def _get_valid_characteres():
    characteres = string.digits
    if not settings.ONLY_DIGITS_ID_GENERATOR:
        characteres += string.ascii_lowercase
    return [x for x in characteres if x not in settings.BLACKLIST_CHARACTERS]


class IdGenerator:

    def __init__(self):
        self.conn = MongoClient(settings.MONGO_URI)
        self.database = getattr(self.conn, settings.MONGO_DATABASE)
        self.collection = self.database.items_ids

    @property
    def valid_characteres(self):
        if not hasattr(self, '_valid_characteres'):
            self._valid_characteres = _get_valid_characteres()
        return self._valid_characteres

    def insert_id(self, _id):
        self.collection.insert_one({'id': _id})

    def generate_id(self):
        generated_id = None

        prefix = settings.ID_PREFIX
        length = settings.ID_LENGTH

        for _ in range(settings.ID_GENERATOR_RETRIES):
            temp_id = self._random_id(length, prefix)
            if self.is_uniq(temp_id):
                generated_id = temp_id
                break

        if not generated_id:
            raise MaxRetriesException()

        self.insert_id(generated_id)

        return generated_id

    def _random_id(self, length, id_prefix=None):
        prefix = ''
        if id_prefix:
            prefix = random.choice(id_prefix)

        random_id = ''.join([
            random.choice(self.valid_characteres)
            for _ in range(length - len(prefix))
        ])

        return '{}{}'.format(prefix, random_id)

    def is_uniq(self, generated_id):
        return not self.collection.find_one({'id': generated_id})


id_generator = IdGenerator()
