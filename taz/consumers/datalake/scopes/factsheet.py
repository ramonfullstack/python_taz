import datetime
import logging
from copy import copy
from functools import cached_property
from typing import Dict, List

from taz.constants import DELETE_ACTION
from taz.core.storage.factsheet_storage import FactsheetStorage

logger = logging.getLogger(__name__)


class Scope:
    name = 'factsheet'

    def __init__(
        self,
        sku: str,
        seller_id: str,
        navigation_id: str = None,
        **kwargs
    ):
        self.__sku = sku
        self.__seller_id = seller_id
        self.__navigation_id = navigation_id
        self.__action = kwargs.get('action')

    @cached_property
    def factsheet_storage(self):
        return FactsheetStorage()

    def get_data(self):
        factsheet = self.__get_factsheet()

        if not factsheet:
            logger.warning(
                f'Item not found with scope:{self.name} '
                f'sku:{self.__sku} seller_id:{self.__seller_id}'
            )
            return []

        return self.__format_payload(factsheet)

    def __format_payload(self, factsheet):
        try:
            items = []
            for item in factsheet['items']:
                element_group = item['display_name']
                if self.__is_hierarchical(item['elements']):
                    for elements in item['elements']:
                        element_key = elements['key_name']
                        element_values = self.__generate_elements(
                            item['elements'], element_key
                        )
                        result = {
                            'element_group': element_group,
                            'element_key': element_key,
                            'element_values': element_values
                        }
                        items.append(result)
                else:
                    element_key = copy(element_group)
                    for elements in item['elements']:
                        element_key = elements['key_name']
                        element_values = self.__generate_elements(
                            elements.get('elements', [elements]), element_key
                        )
                        result = {
                            'element_group': element_group,
                            'element_key': element_key,
                            'element_values': element_values
                        }
                        items.append(result)

            return {
                'sku': self.__sku,
                'seller_id': self.__seller_id,
                'navigation_id': self.__navigation_id,
                'action': self.__action,
                'updated_at': datetime.datetime.now().isoformat(),
                'items': items
            }
        except Exception as e:
            logger.error(
                f'An error occurred while processing with scope:{self.name} '
                f'seller_id:{self.__seller_id} sku:{self.__sku} error:{e}'
            )
            return

    def __generate_elements(self, elements, element_key):
        elements_values = []
        for element in elements:
            if element.get('elements'):
                element_key = element.get('key_name', element_key)
                elements_values += self.__generate_elements(
                    element.get('elements'),
                    element_key
                )
            else:
                elements_values.append({
                    'key': element.get('key_name', element_key),
                    'value': element.get('value')
                })
        return elements_values

    def __get_factsheet(self):
        if self.__action == DELETE_ACTION:
            return {
                'items': [],
                'navigation_id': self.__navigation_id
            }

        return self.factsheet_storage.get_bucket_data(
            sku=self.__sku,
            seller_id=self.__seller_id,
        )

    @staticmethod
    def __is_hierarchical(elements: List[Dict]) -> int:
        for element in elements:
            for element_item in element.get('elements') or []:
                if element_item.get('elements'):
                    return True
        return False
