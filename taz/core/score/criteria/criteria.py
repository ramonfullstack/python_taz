import importlib

from simple_settings import settings

from taz.consumers.core.database.mongodb import MongodbMixin


class ScoreCriteria(MongodbMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.score_criterias = self.get_collection('score_criterias')

    def get(self, entity_name, criteria_name, value):
        entity = self._get_entity(entity_name)

        for element in entity['elements']:
            if element['name'] != criteria_name:
                continue

            _type = self._get_type(element['type'])
            points, name = _type.get(element, value)
            return points, '{}::{}'.format(element['name'], name)

        return 0, None

    def _get_type(self, type_name):
        type_name = settings.SCORE_CRITERIA_TYPES[type_name]
        return importlib.import_module(type_name)

    def _get_entity(self, entity_name):
        default = self.score_criterias.find_one(
            {
                'entity_name': 'default',
                'score_version': settings.SCORE_VERSION
            },
            {'_id': 0}

        )
        entity = self.score_criterias.find_one(
            {
                'entity_name': entity_name.lower(),
                'score_version': settings.SCORE_VERSION
            },
            {'_id': 0}
        )

        if entity:
            element_names = [element['name'] for element in entity['elements']]

            elements = [
                element
                for element in default['elements']
                if element['name'] not in element_names
            ]

            default = {
                'entity_name': entity_name,
                'elements': elements + entity['elements']
            }

        return default
