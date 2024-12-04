import logging
import re

from simple_settings import settings

from taz.core.matching.strategies.base.matcher import Matcher

logger = logging.getLogger(__name__)


class ProductMatcher(Matcher):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.raw_products = self.get_collection('raw_products')
        self.exclusive_strategy = kwargs.get('exclusive_strategy', False)

    def _find_direct_relatives_including_self(self, variation):
        criteria = {
            'seller_id': variation['seller_id'],
            'disable_on_matching': False,
            '$or': [
                {'sku': variation['sku']},
                {'parent_sku': variation['parent_sku']}
            ]
        }

        if self.exclusive_strategy:
            variation_strategy = variation.get(
                'matching_strategy'
            ) or settings.DEFAULT_MATCHING_STRATEGY

            criteria.update({
                'matching_strategy': variation_strategy
            })

        return self.raw_products.find(criteria).batch_size(10)

    def _find_possible_relatives_excluding_direct(self, variation):
        escaped_brand = re.escape(variation['brand'])
        brand_expression = r'^{}'.format(escaped_brand)
        brand_re = re.compile(brand_expression, re.IGNORECASE)

        criteria = {
            'disable_on_matching': False,
            'brand': brand_re,
            '$or': [
                {
                    'categories.id': {
                        '$in': [c['id'] for c in variation['categories']]
                    }
                }
            ]
        }

        ean = variation.get('ean')
        if ean:
            criteria['$or'].append({'ean': ean})

        if self.exclusive_strategy:
            variation_strategy = variation.get(
                'matching_strategy'
            ) or settings.DEFAULT_MATCHING_STRATEGY

            criteria.update({
                'matching_strategy': variation_strategy
            })

        return self.raw_products.find(criteria).batch_size(10)

    def _gather_self_and_similar_variations(self, variation):
        self_and_direct_relatives = self._find_direct_relatives_including_self(
            variation
        )

        similar_variations = []
        eans_with_attribute = set()

        def add_similar_variations(new_similar_variation):
            similar_variations.append(new_similar_variation)
            attributes = new_similar_variation.get('attributes')
            ean = new_similar_variation.get('ean')
            if attributes and ean:
                eans_with_attribute.add(ean)

        self_and_direct_relatives_list = list(self_and_direct_relatives)

        variation_attributes = variation.get('attributes')
        if variation_attributes:
            variation_attributes = sorted(
                variation_attributes,
                key=lambda x: x.get('type') + x.get('value')
            )

        for similar_variation in self_and_direct_relatives_list:
            if (
                similar_variation['sku'] == variation['sku'] and
                similar_variation['seller_id'] == variation['seller_id']
            ):
                add_similar_variations(similar_variation)
                continue

            similar_variation_attributes = similar_variation.get('attributes')
            if similar_variation_attributes:
                similar_variation_attributes = sorted(
                    similar_variation_attributes,
                    key=lambda x: x.get('type') + x.get('value')
                )

            similar_type_variation = [
                attr['type']
                for attr in similar_variation.get('attributes') or []
            ]

            type_variation = [
                attr['type']
                for attr in variation.get('attributes') or []
            ]

            if (
                sorted(similar_type_variation) != sorted(type_variation) and
                variation['parent_sku'] == similar_variation['parent_sku'] and
                variation['seller_id'] == similar_variation['seller_id']
            ):
                continue

            if (
                variation['sku'] == similar_variation['sku'] and
                variation['seller_id'] == similar_variation['seller_id'] and
                variation_attributes and similar_variation_attributes and
                variation_attributes == similar_variation_attributes
            ):
                add_similar_variations(similar_variation)
                continue

            if (
                similar_variation.get('attributes') and
                variation.get('attributes') and
                similar_variation.get('attributes') != variation.get('attributes')  # noqa
            ):
                add_similar_variations(similar_variation)

        possible_relatives = self._find_possible_relatives_excluding_direct(
            variation
        )

        possible_relatives = list(possible_relatives)

        with_attributes = []
        without_attributes = []
        for relative in possible_relatives:
            if relative.get('attributes'):
                with_attributes.append(relative)
            else:
                without_attributes.append(relative)

        if any(with_attributes) and any(without_attributes):
            if variation.get('attributes'):
                possible_relatives = with_attributes
            else:
                possible_relatives = without_attributes

        retry_variations = []

        for possible_relative in possible_relatives:
            variations_are_similar = self._variations_are_similar(
                variation,
                possible_relative,
                self_and_direct_relatives_list
            )

            similar_type_variation = [
                attr['type']
                for attr in possible_relative.get('attributes') or []
            ]

            type_variation = [
                attr['type']
                for attr in variation.get('attributes') or []
            ]

            if sorted(similar_type_variation) != sorted(type_variation):
                continue

            if variations_are_similar:
                add_similar_variations(possible_relative)
            elif possible_relative not in similar_variations:
                retry_variations.append(possible_relative)

        similar_variations = self._retry_match_variations_each_other(
            similar_variations,
            retry_variations,
            eans_with_attribute
        )

        return similar_variations

    def _retry_match_variations_each_other(
        self,
        variations_approved_to_match,
        possible_relatives,
        eans_with_attribute
    ):
        '''
        This method checks whether a discarded variation for match is
        similar to some approved variation.
        Inference that if a variation 'A'
        is similar to 'B', and 'B' is similar to 'C',
        'A' is considered to be similar to 'C'
        A -> B | B -> C | A -> C
        '''
        previously_approved_variations_quantity = len(
            variations_approved_to_match
        )

        def add_similar_variations(new_similar_variation):
            variations_approved_to_match.append(new_similar_variation)
            attributes = new_similar_variation.get('attributes')
            ean = new_similar_variation.get('ean')
            if attributes and ean:
                eans_with_attribute.add(ean)
        variations_to_retry_match = []

        for possible_relative in possible_relatives:
            # for each possible relative,
            # check if it is similar to some approved variation
            if possible_relative in variations_approved_to_match:
                continue
            for approved_variation in variations_approved_to_match:
                variations_are_similar = self._variations_are_similar(
                    approved_variation,
                    possible_relative,
                )
                possible_relative_is_trustable = (
                    self._variation_is_trustable(
                        possible_relative,
                        eans_with_attribute
                    )
                )
                if (
                    variations_are_similar and
                    possible_relative_is_trustable
                ):
                    add_similar_variations(possible_relative)
                    break
            if (
                possible_relative not in variations_approved_to_match and
                possible_relative not in variations_to_retry_match
            ):
                variations_to_retry_match.append(possible_relative)

        there_are_more_possibilities_to_match = (
            len(variations_approved_to_match) >
            previously_approved_variations_quantity
        )
        if there_are_more_possibilities_to_match:
            return self._retry_match_variations_each_other(
                variations_approved_to_match,
                variations_to_retry_match,
                eans_with_attribute
            )
        else:
            return variations_approved_to_match

    def _variation_is_trustable(self, variation, eans_trustables_list):
        '''
        A trustable variation, in this point,
        is a variation with attribute or
        has ean equal of an approved variation that has attributes
        '''
        variation_has_attributes = bool(variation.get('attributes'))
        variation_ean = variation.get('ean')
        variation_enable_to_match = (
            variation.get('disable_on_matching') is False
        )
        return (
            variation_enable_to_match and (
                variation_ean in eans_trustables_list or
                variation_has_attributes
            )
        )

    def _variations_are_similar(
        self,
        variation,
        possible_relative,
        self_and_direct_relatives_list=None
    ):
        if (
            self_and_direct_relatives_list and
            possible_relative in self_and_direct_relatives_list
        ):
            logger.debug(
                'Relative sku:{} seller:{} already belongs '
                'to similar variations.'.format(
                    possible_relative['sku'],
                    possible_relative['seller_id']
                )
            )
            return False

        if not self._has_parent_proximity(variation, possible_relative):
            logger.debug(
                'Relative sku:{} seller:{} is not from same '
                'parent_id of sku:{} seller:{}. '
                'Untrusty match could happen, skipping.'.format(
                    possible_relative['sku'],
                    possible_relative['seller_id'],
                    variation['sku'],
                    variation['seller_id'],
                )
            )
            return False

        eans_are_matching = self._eans_are_matching(
            variation, possible_relative
        )
        titles_are_matching = self._titles_are_matching(
            variation, possible_relative
        )
        brands_are_matching = self._brands_are_matching(
            variation, possible_relative
        )

        if not brands_are_matching:
            logger.debug(
                'Brands are not matching. '
                'Variation {}:{} is not similar to {}:{}'.format(
                    possible_relative['sku'],
                    possible_relative['seller_id'],
                    variation['sku'],
                    variation['seller_id']
                )
            )
            return False

        if not eans_are_matching and not titles_are_matching:
            logger.debug(
                'Relative sku:{} seller:{} '
                'doesnt match EAN and title, skipping.'.format(
                    possible_relative['sku'],
                    possible_relative['seller_id']
                )
            )
            return False

        if not eans_are_matching and not brands_are_matching:
            logger.warning(
                'Relative sku:{} seller:{} '
                'doesn\'t not have attributes, skipping.'.format(
                    possible_relative['sku'],
                    possible_relative['seller_id']
                )
            )
            return False

        logger.info(
            'Relative sku:{} seller:{} being gathered as a similar '
            'of sku:{} seller:{} persist_changes:{}'.format(
                possible_relative['sku'],
                possible_relative['seller_id'],
                variation['sku'],
                variation['seller_id'],
                self.persist_changes
            )
        )
        return True
