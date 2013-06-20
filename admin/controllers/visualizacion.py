# -*- coding: utf-8 -*-
# cache resolved
def call(): return service()

def download(): return response.download(request,db)


def caso_organizacion():
    from conversion import convert_latin_chars
    url =request.env.http_host + request.env.request_uri
    _id=request.args(0) or redirect(URL('default','index'))

    organizacion=db.Organizacion(_id)


    db.Organizacion.id.readable=False
    db.Organizacion.haslogo.readable=False
    db.Organizacion.depiction.readable=False
    db.Organizacion.documentSource.readable=False
    db.Organizacion.shortBio.readable=False
    db.Organizacion.longBio.readable=False
    db.Organizacion.documentCloud.readable=False

    for fields in db.Organizacion:
        if (organizacion[fields]==None) | (organizacion[fields]=='') | (organizacion[fields]==False) | (organizacion[fields]==[])\
           | (organizacion[fields]=='NULL'):
            fields.readable=False
        fields.writable=False
    form=SQLFORM(db.Organizacion,organizacion)
    form['_class']='form-horizontal'
    submit = form.element('input',_type='submit')
    submit['_style'] = 'display:none;'

    borrar=auth.has_membership('administrator')

    return dict(Organizacion=organizacion, _id=_id, form=form, borrar=borrar, url=url )

def caso_perfil():
    from conversion import convert_latin_chars
    url =request.env.http_host + request.env.request_uri
    person=db.persona(request.args(0)) or redirect(URL('error','error404'))

    #redirect(URL('personas','conexiones',args=convert_latin_chars(person.alias)))

    _id=request.args(0)
    db.persona.id.readable=False
    db.persona.ICN.readable=False
    db.persona.shortBio.readable=False
    db.persona.longBio.readable=False
    db.persona.depiction.readable=False
    db.persona.documentSource.readable=False
    db.persona.documentCloud.readable=False
    for fields in db.persona:
        if (person[fields]==None) | (person[fields]=='') | (person[fields]==False) | (person[fields]==[])\
           | (person[fields]=='NULL'):
            fields.readable=False
        fields.writable=False
    form=SQLFORM(db.persona,person)
    form['_class']='form-horizontal'
    submit = form.element('input',_type='submit')
    submit['_style'] = 'display:none;'


    borrar=auth.has_membership('administrator')


    return dict(persona=person, _id=request.args(0), form=form, borrar=borrar, url=url )

#hay que construir caso_caso ya que hasta la fecha no hay casos ingresados al sistema
def caso_caso():
    return dict(_id=1,page=0, sort=0, target=0, entity=0)

def familia():
    _id=request.args(0) or redirect(URL('default','index'))

    editar=auth.has_membership('editor')
    borrar=auth.has_membership('administrator')
    doctmp=[]
    ##Origen
    parientes=db((db.relFamiliar.origenP==_id) & (db.relFamiliar.parentesco==db.tipoParentesco.id)
                 & (db.relFamiliar.is_active==True) &
                 (db.relFamiliar.destinoP==db.persona.id) & (db.persona.is_active==True)).select(
        db.relFamiliar.id,db.tipoParentesco.name,db.persona.alias,db.relFamiliar.destinoP,db.relFamiliar.documentSource,
        cache=(cache.ram,3600))
    for relation in parientes:
        doctmp.append(relation.relFamiliar.documentSource)
    ##Destino
    parientesD=db((db.relFamiliar.destinoP==_id) & (db.relFamiliar.parentesco==db.tipoParentesco.id)
                  & (db.relFamiliar.is_active==True) &
                  (db.relFamiliar.origenP==db.persona.id) & (db.persona.is_active==True)).select(
        db.relFamiliar.id,db.tipoParentesco.nameInverso,db.persona.alias,db.relFamiliar.origenP,
        db.relFamiliar.documentSource, cache=(cache.ram,3600))
    for relation in parientesD:
        doctmp.append(relation.relFamiliar.documentSource)

    parsedDoc=[]

    for doc in doctmp:
        if (doc!=[]) & (doc!=None):
            for item in doc:
                parsedDoc.append(item)

    documentSource={}
    if(parsedDoc!=[]):
        document_set = set(parsedDoc)
        for item in document_set:
            documentSource[item]= db(db.document.id==item).select(cache=(cache.ram,3600)).first()

    return dict(parientes=parientes,parientesD=parientesD,editar=editar,borrar=borrar,documentSource=documentSource)

def conyuge():
    import time
    from datetime import date
    _id=request.args(0) or redirect(URL('default','index'))
    borrar=auth.has_membership('administrator')
    editar=auth.has_membership('editar')
    doctmp=[]



    conyugesO=db((db.relPersona.origenP==_id) &
                 (db.relPersona.relacion==db.tipoRelacionP2P.id)& (db.relPersona.is_active==True) &
                 (db.tipoRelacionP2P.parent==1) &
                 (db.relPersona.destinoP==db.persona.id) & (db.persona.is_active==True)
    ).select(cache=(cache.ram,3600))

    for relation in conyugesO:
        doctmp.append(relation.relPersona.documentSource)

    conyugesD=db((db.relPersona.destinoP==_id) &
                 (db.relPersona.relacion==db.tipoRelacionP2P.id)& (db.relPersona.is_active==True) &
                 (db.tipoRelacionP2P.parent==1) &
                 (db.relPersona.origenP==db.persona.id) & (db.persona.is_active==True)
    ).select(cache=(cache.ram,3600))
    for relation in conyugesD:
        doctmp.append(relation.relPersona.documentSource)

    parsedDoc=[]

    for doc in doctmp:
        if (doc!=[]) & (doc!=None):
            for item in doc:
                parsedDoc.append(item)

    documentSource={}
    if(parsedDoc!=[]):
        document_set = set(parsedDoc)
        for item in document_set:
            documentSource[item]= db(db.document.id==item).select(cache=(cache.ram,3600)).first()

    return dict(conyugesO=conyugesO,conyugesD=conyugesD,borrar=borrar,editar=editar,hoy=date.today(), documentSource=documentSource)

def comp_estudios():
    import time
    from datetime import date
    persona={}
    _id=request.args(0) or redirect(URL('default','index'))
    try:
        _id=int(_id)
    except Error:
        redirect(URL('error','error404',extension=False))

    borrar=auth.has_membership('administrator')
    editar=auth.has_membership('editar')
    doctmp=[]

    conexiones=db(((db.relPersona.origenP==_id) | (db.relPersona.destinoP==_id)) &
                  (db.relPersona.relacion==db.tipoRelacionP2P.id)& (db.relPersona.is_active==True) &
                  (db.relPersona.relacion==32) &
                  (db.relPersona.destinoP==db.persona.id) & (db.persona.is_active==True) &
                  (db.relPersona.extraO==db.Organizacion.id)
                ).select(cache=(cache.ram,3600))

    for relation in conexiones:
        person_id=relation.relPersona.origenP
        if _id==relation.relPersona.origenP:
            person_id=relation.relPersona.destinoP
        persona[relation.relPersona.id]=db.persona(person_id)
        if persona[relation.relPersona.id].is_active==False:
            persona[relation.relPersona.id]=None
        doctmp.append(relation.relPersona.documentSource)

    parsedDoc=[]
    for doc in doctmp:
        if (doc!=[]) & (doc!=None):
            for item in doc:
                parsedDoc.append(item)

    documentSource={}
    if(parsedDoc!=[]):
        document_set = set(parsedDoc)
        for item in document_set:
            documentSource[item]= db(db.document.id==item).select(cache=(cache.ram,3600)).first()


    return dict(borrar=borrar, editar=editar,hoy=date.today(), documentSource=documentSource,
                conexiones=conexiones, persona=persona, largo=len(conexiones))

def relPersona():
    import time
    from datetime import date
    _id=request.args(0) or redirect(URL('default','index'))
    borrar=auth.has_membership('administrator')
    editar=auth.has_membership('editor')
    conexionO={}; conexionD={}; selectP2P={}
    ##parents relPersona
    parentsP2P=db((db.tipoRelacionP2P.parent==0) & (db.tipoRelacionP2P.id!=1)).select(cache=(cache.ram,3600))

    Org={}
    orgs=db( ((db.relPersona.origenP==_id) | (db.relPersona.destinoP==_id)) & (db.relPersona.extraO==db.Organizacion.id)
             &(db.relPersona.is_active==True) & (db.Organizacion.is_active==True)).select(groupby=db.relPersona.extraO,cache=(cache.ram,3600))
    for org in orgs:
        Org[org.relPersona.extraO]=org.Organizacion.alias
        ##rel Persona a Persona
    doctmp=[]
    for parents in parentsP2P:
        conexionO[parents.name]=db((db.relPersona.origenP==_id) &
                                   (db.relPersona.relacion==db.tipoRelacionP2P.id) &(db.relPersona.is_active==True) &
                                   (db.tipoRelacionP2P.parent==parents.id) &
                                   (db.relPersona.destinoP==db.persona.id) & (db.persona.is_active==True)).select(
                                    cache=(cache.ram,3600))
        for relation in conexionO[parents.name]:
            doctmp.append(relation.relPersona.documentSource)
        conexionD[parents.name]=db((db.relPersona.destinoP==_id) &
                                   (db.relPersona.relacion==db.tipoRelacionP2P.id) &(db.relPersona.is_active==True) &
                                   (db.tipoRelacionP2P.parent==parents.id) &
                                   (db.relPersona.origenP==db.persona.id) & (db.persona.is_active==True)).select(
                                    cache=(cache.ram,3600))
        for relation in conexionD[parents.name]:
            doctmp.append(relation.relPersona.documentSource)

        selectP2P[parents.id]=parents.name

    parsedDoc=[]

    for doc in doctmp:
        if (doc!=[]) & (doc!=None):
            for item in doc:
                parsedDoc.append(item)

    documentSource={}
    if(parsedDoc!=[]):
        document_set = set(parsedDoc)
        for item in document_set:
            documentSource[item]= db(db.document.id==item).select(cache=(cache.ram,3600)).first()

    return dict(selectP2P=selectP2P,conexionO=conexionO, conexionD=conexionD,borrar=borrar, editar=editar,
        Org=Org,hoy=date.today(), documentSource=documentSource)

def relOrgs():
    import time
    from datetime import date


    _id=request.args(0) or redirect(URL('default','index'))
    ##parents relPersona Organizacion
    parentsP20=db(db.tipoRelacionP20.parent==0).select(cache=(cache.ram,3600),orderby='orden')
    borrar=auth.has_membership('administrator')
    editar=auth.has_membership('editor')



    P2O={}; seleccionP20={}
    hoy = date.today(); doctmp=[]
    ## rel Persona a Organización
    for parents in parentsP20:
        P2O[parents.relationship]=db((db.RelPersOrg.is_active==True)&(db.RelPersOrg.origenP==_id) & (db.RelPersOrg.destinoO==db.Organizacion.id) &
                                     (db.RelPersOrg.specificRelation==db.tipoRelacionP20.id) & (db.Organizacion.is_active==True) &
                                     (db.tipoRelacionP20.parent==parents.id)).select(cache=(cache.ram,15))
        for relation in P2O[parents.relationship]:
            doctmp.append(relation.RelPersOrg.documentSource)
        seleccionP20[parents.id]=parents.relationship

    parsedDoc=[]

    for doc in doctmp:
        if (doc!=[]) & (doc!=None):
            for item in doc:
                parsedDoc.append(item)

    documentSource={}
    if(parsedDoc!=[]):
        document_set = set(parsedDoc)
        for item in document_set:
            documentSource[item]= db(db.document.id==item).select(cache=(cache.ram,3600)).first()

    return dict(P2O=P2O, seleccionP20=seleccionP20, parentsP20=parentsP20, borrar=borrar,editar=editar,hoy=hoy,
        documentSource=documentSource)

def rows():
    rows=db(db.persona).select().as_list()
    if rows:
        for row in rows:
            for field in row[0].keys():
                table=TABLE(*[TR(TH(field),*[TD(row[field])])\
                     ])
    else:
        table="nothing to see here"
    return dict(table=table)

def gridFamiliar():
    grid=SQLFORM.grid(db.persona)
    return dict(grid=grid)

@service.json
def get_persona_relfamiliar_id(id):
    lista = []; visual={}
    rows = db((db.persona.id==id)&(db.persona.is_active==True)).select()
    if(rows!=None):
        for row in rows:
            listaparents=[]
            for parents in db(db.relFamiliar.origenP==row.id).select():
                destino = db.persona[parents.destinoP]
                relation = db.tipoParentesco[parents.parentesco]
                node={'id':parents.destinoP,'name':destino.alias, 'data':{'name':'isParent','relation':relation.name}}
                listaparents.append(node)
            children={'children':listaparents, 'data':{'name':'hasParents','relation':'Familiar'}, 'name':row.alias, 'id':row.id}
            lista.append(children)
            visual =  { 'name':row.alias,'children':lista, 'data':{'name':'work at','relation':'member political institution'},'id':row.id}
    return visual

@auth.requires_membership('editor')
@auth.requires_membership('administrator')
def persona():
    table=SQLFORM.grid(db.relFamiliar)
    return dict(table=table)

##TODO
def relPersona_Organizacion():
    import datetime
    import time
    hoy = str(datetime.date.today())
    _id=request.args(0) or redirect(URL('default','index'))
    parentsP2P=db((db.tipoRelacionP2P.parent==0) & (db.tipoRelacionP2P.id!=1)).select(cache=(cache.ram,3600))
    borrar=auth.has_membership('administrator')
    relationship={}; personas=None
    for parents in parentsP2P:
        lista=[]
        #relPersona
        relPersona=db( (db.relPersona.extraO==_id) & (db.relPersona.is_active==True) & (db.relPersona.relacion==db.tipoRelacionP2P.id) & (db.tipoRelacionP2P.parent==parents.id)).select(cache=(cache.ram,3600))
        for relation in relPersona:
            lista.append(relation.relPersona.origenP)
            lista.append(relation.relPersona.destinoP)
        if(lista!=[]):
            setlista=set(lista)
            personas=db((db.persona.id.belongs(setlista)) & (db.persona.is_active==True)).select(cache=(cache.ram,3600))
            relationship[parents.name]=personas

    return dict(relationship=relationship,parentsP2P=parentsP2P,borrar=borrar,_id=_id,hoy=hoy)


def relOrgs_Organizacion():
    import datetime
    import time
    hoy = datetime.date.today()
    _id=request.args(0) or redirect(URL('default','index'))
    ##parents relPersona Organizacion
    parentsP20=db(db.tipoRelacionP20.parent==0).select(cache=(cache.ram,3600))
    borrar=auth.has_membership('administrator')

    P2O={}; seleccionP20={}; doctmp=[]
    ## rel Persona a Organización
    for parents in parentsP20:
        #P2O[parents.inverse]=db((db.RelPersOrg.is_active==True)&(db.RelPersOrg.destinoO==_id) & (db.RelPersOrg.origenP==db.persona.id) &
        #                             (db.RelPersOrg.specificRelation==db.tipoRelacionP20.id) & (db.persona.is_active==True) &
        #                             (db.tipoRelacionP20.parent==parents.id)).select(cache=(cache.ram,3600))
        P2O[parents.id]=db((db.RelPersOrg.is_active==True)&(db.RelPersOrg.destinoO==_id) & (db.RelPersOrg.origenP==db.persona.id) &
                                (db.RelPersOrg.specificRelation==db.tipoRelacionP20.id) & (db.persona.is_active==True) &
                                (db.tipoRelacionP20.parent==parents.id)).select()
        for relation in P2O[parents.id]:
            doctmp.append(relation.RelPersOrg.documentSource)
        seleccionP20[parents.id]=parents.inverse

    parsedDoc=[]

    for doc in doctmp:
        if (doc!=[]) & (doc!=None):
            for item in doc:
                parsedDoc.append(item)

    documentSource={}
    if(parsedDoc!=[]):
        document_set = set(parsedDoc)
        for item in document_set:
            documentSource[item]= db(db.document.id==item).select(cache=(cache.ram,10)).first()

    return dict(P2O=P2O, seleccionP20=seleccionP20, parentsP20=parentsP20, borrar=borrar,hoy=hoy,documentSource=documentSource)

def Orgs2_Organizacion():
    _id=request.args(0) or redirect(URL('default','index'))
    parentsO2O=db((db.tipoRelacionOrg2Org.parent==0)).select(cache=(cache.ram,10))
    borrar=auth.has_membership('administrator')
    relationship={}; orgs=None; lista=[]; doctmp=[]
    for parents in parentsO2O:
        relationTuple=[]
        #relPersona
        relOrgs=db( ((db.relOrg2Org.origenO==_id) | ((db.relOrg2Org.destinoO==_id))) & (db.relOrg2Org.is_active==True) & (db.relOrg2Org.relationOrg==db.tipoRelacionOrg2Org.id) & (db.tipoRelacionOrg2Org.parent==parents.id)).select(cache=(cache.ram,10))
        #relOrgs=db( ((db.relOrg2Org.origenO==_id) | ((db.relOrg2Org.destinoO==_id))) & (db.relOrg2Org.is_active==True) & (db.relOrg2Org.relationOrg==db.tipoRelacionOrg2Org.id) & (db.tipoRelacionOrg2Org.parent==parents.id)).select()
        for relation in relOrgs:
            append=relation.relOrg2Org.destinoO
            link=db.tipoRelacionOrg2Org(relation.relOrg2Org.relationOrg)
            relacion=link.name
            if relation.relOrg2Org.destinoO==int(_id):
                append=relation.relOrg2Org.origenO
                relacion=link.inverse
            org=db.Organizacion(append)
            if org.is_active==True:
                lista.append(append)
                relationTuple.append((append,relacion,relation.relOrg2Org.documentSource,relation.relOrg2Org.fdesde,relation.relOrg2Org.fhasta,relation.relOrg2Org.isPast))
                doctmp.append(relation.relOrg2Org.documentSource)

        relationship[parents.name]=relationTuple

    if(lista!=[]):
        setlista=set(lista)
        orgs={}
        organizaciones=db((db.Organizacion.id.belongs(setlista)) & (db.Organizacion.is_active==True)).select(cache=(cache.ram,10))
        #organizaciones=db((db.Organizacion.id.belongs(setlista)) & (db.Organizacion.is_active==True)).select()
        for org in organizaciones:
            orgs[org.id]=org.alias

    parsedDoc=[]
    for doc in doctmp:
        if (doc!=[]) & (doc!=None):
            for item in doc:
                parsedDoc.append(item)

    documentSource={}
    if(parsedDoc!=[]):
        document_set = set(parsedDoc)
        for item in document_set:
            documentSource[item]= db(db.document.id==item).select(cache=(cache.ram,10)).first()


    return dict(relationship=relationship,parentsO2O=parentsO2O,organizacion=orgs,
        borrar=borrar,_id=_id,documentSource=documentSource)

##person 2 person nodes and links
@service.json
def person2person(_id=0):
    nodes=[]; links=[]; PersonID={}
    num = db.relPersona.origenP.count()
    if(_id!=0):
        relPersona=db(db.relPersona.is_active==True).select(db.relPersona.origenP,db.relPersona.destinoP,num,
            groupby=[db.relPersona.origenP,db.relPersona.destinoP],cache=(cache.ram,3600))

        for relation in relPersona:
            selSource=relation.relPersona.origenP
            selTarget=relation.relPersona.destinoP
            PersonID[selSource]=None
            PersonID[selTarget]=None

        relPersona=db((db.relPersona.is_active==True) & ((db.relPersona.origenP==_id) | (db.relPersona.destinoP==_id))).select(db.relPersona.origenP,db.relPersona.destinoP,num,
            groupby=[db.relPersona.origenP,db.relPersona.destinoP],cache=(cache.ram,3600))
        i=0

        for relation in relPersona:
            selSource=relation.relPersona.origenP
            selTarget=relation.relPersona.destinoP

            personas=db(((db.persona.id==selSource) | (db.persona.id==selTarget))
                        & (db.persona.is_active==True)).select(cache=(cache.ram,3600))
            if personas!=None:
                if(PersonID[selSource]==None):
                    PersonID[selSource]=i;
                    persona=db.persona(selSource)
                    nodes.append(dict(alias=persona.alias,shortbio=persona.shortBio))
                    i=i+1
                    relPersonaNewSource=db((db.relPersona.is_active==True) & ((db.relPersona.origenP==selSource) | (db.relPersona.destinoP==selSource))).select(db.relPersona.origenP,db.relPersona.destinoP,num,
                        groupby=[db.relPersona.origenP,db.relPersona.destinoP],cache=(cache.ram,3600))
                    for sourceRelation in relPersonaNewSource:
                        selSourceNew=sourceRelation.relPersona.origenP
                        selTargetNew=sourceRelation.relPersona.destinoP
                        personas=db(((db.persona.id==selSourceNew) | (db.persona.id==selTargetNew))
                                    & (db.persona.is_active==True)).select(cache=(cache.ram,3600))
                        if personas!=None:
                            if(PersonID[selSourceNew]==None):
                                PersonID[selSourceNew]=i;
                                persona=db.persona(selSourceNew)
                                nodes.append(dict(alias=persona.alias,shortbio=persona.shortBio))
                                i=i+1
                            if(PersonID[selTargetNew]==None):
                                PersonID[selTargetNew]=i
                                persona=db.persona(selTargetNew)
                                nodes.append(dict(alias=persona.alias,shortbio=persona.shortBio))
                                i=i+1
                            source=PersonID[selSourceNew]; target=PersonID[selTargetNew]
                            links.append(dict(source=source,target=target,value=int(sourceRelation[num]*10)))

                if(PersonID[selTarget]==None):
                    PersonID[selTarget]=i
                    persona=db.persona(selTarget)
                    nodes.append(dict(alias=persona.alias,shortbio=persona.shortBio))
                    i=i+1
                    relPersonaNewSource=db((db.relPersona.is_active==True) & ((db.relPersona.origenP==selTarget) | (db.relPersona.destinoP==selTarget))).select(db.relPersona.origenP,db.relPersona.destinoP,num,
                        groupby=[db.relPersona.origenP,db.relPersona.destinoP],cache=(cache.ram,3600))
                    for sourceRelation in relPersonaNewSource:
                        selSourceNew=sourceRelation.relPersona.origenP
                        selTargetNew=sourceRelation.relPersona.destinoP
                        personas=db(((db.persona.id==selSourceNew) | (db.persona.id==selTargetNew))
                                    & (db.persona.is_active==True)).select(cache=(cache.ram,3600))
                        if personas!=None:
                            if(PersonID[selSourceNew]==None):
                                PersonID[selSourceNew]=i;
                                persona=db.persona(selSourceNew)
                                nodes.append(dict(alias=persona.alias,shortbio=persona.shortBio))
                                i=i+1
                            if(PersonID[selTargetNew]==None):
                                PersonID[selTargetNew]=i
                                persona=db.persona(selTargetNew)
                                nodes.append(dict(alias=persona.alias,shortbio=persona.shortBio))
                                i=i+1
                            source=PersonID[selSourceNew]; target=PersonID[selTargetNew]
                            links.append(dict(source=source,target=target,value=int(sourceRelation[num]*10)))

                source=PersonID[selSource]; target=PersonID[selTarget]
                links.append(dict(source=source,target=target,value=int(relation[num]*10)))



    else:
        relPersona=db(db.relPersona.is_active==True).select(db.relPersona.origenP,db.relPersona.destinoP,num,
            groupby=[db.relPersona.origenP,db.relPersona.destinoP],cache=(cache.ram,3600))
        i=0
        for relation in relPersona:
            selSource=relation.relPersona.origenP
            selTarget=relation.relPersona.destinoP
            PersonID[selSource]=None
            PersonID[selTarget]=None

        for relation in relPersona:
            selSource=relation.relPersona.origenP
            selTarget=relation.relPersona.destinoP

            personas=db(((db.persona.id==selSource) | (db.persona.id==selTarget))
                      & (db.persona.is_active==True)).select(cache=(cache.ram,3600))
            if personas!=None:
                if(PersonID[selSource]==None):
                    PersonID[selSource]=i;
                    persona=db.persona(selSource)
                    nodes.append(dict(alias=persona.alias,shortbio=persona.shortBio))
                    i=i+1
                ##TODO
                if(PersonID[selTarget]==None):
                    PersonID[selTarget]=i
                    persona=db.persona(selTarget)
                    nodes.append(dict(alias=persona.alias,shortbio=persona.shortBio))
                    i=i+1
                source=PersonID[selSource]; target=PersonID[selTarget]
                links.append(dict(source=source,target=target,value=relation[num]))

    return dict(nodes=nodes,links=links)


##
##nodes: [
#           { name: "alias"
#             group: "entity_name"
#             id: "unique_id"
#             num: "level_importance"
#           }
# ]
##
##
@service.json
def persona2all(_id=0):
    from conversion import convert_latin_chars
    from collections import Counter

    nodes=[]; links=[]; PersonID={}; listaNodosPersona=[]; listaNodosOrgs=[]

    if id!=0:
        listaNodosPersona.append(_id)
        relFamiliar=db(((db.relFamiliar.origenP==_id) | (db.relFamiliar.destinoP==_id)) & (db.relFamiliar.is_active==True)
                       & (db.relFamiliar.parentesco==db.tipoParentesco.id)
                       & (db.relFamiliar.origenP==db.persona.id) & (db.persona.is_active==True)
        ).select(
            db.relFamiliar.origenP,db.relFamiliar.destinoP, db.tipoParentesco.name,
            cache=(cache.ram,3600)
        )
        for relation in relFamiliar:
            person=db(db.persona.id==relation.relFamiliar.destinoP).select(cache=(cache.ram,3600)).first()
            if person.is_active:
                listaNodosPersona.append(relation.relFamiliar.origenP)
                listaNodosPersona.append(relation.relFamiliar.destinoP)
                links.append(dict(
                    source='P'+str(relation.relFamiliar.origenP),
                    target='P'+str(relation.relFamiliar.destinoP),
                    value="1",
                    grupo='Familiar'
                ))
        ##person2person
        num = db.relPersona.origenP.count()
        relPersona=db((db.relPersona.is_active==True) & ((db.relPersona.origenP==_id) | (db.relPersona.destinoP==_id))
                      & (db.relPersona.relacion==db.tipoRelacionP2P.id)).select(
                            db.relPersona.origenP,db.relPersona.destinoP,num,db.tipoRelacionP2P.name,
                            groupby=[db.relPersona.origenP,db.relPersona.destinoP],cache=(cache.ram,3600))
        for relation in relPersona:
            listaNodosPersona.append(relation.relPersona.origenP)
            listaNodosPersona.append(relation.relPersona.destinoP)
            links.append(dict(source='P'+str(relation.relPersona.origenP),target='P'+str(relation.relPersona.destinoP),value=relation[num], grupo=relation.tipoRelacionP2P.name))
        #if listaNodosPersona!=[]:
        #    listatmp=set(listaNodosPersona)
            ##segundo nivel
        #    relPersona2=db((db.relPersona.is_active==True) & (db.relPersona.relacion==db.tipoRelacionP2P.id) & ((db.relPersona.origenP.belongs(listatmp)) | (db.relPersona.destinoP.belongs(listatmp)))).select(db.relPersona.origenP,db.relPersona.destinoP,num,db.tipoRelacionP2P.parent,
        #        groupby=[db.relPersona.origenP,db.relPersona.destinoP],cache=(cache.ram,3600))
        #    for relation in relPersona2:
        #       listaNodosPersona.append(relation.relPersona.origenP)
        #        listaNodosPersona.append(relation.relPersona.destinoP)
        #        links.append(dict(source='P'+str(relation.relPersona.origenP),target='P'+str(relation.relPersona.destinoP),value=relation[num],grupo='P2P'+str(relation.tipoRelacionP2P.parent)))

        num=db.RelPersOrg.origenP.count()
        rel2Orgs=db((db.RelPersOrg.origenP==_id) & (db.RelPersOrg.is_active==True) &
                    (db.RelPersOrg.specificRelation==db.tipoRelacionP20.id) &
                    (db.RelPersOrg.destinoO==db.Organizacion.id) &
                    (db.Organizacion.is_active==True)).select(
                        db.RelPersOrg.origenP,db.RelPersOrg.destinoO,num,db.tipoRelacionP20.relationship,
                        groupby=[db.RelPersOrg.origenP,db.RelPersOrg.destinoO],cache=(cache.ram,3600))
        for relation in rel2Orgs:
            listaNodosOrgs.append(relation.RelPersOrg.destinoO)
            links.append(dict(source='P'+str(relation.RelPersOrg.origenP),target='O'+str(relation.RelPersOrg.destinoO),value=relation[num],grupo=relation.tipoRelacionP20.relationship))
        #if listaNodosOrgs!=[]:
        #    listatmp=set(listaNodosOrgs)
        #    rel2Orgs=db((db.RelPersOrg.destinoO.belongs(listatmp)) & (db.RelPersOrg.specificRelation==db.tipoRelacionP20.id) &(db.RelPersOrg.is_active==True)).select(db.RelPersOrg.origenP,db.RelPersOrg.destinoO,num,
        #        db.tipoRelacionP20.parent,groupby=[db.RelPersOrg.origenP,db.RelPersOrg.destinoO],cache=(cache.ram,3600))
        #    for relation in rel2Orgs:
        #        listaNodosPersona.append(relation.RelPersOrg.origenP)
        #        listaNodosOrgs.append(relation.RelPersOrg.destinoO)
        #        links.append(dict(source='P'+str(relation.RelPersOrg.origenP),target='O'+str(relation.RelPersOrg.destinoO),value=relation[num],grupo='P20'+str(relation.tipoRelacionP20.parent)))
        #    num=db.relOrg2Org.origenO.count()
        #    relOrg2Orgs=db((db.relOrg2Org.is_active==True) & (db.relOrg2Org.relationOrg==db.tipoRelacionOrg2Org.id) & ((db.relOrg2Org.origenO.belongs(listatmp)) | (db.relOrg2Org.destinoO.belongs(listatmp)))).select(db.relOrg2Org.origenO,db.relOrg2Org.destinoO,num,
        #        db.tipoRelacionOrg2Org.parent, groupby=[db.relOrg2Org.origenO,db.relOrg2Org.destinoO],cache=(cache.ram,3600))
        #    for relation in relOrg2Orgs:
        #        listaNodosOrgs.append(relation.relOrg2Org.origenO)
        #        listaNodosOrgs.append(relation.relOrg2Org.destinoO)
        #        links.append(dict(source='O'+str(relation.relOrg2Org.origenO),target='O'+str(relation.relOrg2Org.destinoO),value=relation[num],grupo='O2O'+str(relation.tipoRelacionOrg2Org.parent)))



        if listaNodosPersona!=[]:
            c = Counter(listaNodosPersona)
            listatmp=set(listaNodosPersona)
            personas= db((db.persona.id.belongs(listatmp))).select(cache=(cache.ram,3600))
            for persona in personas:
                root='false'
                relevance=56
                imagen=URL('static','img/icono-persona56.png')
                shortBio=''
                if persona.depiction:
                    imagen=URL('default','fast_download',args=persona.depiction)
                if persona.shortBio:
                    shortBio=persona.shortBio.decode('utf-8')[:180]+'...'
                if persona.id==int(_id):
                    relevance=56
                    root='true'
                nodes.append(dict(name=persona.alias,shortBio=shortBio,group='persona',id="P"+str(persona.id),relevance=relevance,url=URL('personas','conexiones',args=convert_latin_chars(persona.alias)),root=root,imagen=imagen))

        if listaNodosOrgs!=[]:
            c = Counter(listaNodosOrgs)
            listatmp=set(listaNodosOrgs)
            orgs=db((db.Organizacion.is_active==True) & (db.Organizacion.id.belongs(listatmp))).select(cache=(cache.ram,3600))
            for org in orgs:
                imagen=URL('static','img/icono-organizaciones56.png')
                shortBio=''
                url=URL('organizaciones','conexiones',args=convert_latin_chars(org.alias))
                if org.tipoOrg==2:
                    imagen=URL('static','img/icono-empresas56.png')
                    group1='empresa'
                    url=URL('empresas','conexiones',args=convert_latin_chars(org.alias))
                else:
                    group1='organizacion'
                if org.haslogo:
                    imagen=URL('default','fast_download',args=org.haslogo)
                if org.shortBio:
                    shortBio=org.shortBio.decode('utf-8')[:180]+'...'
                #relevance=c[org.id]*100
                relevance=56
                nodes.append(dict(name=org.alias,shortBio=shortBio,group=group1, id="O"+str(org.id),relevance=relevance,url=url,root='false',imagen=imagen))

        #relPerOrgs=db((db.RelPersOrg.is_active==True) ).select()
    return dict(nodes=nodes,links=links)

@service.json
def orgs2all(_id=0,user_key='xxxxxxxx'):
    """

    :param _id:
    :return:
    """
    cid=request.cid or redirect(URL('error','error404.load'))
    from collections import Counter
    from conversion import convert_latin_chars
    error='OK'
    provider_key = 'c1f18606c752b4942771205b16a01249'
    #app_id = 'f8395cf0'
    #app_key = 'dd88190daab4754b60b77c5db71b4e96'
    nodes=[]; links=[]; PersonID={}; listaNodosPersona=[]; listaNodosOrgs=[]
    #import ThreeScalePY
    #authrep = ThreeScalePY.ThreeScaleAuthRepUserKey(provider_key, user_key)
    #if authrep.authrep():

    num = db.relPersona.origenP.count()
    if(_id!=0):
        listaNodosOrgs.append(_id)
        num=db.RelPersOrg.destinoO.count()
        rel2Orgs=db((db.RelPersOrg.destinoO==_id) & (db.RelPersOrg.is_active==True) & (db.RelPersOrg.origenP==db.persona.id) &
                    (db.persona.is_active==True) & (db.RelPersOrg.destinoO==db.Organizacion.id) & (db.Organizacion.is_active==True)
                    ).select(db.RelPersOrg.origenP,db.RelPersOrg.destinoO,num,groupby=[db.RelPersOrg.origenP,db.RelPersOrg.destinoO],cache=(cache.ram,3600))
        for relation in rel2Orgs:
            listaNodosPersona.append(relation.RelPersOrg.origenP)
            links.append(dict(source='P'+str(relation.RelPersOrg.origenP),target='O'+str(relation.RelPersOrg.destinoO),value=relation[num]))
        #if listaNodosPersona!=[]:
            #listatmp=set(listaNodosPersona)
            #rel2Orgs=db((db.RelPersOrg.origenP.belongs(listatmp)) & (db.RelPersOrg.is_active==True) & (db.RelPersOrg.origenP==db.persona.id) &
            #    (db.persona.is_active==True) & (db.RelPersOrg.destinoO==db.Organizacion.id) & (db.Organizacion.is_active==True)).select(
            #    db.RelPersOrg.origenP,db.RelPersOrg.destinoO,num,groupby=[db.RelPersOrg.origenP,db.RelPersOrg.destinoO],cache=(cache.ram,3600))
            #for relation in rel2Orgs:
            #    listaNodosPersona.append(relation.RelPersOrg.origenP)
            #    listaNodosOrgs.append(relation.RelPersOrg.destinoO)
            #    links.append(dict(source='P'+str(relation.RelPersOrg.origenP),target='O'+str(relation.RelPersOrg.destinoO),value=relation[num]))
            ##person2person
            #num=db.relPersona.destinoP.count()
            #listatmp=set(listaNodosPersona)
            #relPersona=db((db.relPersona.is_active==True) & ((db.relPersona.origenP.belongs(listatmp)) | (db.relPersona.destinoP.belongs(listatmp)))).select(db.relPersona.origenP,db.relPersona.destinoP,num,
            #    groupby=[db.relPersona.origenP,db.relPersona.destinoP],cache=(cache.ram,3600))
            #for relation in relPersona:
            #    listaNodosPersona.append(relation.relPersona.origenP)
            #    listaNodosPersona.append(relation.relPersona.destinoP)
            #    links.append(dict(source='P'+str(relation.relPersona.origenP),target='P'+str(relation.relPersona.destinoP),value=relation[num]))




        num=db.relOrg2Org.origenO.count()
        relOrgs2Orgs=db((db.relOrg2Org.is_active==True) & ((db.relOrg2Org.origenO==_id) | (db.relOrg2Org.destinoO==_id)) &
                        (db.relOrg2Org.destinoO==db.Organizacion.id) & (db.Organizacion.is_active==True)).select(db.relOrg2Org.origenO,db.relOrg2Org.destinoO,num,groupby=[db.relOrg2Org.origenO,db.relOrg2Org.destinoO],cache=(cache.ram,3600))
        for relation in relOrgs2Orgs:
            listaNodosOrgs.append(relation.relOrg2Org.origenO)
            listaNodosOrgs.append(relation.relOrg2Org.destinoO)
            links.append(dict(source='O'+str(relation.relOrg2Org.origenO),target='O'+str(relation.relOrg2Org.destinoO),value=relation[num]))

        #if listaNodosOrgs!=[]:
            #listatmp=set(listaNodosOrgs)
            #relOrg2Orgs=db((db.relOrg2Org.is_active==True) & ((db.relOrg2Org.origenO.belongs(listatmp)) | (db.relOrg2Org.destinoO.belongs(listatmp))) &
            #               (db.relOrg2Org.destinoO==db.Organizacion.id) & (db.Organizacion.is_active==True)).select(db.relOrg2Org.origenO,db.relOrg2Org.destinoO,num,groupby=[db.relOrg2Org.origenO,db.relOrg2Org.destinoO],cache=(cache.ram,3600))
            #for relation in relOrg2Orgs:
            #    listaNodosOrgs.append(relation.relOrg2Org.origenO)
            #    listaNodosOrgs.append(relation.relOrg2Org.destinoO)
            #    links.append(dict(source='O'+str(relation.relOrg2Org.origenO),target='O'+str(relation.relOrg2Org.destinoO),value=relation[num]))

            #listatmp=set(listaNodosOrgs)
            #rel2Orgs=db((db.RelPersOrg.destinoO.belongs(listatmp)) & (db.RelPersOrg.is_active==True) & (db.RelPersOrg.origenP==db.persona.id) &
            #            (db.persona.is_active==True) & (db.RelPersOrg.destinoO==db.Organizacion.id) & (db.Organizacion.is_active==True)
            #            ).select(db.RelPersOrg.origenP,db.RelPersOrg.destinoO,num,groupby=[db.RelPersOrg.origenP,db.RelPersOrg.destinoO],cache=(cache.ram,3600))
            #for relation in rel2Orgs:
            #    listaNodosOrgs.append(relation.RelPersOrg.destinoO)
            #    listaNodosPersona.append(relation.RelPersOrg.origenP)
            #    links.append(dict(source='P'+str(relation.RelPersOrg.origenP),target='O'+str(relation.RelPersOrg.destinoO),value=relation[num]))




        if listaNodosPersona!=[]:
            c = Counter(listaNodosPersona)
            listatmp=set(listaNodosPersona)
            personas= db((db.persona.id.belongs(listatmp)) & (db.persona.is_active==True)).select(cache=(cache.ram,3600))
            for persona in personas:
                root='false'
                relevance = 56
                #relevance=c[persona.id]*100
                imagen=URL('static','img/icono-persona56.png')
                shortBio=''
                if persona.depiction:
                    imagen=URL('default','fast_download',args=persona.depiction)
                if persona.shortBio:
                    shortBio=persona.shortBio.decode('utf-8')[:180]+'...'
                nodes.append(dict(name=persona.alias,shortBio=shortBio,group='persona',id="P"+str(persona.id),relevance=relevance,url=URL('personas','conexiones',args=convert_latin_chars(persona.alias)),root=root,imagen=imagen))

        if listaNodosOrgs!=[]:
            c = Counter(listaNodosOrgs)
            listatmp=set(listaNodosOrgs)
            orgs=db((db.Organizacion.is_active==True) & (db.Organizacion.id.belongs(listatmp))).select(cache=(cache.ram,3600))
            for org in orgs:
                relevance = 56
                imagen=URL('static','img/icono-organizaciones56.png')
                shortBio=''
                url=URL('organizaciones','conexiones',args=convert_latin_chars(org.alias))
                if org.tipoOrg==2:
                    imagen=URL('static','img/icono-empresas56.png')
                    group1='empresa'
                    url=URL('empresas','conexiones',args=convert_latin_chars(org.alias))
                else:
                    group1='organizacion'
                if org.haslogo:
                    imagen=URL('default','fast_download',args=org.haslogo)
                if org.shortBio:
                    shortBio=org.shortBio.decode('utf-8')[:180]+'...'
                #relevance=c[org.id]*100
                nodes.append(dict(name=org.alias,shortBio=shortBio,group=group1, id="O"+str(org.id),relevance=relevance,url=url,root='false',imagen=imagen))

                #relPerOrgs=db((db.RelPersOrg.is_active==True) ).select()

                    # all was ok, proceed normally


    return dict(nodes=nodes,links=links)

def MapasAll():
    from conversion import convert_latin_chars
    url =request.env.http_host + request.env.request_uri
    _id=request.args(0) or redirect(URL('error','error404'))
    person=None
    imagen=IMG(_src=URL('static','tmp/avatar-36.gif'))

    person=db.persona(_id)
    if (person!=None):
        redirect(URL('personas','mapa_relaciones',args=convert_latin_chars(person.alias)))
    else:
        redirect(URL('error','error404'))



    return dict(_id=_id,person=person,imagen=imagen,url=url)

def MapasAllOrgs():
    from conversion import convert_latin_chars
    url =request.env.http_host + request.env.request_uri
    _id=request.args(0) or redirect(URL('error','error404'))
    org=None
    imagen=IMG(_src=URL('static','tmp/avatar-36.gif'))

    org=db.Organizacion(_id)
    if (org!=None):
        if org.tipoOrg==2:
            redirect(URL('empresas','mapa_relaciones',args=convert_latin_chars(org.alias)))
        else:
            redirect(URL('organizaciones','mapa_relaciones',args=convert_latin_chars(org.alias)))

    redirect(URL('error','error404'))

    return dict(_id=_id,org=org,imagen=imagen,url=url)

def index():
    return locals()

def notificaciones():
    _id=request.args(0) or redirect(URL('default','index'))
    tipos=request.args(1) or redirect(URL('default','index'))
    tabla = request.args(2) or redirect(URL('default','index'))
    if tabla == 'persona':
        rows = db(db.persona.id==_id).select(db.persona.alias,db.persona.depiction,cache=(cache.ram,3600)).first()
        var = rows.alias
    else:
        rows = db(db.Organizacion.id==_id).select(db.Organizacion.alias,db.Organizacion.haslogo,db.Organizacion.tipoOrg,cache=(cache.ram,3600)).first()
        var = rows.alias

    form=SQLFORM(db.notificaciones)
    form.vars.referenceEntity=tabla
    form.vars.reference=_id
    form.vars.tipoError=tipos


    if form.process().accepted:
        response.flash = 'Formulario Aceptado'

        mail.send(to=['team@poderopedia.com'],
            subject='Sugerencia de Perfil',
            # If reply_to is omitted, then mail.settings.sender is used
            #reply_to='us@example.com',
            message=var+'Un usuario sugirio el perfil de "'+form.vars['contenido']+'" la importancia de este perfil es  y obtuvo la informacion desde la siguiente URL '+form.vars['URL']+'.' )
        #redirect(URL('notificaciones', args=[_id,tipos,tabla],vars={'success':'ok'}))
    elif form.errors:
        response.flash = 'Error en el Formulario'


    return dict(item=rows,form=form,tipo=tipos,tabla=tabla)

def tipoerror():
    email=None; nombre=None;
    if me:
        email=auth.user.email
        nombre=auth.user.user_name
    _id=request.args(0) or redirect(URL('default','index'))
    #tipos=request.args(1) or redirect(URL('default','index'))
    tabla = request.args(1) or redirect(URL('default','index'))
    if tabla == 'persona':
        rows = db(db.persona.id==_id).select(db.persona.alias,db.persona.depiction,cache=(cache.ram,3600)).first()
        var = rows.alias
    else:
        rows = db(db.Organizacion.id==_id).select(db.Organizacion.alias,db.Organizacion.haslogo,db.Organizacion.tipoOrg,cache=(cache.ram,3600)).first()
        var = rows.alias

    form=SQLFORM(db.tipoerror)
    form.vars.referenceEntity=tabla
    form.vars.reference=_id
    #form.vars.tipoError='reportarError'


    if form.process().accepted:
        response.flash = 'Formulario Aceptado'

        mail.send(to=['team@poderopedia.com'],
            subject='Reporte de Errror en '+var,
            # If reply_to is omitted, then mail.settings.sender is used
            #reply_to='us@example.com',
            message='El usuario "'+nombre+'" de email "'+email+'", reporto un Error en '+var+', el contenido con error es el siguiente: '+form.vars['contenido']+'" y obtuvo la informacion desde la siguiente URL '+form.vars['URL']+'.',
            headers = {'Content-Type' : 'text/plain; charset="utf-8"'})

        redirect(URL('tipoerror',args=[_id,tabla],vars={'success':'ok'}))
    elif form.errors:
        response.flash = 'Error en el Formulario'
    return dict(item=rows,form=form,tabla=tabla)

def tipoinadecuado():
    email=None; nombre=None;
    if me:
        email=auth.user.email
        nombre=auth.user.user_name
    _id=request.args(0) or redirect(URL('default','index'))
    #tipos=request.args(1) or redirect(URL('default','index'))
    tabla = request.args(1) or redirect(URL('default','index'))
    if tabla == 'persona':
        rows = db(db.persona.id==_id).select(db.persona.alias,db.persona.depiction,cache=(cache.ram,3600)).first()
        var = rows.alias
    else:
        rows = db(db.Organizacion.id==_id).select(db.Organizacion.alias,db.Organizacion.haslogo,db.Organizacion.tipoOrg,cache=(cache.ram,3600)).first()
        var = rows.alias

    form=SQLFORM(db.tipoinadecuado)
    form.vars.referenceEntity=tabla
    form.vars.reference=_id
    #form.vars.tipoError='contenidoInadecuado'


    if form.process().accepted:
        response.flash = 'Formulario Aceptado'

        mail.send(to=['juan.eduardo@poderopedia.com'],
            cc=['monica@poderopedia.com'],
            bcc=['miguel@poderopedia.com'],
            subject='Contenido Inadecuado en '+var,
            # If reply_to is omitted, then mail.settings.sender is used
            #reply_to='us@example.com',
            message='El usuario "'+nombre+'" de email "'+email+'", reporto un Contenido Inadecuado en '+var+', el contenido con inadecuado es el siguiente: '+form.vars['contenido']+'" y obtuvo la informacion desde la siguiente URL '+form.vars['URL']+'.',
            headers = {'Content-Type' : 'text/plain; charset="utf-8"'})
        redirect(URL('tipoinadecuado',args=[_id,tabla],vars={'success':'ok'}))
    elif form.errors:
        response.flash = 'Error en el Formulario'


    return dict(title_message='Reportar Contenido Inadecuado',item=rows,form=form,tabla=tabla)


def sugerir_perfil():
    email=None; nombre=None;
    if me:
        email=auth.user.email
        nombre=auth.user.user_name
    form=SQLFORM(db.sugerirPersona)
    if form.process().accepted:
        response.flash = 'Formulario Aceptado'
        mail.send(to=['juan.eduardo@poderopedia.com'],
            cc=['monica@poderopedia.com'],
            bcc=['miguel@poderopedia.com'],
            subject='Sugerencia de Perfil de'+form.vars['name'],
            # If reply_to is omitted, then mail.settings.sender is used
            #reply_to='us@example.com',
            message='El usuario "'+nombre+'" de email "'+email+'", sugirio el perfil de "'+form.vars['name']+'" la importancia de este perfil es "'+form.vars['texto']+'" y obtuvo la informacion desde la siguiente URL '+form.vars['documentURL']+'.',
            headers = {'Content-Type' : 'text/plain; charset="utf-8"'})
        redirect(URL('sugerir_perfil',vars={'success':'ok'}))
    elif form.errors:
        response.flash = 'Error en el Formulario'

    return dict(form=form)

def compartir():
    _id=request.args(0)
    url1=request.args(1)
    db.compartir.pagina.default='http://beta.poderopedia.org/visualizacion/'+str(url1)+'/'+str(_id)
    form=SQLFORM(db.compartir)
    if form.process().accepted:
        response.flash = 'Formulario Aceptado'
        mail.send(to=[form.vars['email']],
            subject='Sugerencia de Perfil',
            message='Un usuario de nuestro sitio web te sugire que revises el siguiente link "http://beta.poderopedia.org/visualizacion/'+url1+'/'+_id+'" para él, la importancia de este perfil es "'+form.vars['contenido'],
            headers = {'Content-Type' : 'text/plain; charset="utf-8"'})

        redirect(URL('compartir',vars={'success':'ok'}))
    elif form.errors:
        response.flash = 'Error en el Formulario'

    return dict(form=form,_id=_id,url1=url1)

def historial():
    _id=request.args(0) or redirect(URL('default','index'))
    page=request.args(1) or redirect(URL('error','error404'))
    entity=None; historial=None; creador=None
    if page=='caso_perfil':
        entity=db.persona(_id)
        historial=db((db.persona_archive.current_record==_id) & (db.persona_archive.modified_on!=None) & (db.persona_archive.modified_by!=None) ).select(orderby='~modified_on',limitby=(0,10))
    elif page=='caso_organizacion':
        entity=db.Organizacion(_id)
        historial=db((db.Organizacion_archive.current_record==_id) & (db.Organizacion_archive.modified_on!=None) & (db.Organizacion_archive.modified_by!=None)).select(orderby='~modified_on',limitby=(0,10))

    if entity!=None:
        creador=db.auth_user(entity.created_by)
    else: redirect(URL('error','error404'))

    return dict(entity=entity, historial=historial, creador=creador, page=page)

## friendly url
def perfil():
    id=""
    alias=request.args(0)
    persona=db.persona(alias=alias)
    if persona:
        id=persona.id
        ##redirect(URL('caso_perfil',args=id))
    else: redirect(URL('error','error404'))
    #redirect(URL('visualizacion','caso_perfil',args=id))
    return id

@service.json
def childnodes(idx):
    json={}
    if idx[0]=='P':
        json= persona2all(int(idx[1:]))
    elif idx[0]=='O':
        json= orgs2all(int(idx[1:]))
    return json