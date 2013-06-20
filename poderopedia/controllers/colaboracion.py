# coding: utf8
__author__ = 'Evolutiva'


def actualizacion():
    response.view='visualizacion/tipoinadecuado.load'
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

    form=SQLFORM(db.actualizacion)
    form.vars.referenceEntity=tabla
    form.vars.reference=_id
    #form.vars.tipoError='contenidoInadecuado'


    if form.process().accepted:
        response.flash = 'Formulario Aceptado'

        mail.send(to=['juan.eduardo@poderopedia.com'],
            cc=['monica@poderopedia.com'],
            bcc=['miguel@poderopedia.com'],
            subject='Requiere Actualizacion en '+var,
            # If reply_to is omitted, then mail.settings.sender is used
            #reply_to='us@example.com',
            message='El usuario "'+nombre+'" de email "'+email+'", indicó se requiere actualización en: '+var+', debido a: '+form.vars['contenido']+'" y obtuvo la informacion desde la siguiente URL '+form.vars['URL']+'.',
            headers = {'Content-Type' : 'text/plain; charset="utf-8"'})
        redirect(URL('actualizacion',args=[_id,tabla],vars={'success':'ok'}))
    elif form.errors:
        response.flash = 'Error en el Formulario'


    return dict(title_message='Requiere Actualización',item=rows,form=form,tabla=tabla)