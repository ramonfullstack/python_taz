STATEMENT = """
SELECT
    substring(m.strCodigo, 1, 5) as batch_key,
    m.strcodigo+m.strmodelo as sku,
    isnull(pc.mnyPreco, p.mnyPreco) list_price,
    isnull(pc.mnyPrecoDesconto, p.mnyPreco) price,
    1 as nationwide_delivery,
    0 as regional_delivery,
    CASE WHEN isnull(stock_count, 0) > 0 THEN 1 ELSE 0 END AS stock_count,
    CASE
        WHEN (SELECT COUNT(1) FROM tabEstoque te (nolock) WHERE te.strcodigo = m.strcodigo AND te.strmodelo = m.strmodelo AND te.strstatus_estoque in ('E','F') AND isnull(stock_count,0) > 0 ) >= 1 THEN 'on_supplier'
        WHEN (SELECT COUNT(1) FROM tabEstoque te (nolock) WHERE te.strcodigo = m.strcodigo AND te.strmodelo = m.strmodelo AND ISNULL(te.strstatus_estoque,'N') = 'N' AND isnull(stock_count,0) > 0 ) >= 1 THEN 'on_seller'
    ELSE
        'on_seller'
    END AS stock_type,
    isnull(pc.idparceiro, 0) as campaign_code,
    0 as checkout_price
FROM
    tabmodelo m (nolock)
INNER JOIN
    tabproduto p (nolock) ON p.strcodigo = m.strcodigo
INNER JOIN
    tabSetor s (nolock) ON p.strSetor = s.strSetor
LEFT JOIN
    (SELECT SUM(isnull(intquantidade_estoque,0)+isnull(intquantidade_estoque_logico,0)) AS stock_count,
        strcodigo,
        strmodelo
FROM tabEstoque te (nolock)
    GROUP BY strcodigo, strmodelo
    HAVING SUM(isnull(intquantidade_estoque,0)+isnull(intquantidade_estoque_logico,0)) > 0) e
    ON e.strcodigo = m.strcodigo AND e.strmodelo = m.strmodelo
LEFT JOIN
    mag_t_preco_cache_v2 pc (nolock) ON pc.strProduto = p.strCodigo AND pc.idLoja = 200 AND pc.idParceiro = 0
WHERE
    (
        p.blnAtivo = 1
        AND p.strLinha NOT IN ('TM')
    ) OR
    (
        p.dtInclusao >= (getdate() - 90)
    )
ORDER BY
    1, 2
"""
