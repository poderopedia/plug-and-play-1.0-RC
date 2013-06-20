# coding: utf8
__author__ = 'Evolutiva'

def index():
    alias=request.args(0)or redirect(URL('error','error404'))
    alias=alias.decode('utf-8').replace('_',' ')

    caso=db.caso(name=alias,is_active=True) or redirect('error','error404')
    response.view='visualizacion/caso_caso.html'
    return locals()
