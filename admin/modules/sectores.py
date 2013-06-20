__author__ = 'Evolutiva'

from gluon.globals import current
def grupo_sectores():
    db = current.db
    grupo={}
    orderby=db.sector.name
    groups = db(db.sector.parent==0).select(orderby=orderby)
    for group in groups:
        options = db(db.sector.parent==group.id).select(db.sector.name,db.sector.id,orderby=orderby)
        opcion ={}
        for item in options:
            opcion[item.name]=item.id
        grupo[group.name] = opcion

    return grupo

