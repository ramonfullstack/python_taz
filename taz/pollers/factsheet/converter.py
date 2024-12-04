import logging
import re
from enum import Enum

from slugify import slugify

from taz.constants import MAGAZINE_LUIZA_SELLER_ID
from taz.pollers.core.data.converter import BaseConverter
from taz.pollers.core.exceptions import DatabaseException

logger = logging.getLogger(__name__)


class GroupType(Enum):
    tab = 1
    group = 2
    attribute = 3


class FactsheetConverter(BaseConverter):

    REGEX_HTML = re.compile('<[^<]+?>')

    def __init__(self, data_source):
        super().__init__()
        self.data_source = data_source

    def _add_item(self, raw):
        try:
            cursor = self.data_source.fetch_details(
                raw['factsheet_id'],
                raw['product_id']
            )
            factsheet_rows = cursor.fetchall()

        except Exception as e:
            raise DatabaseException(
                'Error fetching details from factsheet {sku}: {msg}'.format(
                    sku=raw['sku'],
                    msg=str(e)
                )
            )

        grouped_factsheet = {}

        for factsheet_row in factsheet_rows:
            parent_id = factsheet_row['parent_id'] or 0
            grouped_factsheet.setdefault(parent_id, []).append(
                factsheet_row
            )

        result = {
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'sku': raw['sku'],
            'items': self._build_factsheet_payload(grouped_factsheet)
        }

        self.items.setdefault(raw['batch_key'], {}).update(
            {result['sku']: result}
        )

    def _build_factsheet_payload(self, items):
        result = []
        root_nodes = items.get(0) or []
        for root_node in root_nodes:
            elements = self._get_nodes_from(items, root_node['element_id'])
            if elements:
                tab = self._create_tab(root_node, elements)
                result.append(tab)

        return result

    def _get_nodes_from(self, items, element_id):
        result = []
        nodes = items.get(element_id) or []
        for node in nodes:
            elements = self._get_nodes_from(items, node['element_id'])

            group_type = GroupType(
                node.get('group_id') or GroupType.attribute.value
            )

            if group_type == GroupType.group:
                group = self._create_group(node, elements)
                if elements:
                    result.append(group)

            elif group_type == GroupType.attribute:
                if (
                    not node['attribute_value'] and
                    not node['attribute_description']
                ):
                    continue

                attribute = self._create_attribute(node, elements)

                is_new_key = True
                for existent_element in result:
                    if existent_element['key_name'] == attribute['key_name']:
                        if 'elements' not in existent_element:

                            old_element = existent_element.copy()
                            del old_element['key_name']
                            old_element['slug'] = slugify(old_element['value'])

                            existent_element['elements'] = [old_element]
                            del existent_element['value']
                            del existent_element['is_html']

                        del attribute['key_name']

                        attribute['slug'] = slugify(attribute['value'])
                        existent_element['elements'].append(attribute)
                        is_new_key = False
                        break

                if is_new_key:
                    result.append(attribute)

        return result

    def _create_tab(self, row, elements):
        """
        Tab is always the first level in factsheet payload.
        Inside of tabs should have groups or attributes.
        """
        return {
            'slug': slugify(row['group_name']),
            'display_name': row['group_name'],
            'position': row['int_order'],
            'elements': self._change_keys_from_group(elements)
        }

    def _create_group(self, row, elements):
        """
        Group is always the second level in factsheet payload.
        Inside of groups must have only attributes.
        This is not required, some tabs should not have a group inside.
        """
        return {
            'key_name': row['group_name'],
            'elements': elements,
            'position': row['int_order'],
            'slug': slugify(row['group_name']),
        }

    def _create_attribute(self, row, elements):
        """
        Attribute is often the third level in factsheet payload.
        If a tab doesn't have a group, you can add attributes inside of tabs.
        An attribute could have other attributes inside.
        """
        attribute = {
            'key_name': row['attribute_name'],
            'position': row['int_order'],
            'slug': slugify(row['attribute_name'])
        }

        if elements:
            attribute['elements'] = elements
            return attribute

        description = (
            row['attribute_value'] or row['attribute_description']
        )

        attribute.update({
            'value': description,
            'is_html': self._is_html(description)
        })

        return attribute

    def _change_keys_from_group(self, elements):
        for element in elements:
            if 'elements' not in element:
                element['elements'] = [
                    {
                        'value': element['value'],
                        'is_html': element['is_html']
                    }
                ]
                del element['value']
                del element['is_html']

        return elements

    def _is_html(self, value):
        return bool(self.REGEX_HTML.search(value, re.MULTILINE))

    def from_source(self, data):
        logger.debug('Converting data: {}'.format(data))
        [self._add_item(item) for item in data]
