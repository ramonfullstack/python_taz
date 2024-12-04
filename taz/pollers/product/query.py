from taz.pollers.product.base_query import BASE_STATEMENT, str_selections

STATEMENT = BASE_STATEMENT + """
SELECT
    t.batch_key,
    t.ean,
    t.parent_sku,
    t.main_variation,
    t.sku,
    t.product_type,
    t.title,
    t.description,
    t.reference,
    t.brand,
    t.sold_count,
    t.review_count,
    t.review_score,
    t.category_id,
    t.subcategory_id,
    t.width,
    t.height,
    t.depth,
    t.weight,
    t.voltage,
    t.color,
    t.specification_id,
    t.specification_description,
    t.release_date,
    t.updated_at,
    t.created_at,
    t.extra_categories,
    selections = STUFF(
        (SELECT DISTINCT('|' + CONVERT(varchar, sep.id_parceiro) + ';' + CONVERT(varchar, sep.id_selecao_produto))
        FROM #TMP_R_SELECAO_PRODUTO_AT sep (nolock)
        WHERE
        sep.strCodigo = t.strCodigo
        FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, ''
    ),
    t.bundles,
    t.gift_product,
    t.active
FROM
    #tmp_tabproduto t
ORDER BY
    t.batch_key DESC,
    t.sku DESC;
"""
