import logging
from collections import OrderedDict
from copy import deepcopy
from functools import cached_property
from typing import Dict, List
from uuid import uuid4

from taz.constants import OMNILOGIC_STRATEGY, SOURCE_OMNILOGIC
from taz.core.matching.strategies.base.matcher import Matcher
from taz.core.matching.strategies.utils import _mount_similar_variations

logger = logging.getLogger(__name__)


class ProductMatcher(Matcher):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    @cached_property
    def enriched_products(self):
        return self.get_collection('enriched_products')

    def _get_enriched_product(self, sku: str, seller_id: str) -> Dict:
        return self.enriched_products.find_one(
            {
                'sku': sku,
                'seller_id': seller_id,
                'source': SOURCE_OMNILOGIC
            },
            {
                '_id': 0,
                'product_hash': 1
            }
        ) or {}

    def _find_direct_relatives_including_self(self, variation):
        sku = variation['sku']
        seller_id = variation['seller_id']

        enriched_product = self._get_enriched_product(sku, seller_id)

        if not enriched_product or not enriched_product.get('product_hash'):
            logger.warning(
                f'Product hash not found for sku:{sku} and '
                f'seller_id:{seller_id} with source:{SOURCE_OMNILOGIC}'
            )

            return [
                self.raw_products.find_one(
                    {
                        'sku': sku,
                        'seller_id': seller_id
                    }
                )
            ]

        similar_variations = list(
            self.raw_products.find(
                {
                    'matching_strategy': OMNILOGIC_STRATEGY,
                    'product_hash': enriched_product['product_hash']
                }
            )
        )
        return similar_variations

    def _gather_self_and_similar_variations(self, variation: Dict) -> List:
        self_and_direct_relatives = self._find_direct_relatives_including_self(
            variation
        )

        return _mount_similar_variations(
            variation,
            self_and_direct_relatives
        )

    def _group_variations(self, variations: List) -> Dict:
        """
        Here variations are grouped using the following logic:
        1) Possible attributes that can be used for the group key are checked
        2) Based on the previous check, we start grouping products
        3) Checking and deduplication is made to ensure proper grouping
        """
        def build_key(variation):
            return '{}:{}'.format(variation['sku'], variation['seller_id'])

        variation_groups = OrderedDict()

        grouped_variations_keys = []

        built_attributes = []

        variations_copy = deepcopy(variations)
        for variation in variations:
            matched_variations = []
            variation_sellers = []
            variation_key = build_key(variation)

            if variation_key in grouped_variations_keys:
                continue

            for possible_relative in variations_copy:
                possible_relative_key = build_key(possible_relative)

                if (
                    possible_relative_key in grouped_variations_keys and
                    variation_key != possible_relative_key
                ):
                    continue

                attributes_are_matching = self._attributes_are_matching(
                    variation, possible_relative
                )

                if (
                    variation_key != possible_relative_key and
                    not attributes_are_matching
                ):
                    continue

                variation_attributes = possible_relative.get('attributes')
                if variation_attributes:
                    seller_repeats_attribute = any(
                        variation_attributes == attribute and
                        possible_relative['seller_id'] in sellers
                        for attribute, sellers in built_attributes
                    )

                    if seller_repeats_attribute:
                        logger.error(
                            'Attribute {} is already contained on another '
                            'group. sku:{} seller:{} will be '
                            'skipped.'.format(
                                variation_attributes,
                                possible_relative['sku'],
                                possible_relative['seller_id'],
                            )
                        )
                        variations_copy.remove(possible_relative)
                        continue

                variation_sellers.append(possible_relative['seller_id'])
                matched_variations.append(possible_relative)
                grouped_variations_keys.append(possible_relative_key)

                if (
                    variation_key != possible_relative_key and
                    variation_key not in grouped_variations_keys
                ):
                    grouped_variations_keys.append(variation_key)

                if variation_attributes:
                    built_attributes.append(
                        (
                            variation_attributes,
                            [v['seller_id'] for v in matched_variations]
                        )
                    )

            if not matched_variations:
                continue

            group_key = uuid4().hex
            variation_groups[group_key] = matched_variations

        return variation_groups

    def _attributes_are_matching(
        self,
        variation: Dict,
        possible_relative: Dict
    ) -> bool:
        variation_attributes = variation.get('attributes') or []
        relative_attributes = possible_relative.get('attributes') or []

        return variation_attributes == relative_attributes
