__author__ = 'Evolutiva'
import sphinxapi
import web

from fsphinx import FSphinxClient, Facet, DBFetch, SplitOnSep
from fsphinx import QueryParser, MultiFieldQuery, RedisCache

# connect to database
db = web.database(dbn='mysql', db='powertest', user='developer', passwd='mobutu')

# let's have a cache for later use
cache = RedisCache(db=0)

# show output of mysql statements
db.printing = False

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
    SplitOnSep('organizaciones', 'relacion_empresa', 'conyuge', 'relacion_persona', 'relacion_familiar',sep='@#@')
    ]
)
cl.AttachDBFetch(db_fetch)

# give it a cache for the search and the facets
#cl.AttachCache(cache)

# setup the different facets
cl.AttachFacets(
    Facet('organizaciones', attr='organizacion_attr', sql_col='alias', sql_table='Organizacion'),
    Facet('empresas', attr='empresa_attr', sql_col='alias', sql_table='Organizacion'),
    Facet('relacion_empresa', attr='relacionEmp_attr', sql_col='relationship', sql_table='tipoRelacionP20'),
    Facet('relacion_persona', attr='relacionPers_attr', sql_col='alias', sql_table='persona'),
    Facet('relacion_familiar', attr='relacionFam_attr', sql_col='alias', sql_table='persona'),
)

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


