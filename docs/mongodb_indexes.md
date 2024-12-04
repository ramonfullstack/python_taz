# MongoDB Indexes

```javascript

db.items_ids.createIndex({'product_id': 1})

db.id_correlations.createIndex({'sku': 1, 'seller_id': 1})
db.id_correlations.createIndex({'variation_id': 1, 'product_id': 1})
db.id_correlations.createIndex({'variation_id': 1})
db.id_correlations.createIndex({'seller_id': 1, 'sku': 1, 'product_id': 1, 'variation_id': 1})
db.id_correlations.createIndex({'product_id': 1})
db.medias.createIndex({'sku': 1, 'seller_id': 1})
db.raw_products.createIndex({'ean': 1, 'disable_on_matching': 1})
db.raw_products.createIndex({'ean': 1, 'seller_id': 1})
db.raw_products.createIndex({'parent_sku': 1, 'seller_id': 1, 'disable_on_matching': 1})
db.raw_products.createIndex({'seller_id': 1, 'disable_on_matching': 1, 'sku': 1, 'parent_sku': 1})
db.raw_products.createIndex({'seller_id': 1, 'disable_on_matching': 1})
db.raw_products.createIndex({'sku': 1, 'seller_id': 1, 'disable_on_matching': 1})
db.raw_products.createIndex({'sku': 1, 'seller_id': 1})
db.raw_products.createIndex({seller_id: 1})
db.raw_products.createIndex({'navigation_id': 1})
db.raw_products.createIndex({matching_uuid: 1, matching_strategy: 1},{partialFilterExpression: {'matching_strategy': 'CHESTER'}})
db.raw_products.createIndex({product_hash: 1, matching_strategy: 1}, {partialFilterExpression: {'matching_strategy': 'OMNILOGIC'}})

db.pending_products.createIndex({'brand': 1, 'categories.id': 1, 'disable_on_matching': 1})
db.pending_products.createIndex({'brand': 1, 'categories.id': 1, 'ean': 1})
db.pending_products.createIndex({'brand': 1})
db.pending_products.createIndex({'categories.id': 1, 'brand': 1})
db.pending_products.createIndex({'categories.id': 1})
db.pending_products.createIndex({'disable_on_matching': 1})
db.pending_products.createIndex({'ean': 1, 'disable_on_matching': 1})
db.pending_products.createIndex({'ean': 1, 'seller_id': 1})
db.pending_products.createIndex({'parent_sku': 1})
db.pending_products.createIndex({'parent_sku': 1, 'seller_id': 1, 'disable_on_matching': 1})
db.pending_products.createIndex({'seller_id': 1, 'disable_on_matching': 1, 'sku': 1, 'brand': 1, 'ean': 1, 'categories.id': 1})
db.pending_products.createIndex({'seller_id': 1, 'disable_on_matching': 1, 'sku': 1, 'parent_sku': 1})
db.pending_products.createIndex({'seller_id': 1, 'disable_on_matching': 1})
db.pending_products.createIndex({'seller_id': 1, 'sku': 1, 'parent_sku': 1})
db.pending_products.createIndex({'sku': 1, 'disable_on_matching': 1})
db.pending_products.createIndex({'sku': 1, 'parent_sku': 1})
db.pending_products.createIndex({'sku': 1, 'seller_id': 1, 'disable_on_matching': 1})
db.pending_products.createIndex({'sku': 1, 'seller_id': 1})
db.pending_products.createIndex({'sku': 1})
db.pending_products.createIndex({seller_id: 1})


db.unified_objects.createIndex({'id': 1})
db.unified_objects.createIndex({'id': 1, 'type': 1})
db.unified_objects.createIndex({'seller_id': 1, 'sku': 1, 'type': 1})

db.prices.createIndex({'sku': 1, 'seller_id': 1})

db.categories.createIndex({'id': 1})

db.customer_behaviors.createIndex({'product_id': 1})
db.customer_behaviors.createIndex({'product_id': 1, 'type': 1})

db.product_scores.createIndex({'sku': 1, 'type': 1, 'seller_id': 1})

db.unpublished_products.createIndex({'navigation_id': 1})

db.products.createIndex({'navigation_id': 1, 'seller_id': 1, 'sku': 1})

db.enriched_products.createIndex({'sku': 1, 'seller_id': 1})
db.enriched_products.createIndex({'product_hash': 1})
db.enriched_products.createIndex({'navigation_id': 1})
db.enriched_products.createIndex({'seller_id': 1, 'sku': 1, 'source': 1})
db.enriched_products.createIndex({'source': 1})
db.enriched_products.createIndex({'entity': 1})
db.enriched_products.createIndex({'source': 1, 'entity': 1, 'navigation_id': 1}, {partialFilterExpression: { source: 'magalu'}, background: true})
db.enriched_products.createIndex({'source': 1, 'classifications.product_type': 1, 'navigation_id': 1}, {partialFilterExpression: { source: 'hector'}, background: true})

db.blacklist.createIndex({'field': 1, 'term': 1})

db.price_lock.createIndex({'seller_id': 1})

db.custom_ranks.createIndex({'navigation_id': 1})
db.custom_ranks.createIndex({'type': 1})
db.custom_ranks.createIndex({'navigation_id': 1, 'type': 1})

db.custom_attributes.createIndex({'sku': 1, 'seller_id': 1})

db.scores.createIndex({'active': 1})
db.scores.createIndex({'sku': 1, 'seller_id': 1})

db.score_criterias.createIndex({'entity_name': 1, 'score_version': 1})

db.score_weights.createIndex({'entity_name': 1, 'criteria_name': 1, 'score_version': 1})

db.sellers.createIndex({'id': 1})

db.lock.createIndex([('key', 1)],unique=True)
db.lock.createIndex( [( 'created_at', 1 )], expireAfterSeconds= 1 )

db.factsheets.createIndex({'sku': 1, 'seller_id': 1}, unique=True)
sh.shardCollection('taz.factsheets', {'sku': 1, 'seller_id': 1})


db.classifications_rules.createIndex({'product_type': 1, 'operation': 1}, {unique: true})
db.classifications_rules.createIndex({'active': 1, 'product_type': 1})
db.classifications_rules.createIndex({'status': 1})

db.minimum_order_quantity.createIndex({'sku': 1, 'seller_id': 1}, {unique: true})
db.minimum_order_quantity.createIndex({'navigation_id': 1}, {unique: true})

```