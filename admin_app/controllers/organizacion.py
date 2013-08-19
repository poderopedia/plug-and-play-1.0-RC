# coding: utf8
__author__ = 'Evolutiva'

def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()

@auth.requires_login()
def index():
    class Virtual(object):
        @virtualsettings(label=T('Relaciones'))
        def edit(self):
            picture=A('editar', _href=URL('default','organization_edit', args=self.Organizacion.id))
            return picture
        @virtualsettings(label=T('Conexion'))
        def connections(self):
            ref=A('ver', _href=URL('organizacion','connections', args=self.Organizacion.id))
            return ref
    if(request.args(0)>0):
        datasource=db(db.Organizacion.id==request.args(0)).select()
    else:
        datasource=db(db.Organizacion.is_active==True).select()
    table = plugins.powerTable
    table.datasource = datasource
    table.headers = 'labels'
    table.dtfeatures['sScrollY'] = '100%'
    table.uitheme = 'redmond'
    table.virtualfields = Virtual()
    table.keycolumn = 'Organizacion.id'
    table.columns = ['Organizacion.alias','virtual.edit','virtual.connections']
    table.showkeycolumn = False
    table.extra = dict(autoresize={},
        tooltip={},
        details={'detailscallback':URL('organizacion','Organizationdetails')
        })

    table = table.create()
    return dict(table=table)

@auth.requires_login()
def Organizationdetails():
    datas=request.vars
    data=datas.keys()
    _id=data[0]
    data,_id=_id.split('_')
    if(_id!=None):
        ##relPers2Org
        aPersonas=db((db.RelPersOrg.destinoO==_id) & (db.RelPersOrg.origenP==db.persona.id) & (db.RelPersOrg.is_active==True) &
                 (db.RelPersOrg.specificRelation==db.tipoRelacionP20.id)).select()

        aOrganizaciones=db((db.relOrg2Org.origenO==_id) & (db.Organizacion.id==db.relOrg2Org.destinoO) & (db.relOrg2Org.is_active==True)&
                (db.relOrg2Org.relationOrg==db.tipoRelacionOrg2Org.id)).select()
        aOrganizacionesD=db((db.relOrg2Org.destinoO==_id) & (db.Organizacion.id==db.relOrg2Org.origenO) & (db.relOrg2Org.is_active==True)&
                         (db.relOrg2Org.relationOrg==db.tipoRelacionOrg2Org.id)).select()
        origenP=db.persona.with_alias('origenP')
        destinoP=db.persona.with_alias('destinoP')
        relacion=db.tipoRelacionP2P.with_alias('relacion')
        aRelPersonas=db((db.relPersona.is_active==True)&(db.relPersona.extraO==_id) & (db.tipoRelacionP2P.id==db.relPersona.relacion)
                        &(db.relacion.id==db.tipoRelacionP2P.parent)).\
                        select(db.tipoRelacionP2P.name,origenP.alias, destinoP.alias,db.relPersona.id,db.relPersona.origenP,
                                db.relPersona.destinoP,relacion.name,
                        join=[origenP.on(db.origenP.id==db.relPersona.origenP),
                              destinoP.on(db.destinoP.id==db.relPersona.destinoP)])

    borrar=auth.has_membership('administrator')
    return dict(aPersonas=aPersonas, _id=_id, aOrganizaciones=aOrganizaciones,
        aOrganizacionesD=aOrganizacionesD,aRelPersonas=aRelPersonas,borrar=borrar)

def relorgs_create():
    from gluon.serializers import json
    from fechas import fechas

    #Initialize the widget
    add_option = SELECT_OR_ADD_OPTION(form_title=T("Agregar Fuentes"), controller="fuentes", function="add_source", button_text = T("Nueva Fuente"))
    #assign widget to field
    db.RelPersOrg.documentSource.widget = add_option.widget

    id = request.args(0)

    persona = db.Organizacion(id) or redirect(URL('default','organization'))



    default_args= request.args(1) or 11

    ##redirect(URL('default','relorgs_create',args=[0,request.args(1),request.args(0)]))

    db.RelPersOrg.origenP.required = False
    db.RelPersOrg.origenP.requires = False
    db.RelPersOrg.origenP.widget = SQLFORM.widgets.autocomplete(request, db.persona.alias,
        id_field=db.persona.id, db=db(db.persona.is_active==True))
    #db.RelPersOrg.origenP.requires = False
    db.RelPersOrg.destinoO.requires = IS_IN_DB(db, 'Organizacion.id', 'Organizacion.alias')
    db.RelPersOrg.destinoO.widget = SQLFORM.widgets.options.widget
    db.RelPersOrg.destinoO.default = request.args(0)

    ##form=SQLFORM.factory(db.RelPersOrg,db.document)
    form=SQLFORM(db.RelPersOrg)
    if form.validate():
        form.vars.is_active=True
        form.vars.fdesde=fechas(form.vars.iniDay,form.vars.iniMonth,form.vars.iniYear)
        form.vars.fhasta=fechas(form.vars.finDay,form.vars.finMonth,form.vars.finYear)
        if(form.vars.origenP==""):
            if(form.vars._autocomplete_persona_alias_aux!=""):
                form.vars.alias=form.vars._autocomplete_persona_alias_aux
                form.vars.countryOfResidence=44
                idP = db.persona.insert(**db.persona._filter_fields(form.vars))
                if(idP!=None):
                    form.vars.origenP=idP
                    id = db.RelPersOrg.insert(**db.RelPersOrg._filter_fields(form.vars))
                    response.flash=T('Formulario aceptado')

            else:
                response.flash=T('Debe Ingresar una persona')
        else:
            id = db.RelPersOrg.insert(**db.RelPersOrg._filter_fields(form.vars))
            #response.flash = T('auto '+str(form.vars._autocomplete_persona_alias_aux)+' origen='+form.vars.origenP+'destino='+form.vars.destinoO)
            ##redirect(URL('default','persona'))
            ##redirect(URL('relorgs_edit',args=record.id))
            ##response.flash = T('Formulario aceptado'+form.vars.destinoO)
    elif form.errors:
        response.flash = T('auto '+str(form.vars._autocomplete_persona_alias_aux)+' origen='+form.vars.origenP)
        ##response.flash = T('Hay errores en el formulario')
    tree={}
    options=db(db.tipoRelacionP20.parent==0).select(orderby=db.tipoRelacionP20.relationship)
    for option in options:
        tree[str(option.id)]=T(option.relationship)

    default=db(db.tipoRelacionP20.id==default_args).select().first()
    pordefecto='"'+str(default.id)+'"'
    if(default.parent!=0):
        ##parent=db(db.tipoRelacionP20.id==default.parent).select().first()
        pordefecto='"'+str(default.parent)+'", "'+str(default.id)+'"'


    back_button = A(TAG.BUTTON(T('Volver'),_class='button'),_href=URL('organizations','index',vars=dict(keywords='Organizacion'+'.id="'+str(id)+'"')))

    return dict(form=form, option_tree=json(tree), default=pordefecto, _id=persona.id, back_button=back_button)

def organizacion_relation_create():
    relP2P = db.relPersona(request.args(0)) or redirect(URL('organization','index'))
    tiporelacion = request.args(1) or redirect(URL('organization','index'))

    ##permite crear entidad a partir del autocomplete
    db.RelPersOrg.destinoO.requires=None


    ##filter_args = request.args(1) or redirect(URL('profile'))
    personaO=db(db.persona.id==relP2P.origenP).select().first()
    personaD=db(db.persona.id==relP2P.destinoP).select().first()

    db.Organizacion.relationOrg.default=tiporelacion
    db.Organizacion.relacionP2P.default=request.args(0)

    tipoRel=db.tipoRelacionP2P(relP2P.relacion)
    db.Organizacion.nexo.default=tipoRel.name

    parent = T("Relación:")+ " "+personaO.alias+" "+T("es/fue (")+\
             tipoRel.name+") en/con "+personaD.alias

    form=SQLFORM(db.Organizacion, formstyle = 'divs')

    if form.validate():
        form.vars.relacionP2P=relP2P.id
        form.vars.relationOrg=tiporelacion
        if(form.vars.destinoO==""):
            if(form.vars._autocomplete_Organizacion_alias_aux!=""):

                form.vars.tipoOrg=12
                form.vars.name=form.vars._autocomplete_Organizacion_alias_aux
                form.vars.alias=form.vars._autocomplete_Organizacion_alias_aux
                form.vars.countryOfResidence=44
                idO = db.Organizacion.insert(**db.Organizacion._filter_fields(form.vars))
                if(idO!=None):
                    form.vars.destinoO=idO
                    id = db.organization_relation.insert(**db.organization_relation._filter_fields(form.vars))

                    ##if not exist relation insert data for 2 person
                    relPersonaO=db((db.RelPersOrg.origenP==personaO.id)&(db.RelPersOrg.destinoO==idO)).select().first()
                    if(relPersonaO==None):
                        idrelO=db.RelPersOrg.insert(specificRelation=156,
                            origenP=personaO.id, destinoO=idO, transitiveP2P=relP2P.id)

                    relPersonaD=db((db.RelPersOrg.origenP==personaD.id) & (db.RelPersOrg.destinoO==idO)).select().first()
                    if(relPersonaD==None):
                        idrelD=db.RelPersOrg.insert(specificRelation=156,
                            origenP=personaD.id, destinoO=idO, transitiveP2P=relP2P.id)


                    ##update transitive
                    ##relP2P.update_record(transitive=idrel)

                    response.flash=T('Formulario aceptado')
                    redirect(URL('default','profile'))
            else:
                response.flash=T('Debe Ingresar una Organización/Empresa ')
        else:
            idO = db.organization_relation.insert(**db.organization_relation._filter_fields(form.vars))
            ##if not exist relation insert data for 2 person
            relPersonaO=db((db.RelPersOrg.origenP==personaO.id)&(db.RelPersOrg.destinoO==idO)).select().first()
            if(relPersonaO==None):
                idrelO=db.RelPersOrg.insert(specificRelation=156,
                    origenP=personaO.id, destinoO=idO, transitiveP2P=relP2P.id)

            relPersonaD=db((db.RelPersOrg.origenP==personaD.id) & (db.RelPersOrg.destinoO==idO)).select().first()
            if(relPersonaD==None):
                idrelD=db.RelPersOrg.insert(specificRelation=156,
                    origenP=personaD.id, destinoO=idO, transitiveP2P=relP2P.id)

            ##update transitive
            ##relPersona2Org.update_record(transitive=idrel)

            redirect(URL('default','profile'))

    elif form.errors:
        response.flash = T('Hay errores en el formulario')
    return dict(form=form, parent=parent)

@auth.requires_login()
def relPersona_create():
    redirect(URL('default','relPersona_create',args=[0,request.args(1),request.args(0)]))

    return locals()

def relPersona_edit():
    redirect(URL('default','relPersona_edit',args=[0,request.args(1),request.args(0)]))
    return locals()

def relOrg2Org_create():
    from gluon.serializers import json
    from fechas import fechas

    #Initialize the widget
    add_option = SELECT_OR_ADD_OPTION(form_title=T("Agregar Fuentes"), controller="fuentes", function="add_source", button_text = T("Nueva Fuente"))
    #assign widget to field
    db.relOrg2Org.documentSource.widget = add_option.widget

    db.relOrg2Org.destinoO.requires =  None



    organizacion=db.Organizacion(request.args(0)) or redirect(URL('default','organization'))
    _id=request.args(0); filter_arg=request.args(1) or 1
    tree={}
    options=db(db.tipoRelacionOrg2Org.parent==0).select(orderby=db.tipoRelacionOrg2Org.name)
    for option in options:
        tree[str(option.id)]=T(option.name)

    default=db(db.tipoRelacionOrg2Org.id==filter_arg).select().first()
    pordefecto='"'+str(default.id)+'"'
    if(default.parent!=0):
        pordefecto='"'+str(default.parent)+'", "'+str(default.id)+'"'

    db.relOrg2Org.origenO.default=organizacion.id

    form=SQLFORM(db.relOrg2Org,formstyle = 'divs')

    if form.validate():
        form.vars.is_active='T'
        form.vars.fdesde=fechas(form.vars.iniDay,form.vars.iniMonth,form.vars.iniYear)
        form.vars.fhasta=fechas(form.vars.finDay,form.vars.finMonth,form.vars.finYear)
        if(form.vars.destinoO==""):
            if(form.vars._autocomplete_Organizacion_alias_aux!=""):
                form.vars.tipoOrg=12
                form.vars.name=form.vars._autocomplete_Organizacion_alias_aux
                form.vars.alias=form.vars._autocomplete_Organizacion_alias_aux
                form.vars.countryOfResidence=44
                form.vars.is_active='T'
                idO = db.Organizacion.insert(**db.Organizacion._filter_fields(form.vars))
                if(idO!=None):
                    form.vars.destinoO=idO
                    id = db.relOrg2Org.validate_and_insert(**db.relOrg2Org._filter_fields(form.vars))
                    if(id!=None):
                        response.flash=T('Formulario aceptado')
                    response.flash=T('despues '+form.vars.relationOrg)
                else:
                    response.flash=T('despues1 '+form.vars.relationOrg)
            else:
                response.flash=T('Debe Ingresar un grupo ')
        else:
            id = db.relOrg2Org.validate_and_insert(**db.relOrg2Org._filter_fields(form.vars))
            response.flash=T('Formulario aceptado')
    elif form.errors:
        response.flash = T('Hay errores en el formulario')

    perfil = 'Organizacion'
    back_controller = 'organizations'
    if organizacion.tipoOrg==2:
        back_controller = 'companies'

    back_button = A(TAG.BUTTON(T('Volver'),_class='button'),_href=URL(back_controller,'index',vars=dict(keywords=perfil+'.id="'+str(_id)+'"')))

    return dict(form=form, option_tree=json(tree), default=pordefecto, _id=_id, back_button=back_button)

def relOrg2Org_edit():
    from gluon.serializers import json
    from fechas import fechas
    response.view='organizacion/relOrg2Org_create.html'
    record=db.relOrg2Org(request.args(0)) or redirect(URL('default','organization'))

    #Initialize the widget
    add_option = SELECT_OR_ADD_OPTION(form_title=T("Agregar Fuentes"), controller="fuentes", function="add_source", button_text = T("Nueva Fuente"))
    #assign widget to field
    db.relOrg2Org.documentSource.widget = add_option.widget

    db.relOrg2Org.destinoO.requires =  None


    form=SQLFORM(db.relOrg2Org, record, formstyle = 'divs')

    if form.validate():
        form.vars.is_active='T'
        form.vars.fdesde=fechas(form.vars.iniDay,form.vars.iniMonth,form.vars.iniYear)
        form.vars.fhasta=fechas(form.vars.finDay,form.vars.finMonth,form.vars.finYear)
        if(form.vars.destinoO==""):
            if(form.vars._autocomplete_Organizacion_alias_aux!=""):
                form.vars.tipoOrg=12
                form.vars.name=form.vars._autocomplete_Organizacion_alias_aux
                form.vars.alias=form.vars._autocomplete_Organizacion_alias_aux
                form.vars.countryOfResidence=44
                form.vars.is_active='T'
                idO = db.Organizacion.insert(**db.Organizacion._filter_fields(form.vars))
                if(idO!=None):
                    form.vars.destinoO=idO
                    form.vars.id=record.id
                    auth.archive(form)
                    id = record.update_record(**db.relOrg2Org._filter_fields(form.vars))
                    response.flash=T('Formulario aceptado')
                else:
                    response.flash=T('Error al ingresar '+form.vars.relationOrg)
            else:
                response.flash=T('Debe Ingresar un grupo ')
        else:
            form.vars.id=record.id
            auth.archive(form)
            id = record.update_record(**db.relOrg2Org._filter_fields(form.vars))
            response.flash=T('Formulario aceptado '+form.vars.relationOrg)
    elif form.errors:
        response.flash = T('Hay errores en el formulario')

    _id=record.origenO; filter_arg=record.relationOrg
    tree={}
    options=db(db.tipoRelacionOrg2Org.parent==0).select(orderby=db.tipoRelacionOrg2Org.name)
    for option in options:
        tree[str(option.id)]=T(option.name)

    default=db(db.tipoRelacionOrg2Org.id==filter_arg).select().first()
    pordefecto='"'+str(default.id)+'"'
    if(default.parent!=0):
        pordefecto='"'+str(default.parent)+'", "'+str(default.id)+'"'

    organizacion = db.Organizacion(_id)
    perfil = 'Organizacion'
    back_controller = 'organizations'
    if organizacion.tipoOrg==2:
        back_controller = 'companies'

    back_button = A(TAG.BUTTON(T('Volver'),_class='button'),_href=URL(back_controller,'index',vars=dict(keywords=perfil+'.id="'+str(_id)+'"')))

    return dict(form=form, option_tree=json(tree), default=pordefecto, _id=_id, back_button=back_button)

def perfil():
    redirect(URL('default','organization',args=request.args(0)))

@service.json
def get_relacion(id):
    tree={}
    options=db(db.tipoRelacionOrg2Org.parent==id).select(orderby=db.tipoRelacionOrg2Org.name)
    for option in options:
        tree[str(option.id)]=T(option.name)
    return tree



