# coding: utf8
__author__ = 'Evolutiva'


# coding: utf8
entityList=['persona','empresa','organizacion']
db.define_table('actualizacion',
    Field('referenceEntity','string',requires=IS_IN_SET(entityList),label=T('Requiere actualizacion:'),writable=False,readable=True),
    Field('reference', 'integer', writable=False,readable=True),
    Field('contenido','text',label=T('¿Por qué requiere actualizarse?'),requires=IS_NOT_EMPTY(T('complete este campo!'))),
    Field('URL','string',requires=IS_URL(T('Ingrése una URL válida!')), label=T('Obtuve esta información de'), required=True),
    #Field('tipoError',requires=IS_IN_SET(errorEstado),writable=False,readable=True),
    Field('estado','string',requires=IS_IN_SET(estadoList), default='sin revision',writable=False,readable=True),
    auth.signature,
    migrate=True
    )
