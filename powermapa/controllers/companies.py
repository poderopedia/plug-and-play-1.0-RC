__author__ = 'Evolutiva'

def index():

    #Initialize the widget
    add_option = SELECT_OR_ADD_OPTION(form_title=T("Agregar Fuentes"), controller="fuentes", function="add_source", button_text = T("Nueva Fuente"))
    #assign widget to field
    db.Organizacion.documentSource.widget = add_option.widget

    #Initialize the widget
    add_option_document = SELECT_OR_ADD_OPTION(form_title=T("Agregar Documento"), controller="document",
                                               function="add_document", button_text = T("Nuevo Documento"),
                                               dialog_width=600)
    #assign widget to field
    db.Organizacion.documentCloud.widget = add_option_document.widget

    links=[]

    if request.args(0)=='view':
        #response.new_window = URL('visualizacion','caso_perfil',args=[request.args(1),request.args(1)])
        redirect(URL('visualizacion','caso_organizacion',args=[request.args(2),request.args(1)]))
    elif request.args(0)=='new':
        redirect(URL('companies','new'))
    elif request.args(0)=='edit':
        redirect(URL('default','organization_edit',args=request.args(2)))

    if auth.user_id:
        links = [dict(header=T('Conexiones'),_class='w2p_trap',
                      body=lambda row: A(IMG(_src=URL('static','plugin_powertable/images/details_open.png'),
                                            _alt=T('Ver Conexiones'),_id='image'+str(row.id)),
                                         #callback=URL('personas','connections',args=row.id),, target='t'
                                         _onclick='addConnections(event,'+str(row.id)+')'))]

    query = (db.Organizacion.is_active==True) & (db.Organizacion.tipoOrg==2)
    fields=(db.Organizacion.id,db.Organizacion.alias,
            db.Organizacion.haslogo,db.Organizacion.hasSocialReason)
    grid = SQLFORM.grid(query, fields = fields, orderby=db.Organizacion.alias,
                        csv=False,formargs={'active':'persona'},links=links)
    return dict(companies_grid=grid)

def company():
    return dict()


def connections():
    response.view = 'organizacion/Organizationdetails.html'
    if(request.ajax):
        _id=request.args(0)
        if _id==None: response.view='error404.html'; return dict()
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
            aRelPersonas=db((db.relPersona.is_active==True)&(db.relPersona.extraO==_id) &
                            (db.tipoRelacionP2P.id==db.relPersona.relacion)
                            &(relacion.id==db.tipoRelacionP2P.parent)
                            &(db.persona.id==origenP.id)
                            &(origenP.id==db.relPersona.origenP)
                            &(destinoP.id==db.relPersona.destinoP)
                            ).select()


    borrar=auth.has_membership('administrator')
    return dict(aPersonas=aPersonas, _id=_id, aOrganizaciones=aOrganizaciones,
        aOrganizacionesD=aOrganizacionesD,aRelPersonas=aRelPersonas,borrar=borrar)

def new():
    response.view = 'personas/new.html'
    #Initialize the widget
    add_option = SELECT_OR_ADD_OPTION(form_title=T("Agregar Fuentes"), controller="fuentes", function="add_source", button_text = T("Nueva Fuente"))
    #assign widget to field
    db.Organizacion.documentSource.widget = add_option.widget

    #Initialize the widget
    add_option_document = SELECT_OR_ADD_OPTION(form_title=T("Agregar Documento"), controller="document",
                                               function="add_document", button_text = T("Nuevo Documento"),
                                               dialog_width=600)
    #assign widget to field
    db.Organizacion.documentCloud.widget = add_option_document.widget

    db.Organizacion.tipoOrg.default=2
    db.Organizacion.tipoOrg.writeable=False

    form=SQLFORM(db.Organizacion)
    if form.process().accepted:
       response.flash = 'Formulario Acceptado'
       redirect(URL('companies','index',vars=dict(keywords='Organizacion.id="'+str(form.vars.id)+'"')))
    elif form.errors:
       response.flash = 'Formulario tiene errores'


    return dict(form=form,title=T('Empresas: Datos Básicos'))

