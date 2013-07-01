__author__ = 'Evolutiva'
from documentCloud import document_cloud

#document settings
dc_username='username'
dc_password='password'

entityList=['persona','empresa','organizacion']
access_list=['public','private','organization']
dc_cloud = document_cloud (username=dc_username, password=dc_password)
project_list = dc_cloud.get_projects()
db.define_table('documentCloud',
    Field('dc_id','string',readable=False,writable=False),
    Field('file', 'upload', requires = IS_UPLOAD_FILENAME(extension='pdf',lastdot=True)),
    Field('title', 'string', required=True,requires=IS_NOT_EMPTY(), label=T('Titulo Documento')),
    Field('source', 'string', label=T('Fuente del Documento'),requires=IS_NOT_EMPTY()),
    Field('description', 'text',label=T('Descripción del Documento')),
    Field('related_article', 'string',label=T('URL del documento asociado'),comment=T('the URL of the article associated with the document')),
    Field('published_url', 'string',label=T('URL donde el documento será embedido'),comment=T('the URL of the page on which the document will be embedded')),
    Field('access', 'string',requires=IS_IN_SET(access_list),default='public'),
    Field('project', 'integer', requires=IS_IN_SET(project_list)),
    Field('data', 'string',default='{"date":'+str(request.now)+', "auth_user":'+str(me)+'}'),
    Field('secure', 'string',default='false'),
    auth.signature,
    format='%(title)s'
)
