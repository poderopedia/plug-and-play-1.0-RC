__author__ = 'Evolutiva'

def sugerirConexion():
    query=db.sugerirConexion.is_active==True
    grid=SQLFORM.grid(query,orderby=db.sugerirConexion.estado)
    return dict(grid=grid)

def tengoDato():
    query=db.tengoDato
    grid=SQLFORM.grid(query,orderby=db.tengoDato.estado)
    return dict(grid=grid)

def sugerirPersona():
    query=db.sugerirPersona.is_active==True
    grid=SQLFORM.grid(query,orderby=db.sugerirPersona.estado)
    return dict(grid=grid)

def tipoerror():
    query=db.tipoerror.is_active==True
    grid=SQLFORM.grid(query,orderby=db.tipoerror.estado)
    return dict(grid=grid)

def tipoinadecuado():
    query=db.tipoinadecuado.is_active==True
    grid=SQLFORM.grid(query,orderby=db.tipoinadecuado.estado)
    return dict(grid=grid)

def compartir():
    query=db.compartir
    grid=SQLFORM.grid(query,orderby=~db.compartir.fecha)
    return dict(grid=grid)

def notificaciones():
    query=db.notificaciones.is_active==True
    grid=SQLFORM.grid(query,orderby=db.notificaciones.estado)
    return dict(grid=grid)