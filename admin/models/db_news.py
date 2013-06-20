# coding: utf8


db.define_table('destacados',
    Field('imagen', 'upload', uploadfield=True, required=True),
    Field('titulo', 'string', readable=True, writable=True, label=T('Titulo'), required=True),
    Field('tag', 'string', readable=True, writable=True, label=T('Tag'),length=19),
    Field('contenido','text', readable=True, writable=True, label=T('Contenido'), required=True),
    Field('fecha','datetime', readable=True, required=True, default=request.now),
    Field('url','string', default='#', readable=True, writable=True, label=T('URL'), required=True),
    Field('referenceEntity', 'string',requires=IS_IN_SET(entityList),label=T('Seleccione Entidad'),writable=True,readable=True),
    Field('reference', 'integer', writable=True,readable=False,required=True, requires=IS_NOT_EMPTY(error_message=T('complete este campo!'))),
    Field('alias', 'string', writable=True,readable=True,required=True, requires=IS_NOT_EMPTY(T('complete este campo!'))),
    auth.signature,
    migrate=False
)


