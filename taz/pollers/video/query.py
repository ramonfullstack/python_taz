STATEMENT = """
SELECT
	left(m.strcodigo + '0000000', 7) + m.strmodelo as batch_key
	, strlinkVideo as video
FROM tabproduto (nolock) p
INNER JOIN tabmodelo m (nolock) ON p.strcodigo = m.strcodigo
WHERE COALESCE(strlinkVideo, '') != ''
ORDER BY 1
"""