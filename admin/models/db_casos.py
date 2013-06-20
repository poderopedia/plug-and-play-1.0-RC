__author__ = 'Evolutiva'
from plugin_ckeditor import CKEditor
ckeditor = CKEditor(db)
ckeditor.define_tables()

##tabla caso
db.define_table('caso',
                Field('depiction', 'upload', label=T('Logotipo')),
                Field('name','string',label=T('Nombre')),
                Field('description','text',label=T('Reseña'), widget=ckeditor.widget),
                Field('country',db.country,label=T('País'),requires=IS_IN_DB(db, 'country.id', 'country.name'),default=44),
                Field('city','string',label=T('Ciudad')),
                Field('documentSource','list:reference document',required=False,
                      requires=IS_IN_DB(requiere,'document.id','%(name)s / (documentURL)s',multiple=True),
                      label=T('Fuentes')),
                Field('documentCloud','list:reference documentCloud',required=False,
                      requires=IS_IN_DB(db,'documentCloud.id','%(title)s',multiple=True),
                      label=T('Fuentes Document Cloud')),
                auth.signature,
                format='%(name)s'
)

db.define_table('person2caso',
                Field('origenC',db.caso,required=True, label=T('Caso')),
                Field('destinoP',db.persona, required=True,  label=T('Persona'),
                      widget = SQLFORM.widgets.autocomplete(request, db.persona.alias, id_field=db.persona.id, limitby=(0,10), min_length=2)),
                Field('nexus','text', label=T('Nexo'))
)

db.define_table('org2caso',
                Field('origenC',db.caso,required=True, label=T('Caso')),
                Field('destinoO',db.Organizacion,required=True, label=T('Organización'),
                      widget = SQLFORM.widgets.autocomplete(request, db.Organizacion.alias, id_field=db.Organizacion.id, limitby=(0,10), min_length=2)),
                Field('nexus','text',label=T('Nexo'))
)