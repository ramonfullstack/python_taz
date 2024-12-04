STATEMENT = """
SELECT
    substring(m.strCodigo, 1, 5) AS batch_key,
    m.strcodigo + m.strmodelo AS sku,
    p.mnyPreco AS list_price,
    isnull(convert(varchar(20), m.CODITPROD) + convert(varchar(20), m.DIGITPROD), 0) AS gemco_id,
    bundles = STUFF(
        (SELECT DISTINCT('|' + CONVERT(varchar, pb.strcodigo) + CONVERT(varchar, pb.strmodelo) + ';' + CONVERT(varchar, pb.intquantidade))
        FROM MAG_T_PRODS_BUNDLE pb (nolock)
        WHERE pb.strbundle = m.strcodigo
        FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, ''
    )
FROM
    tabModelo m (NOLOCK)
INNER JOIN
    tabProduto p (NOLOCK) ON p.strCodigo = m.strCodigo
INNER JOIN
    tabSetor s (NOLOCK) ON p.strSetor = s.strSetor
LEFT JOIN
    MAG_T_BUNDLE b (nolock) ON b.strCodigo = m.strCodigo
WHERE
    p.strLinha NOT IN ('TM')
    AND p.blnAtivo = 1
ORDER BY
    substring(m.strCodigo, 1, 5) DESC,
    m.strcodigo DESC,
    m.strmodelo DESC
"""
