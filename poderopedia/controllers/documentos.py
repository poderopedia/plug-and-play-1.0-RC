__author__ = 'Evolutiva'

def index():
    url =request.env.http_host + request.env.request_uri
    dc_id=request.args(0)
    return dict(dc_id=dc_id, url=url)
