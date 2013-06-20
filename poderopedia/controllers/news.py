# coding: utf8
# intente algo como

def index():
    return locals()
    
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


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

#@auth.requires_login()
#@auth.requires_membership('administrator')

def news():
    import random
    from conversion import convert_latin_chars
    if request.cid==None: redirect(URL('error','error404'))
    alias=direccion=None; lista=[]; short=None; error=None

    aleatorio = random.randint(1,2) #1 empresas 2 organizaciones 3 casos, como no hay casos solo se tiene que agregar mas adelante
    principal = db(db.destacados.is_active == True).select(orderby="destacados.fecha DESC",limitby=(0,1),cache=(cache.ram,15)).first()
    secundarios = db(db.destacados.is_active == True).select(orderby="destacados.fecha DESC",limitby=(1,3),cache=(cache.ram,15))
    carrusel = db(db.destacados.is_active == True).select(orderby="destacados.fecha DESC",limitby=(3,9),cache=(cache.ram,15))
    resto = db(db.destacados.is_active == True).select(orderby="destacados.fecha DESC",limitby=(9,13),cache=(cache.ram,15))

    personas = db((db.persona.is_active==True) & (db.persona.shortBio!=None) & (db.persona.shortBio!='')
        & (db.persona.depiction!=None) & (db.persona.depiction!='')).select(
        db.persona.alias,db.persona.shortBio,db.persona.depiction,db.persona.created_on,
        orderby=[~db.persona.modified_on],limitby=(0,2))

    organizacion = db((db.Organizacion.is_active==True) & (db.Organizacion.shortBio!=None) & (db.Organizacion.shortBio!='')
        & (db.Organizacion.haslogo!=None) & (db.Organizacion.haslogo!='')).select(
        db.Organizacion.id,db.Organizacion.tipoOrg,
        db.Organizacion.alias,db.Organizacion.shortBio,db.Organizacion.haslogo,db.Organizacion.created_on,
        orderby=[~db.Organizacion.modified_on],limitby=(0,2))

    url={}
    for org in organizacion:
        url[org.id]=URL('organizaciones','conexiones',args=convert_latin_chars(org.alias),extension=False)
        if org.tipoOrg==2:
            url[org.id]=URL('empresas','conexiones',args=convert_latin_chars(org.alias),extension=False)

    shortBio={}
    for news in resto:

        if (news.referenceEntity!=None) & (news.reference!=None):
            shortBio[news.referenceEntity[:1]+'_'+str(news.reference)]='maluenda'
            if news.referenceEntity=='persona':
                entity=db.persona(id=news.reference)
            elif (news.referenceEntity=='empresa') | (news.referenceEntity=='organizacion'):
                entity=db.Organizacion(id=news.reference)
            if entity!=None:
                shortBio[news.referenceEntity[:1]+'_'+str(news.reference)]=p.sub('',entity.shortBio)[:184]
    
    if aleatorio == 1:
        random = db((db.persona.is_active==True)&(db.persona.shortBio!='')).select(db.persona.alias, orderby='<random>',limitby=(0,1),cache=(cache.ram,15)).first()
        if random:
            direccion = URL('personas','conexiones',args=convert_latin_chars(random.alias),extension=False)
    else:
        random = db((db.Organizacion.is_active==True)&(db.Organizacion.shortBio!='')).select(db.Organizacion.alias, db.Organizacion.tipoOrg,orderby='<random>',limitby=(0,1),cache=(cache.ram,15)).first()
        if random:
            direccion = URL('organizaciones','conexiones',args=convert_latin_chars(random.alias),extension=False)
            if random.tipoOrg==2:
                direccion=URL('empresas','conexiones',args=convert_latin_chars(random.alias),extension=False)

    


    return dict(random=random,direccion=direccion,url=url,principal=principal,
        secundarios=secundarios,carrusel=carrusel,resto=resto,alias=lista, shortBio=shortBio,
        personas=personas,organizacion=organizacion)
   
    


