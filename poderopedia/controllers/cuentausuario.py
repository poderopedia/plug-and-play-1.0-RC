# coding: utf8

def index(): return dict(message="hello from cuentausuario.py")

#TODO _id=1,page=0, sort=0, target=0, entity=0
def configuracion():
    conf='configuracion'
    return dict(form=auth.profile(),conf=conf)

#TODO _id=1,page=0, sort=0, target=0, entity=0
def registrogeneral():
    return dict(_id=1,page=0, sort=0, target=0, entity=0)

#TODO _id=1,page=0, sort=0, target=0, entity=0    
def ingresogeneral():
    form=auth.login()
    form['_class']='form-horizontal'
    form['_formstyle']='divs'
    form.submit_button = 'Enviar'
    return dict(form=form)

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
def notificacionesgenerales():
    conf='notificaciones'
    return dict(_id=1,page=0, sort=0, target=0, entity=0,conf=conf)

#TODO _id=1,page=0, sort=0, target=0, entity=0
def notificacionesindividual():
    return dict(_id=1,page=0, sort=0, target=0, entity=0)

#TODO _id=1,page=0, sort=0, target=0, entity=0
def editaravatar():
    conf='avatar'
    return dict(_id=1,page=0, sort=0, target=0, entity=0,conf=conf)

#TODO _id=1,page=0, sort=0, target=0, entity=0
def editarperfil():
    conf='perfil'
    return dict(_id=1,page=0, sort=0, target=0, entity=0,conf=conf)

#def contrasena():
#    return locals()
