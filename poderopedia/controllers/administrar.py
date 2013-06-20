# coding: utf8

def index(): return dict(message="hello from administrar.py")

@auth.requires_login()
def mispublicaciones_tab_abierto_grillaaz():
    return dict(_id=1,page=0, sort=0, target=0, entity=0)

def mispublicaciones_tab_abierto_grillaporfecha():
    return dict(_id=1,page=0, sort=0, target=0, entity=0)

def mispublicaciones_tab_abierto_listaaz():
    return dict(_id=1,page=0, sort=0, target=0, entity=0)

def mispublicaciones_todo():
    return dict(_id=1,page=0, sort=0, target=0, entity=0)
