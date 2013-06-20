__author__ = 'Evolutiva'

def personasrelacionadas():
    from conversion import convert_latin_chars
    url =request.env.http_host + request.env.request_uri
    _id=request.args(0) or redirect(URL('error','error404'))

    organizacion=db.Organizacion(_id)
    if organizacion:
        if organizacion.tipoOrg==2:
            redirect(URL('empresas','personasrelacionadas',args=convert_latin_chars(organizacion.alias)))
        else:
            redirect(URL('organizaciones','personasrelacionadas',args=convert_latin_chars(organizacion.alias)))
    else:
        redirect(URL('error','error404'))

    return dict(_id=_id, organizacion=organizacion,url=url)
    
def organizacionesrelacionadas():
    from conversion import convert_latin_chars
    url =request.env.http_host + request.env.request_uri
    _id=request.args(0) or redirect(URL('error','error404'))
    organizacion=db.Organizacion(_id)
    if organizacion:
        if organizacion.tipoOrg==2:
            redirect(URL('empresas','personasrelacionadas',args=convert_latin_chars(organizacion.alias)))
        else:
            redirect(URL('organizaciones','personasrelacionadas',args=convert_latin_chars(organizacion.alias)))
    else:
        redirect(URL('error','error404'))

    return dict(_id=_id, organizacion=organizacion,url=url)
    
def empresasrelacionadas():
    from conversion import convert_latin_chars
    url =request.env.http_host + request.env.request_uri
    _id=request.args(0) or redirect(URL('error','error404'))
    organizacion=db.Organizacion(_id)
    if organizacion:
        if organizacion.tipoOrg==2:
            redirect(URL('empresas','personasrelacionadas',args=convert_latin_chars(organizacion.alias)))
        else:
            redirect(URL('organizaciones','personasrelacionadas',args=convert_latin_chars(organizacion.alias)))
    else:
        redirect(URL('error','error404'))
    return dict(_id=_id, organizacion=organizacion,url=url)


##@auth.requires_login()
def sugerir_persona():
    email=None; nombre=None;
    if me:
        email=auth.user.email
        nombre=auth.user.user_name
    _id=request.args(0) or redirect(URL('default','index'))
    desde=request.vars['desde']
    response.view='persona/sugerir_persona.load'
    entidad='organizacion'


    org=db.Organizacion(_id)
    if org==None: redirect(URL('default','index'))

    alias=org.alias
    entidad='organizacion'
    if org.tipoOrg==2:
        entidad='empresa'
    db.sugerirConexion.referenceEntity.default=entidad
    db.sugerirConexion.reference.default=_id
    db.sugerirConexion.alias.default=alias

    form = SQLFORM(db.sugerirConexion)
    form.vars.reference=_id

    if form.process().accepted:
        if form.vars['alias']:
            alias=form.vars['alias']
        response.flash = T('Formulario aceptado')
        mail.send(to=['juan.eduardo@poderopedia.com'],
            cc=['monica@poderopedia.com'],
            bcc=['miguel@poderopedia.com'],
            subject='Sugerencia de Conexion entre '+alias+' y '+form.vars['name'],
        # If reply_to is omitted, then mail.settings.sender is used
        #reply_to='us@example.com',
            message='El usuario "'+nombre+'" de email "'+email+'", sugirio una conexion entre "'+alias+'" y el perfil de "'+form.vars['name']+'", la relacion entre ellos es de "'+form.vars['texto']+'" y obtuvo la informacion desde la siguiente URL '+form.vars['documentURL']+'.' ,
            headers = {'Content-Type' : 'text/plain; charset="utf-8"'})
        redirect(URL('sugerir_persona',args=_id,vars={'success':'ok'}))
    elif form.errors:
        response.flash = 'Existen Errores'

    return dict(form=form,alias=alias,desde=desde)



def sugerir_organizacion():
    _id=request.args(0) or redirect(URL('default','index'))
    org=db.Organizacion(_id)
    alias=org.alias
    entidad='organizacion'
    if org.tipoOrg==2:
        entidad='empresa'

    form = SQLFORM(db.sugerirConexion)
    form.vars.reference=_id
    form.vars.referenceEntity=entidad
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'

    return dict(form=form,alias=alias)
