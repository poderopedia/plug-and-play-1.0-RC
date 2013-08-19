# coding: utf8
# intente algo como

def index():
    conf='poderopedia'; 
    general='acercade'
    return dict(conf=conf,general=general)
    
def equipo():
    conf='equipo';
    general='acercade'
    return dict(conf=conf,general=general)
   
def prensa():
    conf='prensa';
    general='acercade'
    return dict(conf=conf,general=general)

def contactanos():
    conf='contacto';
    general='acercade'
    form = SQLFORM.factory(
        Field('nombre', requires=IS_NOT_EMPTY()),
        Field('apellido',requires=IS_NOT_EMPTY()),
        Field('email',requires=IS_NOT_EMPTY()),
        Field('mensaje','text',requires=IS_NOT_EMPTY()),
        Field('compania'),
        Field('telefono'),)    
    if form.accepts(request,session):
        response.flash = 'form accepted'
        mail.send(to=['juan.eduardo@poderopedia.com'],
            cc=['monica@poderopedia.com'],
            bcc=['miguel@poderopedia.com'],
            subject='Formulario de Contacto',
            message='<html><body>Hola<p>Tienes un mensaje de '+form.vars['nombre']+' '+form.vars['apellido']+' </p><p>Su Email es: '+form.vars['email']+'</p><p>Compañia: '+form.vars['compania']+'</p><p> Telefono: '+form.vars['telefono']+'</p><p>Mensaje: '+form.vars['mensaje']+'</p><p>El Equipo de Poderopedia</p><h5>Por favor, no respondas a este mensaje: fue enviado de manera automática por DomoArigatoDiscoRoboto, el robot de mensajería instantánea de Poderopedia. </h5></body></html>',
            headers = {'Content-Type' : 'text/plain; charset="utf-8"'})
        redirect(URL('acercade','contactanos_ok'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form,conf=conf,general=general) 

def contactanos_ok():
    conf='contacto';
    general='acercade'
    return dict(conf=conf,general=general)

def prueba():
    form = SQLFORM.factory(
        Field('name', requires=IS_NOT_EMPTY()),
        Field('image', 'upload'))
    if form.accepts(request.vars, session):
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)                                            
                                    
def condiciones_de_uso():
    conf='condiciones';
    general='acercade'
    return dict(conf=conf,general=general)
    
def politica_de_privacidad():
    conf='politica';
    general='acercade'
    return dict(conf=conf,general=general)
