# -*- coding: utf-8 -*-

##controlador de la opción de republicar contenidos
##requiere pixel-ping instalado y corriendo
##se debe configurar settings en 0.py
##parametro: setting.pixel_ping
##para generación de analiticas

## visualizacion / mapa de relaciones
## crea vista especifica para poder embeder el contenido

def mapa_relaciones():
    alias=request.args(1)or redirect(URL('error','error404'))
    alias=alias.decode('utf-8').replace('_',' ')
    entity=request.args(0)
    if entity=='persona':
        person=db.persona(alias=alias,is_active=True)
        if person:
            _id=person.id
        else: redirect(URL('error','error404'))
    else:
        orgs=db.Organizacion(alias=alias,is_active=True)
        if orgs:
            _id=orgs.id
        else: redirect(URL('error','error404'))

    return dict(_id=_id,entity=entity)

def entity():
    _id=request.args(0) or redirect(URL('error','error404'))
    entity=request.args(1)
    if entity=='persona':
        entidad = db.persona(id=_id, is_active=True)
    else:
        entidad = db.Organizacion(id=_id, is_active=True)


    return dict(_id=_id, entity=entidad)

def mapa_lightbox():
    cid=request.cid or redirect(URL('error','error404.load'))
    alias=request.args(0) or redirect('error','error.load')
    entity = request.args(1)
    return dict(alias=alias,entity=entity)
