@auth.requires_login()
def index():
   caso = SQLFORM.grid(db.caso,csv=False)
   if request.args(0) == 'edit':
       redirect(URL('edit',vars=dict(caso_id=request.args(2))))

   return locals()

@auth.requires_login()
def create():
    form=SQLFORM(db.caso)
    if form.process().accepted:
        response.flash = T('formulario aceptado')
    elif form.errors:
        response.flash = T('formulario tiene errores')
    return dict(form=form)

@auth.requires_login()
def edit():
    #Initialize the widget
    add_option = SELECT_OR_ADD_OPTION(form_title=T("Agregar Fuentes"), controller="fuentes", function="add_fuentes", button_text = T("Nueva Fuente"))
    #assign widget to field
    db.caso.documentSource.widget = add_option.widget


    caso_id=request.vars.caso_id or redirect(URL('index'))
    record = db.caso(request.vars.get('caso_id',None))



    form=SQLFORM(db.caso,record)
    if form.process().accepted:
        response.flash = T('formulario aceptado')
    elif form.errors:
        response.flash = T('formulario tiene errores')
    return dict(form=form, caso_id=caso_id)

@auth.requires_login()
def conex_persona():
    id=request.vars.caso_id or redirect(URL('casos','index'))
    if (request.args(0) == 'new') or (request.args(0)== 'edit'):
        db.person2caso.origenC.default=id
        db.person2caso.origenC.writable=False
    query=db.person2caso.origenC==id
    conex_persona = SQLFORM.grid(query,formname='conex_persona',csv=False)
    return dict(conex_persona=conex_persona)

@auth.requires_login()
def conex_orgs():
    id=request.vars.caso_id or redirect(URL('casos','index'))
    if (request.args(0) == 'new') or (request.args(0)== 'edit'):
        db.org2caso.origenC.default=id
        db.org2caso.origenC.writable=False
    query=db.org2caso.origenC==id
    conex_orgs = SQLFORM.grid(query,formname='conex_orgs', csv=False)
    return dict(conex_orgs=conex_orgs)