__author__ = 'Evolutiva'


def index():
    active = request.vars['active']
    if len(request.vars)==0:
        active='person'

    return dict(active=active)


