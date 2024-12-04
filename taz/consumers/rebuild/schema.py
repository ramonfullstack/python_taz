from marshmallow import Schema, fields, validate


class RebuildSchema(Schema):
    scope = fields.String(
        required=True,
        validate=[validate.OneOf([
            'seller',
            'complete_products_by_seller',
            'complete_products_by_sku',
            'catalog_notification',
            'product_score_by_seller',
            'product_score_by_sku',
            'marvin_seller',
            'matching_omnilogic',
            'inactivate_seller_products',
            'marvin_seller_ipdv',
            'seller_sells_to_company',
            'matching_by_sku',
            'classify_by_sku',
            'maas_product_reprocess',
            'media_rebuild'
        ],
            error='Scope must be between ({choices})')]
    )
    action = fields.String(
        required=True,
        validate=[validate.OneOf(
            ['update', 'delete'],
            error='Action must be between ({choices})')]
    )
