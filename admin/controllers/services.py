__author__ = 'Evolutiva'

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
##sidebar-persona
def relation_privateOrg():
    if request.cid==None: redirect(URL('error','error404'))
    from conversion import convert_latin_chars
    _id=request.args(0) or redirect(URL('default','index'))
    target=request.cid
    if (target==None) | (target==''):
        redirect(URL('error','error404'))

    persona=db.persona(_id)
    if persona:
        alias=convert_latin_chars(persona.alias)
    else:
        redirect(URL('error','error404'))



    Org=""; total=0;

    if len(request.args)>2: page=int(request.args[2])
    else: page=0
    items_per_page=8
    limitby=(page*items_per_page,(page+1)*items_per_page+1)

    lista=[]
    ##relPersona
    relPersonas=db(((db.relPersona.origenP==_id) | (db.relPersona.destinoP==_id)) & (db.relPersona.is_active==True) &(db.relPersona.extraO>0)).select(db.relPersona.extraO,groupby=db.relPersona.extraO,cache=(cache.ram,3600))
    for relPersona in relPersonas:
        lista.append(relPersona.extraO)

    ##relPersOrg
    relPersOrgs=db((db.RelPersOrg.is_active==True) &(db.RelPersOrg.origenP==_id)).select(db.RelPersOrg.destinoO,groupby=db.RelPersOrg.destinoO,cache=(cache.ram,3600))
    for relPersOrg in relPersOrgs:
        lista.append(relPersOrg.destinoO)



    tipoOrg=request.args(1)
    Organizationtype="Organización"


    if tipoOrg=='2':
        if lista!=[]:
            total=len(db((db.Organizacion.id.belongs(lista)) &(db.Organizacion.is_active==True) & (db.Organizacion.tipoOrg==2)).select(cache=(cache.ram,3600)))
            Org=db((db.Organizacion.id.belongs(lista)) &(db.Organizacion.is_active==True) & (db.Organizacion.tipoOrg==2)).select(
                db.Organizacion.id,db.Organizacion.alias,db.Organizacion.name,db.Organizacion.haslogo,db.Organizacion.depiction,
                db.Organizacion.tipoOrg,limitby=limitby,cache=(cache.ram,3600))
        Organizationtype="Empresa";
        controller='personas'; function='empresasrelacionadas'
    else:
        if lista!=[]:
            total=len(db((db.Organizacion.id.belongs(lista)) &(db.Organizacion.is_active==True) & (db.Organizacion.tipoOrg!=2)).select(cache=(cache.ram,3600)))
            Org=db((db.Organizacion.id.belongs(lista)) &(db.Organizacion.is_active==True) & (db.Organizacion.tipoOrg!=2)).select(
                db.Organizacion.id,db.Organizacion.alias,db.Organizacion.name,db.Organizacion.haslogo,db.Organizacion.depiction,
                db.Organizacion.tipoOrg,limitby=limitby,cache=(cache.ram,3600))
        controller='personas'; function='organizacionesrelacionadas'
    return dict(controller=controller,function=function,Org=Org,
        Organizationtype=Organizationtype,page=page,items_per_page=items_per_page,tipoOrg=tipoOrg,_id=_id,
        total=total,target=target,alias=alias)

##sidebar-persona
def relation_persona_sidebar():
    if request.cid==None: redirect(URL('error','error404'))
    from conversion import convert_latin_chars
    _id=request.args(0) or redirect(URL('default','index'))
    famrelations=[];target='sidebar_persona'; controller='personas'
    persona=db.persona(_id)
    if persona:
        alias=convert_latin_chars(persona.alias)
    else:
        redirect(URL('error','error404'))
    total=0; personas=""

    if len(request.args)>1: page=int(request.args[1])
    else: page=0

    items_per_page=8
    limitby=(page*items_per_page,(page+1)*items_per_page+1)

    lista=[]
    ##Familiar relations
    familiares=db(((db.relFamiliar.origenP==_id) | (db.relFamiliar.destinoP==_id)) &
                  (db.relFamiliar.is_active==True) ).select(
                   db.relFamiliar.origenP,db.relFamiliar.destinoP,cache=(cache.ram,3600))
    for familiar in familiares:
        select=familiar.destinoP
        if(familiar.destinoP==int(_id)):
            select=familiar.origenP
        lista.append(select)

    ##relPersona
    relPersonas=db(((db.relPersona.origenP==_id) | (db.relPersona.destinoP==_id)) &
                   (db.relPersona.is_active==True) ).select(
                    db.relPersona.origenP,db.relPersona.destinoP,cache=(cache.ram,3600))
    for relPersona in relPersonas:
        select=relPersona.destinoP
        if(relPersona.destinoP==int(_id)):
            select=relPersona.origenP
        lista.append(select)

    if lista!=[]:
        tmplista=set(lista)
        total=len(db(db.persona.id.belongs(tmplista)  &(db.persona.is_active==True)).select(cache=(cache.ram,3600)))
        personas=db((db.persona.id.belongs(tmplista))
                    &(db.persona.is_active==True)).select(limitby=limitby,cache=(cache.ram,3600))



    return dict(controller=controller,personas=personas,page=page,
        items_per_page=items_per_page,target=target,entity=famrelations,_id=_id, total=total, alias=alias)

##main content
def relation_persona():
    if request.cid==None: redirect(URL('error','error404'))
    personas=""; target='persona'
    _id=request.args(0) or redirect(URL('default','index'))
    person=db.persona(_id)
    if len(request.args)>1: page=int(request.args[1])
    else: page=0
    if len(request.args)>2: sort=request.args(2)
    else: sort='false'
    if len(request.args)>3: letter=request.args(3)
    else: letter='0'

    items_per_page=15
    limitby=(page*items_per_page,(page+1)*items_per_page+1)

    if(sort!='false'):
        reverse=False
        orderby=~db.persona.firstLastName
    else:
        reverse=True
        orderby=db.persona.firstLastName

    lista=[]; relationship={}

    ##TODO tipo relacion Inversa
    ##relPersona
    relPersona=db(((db.relPersona.origenP==_id) | (db.relPersona.destinoP==_id)) & (db.relPersona.is_active==True)).select(cache=(cache.ram,3600))
    for relation in relPersona:
        tipoRelacion=db.tipoRelacionP2P(relation.relacion)
        relacion=tipoRelacion.name
        select=relation.destinoP
        if(relation.destinoP==int(_id)):
            select=relation.origenP
        lista.append(select)
        relationship[select]=relacion


    ##familiares
    familiares=db(((db.relFamiliar.origenP==_id) | (db.relFamiliar.destinoP==_id)) & (db.relFamiliar.is_active==True) ).select(cache=(cache.ram,3600))
    for relation in familiares:
        select=relation.destinoP
        tipoRelacion=db.tipoParentesco(relation.parentesco)
        relacion=tipoRelacion.name
        if(relation.destinoP==int(_id)):
            select=relation.origenP
            relacion=tipoRelacion.nameInverso
        lista.append(select)
        relationship[select]=relacion


    ## TODO agregar letter like filter in persona.alias
    if(lista!=[]):
        personastmp = set(lista)

        if letter!='0':
            personas=db((db.persona.id.belongs(personastmp)) & (db.persona.is_active==True) & (db.persona.firstLastName.like(letter+'%'))).select(orderby=orderby,limitby=limitby,cache=(cache.ram,3600))
        else:
            personas=db((db.persona.id.belongs(personastmp)) & (db.persona.is_active==True)).select(orderby=orderby,limitby=limitby,cache=(cache.ram,3600))



    ##famrelations = sorted(famrelations, key=lambda k: k['alias'],reverse=reverse)
    return dict(relationship=relationship,personas=personas,page=page,items_per_page=items_per_page,target=target,entity=personas,_id=_id, sort=sort,person=person,letter=letter)

def relation_empresa():
    if request.cid==None: redirect(URL('error','error404'))
    _id=request.args(0) or redirect(URL('default','index'))
    empresas=""; target='relation_empresa'; tipo='Empresas';

    person=db.persona(_id)

    page=0; sort='false'; letter='0'
    if len(request.args)>1: page=int(request.args[1])
    if len(request.args)>2: sort=request.args(2)
    if len(request.args)>3: letter=request.args(3)


    items_per_page=15
    limitby=(page*items_per_page,(page+1)*items_per_page+1)

    if(sort!='false'):
        reverse=False
        orderby=~db.Organizacion.alias
    else:
        reverse=True
        orderby=db.Organizacion.alias

    lista=[]; relationship={}

    ##relPersona
    relPersonas=db(((db.relPersona.origenP==_id) | (db.relPersona.destinoP==_id)) & (db.relPersona.is_active==True)).select(cache=(cache.ram,3600))
    for relPersona in relPersonas:
        if(relPersona.extraO!=None):
            lista.append(relPersona.extraO)
            tipoRelacion=db.tipoRelacionP2P(relPersona.relacion)
            relationship[relPersona.extraO]=tipoRelacion.name

    ##relPersOrg
    relPersOrgs=db((db.RelPersOrg.origenP==_id) & (db.RelPersOrg.is_active==True)).select(cache=(cache.ram,3600))
    for relPersOrg in relPersOrgs:
        lista.append(relPersOrg.destinoO)
        tipoRelacion=db.tipoRelacionP20(relPersOrg.specificRelation)
        relationship[relPersOrg.destinoO]=tipoRelacion.relationship

    if lista!=[]:
        empresatmp=set(lista)
        if letter!='0':
            empresas=db((db.Organizacion.id.belongs(empresatmp)) & (db.Organizacion.tipoOrg==2) & (db.Organizacion.is_active==True) & (db.Organizacion.alias.like(letter+'%'))).select(orderby=orderby,limitby=limitby,cache=(cache.ram,3600))
        else:
            empresas=db((db.Organizacion.id.belongs(empresatmp)) & (db.Organizacion.tipoOrg==2) & (db.Organizacion.is_active==True)).select(orderby=orderby,limitby=limitby,cache=(cache.ram,3600))


    return dict(relationship=relationship,empresas=empresas,page=page,items_per_page=items_per_page,target=target,entity=empresas,_id=_id, sort=sort,person=person,letter=letter,tipo=tipo)

def relation_Organizacion():
    if request.cid==None: redirect(URL('error','error404'))
    empresas=""; target='relation_Organizacion'; tipo = 'Organizaciones'
    response.view='services/relation_empresa.load'
    controller='persona'; function='organizacionesrelacionadas'
    _id=request.args(0) or redirect(URL('default','index'))
    person=db.persona(_id)

    page=0; sort='false'; letter='0'
    if len(request.args)>1: page=int(request.args[1])
    if len(request.args)>2: sort=request.args(2)
    if len(request.args)>3: letter=request.args(3)


    items_per_page=15
    limitby=(page*items_per_page,(page+1)*items_per_page+1)

    if(sort!='false'):
        reverse=False
        orderby=~db.Organizacion.alias
    else:
        reverse=True
        orderby=db.Organizacion.alias

    lista=[]; relationship={}

    ##relPersona
    relPersonas=db(((db.relPersona.origenP==_id) | (db.relPersona.destinoP==_id)) & (db.relPersona.is_active==True)).select(cache=(cache.ram,3600))
    for relPersona in relPersonas:
        if(relPersona.extraO!=None):
            lista.append(relPersona.extraO)
            tipoRelacion=db.tipoRelacionP2P(relPersona.relacion)
            relationship[relPersona.extraO]=tipoRelacion.name

    ##relPersOrg
    relPersOrgs=db((db.RelPersOrg.origenP==_id) & (db.RelPersOrg.is_active==True)).select(cache=(cache.ram,3600))
    for relPersOrg in relPersOrgs:
        lista.append(relPersOrg.destinoO)
        tipoRelacion=db.tipoRelacionP20(relPersOrg.specificRelation)
        relationship[relPersOrg.destinoO]=tipoRelacion.relationship

    if lista!=[]:
        empresatmp=set(lista)
        if letter!='0':
            empresas=db((db.Organizacion.id.belongs(empresatmp)) & (db.Organizacion.tipoOrg!=2) & (db.Organizacion.is_active==True) & (db.Organizacion.alias.like(letter+'%'))).select(orderby=orderby,limitby=limitby,cache=(cache.ram,3600))
        else:
            empresas=db((db.Organizacion.id.belongs(empresatmp)) & (db.Organizacion.tipoOrg!=2) & (db.Organizacion.is_active==True)).select(orderby=orderby,limitby=limitby,cache=(cache.ram,3600))

    return dict(relationship=relationship,empresas=empresas,page=page,items_per_page=items_per_page,target=target,entity=empresas,_id=_id, sort=sort,person=person,letter=letter,tipo=tipo)



def relation_documentos():
    if request.cid==None: redirect(URL('error','error404'))
    from conversion import convert_latin_chars
    _id=request.args(0)
    target = request.vars['target'] or redirect(URL('error','error404',extension=False))
    page=0; sort='false'; letter=' '
    if len(request.args)>1: page=int(request.args[1])
    if len(request.args)>2: sort=request.args(2)
    if len(request.args)>3: letter=request.args(3)

    documentCloud=""; lista=[]

    if(target=='persona'):
        documentList=db((db.persona.id==_id) & (db.persona.is_active==True)).select(
            cache=(cache.ram,10)).first()
        if documentList==None: redirect(URL('error','error404'))
        controller='personas'
        alias=convert_latin_chars(documentList.alias)
    elif target=='organizacion':
        documentList=db((db.Organizacion.id==_id) & (db.Organizacion.is_active==True)).select(
            cache=(cache.ram,10)).first()
        if documentList==None: redirect(URL('error','error404'))
        controller='organizaciones'
        alias=convert_latin_chars(documentList.alias)
        if documentList.tipoOrg==2:
            controller='empresas'


    if documentList!=None:
        if documentList.documentCloud!=None:
                for relation in documentList.documentCloud:
                    lista.append(relation)

    if lista!=[]:
        doctmp = set(lista)
        documentCloud = db((db.documentCloud.id.belongs(doctmp)) & (db.documentCloud.is_active==True)).select(cache=(cache.ram,3600))
        #documentCloud = db((db.documentCloud.is_active==True)).select(cache=(cache.ram,3600))

    return dict(documentCloud=documentCloud,sort=sort,page=page,letter=letter,_id=_id,target=target,alias=alias,controller=controller)


##documentSource
def relation_fuentes():
    if request.cid==None: redirect(URL('error','error404'))
    _id=request.args(0) or redirect(URL('default','index'))
    if len(request.args)>1: page=int(request.args[1])
    else: page=0
    if len(request.args)>2: sort=request.args(2)
    else: sort='false'

    target='fuentesPersona';

    if(sort!='false'):
        reverse=False
        orderby=~db.document.fecha
    else:
        reverse=True
        orderby=db.document.name

    items_per_page=10
    limitby=(page*items_per_page,(page+1)*items_per_page+1)

    document=set(); documentSource={}; doctmp=[]; docos=[]
    persona=db((db.persona.id==_id)& (db.persona.is_active==True)&(db.persona.documentSource!=None)&(db.persona.documentSource!=[])).select(db.persona.documentSource,cache=(cache.ram,3600)).first()
    if persona!=None:
        doctmp.append(persona.documentSource)

    ##relFamiliar
    relFam=db(((db.relFamiliar.origenP==_id)|(db.relFamiliar.destinoP==_id))
            &(db.relFamiliar.is_active==True)&(db.relFamiliar.documentSource!=None) & (db.relFamiliar.documentSource!=[])).select(db.relFamiliar.documentSource,cache=(cache.ram,3600))
    for relation in relFam:
        doctmp.append(relation.documentSource)

    ##relPersona
    relPers=db(((db.relPersona.origenP==_id)|(db.relPersona.destinoP==_id))&(db.relPersona.is_active==True)
            &(db.relPersona.documentSource!=None) &(db.relPersona.documentSource!=[])).select(db.relPersona.documentSource,cache=(cache.ram,3600))
    for relation in relPers:
        doctmp.append(relation.documentSource)

    ##RelPersOrg
    RelPersOrg=db((db.RelPersOrg.origenP==_id)&(db.RelPersOrg.is_active==True)
            &(db.RelPersOrg.documentSource!=None) &(db.RelPersOrg.documentSource!=[])).select(db.RelPersOrg.documentSource,cache=(cache.ram,3600))
    for relation in RelPersOrg:
        doctmp.append(relation.documentSource)

    parsedDoc=[]

    for doc in doctmp:
        if doc!=[]:
            for item in doc:
                parsedDoc.append(item)

    document = set(parsedDoc)

    if(parsedDoc!=[]):
        documentSource= db(db.document.id.belongs(document)).select(orderby=orderby,limitby=limitby,cache=(cache.ram,3600))


    return dict(documentSource=documentSource,page=page,items_per_page=items_per_page,target=target,_id=_id,orderby=orderby,sort=sort)

##documentSource Organizacion
def Org_relation_fuentes():
    if request.cid==None: redirect(URL('error','error404'))
    _id=request.args(0) or redirect(URL('default','index', extension=False))
    response.view='services/relation_fuentes.load'
    if len(request.args)>1: page=int(request.args[1])
    else: page=0
    if len(request.args)>2: sort=request.args(2)
    else: sort='false'

    target='fuentesOrganizacion'

    if(sort!='false'):
        reverse=False
        orderby=~db.document.fecha
    else:
        reverse=True
        orderby=db.document.name

    items_per_page=10
    limitby=(page*items_per_page,(page+1)*items_per_page+1)

    document=set(); documentSource={}; doctmp=[]
    org=db((db.Organizacion.id==_id)& (db.Organizacion.is_active==True)&(db.Organizacion.documentSource!=None)).select(db.Organizacion.documentSource,cache=(cache.ram,10)).first()
    if org!=None:
            doctmp.append(org.documentSource)

    ##relPersona
    relPers=db((db.relPersona.extraO==_id)&(db.relPersona.is_active==True)
               &(db.relPersona.documentSource!=None)).select(db.relPersona.documentSource,cache=(cache.ram,10))
    for relation in relPers:
        doctmp.append(relation.documentSource)

    ##RelPersOrg
    RelPersOrg=db((db.RelPersOrg.destinoO==_id)&(db.RelPersOrg.is_active==True)
                  &(db.RelPersOrg.documentSource!=None)).select(db.RelPersOrg.documentSource,cache=(cache.ram,10))
    for relation in RelPersOrg:
        doctmp.append(relation.documentSource)

    ##RelOrg2Org
    relOrg2Org=db(((db.relOrg2Org.origenO==_id) | (db.relOrg2Org.destinoO==_id))
                  & (db.relOrg2Org.is_active==True) & (db.relOrg2Org.documentSource!=None)).select(db.relOrg2Org.documentSource,cache=(cache.ram,10))
    for relation in relOrg2Org:
        doctmp.append(relation.documentSource)

    parsedDoc=[]

    for doc in doctmp:
        if doc!=[]:
            for item in doc:
                parsedDoc.append(item)



    if(parsedDoc!=[]):
        document = set(parsedDoc)
        documentSource= db(db.document.id.belongs(document)).select(orderby=orderby,limitby=limitby,cache=(cache.ram,10))


    return dict(documentSource=documentSource,page=page,items_per_page=items_per_page,target=target,_id=_id,orderby=orderby,sort=sort)

def Org_relation_persona():
    if request.cid==None: redirect(URL('error','error404'))
    _id=request.args(0) or redirect(URL('default','index'))
    organizacion=db.Organizacion(_id)


    if len(request.args)>1: page=int(request.args[1])
    else: page=0
    if len(request.args)>3: letter=request.args(3)
    else: letter='0'
    items_per_page=15
    limitby=(page*items_per_page,(page+1)*items_per_page+1)

    if len(request.args)>2: sort=request.args(2)
    else: sort='false'

    target='fuentesPersona'

    if(sort!='false'):
        reverse=False
        orderby=~db.persona.alias
    else:
        reverse=True
        orderby=db.persona.alias

    target="persona"

    persontmp=[]; relationship={}; personas=""
    if(organizacion!=None):

        ##relPersona
        relPersona=db(db.relPersona.extraO==_id).select(db.relPersona.origenP,db.relPersona.relacion,db.relPersona.destinoP,
            groupby=[db.relPersona.origenP,db.relPersona.destinoP],cache=(cache.ram,3600))
        for relation in relPersona:
            persontmp.append(relation.origenP)
            persontmp.append(relation.destinoP)

            tipoRelacion=db.tipoRelacionP2P(relation.relacion)
            relationship[relation.origenP]=tipoRelacion.name
            relationship[relation.destinoP]=tipoRelacion.name

        ##relPersOrg
        relPersOrg=db((db.RelPersOrg.destinoO==_id)).select(db.RelPersOrg.origenP,db.RelPersOrg.specificRelation,groupby=db.RelPersOrg.origenP,cache=(cache.ram,3600))
        for relation in relPersOrg:
            persontmp.append(relation.origenP)
            tipoRelacion=db.tipoRelacionP20(relation.specificRelation)
            if(tipoRelacion!=None):
                relationship[relation.origenP]=tipoRelacion.relationship






        if(persontmp!=[]):
            person=set(persontmp)
            if (letter!='0') & (letter!='#'):
                personas= db(db.persona.id.belongs(person) & (db.persona.is_active==True) &(db.persona.firstLastName.like(letter+'%'))).select(orderby=orderby,limitby=limitby,cache=(cache.ram,3600))
            else:
                personas= db(db.persona.id.belongs(person) & (db.persona.is_active==True)).select(orderby=orderby,limitby=limitby,cache=(cache.ram,3600))


    return dict(letter=letter,relationship=relationship,personas=personas,page=page,items_per_page=items_per_page,_id=_id,target=target,entity=personas,organizacion=organizacion,sort=sort)

##Org to persona relation
def Org_relation_persona_sidebar():
    if request.cid==None: redirect(URL('error','error404'))
    from conversion import convert_latin_chars
    _id=request.args(0) or redirect(URL('default','index'))
    #response.view='services/relation_persona_sidebar.load'



    organizacion=db.Organizacion(_id)
    if organizacion:
        alias=convert_latin_chars(organizacion.alias)
        if organizacion.tipoOrg==2:
            controller='empresas'
        else:
            controller='organizaciones'
    else:
        redirect(URL('error','error404'))


    if len(request.args)>1: page=int(request.args[1])
    else: page=0
    items_per_page=8
    limitby=(page*items_per_page,(page+1)*items_per_page+1)

    target='sidebar_persona'
    persontmp=[]
    total=0

    ##relPersOrg
    relPersOrg=db((db.RelPersOrg.destinoO==_id)).select(db.RelPersOrg.origenP,groupby=db.RelPersOrg.origenP,cache=(cache.ram,3600))
    for relation in relPersOrg:
        persontmp.append(relation.origenP)

    ##relPersona
    relPersona=db(db.relPersona.extraO==_id).select(db.relPersona.origenP,db.relPersona.destinoP,groupby=[db.relPersona.origenP,db.relPersona.destinoP],cache=(cache.ram,3600))
    for relation in relPersona:
        persontmp.append(relation.origenP)
        persontmp.append(relation.destinoP)

    person=set(persontmp)

    personas=""
    if(persontmp!=[]):
        total=len(db(db.persona.id.belongs(person)).select(cache=(cache.ram,3600)))
        personas= db(db.persona.id.belongs(person)).select(limitby=limitby,cache=(cache.ram,3600))

    return dict(controller=controller,total=total, personas=personas,limitby=limitby,
        items_per_page=items_per_page,page=page,target=target,_id=_id,alias=alias)

def Org_relation_organizacion():
    if request.cid==None: redirect(URL('error','error404'))
    _id=request.args(0) or redirect(URL('default','index'))
    organizaciones=""
    organizacion=db.Organizacion(_id)

    if len(request.args)>1: page=int(request.args[1])
    else: page=0
    if len(request.args)>2: sort=request.args(2)
    else: sort='false'
    if len(request.args)>3: letter=request.args(3)
    else: letter='0'

    items_per_page=15
    limitby=(page*items_per_page,(page+1)*items_per_page+1)

    target='Org_relation_organizacion'

    if(sort!='false'):
        reverse=False
        orderby=~db.Organizacion.alias
    else:
        reverse=True
        orderby=db.Organizacion.alias

    organizaciontmp=[]; relationship={}

    ##relOrg2Org
    relOrg2Org=db(((db.relOrg2Org.origenO==_id) | (db.relOrg2Org.destinoO==_id)) &(db.relOrg2Org.is_active==True)).select(cache=(cache.ram,10))
    for relation in relOrg2Org:
        select=relation.destinoO
        tipoRelacion=db.tipoRelacionOrg2Org(relation.relationOrg)
        relacion=''
        if relation.relationOrg:
            relacion=tipoRelacion.name
        if(relation.destinoO==int(_id)):
            select=relation.origenO
            if relation.relationOrg:
                relacion=tipoRelacion.inverse
        organizaciontmp.append(select)
        relationship[select]=relacion

    if organizaciontmp!=[]:
        setOrgs=set(organizaciontmp)
        if (letter!=' ') & (letter!='0'):
            organizaciones=db((db.Organizacion.id.belongs(setOrgs)) &(db.Organizacion.tipoOrg!=2)& (db.Organizacion.is_active==True) & (db.Organizacion.alias.like(letter+'%'))).select(orderby=orderby,limitby=limitby,cache=(cache.ram,3600))
        else:
            organizaciones=db((db.Organizacion.id.belongs(setOrgs)) &(db.Organizacion.tipoOrg!=2)& (db.Organizacion.is_active==True)).select(orderby=orderby,limitby=limitby,cache=(cache.ram,3600))

    return dict(letter=letter,relationship=relationship,organizaciones=organizaciones,page=page,items_per_page=items_per_page,_id=_id,target=target,entity=organizaciones,organizacion=organizacion,sort=sort)

def Org_relation_empresa():
    if request.cid==None: redirect(URL('error','error404'))
    _id=request.args(0) or redirect(URL('default','index'))
    response.view='services/Org_relation_organizacion.load'
    organizaciones=""
    organizacion=db.Organizacion(_id)

    if len(request.args)>1: page=int(request.args[1])
    else: page=0
    if len(request.args)>2: sort=request.args(2)
    else: sort='false'
    if len(request.args)>3: letter=request.args(3)
    else: letter='0'

    items_per_page=15
    limitby=(page*items_per_page,(page+1)*items_per_page+1)

    target='Org_relation_empresa'

    if(sort!='false'):
        reverse=False
        orderby=~db.Organizacion.alias
    else:
        reverse=True
        orderby=db.Organizacion.alias

    organizaciontmp=[]; relationship={}

    ##relOrg2Org
    relOrg2Org=db(((db.relOrg2Org.origenO==_id) | (db.relOrg2Org.destinoO==_id)) &(db.relOrg2Org.is_active==True)).select(cache=(cache.ram,3600))
    for relation in relOrg2Org:
        select=relation.destinoO
        tipoRelacion=db.tipoRelacionOrg2Org(relation.relationOrg)
        relacion=''
        if relation.relationOrg:
            relacion=tipoRelacion.name
        if(relation.destinoO==int(_id)):
            select=relation.origenO
            if relation.relationOrg:
                relacion=tipoRelacion.inverse
        organizaciontmp.append(select)
        relationship[select]=relacion

    if organizaciontmp!=[]:
        setOrgs=set(organizaciontmp)
        if letter!='0':
            organizaciones=db((db.Organizacion.id.belongs(setOrgs)) &(db.Organizacion.tipoOrg==2)& (db.Organizacion.is_active==True) & (db.Organizacion.alias.like(letter+'%'))).select(orderby=orderby,limitby=limitby,cache=(cache.ram,3600))
        else:
            organizaciones=db((db.Organizacion.id.belongs(setOrgs)) &(db.Organizacion.tipoOrg==2)& (db.Organizacion.is_active==True)).select(orderby=orderby,limitby=limitby,cache=(cache.ram,3600))

    return dict(letter=letter,relationship=relationship,organizaciones=organizaciones,page=page,items_per_page=items_per_page,_id=_id,target=target,entity=organizaciones,organizacion=organizacion,sort=sort)
##organization to private / non profit Organization
def Org_relation_privateOrg():
    if request.cid==None: redirect(URL('error','error404'))
    from conversion import convert_latin_chars
    _id=request.args(0) or redirect(URL('default','index'))
    if _id<0: redirect(URL('default','index'))
    response.view='services/relation_privateOrg.load'



    organizacion=db.Organizacion(_id)
    if organizacion:
        alias=convert_latin_chars(organizacion.alias)
        if organizacion.tipoOrg==2:
            controller='empresas'
        else:
            controller='organizaciones'
    else:
        redirect(URL('error','error404'))



    if len(request.args)>2: page=int(request.args[2])
    else: page=0
    items_per_page=8
    limitby=(page*items_per_page,(page+1)*items_per_page+1)

    tipoOrg=request.args(1)
    Organizationtype="Organización"
    target="organizacion"

    lista=[];
    Org=db((db.relOrg2Org.destinoO==_id)|(db.relOrg2Org.origenO==_id)).select(db.relOrg2Org.destinoO,db.relOrg2Org.origenO)
    for relation in Org:
        select=relation.destinoO
        if relation.destinoO==int(_id):
            select=relation.origenO
        lista.append(select)

    if tipoOrg=='2':
        total=len(db((db.Organizacion.id.belongs(lista))&(db.Organizacion.tipoOrg==2)).select(cache=(cache.ram,3600)))
        Org=db((db.Organizacion.id.belongs(lista))&(db.Organizacion.tipoOrg==2)).select(limitby=limitby,cache=(cache.ram,3600))
        Organizationtype="Empresa"; target="empresa"
        function='empresasrelacionadas'
    else:
        total=len(db((db.Organizacion.id.belongs(lista))&(db.Organizacion.tipoOrg!=2)).select(cache=(cache.ram,3600)))
        Org=db((db.Organizacion.id.belongs(lista))&(db.Organizacion.tipoOrg!=2)).select(limitby=limitby,cache=(cache.ram,3600))
        function='organizacionesrelacionadas'

    return dict(controller=controller,function=function,Org=Org,Organizationtype=Organizationtype,
        page=page,items_per_page=items_per_page,tipoOrg=tipoOrg,_id=_id,total=total,target=target,alias=alias)

##Organization 2 person relation


##most popular
def mas_popular():
    if request.cid==None: redirect(URL('error','error404'))
    from conversion import convert_latin_chars
    result=[]; active={}; args=''
    active['hoy']=active['semana']=active['mes']=''
    imagen=None
    function='conexiones'
    if request.args(0)=='portada':
        active['hoy']='active'
        query=(db.plugin_stats.dia==request.now)
        if request.args(1)=='month':
            active['mes']='active'; active['hoy']=''
            query=(db.plugin_stats.month==int(request.now.strftime('%m')))& (db.plugin_stats.year==request.now.strftime('%Y'))
        elif request.args(1)=='week':
            active['semana']='active'; active['hoy']=''
            query=(db.plugin_stats.week==int(request.now.strftime('%W')))& (db.plugin_stats.year==request.now.strftime('%Y'))
        sum = db.plugin_stats.hits.sum()
        popular=db(db.plugin_stats.page_key.like('%conexiones%') & query).select(db.plugin_stats.hits,db.plugin_stats.page_key,sum,
            orderby=~sum,limitby=(0,5),groupby=db.plugin_stats.page_key,cache=(cache.ram,3600))

        response.view='services/mas_visto.load'
    else:
        popular=db((db.plugin_stats.page_key.like('%conexiones%')) & (db.plugin_stats.dia==request.now)).select(
            orderby=~db.plugin_stats.hits,limitby=(0,4),cache=(cache.ram,3600))

    for most in popular:
        if request.args(0)=='portada':
            page=most.plugin_stats.page_key.split('/')
            page_key=most.plugin_stats.page_key
        else:
            page=most.page_key.split('/')
            page_key=most.page_key
        largo=len(page)
        if 'personas' in page_key:
            if page[largo-1]:
                alias= page[largo-1].decode('utf-8').replace('_',' ')
                entity=db.persona(alias=alias, is_active=True)
                if entity!=None:
                    imagen=IMG(_alt=entity.alias,_src=URL('static','tmp/imagen-face.gif'), _width='140')
                    if (entity.depiction!=None) & (entity.depiction!=''):
                        imagen=IMG(_alt=entity.alias,_src=URL('default','fast_download',args=entity.depiction),
                                   _class='imagen-perfil-ch', _width='140')
                    args=convert_latin_chars(entity.alias)
                    alias=entity.alias
                controller='personas';
        elif ('organizaciones' in page_key) | ('empresas' in page_key):
            alias= page[largo-1].decode('utf-8').replace('_',' ').replace('-','.')
            entity=db.Organizacion(alias=alias,is_active=True)
            if entity!=None:
                imagen=IMG(_alt=entity.alias,_src=URL('static','tmp/avatar-organizacion45.gif'),
                           _class='imagen-perfil-ch', _width='100')
                controller='organizaciones'
                alias=entity.alias
                if entity.tipoOrg==2:
                    controller='empresas'
                    imagen=IMG(_alt=entity.alias,_src=URL('static','tmp/avatar-empresa.png'), _width='100')
                if (entity.haslogo!=None) & (entity.haslogo!=''):
                    imagen=IMG(_alt=entity.alias,_src=URL('default','fast_download',args=entity.haslogo),
                               _class='imagen-perfil-ch', _width='90', _heigth='80')
                args=convert_latin_chars(entity.alias)



        shortBio=''
        if entity!=None:
            if entity.shortBio!=None:
                shortBio=entity.shortBio
        else:
            redirect(URL('error','error404'))

        result.append(dict(alias=alias,c=controller,f=function,args=args,imagen=imagen,shortBio=shortBio))

    return dict(popular=result, active=active)


def mas_popular_rss():
    from conversion import convert_latin_chars


    entradas=[]
    resultados=dict(
        title="Más Popular Hoy | Poderopedia",
        link="http://www.poderopedia.org",
        description="Poderopedia | Más Popular",
        created_on=str(request.now)
    )
    query=(db.plugin_stats.month==int(request.now.strftime('%m')))& (db.plugin_stats.year==request.now.strftime('%Y'))
    sum = db.plugin_stats.hits.sum()
    popular=db(db.plugin_stats.page_key.like('%conexiones%') & query).select(db.plugin_stats.hits,db.plugin_stats.page_key,sum,
                             orderby=~sum,limitby=(0,2),groupby=db.plugin_stats.page_key,cache=(cache.ram,3600))

    for most in popular:
        page=most.plugin_stats.page_key.split('/')
        page_key=most.plugin_stats.page_key
        largo=len(page)
        if 'personas' in page_key:
            if page[largo-1]:
                alias= page[largo-1].decode('utf-8').replace('_',' ')
                entity=db.persona(alias=alias, is_active=True)
                if entity!=None:
                    imagen=URL('static','tmp/imagen-face.gif')
                    if (entity.depiction!=None) & (entity.depiction!=''):
                        imagen=URL('default','fast_download',args=entity.depiction)

                    args=convert_latin_chars(entity.alias)
                    alias=entity.alias
                controller='personas';
        elif ('organizaciones' in page_key) | ('empresas' in page_key):
            alias= page[largo-1].decode('utf-8').replace('_',' ').replace('-','.')
            entity=db.Organizacion(alias=alias,is_active=True)
            if entity!=None:
                imagen=URL('static','tmp/avatar-organizacion45.gif')

                controller='organizaciones'
                alias=entity.alias
                if entity.tipoOrg==2:
                    controller='empresas'
                    imagen=URL('static','tmp/avatar-empresa.png')
                if (entity.haslogo!=None) & (entity.haslogo!=''):
                    imagen=URL('default','fast_download',args=entity.haslogo)

                args=convert_latin_chars(entity.alias)

        media=dict(url='http://'+request.env.http_host + imagen,medium='image',width='140')
        results=dict(title=alias,link=URL(controller,'conexiones',args=args, extension=False),
                     description=entity.shortBio[:184], created_on=entity.modified_on)
        results['media:content']=media
        entradas.append(results)
    resultados['entries']=entradas
    response.headers['Content-Type']='application/rss+xml'

    return dict(resultados=resultados,title='Más Popular Ahora',desc='Lo más popular en Poderopedia')


def destacados_rss():
    ini = int(request.args(0) or 0)
    end = int(request.args(1) or 10)
    response.view='services/mas_popular_rss.html'
    entradas=[]
    resultados=dict(
        title="Poderopedia ",
        link="http://www.poderopedia.org",
        description="Poderopedia RSS",
        created_on=str(request.now)
    )
    destacados = db(db.destacados.is_active==True).select(orderby=~db.destacados.fecha,limitby=(ini,end),cache=(cache.ram,3600))
    for news in destacados:
        imagen='http://'+request.env.http_host + URL('default','fast_download',args=news.imagen)
        media=dict(url=imagen,medium='image',width='120', height='78')
        results=dict(title=news.titulo,link=news.url,description=news.contenido[:127],created_on=news.fecha)
        results['media:content']=media
        entradas.append(results)
    resultados['entries']=entradas
    response.headers['Content-Type']='application/rss+xml'
    return dict(resultados=resultados,title='Destacados',desc='Destacados en Poderopedia')

def lo_ultimo_rss():
    from conversion import convert_latin_chars
    response.view='services/mas_popular_rss.html'
    entradas=[]
    resultados=dict(
        title="Poderopedia ",
        link="http://www.poderopedia.org",
        description="Poderopedia | Lo último",
        created_on=request.now
    )
    personas = db((db.persona.is_active==True) & (db.persona.shortBio!=None) & (db.persona.shortBio!='')
                  & (db.persona.depiction!=None) & (db.persona.depiction!='')).select(
        db.persona.alias,db.persona.shortBio,db.persona.depiction,db.persona.modified_on,
        orderby=[~db.persona.modified_on],limitby=(0,2))

    for persona in personas:
        imagen=URL('static','tmp/imagen-face.gif')
        if persona.depiction!='':
            imagen=URL('default','fast_download',args=persona.depiction)
        media=dict(url='http://'+request.env.http_host + imagen,medium='image',width='140')
        results=dict(title=persona.alias,link=URL('personas','conexiones',args=convert_latin_chars(persona.alias)),
                     description=persona.shortBio[:184],created_on=persona.modified_on)
        results['media:content']=media
        entradas.append(results)

    organizacion = db((db.Organizacion.is_active==True) & (db.Organizacion.shortBio!=None) & (db.Organizacion.shortBio!='')
                      & (db.Organizacion.haslogo!=None) & (db.Organizacion.haslogo!='')).select(
        db.Organizacion.id,db.Organizacion.tipoOrg,
        db.Organizacion.alias,db.Organizacion.shortBio,db.Organizacion.haslogo,db.Organizacion.modified_on,
        orderby=[~db.Organizacion.modified_on],limitby=(0,2))

    for org in organizacion:
        args=convert_latin_chars(org.alias)
        imagen=URL('static','tmp/avatar-organizacion45.gif')
        link=URL('organizaciones','conexiones',args=args)
        if org.tipoOrg==2:
            imagen=URL('static','tmp/avatar-empresa.png')
            link=URL('empresas','conexiones',args=args)
        if org.haslogo!='':
            imagen=URL('default','fast_download',args=org.haslogo)
        media=dict(url='http://'+request.env.http_host + imagen,medium='image',width='140')
        results=dict(title=org.alias,link=link,description=org.shortBio[:184],created_on=org.modified_on)
        results['media:content']=media
    entradas.append(results)
    entradas=sorted(entradas, key=lambda k: k['created_on'], reverse=True)
    resultados['entries']=entradas
    response.headers['Content-Type']='application/rss+xml'
    return dict(resultados=resultados,title='Lo ültimo',desc='Últimas actualizaciones en Poderopedia')




