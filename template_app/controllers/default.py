#!/usr/bin/python
# -*- coding: utf-8 -*-


def index():
    return dict(_id=1,page=0, sort=0, target=0, entity=0)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    rpx = ''
    form = auth()
    registerurl=URL('default','registrogeneral',args='register')
    if request.vars.token:
        auth.settings.login_form = rpxform
        return dict(form=auth())
    if 'login' in request.args:
        rpx = rpxform.login_form()
        form = auth()
    else:
        form = auth()
    return dict(form=form,conf=request.args(0),_id=0,rpx=rpx)

def sociales():
    rpx = ''
    registerurl=URL('default','registrogeneral',args='register')
    if request.vars.token:
        auth.settings.login_form = rpxform
        return dict(form=auth())
    if 'login' in request.args:
        rpx = rpxform.login_form()
        form = auth()
    else:
        form = auth()

    return dict(form=form,rpx=rpx)


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)

def fast_download():
    import os
    import time

    filename = request.args(0)
    if (filename!=None) & (filename!=''):
        #del response.headers['Cache-Control']
        #del response.headers['Pragma']
        #del response.headers['Expires']
        filepath = os.path.join(request.folder, 'uploads', filename)

    else:
        filepath = os.path.join(request.folder, 'static', 'img/default-pic-profile-person.png')

    response.headers['Cache-Control'] = "max-age=2592000"
    response.headers['Expires'] = "max-age=2592000"
    response.headers['Pragma'] = 'Pragma:public'
    response.headers['Last-Modified'] =\
    time.strftime("%a, %d %b %Y %H:%M:%S +0000",
        time.localtime(os.path.getmtime(filepath)))

    return response.stream(open(filepath, 'rb'))


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())


def list_items():
    if len(request.args): page=int(request.args[0])
    else: page=0
    items_per_page=20
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    rows=db().select(limitby=limitby,cache=(cache.ram,3600))
    return dict(rows=rows,page=page,items_per_page=items_per_page)


@auth.requires_login()
def configuracion():
    conf='configuracion'
    form=auth.change_password()
    return dict(form=form,conf=conf)
    
@auth.requires_login()
def configuracion_ok():
    email=auth.user.email
    mail.send(to=[email],
            subject='Confirmación del cambio de contraseña de Poderopedia',
            message=CONFIGURACION_OK)
    conf='configuracion'
    return dict(conf=conf)

def gracias():
    conf='configuracion'
    return dict(conf=conf)

def olvide_contrasena_error():
    conf='configuracion'
    return dict(conf=conf)

def logout():
    return dict(form=auth.logout())

# Version1
def notificaciones():

    lista=[]
    lista2=[]            
    row1 = db(db.tipoerror.is_active==True).select(db.tipoerror.id,db.tipoerror.contenido,db.tipoerror.reference,db.tipoerror.referenceEntity,db.tipoerror.created_on,orderby="tipoerror.created_on DESC",cache=(cache.ram,3600))
    for item in row1:
        if item.referenceEntity == 'persona':
            persona=db(db.persona.id==item.reference).select(db.persona.alias).first() 
            alias=persona.alias      
        else:
            org=db.Organizacion(item.reference)
            alias=org.alias
        lista.append(dict(id=item.id,contenido=item.contenido,creado=item.created_on,alias=alias))
        
    row2 = db(db.tipoinadecuado.is_active==True).select(db.tipoinadecuado.id,db.tipoinadecuado.contenido,db.tipoinadecuado.reference,db.tipoinadecuado.referenceEntity,db.tipoinadecuado.created_on,orderby="tipoinadecuado.created_on DESC",cache=(cache.ram,3600))
    for item in row2:
        if item.referenceEntity == 'persona':
            persona=db(db.persona.id==item.reference).select(db.persona.alias).first() 
            alias=persona.alias      
        else:
            org=db.Organizacion(item.reference)
            alias=org.alias
        lista2.append(dict(id=item.id,contenido=item.contenido,creado=item.created_on,alias=alias))
    
    row3 = db(db.sugerirPersona).select(db.sugerirPersona.id,db.sugerirPersona.name,db.sugerirPersona.texto,db.sugerirPersona.created_on,orderby="sugerirPersona.id DESC",cache=(cache.ram,3600))
    
    row4 = db((db.sugerirConexion.reference == db.persona.id)&(db.sugerirConexion.referenceEntity == 'persona')).select(db.sugerirConexion.id,db.sugerirConexion.texto,db.sugerirConexion.name,db.sugerirConexion.created_on,db.persona.alias,orderby="sugerirConexion.id DESC",cache=(cache.ram,3600))
    
    row5 = db((db.sugerirConexion.reference == db.Organizacion.id)&(db.sugerirConexion.referenceEntity == 'organizacion')).select(db.sugerirConexion.id,db.sugerirConexion.texto,db.sugerirConexion.name,db.sugerirConexion.created_on,db.Organizacion.alias,orderby="sugerirConexion.id DESC",cache=(cache.ram,3600))

    return dict(lista=lista,lista2=lista2,lista3=row3,lista4=row4,lista5=row5)


#TODO _id=1,page=0, sort=0, target=0, entity=0
def registrogeneral():
    rpx = ''
    registerurl=URL('default','registrogeneral',args='register')
    if request.vars.token:
        auth.settings.login_form = rpxform
        return dict(form=auth())
    if 'login' in request.args:
        rpx = rpxform.login_form()
        form = auth.register()
    else:
        form = auth.register()

    return dict(form=form,rpx=rpx)

#TODO _id=1,page=0, sort=0, target=0, entity=0
def ingresogeneral():
    rpx = ''
    registerurl=URL('default','registrogeneral',args='register')
    if request.vars.token:
        auth.settings.login_form = rpxform
        return dict(form=auth())
    if 'login' in request.args:
        rpx = rpxform.login_form()
        form = auth()
    else:
        form = auth()

    return dict(form=form,rpx=rpx)

def retrieve_password():
    form=auth.retrieve_password()
    email=form.vars['']
    return dict(form=form,target="retrieve")

#TODO _id=1,page=0, sort=0, target=0, entity=0
def registrogeneral_cuentacreada():
    return dict(_id=1,page=0, sort=0, target=0, entity=0)

#TODO _id=1,page=0, sort=0, target=0, entity=0
def registrogeneral_mensajecontrasenaerrada():
    return dict(_id=1,page=0, sort=0, target=0, entity=0)

#TODO _id=1,page=0, sort=0, target=0, entity=0
def editarconexiones_fb_twitter():
    conf='conexiones'
    return dict(_id=1,page=0, sort=0, target=0, entity=0,conf=conf)

#TODO _id=1,page=0, sort=0, target=0, entity=0
@auth.requires_login()
def notificacionesgenerales():
    conf='notificaciones'
    if (auth.has_membership('editor')) | (auth.has_membership('administrator')):
        form = SQLFORM.grid()
    return dict(_id=1,page=0, sort=0, target=0, entity=0,conf=conf)

#TODO _id=1,page=0, sort=0, target=0, entity=0
def notificacionesindividual():
    return dict(_id=1,page=0, sort=0, target=0, entity=0)

def make_thumbnail(table, image_id, size=(72, 72)):
    return locals()

@auth.requires_login()
def editaravatar():
    conf='avatar'
    user=db.auth_user(me)
    db.auth_user.email.readable=db.auth_user.email.writable=False
    db.auth_user.user_name.readable=db.auth_user.user_name.writable=False
    form=SQLFORM(db.auth_user,user)
    if(request.vars.file==None):
        form=auth.profile()

    return dict(form=form,conf=conf,user=user)

@auth.requires_login()
def editarperfil():
    conf='perfil'

    db.auth_user.email.readable=db.auth_user.email.writable=False
    db.auth_user.user_name.readable=db.auth_user.user_name.writable=False
    user=db.auth_user(me)
    form=SQLFORM(db.auth_user,user)

    if form.process().accepted:
        response.flash = 'Datos Ingresados'
    elif form.errors:
        response.flash = 'Existen errores al procesar Formulario'
    else:
        response.flash = 'Por favor llene los campos solicitados'

    return dict(form=form,conf=conf)
    
@auth.requires_login()
def editarperfil_ok():
    conf='perfil'
    return dict(conf=conf)

@auth.requires_login()
def upload_callback():
    if 'qqfile' in request.vars:
        filename = request.vars.qqfile
        newfilename = db.auth_user.thumbnail.store(request.body, filename)

        authuser=db.auth_user(me)
        authuser.update_record(thumbnail=newfilename)



    return response.json({'success': 'true','filename':newfilename})


##barra derecha
@auth.requires_login()
def person_created():
    return locals()

@auth.requires_login()
def sidebar_cuenta():
    ##creaciones
    persona=db((db.persona.created_by==me) & (db.persona.is_active==True)).count()
    empresa=db((db.Organizacion.tipoOrg==2) & (db.Organizacion.created_by==me) & (db.Organizacion.is_active==True)).count()
    organizacion=db((db.Organizacion.tipoOrg!=2) & (db.Organizacion.created_by==me) & (db.Organizacion.is_active==True)).count()

    ##colaboraciones
    persona_histo=db((db.persona.modified_by==me) & (db.persona.is_active==True)).count()
    empresa_histo=db((db.Organizacion.tipoOrg==2) & (db.Organizacion.modified_by==me) & (db.Organizacion.is_active==True)).count()
    organizacion_histo=db((db.Organizacion.tipoOrg!=2) & (db.Organizacion.modified_by==me) & (db.Organizacion.is_active==True)).count()
    ##persona_histo=db(db.persona_archive.created_by==me & db.persona_archive.is_active==True).select(groupby=db.persona_archive.current_record)
    ##empresas_histo=db(db.Organizacion_archive.tipoOrg==2 & db.Organizacion_archive.modified_by==me & db.Organizacion_archive.is_active==True).select(groupby=db.Organizacion_archive.current_record)
    ##organizacion_histo=db(db.Organizacion_archive.tipoOrg!=2 & db.Organizacion_archive.modified_by==me & db.Organizacion_archive.is_active==True).select(groupby=db.Organizacion_archive.current_record)


    return dict(persona=persona,empresa=empresa,organizacion=organizacion,persona_histo=persona_histo,
        empresa_histo=empresa_histo,organizacion_histo=organizacion_histo)

@auth.requires_login()
def mis_personas():
    personas=""; target='mis_personas'
    _id=me
    activo=request.vars['activo']
    total=0

    if len(request.args)>1: page=int(request.args[1])
    else: page=0
    if len(request.args)>2: sort=request.args(2)
    else: sort='false'
    if len(request.args)>3: letter=request.args(3)
    else: letter=''


    items_per_page=20
    if activo=='todos':
        items_per_page=9
        response.view='default/todos_persona.load'
        target='todos_personas'
        total=db((db.persona.created_by==me) & (db.persona.is_active==True)).count()
    limitby=(page*items_per_page,(page+1)*items_per_page+1)

    if(sort!='false'):
        reverse=False
        orderby=~db.persona.alias
    else:
        reverse=True
        orderby=db.persona.alias

    personas=db((db.persona.created_by==me) & (db.persona.is_active==True)).select(orderby=orderby,limitby=limitby,cache=(cache.ram,3600))
    return dict(personas=personas,page=page,items_per_page=items_per_page,target=target,
        entity=personas,_id=_id, sort=sort,letter=letter,total=total)

@auth.requires_login()
def mis_empresas():
    empresas=""; target='mis_empresas'
    _id=me
    activo=request.vars['activo']
    total=0

    if len(request.args)>1: page=int(request.args[1])
    else: page=0
    if len(request.args)>2: sort=request.args(2)
    else: sort='false'
    if len(request.args)>3: letter=request.args(3)
    else: letter=''


    items_per_page=20
    if activo=='todos':
        items_per_page=9
        response.view='default/todos_empresa.load'
        target='todos_empresas'
        total=db((db.Organizacion.tipoOrg==2) & (db.Organizacion.created_by==me) & (db.Organizacion.is_active==True)).count()
    limitby=(page*items_per_page,(page+1)*items_per_page+1)

    if(sort!='false'):
        reverse=False
        orderby=~db.Organizacion.alias
    else:
        reverse=True
        orderby=db.Organizacion.alias


    empresas=db((db.Organizacion.tipoOrg==2) & (db.Organizacion.created_by==me) & (db.Organizacion.is_active==True)).select(orderby=orderby,limitby=limitby,cache=(cache.ram,3600))
    return dict(empresas=empresas,page=page,items_per_page=items_per_page,target=target,
        entity=empresas,_id=_id, sort=sort, letter=letter,total=total)

@auth.requires_login()
def mis_organizaciones():
    organizaciones=""; target='mis_organizaciones'
    _id=me
    activo=request.vars['activo']
    total=0

    if len(request.args)>1: page=int(request.args[1])
    else: page=0
    if len(request.args)>2: sort=request.args(2)
    else: sort='false'
    if len(request.args)>3: letter=request.args(3)
    else: letter=''


    items_per_page=20
    if activo=='todos':
        items_per_page=9
        response.view='default/todos_organizacion.load'
        target='todos_organizaciones'
        total=db((db.Organizacion.tipoOrg!=2) & (db.Organizacion.created_by==me) & (db.Organizacion.is_active==True)).count()
    limitby=(page*items_per_page,(page+1)*items_per_page+1)

    if(sort!='false'):
        reverse=False
        orderby=~db.Organizacion.alias
    else:
        reverse=True
        orderby=db.Organizacion.alias
    organizaciones=db((db.Organizacion.tipoOrg!=2) & (db.Organizacion.created_by==me) & (db.Organizacion.is_active==True)).select(orderby=orderby,limitby=limitby,cache=(cache.ram,3600))

    return dict(organizaciones=organizaciones,page=page,items_per_page=items_per_page,target=target,
        entity=organizaciones,_id=_id, sort=sort, letter=letter,total=total)

@auth.requires_membership('editor')
@auth.requires_membership('administrator')
def mis_publicaciones():
    activo=request.args(0)

    return dict(activo=activo)

@service.rss
def destacados_rss():
    entradas=[]
    resultados=dict(
        title="Poderopedia ",
        link="http://www.poderopedia.org",
        description="Poderopedia RSS",
        created_on=str(request.now)
        )
    destacados = db(db.destacados.is_active==True).select(orderby=~db.destacados.fecha,limitby=(0,10),cache=(cache.ram,3600))
    for news in destacados:
        results=dict(title=news.titulo.decode('utf-8'),link=news.url,description=news.contenido.decode('utf-8'),created_on=str(news.fecha))
        entradas.append(results)
    resultados['entries']=entradas
    response.headers['Content-Type']='application/rss+xml'
    return resultados


#TODO temas union personas organizaciones, revisar doc web2py y uniformar campos
@service.rss
def lo_ultimo():
    from conversion import convert_latin_chars
    entradas=[]
    resultados=dict(
        title="Poderopedia",
        link="http://www.poderopedia.org",
        description="Poderopedia Lo Ultimo",
        created_on=str(request.now)
    )
    personas = db((db.persona.is_active==True) & (db.persona.shortBio!=None) & (db.persona.shortBio!='')
                  & (db.persona.depiction!=None) & (db.persona.depiction!='')).select(
        db.persona.alias,db.persona.shortBio,db.persona.depiction,db.persona.modified_on,
        orderby=[~db.persona.modified_on],limitby=(0,2))

    for persona in personas:
        results=dict(title=persona.alias.decode('utf-8'),link=URL('personas','conexiones',args=convert_latin_chars(persona.alias)),
                     description=persona.shortBio.decode('utf-8'),created_on=str(persona.modified_on))
        entradas.append(results)

    organizacion = db((db.Organizacion.is_active==True) & (db.Organizacion.shortBio!=None) & (db.Organizacion.shortBio!='')
                      & (db.Organizacion.haslogo!=None) & (db.Organizacion.haslogo!='')).select(
        db.Organizacion.id,db.Organizacion.tipoOrg,
        db.Organizacion.alias,db.Organizacion.shortBio,db.Organizacion.haslogo,db.Organizacion.modified_on,
        orderby=[~db.Organizacion.modified_on],limitby=(0,2))

    for org in organizacion:
        args=convert_latin_chars(org.alias)
        link=URL('organizaciones','conexiones',args=args)
        if org.tipoOrg==2:
            link=URL('empresas','conexiones',args=args)
        results=dict(title=org.alias.decode('utf-8'),link=link,description=org.shortBio.decode('utf-8'),created_on=str(org.modified_on))
        entradas.append(results)
    entradas=sorted(entradas, key=lambda k: k['created_on'], reverse=True)
    resultados['entries']=entradas
    response.headers['Content-Type']='application/rss+xml'
    return resultados

def documentos():
    from conversion import convert_latin_chars
    from gluon.storage import Storage
    url =request.env.http_host + request.env.request_uri
    dc_id=request.args(0) or redirect(URL('default','index'))
    _id=request.args(1)  or redirect(URL('default','index'))
    target = request.args(2) or redirect(URL('default','index'))

    alias=''; imagen=IMG(_alt=alias, _src=URL('static','img/default-pic-profile-person.png'))
    href=''

    docs=db.documentCloud(dc_id=dc_id, is_active=True)


    if(target=='persona'):
        person= db(db.persona.id==_id).select(db.persona.alias,db.persona.depiction).first()
        alias=convert_latin_chars(person.alias)

        if docs:
            redirect(URL('personas','documentos',args=[alias,convert_latin_chars(docs.title)]))


    elif target=='organizacion':
        org=db(db.Organizacion.id==_id).select(db.Organizacion.alias,db.Organizacion.haslogo,db.Organizacion.tipoOrg).first()
        alias=convert_latin_chars(org.alias); href='caso_organizacion'
        if (org.haslogo!=None) & (org.haslogo!=''):
            imagen=IMG(_alt=org.alias, _src=URL('default','fast_download',args=org.haslogo),_height=44)
        if org.tipoOrg==2:
            if docs:
                redirect(URL('empresas','documentos',args=[alias,convert_latin_chars(docs.title)]))
        else:
            if docs:
                redirect(URL('organizaciones','documentos',args=[alias,convert_latin_chars(docs.title)]))

    redirect(URL('error','error404'))



    return locals()

def revolucionario():
    return locals()


