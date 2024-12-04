STATEMENT = """
SELECT 
    'SUBCAT'+substring(l.strcodigo, 1, 2) as batch_key,
    l.strCodigo as category_id,
    l.strDescricao as category_description,
    s.strSetor as subcategory_id,
    s.strDescricao as subcategory_description,
    s.blnAtivo as subcategory_active
FROM
    tablinha l (nolock)
JOIN
    tabsetor s (nolock) ON l.strcodigo = s.strlinha AND l.strCodigo <> 'TM'
UNION
SELECT
    'CAT'+substring(l.strcodigo, 1, 2) as batch_key,
    l.strCodigo as category_id,
    l.strDescricao as category_description,
    null as subcategory_id,
    null as subcategory_description,
    null as subcategory_active
FROM
    tablinha l (nolock)
JOIN
    tabsetor s (nolock) ON l.strcodigo = s.strlinha AND l.strCodigo <> 'TM' 
ORDER BY
    batch_key asc,
    s.strSetor asc,
    s.strDescricao asc,
    l.strCodigo asc,
    l.strDescricao asc
"""
