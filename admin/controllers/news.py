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

@auth.requires_login()
@auth.requires_membership('administrator')
def destacados():
    grid = SQLFORM.grid(db.destacados,orderby=~db.destacados.fecha,formstyle = 'table3cols')
    return dict(grid=grid)
   
    

@auth.requires_login()
@auth.requires_membership('administrator')
def news_insert():
    form=SQLFORM(db.destacados)
    if form.process().accepted:
        response.flash = 'Formulario aceptado'
    elif form.errors:
        response.flash = 'Hay errores en el formulario'
    else:
        response.flash = 'Por favor llene el formulario'
    return dict(form=form)
    
@auth.requires_login()
@auth.requires_membership('administrator')
def news_update():
    _id=request.args(0) or redirect (URL('news'))
    news=db.destacados(_id)
    form=SQLFORM(db.destacados,news)
    if form.process().accepted:
        response.flash = T('Formulario aceptado')
    elif form.errors:
        response.flash = T('Hay errores en el formulario')
    else:
        response.flash = T('Por favor llene el formulario')
    return dict(form=form,_id=0)


@service.json
def entity_autocomplete(alias_startsWith,entity):
    jsonObject=''
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
