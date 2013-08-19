from mercurial import hgweb

def index():
    """ Controller to wrap hgweb

    You can access this endpoint either from a browser in which case the
    hgweb interface is displayed or from the mercurial client.

    hg clone http://localhost:8000/app/plugin_mercurial/index app
    """

    # HACK - hgweb expects the wsgi version to be reported in a tuple
    wsgi_version = request.wsgi.environ['wsgi.version']
    request.wsgi.environ['wsgi.version'] = (wsgi_version, 0)

    # map this controller's URL to the repository location and instantiate app
    config = {URL():'applications/'+request.application}
    wsgi_app = hgweb.hgwebdir(config)

    # invoke wsgi app and return results via web2py API
    # http://web2py.com/book/default/chapter/04#WSGI
    items = wsgi_app(request.wsgi.environ, request.wsgi.start_response)
    for item in items:
        response.write(item, escape=False)
    return response.body.getvalue()
