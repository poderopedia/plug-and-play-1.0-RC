__author__ = 'Evolutiva'

def conexiones():
    from urllib2 import unquote
    url =request.env.http_host + request.env.request_uri
    alias=request.args(0) or redirect(URL('default','index'))

    alias=alias.decode('utf-8').replace('_',' ').replace('-','.')
    organizacion=db.Organizacion(alias=alias,is_active=True)
    response.view='visualizacion/caso_organizacion.html'
    if organizacion:
        _id=organizacion.id
        ##redirect(URL('caso_perfil',args=id))
    else: redirect(URL('error','error404'))


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

def personasrelacionadas():
    url =request.env.http_host + request.env.request_uri
    alias=request.args(0) or redirect(URL('default','index'))
    alias=alias.decode('utf-8').replace('_',' ').replace('-','.')

    response.view='organizacion/personasrelacionadas.html'

    organizacion=db.Organizacion(alias=alias,is_active=True)
    if organizacion:
        _id=organizacion.id
    else:
        redirect(URL('error','error404'))

    return dict(_id=_id, organizacion=organizacion,url=url)

def organizacionesrelacionadas():
    url =request.env.http_host + request.env.request_uri
    alias=request.args(0) or redirect(URL('default','index'))
    alias=alias.decode('utf-8').replace('_',' ').replace('-','.')

    response.view='organizacion/organizacionesrelacionadas.html'

    organizacion=db.Organizacion(alias=alias,is_active=True)
    if organizacion:
        _id=organizacion.id
    else:
        redirect(URL('error','error404'))

    return dict(_id=_id, organizacion=organizacion,url=url)

def empresasrelacionadas():
    url =request.env.http_host + request.env.request_uri
    alias=request.args(0) or redirect(URL('default','index'))
    alias=alias.decode('utf-8').replace('_',' ').replace('-','.')

    response.view='organizacion/empresasrelacionadas.html'

    organizacion=db.Organizacion(alias=alias,is_active=True)
    if organizacion:
        _id=organizacion.id
    else:
        redirect(URL('error','error404'))

    return dict(_id=_id, organizacion=organizacion,url=url)

def documentos():
    from gluon.storage import Storage
    from conversion import convert_latin_chars

    url =request.env.http_host + request.env.request_uri
    response.view='default/documentos.html'

    alias=request.args(0)  or redirect(URL('default','index'))
    alias=alias.decode('utf-8').replace('_',' ').replace('-','.')

    dc_title=request.args(1) or redirect(URL('default','index'))
    dc_title=dc_title.decode('utf-8').replace('_',' ').replace('-','.')

    imagen=IMG(_alt=alias, _src=URL('static','img/icono-organizaciones.png'),_height=44)
    href=''


    org= db.Organizacion(alias=alias,is_active=True)
    if org:
        controller='organizaciones'; href='conexiones'
        _id=org.id
        if org.haslogo!=None:
            imagen=IMG(_alt=org.alias,_src=URL('default','fast_download',args=org.haslogo),_height=44)
        args=convert_latin_chars(org.alias)
    else:
        redirect(URL('error','error404'))


    dc_document=db.documentCloud(title=dc_title,is_active=True)
    if dc_document:
        title=dc_document.title
        dc_args_title=convert_latin_chars(title)
        dc_id=dc_document.dc_id
    else:
        redirect(URL('error','error404'))

    response.title=org.alias + ' | ' + title + ' | Poderopedia'

    entity=Storage({'id':_id,'alias':alias,'logo':imagen,'controller':controller,
                    'target':href,'args':args,'dc_args':dc_args_title})

    return dict(dc_id=dc_id,_id=_id,page=0,sort='false',entity=entity,title=title,url=url)

def mapa_relaciones():

    url =request.env.http_host + request.env.request_uri
    alias=request.args(0) or redirect(URL('error','error404'))
    alias=alias.decode('utf-8').replace('_',' ').replace('-','.')

    response.view='visualizacion/MapasAllOrgs.html'

    org=None
    imagen=IMG(_alt=alias, _src=URL('static','img/icono-organizaciones.png'),_height=44)
    org=db.Organizacion(alias=alias,is_active=True)

    if org:
        _id=org.id
        response.title = org.alias+' | Visualización | Poderopedia'
        if (org.shortBio!=None)&(org.shortBio!=''):
            response.meta.description= org.shortBio[:200]
        if (org.haslogo!=None):
            imagen=IMG(_alt=org.alias,_src=URL('default','download',args=org.haslogo),_height=44)
    else:
        redirect(URL('error','error404'))


    return dict(_id=_id,org=org,imagen=imagen,url=url,entity='organizacion')
