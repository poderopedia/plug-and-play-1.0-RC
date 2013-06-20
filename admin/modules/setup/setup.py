from gluon import DAL

def populate_db():
    if not (db(db.country.id>0).count()):
        file = open(request.folder+'/modules/setup/country.csv','r')
        db.country.import_from_csv_file(file)
        file.close()
    if not (db(db.tipoOrganizacion.id>0).count()):
        file = open(request.folder+'/modules/setup/tipoorganizacion.csv','r')
        db.tipoOrganizacion.import_from_csv_file(file)
        file.close()
    if not (db(db.tipoParentesco.id>0).count()):
        file = open(request.folder+'/modules/setup/tipoparentesco.csv','r')
        db.tipoParentesco.import_from_csv_file(file)
        file.close()
    if not (db(db.tipoRelacionOrg2Org.id>0).count()):
        file = open(request.folder+'/modules/setup/tiporelacionorg2org.csv','r')
        db.tipoRelacionOrg2Org.import_from_csv_file(file)
        file.close()
    if not (db(db.tipoRelacionP20.id>0).count()):
        file = open(request.folder+'/modules/setup/tiporelacionp20.csv','r')
        db.tipoRelacionP20.import_from_csv_file(file)
        file.close()
    if not (db(db.tipoRelacionP2P.id>0).count()):
        file = open(request.folder+'/modules/setup/tiporelacionp2p.csv','r')
        db.tipoRelacionP2P.import_from_csv_file(file)
        file.close()
