import logging
from collections import OrderedDict
from copy import deepcopy
from functools import cached_property
from typing import Dict, List
from uuid import uuid4

from taz.core.matching.strategies.base.matcher import Matcher

logger = logging.getLogger(__name__)


class ProductMatcher(Matcher):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cached_property
    def mongo_collection(self):
        return self.get_collection('raw_products')

    def _find_direct_relatives_including_self(self, variation: Dict) -> List:
        return self.mongo_collection.find({
            '$or': [
                {
                    'seller_id': variation['seller_id'],
                    'sku': variation['sku']
                },
                {
                    'seller_id': variation['seller_id'],
                    'parent_sku': variation['parent_sku']
                }
            ]
        }).batch_size(10)

    def _sort_attributes(self, attributes: List) -> List:
        if attributes:
            return sorted(
                attributes,
                key=lambda x: x.get('type') + x.get('value')
            )

    def _gather_self_and_similar_variations(self, variation: Dict) -> List:
        self_and_direct_relatives = self._find_direct_relatives_including_self(
            variation
        )

        similar_variations = []
        self_and_direct_relatives_list = list(self_and_direct_relatives)

        variation_attributes = self._sort_attributes(
            variation.get('attributes')
        )

        attributes_type = sorted([
            attr['type']
            for attr in variation_attributes or []
        ])

        for similar_variation in self_and_direct_relatives_list:
            if (
                similar_variation['sku'] == variation['sku'] and
                similar_variation['seller_id'] == variation['seller_id']
            ):
                similar_variations.append(similar_variation)
                continue

            similar_variation_attributes = self._sort_attributes(
                similar_variation.get('attributes')
            )

            similar_attributes_type = sorted([
                attr['type']
                for attr in similar_variation_attributes or []
            ])

            if similar_attributes_type != attributes_type:
                continue

            if (
                similar_variation_attributes and variation_attributes and
                similar_variation_attributes != variation_attributes
            ):
                similar_variations.append(similar_variation)

        return similar_variations

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

        grouped_variations = []

        built_attributes = []

        variations_copy = deepcopy(variations)
        for variation in variations:
            matched_variations = []
            variation_sellers = []
            variation_key = build_key(variation)

            if variation_key in grouped_variations:
                continue

            for possible_relative in variations_copy:
                possible_relative_key = build_key(possible_relative)

                if (
                    possible_relative_key in grouped_variations and
                    variation_key != possible_relative_key
                ):
                    continue

                attributes_are_matching = self._attributes_are_matching(
                    variation, possible_relative
                )
                brands_are_matching = self._brands_are_matching(
                    variation, possible_relative
                )

                if (
                    variation_key == possible_relative_key or
                    brands_are_matching or
                    attributes_are_matching
                ):
                    if possible_relative['seller_id'] in variation_sellers:
                        logger.debug(
                            'Multiple SKUs from same seller are '
                            'being grouped. sku:{} seller:{} will be skipped. '
                            'Fix the product on its source '
                            'and submit it for matching again. '
                            'Condition "variation_key == possible_relative_key":{} '  # noqa
                            'and brands_are_matching:{} or '
                            'attributes_are_matching:{}'.format(
                                possible_relative['sku'],
                                possible_relative['seller_id'],
                                variation_key == possible_relative_key,
                                brands_are_matching,
                                attributes_are_matching
                            )
                        )

                        continue

                    variation_attributes = possible_relative.get('attributes')
                    if (
                        variation_attributes and
                        variation_attributes in [
                            k for k, _ in built_attributes
                        ]
                    ):
                        seller_repeats_attribute = any(
                            possible_relative['seller_id'] in sellers and
                            variation_attributes == attribute
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
                    grouped_variations.append(possible_relative_key)

                    if (
                        variation_key != possible_relative_key and
                        variation_key not in grouped_variations
                    ):
                        grouped_variations.append(variation_key)

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
