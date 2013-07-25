@auth.requires_login()
def index():
   case = SQLFORM.grid(db.caso,csv=False)
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
    add_option = SELECT_OR_ADD_OPTION(form_title=T("Agregar Fuentes"), controller="fuentes", function="add_source", button_text = T("Nueva Fuente"))
    #assign widget to field
    db.caso.documentSource.widget = add_option.widget

    #multi-select widget
    #response.files.append(URL('static','js/jquery.multiselect.js'))
    #response.files.append(URL('static','js/jquery.multiselect.filter.js'))
    #response.files.append(URL('static','css/jquery.multiselect.css'))
    #response.files.append(URL('static','css/jquery.multiselect.filter.css'))

    js_script="""<script type="text/javascript">
    $("#caso_documentSource").multiselect({minWidth:600}).multiselectfilter({width:200});
    $("#caso_documentCloud").multiselect({minWidth:600}).multiselectfilter({width:200});
    </script>
    """

    caso_id=request.vars.caso_id or redirect(URL('index'))
    record = db.caso(request.vars.get('caso_id',None))



    form=SQLFORM(db.caso,record)
    if form.process().accepted:
        response.flash = T('formulario aceptado')
    elif form.errors:
        response.flash = T('formulario tiene errores')
    return dict(form=form, caso_id=caso_id, js_script=js_script)

@auth.requires_login()
def person_connection():
    id=request.vars.caso_id or redirect(URL('casos','index'))
    if (request.args(0) == 'new') or (request.args(0)== 'edit'):
        db.person2caso.origenC.default=id
        db.person2caso.origenC.writable=False
    query=db.person2caso.origenC==id
    person_connection = SQLFORM.grid(query,formname='person_connection',csv=False)
    return dict(person_connection=person_connection)

@auth.requires_login()
def orgs_connection():
    id=request.vars.caso_id or redirect(URL('casos','index'))
    if (request.args(0) == 'new') or (request.args(0)== 'edit'):
        db.org2caso.origenC.default=id
        db.org2caso.origenC.writable=False
    query=db.org2caso.origenC==id
    orgs_connection = SQLFORM.grid(query,formname='orgs_connection', csv=False)
    return dict(orgs_connection=orgs_connection)