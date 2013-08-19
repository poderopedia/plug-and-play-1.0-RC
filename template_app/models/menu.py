# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = ' '.join(word.capitalize() for word in request.application.split('_'))
response.subtitle = T('customize me!')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.title = request.application
response.subtitle = T('Redes de Poder en la Política y Negocios')
response.meta.author = 'Equipo Poderopedia'
response.meta.description = T('Redes de Poder en la Política y Negocios')
response.meta.keywords = 'Redes, Poder, Negocios, Política'
response.meta.generator = 'Equipo Poderopedia'


## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default','index'), [])
    ]



