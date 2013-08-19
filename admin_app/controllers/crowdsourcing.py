__author__ = 'Evolutiva'

def suggest_connection():
    query=db.sugerirConexion.is_active==True
    grid=SQLFORM.grid(query,orderby=db.sugerirConexion.estado)
    return dict(grid=grid)

def have_info():
    query=db.tengoDato
    grid=SQLFORM.grid(query,orderby=db.tengoDato.estado)
    return dict(grid=grid)

def suggest_person():
    query=db.sugerirPersona.is_active==True
    grid=SQLFORM.grid(query,orderby=db.sugerirPersona.estado)
    return dict(grid=grid)

def have_error():
    query=db.tipoerror.is_active==True
    grid=SQLFORM.grid(query,orderby=db.tipoerror.estado)
    return dict(grid=grid)

def inappropiate_content():
    query=db.tipoinadecuado.is_active==True
    grid=SQLFORM.grid(query,orderby=db.tipoinadecuado.estado)
    return dict(grid=grid)

def share():
    query=db.compartir
    grid=SQLFORM.grid(query,orderby=~db.compartir.fecha)
    return dict(grid=grid)

def notification():
    query=db.notificaciones.is_active==True
    grid=SQLFORM.grid(query,orderby=db.notificaciones.estado)
    return dict(grid=grid)