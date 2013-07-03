# -*- coding: utf-8 -*-
from gluon import DAL
from gluon import languages

class SetupPopulate(object):

    def __init__(self, db=None, request=None):
        self.db=db
        self.request=request
        msg=''
        if not (db(db.country.id>0).count()):
            file = open(request.folder+'/modules/setup/country.csv','r')
            db.country.import_from_csv_file(file)
            file.close()
            #msg += T('Loaded Country')
        if not (db(db.tipoOrganizacion.id>0).count()):
            file = open(request.folder+'/modules/setup/tipoorganizacion.csv','r')
            db.tipoOrganizacion.import_from_csv_file(file)
            file.close()
            #msg += T('Loaded Organization Types')
        if not (db(db.tipoParentesco.id>0).count()):
            file = open(request.folder+'/modules/setup/tipoparentesco.csv','r')
            db.tipoParentesco.import_from_csv_file(file)
            file.close()
            #msg += T('Loaded Relatives Conections')
        if not (db(db.tipoRelacionOrg2Org.id>0).count()):
            file = open(request.folder+'/modules/setup/tiporelacionorg2org.csv','r')
            db.tipoRelacionOrg2Org.import_from_csv_file(file)
            file.close()
            #msg += T('Loaded Organization conections')
        if not (db(db.tipoRelacionP20.id>0).count()):
            file = open(request.folder+'/modules/setup/tiporelacionp20.csv','r')
            db.tipoRelacionP20.import_from_csv_file(file)
            file.close()
            #msg += T('Loaded Person to Organization connections')
        if not (db(db.tipoRelacionP2P.id>0).count()):
            file = open(request.folder+'/modules/setup/tiporelacionp2p.csv','r')
            db.tipoRelacionP2P.import_from_csv_file(file)
            file.close()
        if not (db(db.sector.id>0).count()):
            file = open(request.folder+'/modules/setup/sector.csv','r')
            db.sector.import_from_csv_file(file)
            file.close()
            #msg += T('Loaded Main Sector')
        if not (db(db.auth_group.role=='super_administrator').count()):
            db.auth_group.validate_and_insert(
                role='super_administrator',
                description='super administrator for Poderopedia'
            )
        if not (db(db.auth_group.role=='administrator').count()):
            db.auth_group.validate_and_insert(
                role='administrator',
                description='administrator for Poderopedia'
            )

