__author__ = 'Evolutiva'


entityList=[T('persona'),('empresa'),T('organizacion')]
estadoList=[T('sin revision'),T('rechazada'),T('aprobada / en curso / asignado')]
db.define_table('sugerirConexion',
    Field('referenceEntity', 'string',requires=IS_IN_SET(entityList),label=T('Seleccione Entidad'),writable=False,readable=True),
    Field('reference', 'integer', writable=False,readable=True,required=True, requires=IS_NOT_EMPTY(error_message=T('complete este campo!'))),
    Field('alias', 'string', writable=False,readable=True,required=True, requires=IS_NOT_EMPTY(T('complete este campo!'))),
    Field('name','string',required=True,label=T('Quiero sugerir'), requires=IS_NOT_EMPTY(T('complete este campo!'))),
    Field('texto','text',label=T('¿Cómo están relacionados?'), required=True, requires=IS_NOT_EMPTY(T('complete este campo!'))),
    Field('documentURL','string',requires=IS_URL(T('ingrese URL válida!')), label=T('Obtuve esta información de'), required=True, default='Ingresa =URL'),
    Field('estado','string',requires=IS_IN_SET(estadoList), default='sin revision',writable=True,readable=True,label=T('Estado')),
    auth.signature
)

##sugerir persona
db.define_table('sugerirPersona',
    Field('name','string',required=True,label=T('Quiero sugerir el perfil de'),requires=IS_NOT_EMPTY(error_message=T('complete este campo!'))),
    Field('texto','text',label=T('¿Por qué es importante?'),requires=IS_NOT_EMPTY(error_message=T('complete este campo!'))),
    Field('documentURL','string',requires=IS_URL(T('ingrese URL válida!')), label=T('Obtuve esta información de'), required=True),
    Field('estado','string',requires=IS_IN_SET(estadoList), default='sin revision',writable=False,readable=True,label=T('Estado')),
    auth.signature
)

db.define_table('tipoerror',
    Field('referenceEntity','string',requires=IS_IN_SET(entityList),label=T('Reportar Error en:'),writable=False,readable=True),
    Field('reference', 'integer', writable=False,readable=True),
    Field('contenido','text',label=T('¿Cual es el Error?'),requires=IS_NOT_EMPTY(T('complete este campo!'))),
    Field('URL','string',requires=IS_URL(T('Ingrése una URL válida!')), label=T('Obtuve esta información de'), required=True),
    #Field('tipoError',requires=IS_IN_SET(errorEstado),writable=False,readable=True),
    Field('estado','string',requires=IS_IN_SET(estadoList), default='sin revision',writable=False,readable=True,label=T('Estado')),
    auth.signature
)

##notificaciones tipoerror
#errorEstado=['reportarError','contenidoInadecuado']
db.define_table('tipoinadecuado',
    Field('referenceEntity','string',requires=IS_IN_SET(entityList),label=T('Reportar Contenido Inadecuado en:'),writable=False,readable=True),
    Field('reference', 'integer', writable=False,readable=True),
    Field('contenido','text',label=T('¿Cual es el Contenido Inadecuado?')),
    Field('URL','string',requires=IS_URL(), label=T('Obtuve esta información de'), required=True),
    #Field('tipoError',requires=IS_IN_SET(errorEstado),writable=False,readable=True),
    Field('estado','string',requires=IS_IN_SET(estadoList), default='sin revision',writable=False,readable=True,label=T('Estado')),
    auth.signature
)

##compartir a un amigo
db.define_table('compartir',
    Field('email','string',required=True,label=T('Email'),requires=IS_EMAIL()),
    Field('contenido','text',label=T('mensaje')),
    Field('fecha','date',writable=False,readable=False,default=request.now),
    Field('pagina','string',writable=False,readable=False),
)
errorEstado=['reportarError','contenidoInadecuado']
db.define_table('notificaciones',
    Field('referenceEntity','string',requires=IS_IN_SET(entityList),label=T('Conexión con'),writable=False,readable=True),
    Field('reference', 'integer', writable=False,readable=True),
    Field('contenido','text',label=T('¿Cual es el contenido inadecuado?')),
    Field('URL','string',requires=IS_URL(), label=T('Obtuve esta información de'), required=True),
    Field('tipoError',requires=IS_IN_SET(errorEstado),writable=False,readable=True),
    Field('estado','string',requires=IS_IN_SET(estadoList), default='sin revision',writable=False,readable=True,label=T('Estado')),
    auth.signature
)



##TODO
##tengo un dato
db.define_table('tengoDato',
    Field('nombre','string',required=True,label=T('Tengo datos importantes sobre'),requires=IS_NOT_EMPTY(T('complete este campo!'))),
    Field('contenido','text',label=T('Contenido'),requires=IS_NOT_EMPTY(T('complete este campo!'))),
    Field('URL','string',requires=IS_URL(T('ingrese URL válida!')), label=T('Obtuve esta información de'), required=True),
    Field('estado','string',requires=IS_IN_SET(estadoList), default='sin revision',writable=False,readable=True,label=T('Estado')),
    Field('created_on','datetime',default=request.now)
)