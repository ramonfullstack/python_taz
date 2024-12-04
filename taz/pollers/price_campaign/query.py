STATEMENT = """
    WITH Tab1 (strcodigo, string)  
    AS  
    (  
    SELECT p.strcodigo,  '|' + CONVERT(VARCHAR(20), pc.idParceiro) + ';' + CONVERT(VARCHAR(20), isnull(pc.mnyPreco, p.mnyPreco)) + ';' + CONVERT(VARCHAR(20), isnull(pc.mnyPrecoDesconto, p.mnyPreco)) string 
    FROM MAG_T_PRECO_CACHE_v2 pc (NOLOCK)
        inner join  tabproduto p (nolock) ON p.strcodigo = pc.strProduto AND p.blnAtivo = 1 AND p.strLinha NOT IN ('TM')
    WHERE
        (
            pc.idparceiro = 0 AND
            pc.idLoja = 200
        ) OR
        (
            pc.idLoja = 200 AND 
            pc.idparceiro != 0 AND
            NOT EXISTS (      
                SELECT NULL
                FROM mag_t_preco_cache_v2 pc1 (nolock)
                WHERE 
                    pc1.strProduto = pc.strProduto and
                    pc1.idLoja = 200 AND 
                    pc1.idParceiro = 0 AND 
                    pc1.mnyPreco = pc.mnyPreco AND 
                    pc1.mnyPrecoDesconto = pc.mnyPrecoDesconto
            )
        )
    ),
    e (stock_count, strcodigo, strmodelo)
    as
    ( 
    SELECT SUM(isnull(intquantidade_estoque,0)+isnull(intquantidade_estoque_logico,0)) AS stock_count, strcodigo, strmodelo        
        FROM tabEstoque te (nolock)       
        GROUP BY strcodigo, strmodelo
    )          
    SELECT
            substring(m.strCodigo, 1, 5) AS batch_key, 
            m.strcodigo+m.strmodelo AS sku,
            prices = STUFF(
                (
                    select string from tab1  where tab1.strcodigo = m.strCodigo
                    FOR XML PATH(''), TYPE
                ).value('.', 'NVARCHAR(MAX)'), 1, 1, ''
            )
        FROM
            tabmodelo m (nolock)
        INNER JOIN
            tabproduto p (nolock) ON p.strcodigo = m.strcodigo AND p.blnAtivo = 1 AND p.strLinha NOT IN ('TM')
        INNER JOIN
            tabSetor s (nolock) ON p.strSetor = s.strSetor
        INNER JOIN  e
            ON e.strcodigo = m.strcodigo AND e.strmodelo = m.strmodelo AND e.stock_count > 0
"""
