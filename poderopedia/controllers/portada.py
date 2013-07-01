# coding: utf8
# intente algo como

def download():
        return response.download(request,db)

#Enlista los ultimos insertados en perfil, empresas, organizaciones y casos.
def last_inserts():
    from gluon.tools import prettydate

    row1 = db((db.persona.created_on != None)&(db.persona.shortBio != '')&(db.persona.is_active == True)).select(db.persona.id,db.persona.alias,db.persona.created_on,db.persona.depiction,orderby="persona.created_on DESC",limitby=(0,15),cache=(cache.ram,3600))
    lista1 = []
    for item in row1:
        pretty_d = item.created_on.strftime('%d-%m-%Y')
        lista1.append((item.id, item.alias, item.created_on,item.depiction,'Persona',pretty_d))
        
    row2 = db((db.Organizacion.created_on != None)&(db.Organizacion.tipoOrg != '2')&(db.Organizacion.shortBio != '')&(db.Organizacion.is_active == True)).select(db.Organizacion.id,db.Organizacion.alias,db.Organizacion.created_on,db.Organizacion.haslogo,orderby="Organizacion.created_on DESC",limitby=(0,15),cache=(cache.ram,3600))
    for item in row2:
        pretty_d = item.created_on.strftime('%d-%m-%Y')
        lista1.append((item.id, item.alias, item.created_on,item.haslogo,'Organizacion',pretty_d))
    
    row3 = db((db.caso.created_on != None)&(db.caso.is_active == True)).select(
        db.caso.id,
        db.caso.name,
        db.caso.created_on,
        db.caso.depiction,
        orderby="caso.created_on DESC",limitby=(0,15),cache=(cache.ram,3600))

    for item in row3:
        pretty_d = item.created_on.strftime('%d-%m-%Y')
        lista1.append((item.id, item.name, item.created_on,item.depiction,'Caso', pretty_d))

    row4 = db((db.Organizacion.created_on != None)&(db.Organizacion.tipoOrg == '2')&(db.Organizacion.shortBio != '')&(db.Organizacion.is_active == True)).select(db.Organizacion.id,db.Organizacion.alias,db.Organizacion.created_on,db.Organizacion.haslogo,orderby="Organizacion.created_on DESC",limitby=(0,15),cache=(cache.ram,3600))
    for item in row4:
        pretty_d = item.created_on.strftime('%d-%m-%Y')
        lista1.append((item.id, item.alias, item.created_on,item.haslogo,'Empresa', pretty_d))
                        
    lista=sorted(lista1, key=lambda fecha: fecha[2], reverse=True)
    lista=lista[:5]
    return dict(lista=lista)


#Enlista las ultimas modificaciones que se hisieron en perfil, empresas, organizaciones y casos.
def last_update():
    from gluon.tools import prettydate
    row1 = db((db.persona.modified_on != None)&(db.persona.shortBio != '')&(db.persona.is_active == 'T')).select(db.persona.id,db.persona.alias,db.persona.modified_on,db.persona.depiction,orderby="persona.modified_on DESC",limitby=(0,15),cache=(cache.ram,3600))
    lista1 = []
    for item in row1:
        pretty_d = item.modified_on.strftime('%d-%m-%Y')
        lista1.append((item.id, item.alias, item.modified_on, item.depiction,'Persona', pretty_d))
        
    row2 = db((db.Organizacion.modified_on != None)&(db.Organizacion.tipoOrg != '2')&(db.Organizacion.shortBio != '')&(db.Organizacion.is_active == 'T')).select(db.Organizacion.id,db.Organizacion.alias,db.Organizacion.modified_on,db.Organizacion.haslogo,orderby="Organizacion.modified_on DESC",limitby=(0,15),cache=(cache.ram,3600))
    for item in row2:
        pretty_d = item.modified_on.strftime('%d-%m-%Y')
        lista1.append((item.id, item.alias, item.modified_on,item.haslogo,'Organizacion', pretty_d))
    
    row3 = db((db.caso.modified_on != None)&(db.caso.is_active == 'T')).select(
        db.caso.id,
        db.caso.name,
        db.caso.modified_on,
        db.caso.depiction,
        orderby="caso.modified_on DESC",limitby=(0,15),cache=(cache.ram,3600))

    for item in row3:
        pretty_d = item.modified_on.strftime('%d-%m-%Y')
        lista1.append((item.id, item.name, item.modified_on,item.depiction,'Caso', pretty_d))

    row4 = db((db.Organizacion.modified_on != None)&(db.Organizacion.tipoOrg == '2')&(db.Organizacion.shortBio != '')&(db.Organizacion.is_active == 'T')).select(db.Organizacion.id,db.Organizacion.alias,db.Organizacion.modified_on,db.Organizacion.haslogo,orderby="Organizacion.created_on DESC",limitby=(0,15),cache=(cache.ram,3600))
    for item in row4:
        pretty_d = item.modified_on.strftime('%d-%m-%Y')
        lista1.append((item.id, item.alias, item.modified_on,item.haslogo,'Empresa', pretty_d))
                        
    lista=sorted(lista1, key=lambda fecha: fecha[2], reverse=True)
    lista=lista[:5]
    
    return dict(lista=lista)
    

#TODO saber que es lo que se esta preguntado para hacer la consulta a la tabla correspondiente.
def last_today():
    import datetime
    import time
    today = datetime.date.today()
    return dict(today = today)
    

#TODO saber que es lo que se esta preguntado para hacer la consulta a la tabla correspondiente.    
def last_weeks():
    import datetime
    import time
    today = datetime.date.today()
    one_week = datetime.timedelta(weeks = 1)
    now = today - one_week
    return dict(now = now)
    

#TODO saber que es lo que se esta preguntado para hacer la consulta a la tabla correspondiente.
def last_month():
    import datetime
    import time
    today = datetime.date.today()
    one_month = datetime.timedelta(weeks = 4)
    now = today - one_month
    return dict(now = now)

#Cuenta las personas, las empresas, las organizaciones y los casos totales del sistema        
def count_entity():
    personas = db(db.persona.is_active==True).count()
    empresas = db((db.Organizacion.tipoOrg == '2') & (db.Organizacion.is_active==True)).count()
    casos = db(db.caso.is_active==True).count()
    organizaciones = db((db.Organizacion.tipoOrg != '2') & (db.Organizacion.is_active==True)).count()
    return dict(personas=personas, empresas=empresas, casos=casos, organizaciones=organizaciones)



def tengo_datos():
   form = SQLFORM(db.tengoDato, submit_button = 'Enviar',labels = {'entity':'Entidad'})
   if form.process().accepted:
       response.flash = 'Gracias por colaborar con nosotros'

       mail.send(to=['juan.eduardo@poderopedia.com'],
            cc=['monica@poderopedia.com'],
            bcc=['miguel@poderopedia.com'],
            subject='Tengo un Dato de '+form.vars['nombre'],
            # If reply_to is omitted, then mail.settings.sender is used
            #reply_to='us@example.com',
            message='Un usuario sugirio una dato de "'+form.vars['nombre']+'", la informacion exclusiva es "'+form.vars['contenido']+'" y obtuvo la informacion desde la siguiente URL '+form.vars['URL']+'.' ,
            headers = {'Content-Type' : 'text/plain; charset="utf-8"'})
       redirect(URL('tengo_datos',vars={'success':'ok'}))      
   elif form.errors:
       response.flash = 'Debe ingresar todos los datos'
   else:
       response.flash = 'Debe completar el Formulario'
   return dict(form=form)
   
##TODO construir funcion completa
def sugerir_perfil():
   form = SQLFORM(db.sugerirPerfil, submit_button = 'Enviar',labels = {'entity':'Entidad'})
   if form.process().accepted:
       response.flash = 'form accepted'
   elif form.errors:
       response.flash = 'form has errors'
   else:
       response.flash = 'please fill out the form'
   return dict(form=form)
