__author__ = 'Evolutiva'

##id hereda hermanos (hijos de origenP)
def padres(origenP,id,isNew=True):
    response.flash=T('Padre inside ')
    listaHijos=db(
        ((db.relFamiliar.origenP==origenP) &(db.relFamiliar.parentesco==1))).select()
    r=0

    for detalle in listaHijos:
        pivot=detalle.destinoP
        if(detalle.destinoP==origenP):
            pivot=detalle.origenP
        if(isNew):
            r=db.relFamiliar.validate_and_insert(parentesco=3,origenP=pivot,destinoP=id)
            if r.errors: print origenP, r.errors


        else:


            result = db(
                ((db.relFamiliar.origenP==pivot) & (db.relFamiliar.destinoP==id) &(db.relFamiliar.parentesco==3)) |
                ((db.relFamiliar.destinoP==pivot) & (db.relFamiliar.origenP==id) &(db.relFamiliar.parentesco==3))
            ).select().first()
            if (result==None):
                r=db.relFamiliar.validate_and_insert(parentesco=3,origenP=pivot,destinoP=id)
                ##pivot hereda hermanos de id
                r=heredaHermanos(pivot, id,False)
                ##if r.errors: print origenP, r.errors

    db.commit()
    return r

##id hereda hermanos de hermanoID
def heredaHermanos(id,hermanoID,isNew=True):
    r=0
    listaHermanos=db( ((db.relFamiliar.origenP==hermanoID) &(db.relFamiliar.parentesco==3)) |
                      ((db.relFamiliar.destinoP==hermanoID) & (db.relFamiliar.parentesco==3))
        ).select()

    for detalle in listaHermanos:
        pivot=detalle.destinoP
        if(detalle.destinoP==hermanoID):
            pivot=detalle.origenP
        if(isNew):
            r=db.relFamiliar.validate_and_insert(parentesco=3,origenP=pivot,destinoP=id)
            if r.errors: print pivot, r.errors
        else:
            result = db(
                ((db.relFamiliar.origenP==pivot) & (db.relFamiliar==id) &(db.relFamiliar.parentesco==3)) |
                ((db.relFamiliar.destinoP==pivot) & (db.relFamiliar.origenP==id) &(db.relFamiliar.parentesco==3))
            ).select().first()
            if(result==None):
                r=db.relFamiliar.validate_and_insert(parentesco=3,origenP=pivot,destinoP=id)
                ##if r.errors: print origenP, r.errors

    return r


def OldBrothers(aBrother,bBrother):
    response.flash=T('Brothers inside ')

    r=0; sets=set()

    aBrotherListO=db((db.relFamiliar.origenP==aBrother) &(db.relFamiliar.parentesco==3)).select(db.relFamiliar.destinoP)
    aBrotherListD=db((db.relFamiliar.destinoP==aBrother) &(db.relFamiliar.parentesco==3)).select(db.relFamiliar.origenP)
    bBrotherListO=db((db.relFamiliar.origenP==bBrother) &(db.relFamiliar.parentesco==3)).select(db.relFamiliar.destinoP)
    bBrotherListD=db((db.relFamiliar.destinoP==bBrother) &(db.relFamiliar.parentesco==3)).select(db.relFamiliar.origenP)
    sets=createSet(aBrotherListO,bBrotherListO,'destinoP')

    setsD = createSet(bBrotherListD,bBrotherListD,'origenP')

    setsfinal = sets | setsD
    print setsfinal
    relacion= set()
    for detalle in setsfinal:
        pivot=detalle
        for destino in relacion:

            result = db(
                ((db.relFamiliar.origenP==pivot) & (db.relFamiliar.destinoP==destino) &(db.relFamiliar.parentesco==3)) |
                ((db.relFamiliar.destinoP==pivot) & (db.relFamiliar.origenP==destino) &(db.relFamiliar.parentesco==3))
            ).select().first()
        ##print result.origenP, result.destinoP
            if(result==None):
                r=db.relFamiliar.validate_and_insert(parentesco=3,origenP=pivot,destinoP=destino)
                ##if r.errors: print origenP, r.errors
                print pivot,destino, r
        relacion.add(pivot)
    db.commit()
    return r

def createSet(Rows1,Rows2,key):
    sets=set()
    for row in Rows1:
        p=row[key]
        sets.add(p)
    for row in Rows2:
        p=row[key]
        sets.add(p)
    return sets

