# -*- coding: utf-8 -*-
"""
@author: Bruno Cezar Rocha 
@titter: @rochacbruno
@company: blouweb.com
@depends: http://www.wbotelhos.com/gridy/ - Jquery Gridy Plugin
@include: http://nyromodal.nyrodev.com/ - nyroModal
@include: http://css3buttons.michaelhenriksen.dk/ - CSS3 Buttons
@depends: http://www.web2py.com - web2py Faster, Better and more easily web development! 

@license for Gridy library and PowerGrid Plugin
The MIT License

Copyright (c) 2010 Washington Botelho dos Santos (jquery.gridy)
Copyright (c) 2011 Bruno Cezar Rocha (PowerGrid Plugin for web2py)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

@DONATE! PayPal - rochacbruno@gmail.com

Go VEGAN!
"""
from gluon import *

from gluon.dal import Table ,Query, Set, Rows, Row
class CallBack(dict):
    def __init__(self, datasource, params=None, virtualfields=[]):
        
        if not params:
            params = current.request.vars

        assert params 

        
        # GET PARAMS
        page = int(params.get('page', 1))
        rows = int(params.get('rows', 5))
        key = params.get('search', None)
        find = params.get('find', None)
        sortName = params.get('sortName', None)
        sortOrder = params.get('sortOrder', 'asc')
        searchBy = params.get('searchBy','like') #like, equal, notequal, startswith, endswith, gt, lt, ge, le
        
        # DEFINE PAGINATION
        start = (rows * page) - rows
        end = start + rows
        #limiter
        limiter = (start, end)
        
        assert isinstance(datasource, (Table, Query))

        # IF TABLE
        if isinstance(datasource, Table):
            for v in virtualfields:
                datasource.virtualfields.append(v)

            if not (key and find):
                query = datasource
            else:
                try:
                    if searchBy == 'like':
                        query = datasource[find].like("%"+key+"%")
                    elif searchBy == 'equal':
                        query = datasource[find] == key
                    elif searchBy == 'notequal':
                        query = datasource[find] != key
                    elif searchBy == 'startswith':
                        query = datasource[find].like(key+"%")
                    elif searchBy == 'endswith':
                        query = datasource[find].like("%"+key)
                except:
                    query = datasource['id'].like("%"+key+"%")
            
            #counter
            recordscount = datasource._db(query).count()


            #SORTING
            sorter = None
            try:
                if (sortName and (sortOrder == 'asc')):
                    sorter = datasource[sortName]
                elif (sortName and (sortOrder == 'desc')):
                    sorter = ~datasource[sortName]
            except:
                pass

            # FETCHING
            recordset = datasource._db(query)
        
        
        # IF QUERY
        elif isinstance(datasource, Query):
            for v in virtualfields:
                datasource.first.table.virtualfields.append(v)

            if not (key and find):
                query = datasource
            else:
                if len(find.split('.')) == 1:
                    try:
                        if searchBy == 'like':
                            query = datasource.first.table[find].like("%"+key+"%")
                        elif searchBy == 'equal':
                            query = datasource.first.table[find] == key
                        elif searchBy == 'notequal':
                            query = datasource.first.table[find] != key
                        elif searchBy == 'startswith':
                            query = datasource.first.table[find].like(key+"%")
                        elif searchBy == 'endswith':
                            query = datasource.first.table[find].like("%"+key)
                    except:
                        query = datasource.first.table['id'].like("%"+key+"%")
                else:
                    try:
                        tablename = find.split('.')[0]
                        field = find.split('.')[1]
                        #ds.db(ds&ds.db.auth_user.first_name.like('%jon%'))
                        if searchBy == 'like':
                            query = datasource&datasource.db[tablename][field].like("%"+key+"%")
                        elif searchBy == 'equal':
                            query = datasource&datasource.db[tablename][field] == key
                        elif searchBy == 'notequal':
                            query = datasource&datasource.db[tablename][field] != key
                        elif searchBy == 'startswith':
                            query = datasource&datasource.db[tablename][field].like(key+"%")
                        elif searchBy == 'endswith':
                            query = datasource&datasource.db[tablename][field].like("%"+key)
                    except:
                        query = datasource&datasource.db[tablename]['id'].like("%"+key+"%")
            
            #counter
            recordscount = datasource.db(query).count()


            #SORTING
            sorter = None
            try:
                if (sortName and (sortOrder == 'asc')):
                    if len(sortName.split('.')) == 1:
                        sorter = datasource.first.table[sortName]
                    else:
                        tablename = sortName.split('.')[0]
                        field = sortName.split('.')[1]
                        sorter = datasource.db[tablename][field]
                elif (sortName and (sortOrder == 'desc')):
                    if len(sortName.split('.')) == 1:
                        sorter = ~datasource.first.table[sortName]
                    else:
                        tablename = sortName.split('.')[0]
                        field = sortName.split('.')[1]
                        sorter = ~datasource.db[tablename][field]
            except:
                pass

            # FETCHING
            recordset = datasource.db(query)        


        
        records = recordset.select(limitby=limiter, 
                                    orderby=sorter)
        
        
        # RETURN OBJECT
        self['entityList'] = []
        self['total'] = recordscount
        self['headers'] = []
        
        # Building the headers
        if isinstance(datasource, Query):
            for field in datasource.first.table.fields:
                self['headers'].append([field,field])

            


        if isinstance(datasource, Table):
            fields = datasource.fields

        #for r in records:
        #    if callable(r):
        #        self['entityList'].append(r.as_dict())

        for record in records:
            #TODO: REPRESENT OF FIELDS
            # records_dict = {}
            # if callable(record):
            #     for r in record:
            #         if isinstance(datasource, Query):
            #             if callable(datasource.first.table[r].represent):
            #                 print '___'#,datasource.first.table[r].represent
            #             else:
            #                 print '###',r,record(r)
            if callable(record):
                #if isinstance(record, Row):
                if not record.has_key('id'):
                    newrecord = {}
                    for r in record:
                        prefix = str(r)
                        newr = {}
                        for x,v in record[r].items():
                            if not callable(v):
                                newr["_".join([prefix,x])] = v
                        newrecord.update(newr)
                    self['entityList'].append(newrecord)
                else:
                    self['entityList'].append(record.as_dict())
                    

