STATEMENT_LIST_SKUS = """
    SELECT
        substring(f.strcodigo, 1, 5) as batch_key,
        f.strcodigo + f.strmodelo as sku,
        f.idFichaTecnicaPublicada as factsheet_id,
        f.idProduto as product_id
    FROM
        MAG_T_FICHA_FICHA_TECNICA_PUBLICADA f (nolock)
    INNER JOIN
        tabproduto p (nolock) ON p.strcodigo = f.strcodigo
    ORDER BY
        substring(f.strcodigo, 1, 5) DESC,
        f.strcodigo DESC,
        f.strmodelo DESC
"""

STATEMENT_DETAILS = """
    SELECT
        va.intOrdem AS int_order,
        va.idTipoGrupo AS group_id,
        va.strGrupoNome AS group_name,
        ISNULL(va.strChave, va.strNomeExibicao) AS attribute_name,
        CASE WHEN va.strValor IS NOT NULL AND vsa.strDescricaoItemAtributo IS NOT NULL
            THEN vsa.strDescricaoItemAtributo + ' ' + ISNULL(vsa.strUnidadeMedidaAbreviacao, '') + ' ' + convert(nvarchar(1000), va.strValor)
            ELSE va.strValor
        END AS attribute_value, 
        vsa.strDescricaoItemAtributo + '' + ISNULL(vsa.strUnidadeMedidaAbreviacao, '') AS attribute_description,
        va.idElemento AS element_id,
        va.idElementoPai AS parent_id
    FROM
        MAG_T_FICHA_VALOR_ATRIBUTO_FICHA_TECNICA_PUBLICADA va (nolock)
    LEFT JOIN
        MAG_T_FICHA_VALOR_SELECAO_ATRIBUTO_FICHA_TECNICA_PUBLICADA vsa (nolock) ON vsa.idFichaTecnicaPublicada = va.idFichaTecnicaPublicada AND vsa.idProduto = va.idProduto AND vsa.intOrdem = va.intOrdem
    WHERE
        va.idFichaTecnicaPublicada = {}
        AND va.idProduto = {}
    ORDER BY
        va.intOrdem ASC
"""
