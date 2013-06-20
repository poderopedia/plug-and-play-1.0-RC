__author__ = 'Evolutiva'

def call(): return service()

@cache(request.env.path_info,time_expire=10,cache_model=cache.ram)
def personasrelacionadas():
    from conversion import convert_latin_chars
    url =request.env.http_host + request.env.request_uri
    _id=request.args(0) or redirect(URL('error','error404'))
    persona=db.persona(_id)
    redirect(URL('personas','personasrelacionadas',args=convert_latin_chars(persona.alias)))
    return dict(_id=_id, persona=persona,url=url)


@cache(request.env.path_info,time_expire=10,cache_model=cache.ram)
def empresasrelacionadas():
    from conversion import convert_latin_chars
    url =request.env.http_host + request.env.request_uri
    _id=request.args(0) or redirect(URL('default','index'))
    persona=db.persona(_id)
    redirect(URL('personas','empresasrelacionadas',args=convert_latin_chars(persona.alias)))
    return dict(_id=_id, persona=persona,url=url)

@cache(request.env.path_info,time_expire=10,cache_model=cache.ram)
def organizacionesrelacionadas():
    from conversion import convert_latin_chars
    url =request.env.http_host + request.env.request_uri
    _id=request.args(0) or redirect(URL('default','index'))
    persona=db.persona(_id)
    redirect(URL('personas','organizacionesrelacionadas',args=convert_latin_chars(persona.alias)))
    return dict(_id=_id, persona=persona,url=url)





def sugerir_persona():
    email=None; nombre=None;
    if me:
        email=auth.user.email
        nombre=auth.user.user_name
    _id=request.args(0) or redirect(URL('default','index'))
    desde=request.vars['desde']; alias=''
    db.sugerirConexion.referenceEntity.default='persona'
    if desde=='portada':
        db.sugerirConexion.referenceEntity.writable=True
        db.sugerirConexion.reference.writable=True
        db.sugerirConexion.alias.writable=True
    else:
        db.sugerirConexion.reference.default=_id
        persona=db.persona(_id)
        db.sugerirConexion.alias.default=persona.alias
        alias=persona.alias

    form = SQLFORM(db.sugerirConexion)

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
        redirect(URL('sugerir_persona',args=_id,vars={'success':'ok','desde':desde,'alias':form.vars['alias']}))
    elif form.errors:
        response.flash = T('Hay errores en Formulario')
 
    return dict(form=form,desde=desde)



def sugerir_organizacion():
   _id=request.args(0) or redirect(URL('default','index'))
   persona=db.persona(_id)
   alias=persona.alias

   form = SQLFORM(db.sugerirConexion, submit_button = 'Enviar',labels = {'entity':'Entidad'})
   form.vars.reference=_id
   form.vars.referenceEntity='persona'
   if form.process().accepted:
       response.flash = 'form accepted'
   elif form.errors:
       response.flash = 'form has errors'

   return dict(form=form,alias=alias)

##autocomplete persona
@service.json
def persona_autocomplete(alias_startsWith):
    persona=db((db.persona.is_active==True) & (db.persona.alias.like(alias_startsWith+'%'))).select(db.persona.id,db.persona.alias,orderby='persona.alias',cache=(cache.ram,3600),limitby=(0,10))
    return persona

@service.json
def entity_autocomplete(alias_startsWith,entity):

    if entity=='persona':
        jsonObject=db((db.persona.is_active==True) & (db.persona.alias.like(alias_startsWith+'%'))).select(
            db.persona.id,db.persona.alias,orderby='persona.alias',cache=(cache.ram,3600), limitby=(0,10))
    elif entity=='empresa':
        jsonObject=db((db.Organizacion.is_active==True) & (db.Organizacion.tipoOrg==2) & (db.Organizacion.alias.like(alias_startsWith+'%'))).select(
            db.Organizacion.id,db.Organizacion.alias,orderby='Organizacion.alias',cache=(cache.ram,3600), limitby=(0,10))
    elif entity=='organizacion':
        jsonObject=db((db.Organizacion.is_active==True) & (db.Organizacion.tipoOrg!=2) & (db.Organizacion.alias.like(alias_startsWith+'%'))).select(
            db.Organizacion.id,db.Organizacion.alias,orderby='Organizacion.alias',cache=(cache.ram,3600), limitby=(0,10))
    return jsonObject

def perfil():

    id=""
    alias=request.args(0).decode('utf-8').replace('_',' ')
    person=db.persona(alias=alias)
    response.view='visualizacion/caso_perfil.html'
    if person:
        _id=person.id
        ##redirect(URL('caso_perfil',args=id))
    else: redirect(URL('error','error404'))

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


    return dict(persona=person, _id=_id, form=form, borrar=borrar )
