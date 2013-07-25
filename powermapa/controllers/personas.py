__author__ = 'Evolutiva'

@auth.requires_login()
def index():
    #Initialize the widget
    add_option = SELECT_OR_ADD_OPTION(form_title=T("Agregar Fuentes"), controller="fuentes", function="add_source",
                                      button_text = T("Nueva Fuente"))
    #assign widget to field
    db.persona.documentSource.widget = add_option.widget

    add_option_document_cloud = SELECT_OR_ADD_OPTION(form_title=T("Agregar Document Cloud"), controller="document",
                                                     function="add_document",
                                                     button_text = T("Nuevo Documento"),dialog_width=600)
    #assign widget to field
    db.persona.documentCloud.widget = add_option_document_cloud.widget

    if request.args(0)=='view':
        #response.new_window = URL('visualizacion','caso_perfil',args=[request.args(1),request.args(1)])
        redirect(URL('visualizacion','caso_perfil',args=[request.args(2),request.args(1)]))
    elif request.args(0)=='new':
        redirect(URL('personas','new'))
    elif request.args(0)=='edit':
        redirect(URL('default','person',args=request.args(2)))


    query = (db.persona.is_active==True)
    links =[]
    fields=(db.persona.id,db.persona.alias,db.persona.depiction,db.persona.firstName,
            db.persona.firstLastName, db.persona.otherLastName)
    if auth.user_id:
        links = [dict(header=T('Conexiones'),_class='w2p_trap',
                      body=lambda row: A(IMG(_src=URL('static','plugin_powertable/images/details_open.png'),
                                            _alt=T('Ver Conexiones'),_id='image'+str(row.id)),
                                         #callback=URL('personas','connections',args=row.id),, target='t'
                                         _onclick='addConnections(event,'+str(row.id)+')'))]
    grid = SQLFORM.grid(query, fields = fields, orderby=db.persona.alias,
                        csv=False,formargs={'active':'persona'},links=links)
    return dict(persona_grid=grid)

@auth.requires_login()
def person():
    query = (db.persona.is_active==True)
    fields=(db.persona.id,db.persona.alias,db.persona.depiction,db.persona.firstName,
            db.persona.firstLastName, db.persona.otherLastName)
    grid = SQLFORM.grid(query, fields = fields)
    return dict(grid=grid)


@auth.requires_login()
def connections():
    response.view = 'default/familydetails.html'
    _id=""; parientes=parientesD=conexiones=selectP2P=conexionO=conexionD=seleccionP20=P2O=companeros=companerosD=conyuges=conyugesD=None; borrar=None; grid=""
    if(request.ajax):
        _id=request.args(0)
        if _id==None: response.view='error404.html'
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

            grid = ""

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
def new():
    #Initialize the widget
    add_option = SELECT_OR_ADD_OPTION(form_title=T("Agregar Fuentes"), controller="fuentes", function="add_source", button_text = T("Nueva Fuente"))
    #assign widget to field
    db.persona.documentSource.widget = add_option.widget

    add_option_document_cloud = SELECT_OR_ADD_OPTION(form_title=T("Agregar Document Cloud"), controller="document", function="add_document",
                                                     button_text = T("Nuevo Documento"),dialog_width=600)
    #assign widget to field
    db.persona.documentCloud.widget = add_option_document_cloud.widget

    form=SQLFORM(db.persona)

    if form.process().accepted:
       response.flash = 'Formulario Acceptado'
       redirect(URL('personas','index',vars=dict(keywords='persona.id="'+str(form.vars.id)+'"')))
    elif form.errors:
       response.flash = 'Formulario tiene errores'


    return dict(form=form,title=T('Personas: Datos Básicos'))


