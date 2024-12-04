STATEMENT_DETAIL = """
    select
        txtCodigoHtml as html 
    from 
        MAG_T_SITE_LU_MATERIA
    where
        idConteudo = {}
"""

STATEMENT = """
select DISTINCT 
    substring(left(convert(varchar, lc.idConteudo) + '0000000', 7), 1, 3) as batch_key,
    left(convert(varchar, lc.idConteudo) + '0000000', 9) as sku,
    lc.idConteudo as id, 
    lc.strUrlFoto as image, 
    lc.strTitulo as title, 
    lc.strlegenda as caption, 
    lc.idStatus as status, 
    lc.idTipoConteudo as contentTypeId, 
    lc.strsubTitulo as subtitle,  
    lc.intClassificacao as classification, 
    DATEDIFF(s, '19700101', lc.dtaDataCadastro) as createdAt, 
    lc.strFonte as source,
    p.strCodigo as productCode,
    p.strLinha as productCategory,
    p.strSetor as productSubSategory, 
    p.strDescricao as productDescription,
    p.strReferencia as productReference,
    p.strlinkVideo as videoUrl,
    p.blnPodcast as hasPodcast, 
    p.strMarca as productBrand,
    category_values = STUFF(
        (SELECT DISTINCT('|' + CONVERT(varchar, lca.strValor) + ';' + mls.strLinha + ';' + mls.strSetor)
        FROM MAG_T_SITE_LU_CONTEUDO_ASSOC lca (nolock)
        left join MAG_T_SITE_LU_MARCA_LINHA_SETOR mls (nolock) on lca.strValor = mls.strMarca
        WHERE lc.idConteudo = lca.idConteudo
        FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, ''
    ),
    display_sessions = STUFF(
        (SELECT DISTINCT('|' + lce.strSessao)
        FROM MAG_T_SITE_LU_CONTEUDO_EXIBICAO lce (nolock)
        WHERE lc.idConteudo = lce.idConteudo
        FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, ''
    )
from MAG_T_SITE_LU_CONTEUDO lc (nolock) 
left join MAG_T_SITE_LU_CONTEUDO_ASSOC lca (nolock)
    on lc.idConteudo = lca.idConteudo
left join MAG_T_SITE_LU_MARCA_LINHA_SETOR mls (nolock)
    on lca.strValor = mls.strMarca 
left join MAG_T_SITE_LU_PODCAST pod (nolock)
    on lc.idConteudo = pod.idConteudo  left join MAG_T_SITE_LU_WEBVIDEO web (nolock) on lc.idConteudo = web.idConteudo 
left join tabProduto p (nolock)
    on p.strcodigo = pod.idProdutoMestre or p.strCodigo = web.idProdutoMestre 
left join MAG_T_SITE_LU_CONTEUDO_AGENDAMENTO ad (nolock)
    on ad.idConteudo = lc.idConteudo  
left join MAG_T_SITE_GLOSS_ITEMxCONTEUDO lic (nolock)
    on lic.idConteudo = lc.idConteudo
where 
    lc.idStatus = 2 and
    (
        (ad.dtaDataInicio < getdate() and ad.dtaDataFim is null) or
        (ad.dtaDataInicio is null and ad.dtaDataFim > getdate()) or 
        (ad.dtaDataInicio < getdate() and ad.dtaDataFim > getdate()) or 
        (ad.dtaDataInicio is null and ad.dtaDataFim is null)
    )
order by
    substring(left(convert(varchar, lc.idConteudo) + '0000000', 7), 1, 3),
    lc.idConteudo 
"""
