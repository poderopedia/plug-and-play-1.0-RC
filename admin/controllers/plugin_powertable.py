# -*- coding: utf-8 -*- 

#########################################################################
## This is a samples controller
#########################################################################

def editable():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    return dict(message=T('This Field was edited'))
    
def details():
    key = None
    cols = None
    for k in request.vars.keys():
        if k[:3] == 'dt_':
            key = request.vars[k]
        elif k[:6] == 'dtcols':
            cols = request.vars[k]
    
    tablename = key.split('.')[0]
    fieldname = key.split('.')[1]
    value = key.split('.')[2]
    
    
    if cols:
        cols = cols.split(',')
        ftablename = cols[0].split('.')[0]
        if ftablename != tablename:
            row = plugin_powertablesdb(plugin_powertablesdb[ftablename][tablename]==value).select(*cols)
        else:
            row = plugin_powertablesdb(plugin_powertablesdb[tablename][fieldname]==value).select(*cols)
    else:
        row = plugin_powertablesdb(plugin_powertablesdb[tablename][fieldname]==value).select()
        
    tbl = SQLTABLE(row,headers='labels',truncate=32,linkto='show')
    
    #dbg(key,tablename,fieldname,plugin_powertablesdb._lastsql)
    return tbl