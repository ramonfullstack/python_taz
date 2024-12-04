from typing import Dict, List


def _get_attribute_types(variation: Dict) -> List:
    variation_attributes = variation.get('attributes') or []

    attribute_types = sorted([
        attr['type']
        for attr in variation_attributes
    ])

    return attribute_types


def _mount_similar_variations(
    variation: Dict,
    self_and_direct_relatives: List
) -> List:
    variation_attr_types = _get_attribute_types(variation)
    similar_variations = []

    for similar_variation in self_and_direct_relatives:
        if (
            similar_variation['sku'] == variation['sku'] and
            similar_variation['seller_id'] == variation['seller_id']
        ):
            similar_variations.append(similar_variation)
            continue

        similar_variation_attr_types = _get_attribute_types(
            similar_variation
        )

        if similar_variation_attr_types != variation_attr_types:
            continue

        similar_variations.append(similar_variation)

    return similar_variations
