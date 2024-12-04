from simple_settings import settings

selections = list(
    filter(None, settings.POLLER_PRODUCT_SELECTIONS.split(','))
)

str_selections = ', '.join(list(
    map(lambda sel: "'{0}'".format(sel.strip()), selections)
))

ACTIVE_FILTER = """
WHERE
    (active = 1 --O campo active representa o status do BUNDLE, GIFT ou PRODUCT nessa respectiva ordem. Evitando que um bundle ou gift inativo/expirado tenham o status do produto retornado.
    OR created_at >= (getdate() - 90)) --Mesmo que um BUNDLE, GIFT ou PRODUCT esteja inativo ele será retornado durante 90 dias
"""

BASE_STATEMENT = """
-- VERIFICA E EXCLUI TABELAS TEMPORARIAS
IF OBJECT_ID('tempdb.dbo.#tmp_tabproduto', 'U') IS NOT NULL  
   DROP TABLE #tmp_tabproduto;
IF OBJECT_ID('tempdb.dbo.#tmp_selecao_produto', 'U') IS NOT NULL  
   DROP TABLE #tmp_selecao_produto;
IF OBJECT_ID('tempdb.dbo.#tmp_r_selecao_produto_at', 'U') IS NOT NULL  
   DROP TABLE #tmp_r_selecao_produto_at;
IF OBJECT_ID('tempdb.dbo.#tmp_gift', 'U') IS NOT NULL
   DROP TABLE #tmp_gift;

SELECT
  strcodigomodelo,
  gift_product,
  bitativo
INTO #tmp_gift
FROM
  (
    SELECT
      strcodigomodelo,
      gift_product,
      bitativo,
      row_number() over (partition by strcodigomodelo order by bitativo desc) as position
    FROM
      (
        SELECT DISTINCT
          isnull(bp.strCodigoModelo, bp.strCodigoMestre + '00') as strCodigoModelo,
          isnull(bb.strCodigoModelo, bb.strCodigoMestre + '00') as gift_product,
          case
			when bc.bitAtivo = 1 and getdate() BETWEEN bc.dtaInicio and bc.dtaFim then 1
			else 0
		  end as bitAtivo
        FROM
          MAG_T_BRIN_PRODUTOS bp (nolock)
          INNER JOIN MAG_T_BRIN_CAMPANHAS bc (nolock) ON bc.id = bp.intIdCampanha
          INNER JOIN MAG_T_BRIN_BENEFICIOS bb (nolock) ON bc.id = bb.intIdCampanha
      ) t
  ) a
WHERE
  a.position = 1 AND
  a.strcodigomodelo is not null;
CREATE INDEX idx_tmp_gift_001 on #tmp_gift (strcodigomodelo);

-- BUSCA OS PRODUTOS PARA SEREM EXPORTADOS
SELECT
    *
INTO
    #tmp_tabproduto
FROM (    
    SELECT
        substring(m.strCodigo, 1, 5) as batch_key,
        m.codbarra as ean,
        isnull(p.strAgruparProduto, p.strmestre) as parent_sku,
        main_variation = case when m.strCodigo = p.strmestre and (spec.idTipoEspecificacao is not null or ltrim(rtrim(v.descricao_voltagem_produto)) is not null) then 1 else 0 end,
        m.strcodigo + m.strmodelo as sku,
        product_type = case when b.strCodigo is not null then 2
                            when brin.strCodigoModelo is not null then 3
                            else 1 end,
        p.strDescricao as title,
        vtb.strvalor as description,
        ltrim(rtrim(p.strReferencia)) as reference,
        lower(ltrim(rtrim(p.strMarca))) as brand,
        0 as sold_count,
        0 as review_count,
        0 as review_score,
        ltrim(rtrim(p.strLinha)) as category_id,
        ltrim(rtrim(p.strSetor)) as subcategory_id,
        ROUND(p.fltLargura, 3) as width,
        ROUND(p.fltAltura, 3) as height,
        ROUND(p.fltProfundidade, 3) as depth,
        ROUND(p.fltPeso, 3) as weight,
        ltrim(rtrim(v.descricao_voltagem_produto)) as voltage,
        case when c.strDescricao != '' and ltrim(rtrim(v.descricao_voltagem_produto)) is null then isnull(cor_ficha.strValor, c.strDescricao) else null end as color,
        spec.idTipoEspecificacao as specification_id,
        spec.strDescricaoSite as specification_description,
        p.dtPrevenda as release_date,
        m.dtstatus as updated_at,
        p.dtInclusao as created_at,
        null as extra_categories,
        bundles = STUFF(
                    (SELECT DISTINCT('|' + CONVERT(varchar, pb.strcodigo) + ';' + CONVERT(varchar, pb.strmodelo) + ';' + CONVERT(varchar, pb.valor) + ';' + CONVERT(varchar, pb.intquantidade))
                    FROM MAG_T_PRODS_BUNDLE pb (nolock)
                    WHERE pb.strbundle = m.strcodigo
                    FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, ''
                ),
        gift_product,
        case when b.strCodigo is not null /*BUNDLE*/ and b.ativo = 1 and (getdate() BETWEEN b.dtInicial AND b.dtfinal) and p.blnativo = 1 then 1
             when brin.strCodigoModelo is not null /*GIFT*/ and brin.bitAtivo = 1 and p.blnativo = 1 then 1
             when b.strCodigo is null /*NOT BUNDLE*/ and brin.strCodigoModelo is null /*NOT GIFT*/ and p.blnativo = 1 then 1
             else 0
        end as active,
        p.strMestre,
        p.strCodigo,
        p.strMarca,
        p.strlinha,
        p.strSetor
    FROM
        tabmodelo m (nolock)
    INNER JOIN
        tabproduto p (nolock) ON p.strCodigo = m.strCodigo AND p.strReferencia NOT IN ('Garantia Estendida', 'Troca Certa', 'SERVICO')
    INNER JOIN
        tabLinha l (nolock) ON l.strCodigo = p.strLinha
    INNER JOIN
        tabSetor s (nolock) ON s.strLinha = p.strLinha AND s.strSetor = p.strSetor
    LEFT JOIN
        mag_t_ficha_ficha_tecnica_publicada tb (nolock) ON tb.strCodigo = m.strCodigo AND tb.strModelo = m.strModelo
    LEFT JOIN
        mag_t_ficha_valor_atributo_ficha_tecnica_publicada vtb (nolock) ON vtb.idfichatecnicapublicada = tb.idfichatecnicapublicada AND vtb.intordem = 2
    LEFT JOIN
        tabvoltagem_produto v (nolock) ON v.id_voltagem_produto = p.blnModelo AND p.blnModelo not in (0, 3)
    LEFT JOIN
        tabCor c (nolock) ON c.strCor = m.strModelo
    LEFT JOIN
        MAG_T_FICHA_VALOR_ATRIBUTO_FICHA_TECNICA_PUBLICADA cor_ficha (nolock)  on tb.idProduto = cor_ficha.idProduto and cor_ficha.strNomeAtributo = 'Cor'
    LEFT JOIN
        MAG_T_PRODUTO_ESPECIFICACAO spec (nolock) ON spec.idEspecificacao = p.idEspecificacao
    LEFT JOIN
        MAG_T_BUNDLE b (nolock) ON b.strCodigo = m.strCodigo --and b.ativo = 1 and b.dtfinal > getdate()
    LEFT JOIN
        #tmp_gift brin on brin.strCodigoModelo = m.strCodigo+m.strModelo
) AS a
{filter_actives}
ORDER BY
    sku DESC
CREATE INDEX IDX_TMP_TABPRODUTO_001 ON #tmp_tabproduto (strCodigo);
    -- BUSCA A SELECAO DE PRODUTO
    SELECT DISTINCT 
            se.id_parceiro,
            se.id_selecao_produto,
            sep.strCodigo,
            sep.strMarca,
            sep.strLinha,
            sep.strSetor
    INTO
        #tmp_selecao_produto
    FROM
        selecao_produto se (nolock)
        INNER JOIN r_selecao_produto_at sep (nolock) ON sep.id_selecao_produto = se.id_selecao_produto
    WHERE             
        se.id_selecao_produto in ({selections})
        AND se.ativo_selecao_produto = 1
        AND getdate() BETWEEN se.dtinicial_selecao_produto AND se.dtfinal_selecao_produto;
    CREATE INDEX IDX_TMP_SELECAO_PRODUTO_001 ON #TMP_SELECAO_PRODUTO (strCodigo) include (strMarca, strLinha, strSetor);
    CREATE INDEX IDX_TMP_SELECAO_PRODUTO_002 ON #TMP_SELECAO_PRODUTO (strMarca) include (strCodigo, strLinha, strSetor);
    CREATE INDEX IDX_TMP_SELECAO_PRODUTO_003 ON #TMP_SELECAO_PRODUTO (strLinha) include (strCodigo, strMarca, strSetor);
    CREATE INDEX IDX_TMP_SELECAO_PRODUTO_004 ON #TMP_SELECAO_PRODUTO (strSetor) include (strCodigo, strMarca, strLinha);
    -- BUSCA A SELECAO DE PRODUTO RECURSIVA
    SELECT DISTINCT
        p.strcodigo,
        sep.id_parceiro,
        sep.id_selecao_produto
    INTO
        #tmp_r_selecao_produto_at
    FROM
        #tmp_selecao_produto sep (nolock),
        #tmp_tabproduto p (nolock)
    WHERE
        (sep.strCodigo IS NOT NULL and sep.strLinha IS NULL and sep.strSetor IS NULL and sep.strMarca IS NULL and (sep.strCodigo = p.strMestre ))
    UNION
    SELECT
        p.strcodigo,
        sep.id_parceiro,
        sep.id_selecao_produto
    FROM
        #tmp_selecao_produto sep (nolock),
        #tmp_tabproduto p (nolock)
    WHERE
        (sep.strCodigo IS NOT NULL and sep.strLinha IS NULL and sep.strSetor IS NULL and sep.strMarca IS NULL and (sep.strCodigo = p.strCodigo))
    UNION
    SELECT
        p.strcodigo,
        sep.id_parceiro,
        sep.id_selecao_produto
    FROM
        #tmp_selecao_produto sep (nolock),
        #tmp_tabproduto p (nolock)
    WHERE
        (sep.strCodigo IS NULL and sep.strLinha IS NULL and sep.strSetor IS NULL and sep.strMarca IS NOT NULL and sep.strMarca = p.strMarca )
    UNION
    SELECT
        p.strcodigo,
        sep.id_parceiro,
        sep.id_selecao_produto
    FROM
        #tmp_selecao_produto sep (nolock),
        #tmp_tabproduto p (nolock)
    WHERE
        (sep.strCodigo IS NULL and sep.strLinha IS NOT NULL and sep.strSetor IS NULL and sep.strMarca IS NULL and  sep.strLinha = p.strlinha)
    UNION
    SELECT
        p.strcodigo,
        sep.id_parceiro,
        sep.id_selecao_produto
    FROM
        #tmp_selecao_produto sep (nolock),
        #tmp_tabproduto p (nolock)
    WHERE
        (sep.strCodigo IS NULL and sep.strLinha IS NOT NULL and sep.strSetor IS NULL and sep.strMarca IS NOT NULL and sep.strLinha = p.strlinha and sep.strMarca = p.strMarca)                      
    UNION
    SELECT
        p.strcodigo,
        sep.id_parceiro,
        sep.id_selecao_produto
    FROM
        #tmp_selecao_produto sep (nolock),
        #tmp_tabproduto p (nolock)
    WHERE
        (sep.strCodigo IS NULL and sep.strLinha IS NOT NULL and sep.strSetor IS NOT NULL and sep.strMarca IS NULL and sep.strLinha = p.strlinha and sep.strSetor = p.strSetor)
    UNION
    SELECT
        p.strcodigo,
        sep.id_parceiro,
        sep.id_selecao_produto
    FROM
        #tmp_selecao_produto sep (nolock),
        #tmp_tabproduto p (nolock)
    WHERE
        (sep.strCodigo IS NULL and sep.strLinha IS NOT NULL and sep.strSetor IS NOT NULL and sep.strMarca IS NOT NULL and sep.strMarca = p.strMarca and sep.strLinha = p.strlinha and sep.strSetor = p.strSetor)
    UNION
    SELECT
        p.strcodigo,
        sep.id_parceiro,
        sep.id_selecao_produto
    FROM
        #tmp_selecao_produto sep (nolock),
        #tmp_tabproduto p (nolock)
    WHERE
        (sep.strCodigo IS NULL and sep.strLinha IS NULL and sep.strSetor IS NULL and sep.strMarca IS NULL);
    CREATE INDEX IDX_TMP_R_SELECAO_PRODUTO_AT_001 ON #TMP_R_SELECAO_PRODUTO_AT (strcodigo, id_parceiro, id_selecao_produto);
""".format(
    selections=str_selections,
    filter_actives=(
        ACTIVE_FILTER
        if settings.POLLER_PRODUCT_SHOULD_FILTER_CREATED_AT_AND_ACTIVE else ''
    )
)