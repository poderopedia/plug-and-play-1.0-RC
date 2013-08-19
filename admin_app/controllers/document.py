__author__ = 'Evolutiva'

def create():
    #from documentCloud import document_cloud
    import os
    import json
    from documentcloud import DocumentCloud
    dc_id =None



    #db.documentCloud.referenceEntity.default='organizacion'
    #db.documentCloud.id_reference.default=_id
    #db.documentCloud.project.default=7144

    form=SQLFORM(db.documentCloud)


    jeison={}
    if form.validate():
        dc_cloud = DocumentCloud(username=dc_username,password=dc_password)
        dc_id=dc_cloud.documents.upload(
            os.path.join(request.folder,'uploads',form.vars['file']),
            title=form.vars['title'],
            source=form.vars['source'],
            description=form.vars['description'],
            related_article=form.vars['related_article'],
            published_url=form.vars['published_url'],
            access=form.vars['access'],
            project=form.vars['project'],
            #data=json.dumps(form.vars['data']),
            secure=form.vars['secure']
            )
        if dc_id is not None:
            form.vars.dc_id = dc_id.id
            id = db.documentCloud.insert(**db.documentCloud._filter_fields(form.vars))

            response.flash = T('Formulario aceptado')
        else:
            response.flash = T('Error en subir Documento a DocumentCloud')

    elif form.errors:
        response.flash = T('Hay errores en el formulario')
    else:
        response.flash = T('Por favor llene el formulario')




    return dict(form=form)

def search():
    from documentcloud import DocumentCloud
    client = DocumentCloud()

    obj_list = {}

    form=FORM(T('Búsqueda:'), INPUT(_name='q'), INPUT(_type='submit'))
    if form.validate():

        obj_list = client.documents.search(form.vars.q)




    return dict(form=form, obj_list=obj_list)

def dc_restful_client():
    return locals()


def add_document():
    import os
    import json
    from documentcloud import DocumentCloud
    dc_id =None
    respuesta = None
    #this is the controller function that will appear in our dialog
    form = SQLFORM(db.documentCloud)

    if form.validate():
        dc_cloud = DocumentCloud(username=dc_username,password=dc_password)
        dc_id=dc_cloud.documents.upload(
            os.path.join(request.folder,'uploads',form.vars['file']),
            title=form.vars['title'],
            source=form.vars['source'],
            description=form.vars['description'],
            related_article=form.vars['related_article'],
            published_url=form.vars['published_url'],
            access=form.vars['access'],
            project=form.vars['project'],
            #data=json.dumps(form.vars['data']),
            secure=form.vars['secure']
            )
        if dc_id is not None:
            form.vars.dc_id = dc_id.id
            id = db.documentCloud.insert(**db.documentCloud._filter_fields(form.vars))
            respuesta = request.post_vars


            #Successfully added new item
            #do whatever else you may want

            #Then let the user know adding via our widget worked
            response.flash = T("Added")
            target= request.args[0]
            #close the widget's dialog box
            response.js = '$( "#%s_dialog-form" ).dialog( "close" ); ' %(target)
            #update the options they can select their new category in the main form
            response.js += """$("#%s").append("<option value='%s'>%s</option>");""" \
                    % (target, form.vars.id, form.vars.name)
            #and select the one they just added
            response.js += """var selected=$("#%s").val();""" %(target)
            response.js += """if (selected==null) { selected = [] }"""
            response.js += """selected.push("%s");""" %(form.vars.id)
            response.js += """$("#%s").val(selected);""" %(target)
            #finally, return a blank form incase for some reason they wanted to add another option
            return form
        else:
            response.flash = T('Error en subir Documento a DocumentCloud')
            return form
    elif form.errors:
        #silly user, just send back the form and it'll still be in our dialog box complete with error messages
        return form
    else:
        #hasn't been submitted yet, just give them the fresh blank form
        return form

def edit():
    from documentcloud import DocumentCloud
    dc_id = request.args(0) or redirect(URL('document','index'))
    db.documentCloud.file.requires=None
    record = db.documentCloud(dc_id)
    form = SQLFORM(db.documentCloud,record)

    if form.validate():
        client = DocumentCloud(username=dc_username,password=dc_password)
        doc_cloud = client.documents.get(record.dc_id)
        doc_cloud.title=form.vars['title']
        doc_cloud.source=form.vars['source']
        doc_cloud.description=form.vars['description']
        doc_cloud.related_article=form.vars['related_article']
        doc_cloud.published_url=form.vars['published_url']
        doc_cloud.access=form.vars['access']
        doc_cloud.project=form.vars['project']
        #data=json.dumps(form.vars['data']),
        doc_cloud.secure=form.vars['secure']
        rest = doc_cloud.put()
        if rest is not None:
            response.flash = T('Documento actualizado')
    elif form.errors:
        response.flash = T('Hay errores en el formulario')
    else:
        response.flash = T('Por favor llene el formulario')


    return dict(form=form)

def index():

    if request.args(0)=='edit':
        redirect(URL('document','edit',args=request.args(2)))
    elif request.args(0)=='view':
        redirect(URL('document','view',args=request.args(2)))

    query = (db.documentCloud.is_active==True)
    links =[]
    fields=(db.documentCloud.id,db.documentCloud.title,db.documentCloud.file,db.documentCloud.source,
            db.documentCloud.access)
    if auth.user_id:
        links = [dict(header=T('Conexiones'),_class='w2p_trap',
                      body=lambda row: A(IMG(_src=URL('static','plugin_powertable/images/details_open.png'),
                                            _alt=T('Ver Conexiones'),_id='image'+str(row.id)),
                                         #callback=URL('personas','connections',args=row.id),, target='t'
                                         _onclick='addConnections(event,'+str(row.id)+')'))]
    grid = SQLFORM.grid(query, fields = fields, orderby=db.documentCloud.title,
                        csv=False,formargs={'active':'persona'},links=links)
    return dict(persona_grid=grid)

def view():
    id=request.args(0)
    doc_cloud = db.documentCloud(id)
    dc_id = doc_cloud.dc_id
    title=doc_cloud.title
    return dict(dc_id=dc_id,title=title)

def update_all():
    from documentcloud import DocumentCloud
    client = DocumentCloud(username=dc_username,password=dc_password)
    client_docs = DocumentCloud(username=dc_username,password=dc_password)
    document_ids = {}; insert=[]

    projects_list = client.projects.all()
    for project in projects_list:
        try:
            obj = client_docs.projects.get(project.id)
            document_ids[project.id] = obj.document_list
        except:
            ex = T('No existe Projecto')
        #document_ids[project] = obj.document_ids
        #document_ids[project] = project.title
        if len(document_ids[project.id])>0:
            for doc in document_ids[project.id]:
                doc_cloud=db((db.documentCloud.dc_id==doc.id) & (db.documentCloud.is_active==True)).select().first()
                if doc_cloud is None:
                    docs=db.documentCloud.validate_and_insert(dc_id=doc.id,title=doc.title,project=project.id,is_active=True)
                    insert.append(docs)
                else:
                    doc_cloud.dc_id=doc.id
                    doc_cloud.title=doc.title
                    doc_cloud.source=doc.source
                    doc_cloud.description=doc.description
                    doc_cloud.related_article=doc.related_article
                    doc_cloud.published_url=doc.published_url
                    doc_cloud.access=doc.access
                    doc_cloud.project=project.id
                    #data=json.dumps(form.vars['data']),
                    #doc_cloud.secure=doc.secure
                    doc_cloud.update_record()

    return dict(projects=projects_list, docs=insert)
