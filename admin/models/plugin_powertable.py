# -*- coding: utf-8 -*-
###############################################################################
#    AUTHOR AND LICENSE
###############################################################################
# This is an ALPHA VERSION
# This uses code taken from web2py gluon/sqlhtml.py, plugin_datatable,plugin_webgrid 
#
# Web2py plugin powerTable ( Version ALPHA 0.1.1 : 2010-12-28 ) 
# Copyright (c) 2010 Rocha, Bruno Cezar
# @rochacbruno
# https://bitbucket.org/rochacbruno/powertable
# http://powertable.blouweb.com
#
# License Code: GPL, General Public License v. 2.0
# License Content: Creative Commons Attribution 3.0 
#
# Also visit: www.web2py.com 
#             or Groups: http://groups.google.com/group/web2py 
#                http://groups.google.com/group/web2py-usuarios  
#
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/
###############################################################################
###############################################################################
#    HOW TO : More info, tutorial and complete API in powertable.blouweb.com
###############################################################################
#def index():
#    #every method of this class is a function which returns a Virtual Field
#    class Virtual(object):
#        @virtualsettings(label=T('Information:'))
#        def virtualtooltip(self):
#            return T('This is a virtual tooltip for record %s' % self.person.id)
#
#    # Alias to the plugin object
#    mytable = plugins.powerTable
#    
#    mytable.datasource = db.auth_user
#    mytable.virtualfields = Virtual()
#    mytable.headers = 'fieldname:capitalize'
#    mytable.dtfeatures['bJQueryUI'] = True
#    mytable.uitheme = 'smoothness'
#    mytable.extra = dict(tooltip={'value':'vitualtooltip'})
#    mytable.dtfeatures['sPaginationType'] = 'scrolling'
#    # you can specify the columns, remove to show all
#    mytable.columns = ['auth_user.id','auth_user.first_name','auth_user.last_name','auth_user.email']
#    
#    return dict(table=mytable.create())
#
#################################################################################



###############################################################################
#    INITIALISATION
###############################################################################

import re
table_field = re.compile('[\w_]+\.[\w_]+')
from gluon.sql import  Row, Rows, Set, Query,Table

if not 'plugin_powertablesdb' in globals():
    if 'db' in globals():
        plugin_powertablesdb = db
    else:
        raise ReferenceError('You need to define either db or plugin_powertablesdb for PowerTables')


plugins = PluginManager('powerTable')
powerTable = plugins.powerTable


###############################################################################
#    MAIN CLASS, THE powerTable OBJECT
###############################################################################

class PowerTable(TABLE):
    
    def __init__(self):
        
        #load attributes from plugin manager
        datasource = powerTable.get('datasource',getfakerow())
        database = powerTable.get('database',plugin_powertablesdb)
        headers = powerTable.get('headers',{})
        columns = powerTable.get('columns',None)
        hiddencolumns = powerTable.get('hiddencolumns',[])
        orderby = powerTable.get('orderby',None)
        linkto = powerTable.get('linkto',None)
        upload = powerTable.get('upload',None)
        truncate = powerTable.get('truncate',32)
        th_link = powerTable.get('th_link','')
        virtualfields = powerTable.get('virtualfields',None)
        keycolumn = powerTable.get('keycolumn',None)
        showkeycolumn = powerTable.get('showkeycolumn',True)
        columnsearch = powerTable.get('columnsearch', False)
        #merge columns and hidden columns for select (after that we'll remove
        if columns: columns.extend(hiddencolumns)
         
        #By default insert the kwycolum as the first
        if columns and keycolumn: columns.insert(0,keycolumn)
       
        #check and get the sqlrows from datasource
        #TODO!!! parse list and dict as Json, open URL as ajax response
        if isinstance(datasource,Rows):
            sqlrows = datasource
        elif isinstance(datasource,Set):
            sqlrows = datasource.select(*columns) if columns else datasource.select()
        elif isinstance(datasource,(Query,Table)):
            if columns:
                cols = [col for col in columns if col.split('.')[0]!='virtual']
            sqlrows = database(datasource).select(*cols) if columns else database(datasource).select()
        elif isinstance(datasource, (type(dict()),type([]))):
            try:
                sqlrows = my_parser(datasource)
            except NotImplementedError:
                raise NotImplementedError(T('Cant serialize lists and dicts yet'))
        elif isinstance(datasource,XML):
            try:
                sqlrows = get_values_from_url(datasource)
            except NotImplementedError:
                raise NotImplementedError(T('Cant load server data yet'))
        elif isinstance(datasource,URL):
            try:
                sqlrows = get_values_from_url(datasource)
            except NotImplementedError:
                raise NotImplementedError(T('Cant load server data yet'))
        else:
            raise AttributeError(T("Invalid datasource for DATATABLES plugin"))
            
        #setting virtuallabels     
        if virtualfields:
            virtuallabels = powerTable.get('virtuallabels',{})
            virtuallabels['virtual.virtualtooltip'] = 'Virtual Tooltip'
            vfields = [i for i in dir(virtualfields) if not i.startswith('_')]
            for vf in vfields:
                sqlrows.colnames.append('virtual.%s' % vf)
                if not 'virtual.%s' % vf in virtuallabels:
                    try:
                        virtuallabels['virtual.%s' % vf] = getattr(virtualfields,vf).label
                    except AttributeError:
                        pass

            #appending virtual fields to the rows        
            sqlrows.setvirtualfields(virtual=virtualfields)
            
        #keycolumn is required, if not set, it will be the first column    
        if not keycolumn: keycolumn = sqlrows.colnames[0]
        keycolumntbl = keycolumn.split('.')[0]
        keycolumnfld = keycolumn.split('.')[-1] 
        
        #remove hiddencolumns from columns
        for hidden in hiddencolumns: columns.remove(hidden)
        
        #TABLE <table> object initialisation
        TABLE.__init__(self, powerTable)
        self.components = []
    
        #powerTable._class = powerTable._class+' display'
        self.attributes = powerTable
        self.sqlrows = sqlrows
        (components, row) = (self.components, [])
        if not columns:
            columns = sqlrows.colnames
            #remove undesired fields for hide
            if 'virtual.virtualtooltip' in columns:
                columns.remove('virtual.virtualtooltip')
        if headers=='fieldname:capitalize':
            headers = {}
            for c in columns:
                headers[c] = capitalizefieldname(c)
                ## ' '.join([w.capitalize() for w in c.split('.')[-1].split('_')])
        elif headers=='labels':
            headers = {}
            for c in columns:
                (t,f) = c.split('.')
                try:
                    headers[c] = sqlrows.db[t][f].label
                except (KeyError, AttributeError):
                    headers[c] = virtuallabels.get(c,capitalizefieldname(c))
                      
        if headers!=None:
            for c in columns:
                if orderby:
                    row.append(TH(A(headers.get(c, c),
                                    _href=th_link+'?orderby=' + c)))
                else:
                    row.append(TH(headers.get(c, c)))
            components.append(THEAD(TR(*row)))
        
        tbody = []
        for (rc, record) in enumerate(sqlrows):
            
            #setting the tooltip for rows
            #TODO!!! Set tooltip for cells
           
            if virtualfields:
                if 'virtualtooltip' in dir(virtualfields):
                
                    _title = DIV()
                    _title.append(H3(getattr(virtualfields,'virtualtooltip').label))
                    _title.append(SPAN(record.virtual.get('virtualtooltip',T('Record %s' % str(rc+1)))))
                else:
                    _title = T('Record %s' % str(rc+1))
            else:
                _title = T('Record %s' % str(rc+1))
                
            #setting the id and key for every <tr> based on required keycolumn    
            try:
                _id = record[keycolumntbl][keycolumnfld]
            except KeyError:
                if virtualfields:
                    _id = record[sqlrows.colnames[0].split('.')[0]].id
                else:
                    _id = record.id
            try:
                _key = '%s.%s.%s' % (keycolumntbl,keycolumnfld,str(record[keycolumntbl][keycolumnfld]))
            except Exception:
                if virtualfields:
                    _key = '%s.%s' % (sqlrows.colnames[0],record[sqlrows.colnames[0].split('.')[0]].id)
                else:
                    _key = '%s.%s' % (sqlrows.colnames[0],record.id)
            #dbg(_key)    
                                
            row = []
            if rc % 2 == 0:
                _class = 'even clickable'
            else:
                _class = 'odd clickable'
            for colname in columns:
                if not table_field.match(colname):
                    if "_extra" in record and colname in record._extra:
                        r = record._extra[colname]
                        row.append(TD(r))
                        continue
                    else:
                        raise KeyError("Column %s not found (powerTable)" % colname)
                (tablename, fieldname) = colname.split('.')
                try:
                    field = sqlrows.db[tablename][fieldname]
                except (KeyError, AttributeError):
                    field = None
                if tablename in record \
                        and isinstance(record,Row) \
                        and isinstance(record[tablename],Row):
                    r = record[tablename][fieldname]
                elif fieldname in record:
                    r = record[fieldname]
                else:
                    raise SyntaxError, 'something wrong in Rows object'
                r_old = r
                if not field:
                    pass
                elif linkto and field.type == 'id':
                    try:
                        href = linkto(r, 'table', tablename)
                    except TypeError:
                        href = '%s/%s/%s' % (linkto, tablename, r_old)
                    r = A(r, _href=href)
                elif linkto and field.type.startswith('reference'):
                    ref = field.type[10:]
                    try:
                        href = linkto(r, 'reference', ref)
                    except TypeError, e:
                        href = '%s/%s/%s' % (linkto, ref, r_old)
                        if ref.find('.') >= 0:
                            tref,fref = ref.split('.')
                            if hasattr(sqlrows.db[tref],'_primarykey'):
                                href = '%s/%s?%s' % (linkto, tref, urllib.urlencode({fref:ur}))
                    r = A(str(r), _href=str(href))
                elif linkto and hasattr(field._table,'_primarykey') and fieldname in field._table._primarykey:
                    # have to test this with multi-key tables
                    key = urllib.urlencode(dict( [ \
                                ((tablename in record \
                                      and isinstance(record, Row) \
                                      and isinstance(record[tablename], Row)) and
                                 (k, record[tablename][k])) or (k, record[k]) \
                                    for k in field._table._primarykey ] ))
                    r = A(r, _href='%s/%s?%s' % (linkto, tablename, key))
                elif field.represent:
                    r = field.represent(r)
                elif field.type == 'blob' and r:
                    r = 'DATA'
                elif field.type == 'upload':
                    if upload and r:
                        r = A('file', _href='%s/%s' % (upload, r))
                    elif r:
                        r = 'file'
                    else:
                        r = ''
                elif field.type in ['string','text']:
                    r = str(field.formatter(r))
                    ur = unicode(r, 'utf8')
                    if truncate!=None and len(ur) > truncate:
                        r = ur[:truncate - 3].encode('utf8') + '...'
                        
                try:
                    tdclass = colname+'.'+field.type
                except AttributeError:
                    #tdclass = colname+'None'
                    tdclass = colname+'.'+getattr(virtualfields,colname.split('.')[-1]).type
                row.append(TD(r,_class=tdclass))
                
                #dbg(tdclass)
                
  
            tbody.append(TR(_class=_class,_title=_title,_id=_id,_key=_key, *row))
        components.append(TBODY(*tbody))
        
        #footer
        
        if columnsearch:            
            row = [''] if 'details'in powerTable.extra else []
            for c in columns:
                row.append(TH(INPUT(_type='text',_value=T('Search in %s' % headers[c]),_class='search_init')))
            components.append(TFOOT(TR(*row)))
        #columnsearch


###############################################################################
#    SOME UTIL METHODS
###############################################################################
#Dummy virtualfields


#used when no datasource is defined
#TODO!! return JSON instead of Rows
def getfakerow():
    if request.env.web2py_runtime_gae:
        b = DAL('gae://powertable')  
    else:
        b = DAL('sqlite:memory:')
        
    b.define_table('fake',Field('nothing',label='Nothing Found'))
    b.fake.insert(nothing='You need to define a datasource')
    return b(b.fake).select(b.fake.nothing)

#decoretor for setting of virtual fields
#@virtualsettings(label=T('Label 2'),comment=T('my comment'), type='integer'
def virtualsettings(label='No Label',comment='',type='string'):
    def _(f):
        f.label=label
        f.comment=comment
        f.type=type
        return f
    return _

#get table.field_1 , return Field 1
def capitalizefieldname(c):
    return ' '.join([w.capitalize() for w in c.split('.')[-1].split('_')])

#include extra JS and CSS files
def plugin_datatable_include():
    response.files.append(URL(r=request,c='static',f='plugin_powertable/jquery.dataTables.min.js'))
    response.files.append(URL(r=request,c='static',f='plugin_powertable/jquery.dataTables.css'))
    
    extra = powerTable.get('extra',[])
    ui = powerTable.dtfeatures.get('bJQueryUI',True)
    theme = powerTable.get('uitheme','smoothness')
    if 'tooltip' in extra:
        response.files.append(URL(r=request,c='static',f='plugin_powertable/extra/jquery.tooltip.js'))
        response.files.append(URL(r=request,c='static',f='plugin_powertable/extra/jquery.tooltip.css'))
     
    if 'editable' in extra:
        response.files.append(URL(r=request,c='static',f='plugin_powertable/extra/jquery.jeditable.js'))
        
    if  powerTable.dtfeatures['sPaginationType'] == 'scrolling':
        response.files.append(URL(r=request,c='static',f='plugin_powertable/extra/scrolling.js'))
        
    if ui and not 'jquery-ui' in response.files:
        response.files.append(URL(r=request,c='static',f='plugin_powertable/ui/css/%s/jquery-ui-1.8.5.custom.css' % theme))
        response.files.append(URL(r=request,c='static',f='plugin_powertable/ui/js/jquery-ui-1.8.5.custom.min.js'))
  
#debugger  
def dbg(*attributes):
    print '----------\n'
    print attributes
    while not raw_input('\nPRESS TO CONTINUE\n'):
        break
###############################################################################
#    JS STRINGS
###############################################################################  

fnRowCallback = ''

xxx = """function( nRow, aData, iDisplayIndex ) {
if ( jQuery.inArray(aData[0], gaiSelected) != -1 ){
$(nRow).addClass('row_selected');
}
return nRow
;}"""
                        
                
###############################################################################
#    DEFAULT ATTRIBUTES
###############################################################################
powerTable._class = powerTable.get('_class','powerTable')
powerTable.columnsearch = powerTable.get('columnsearch', False)
powerTable.defaultlanguage =  {'sLengthMenu': str(T('Display _MENU_ entries')),
                        'sZeroRecords': str(T('Nothing found - sorry')),
                        'sInfo': str(T('Showing _START_ to _END_ of _TOTAL_ records')),
                        'sInfoEmpty': str(T('Showing 0 to 0 of 0 records')),
                        'sInfoFiltered': str(T('(filtered from _MAX_ total records)')),
                        "sInfoPostFix":  "",
                        "sProcessing":  str(T("Processing...")),
                        "sUrl":"",
                        "sSearch":str(T('Search:')),
                        "oPaginate": {"sFirst":str(T('First')),
                                      "sPrevious":str(T('Previous')),
                                      "sNext":str(T('Next')),
                                      "sLast":str(T('Last'))}
                        }


#Initialisation keys
powerTable.dtfeatures = {}
powerTable.dtfeatures['bJQueryUI'] = powerTable.dtfeatures.get('bJQueryUI',True)
powerTable.dtfeatures['bProcessing'] = powerTable.dtfeatures.get('bProcessing',True)
powerTable.dtfeatures['bServerSide'] = powerTable.dtfeatures.get('bServerSide',False)

lengthmenu = [[2, 5, 10,25, 50, 100, -1],[2, 5, 10, 25, 50, 100,str(T("All"))]]
powerTable.dtfeatures['aLengthMenu'] = powerTable.dtfeatures.get('aLengthMenu',lengthmenu)
powerTable.dtfeatures['oLanguage'] = powerTable.dtfeatures.get('oLanguage', powerTable.defaultlanguage)
powerTable.dtfeatures['bPaginate'] = powerTable.dtfeatures.get('bPaginate', 'true')
powerTable.dtfeatures['sPaginationType'] = powerTable.dtfeatures.get('sPaginationType', 'full_numbers') # two_button | scrolling
powerTable.dtfeatures['fnRowCallback'] = powerTable.dtfeatures.get('fnRowCallback', fnRowCallback)
powerTable.dtfeatures['fnDrawCallback'] = powerTable.dtfeatures.get('fnDrawCallback', '')


powerTable.dtfeatures['bSortClasses'] = powerTable.dtfeatures.get('bSortClasses', 'false')
powerTable.dtfeatures['sScrollY'] = powerTable.dtfeatures.get('sScrollY','300px')
powerTable.dtfeatures['sScrollX'] = powerTable.dtfeatures.get('sScrollX','100%')
##OPTIONAL##
#dtfeatures['bRetrieve'] = 'true'
#"bStateSave": true
#"sScrollY": "100%",
#"bScrollCollapse": true,
#powerTable['selectrow'] = False
#iCookieDuration:400
#"sScrollXInner": "110%",
# Extra JS Features
powerTable.extra = powerTable.get('extra',{})

powerTable.extra.get('editable',{})['editablecallback'] = powerTable.extra.get('editable',{}).get('editablecallback','../plugin_powertable/editable.load') 

powerTable.extra.get('details',{})['detailscallback'] = powerTable.extra.get('details',{}).get('detailscallback','../plugin_powertable/details')
powerTable.extra.get('details',{})['detailscolumns'] = powerTable.extra.get('details',{}).get('detailscolumns','')

###############################################################################
#    THE powerTable CREATOR FUNCTION
###############################################################################
#the plugin call method, renamed to powerTable.create() at the end
def plugin_powertable():
    #reload  values
    _class = powerTable.get('_class','powerTable')
    dtfeatures = powerTable.get('dtfeatures',{})
    extra = powerTable['extra'] = powerTable.get('extra',{})
    editablecallback = extra.get('editable',{}).get('editablecallback',URL('plugin_powertable','editable.load')) 
    detailscallback = extra.get('details',{}).get('detailscallback',URL('plugin_powertable','details'))
    detailscolumns = extra.get('details',{}).get('detailscolumns','')
    selectrow = powerTable.get('selectrow',True)
    ifunctions = powerTable.get('ifunctions','')
    powerTable.dtfeatures['sPaginationType'] = powerTable.dtfeatures.get('sPaginationType', 'full_numbers')
    powerTable.dtfeatures['bJQueryUI'] = powerTable.dtfeatures.get('bJQueryUI',True)
    
    powerTable.dtfeatures['sScrollY'] = powerTable.dtfeatures.get('sScrollY','300px')
    powerTable.dtfeatures['sScrollX'] = powerTable.dtfeatures.get('sScrollX','100%')
    

    
    
    if 'tooltip' in extra:
        tooltipjs = """$('.%s tbody tr[title]').tooltip( {
                    "delay": 0,"track": true,"fade": 250} );""" % _class
    else:
        tooltipjs = '/*no tooltip*/'
        
        
    if 'editable' in extra:
        editablejs = """/* Apply the jEditable handlers to the table */
				$('td', oTable.fnGetNodes()).editable( '%(editablecallback)s', {
                                        indicator:'Saving',
                                        tooltip:'click to edit',
					"callback": function( sValue, y ) {
						var aPos = oTable.fnGetPosition( this );
						oTable.fnUpdate( sValue, aPos[0], aPos[1] );
					},
					"submitdata": function ( value, settings ) {
						return {
							"row_id": this.parentNode.getAttribute('id'),
							"column": oTable.fnGetPosition( this )[2]
						};
					},
					"height": "20px"
				} );
                    /* Apply the jEditable handlers to the table */
                    """ % dict(editablecallback=editablecallback)
    else:
        editablejs = '/*not editable*/'
        
    #TODO: things here    
        
    if 'details' in extra:    
        detailsimagebutton = """
             /*
	 * Insert a 'details' column to the table
	 */
	var nCloneTh = document.createElement( 'th' );
	var nCloneTd = document.createElement( 'td' );
	nCloneTd.innerHTML = '<img src="%(imageurl)s" alt="Click to see details" title="Click for details" style="cursor:pointer;">';
	nCloneTd.className = "dtclick center";
	
        $('.%(_class)s tfoot tr').each( function () {
		this.insertBefore( nCloneTh, this.childNodes[1] );
	} );
        
	$('.%(_class)s thead tr').each( function () {
		this.insertBefore( nCloneTh, this.childNodes[1] );
	} );
        
	$('.%(_class)s tbody tr').each( function () {
		this.insertBefore(  nCloneTd.cloneNode( true ), this.childNodes[1] );
	} );
        
      
                   
                   
                   /*insert detail column image*/
        """ % dict(_class=_class,
		   imageurl=URL('static','plugin_powertable/images/details_open.png'),
                  )
        
        
        
          
        detailsclick = """
    /*click on image to show details*/
                    
                    $('.%(_class)s tbody td.dtclick img').live( 'click', function () {
					var nTr = this.parentNode.parentNode;
                                        var rid = this.parentNode.parentNode.getAttribute('id');
                                        var key = this.parentNode.parentNode.getAttribute('key');
                                        //alert(this.parentNode.parentNode.getAttribute('key'));
					if ( this.src.match('details_close') )
					{
						/* This row is already open - close it */
						this.src = "%(openurl)s";
                                                this.title = "Click for details";
                                                this.alt =  "Open Details";
						oTable.fnClose( nTr );
					}
					else
					{
						/* Open this row */
						this.src = "%(closeurl)s";
                                                this.title = "Click to close details";
                                                this.alt =  "Close Details";
						oTable.fnOpen( nTr, fnFormatDetails(oTable,nTr,key,rid), 'details' );
                                                ajax('%(detailscallback)s', ['dt_'+rid,'dtcols_'+rid], 'target'+rid+'div');
					}
				} );
                                
                                
                    
                    
                    /*click on image to show details*/
                    """ % dict(_class=_class,
                                detailscallback=detailscallback,
                               openurl=URL('static','plugin_powertable/images/details_open.png'),
                               closeurl=URL('static','plugin_powertable/images/details_close.png'),
                               )
                    
        formatdetails = """
         /*function to format details*/	
			/* Formating function for row details */
			function fnFormatDetails ( oTable, nTr,key,rid )
			{
				var aData = oTable.fnGetData( nTr );
                                var sOut = '<form><input type="hidden" value='+key+ ' id=dt_'+rid+' name=dt_'+rid+' />'
                                sOut += '<input type="hidden" value="%(detailscolumns)s" id=dtcols_'+rid+' name=dtcols_'+rid+' /></form>'
                                sOut += '<div class="datatabledetail" id="target'+rid+'div"></div>'
				
				return sOut;
			}
    
    
                   /*function to format details*/
                   """ % dict(detailscolumns=detailscolumns)
    else:
        detailsimagebutton = '/*No details table*/'
        detailsclick = '/*No details table*/'
        formatdetails = '/*No format details*/'
    
    if 'columnhighlight' in extra:
        highlight = """
                        /*highlight*/
        
        $('td', oTable.fnGetNodes()).hover( function() {
                                        //alert(oTable.fnSettings().aoColumns.length - hidekeycolumn)
					var iCol = $('td').index( this ) % oTable.fnSettings().aoColumns.length - hidekeycolumn;
					var nTrs = oTable.fnGetNodes();
					$('td:nth-child('+(iCol+1)+')', nTrs).addClass( 'highlighted' );
				}, function() {
					$('td.highlighted', oTable.fnGetNodes()).removeClass('highlighted');
				} );
        
        
        /*highlight*/
        """
    else:
        highlight = '/*No highlight*/'
        
        
    if selectrow:    
        rowclick = """
                 /* Click on row event handler */
	$('.%(_class)s tbody tr.clickable').live('click', function () {
		var aData = oTable.fnGetData( this );
		var iId = aData[0];
		
		if ( jQuery.inArray(iId, gaiSelected) == -1 )
		{
			gaiSelected[gaiSelected.length++] = iId;
                        //alert(gaiSelected)
		}
		else
		{
			gaiSelected = jQuery.grep(gaiSelected, function(value) {
				return value != iId;
			} );
                        //alert(gaiSelected)
		}
		
		$(this).toggleClass('row_selected');
	} );
        /*Click on row event handler*/
        """ % dict(_class=_class)
    else:
        rowclick = '/*norowclick*/'
        
    if 'autoresize' in extra:
        autoresize = """
          /*adjust columns */
    if ($.browser.msie){}else{  
        $(window).bind('resize', function () {
            oTable.fnAdjustColumnSizing();
	} );
        
     }   """
    else:
        autoresize = ''
    
    
    if powerTable.columnsearch:
        index  = 1 if 'details' in extra else 0
        index = -1 if powerTable.showkeycolumn else index
        indexs = index if 'details' in extra else 1
        indexs = 0 if powerTable.showkeycolumn else indexs
        print index
        print indexs
        searchcolumnjs = """
        $("tfoot input").keyup( function () {
					/* Filter on the column (the index) of this element */
					oTable.fnFilter( this.value, $("tfoot input").index(this) + %(index)s + 1);
                                        //alert($("tfoot input").index(this))
				} );
				
				
				
				/*
				 * Support functions to provide a little bit of 'user friendlyness' to the textboxes in 
				 * the footer
				 */
				$("tfoot input").each( function (i) {
					asInitVals[i] = this.value;
				} );
				
				$("tfoot input").focus( function () {
					if ( this.className == "search_init" )
					{
						this.className = "";
						this.value = "";
					}
				} );
				
				$("tfoot input").blur( function (i) {
					if ( this.value == "" )
					{
						this.className = "search_init";
						this.value = asInitVals[$("tfoot input").index(this) + %(indexs)s];
					}
				} );
        
        
        """ % dict(index=index,indexs=indexs)
    else:
        searchcolumnjs = ''
    
    
    jquery = """
                  
                  var oTable;
                  var gaiSelected =  [];
                  var asInitVals = new Array();
		   %(formatdetails)s
                   jQuery(document).ready(function() {
                    %(detailsimagebutton)s
                    %(tooltipjs)s
                    var oTable = jQuery('.%(_class)s').dataTable(
                                                             
                                                             %(dtfeatures)s
                                                             
                                                             );
                    %(searchcolumnjs)s
                    %(editablejs)s
                    %(hidekeycolumnjs)s
                    %(highlight)s
                    %(detailsclick)s
                    %(rowclick)s
                    %(autoresize)s
                   
   });
    %(ifunctions)s
    
    function getTarget(e){  
            if(e.srcElement)  
               return e.srcElement;  
            else  
               return e.target;  
         }  
   """
                    
    showkeycolumn = powerTable.get('showkeycolumn',True)
    if not showkeycolumn:
        hidekeycolumnjs = "var hidekeycolumn = 200;oTable.fnSetColumnVis(0,false);oTable.fnDraw();"
    else:
        hidekeycolumnjs = 'var hidekeycolumn = 0'
    
    plugin_datatable_include()
    CSS = ''
    CSS = TAG.STYLE(
        """
        .%(_class)s tbody tr.even:hover, .%(_class)s  tbody tr.even td.highlighted {
        background-color: #ccc !important;
        }
        
        .%(_class)s tbody tr.odd:hover, .%(_class)s  tbody tr.odd td.highlighted {
                background-color: #ccc;
        }
        
        
        
        .%(_class)s tr.even:hover {
                background-color: #ECFFB3;
        }
        
        .%(_class)s th {
                
                white-space:nowrap;
        }
        
        .%(_class)s tr.row_selected  {
                background-color: #d5effc;
        }
        
        .dataTables_wrapper{}
        
        .dataTables_length select{
            
            margin:0;
            width: 60px;      
            border:none;        
            
        }
        .dataTables_filter input{
             margin:0;
             width: 150px;
             border:none;
        }
        .DataTables_sort_wrapper{position:relative;padding-right: 20px;}
        .dataTables_wrapper .ui-state-default{line-height:20px;}
        .dataTables_wrapper .ui-icon{cursor: pointer;}
        .dataTables_wrapper .ui-button, .dataTables_paginate,.dataTables_info,.%(_class)s thead {line-height: 100%%;}
        .dataTables_processing{top:50%%;background-color: #FFFEF3;color:#000;}
        .dataTables_wrapper .css_right {float: right;}
        """ % dict(_class=_class)
        
    )
    
    return TAG[''](SCRIPT(
                          jquery % dict(_class=_class,
                                        dtfeatures=str(dtfeatures).\
                                            replace("'false'","false").\
                                            replace("'true'","true").\
                                            replace('True','true').\
                                            replace('False','false').\
                                            replace('"function','function').\
                                            replace(');}}"',');}}'),
                                        tooltipjs=str(tooltipjs),
                                        editablejs=str(editablejs),
                                        detailsimagebutton=str(detailsimagebutton),
                                        hidekeycolumnjs=str(hidekeycolumnjs),
                                        detailsclick=str(detailsclick),
                                        formatdetails=str(formatdetails),
                                        highlight=str(highlight),
                                        rowclick=str(rowclick),
                                        autoresize=str(autoresize),
                                        ifunctions=str(ifunctions),
                                        searchcolumnjs=str(searchcolumnjs)
                                        )
                        ),
                    CSS,
                    PowerTable(),
                    )


plugins.powerTable.create = plugin_powertable


def plugin_powerTable(datasource=None,attrs={},features={},extra={}):
    tbl = plugins.powerTable
    tbl.datasource = datasource
    tbl.dtfeatures = features
    tbl.extra = extra
    for k in attrs: tbl[k] = attrs[k]
    return tbl.create()
