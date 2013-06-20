response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description
response.menu = [
    (T('Home'), False, URL('default','index'),[]),
    (T('Crear'),False, False,[
        (T('Persona'), False, URL('personas','index'),[]),
        (T('Empresa'), False, URL('companies','index'),[]),
        (T('Organizacion'), False, URL('organizations','index'),[]),
        (T('Crear Caso'),False, False,[
            (T('Editar Caso'), False, URL('casos','edit'),[]),
            (T('Crear/Listar Caso'), False, URL('casos','index',),[]),
        ]),
    ]),
    (T('Administrar'),False,False,[
    (T('Portada'), False, False,[
            (T('Nueva'), False, URL('news','news_insert'),[]),
            (T('Listar'), False, URL('news','destacados'),[]),
        ]),
    (T('Mis Fuentes'), False, URL('default','document'),[]),
    (T('Document Cloud'), False, False,[
            (T('Subir a DocumentCloud'),False,URL('document','create'),[]),
            (T('Editar/Listar'),False,URL('document','index'),[]),
            (T('Recuperar documentos desde DocumentCloud'),False, URL('document','update_all'),[])
        ]),
    ]),
    (T('Sugerencias'),False,False,[
        (T('Conexiones'), False, URL('crowdsourcing','sugerirConexion'),[]),
        (T('Tengo Dato'), False, URL('crowdsourcing','tengoDato'),[]),
        (T('Persona'), False, URL('crowdsourcing','sugerirPersona'),[]),
        (T('Error'), False, URL('crowdsourcing','tipoerror'),[]),
        (T('Contenido Inadecuado'), False, URL('crowdsourcing','tipoinadecuado'),[]),
        ]),
    ]
