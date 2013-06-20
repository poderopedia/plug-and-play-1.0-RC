# coding: utf8
def download(): return response.download(request,db)
def index(): return dict(message="hello from busqueda.py")
def call(): return service()


def resultadogeneral():
    return dict(_id=1,page=0, sort=0, target=0, entity=0)


def facetedsearch():
    from gluon.custom_import import track_changes; track_changes(True)
    import sphinxapi
    import fsphinx
    from fsphinx.sphinx import FSphinxClient
    from fsphinx.cache import RedisCache
    import fsphinx.utils
    from fsphinx.facets import Facet
    from fsphinx.queries import QueryParser, MultiFieldQuery
    #from gluon.contrib.redis_cache import RedisCache

    searchquery=request.args(0)

    ##
    ##cl = FSphinxClient.FromConfig('c:\web2py2\web2py\applications\poderopedia\private\sphinx_client.py')


    #import MySQLdb
    #import web


    #from fsphinx import FSphinxClient, Facet, DBFetch, SplitOnSep
    #from fsphinx import QueryParser, MultiFieldQuery, RedisCache

    # connect to database
    #data = web.database(dbn='mysql', db='powertest', user='developer', passwd='mobutu')

    # let's have a cache for later use
    cache = RedisCache(db=0)

    # show output of mysql statements
    #db2.printing = False

    # create sphinx client
    cl = FSphinxClient()

    # connect to searchd
    cl.SetServer('localhost', 9312)

    # matching mode (faceted client should be SPH_MATCH_EXTENDED2)
    cl.SetMatchMode(sphinxapi.SPH_MATCH_EXTENDED2)

    # sorting and possible custom sorting function
    #cl.SetSortMode(sphinxapi.SPH_SORT_EXPR, '@weight * user_rating_attr * nb_votes_attr * year_attr / 100000')

    # set the default index to search
    cl.SetDefaultIndex('items')

    # some fields could matter more than others
    cl.SetFieldWeights({'alias' : 30})
    cl.SetFieldWeights({'empresas' : 30})
    cl.SetFieldWeights({'organizaciones' : 30})

    ##cl.AttachDBFetch(db)


    # give it a cache for the search and the facets
    #cl.AttachCache(cache)

    organizaciones=Facet('organizaciones', attr='organizacion_attr', sql_col='alias', sql_table='Organizacion')
    empresas=Facet('empresas', attr='empresa_attr', sql_col='alias', sql_table='Organizacion')
    relacion_empresa=Facet('relacion_empresa', attr='relacionEmp_attr', sql_col='relationship', sql_table='tipoRelacionP20')
    relacion_persona=Facet('relacion_persona', attr='relacionPers_attr', sql_col='alias', sql_table='persona')
    relacion_familiar=Facet('relacion_familiar', attr='relacionFam_attr', sql_col='alias', sql_table='persona')

    organizaciones.AttachSphinxClient(cl, db)
    empresas.AttachSphinxClient(cl,db)
    relacion_empresa.AttachSphinxClient(cl,db)
    relacion_persona.AttachSphinxClient(cl,db)
    relacion_familiar.AttachSphinxClient(cl,db)

    # setup the different facets
    #cl.AttachFacets(
    #    organizaciones,
    #    empresas,
    #    relacion_empresa,
    #    relacion_persona,
    #    relacion_familiar,
    #)

    # for all facets compute count, groupby and this score


    # setup sorting and ordering of each facet
    for f in cl.facets:
        #f.SetGroupFunc(group_func)
        # order the term alphabetically within each facet
        f.SetOrderBy('@term')

    # the query should always be parsed beforehand
    query_parser = QueryParser(MultiFieldQuery, user_sph_map={
        'organizaciones' : 'organizacion',
        'empresas' : 'empresa',
        'relacion_empresa' : 'cargos',
        'relacion_persona' : 'personas_relacionadas',
        'relacion_familiar' : 'familiares'
    })
    cl.AttachQueryParser(query_parser)

    cl.SetSortMode(sphinxapi.SPH_SORT_RELEVANCE)
    cl.Query(searchquery)
    cl.AddQuery(searchquery,'organizaciones')
    cl.AddQuery(searchquery,'empresas')
    cl.AddQuery(searchquery,'relacion_empresa')
    cl.AddQuery(searchquery,'relacion_persona')
    cl.AddQuery(searchquery,'relacion_familiar')
    resultsAll=cl.RunQueries()
    results=cl.query
    facets=cl.facets
    hits=cl.hits

    return dict(results=results,facets=facets,hits=hits,resultsAll=resultsAll,_id=1,page=0, sort=0, target=0, entity=0)

def podersearch():
    from gluon.custom_import import track_changes; track_changes(True)
    import sphinxapi
    import fsphinx
    #from fsphinx import *
    from fsphinx.facets import Facet
    from fsphinx.hits import DBFetch, SplitOnSep
    from fsphinx.sphinx import FSphinxClient
    from fsphinx.cache import RedisCache
    #from fsphinx.utils import storage

    from fsphinx.queries import QueryParser, MultiFieldQuery
    #from gluon.contrib.redis_cache import RedisCache

    searchquery="chile"
    if request.vars['search']: searchquery=request.vars['search']
    filter=request.vars['filter']
    term=request.vars['term']

    #'@year 1999 @genre drama @actor harrison ford'
    queryEmpresas='@empresas '+searchquery.decode('utf-8')
    queryOrgs='@organizaciones '+searchquery.decode('utf-8')
    #queryEmpresas=None; queryOrgs=None;
    query=searchquery.decode('utf-8')
    if (filter!=None) & (term!=None):
        query=(query+' @'+filter+' '+term.decode('utf-8'))
        queryEmpresas=queryEmpresas+' @'+filter+' '+term.decode('utf-8')
        #queryEmpresas='@'+filter+' '+term.decode('utf-8')
        queryOrgs=queryOrgs+' @'+filter+' '+term.decode('utf-8')
        #queryOrgs='@'+filter+' '+term.decode('utf-8')
    ##
    ##cl = FSphinxClient.FromConfig('c:\web2py2\web2py\applications\poderopedia\private\sphinx_client.py')




    # let's have a cache for later use
    #cache = RedisCache(db=0)

    # show output of mysql statements
    #db2.printing = False

    # create sphinx client
    cl = FSphinxClient()

    # connect to searchd
    cl.SetServer('localhost', 9312)

    # matching mode (faceted client should be SPH_MATCH_EXTENDED2)
    #cl.SetRankingMode ( sphinxapi.SPH_RANK_PROXIMITY_BM25 )
    # matching mode (faceted client should be SPH_MATCH_EXTENDED2)
    cl.SetMatchMode(sphinxapi.SPH_MATCH_EXTENDED2)

    # sorting and possible custom sorting function
    #cl.SetSortMode(sphinxapi.SPH_SORT_EXPR, '@weight * user_rating_attr * nb_votes_attr * year_attr / 100000')

    # set the default index to search
    cl.SetDefaultIndex('items')

    # some fields could matter more than others
    cl.SetFieldWeights({'alias' : 30})
    cl.SetFieldWeights({'empresas' : 30})
    cl.SetFieldWeights({'organizaciones' : 30})

    # some fields could matter more than others
    #   cl.SetFieldWeights({'alias' : 30})

    #

    # sql query to fetch the hits
    db_fetch = DBFetch(db, sql = '''
        select id, ICN, firstName, firstLastName, otherLastName, alias, shortBio, longBio, isDead, web, twitterNick, facebookNick, linkedinNick,
        (select group_concat(distinct name separator '@#@') from country c where c.id=p.countryofResidence) as pais,
        (select group_concat(distinct relationship separator '@#@') from RelPersOrg as r, tipoRelacionP20 as t where r.origenP=p.id and r.specificRelation=t.id and t.generalizacion='Propiedad' and r.is_active='T') as propiedad,
        (select group_concat(distinct relationship separator '@#@') from RelPersOrg as r, tipoRelacionP20 as t where r.origenP=p.id and r.specificRelation=t.id and t.generalizacion is null and t.parent=3 and r.is_active='T') as cargos_gobierno,
        (select group_concat(distinct relationship separator '@#@') from RelPersOrg as r, tipoRelacionP20 as t where r.origenP=p.id and r.specificRelation=t.id and t.generalizacion is null and t.parent!=3 and t.parent!=1 and t.parent!=4 and parent!=11 and r.is_active='T') as cargos_trabajo,
        (select group_concat(distinct o.alias separator '@#@') from RelPersOrg as r, Organizacion as o where r.origenP=p.id and r.destinoO=o.id and o.tipoOrg!=2 and o.tipoOrg!=1 and o.tipoOrg!=1 and o.tipoOrg!=4 and o.tipoOrg!=5 and o.tipoOrg!=6 and o.tipoOrg!=8 and r.is_active='T' and o.is_active='T') as organizaciones,
        (select group_concat(distinct o.alias separator '@#@') from RelPersOrg as r, Organizacion as o where r.origenP=p.id and r.destinoO=o.id and o.tipoOrg=1 and r.is_active='T' and o.is_active='T') as estudios,
        (select group_concat(distinct o.alias separator '@#@') from RelPersOrg as r, Organizacion as o where r.origenP=p.id and r.destinoO=o.id and o.tipoOrg=2 and r.is_active='T' and o.is_active='T') as empresas,
        (select group_concat(distinct o.alias separator '@#@') from RelPersOrg as r, Organizacion as o where r.origenP=p.id and r.destinoO=o.id and o.tipoOrg=4 and r.is_active='T' and o.is_active='T') as partidos,
        (select group_concat(distinct o.alias separator '@#@') from RelPersOrg as r, Organizacion as o where r.origenP=p.id and r.destinoO=o.id and o.tipoOrg=5 and r.is_active='T' and o.is_active='T') as religion,
        (select group_concat(distinct o.alias separator '@#@') from RelPersOrg as r, Organizacion as o where r.origenP=p.id and r.destinoO=o.id and o.tipoOrg=6 and r.is_active='T' and o.is_active='T') as clubes,
        (select group_concat(distinct o.alias separator '@#@') from RelPersOrg as r, Organizacion as o where r.origenP=p.id and r.destinoO=o.id and o.tipoOrg=8 and r.is_active='T' and o.is_active='T') as grupos_apoyo,
        (select group_concat(distinct s.alias separator '@#@') from relPersona as r, tipoRelacionP2P as t, persona as s where r.origenP=p.id and r.destinoP=s.id and r.relacion=t.id and t.parent=1) as conyuge,
        (select group_concat(distinct s.alias separator '@#@') from relPersona as r, tipoRelacionP2P as t, persona as s where r.origenP=p.id and r.destinoP=s.id and r.relacion=t.id and t.parent!=1) as relacion_persona,
        (select group_concat(distinct s.alias separator '@#@') from relFamiliar as r, persona as s where r.origenP=p.id and r.destinoP=s.id) as relacion_familiar
        from persona p
        where p.is_active='T' and id in ($id)
        order by field(id, $id)''', post_processors = [
        SplitOnSep('pais','propiedad','cargos_gobierno','cargos_trabajo','organizaciones','estudios','empresas','partidos','religion','clubes','grupos_apoyo','conyuge','relacion_persona','relacion_familiar',sep='@#@')
    ]
    )
    cl.AttachDBFetch(db_fetch)

    pais=Facet('pais', attr='pais_attr', sql_col='name', sql_table='country')
    propiedad=Facet('propiedad', attr='propiedad_attr', sql_col='relationship', sql_table='tipoRelacionP20')
    cargos_gobierno=Facet('cargos_gobierno', attr='cargos_gobierno_attr', sql_col='relationship', sql_table='tipoRelacionP20')
    cargos_trabajo=Facet('cargos_trabajo', attr='cargos_trabajo_attr', sql_col='relationship', sql_table='tipoRelacionP20')
    organizaciones=Facet('organizaciones', attr='organizaciones_attr', sql_col='alias', sql_table='Organizacion')
    estudios=Facet('estudios', attr='estudios_attr', sql_col='alias', sql_table='Organizacion')
    empresas=Facet('empresas', attr='empresas_attr', sql_col='alias', sql_table='Organizacion')
    partidos=Facet('partidos', attr='partidos_attr', sql_col='alias', sql_table='Organizacion')
    religion=Facet('religion', attr='religion_attr', sql_col='alias', sql_table='Organizacion')
    clubes=Facet('clubes', attr='clubes_attr', sql_col='alias', sql_table='Organizacion')
    grupos_apoyo=Facet('grupos_apoyo', attr='grupos_apoyo_attr', sql_col='alias', sql_table='Organizacion')
    conyuge=Facet('conyuge', attr='conyuge_attr', sql_col='alias', sql_table='persona')
    relacion_persona=Facet('relacion_persona', attr='relacion_persona_attr', sql_col='alias', sql_table='persona')
    relacion_familiar=Facet('relacion_familiar', attr='relacion_familiar_attr', sql_col='alias', sql_table='persona')

    # setup the different facets
    cl.AttachFacets(
        organizaciones,
        empresas,
        pais,
        propiedad,
        cargos_gobierno,
        cargos_trabajo,
        estudios,
        partidos,
        religion,
        clubes,
        grupos_apoyo,
        conyuge,
        relacion_persona,
        relacion_familiar,
    )

    # give it a cache for the search and the facets
    #cl.AttachCache(cache)



    # for all facets compute count, groupby and this score


    # setup sorting and ordering of each facet
    for f in cl.facets:
        #f.SetGroupFunc(group_func)
        # order the term alphabetically within each facet
        #f.SetOrderBy('@term')
        f.SetOrderBy('@count')

    # the query should always be parsed beforehand
    query_parser = QueryParser(MultiFieldQuery, user_sph_map={
        'organizaciones':'organizaciones',
        'empresas':'empresas',
        'pais':'pais',
        'propiedad':'propiedad',
        'cargos_gobierno':'cargos_gobierno',
        'cargos_trabajo':'cargos_trabajo',
        'estudios':'estudios',
        'partidos':'partidos',
        'religion':'religion',
        'clubes':'clubes',
        'grupos_apoyo':'grupos_apoyo',
        'organizaciones' : 'organizaciones',
        'empresas' : 'empresas',
        'conyuge': 'conyuge',
        'relacion_persona': 'relacion_persona',
        'relacion_familiar':'relacion_familiar',
    })
    cl.AttachQueryParser(query_parser)


    ##cl.SetSortMode(sphinxapi.SPH_SORT_RELEVANCE)
    ##cl.AddQuery(searchquery,'organizaciones')
    ##cl.AddQuery(searchquery,'empresas')
    ##cl.AddQuery(searchquery,'relacion_empresa')
    ##cl.AddQuery(searchquery,'relacion_persona')
    ##cl.AddQuery(searchquery,'relacion_familiar')
    ##resultsAll=cl.RunQueries()

    addEmpresa=[]
    if queryEmpresas:
        cl.Query(queryEmpresas)
        hits=cl.hits
        if hits.total_found>0:
            for empresa in empresas:
                if empresa['@selected']==True:
                    emp=db.Organizacion(empresa['@groupby'])
                    imagen=emp.haslogo
                    if imagen:
                        html=IMG(_src=URL('download',args=imagen),_alt=emp.alias,_width="50")
                    else:
                        html=IMG(_src=URL('static','tmp/avatarempresa.png'),_alt=emp.alias, _width="50")
                    addEmpresa.append(dict(id=empresa['@groupby'],alias=emp.alias,picture=html))

    if queryOrgs:
        cl.Query(queryOrgs)
        hits=cl.hits
        if hits.total_found>0:
            for org in organizaciones:
                if org['@selected']==True:
                    organiz=db.Organizacion(org['@groupby'])
                    imagen=organiz.haslogo
                    if imagen:
                        html=IMG(_src=URL('download',args=imagen),_alt=organiz.alias,_width="50")
                    else:
                        html=IMG(_src=URL('static','img/icono-organizaciones.png'),_alt=organiz.alias, _width="50")
                    addEmpresa.append(dict(id=org['@groupby'],alias=organiz.alias,picture=html))

    #hits = db_fetch.Fetch(results)
    cl.Query(query)
    results=cl.query
    facets=cl.facets
    hits=cl.hits
    person={}
    for match in hits:
        if '@hit' in match:
            persona=db.persona(match['@hit']['id'])
            imagen=persona.depiction
            if imagen:
                html=IMG(_src=URL('download',args=imagen),_alt=match['@hit']['alias'],_width="50")
            else:
                html=IMG(_src=URL('static','tmp/avatar-45.gif'),_alt=match['@hit']['alias'])
            person[match['@hit']['id']]=html

    items_per_page=19
    letter='0'

    nomFacetas=['Organizaciones','Empresas','Pais','Propiedad','Cargos de Gobierno','Cargos Privados','Estudios','Partidos','Religion','Clubes Privados','Grupos de Apoyo','Conyuge','Amigos y Conocidos','Familiar']




    return dict(addEmpresa=addEmpresa,searchquery=searchquery, nomFacetas=nomFacetas, results=results,facets=facets,hits=hits,_id=1,page=0, sort=0, target=0, entity=[1],items_per_page=items_per_page,letter=letter, person=person)

@service.json
def service_search():
    import sphinxapi
    import fsphinx
    #from fsphinx import *
    from fsphinx.facets import Facet
    from fsphinx.hits import DBFetch, SplitOnSep
    from fsphinx.sphinx import FSphinxClient
    from fsphinx.cache import RedisCache
    #from fsphinx.utils import storage

    from fsphinx.queries import QueryParser, MultiFieldQuery
    #from gluon.contrib.redis_cache import RedisCache

    searchquery=request.args(0)
    ##
    ##cl = FSphinxClient.FromConfig('c:\web2py2\web2py\applications\poderopedia\private\sphinx_client.py')



    # let's have a cache for later use
    cache = RedisCache(db=0)

    # show output of mysql statements
    #db2.printing = False

    # create sphinx client
    cl = FSphinxClient()

    # connect to searchd
    cl.SetServer('localhost', 9312)

    # matching mode (faceted client should be SPH_MATCH_EXTENDED2)
    cl.SetMatchMode(sphinxapi.SPH_MATCH_EXTENDED2)

    # sorting and possible custom sorting function
    #cl.SetSortMode(sphinxapi.SPH_SORT_EXPR, '@weight * user_rating_attr * nb_votes_attr * year_attr / 100000')

    # set the default index to search
    cl.SetDefaultIndex('items')

    # some fields could matter more than others
    cl.SetFieldWeights({'alias' : 30})

    #

    # sql query to fetch the hits
    db_fetch = DBFetch(db, sql = '''
            select id, ICN, firstName, firstLastName, otherLastName, alias, shortBio, longBio, isDead, web, twitterNick, facebookNick, linkedinNick,
            (select group_concat(distinct o.alias separator '@#@') from RelPersOrg as r, Organizacion as o where r.origenP=p.id and r.destinoO=o.id and o.tipoOrg!=2) as organizaciones,
            (select group_concat(distinct o.alias separator '@#@') from RelPersOrg as r, Organizacion as o where r.origenP=p.id and r.destinoO=o.id and o.tipoOrg=2) as empresas,
            (select group_concat(distinct relationship separator '@#@') from RelPersOrg as r, tipoRelacionP20 as t where r.origenP=p.id and r.specificRelation=t.id) as relacion_empresa,
            (select group_concat(distinct s.alias separator '@#@') from relPersona as r, tipoRelacionP2P as t, persona as s where r.origenP=p.id and r.destinoP=s.id and r.relacion=t.id and t.parent=1) as conyuge,
            (select group_concat(distinct s.alias separator '@#@') from relPersona as r, tipoRelacionP2P as t, persona as s where r.origenP=p.id and r.destinoP=s.id and r.relacion=t.id and t.parent!=1) as relacion_persona,
            (select group_concat(distinct s.alias separator '@#@') from relFamiliar as r, persona as s where r.origenP=p.id and r.destinoP=s.id) as relacion_familiar
            from persona p
            where p.is_active='T' and id in ($id)
            order by field(id, $id)''', post_processors = [
        SplitOnSep('organizaciones', 'empresas','relacion_empresa', 'conyuge', 'relacion_persona', 'relacion_familiar',sep='@#@')
    ]
    )
    cl.AttachDBFetch(db_fetch)

    organizaciones=Facet('organizaciones', attr='organizaciones_attr', sql_col='alias', sql_table='Organizacion')
    empresas=Facet('empresas', attr='empresas_attr', sql_col='alias', sql_table='Organizacion')
    relacion_empresa=Facet('relacion_empresa', attr='relacion_empresa_attr', sql_col='relationship', sql_table='tipoRelacionP20')
    relacion_persona=Facet('relacion_persona', attr='relacion_persona_attr', sql_col='alias', sql_table='persona')
    relacion_familiar=Facet('relacion_familiar', attr='relacion_familiar_attr', sql_col='alias', sql_table='persona')

    # setup the different facets
    cl.AttachFacets(
        organizaciones,
        empresas,
        relacion_empresa,
        relacion_persona,
        relacion_familiar,
    )

    # give it a cache for the search and the facets
    cl.AttachCache(cache)



    # for all facets compute count, groupby and this score


    # setup sorting and ordering of each facet
    for f in cl.facets:
        #f.SetGroupFunc(group_func)
        # order the term alphabetically within each facet
        #f.SetOrderBy('@term')
        f.SetOrderBy('@count')

    # the query should always be parsed beforehand
    query_parser = QueryParser(MultiFieldQuery, user_sph_map={
        'organizaciones' : 'organizaciones',
        'empresas' : 'empresas',
        'relacion_empresa' : 'relacion_empresa',
        'relacion_persona' : 'relacion_persona',
        'relacion_familiar' : 'relacion_familiar'
    })
    cl.AttachQueryParser(query_parser)


    cl.facets.Compute(searchquery)
    cl.Query(searchquery)
    results=cl.query
    facets=cl.facets
    hits=cl.hits


    return dict(hits=hits)
