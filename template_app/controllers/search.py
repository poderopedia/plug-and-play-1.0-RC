# coding: utf8
__author__ = 'Evolutiva'

def podersearch():
    import pysolr
    from urllib2 import unquote

    fq=''
    if len(request.args)>1: page=int(request.args(1))
    else: page=0
    items_per_page=30
    page_start=page*items_per_page

    facetsFields = ['doc_type','pais','sector','cargostrabajo','cargosgobierno','propiedad','empresas_relacionadas',
                    'organizaciones_relacionadas','personas_relacionadas']
    facetsName=dict(cargostrabajo='Cargos en Empresa',cargosgobierno='Cargos en Gobierno',propiedad='Propiedad en Empresas',
                    sector='Sector Económico',pais='País',doc_type='Tipo Entidad',tipoOrganizacion='Institución',
                    empresas_relacionadas='Empresas Relacionadas',organizaciones_relacionadas='Organizaciones Relacionadas',
                    personas_relacionadas='Personas Relacionadas')

    search = '*:*'
    route = ''
    if request.vars['q']:
        search = unquote(request.vars['q']).decode('utf-8')
    for field in request.vars:
        if field!='q':
            #route += facetsName[field]+ ':'+ unquote(request.vars[field]).decode('utf-8')+'>'
            if '(' in unquote(request.vars[field]).decode('utf-8'):
                fq+='+'+field.decode('utf-8')+':'+unquote(request.vars[field]).decode('utf-8')
            else:
                fq+='+'+field.decode('utf-8')+':"'+unquote(request.vars[field]).decode('utf-8')+'"'
        request.vars[field]=unquote(request.vars[field]).decode('utf-8')


    solr = pysolr.Solr('http://localhost:8080/solr-poderopedia/collection1/', timeout=40)
    results = solr.search( search,facet = 'on', **{
        'hl': 'true',
        'hl.fragsize': 10,
        'start': page_start,
        'rows': items_per_page,
        'fq': fq,
        'facet.field' : facetsFields,
        'sort' : 'score desc',
        'facet.mincount': 1,
        })

    return dict(search=search,total=len(results),results=results,_id=0, page=page, fq=fq,facetsName=facetsName,
                facetsFields=facetsFields)

def visualizacion():
    import pysolr
    from urllib2 import unquote

    if len(request.args)>1: page=int(request.args(1))
    else: page=0
    items_per_page=30
    page_start=page*items_per_page

    facetsFields = ['doc_type','pais','sector','cargostrabajo','cargosgobierno','propiedad','empresas_relacionadas',
                    'organizaciones_relacionadas','personas_relacionadas']
    facetsName=dict(cargostrabajo='Cargos en Empresa',cargosgobierno='Cargos en Gobierno',propiedad='Propiedad en Empresas',
                    sector='Sector Económico',pais='País',doc_type='Tipo Entidad',tipoOrganizacion='Institución',
                    empresas_relacionadas='Empresas Relacionadas',organizaciones_relacionadas='Organizaciones Relacionadas',
                    personas_relacionadas='Personas Relacionadas')

    if request.vars['q']:
        search = unquote(request.vars['q']).decode('utf-8')
    for field in request.vars:
        if field!='q':
            #route += facetsName[field]+ ':'+ unquote(request.vars[field]).decode('utf-8')+'>'
            if '(' in unquote(request.vars[field]).decode('utf-8'):
                fq+='+'+field.decode('utf-8')+':'+unquote(request.vars[field]).decode('utf-8')
            else:
                fq+='+'+field.decode('utf-8')+':"'+unquote(request.vars[field]).decode('utf-8')+'"'
        request.vars[field]=unquote(request.vars[field]).decode('utf-8')

    solr = pysolr.Solr('http://localhost:8080/solr-poderopedia/collection1/', timeout=40)
    results = solr.search( search,facet = 'on', **{
        'hl': 'true',
        'hl.fragsize': 10,
        'start': page_start,
        'rows': items_per_page,
        'fq': fq,
        'facet.field' : facetsFields,
        'sort' : 'score desc',
        'facet.mincount': 1,
        })

    ##listas sin repeticion
    lista_nodos_persona=[]
    lista_nodos_empresa=[]
    lista_nodos_organizacion=[]

    ##enlaces
    ##links=[]
    for result in results:
        if result['doc_type']=='Persona':
            lista_nodos_persona.append(result['id'])
        if result['doc_type']=='Organizacion':
            lista_nodos_organizacion.append(result['id'])
        if result['doc_type']=='Empresas':
            lista_nodos_empresa.append(result['id'])

    ##relaciones persona a persona
    if lista_nodos_persona is not None:
        rel_persona = db((db.relPersona.origenP.belongs(lista_nodos_persona)) |
                         (db.relPersona.destinoP.belongs(lista_nodos_persona))).select()
        for relation in rel_persona:
            lista_nodos_persona.append(relation.relPersona.origenP)
            lista_nodos_persona.append(relation.relPersona.destinoP)
            links.append(dict(source='P'+str(relation.relPersona.origenP),target='P'+str(relation.relPersona.destinoP),value=10, grupo=relation.tipoRelacionP2P.name))

    return dict(search=search,total=len(results),results=results,_id=0, page=page, fq=fq,facetsName=facetsName,
                facetsFields=facetsFields)



