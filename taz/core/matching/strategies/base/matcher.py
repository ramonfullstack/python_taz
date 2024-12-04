import hashlib
import logging
from abc import abstractmethod
from collections import OrderedDict
from typing import Dict, List, Tuple
from uuid import uuid4

from simple_settings import settings

from taz import constants
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.core.matching.common.algorithms import (
    distance,
    ngram,
    word_processing
)
from taz.helpers.json import json_dumps
from taz.utils import diacriticless

logger = logging.getLogger(__name__)


class Matcher(MongodbMixin):

    def __init__(self, *args, **kwargs):
        self.cosine = distance.CosineSimilarity()
        self.persist_changes = kwargs.get('persist_changes', True)
        self.analyzer = word_processing.SyntacticAnalyzer()
        self.ngram = ngram.ReferenceAnalyzer()

    @abstractmethod
    def _gather_self_and_similar_variations(self, variation: Dict):
        pass

    @abstractmethod
    def _find_direct_relatives_including_self(self, variation: Dict):
        pass

    @abstractmethod
    def _find_possible_relatives_excluding_direct(self, variation: Dict):
        pass

    def match_variations(self, variation: Dict) -> OrderedDict:
        """
        This method gathers many similar variations and groups them
        into a single product.
        For instance, a variation with three colors (blue, yellow and purple)
        should be assembled as a single product with three variations.
        Items must be sorted after gathering in order to successfully
        assemble a product as expected by gathering rules.
        """
        logger.debug(
            'Matching similar variations using '
            'sku:{} seller:{} as reference'.format(
                variation['sku'],
                variation['seller_id'],
            )
        )

        similar_variations = self._gather_self_and_similar_variations(
            variation
        )

        grouped = self._group_variations(
            self.sort_variations(similar_variations)
        )

        logger.debug(
            f'Grouped matched variations with {json_dumps(grouped)}'
        )

        return grouped

    def sort_variations(self, variations: List):
        """
        The criteria for variation sorting is the following:
        - main variation set by default seller
        - biggest grade

        All internal sorting methods doesn't return the variations
        that resulted in a draw.
        For instance, the sorting of a list [3,2,2,1]
        would return only [3,1], because 2 and 2 are equal.
        The criteria to sort equal members of a given method will be resolved
        on the following one.
        If a draw still happens in the last sorting method the overall list
        will have the remaining members appended.
        """
        grade_sorted = self._sort_by_biggest_grade(variations)

        logger.debug(
            f'Graded sorting for variations is {json_dumps(grade_sorted)}'
        )

        default_seller_sorted = self._sort_by_default_seller_priority(
            grade_sorted
        )
        logger.debug(
            'Default seller sorting for variations '
            f' is {json_dumps(default_seller_sorted)}'
        )

        return default_seller_sorted + [
            variation
            for variation in grade_sorted
            if variation not in default_seller_sorted
        ]

    def _group_variations(self, variations: List) -> OrderedDict:
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

        for variation in variations:
            matched_variations = []
            variation_sellers = []
            variation_key = build_key(variation)

            if variation_key in grouped_variations:
                continue

            for possible_relative in variations:
                possible_relative_key = build_key(possible_relative)

                if (
                    possible_relative_key in grouped_variations and
                    variation_key != possible_relative_key
                ):
                    continue

                attributes_are_matching = self._attributes_are_matching(
                    variation, possible_relative
                )
                eans_are_matching = self._eans_are_matching(
                    variation, possible_relative
                )
                brands_are_matching = self._brands_are_matching(
                    variation, possible_relative
                )

                if (
                    variation_key == possible_relative_key or
                    eans_are_matching and
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
                            'or eans_are_matching:{} and brands_are_matching:{} or '  # noqa
                            'attributes_are_matching:{}'.format(
                                possible_relative['sku'],
                                possible_relative['seller_id'],
                                variation_key == possible_relative_key,
                                eans_are_matching,
                                brands_are_matching,
                                attributes_are_matching
                            )
                        )

                        variations.remove(possible_relative)
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
                            variations.remove(possible_relative)
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

    def _sort_by_default_seller_priority(self, variations: List) -> List:
        """
        This method filters only variations that
        belongs to the default seller and have
        the attribute 'main_variation' set to True
        """
        default_seller_items = [
            variation
            for variation in variations
            if variation['seller_id'] == constants.MAGAZINE_LUIZA_SELLER_ID
        ]

        return sorted(
            default_seller_items,
            key=lambda v: v.get('main_variation', False),
            reverse=True
        )

    def _sort_by_biggest_grade(self, variations: List) -> List:
        """
        This method returns a list
        sorted by grades, descending (from biggest to lowest),
        but excludes the items contained on
        excluded_variations parameter.
        """
        return sorted(
            variations, key=lambda v: v.get('grade') or 0, reverse=True
        )

    def _has_parent_proximity(
        self,
        variation: Dict,
        possible_relative: Dict
    ) -> bool:
        variation_parent_id = variation.get('parent_sku')
        relative_parent_id = possible_relative.get('parent_sku')

        if variation_parent_id and relative_parent_id:
            variation_seller_id = variation['seller_id']
            relative_seller_id = possible_relative['seller_id']

            if (
                variation_seller_id == relative_seller_id and
                variation_parent_id != relative_parent_id
            ):
                return False
        return True

    def _eans_are_matching(
        self,
        variation: Dict,
        possible_relative: Dict
    ) -> bool:
        variation_ean = variation.get('ean')
        relative_ean = possible_relative.get('ean')

        return (
            bool(variation_ean) and bool(relative_ean) and
            variation_ean == relative_ean
        )

    def _brands_are_matching(
        self,
        variation: Dict,
        possible_relative: Dict
    ) -> bool:
        variation_brand = diacriticless(variation['brand'])
        possible_relative_brand = diacriticless(possible_relative['brand'])
        return variation_brand == possible_relative_brand

    def _attributes_are_matching(
        self,
        variation: Dict,
        possible_relative: Dict
    ) -> bool:
        variation_attributes = variation.get('attributes')
        if not variation_attributes:
            return False

        relative_attributes = possible_relative.get('attributes')
        if not relative_attributes:
            return False

        return variation_attributes == relative_attributes

    def _hash(self, value: str) -> str:
        return hashlib.md5(str(value).encode('utf-8')).hexdigest()

    def _clean_title(self, variation: Dict):
        words = [variation['brand']] + [
            attr['value'] for attr in variation.get('attributes', [])
        ]
        title = '{} {}'.format(
            variation['title'],
            variation.get('reference', '')
        )
        return self.analyzer.remove_ambiguous_words(title, words)

    def _clean_title_ngrams(self, variation: Dict) -> List:
        words = [variation['brand']] + [
            attr['value'] for attr in variation.get('attributes', [])
        ]

        title = variation.get('title')
        reference = variation.get('reference', '')

        cleaned_reference = self.analyzer.remove_ambiguous_words(
            reference, words
        )
        cleaned_title = self.analyzer.remove_ambiguous_words(title, words)

        reference_ngrams = self.ngram.generate_ngrams_for_variation_reference(
            cleaned_reference
        )

        title_permutations = [
            f'{cleaned_title} {ngram}'.strip()
            for ngram in reference_ngrams
        ]

        return title_permutations

    def _clean_titles(
        self,
        variation: Dict,
        possible_relative: Dict
    ) -> Tuple[str, str]:
        variation_title = self._clean_title(variation)
        possible_relative_title = self._clean_title(possible_relative)
        return variation_title, possible_relative_title

    def _titles_are_matching(
        self,
        variation: Dict,
        possible_relative: Dict
    ) -> bool:
        variation_title, possible_relative_title = self._clean_titles(
            variation,
            possible_relative
        )

        variation_title_ngrams = self._clean_title_ngrams(
            variation
        )
        possible_relative_title_ngrams = self._clean_title_ngrams(
            possible_relative
        )

        if not variation_title:
            logger.error(
                'Variation sku:{} seller:{} has no title!'.format(
                    variation['sku'],
                    variation['seller_id'],
                )
            )
            return False

        if not possible_relative_title:
            logger.error(
                'Relative variation sku:{} seller:{} has no title!'.format(
                    variation['sku'],
                    variation['seller_id'],
                )
            )
            return False

        try:
            titles_are_similar = self.cosine.are_similar(
                variation_title,
                possible_relative_title,
                variation_title_ngrams,
                possible_relative_title_ngrams,
                threshold=settings.TITLE_COMPARISON_THRESHOLD
            )
        except Exception:
            titles_are_similar = False

        if titles_are_similar:
            logger.debug(
                'Matching by title sku:{} seller:{} with relative reference '
                'sku:{} seller:{}'.format(
                    possible_relative['sku'],
                    possible_relative['seller_id'],
                    variation['sku'],
                    variation['seller_id'],
                )
            )
            return True
        return False
