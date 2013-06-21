from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = 'Poderopedia'
settings.subtitle = 'powered by Poderopedia'
settings.author = 'Juan Eduardo'
settings.author_email = 'dev@poderopedia.com'
settings.keywords = ''
settings.description = ''
settings.layout_theme = 'default'
settings.database_uri = 'mysql://uername:password@localhost/databasename'
settings.security_key = 'b0336a10-e263-487f-b744-719b83741aeb'
settings.email_server = 'tourmailserver.org'
settings.email_sender = 'mailsender@mailserver.org'
settings.login_config = 'username:password'
settings.plugins = []
TEXT_EDITOR = 'amy'
VERIFIY_EMAIL = """
<html><body>Hola
                            <p>Gracias por registrarte en Poderopedia y sumarte a nuestra comunidad.</p>
                            <p>Por favor confirma tu email haciendo click <a href='"""+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+"""/%(key)s'>aquí</a>
                            (o copia y pega la URL en tu navegador):<br /> http://"""\
                +request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+"""/%(key)s para verificar tu email</p>
<p>Como miembro registrado de Poderopedia puedes:</p>
<ul>
  <li>Sugerir que incluyamos de nuevos perfiles</li>
  <li>Sugerir conexiones para ser agregadas a perfiles existentes</li>
  <li> Reportar errores</li>
  <li> Reportar contenido inadecuado</li>
  <li>Recibir notificaciones de tus sugerencias y reportes</li>
</ul>
<p>Siempre estamos agregando nuevas características y escuchando tus sugerencias de cómo mejorar.
Sigue nuestro <a href="http://blog.poderopedia.org">blog</a> para novedades y haznos saber lo que necesitas de Poderopedia <a href="http://poderopedia.uservoice.com">aquí</a> </p>
<p>Bienvenido,<br />
  El Equipo de Poderopedia</p>
  <h5>Por  favor, no respondas a este mensaje: fue enviado de manera automática por DomoArigatoDiscoRoboto, el robot de mensajería instantánea de Poderopedia. </h5>
</body>
</html>
"""

RESET_PASSWORD = """
<html><body>Hola
                            <p>¿Olvidaste tu contraseña de Poderopedia? No te preocupes, pasa hasta en las mejores familias.</p>
                            <p>Haz click <a href='"""+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+"""/%(key)s'>aquí</a> para restablecer tu contraseña
                            (o copia y pega la URL en tu navegador):<br /> http://"""\
                +request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+"""/%(key)s</p>
<p>*Si recibiste este correo pero no has solicitado restablecer tu contraseña, puedes entrar <a href='"""+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+"""/%(key)s'>aquí</a> y cambiar la configuración de tu cuenta.</p>

<p>Gracias,<br />
  El Equipo de Poderopedia</p>
  <h5>Por  favor, no respondas a este mensaje: fue enviado de manera automática por DomoArigatoDiscoRoboto, el robot de mensajería instantánea de Poderopedia. </h5>
</body>
</html>
"""

RESET_PASSWORD_NEXT= """
<html><body>Hola
                            <p>Felicitaciones. Has cambiado tu contraseña con éxito.</p>
                            
<p>Gracias,<br />
  El Equipo de Poderopedia</p>
  <h5>Por  favor, no respondas a este mensaje: fue enviado de manera automática por DomoArigatoDiscoRoboto, el robot de mensajería instantánea de Poderopedia. </h5>
</body>
</html>
"""

T.set_current_languages('es', 'es-es')
T.set_current_languages('en', 'en-en')
T.force(request.lang)
import re
p = re.compile(r'<.*?>')


CONFIGURACION_OK = """
<html><body>Hola
                            <p>Felicitaciones. Has cambiado tu contraseña con éxito.</p>
                            <p>Gracias, </p>
                            <p>El Equipo de Poderopedia</p>

  <h5>Por favor, no respondas a este mensaje: fue enviado de manera automática por DomoArigatoDiscoRoboto, el robot de mensajería instantánea de Poderopedia. </h5>
</body>
</html>
"""


