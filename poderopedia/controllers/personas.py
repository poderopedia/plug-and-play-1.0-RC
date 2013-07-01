__author__ = 'Evolutiva'
#!/usr/bin/python
# -*- coding: utf-8 -*-
# cache resolved

def index():
    id=""
    alias=request.args(0)or redirect(URL('error','error404'))
    alias=alias.decode('utf-8').replace('_',' ')
    tab=request.args(1)

    person=db.persona(alias=alias,is_active=True)
    response.view='visualizacion/caso_perfil.html'
    if person:
        _id=person.id
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


    return dict(persona=person, _id=_id, form=form, borrar=borrar)



def perfil():

    id=""
    alias=request.args(0) or redirect(URL('error','error404'))
    alias=alias.decode('utf-8').replace('_',' ')
    person=db.persona(alias=alias,is_active=True)
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


    return dict(persona=person, _id=_id, form=form, borrar=borrar)


def conexiones():

    id=""
    alias=request.args(0) or redirect(URL('error','error404'))
    alias=alias.decode('utf-8').replace('_',' ')
    person=db.persona(alias=alias,is_active=True)
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


    return dict(persona=person, _id=_id, form=form, borrar=borrar)

@cache(request.env.path_info,time_expire=10,cache_model=cache.ram)
def personasrelacionadas():
    response.view='persona/personasrelacionadas.html'

    alias=request.args(0) or redirect(URL('error','error404'))
    alias=alias.decode('utf-8').replace('_',' ')
    persona=db.persona(alias=alias,is_active=True)

    if persona:
        _id=persona.id
        ##redirect(URL('caso_perfil',args=id))
    else: redirect(URL('error','error404'))

    return dict(_id=_id, persona=persona)

@cache(request.env.path_info,time_expire=10,cache_model=cache.ram)
def empresasrelacionadas():
    response.view='persona/empresasrelacionadas.html'

    alias=request.args(0) or redirect(URL('error','error404'))
    alias=alias.decode('utf-8').replace('_',' ')
    persona=db.persona(alias=alias,is_active=True)

    if persona:
        _id=persona.id
        ##redirect(URL('caso_perfil',args=id))
    else: redirect(URL('error','error404'))

    return dict(_id=_id, persona=persona)

@cache(request.env.path_info,time_expire=10,cache_model=cache.ram)
def organizacionesrelacionadas():
    response.view='persona/organizacionesrelacionadas.html'
    alias=request.args(0) or redirect(URL('error','error404'))
    alias=alias.decode('utf-8').replace('_',' ')


    persona=db.persona(alias=alias,is_active=True)

    if persona:
        _id=persona.id
        ##redirect(URL('caso_perfil',args=id))
    else: redirect(URL('error','error404'))

    return dict(_id=_id, persona=persona)

def documentos():
    from gluon.storage import Storage
    from conversion import convert_latin_chars


    response.view='default/documentos.html'

    alias=request.args(0)  or redirect(URL('default','index'))
    alias=alias.decode('utf-8').replace('_',' ')

    dc_title=request.args(1) or redirect(URL('default','index'))
    dc_title=dc_title.decode('utf-8').replace('_',' ').replace('-','.')


    imagen=IMG(_alt=alias, _src=URL('static','img/default-pic-profile-person.png'))
    href=''


    person= db.persona(alias=alias,is_active=True)
    if person:
        controller='personas'; href='conexiones'
        imagen=IMG(_alt=person.alias,_src=URL('static','img/default-pic-profile-person.png'),_height=44)
        _id=person.id
        if person.depiction!=None:
            imagen=IMG(_alt=person.alias,_src=URL('default','fast_download',args=person.depiction),_height=44)
        args=convert_latin_chars(person.alias)
    else:
        redirect(URL('error','error404'))




    dc_document=db.documentCloud(title=dc_title,is_active=True)
    if dc_document:
        title=dc_document.title
        dc_args_title=convert_latin_chars(title)
        dc_id=dc_document.dc_id
    else:
        redirect(URL('error','error404'))

    response.title=person.alias + '|' + title + ' Poderopedia'
    entity=Storage({'id':_id,'alias':alias,'logo':imagen,'controller':controller,
                    'target':href,'args':args,'dc_args':dc_args_title})

    return dict(dc_id=dc_id,_id=_id,page=0,sort='false',entity=entity,title=title)


def mapa_relaciones():


    alias=request.args(0) or redirect(URL('error','error404'))
    alias=alias.decode('utf-8').replace('_',' ')

    response.view='visualizacion/MapasAll.html'

    person=None
    imagen=IMG(_alt=alias, _src=URL('static','img/default-pic-profile-person.png'))
    person=db.persona(alias=alias,is_active=True)

    if person:
        _id=person.id
        response.title = person.alias+' | Visualización | Poderopedia'
        if (person.shortBio!=None)&(person.shortBio!=''):
            response.meta.description= person.shortBio[:200]
        if (person.depiction!=None):
            imagen=IMG(_alt=person.alias,_src=URL('default','download',args=person.depiction),_height=44)
    else:
        redirect(URL('error','error404'))

    return dict(_id=_id,person=person,imagen=imagen)
