from taz.pollers.product.base_query import BASE_STATEMENT, str_selections

CONTROL_STATEMENT = BASE_STATEMENT + """
SELECT
    COUNT(1) AS actives
FROM
    #tmp_tabproduto
WHERE active = 1;
"""
