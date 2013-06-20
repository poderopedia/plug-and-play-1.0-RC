__author__ = 'Evolutiva'


##api request
auth.settings.allow_basic_login = True
@auth.requires_login()
@request.restful()
def api():
    response.view = 'generic.'+request.extension
    def GET(*args,**vars):
        patterns = 'auto'
        parser = db.parse_as_rest(patterns,args,vars)
        if parser.status == 200:
            return dict(content=parser.response)
        else:
            raise HTTP(parser.status,parser.error)
    def POST(table_name,**vars):
        return db[table_name].validate_and_insert(**vars)
    def PUT(table_name,record_id,**vars):
        return db(db[table_name]._id==record_id).update(**vars)
    def DELETE(table_name,record_id):
        return db(db[table_name]._id==record_id).delete()
    return locals()

@auth.requires_login()
def upload_callback():

    if 'qqfile' in request.vars:
        filename = request.vars.qqfile
        newfilename = db.importer.filename.store(request.body, filename)
        id=db.importer.insert(filename=newfilename)

    return response.json({'success': 'true','filename':id})


@auth.requires_login()
def upload():
    return dict()

def parser_definition():
    import os
    uploadfolder=os.path.join(request.folder, 'uploads')
    doc=db.importer(request.args(0)) or redirect(URL('upload'))
    filename=doc.filename
    name = filename.strip().split('.')
    extension=name[4]
    columns='error'
    if (extension=='csv'):
        ##first line
        files = open(uploadfolder+'/'+filename,'r')
        for line in files:
            columns=line.strip().split(',')
            break
    form=SQLFORM.factory(
        Field('options', requires=IS_IN_SET(columns), required=False, label=T('Opciones'))
    )
    return dict(columns=columns, form=form)

def consumer():
    return dict()

def call(): return service()
##alias of the Person like 'Sebastian'
##country: isocode2 like 'Cl'
##relationship: family relationship
##isFather:{(alias='',country='',documentSource={..,..,..}),(alias='',country='',documentSource={..,..,..})}
##
##PersonList {{'alias':@@, 'country':@@},{},{}}
##documentSource: documentList
@auth.requires_login()
@service.json
def put_familyrelations(alias,country,relation,personList):
    countryiso = db(db.country.iso2==country).select().first()
    relationship=db(db.tipoParentesco.relation==relation).select().first()
    if(countryiso==None | relationship==None):
        return {'success':false,'error':T('País o relación no definida')}
    person = db((db.persona.alias==alias) & (db.persona.countryofResidence==countryiso.id)).select().first()
    if(person!=None):
        ID = db.persona.insert(alias=alias, countryofResidence=countryiso.id)
    else:
        ID = person.id
    for persona in PersonList:
        countryiso = db(db.country.iso2==persona.country).select().first()
        if(countryiso!=None):
            person=db((db.persona.alias==persona.alias) & (db.persona.countryofResidence==country.id)).select().first()
            if(person!=None):
                destinoP = db.persona.insert(alias=alias, countryofResidence=countryiso.id)
            else:
                destinoP = person.id
            relID=db.relFamiliar.validate_and_insert(origenP=ID,parentesco=relationship.id,destinoP=destinoP)
    return

def index():
    return dict()
