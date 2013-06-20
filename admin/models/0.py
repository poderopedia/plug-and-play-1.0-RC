from gluon.storage import Storage
settings = Storage()

settings.migrate = False
settings.title = 'Poderopedia'
settings.subtitle = 'powered by Poderopedia'
settings.author = 'Juan Eduardo'
settings.author_email = 'dev@poderopedia.com'
settings.keywords = ''
settings.description = ''
settings.layout_theme = 'default'
settings.database_uri = 'mysql://testing:powertest@localhost/powertest'
settings.security_key = 'b0336a10-e263-487f-b744-719b83741aeb'
settings.login_config = ''
settings.plugins = []


settings.email_server = 'smtp.gmail.com:587'
settings.email_sender = 'mailman@poderopedia.com'
settings.email_login = 'mailman@poderopedia.com:hgst6s-98als-1'

response.title = request.application
response.subtitle = T('Redes de Poder en la Política y Negocios')
response.meta.author = 'Equipo Poderopedia'
response.meta.description = T('Redes de Poder en la Política y Negocios')
response.meta.keywords = 'Redes, Poder, Negocios, Política'

endYear=int(request.now.strftime('%Y'))
day_list=[x for x in range(1,32)]
day_list.append(T('Sin Fecha'))
day_list.append('')
month_list=[x for x in range(1,13)]
month_list.append(T('Sin Fecha'))
month_list.append('')
year_list=[x for x in range(1900,endYear+10)]
year_list.append(T('Sin Fecha'))
year_list.append('')


if request.vars.force_language:
    session.language=request.vars.force_language
if session.language: T.force(session.language)
