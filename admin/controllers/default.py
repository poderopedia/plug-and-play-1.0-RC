# coding: utf8
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires



##TODO: revisar auth.archive y desagregar Persona/Organizacion/Empresa en sus respectivos controladores
def index():
    return dict()

def error():
    return dict()

@auth.requires_login()
@service.json
def delete(table,id):
    data=None
    if(auth.has_membership('administrator')):
        if(table in ('persona','relFamiliar','relPersona','RelPersOrg','Organizacion','relOrg2Org')):
            record=db[table](id)
            try:
                record.update_record(is_active=False)
            except NotImplementedError:
                raise NotImplementedError(T('Aún no pueden serializarse lists y dicts'))
            if(table=='persona'):
                data=str(id)
            elif table=='relFamiliar':
                data='fam'+str(id)
            elif table=='relPersona':
                data='pers'+str(id)
            elif table=='RelPersOrg':
                data='orgs'+str(id)
            elif table=='relOrg2Org':
                data='relOrg2Org'+str(id)
            elif table=='Organizacion':
                data=str(id)
    return data

@auth.requires_login()
def perfil():
    class Virtual(object):
        @virtualsettings(label=T('Editar Perfil'))
        def editar(self):          
            picture=A('editar', _href=URL('persona', args=self.persona.id))
            return picture
        @virtualsettings(label=T('Eliminar'))
        def delete(self):
            if(auth.has_membership('administrator')):
                return TAG.BUTTON(T('Eliminar'),_class='deletebutton',_onclick='deleteRow(event,"persona",%s);' % self.persona.id)
            else:
                return ""
    if(request.args(0)>0):
        datasource=db(db.persona.id==request.args(0)).select()
    else:
        datasource=db(db.persona.is_active==True).select(cache=(cache.ram,10))
    table = plugins.powerTable
    table.bStateSave= True
    table.iCookieDuration=400
    table.datasource = datasource
    table.headers = 'labels'
    table.dtfeatures['sScrollY'] = '100%'
    table.uitheme = 'redmond'
    table.virtualfields = Virtual()
    table.keycolumn = 'persona.id'
    table.columns = ['persona.alias','persona.firstName','persona.firstLastName','persona.otherLastName',
                     'virtual.editar','virtual.delete']
    table.showkeycolumn = False 
    table.extra = dict(autoresize={},
                             tooltip={'persona.alias'},
                             details={'detailscolumns':'relFamiliar.id,tipoParentesco.name,persona.alias',                                                 
                             'detailscallback':URL('default','familydetails')
                             })
    
    table = table.create()
    return dict(table=table)

@auth.requires_login()
def perfil_listar():
    fields=(db.persona.id,db.persona.alias,db.persona.depiction,db.persona.firstName,
            db.persona.firstLastName, db.persona.otherLastName,db.persona.shortBio,db.persona.longBio)
    grid=SQLFORM.grid((db.persona.is_active==True),fields=fields)
    return dict(grid=grid)

@auth.requires_login()
def manage_users():
    query=(db.persona.is_active==True)
    fields=(db.persona.id,db.persona.alias,db.persona.firstName,
            db.persona.firstLastName, db.persona.otherLastName)
    grid = SQLFORM.grid(query,fields=fields)
    return dict(grid=grid)

@auth.requires_login()
@service.json
def persona_eliminar(id):
    if auth.has_membership('administrator'):
        record=db.persona(id)
        return record.update_record(is_active=False)
    return False

@auth.requires_login()
def formwizard():

    # STEPS: A dict with fields for each step
    mysteps = [dict(title=T('Datos Básicos'),fields=['firstName','firstLastName', 'otherLastName','alias',
                                                  'shortBio','countryofResidence', 'depiction']),
               dict(title=T('Más Información'),fields=['Mainsector','birth','isDead','shortBio']),
               dict(title=T('Redes Sociales'),fields=['web','twitterNick','facebookNick','linkedinNick']),              
               dict(title=T('Perfil Largo'),fields=['longBio'])
            
              ]
    # IMPORT: Import the module
    from plugin_PowerFormWizard import PowerFormWizard
    # CREATE: Create the form object just like the SQLFORM
    form = PowerFormWizard(db.persona, steps=mysteps, options=dict(validate=True))
    if(request.args(0)):
        record=db.persona(request.args(0))
        mysteps = [dict(title=T('Datos Básicos'),fields=['id','firstName','firstLastName', 'otherLastName','alias', 'shortBio','countryofResidence', 'depiction']),
                   dict(title=T('Más Información'),fields=['Mainsector','birth','isDead','shortBio']),
                   dict(title=T('Redes Sociales'),fields=['web','twitterNick','facebookNick','linkedinNick']),
                   dict(title=T('Perfil Largo'),fields=['longBio'])

        ]
        form = PowerFormWizard(db.persona, steps=mysteps, options=dict(validate=True), record=record)

    
    # VALIDATE: web2py form validation
    if form.accepts(request.vars, session):
        response.flash = T('Registro Insertado!')
    elif form.errors: 
        form.step_validation() # VERY IMPORTANT FOR VALIDATION!!!!
        response.flash = T('Hay errores en el formulario')
    
    # Enjoy!
    return dict(form=form)

@auth.requires_login()
def perfil_create():
    db.perfiles.dueno.default=auth.user.id
    db.perfiles.postedon.default=request.now
    form = crud.create(db.perfiles, next='perfil')
    form[0][-1][1].append(TAG.BUTTON('Cancel', _onclick="document.location='%s';"%URL('index')))
    return locals()

@auth.requires_login()
def mapa():
    mapa = db(db.mapas.is_active==True).select(orderby=db.mapas.label)
    return locals()

@auth.requires_login()
def caso():
    caso = SQLFORM.grid(db.caso)
    return locals()

@auth.requires_login()
def casos_create():

    form = SQLFORM(db.casos)
    if form.process().accepted:
        response.flash = T('Formulario aceptado')
    elif form.errors:
        response.flash = T('Hay errores en el formulario')
    return dict(form=form)

@auth.requires_login()
def casos_edit():
    record = db.casos(request.args(0)) or redirect(URL('perfil'))
    form = SQLFORM(db.persona, record)
    if form.process().accepted:
        response.flash = T('Formulario aceptado')
    elif form.errors:
        response.flash = T('Hay errores en el formulario')
    return dict(form=form)

@auth.requires_login()
def persona():

    #Initialize the widget
    add_option = SELECT_OR_ADD_OPTION(form_title=T("Agregar Fuentes"), controller="fuentes", function="add_fuentes", button_text = T("Nueva Fuente"))
    #assign widget to field
    db.persona.documentSource.widget = add_option.widget

    #Initialize the widget
    add_option_document = SELECT_OR_ADD_OPTION(form_title=T("Agregar Documento"), controller="document",
                                               function="add_document", button_text = T("Nuevo Documento"),
                                               dialog_width=600)
    #assign widget to field
    db.persona.documentCloud.widget = add_option_document.widget

    record = db.persona(request.args(0)) or redirect(URL('perfil'))



    form = SQLFORM(db.persona, record)
    if record.shortBio!=None:
        form.vars.shortBio=record.shortBio.replace('&nbsp_place_holder;','').replace('_place_holder;', '')
    if record.longBio!=None:
        form.vars.longBio=record.longBio.replace('&nbsp_place_holder;','').replace('_place_holder;', '')
    if form.validate():
        if form.vars.shortBio!=None:
            form.vars.shortBio = form.vars.shortBio.replace('&nbsp_place_holder;','').replace('\n', '').replace('_place_holder;', '')
        if form.vars.longBio!=None:
            form.vars.longBio = form.vars.longBio.replace('&nbsp_place_holder;','').replace('\n', '').replace('_place_holder;', '')
        id = record.update_record(**db.persona._filter_fields(form.vars))
        form.vars.id=record.id
        auth.archive(form)
        ##if form.process(onsuccess=auth.archive).accepted:
        response.flash = T('Formulario aceptado')
    elif form.errors:
        response.flash = T('Hay errores en el formulario')
        

    return dict(form=form, _id=request.args(0))

@auth.requires_login()
def conexiones():
    record = db.persona(request.args(0)) or redirect(URL('perfil'))
    form = SQLFORM(db.persona, record)
    if form.process().accepted:
        response.flash = T('Formulario aceptado')
    elif form.errors:
        response.flash = T('Hay errores en el formulario')
        
    #conexiones economicas
    class VirtualEco(object):
        @virtualsettings(label=T('Editar'))
        def editar(self):          
            picture=A('editar', _href=URL('relorgs_edit', args=self.RelPersOrg.id))
            return picture
    
    datasource=db((db.RelPersOrg.origenP==record.id) & (db.RelPersOrg.is_active==True) & (db.RelPersOrg.specificRelation==db.tipoRelacionP20.id) &
                  (db.RelPersOrg.destinoO==db.Organizacion.id)& (db.RelPersOrg.origenP==db.persona.id)).select()
    table = plugins.powerTable
    table.datasource = datasource
    table.headers = 'labels'
    table.dtfeatures['sScrollY'] = '100%'
    table.virtualfields = VirtualEco()
    table.keycolumn = 'RelPersOrg.id'
    table.columns = ['RelPersOrg.id','persona.alias','tipoRelacionP20.relationship','Organizacion.name','virtual.editar']
    table.showkeycolumn = False 
    
    table = table.create()
    
    return dict(form=form,table=table)


@auth.requires_login()
def relorgs_edit():
    from gluon.serializers import json
    from fechas import fechas

    db.RelPersOrg.destinoO.requires=None
    
    record = db.RelPersOrg(request.args(0)) or redirect(URL('perfil'))

    #Initialize the widget
    add_option = SELECT_OR_ADD_OPTION(form_title=T("Agregar Fuentes"), controller="fuentes", function="add_fuentes", button_text = T("Nueva Fuente"))
    #assign widget to field
    db.RelPersOrg.documentSource.widget = add_option.widget


    _id=record.origenP; perfil='persona'; back_controller='personas'
    if(request.args(1)=='org'):
        _id=record.destinoO; perfil='Organizacion'; back_controller='organizations'
        org = db.Organizacion(_id)
        if org.tipoOrg==2:
            back_controller = 'companies'


    
    
    form = SQLFORM(db.RelPersOrg, record)
    if form.validate():
        form.vars.is_active='T'
        form.vars.fdesde=fechas(form.vars.iniDay,form.vars.iniMonth,form.vars.iniYear)
        form.vars.fhasta=fechas(form.vars.finDay,form.vars.finMonth,form.vars.finYear)
        if(form.vars.destinoO==""):
            if(form.vars._autocomplete_Organizacion_alias_aux!=""):
                parent=db(db.tipoRelacionP20.id==form.vars.specificRelation).select().first()
                tipoOrg=db(db.tipoOrganizacion.generalizacion==parent.parent).select().first()
                form.vars.tipoOrg=12
                if(tipoOrg!=None):
                    form.vars.tipoOrg=tipoOrg.id
                form.vars.name=form.vars._autocomplete_Organizacion_alias_aux
                form.vars.alias=form.vars._autocomplete_Organizacion_alias_aux
                form.vars.countryOfResidence=44
                idO = db.Organizacion.insert(**db.Organizacion._filter_fields(form.vars))
                if(idO!=None):
                    form.vars.destinoO=idO
                    form.vars.id=record.id
                    auth.archive(form)
                    id = record.update_record(**db.RelPersOrg._filter_fields(form.vars))
                    response.flash=T('Formulario aceptado')
                    
            else:
                response.flash=T('Debe Ingresar un grupo')  
        else:
            form.vars.id=record.id
            auth.archive(form)
            id = record.update_record(**db.RelPersOrg._filter_fields(form.vars))
            response.flash=T('Formulario aceptado')
        ##redirect(URL('perfil'))
    elif form.errors:
        response.flash = T('Hay errores en el formulario')
        
    tree={}
    options=db(db.tipoRelacionP20.parent==0).select(orderby=db.tipoRelacionP20.relationship)
    for option in options:
        tree[str(option.id)]=T(option.relationship)
    
    ##db.RelPersOrg.hasdocument.default=1
    default=db(db.tipoRelacionP20.id==record.specificRelation).select().first()
    pordefecto='"'+str(default.id)+'"'
    if(default.parent!=0):
        ##parent=db(db.tipoRelacionP20.id==default.parent).select().first()
        pordefecto='"'+str(default.parent)+'", "'+str(default.id)+'"'

    back_button = A(TAG.BUTTON(T('Volver'),_class='button'),_href=URL(back_controller,'index',vars=dict(keywords=perfil+'.id="'+str(_id)+'"')))
    
    return dict(form=form, option_tree=json(tree), default=pordefecto, _id=record.id,
        record='RelPersOrg', back=_id,perfil=perfil, back_button=back_button)

## agrega conexion    
@auth.requires_login()
def relorgs_create():
    from gluon.serializers import json
    from fechas import fechas

    #se quita validacion en destinoO para permitir el ingreso de un nuevo registro persona a partir del campo autocomplete
    db.RelPersOrg.destinoO.requires=None

    #Initialize the widget
    add_option = SELECT_OR_ADD_OPTION(form_title=T("Agregar Fuentes"), controller="fuentes", function="add_fuentes", button_text = T("Nueva Fuente"))
    #assign widget to field
    db.RelPersOrg.documentSource.widget = add_option.widget

    ##persona = db.persona(request.args(0))
    db.RelPersOrg.origenP.default = request.args(0)
    db.RelPersOrg.destinoO.default = request.args(2)
    default_args= request.args(1) or 11

    _id=request.args(0); perfil='persona'; back_controller='personas'
    if(request.args(2)):
        _id=request.args(2); perfil='Organizacion'; back_controller='organizations'
        org =db.Organizacion(_id)
        if org.tipoOrg==2:
            back_controller='companies'



    ##form=SQLFORM.factory(db.RelPersOrg,db.document)
    form=SQLFORM(db.RelPersOrg)
    if form.validate():
        form.vars.fdesde=fechas(form.vars.iniDay,form.vars.iniMonth,form.vars.iniYear)
        form.vars.fhasta=fechas(form.vars.finDay,form.vars.finMonth,form.vars.finYear)
        form.vars.is_active='T'
        if(form.vars.destinoO==""):
            if(form.vars._autocomplete_Organizacion_alias_aux!=""):
                parent=db(db.tipoRelacionP20.id==form.vars.specificRelation).select().first()
                tipoOrg=db(db.tipoOrganizacion.generalizacion==parent.parent).select().first()
                form.vars.tipoOrg=12
                if(tipoOrg!=None):
                    form.vars.tipoOrg=tipoOrg.id
                form.vars.name=form.vars._autocomplete_Organizacion_alias_aux
                form.vars.alias=form.vars._autocomplete_Organizacion_alias_aux
                form.vars.countryOfResidence=44
                idO = db.Organizacion.insert(**db.Organizacion._filter_fields(form.vars))
                if(idO!=None):
                    form.vars.destinoO=idO
                    id = db.RelPersOrg.insert(**db.RelPersOrg._filter_fields(form.vars))
                    response.flash=T('Formulario aceptado')
                    
            else:
                response.flash=T('Debe Ingresar un grupo')  
        else:
            id = db.RelPersOrg.insert(**db.RelPersOrg._filter_fields(form.vars))
            ##redirect(URL('default','persona'))
        ##redirect(URL('relorgs_edit',args=record.id))
        ##response.flash = T('form accepted'+form.vars.destinoO)
    elif form.errors:
        response.flash = T('Hay errores en el formulario')

    tree={}
    options=db(db.tipoRelacionP20.parent==0).select(orderby=db.tipoRelacionP20.relationship)
    for option in options:
        tree[str(option.id)]=T(option.relationship)

    default=db(db.tipoRelacionP20.id==default_args).select().first()
    pordefecto='"'+str(default.id)+'"'
    if(default.parent!=0):
        ##parent=db(db.tipoRelacionP20.id==default.parent).select().first()
        pordefecto='"'+str(default.parent)+'", "'+str(default.id)+'"'

    back_button = A(TAG.BUTTON(T('Volver'),_class='button'),_href=URL(back_controller,'index',vars=dict(keywords=perfil+'.id="'+str(_id)+'"')))
    return dict(form=form, option_tree=json(tree), default=pordefecto, back_button=back_button)

@auth.requires_login()
@service.json
def relorgs_delete(id):
    json='NO'
    if(auth.has_membership('administrator')):
        if(db(db.RelPersOrg.id==id).delete()):
            json='OK'
    return json
    
@auth.requires_login()
def persona_create():

   form = SQLFORM(db.persona)
   if form.validate():

        idP = db.persona.insert(**db.persona._filter_fields(form.vars))
        if(idP>0):
            response.flash = T('Formulario aceptado')
   elif form.errors:
       response.flash = T('Hay errores en el formulario')
   else:
       response.flash = T('Por favor llene el formulario')
   return dict(form=form)

@auth.requires_login()
def birthEvent():
    birthEvent = db(db.birthEvent.is_active==True).select(orderby=db.birthEvent.fecha)
    return locals()

@auth.requires_login()
def birthEvent_create():
    form = crud.create(db.birthEvent,next='birthEvent')
    return dict(form=form)

@auth.requires_login()
def document():
    document_query = db.document.is_active==True
    #.select('document.name','document.documentURL','document.fecha',orderby=db.document.fecha)
    grid=SQLFORM.grid(document_query,fields=[db.document.name,db.document.documentURL,db.document.fecha])
    return dict(grid=grid)

@auth.requires_login()
def document_create():

    form=SQLFORM(db.document)
    db.document.source_from.default=me
    if form.accepts(request.vars, session):
       response.flash = T('Formulario aceptado')
    elif form.errors:
       response.flash = T('Hay errores en el formulario')
    else:
       response.flash = T('Por favor llene el formulario')
        
    
    return dict(form=form)

@auth.requires_login()
def place():
    place = db(db.place).select(orderby=db.place.fecha)
    return locals()

@auth.requires_login()
def place_create():
    form = crud.create(db.place,next='place')
    return dict(form=form)
    


    


@auth.requires_login()
def relPersona():
    persona = db.persona(request.args(0)) or redirect(URL('persona'))
    relPersona = db((db.relPersona.is_active==True)&(db.relPersona.origenP==persona.id)).select(
               orderby=~db.relPersona.relacion, limitby=(0, 25))
    return locals()

@auth.requires_login()
def relPersona_create():
    from gluon.serializers import json
    from fechas import fechas

    #Initialize the widget
    add_option = SELECT_OR_ADD_OPTION(form_title=T("Agregar Fuentes"), controller="fuentes", function="add_fuentes", button_text = T("Nueva Fuente"))
    #assign widget to field
    db.relPersona.documentSource.widget = add_option.widget

    #quita validación en destinoP para el caso en que el autocomplete no coincida con una persona creando el registro
    db.relPersona.destinoP.requires=None

    ##persona = db.persona(request.args(0)) or redirect(URL('perfil'))
    filter_arg=request.args(1) or 11
    response.view='default/relPersona_create.html' 
    db.relPersona.origenP.default = request.args(0)
    db.relPersona.extraO.default = request.args(2)

    _id=request.args(0); perfil='persona'; back_controller='personas'
    if(request.args(2)):
        _id=request.args(2); perfil='Organizacion'
        org = db.Organizacion(_id)
        if org.tipoOrg==2:
            back_controller = 'companies'
        else:
            back_controller = 'organizations'



    form=SQLFORM(db.relPersona)
    
    if form.validate():
        form.vars.is_active='T'
        form.vars.fdesde=fechas(form.vars.iniDay,form.vars.iniMonth,form.vars.iniYear)
        form.vars.fhasta=fechas(form.vars.finDay,form.vars.finMonth,form.vars.finYear)

        if((form.vars.extraO=="")&(form.vars._autocomplete_Organizacion_alias_aux!="")):
            form.vars.name=form.vars._autocomplete_Organizacion_alias_aux
            form.vars.alias=form.vars._autocomplete_Organizacion_alias_aux
            form.vars.countryOfResidence=44
            idO=db.Organizacion.insert(**db.Organizacion._filter_fields(form.vars))
            if(idO!=None):
                form.vars.extraO=idO

        if(form.vars.destinoP==""):

            if(form.vars._autocomplete_destinoP_alias_aux!=""):
                form.vars.alias=form.vars._autocomplete_destinoP_alias_aux
                form.vars.countryOfResidence=44
                idP = db.persona.insert(**db.persona._filter_fields(form.vars))
                if(idP!=None):
                    form.vars.destinoP=idP
                    id = db.relPersona.insert(**db.relPersona._filter_fields(form.vars))
                    response.flash=T('form OK ')
            else:
                response.flash=T('Debe Ingresar una Persona ')

        else:
            id = db.relPersona.insert(**db.relPersona._filter_fields(form.vars))
            ##redirect(URL('default','persona'))
            ##redirect(URL('relorgs_edit',args=record.id))
            ##response.flash = T('form accepted '+str(id)+"m "+form.vars.destinoP)
        ##if(form.vars.extraO!=""):
            ##if not exist relation insert data for 2 person
        ##    relPersonaO=db((db.RelPersOrg.origenP==form.vars.origenP)&(db.RelPersOrg.destinoO==form.vars.extraO)).select().first()
        ##    if(relPersonaO==None):
        ##        idrelO=db.RelPersOrg.insert(specificRelation=156,
        ##            origenP=form.vars.origenP, destinoO=form.vars.extraO, transitiveP2P=id)
        ##    relPersonaD=db((db.RelPersOrg.origenP==form.vars.destinoP)&(db.RelPersOrg.destinoO==form.vars.extraO)).select().first()
        ##    if(relPersonaD==None):
        ##        idrelO=db.RelPersOrg.insert(specificRelation=156,
        ##            origenP=form.vars.destinoP, destinoO=form.vars.extraO, transitiveP2P=id)

    elif form.errors:
        text=''
        for item in form.errors:
            text=text+' '+item
        response.flash = T('Hay errores en el formulario'+text)
    tree={}
    options=db(db.tipoRelacionP2P.parent==0).select(orderby=db.tipoRelacionP2P.name)
    for option in options:
        tree[str(option.id)]=T(option.name)
        
    default=db(db.tipoRelacionP2P.id==filter_arg).select().first()
    pordefecto='"'+str(default.id)+'"'
    if(default.parent!=0):
        ##parent=db(db.tipoRelacionP20.id==default.parent).select().first()
        pordefecto='"'+str(default.parent)+'", "'+str(default.id)+'"'


    back_button = A(TAG.BUTTON(T('Volver'),_class='button'),_href=URL(back_controller,'index',vars=dict(keywords=perfil+'.id="'+str(_id)+'"')))
    
    return dict(form=form, option_tree=json(tree), default=pordefecto, _id=_id, back_button=back_button)

@auth.requires_login()    
def relPersona_edit():
    from gluon.serializers import json
    from fechas import fechas
    relPersona = db.relPersona(request.args(0)) or redirect(URL('perfil'))

    #Initialize the widget
    add_option = SELECT_OR_ADD_OPTION(form_title=T("Agregar Fuentes"), controller="fuentes", function="add_fuentes", button_text = T("Nueva Fuente"))
    #assign widget to field
    db.relPersona.documentSource.widget = add_option.widget

    ##filter_arg=request.args(1) or redirect(URL('perfil'))
    response.view='default/relPersona_create.html'
    _id=relPersona.origenP; perfil='persona'; back_controller='personas'
    if(request.args(1)=='org'):
        _id=relPersona.extraO; perfil='Organizacion'
        org = db.Organizacion(_id)
        back_controller = 'organizations'
        if org.tipoOrg==2:
            back_controller = 'companies'





    form=SQLFORM(db.relPersona,relPersona)
    
    if form.validate():
        form.vars.fdesde=fechas(form.vars.iniDay,form.vars.iniMonth,form.vars.iniYear)
        form.vars.fhasta=fechas(form.vars.finDay,form.vars.finMonth,form.vars.finYear)
        form.vars.is_active='T'
        if((form.vars.extraO=="")&(form.vars._autocomplete_Organizacion_alias_aux!="")):
            form.vars.name=form.vars._autocomplete_Organizacion_alias_aux
            form.vars.alias=form.vars._autocomplete_Organizacion_alias_aux
            form.vars.countryOfResidence=44
            idO=db.Organizacion.insert(**db.Organizacion._filter_fields(form.vars))
            if(idO!=None):
                form.vars.extraO=idO

        if(form.vars.destinoP==""):
            if(form.vars._autocomplete_destinoP_alias_aux!=""):
                
                
                form.vars.alias=form.vars._autocomplete_destinoP_alias_aux
                form.vars.countryofResidence=44
                idP = db.persona.insert(**db.persona._filter_fields(form.vars))
                if(idP!=None):
                    response.flash=''
                    form.vars.destinoP=idP
                    form.vars.id=relPersona.id
                    if auth.archive(form):
                        response.flash=T('Archivo aceptado')
                    id = relPersona.update_record(**db.relPersona._filter_fields(form.vars))
                    response.flash+=T('Formulario aceptado')
                    
            else:
                response.flash=T('Debe Ingresar un grupo ')  
        else:
            response.flash=''
            form.vars.id=relPersona.id
            if auth.archive(form):
                response.flash=T('Archivo aceptado')
            id = relPersona.update_record(**db.relPersona._filter_fields(form.vars))
            response.flash+=T('Formulario aceptado')
        ##redirect(URL('perfil'))
    elif form.errors:
        response.flash = T('Hay errores en el formulario')
        
    tree={}
    options=db(db.tipoRelacionP2P.parent==0).select(orderby=db.tipoRelacionP2P.name)
    for option in options:
        tree[str(option.id)]=T(option.name)
        
    default=db(db.tipoRelacionP2P.id==relPersona.relacion).select().first()
    pordefecto='"'+str(default.id)+'"'
    if(default.parent!=0):
        ##parent=db(db.tipoRelacionP20.id==default.parent).select().first()
        pordefecto='"'+str(default.parent)+'", "'+str(default.id)+'"'

    back_button = A(TAG.BUTTON(T('Volver'),_class='button'),_href=URL(back_controller,'index',vars=dict(keywords=perfil+'.id="'+str(_id)+'"')))
    
    return dict(form=form, option_tree=json(tree), default=pordefecto, back_button=back_button)
    

@auth.requires_login()
def new():
    form = SQLFORM.factory(db.persona,db.relFamiliar)

    if form.accepts(request.vars):
        _id_persona = db.contacts.insert(**db.persona._filter_fields(form.vars))
        form.vars.contact = _id_persona
        id = db.relFamiliar.insert(**db.relFamiliar._filter_fields(form.vars))
        response.flash = T('Usuario registrado exitósamente')
    return locals()

@auth.requires_login()    
def country():
    countries = db(db.country).select(orderby=db.country.id)
    return locals()

@auth.requires_login()
@service.json
def Organizacion_eliminar(id):
    data=None
    if(auth.has_membership('administrator')):
        if(table in ('Organizacion','relPersona','RelPersOrg','relOrg2Org')):
            record=db[table](id)
            try:
                record.update_record(is_active=False)
            except NotImplementedError:
                raise NotImplementedError(T('Aún no pueden serializarse lists y dicts'))
            if(table=='Organizacion'):
                data=str(id)
            elif table=='relPersona':
                data='relPersona'+str(id)
            elif table=='RelPersOrg':
                data='RelPersOrg'+str(id)
            elif table=='relOrg2Org':
                data='relOrg2Org'+str(id)
    return data

@auth.requires_login()
def Organizacion():

    class Virtual(object):
        @virtualsettings(label=T('Editar'))
        def editar(self):          
            picture=A('editar', _href=URL('Organizacion_edit', args=self.Organizacion.id))
            return picture
        @virtualsettings(label=T('Document Cloud'))
        def documento(self):
            detalle=A('agregar Documento', _href=URL('document','document_cloud', args=self.Organizacion.id))
            return detalle
        @virtualsettings(label=T('Eliminar'))
        def delete(self):
            if(auth.has_membership('administrator')):
                return TAG.BUTTON(T('Eliminar'),_class='deletebutton',_onclick='deleteRow(event,"Organizacion",%s);' % self.Organizacion.id)
            else:
                return ""
    if(request.args(0)>0):
        datasource=db(db.Organizacion.id==request.args(0)).select()
    else:
        datasource=db(db.Organizacion.is_active==True).select(cache=(cache.ram,10))

    table = plugins.powerTable
    table.datasource = datasource
    table.headers = 'labels'
    table.dtfeatures['sScrollY'] = '100%'
    table.virtualfields = Virtual()
    table.keycolumn = 'Organizacion.id'
    table.columns = ['Organizacion.id','Organizacion.alias','virtual.editar','virtual.delete']
    table.showkeycolumn = False
    table.extra = dict(autoresize={},
        tooltip={},
        details={'detailscallback':URL('organizacion','Organizationdetails')
        })
    table = table.create()
    return dict(table=table)

@auth.requires_login()
def Organizacion_create():

    form = SQLFORM(db.Organizacion)
    db.Organizacion.alias.required=True
    if form.validate():
        form.vars.name=form.vars.alias
        idO = db.Organizacion.insert(**db.persona._filter_fields(form.vars))
        if(idO>0):
            response.flash = T('Formulario aceptado')
    elif form.errors:
        response.flash = T('Hay errores en el formulario')
    else:
        response.flash = T('Por favor llene el formulario')
    return dict(form=form)

@auth.requires_login()    
def Organizacion_edit():

    #Initialize the widget
    add_option = SELECT_OR_ADD_OPTION(form_title=T("Agregar Fuentes"), controller="fuentes", function="add_fuentes", button_text = T("Nueva Fuente"))
    #assign widget to field
    db.Organizacion.documentSource.widget = add_option.widget

    #Initialize the widget
    add_option_document = SELECT_OR_ADD_OPTION(form_title=T("Agregar Documento"), controller="document",
                                               function="add_document", button_text = T("Nuevo Documento"),
                                               dialog_width=600)
    #assign widget to field
    db.Organizacion.documentCloud.widget = add_option_document.widget

    record = db.Organizacion(request.args(0)) or redirect(URL('Organizacion'))


    form = SQLFORM(db.Organizacion, record)

    if form.validate():


        id = record.update_record(**db.Organizacion._filter_fields(form.vars))
        form.vars.id=record.id
        auth.archive(form)
        response.flash = T('Formulario aceptado')
    elif form.errors:
        response.flash = T('Hay errores en el formulario')
        
    return dict(form=form)
    
@auth.requires_login()    
def relFamiliar():
    persona = db.persona(request.args(0)) or redirect(URL('persona'))
    relFamiliar = db(((db.relFamiliar.origenP==persona.id) | (db.relFamiliar.destinoP==persona.id)) (db.relFamiliar.is_active==True)).select(
               orderby=db.relFamiliar.parentesco, limitby=(0, 25))
    return locals()

@auth.requires_login()
def relFamiliar_create():
    #Initialize the widget
    add_option = SELECT_OR_ADD_OPTION(form_title=T("Agregar Fuentes"), controller="fuentes", function="add_fuentes", button_text = T("Nueva Fuente"))
    #assign widget to field
    db.relFamiliar.documentSource.widget = add_option.widget

    #se quita la validacion en el campo autocomplete para permitir el ingreso inmediato cuando no existe la persona
    db.relFamiliar.destinoP.requires=None

    persona = db.persona(request.args(0)) or redirect(URL('persona','index'))
    db.relFamiliar.origenP.default = request.args(0)


    form=SQLFORM(db.relFamiliar)
    if form.validate():

        form.vars.is_active='T'
        if(form.vars.destinoP==''):

            if(form.vars._autocomplete_destinoP_alias_aux!=''):

                form.vars.alias=form.vars._autocomplete_destinoP_alias_aux
                form.vars.countryofResidence=44
                idP = db.persona.insert(**db.persona._filter_fields(form.vars))
                if(idP!=None):
                    form.vars.destinoP=idP

                    ##si es padre chequea hermanos
                    if(form.vars.parentesco=='1'):
                       response.flash=T('Padre ')
                       ## idP hereda Hermanos - hijos de un mismo Padre origenP
                       r=padres(form.vars.origenP,idP,True)
                    if(form.vars.parentesco=='3'):
                        ## idP hereda hermanos de origenP
                        r=heredaHermanos(idP, form.vars.origenP)
                    ##response.flash=T('Padre '+form.vars.parentesco)
                    id = db.relFamiliar.insert(**db.relFamiliar._filter_fields(form.vars))
            else:
                response.flash=T('Debe Ingresar una Persona ')  
        else:

            if(form.vars.parentesco=='1'):
                ## destinoP hereda Hermanos - hijos de un mismo Padre origenP
                padres(form.vars.origenP,form.vars.destinoP,False)
            id = db.relFamiliar.insert(**db.relFamiliar._filter_fields(form.vars))
            if(form.vars.parentesco=='3'):
                ##origenp y destinop heredan sus hermanos:
                r=OldBrothers(form.vars.origenP,form.vars.destinoP)

        ##redirect(URL('relorgs_edit',args=record.id))
        ##response.flash = T('form accepted'+form.vars.destinoO)
        if form.process().accepted:
            response.flash = T('formulario aceptado')
            redirect(URL('persona','index'))
    elif form.errors:
        response.flash = T('Hay errores en el formulario')
    ##form = crud.create(db.relFamiliar,next='relFamiliar/[id]')
    return dict(form=form, persona=persona.id)




@auth.requires_login()
def relFamiliar_edit():
    record=db.relFamiliar(request.args(0)) or redirect(URL('perfil'))

    #Initialize the widget
    add_option = SELECT_OR_ADD_OPTION(form_title=T("Agregar Fuentes"), controller="fuentes", function="add_fuentes", button_text = T("Nueva Fuente"))
    #assign widget to field
    db.relFamiliar.documentSource.widget = add_option.widget

    form = SQLFORM(db.relFamiliar, record)  
    if form.validate():
        form.vars.is_active='T'
        if(form.vars.destinoP==""):
            ##response.flash=T('Maluenda ') 
            if(form.vars._autocomplete_destinoP_alias_aux!=""):
                
                form.vars.alias=form.vars._autocomplete_destinoP_alias_aux
                form.vars.countryofResidence=44
                idP = db.persona.insert(**db.persona._filter_fields(form.vars))
                if(idP!=None):
                    form.vars.destinoP=idP
                    form.vars.id=record.id
                    auth.archive(form)
                    ##si es padre chequea hermanos
                    if(form.vars.parentesco=='1'):
                        response.flash=T('Padre ')
                        ## idP hereda Hermanos - hijos de un mismo Padre origenP
                        r=padres(form.vars.origenP,idP,True)
                    if(form.vars.parentesco=='3'):
                        ## idP hereda hermanos de origenP
                        r=heredaHermanos(idP, form.vars.origenP)
                        ##response.flash=T('Padre '+form.vars.parentesco)
                    id = record.update_record(**db.relFamiliar._filter_fields(form.vars))
                    response.flash=T('Formulario aceptado')
                    
            else:
                response.flash=T('Debe Ingresar una Persona ')  
        else:
            form.vars.id=record.id

            if(form.vars.parentesco=='1'):
                ## destinoP hereda Hermanos - hijos de un mismo Padre origenP
                padres(form.vars.origenP,form.vars.destinoP,False)

            id = record.update_record(**db.relFamiliar._filter_fields(form.vars))
            auth.archive(form)
            if(form.vars.parentesco=='3'):
                ##origenp y destinop heredan sus hermanos:
                r=OldBrothers(form.vars.origenP,form.vars.destinoP)

    elif form.errors:
        response.flash = T('form has errors')

        
    return dict(form=form, persona=record.origenP)

@auth.requires_login()    
def wizard():
    STEPS = {0: ('firstName', 'firstLastName','otherLastName','alias','shortBio','countryofResidence','depiction'), # fields for 1st page
             1: ('longBio', 'hasdocumentation'), # fields for 2nd page
             ##2: ('field5', 'field6'), # fields for 2nd page
             2: URL('persona_done')} # url when wizard completed
    step = int(request.args(0) or 0)
    if not step in STEPS: redirect(URL(args=0))
    fields = STEPS[step]
    print "Fields: " + str(fields) + " Step " + str(step)
    if step==0: 
        session.wizard = {}
    if isinstance(fields,tuple):
        form = SQLFORM.factory(*[f for f in db.persona if f.name in fields])
        if form.accepts(request,session):
            session.wizard.update(form.vars)
            redirect(URL(args=step+1))            
    else:
        db.persona.insert(**session.wizard)
        session.flash = T('Asistente Completado')
        redirect(fields)
    return dict(form=form,step=step)

@auth.requires_login()
def persona_done():
    return dict(message=T('Fin de Asistente'), back=A(T('New wizard'), _href=URL("wizard")))
    
def consumer():
    return dict()
    
@service.json
def get_visual():
    lista = []
    for row in db((db.persona.firstLastName!="")&(db.persona.is_active==True)).select():
        listaparents=[]
        for parents in db(db.relFamiliar.origenP==row.id).select():
            destino = db.persona[parents.destinoP]
            relation = db.tipoParentesco[parents.parentesco]
            node={'id':parents.destinoP,'name':destino.alias, 'data':{'name':'isParent','relation':relation.name}}
            listaparents.append(node)
        children={'children':listaparents, 'data':{'name':'hasParents','relation':'Familiar'}, 'name':row.alias, 'id':row.id}
        lista.append(children)
    visual =  { 'name':"Senado",'children':lista, 'data':{'name':'work at','relation':'member political institution'},'id':10000}
    return visual
    
@service.json
def get_persona_relfamiliar(alias):
    lista = []; visual={}
    rows = db((db.persona.alias.like('%'+alias+'%'))&(db.persona.is_active==True)).select()
    if(rows!=None):
        for row in rows:
            listaparents=[]
            for parents in db(db.relFamiliar.origenP==row.id).select():
                destino = db.persona[parents.destinoP]
                relation = db.tipoParentesco[parents.parentesco]
                node={'id':parents.destinoP,'name':destino.alias, 'data':{'name':'isParent','relation':relation.name}}
                listaparents.append(node)
            children={'children':listaparents, 'data':{'name':'hasParents','relation':'Familiar'}, 'name':row.alias, 'id':row.id}
            lista.append(children)
            visual =  { 'name':row.alias,'children':lista, 'data':{'name':'work at','relation':'member political institution'},'id':row.id}
    return visual

@service.json
def get_relacionP2P(alias):
    lista = []; visual={}
    rows = db((db.persona.alias.like('%'+alias+'%'))&(db.persona.is_active==True)).select()
    if(rows!=None):
        for row in rows:
            listaparents=[]
            for parents in db(db.relPersona.origenP==row.id).select(orderby='relacion'):
                destino = db.persona[parents.destinoP]
                relation = db.tipoRelacionP2P[parents.relacion]
                node={'id':parents.destinoP,'name':destino.alias, 'data':{'name':'isRelation','relation':relation.name}}
                listaparents.append(node)
            children={'children':listaparents, 'data':{'name':'hasRelation','relation':'Relacion P2P'}, 'name':row.alias, 'id':row.id}
            lista.append(children)
            visual =  { 'name':row.alias,'children':lista, 'data':{'name':'work at','relation':'member political institution'},'id':row.id}
    return visual
    
@service.json
def get_persona_relEconomica(alias):
    lista = []
    for row in db((db.persona.alias.like('%'+alias+'%'))&(db.persona.is_active==True)).select():
        listaparents=[]
        for parents in db(db.RelPersOrg.origenP==row.id).select():
            destino = db.Organizacion[parents.destinoO]
            relation = db.tipoRelacionP20[parents.specificRelation]
            node={'id':parents.destinoO,'name':destino.alias, 'data':{'name':'EconomicRelation','relation':relation.relationship}}
            listaparents.append(node)
        children={'children':listaparents, 'data':{'name':'hasParents','relation':'Familiar'}, 'name':row.alias, 'id':row.id}
        lista.append(children)
    visual =  { 'name':row.alias,'children':lista, 'data':{'name':'work at','relation':'member political institution'},'id':row.id}
    return visual
    
@service.json
def get_relacion(id):
    tree={}
    options=db(db.tipoRelacionP2P.parent==id).select(orderby=db.tipoRelacionP2P.name)
    for option in options:
        tree[str(option.id)]=T(option.name)
    return tree

@service.json
def get_specificRelation(id):
    tree={}
    options=db(db.tipoRelacionP20.parent==id).select(orderby=db.tipoRelacionP20.relationship)
    for option in options:
        tree[str(option.id)]=T(option.relationship)
    return tree

@service.json
def get_familyRelations(id):
    record=db.persona(id)
    relation={}
    rows = db((db.relFamiliar.is_active==True)&(db.relFamiliar.origenP==id) & (db.relFamiliar.parentesco==db.tipoParentesco.id) & (db.relFamiliar.destinoP==db.persona.id)).select()
    for row in rows:
        relation[row.id]={'parentesco':row.name,'destino':row.alias}
    return relation

@auth.requires_login()
def familydetails():
    _id=""; parientes=[]; parientesD=[]; conexiones=[]; conyuges=[]; borrar=None
    selectP2P=seleccionP20=P2O={}; conexionO=conexionD=companeros=companerosD=[]
    conyugesO=conyugesD=Org=[]
    grid = ""
    if(request.ajax):
        datas=request.vars
        data=datas.keys()
        _id=data[0] 
        data,_id=_id.split('_')
        if _id==None: _id=request.args(0)
        if _id==None: response.view='404.html'
        if(_id!=None):
            ##parents relPersona
            parentsP2P=db((db.tipoRelacionP2P.parent==0) & (db.tipoRelacionP2P.id!=1)).select(cache=(cache.ram,10))
            ##parents relPersona Organizacion
            parentsP20=db(db.tipoRelacionP20.parent==0).select(cache=(cache.ram,10))


            ##Origen
            parientes=db((db.relFamiliar.origenP==_id) & (db.relFamiliar.parentesco==db.tipoParentesco.id) & (db.relFamiliar.is_active==True) &
                         (db.relFamiliar.destinoP==db.persona.id) & (db.persona.is_active==True)).select(db.relFamiliar.id,db.tipoParentesco.name,db.persona.alias,db.relFamiliar.destinoP,cache=(cache.ram,10))
            ##Destino
            parientesD=db((db.relFamiliar.destinoP==_id) & (db.relFamiliar.parentesco==db.tipoParentesco.id) & (db.relFamiliar.is_active==True) &
                          (db.relFamiliar.origenP==db.persona.id) & (db.persona.is_active==True)).select(db.relFamiliar.id,db.tipoParentesco.nameInverso,db.persona.alias,db.relFamiliar.origenP,cache=(cache.ram,10))

            conexionO={}; conexionD={}; selectP2P={}

            conyugesO=db((db.relPersona.origenP==_id) &
                         (db.relPersona.relacion==db.tipoRelacionP2P.id)& (db.relPersona.is_active==True) &
                         (db.tipoRelacionP2P.parent==1) &
                         (db.relPersona.destinoP==db.persona.id) & (db.persona.is_active==True)).select(cache=(cache.ram,10))
            conyugesD=db((db.relPersona.destinoP==_id) &
                         (db.relPersona.relacion==db.tipoRelacionP2P.id)& (db.relPersona.is_active==True) &
                         (db.tipoRelacionP2P.parent==1) &
                         (db.relPersona.origenP==db.persona.id) & (db.persona.is_active==True)).select(cache=(cache.ram,10))
            Org={}
            orgs=db( ((db.relPersona.origenP==_id) | (db.relPersona.destinoP==_id)) & (db.relPersona.extraO==db.Organizacion.id)
                     &(db.relPersona.is_active==True) ).select(groupby=db.relPersona.extraO)
            for org in orgs:
                Org[org.relPersona.extraO]=org.Organizacion.alias
            ##rel Persona a Persona
            for parents in parentsP2P:
                conexionO[parents.name]=db((db.relPersona.origenP==_id) &
                                             (db.relPersona.relacion==db.tipoRelacionP2P.id) &(db.relPersona.is_active==True) &
                                             ((db.tipoRelacionP2P.parent==parents.id) | (db.tipoRelacionP2P.id==parents.id)) &
                                             (db.relPersona.destinoP==db.persona.id) & (db.persona.is_active==True)).select(cache=(cache.ram,10))
                conexionD[parents.name]=db((db.relPersona.destinoP==_id) &
                                              (db.relPersona.relacion==db.tipoRelacionP2P.id) &(db.relPersona.is_active==True) &
                                              ((db.tipoRelacionP2P.parent==parents.id) | (db.tipoRelacionP2P.id==parents.id)) &
                                              (db.relPersona.origenP==db.persona.id) & (db.persona.is_active==True)).select(cache=(cache.ram,10))

                selectP2P[parents.id]=parents.name


            P2O={}; seleccionP20={}
            ## rel Persona a Organización
            for parents in parentsP20:
                P2O[parents.relationship]=db((db.RelPersOrg.is_active==True)&(db.RelPersOrg.origenP==_id) & (db.RelPersOrg.destinoO==db.Organizacion.id) &
                                     (db.RelPersOrg.specificRelation==db.tipoRelacionP20.id) & (db.Organizacion.is_active==True) &
                                     (db.tipoRelacionP20.parent==parents.id)).select(cache=(cache.ram,10))
                seleccionP20[parents.id]=parents.relationship



            ##persona a persona en Orgaizacion o Grupo
            companeros=db((db.RelPersOrg.is_active==True)&(db.RelPersOrg.origenP==_id) &(db.RelPersOrg.id==db.companeros.relacionP2O) &
                            (db.companeros.destinoP==db.persona.id) & (db.persona.is_active==True) &
                            (db.Organizacion.id==db.RelPersOrg.destinoO) &
                            (db.Organizacion.is_active==True)).select(cache=(cache.ram,10))
            companerosD=db((db.RelPersOrg.is_active==True)&(db.companeros.destinoP==_id) &(db.RelPersOrg.id==db.companeros.relacionP2O) &
                            (db.RelPersOrg.origenP==db.persona.id)& (db.persona.is_active==True) &
                            (db.Organizacion.id==db.RelPersOrg.destinoO) &
                            (db.Organizacion.is_active==True)).select(cache=(cache.ram,10))

            borrar=auth.has_membership('administrator')

            ##tbl = SQLTABLE(conyugesO,headers='labels',truncate=32,linkto='default')
            
    return dict(parientes=parientes, parientesD=parientesD, _id=_id,  borrar=borrar, grid=grid, selectP2P=selectP2P,
        conexionO=conexionO, conexionD=conexionD,
        seleccionP20=seleccionP20, P2O=P2O, companeros=companeros, companerosD=companerosD,
        conyugesO=conyugesO, conyugesD=conyugesD,
        Org=Org
    )

@auth.requires_login()
def conyuge_create():
    from gluon.serializers import json
    persona = db.persona(request.args(0)) or redirect(URL('perfil')) 
    filter_args = request.args(1) or redirect(URL('perfil')) 
    response.view='default/relPersona_create.html' 
    db.relPersona.origenP.default = request.args(0)
    
    
    

    form=SQLFORM(db.relPersona)

    

    if form.validate():
        form.vars.is_active='T'
        if(form.vars.destinoP==""):
            if(form.vars._autocomplete_destinoP_alias_aux!=""):
                
                form.vars.alias=form.vars._autocomplete_destinoP_alias_aux
                form.vars.countryOfResidence=44
                idP = db.persona.insert(**db.persona._filter_fields(form.vars))
                if(idP!=None):
                    form.vars.destinoP=idP
                    id = db.relPersona.insert(**db.relPersona._filter_fields(form.vars))
                    response.flash=T('Formulario aceptado')
                    redirect(URL('default','persona'))
            else:
                response.flash=T('Debe Ingresar una Persona ')  
        else:
            id = db.relPersona.insert(**db.relPersona._filter_fields(form.vars))
            redirect(URL('default','persona'))

    elif form.errors:
        response.flash = T('Hay errores en el formulario')
    tree={}
    options=db(db.tipoRelacionP2P.parent==0).select(orderby=db.tipoRelacionP2P.name)
    for option in options:
        tree[str(option.id)]=option.name
        
    default=db(db.tipoRelacionP2P.id==filter_args).select().first()
    pordefecto='"'+str(default.id)+'"'
    if(default.parent!=0):
        ##parent=db(db.tipoRelacionP20.id==default.parent).select().first()
        pordefecto='"'+str(default.parent)+'", "'+str(default.id)+'"'
    return dict(form=form, option_tree=json(tree), default=pordefecto, persona=persona.id)

##companeros de estudios
@auth.requires_login()
def companeros_create():
    from gluon.serializers import json
    #Initialize the widget
    add_option = SELECT_OR_ADD_OPTION(form_title=T("Agregar Fuentes"), controller="fuentes", function="add_fuentes", button_text = T("Nueva Fuente"))
    #assign widget to field
    db.companeros.fuente.widget = add_option.widget

    record = db.persona(request.args(0)) or redirect(URL('perfil'))
    relPersona2Org = db.RelPersOrg(request.args(0)) or redirect(URL('perfil'))
    tiporelacion = request.args(1) or redirect(URL('perfil'))

    ##filter_args = request.args(1) or redirect(URL('perfil'))
    organizacion=db(db.Organizacion.id==relPersona2Org.destinoO).select().first()
    persona=db(db.persona.id==relPersona2Org.origenP).select().first()

    db.companeros.relacionP2O.default = request.args(0)
    db.companeros.relationComp.default = tiporelacion
    tipoRel=db.tipoRelacionP20(relPersona2Org.specificRelation)
    db.companeros.nexo.default=tipoRel.relationship


    parent = T("Relación:")+ " "+persona.alias+" "+T("es/fue (")+ \
             tipoRel.relationship+") en/con "+organizacion.name



    form=SQLFORM(db.companeros, formstyle = 'divs')




    if form.validate():
        form.vars.is_active='T'
        form.vars.relacionP2O=relPersona2Org.id
        form.vars.relationComp=tiporelacion
        if(form.vars.destinoP==""):
            if(form.vars._autocomplete_destinoP_alias_aux!=""):

                form.vars.alias=form.vars._autocomplete_destinoP_alias_aux
                form.vars.countryOfResidence=44
                idP = db.persona.insert(**db.persona._filter_fields(form.vars))
                if(idP!=None):
                    form.vars.destinoP=idP
                    id = db.companeros.insert(**db.companeros._filter_fields(form.vars))

                    idrel=db.RelPersOrg.insert(specificRelation=156,
                        origenP=idP, destinoO=relPersona2Org.destinoO, transitive=relPersona2Org.id)

                    ##update transitive
                    relPersona2Org.update_record(transitive=idrel)

                    response.flash=T('Formulario aceptado')
                    redirect(URL('default','perfil'))
            else:
                response.flash=T('Debe Ingresar una Persona ')
        else:
            id = db.companeros.insert(**db.companeros._filter_fields(form.vars))
            idrel=db.RelPersOrg.insert(specificRelation=156,
            origenP=form.vars.destinoP, destinoO=relPersona2Org.destinoO,
            transitive=relPersona2Org.id)

            ##update transitive
            relPersona2Org.update_record(transitive=idrel)

            redirect(URL('default','perfil'))

    elif form.errors:
        response.flash = T('Hay errores en el formulario')
    tree={}

    return dict(form=form, parent=parent)

@auth.requires_login()
def companeros_edit():

    record= db.companeros(request.args(0)) or redirect(URL('perfil'))
    persona=db.persona(record.destinoP)

    relacion=db.RelPersOrg(record.relacionP2O)
    personaO=db.persona(relacion.origenP)
    tipoRel=db.tipoRelacionP20(relacion.specificRelation)
    organizacion=db.Organizacion(relacion.destinoO)


    parent = T("Relación:")+" "+personaO.alias+" "+ T("es/fue") +" "+ tipoRel.relationship+" " + T("de")+ " "+persona.alias+" "+\
              "en/con "+organizacion.name

    formFuente=SQLFORM(db.document)
    if formFuente.accepts(request.vars, session):
        response.flash = T('Documento aceptado')
    elif formFuente.errors:
        response.flash = T('Hay errores en el documento')

    form=SQLFORM(db.companeros, record, formstyle = 'divs')


    if form.validate():
        form.vars.is_active='T'
        if(form.vars.destinoP==""):
            if(form.vars._autocomplete_destinoP_alias_aux!=""):

                form.vars.alias=form.vars._autocomplete_destinoP_alias_aux
                form.vars.countryOfResidence=44
                idP = db.persona.insert(**db.persona._filter_fields(form.vars))
                if(idP!=None):

                    form.vars.destinoP=idP
                    form.vars.id=record.id
                    auth.archive(form)
                    id = record.update_record(**db.companeros._filter_fields(form.vars))

                    ##relacion transitiva
                    relacion.update_record(origenP=idP)

                    response.flash=T('Formulario aceptado')

                    redirect(URL('default','perfil'))
            else:
                response.flash=T('Debe Ingresar una Persona ')
        else:
            form.vars.id=record.id
            auth.archive(form)
            id = record.update_record(**db.companeros._filter_fields(form.vars))

            redirect(URL('default','perfil'))

    elif form.errors:
        response.flash = T('Hay errores en el formulario')

    return dict(form=form, parent=parent, formFuente=formFuente)


