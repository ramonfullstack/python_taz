import pytest
from pymongo import MongoClient

from taz.core.matching.common.enriched_products import EnrichedProductSamples
from taz.core.matching.common.samples import ProductSamples
from taz.core.matching.strategies.tests.helpers import (
    generate_medias,
    store_media
)


@pytest.fixture
def same_parent_different_ean(matcher, database):
    var_b = ProductSamples.ml_matching_product_variation_c_xbox()
    var_b['ean'] = '999999999999'
    var_b['sku'] = '999999999999'
    var_b['attributes'] = [{'value': 'PS4', 'type': 'console'}]

    variations_to_store = [
        ProductSamples.ml_matching_product_variation_c_xbox(),
        var_b,
    ]

    for variation in variations_to_store:
        database.raw_products.save(variation)
        database.medias.insert_many(generate_medias(variation))

    return ProductSamples.ml_matching_product_variation_c_xbox()


@pytest.fixture
def same_parent_different_sellers_variation(matcher, database):
    variations_to_store = [
        ProductSamples.mkp_matching_product_variation_a_shovel(),
        ProductSamples.ml_matching_product_variation_a_ps3(),
        ProductSamples.ml_matching_product_variation_b_ps4(),
        ProductSamples.ml_matching_product_variation_c_xbox(),
    ]

    for variation in variations_to_store:
        database.raw_products.save(variation)
        database.medias.insert_many(generate_medias(variation))

    return ProductSamples.ml_matching_product_variation_c_xbox()


@pytest.fixture
def same_parent_variation(matcher, database):
    variations_to_store = [
        ProductSamples.ml_matching_product_variation_a_ps3(),
        ProductSamples.ml_matching_product_variation_b_ps4(),
        ProductSamples.ml_matching_product_variation_c_xbox(),
    ]

    for variation in variations_to_store:
        database.raw_products.save(variation)
        database.medias.insert_many(generate_medias(variation))

    return ProductSamples.ml_matching_product_variation_c_xbox()


@pytest.fixture
def same_parent_variation_different_sellers(matcher, database):
    variations_to_store = [
        ProductSamples.ml_matching_product_variation_a_ps3(),
        ProductSamples.ml_matching_product_variation_b_ps4(),
        ProductSamples.ml_matching_product_variation_c_xbox(),
    ]

    for variation in variations_to_store:
        database.raw_products.save(variation)
        database.medias.insert_many(generate_medias(variation))

    return ProductSamples.ml_matching_product_variation_c_xbox()


@pytest.fixture
def matching_magoo_product(matcher, database):
    variations_to_store = [
        ProductSamples.matching_magoo_product(),
        ProductSamples.matching_ml_product_with_magoo(),
    ]

    for variation in variations_to_store:
        database.raw_products.save(variation)
        database.medias.insert_many(generate_medias(variation))

    return ProductSamples.matching_magoo_product()


@pytest.fixture
def matching_seller_different_variations(matcher, database):
    variations_to_store = [
        ProductSamples.matching_seller_variation_a(),
        ProductSamples.matching_seller_variation_b(),
    ]

    for variation in variations_to_store:
        database.raw_products.save(variation)
        database.medias.insert_many(generate_medias(variation))

    return ProductSamples.matching_seller_variation_b()


@pytest.fixture
def same_product_different_sellers(matcher, database):
    variations_to_store = [
        ProductSamples.matching_product_variation_a_220(
            seller_id='magazineluiza',
            seller_description='Magazine Luiza',
            ean='7898216299331',
            parent_sku='2555531',
            sku='255553101',
        ),
        ProductSamples.matching_product_variation_a_110(
            seller_id='magazineluiza',
            seller_description='Magazine Luiza',
            ean='7898216299330',
            parent_sku='2555531',
            sku='255553102',
        ),
        ProductSamples.matching_product_variation_a_110(
            seller_id='mappin',
            seller_description='Mappin SA',
            ean='7898216299330',
            parent_sku='9713531',
            sku='971353102',
        ),
        ProductSamples.matching_product_variation_a_220(
            seller_id='mappin',
            seller_description='Mappin SA',
            ean='7898216299331',
            parent_sku='9713531',
            sku='971353112',
        ),
    ]

    for variation in variations_to_store:
        database.raw_products.save(variation)
        database.medias.insert_many(generate_medias(variation))

    return ProductSamples.matching_product_variation_a_220(
        seller_id='mappin',
        seller_description='Mappin SA',
        ean='7898216299331',
        parent_sku='9713531',
        sku='971353112',
    )


@pytest.fixture
def matched_variation(matcher, database):
    variations_to_store = [
        ProductSamples.variation_without_parent_reference(),
        ProductSamples.variation_a_with_parent(),
        ProductSamples.ml_parent_variation(),
        ProductSamples.ml_variation_a_with_parent(),
        ProductSamples.seller_a_variation_with_parent(),
        ProductSamples.seller_b_variation_with_parent(),
        ProductSamples.seller_c_variation_with_parent(),
        ProductSamples.variation_without_ean(),
        ProductSamples.unmatched_ml_variation_with_parent()
    ]

    for variation in variations_to_store:
        database.raw_products.save(variation)
        database.medias.insert_many(generate_medias(variation))

    return ProductSamples.unmatched_ml_variation_with_parent()


@pytest.fixture
def variations_to_test():
    return [
        ProductSamples.variation_without_parent_reference(),
        ProductSamples.variation_a_with_parent(),
        ProductSamples.ml_parent_variation(),
        ProductSamples.ml_variation_a_with_parent(),
        ProductSamples.unmatched_ml_variation_with_parent(),
        ProductSamples.seller_a_variation_with_parent(),
        ProductSamples.seller_b_variation_with_parent(),
        ProductSamples.seller_c_variation_with_parent(),
        ProductSamples.variation_without_ean(),
    ]


@pytest.fixture
def database():
    client = MongoClient('127.0.0.1', 27017)
    return client.taz_tests


@pytest.fixture
def assembler_matched_ml_variations(mongo_database):
    variations_to_store = [
        ProductSamples.variation_without_parent_reference(),
        ProductSamples.variation_a_with_parent(),
        ProductSamples.ml_parent_variation(),
        ProductSamples.ml_variation_a_with_parent(),
        ProductSamples.seller_a_variation_with_parent(),
        ProductSamples.seller_b_variation_with_parent(),
        ProductSamples.seller_c_variation_with_parent(),
        ProductSamples.unmatched_ml_variation_with_parent(),
    ]

    for variation in variations_to_store:
        mongo_database.raw_products.insert_one(variation)
        mongo_database.items_ids.insert_one({'id': variation['navigation_id']})

        store_media(mongo_database, variation)

    return variations_to_store


@pytest.fixture
def variations_without_attributes_duplicated():
    return [
        {'seller_id': 'magazineroma', 'sku': '9482200926', 'brand': 'Trato', 'attributes': [{'type': 'color', 'value': 'Rosa'}], 'updated_at': '2021-09-29T11:30:09.607430+00:00'},  # noqa
        {'seller_id': 'magazineroma', 'sku': '9482200887', 'brand': 'Trato', 'attributes': [{'type': 'color', 'value': 'Branco'}],'updated_at': '2021-09-29T11:53:37.893474+00:00'}, # noqa
        {'seller_id': 'magazineroma', 'sku': '9482200890', 'brand': 'Trato', 'attributes': [{'type': 'color', 'value': 'Vermelho'}],'updated_at': '2021-09-28T19:57:04.814288+00:00'}, # noqa
        {'seller_id': 'magazineroma', 'sku': '9482200881', 'brand': 'Trato', 'attributes': [{'type': 'color', 'value': 'Preto'}],'updated_at': '2021-09-23T14:50:28.314474+00:00'}, # noqa
        {'seller_id': 'magazineroma', 'sku': '9482200904', 'brand': 'Trato', 'attributes': [{'type': 'color', 'value': 'Amarelo'}],'updated_at': '2021-09-29T11:46:08.996560+00:00'}, # noqa
        {'seller_id': 'magazineroma', 'sku': '9482200894', 'brand': 'Trato', 'attributes': [{'type': 'color', 'value': 'Bege'}],'updated_at': '2021-09-21T11:45:21.520246+00:00'}, # noqa
        {'seller_id': 'magazineroma', 'sku': '9482200912', 'brand': 'Trato', 'attributes': [{'type': 'color', 'value': 'Verde Claro'}],'updated_at': '2021-09-29T11:34:06.284559+00:00'}, # noqa
        {'seller_id': 'magazineroma', 'sku': '9482200916', 'brand': 'Trato', 'attributes': [{'type': 'color', 'value': 'Azul Claro'}],'updated_at': '2021-09-23T14:50:28.117273+00:00'}, # noqa
        {'seller_id': 'magazineroma', 'sku': '9482200922', 'brand': 'Trato', 'attributes': [{'type': 'color', 'value': 'Cinza'}],'updated_at': '2021-09-28T14:14:34.296194+00:00'} # noqa
    ]


@pytest.fixture
def variations_with_attributes_duplicated(
    variations_without_attributes_duplicated
):
    variations_without_attributes_duplicated.insert(0, {'seller_id': 'magazineroma', 'sku': '14497878997', 'brand': 'Trato', 'attributes': [{'type': 'color', 'value': 'Rosa'}], 'updated_at': '2021-09-23T14:50:28.077225+00:00'}) # noqa
    return variations_without_attributes_duplicated


@pytest.fixture
def variations():
    return [
        ProductSamples.shoploko_sku_74471(),
        ProductSamples.magazineluiza_sku_0233847(),
        ProductSamples.topbrinquedos_sku_2898(),
        ProductSamples.amplocomercial_sku_230(),
        ProductSamples.efacil_sku_200298(),
        ProductSamples.mainshop_sku_5643126(),
        ProductSamples.mainshop_sku_5643123(),
        ProductSamples.gynshop_sku_5643188(),
        ProductSamples.gynshop_sku_5643191(),
        ProductSamples.efacil_sku_185402(),
        ProductSamples.casa_e_video_sku_10359(),
        ProductSamples.topbrinquedos_sku_1964(),
        ProductSamples.amplocomercial_sku_232()
    ]


@pytest.fixture
def enriched_products():
    return [
        EnrichedProductSamples.shoploko_sku_74471(),
        EnrichedProductSamples.magazineluiza_sku_0233847(),
        EnrichedProductSamples.topbrinquedos_sku_2898(),
        EnrichedProductSamples.amplocomercial_sku_230(),
        EnrichedProductSamples.efacil_sku_200298(),
        EnrichedProductSamples.mainshop_sku_5643126(),
        EnrichedProductSamples.mainshop_sku_5643123(),
        EnrichedProductSamples.gynshop_sku_5643188(),
        EnrichedProductSamples.gynshop_sku_5643191(),
        EnrichedProductSamples.efacil_sku_185402(),
        EnrichedProductSamples.casa_e_video_sku_10359(),
        EnrichedProductSamples.topbrinquedos_sku_1964(),
        EnrichedProductSamples.amplocomercial_sku_232()
    ]
