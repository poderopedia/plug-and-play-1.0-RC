from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = 'Poderopedia'
settings.subtitle = 'powered by Poderopedia'
settings.author = 'Poderopedia Team'
settings.author_email = 'dev@poderopedia.com'
settings.keywords = ''
settings.description = ''
settings.layout_theme = 'default'
settings.database_uri = 'mysql://test:test@localhost/test'
settings.security_key = 'b0336a10-e263-487f-b744-719b83741aeb'
settings.login_config = ''
settings.plugins = []


settings.email_server = 'your.smtp.server'
settings.email_sender = 'your.email@domain.org'
settings.email_login = 'username:password'

response.title = request.application
response.subtitle = T('Redes de Poder en la Política y Negocios')
response.meta.author = T('Equipo Poderopedia')
response.meta.description = T('Redes de Poder en la Política y Negocios')
response.meta.keywords = T('Redes, Poder, Negocios, Política')

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


#for testing a particular language
#if request.vars.force_language:
#    session.language=request.vars.force_language
#if session.language: T.force(session.language)
