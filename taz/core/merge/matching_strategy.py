import logging
from abc import abstractmethod
from typing import Dict, List

from simple_settings import settings

from taz.constants import (
    CHESTER_STRATEGY,
    OMNILOGIC_STRATEGY,
    SOURCE_OMNILOGIC
)
from taz.consumers.core.database.mongodb import MongodbMixin

logger = logging.getLogger(__name__)


class MatchingStrategyBase(MongodbMixin):

    @abstractmethod
    def validate_and_get_matching_strategy(self, **kwargs):
        ...


class ChesterMatchingStrategy(MatchingStrategyBase):

    def validate_and_get_matching_strategy(self, **kwargs) -> Dict:
        payload = {}
        product = kwargs.get('product')
        category = product['categories'][0]['id']
        subcategories = product['categories'][0]['subcategories']
        matching_uuid = product.get('matching_uuid')

        if (
            settings.ENABLED_CHESTER_STRATEGY and
            matching_uuid and
            (
                category in settings.ENABLED_CATEGORIES_CHESTER_STRATEGY or
                '*' in settings.ENABLED_CATEGORIES_CHESTER_STRATEGY
            ) and
            self.__validate_subcategories(subcategories)
        ):
            payload.update({'matching_strategy': CHESTER_STRATEGY})

        return payload

    @staticmethod
    def __validate_subcategories(subcategories: List) -> bool:
        if (
            not subcategories or
            '*' in settings.ENABLED_SUBCATEGORIES_CHESTER_STRATEGY
        ):
            return True

        for subcategory in subcategories:
            if (
                subcategory.get('id') in
                settings.ENABLED_SUBCATEGORIES_CHESTER_STRATEGY
            ):
                return True
        return False


class OmnilogicMatchingStrategy(MatchingStrategyBase):

    def validate_and_get_matching_strategy(self, **kwargs):
        enriched_products = kwargs.get('enriched_products')

        payload = {}
        omnilogic = {}

        for enriched_product in enriched_products:
            if enriched_product.get('source') == SOURCE_OMNILOGIC:
                omnilogic.update(enriched_product)
                break

        if not omnilogic:
            return payload

        if (
            omnilogic.get('product_hash') and
            omnilogic.get('entity') in settings.ENABLE_MATCHING_FROM_ENTITY
        ):
            payload.update({'matching_strategy': OMNILOGIC_STRATEGY})

        return payload
