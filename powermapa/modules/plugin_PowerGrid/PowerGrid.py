# -*- coding: utf-8 -*-
"""
PowerGrid
@Version Beta 0.1 - 22/07/2011
@author: Bruno Cezar Rocha 
@titter: @rochacbruno
@company: blouweb.com
@depends: http://www.wbotelhos.com/gridy/ - Jquery Gridy Plugin
@include: http://nyromodal.nyrodev.com/ - nyroModal
@include: http://css3buttons.michaelhenriksen.dk/ - CSS3 Buttons
@depends: http://www.web2py.com - web2py Faster, Better and more easily web development! 

@license for Gridy library and PowerGrid Plugin
The MIT License

Copyright (c) 2011 Washington Botelho dos Santos (jquery.gridy)
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


#TODO:
- EXPORT TO EXCEL / PDF
- SELECT FIELDS IN CALLBACK
- POST TEMPLATE
- SCROLLING
- SEARCH ALL
- USE LABELS
- USE RECORD REPRESENTATION
"""
from gluon import *

__all__ = ['PowerGrid','PowerScript']


class PowerScript(DIV):

    tag = 'script'

    def xml(self):
        (fa, co) = self._xml()
        # no escaping of subcomponents
        co = '\n'.join([str(component) for component in
                        self.components])
        if co:           
            return '<%s%s>%s</%s>' % (self.tag, fa, co, self.tag)

        else:
            return DIV.xml(self)


class PowerGrid(DIV):
    
    tag = 'div'

    def __init__(self,
                 *components, 
                 **attributes):
        T = current.T
        #define the id if not passed
        if not '_id' in attributes:
            attributes['_id'] = "powergrid-wrapper" 
        
        if not 'template' in attributes:
            attributes['template'] = 'grid'

        if not 'searchBy' in attributes:
          attributes['searchBy'] = 'like'

        if not 'target' in attributes:
            attributes['target'] = 'powergrid'
        
        if not 'as_html' in attributes:
            attributes['as_html'] = True
        
        if not 'callback' in attributes:
            raise Exception("Callback is not defined")
        else:
            if not 'headers' in attributes:
                attributes['headers'] = self.get_headers(attributes['callback'])

        self.components = list(components)
        #self.components.append(DIV(_id="find-target"))
        self.components.append(DIV(_id=attributes['target']))
        #self.components.append("aaa")
            
        DIV.__init__(self,
                     *self.components,  
                     **attributes)

        from gluon.storage import Storage
        self.attributes = Storage(attributes)
        if not 'options' in self.attributes:
            self.attributes.options = {}                     
        
        #TODO: AUTO-SCROLL
        #if len(self.attributes.get('headers',[])) >= 5:
        #  self.attributes.options['scroll'] = True
        #  self.attributes.options['height'] = 300
        #  self.attributes.options['width'] = 900

        self.append_js()
      
    def get_headers(self, url):
      from urllib2 import urlopen
      
      if 'http' in url:
          u = urlopen(url).read()
      else:
          u = urlopen('http://'+current.request.env.http_host+url+"?page=1&rows=1").read()
      null = None
      d = eval(u)
      try:
          return d['headers']
      except:
          return [['noheaders','noheaders']]


    def append_js(self):
        current.response.files.append(URL('static','plugin_PowerGrid',args=['css','jquery.gridy.css']))
        current.response.files.append(URL('static','plugin_PowerGrid',args=['buttons','stylesheets','css3buttons.css']))
        current.response.files.append(URL('static','plugin_PowerGrid',args=['modal','styles','nyroModal.css']))
        current.response.files.append(URL('static','plugin_PowerGrid',args=['js','jquery.tmpl.min.js']))
        current.response.files.append(URL('static','plugin_PowerGrid',args=['js','jquery.gridy.min.js']))
        current.response.files.append(URL('static','plugin_PowerGrid',args=['modal','js','jquery.nyroModal.custom.min.js']))
        current.response.files.append(URL('static','plugin_PowerGrid',args=['modal','js','initmodal.js']))
        if 'ie6' in self.attributes:
            current.response.files.append(URL('static','plugin_PowerGrid',args=['modal','js','jquery.nyroModal-ie6.min.js']))


        template = self.power_template(template=self.attributes['template'])

        T = current.T
        
        params = self.attributes.options.get('params','')
        params += '&searchBy=%s' % self.attributes.get('searchBy','like')

        lenheaders = len(self.attributes.get('headers',[]))
        lenbuttons = len(self.attributes.get('buttons',[]))
        colswidth = [(self.attributes.options.get('width', 900)+(lenbuttons*100)) / (lenheaders + lenbuttons) for head in self.attributes.get('headers',[])]

        # CONTROL BUTTONS

        if not 'hidecontrolbuttons' in self.attributes:
            self.attributes['hidecontrolbuttons'] = False
        if not self.attributes['hidecontrolbuttons']:
            if not 'hideaddbutton' in self.attributes:
                self.attributes['hideaddbutton'] = False
            if not self.attributes['hideaddbutton']:
                if not 'addurl' in self.attributes:
                    self.attributes['addurl'] = '#'
                
                if not 'addLabel' in self.attributes:
                    self.attributes['addLabel'] = 'Add New Record'

                if not 'addTitle' in self.attributes:
                    self.attributes['addTitle'] = self.attributes['addLabel']

                self.attributes.addbutton = """<a id=%(target)s_addbutton target=_blank class=button href=%(addurl)s>
                                                  %(addLabel)s</a>""" % self.attributes
            else:
                 self.attributes.addbutton = ''
                 self.attributes['addTitle'] = ''
                                                  

            if not 'hiderefreshbutton' in self.attributes:
                self.attributes['hiderefreshbutton'] = False
            if not self.attributes['hiderefreshbutton']:
                if not 'refreshLabel' in self.attributes:
                    self.attributes['refreshLabel'] = 'Refresh'

                self.attributes.refreshbutton = """<a id=%(target)s_refreshbutton class=button href=# >
                                                 %(refreshLabel)s</a>""" % self.attributes
            else:
                self.attributes.refreshbutton = ''

            
            self.attributes['controlbuttons'] = '''<span id=%(target)s_controlbuttons>
                                                        %(addbutton)s
                                                        %(refreshbutton)s
                                                    </span>
                                                 ''' % self.attributes
        

            # add controlbuttons?
            self.attributes.addcontrolbuttons = """
            $('#%(target)s_controlbuttons').remove();
            $('#%(target)s').prepend('%(controlbuttons)s');
            $('#%(target)s_controlbuttons').css('float','left').css('margin-right','40px');
            
            $('#%(target)s_addbutton').addClass('addmodal positive');
            $('#%(target)s_addbutton').attr('title','%(addTitle)s');
            $('#%(target)s_addbutton').prepend('<span class=icon></span>');

            $('#%(target)s_addbutton span').addClass('plus');
            
            $('#%(target)s_refreshbutton').prepend('<span class=icon></span>');
            $('#%(target)s_refreshbutton span').addClass('loop');

            $('#%(target)s_refreshbutton').click(function(e){
               e.preventDefault();
               $.fn.gridy.reload('#%(target)s',{
                                          page:$('#%(target)s input#current-page').val(),
                                          rows:$('#%(target)s .gridy-row-option select').val(),  
                                          find:$('#%(target)s .gridy-search select').val(), 
                                          sortName:$('#%(target)s input#current-sort-name').val(),
                                          sortOrder:$('#%(target)s input#current-sort-order').val(),
                                          search:$('#%(target)s .gridy-search input#search').val()
                                                                }
                                                         );
            });

            """ % self.attributes
        else:
            self.attributes.addcontrolbuttons = '' 


        if not 'crudstyle' in self.attributes:
            self.attributes.crudstyle = """
                                        <link type=text/css rel=stylesheet href=%s>
                                        """ % URL('static','plugin_PowerGrid',args='css/crud.css' )

        if not 'minW' in self.attributes:
            self.attributes.minW = 600

        if not 'minH' in self.attributes:
            self.attributes.minH = 400

        self.attributes.options = {
        'arrowDown':      self.attributes.options.get('arrowDown', 'gridy-arrow-down'),
        'arrowNone':      self.attributes.options.get('arrowNone', 'gridy-arrow-none'),
        'arrowUp':        self.attributes.options.get('arrowUp', 'gridy-arrow-up'),
        'before':         self.attributes.options.get('before', None),
        'buttonBackTitle':self.attributes.options.get('buttonBackTitle', str(T('Back'))),
        'buttonNextTitle':self.attributes.options.get('buttonNextTitle', str(T('Next'))),
        'buttonMax':      self.attributes.options.get('buttonMax', 5),
        'buttonOption':   self.attributes.options.get('buttonOption', True),
        'buttonTitle':    self.attributes.options.get('buttonTitle', str(T('page'))),
        'buttonsWidth':   self.attributes.options.get('buttonsWidth', 'auto'),
        'cache':          self.attributes.options.get('cache', False),
        'clickFx':        self.attributes.options.get('clickFx', True),
        'colsWidth':      self.attributes.options.get('colsWidth', colswidth ),
        'complete':       self.attributes.options.get('complete', """function(){
                                                                        

                                                                        $('.gridy-find-option select').prependTo('.gridy-search');
                                                                        %(addcontrolbuttons)s
                                                                        $('.confirmationmodal').click(function(e){
                                                                            e.preventDefault();
                                                                            if (confirm($(this).attr('title'))){
                                                                                  $.ajax({
                                                                                      type:'POST',
                                                                                      url:$(this).attr('href'),
                                                                                      success: function(){
                                                                                          $.fn.gridy.reload('#%(target)s',{
                                                                                                                    page:$('#%(target)s input#current-page').val(),
                                                                                                                    rows:$('#%(target)s .gridy-row-option select').val(),  
                                                                                                                    find:$('#%(target)s .gridy-search select').val(), 
                                                                                                                    sortName:$('#%(target)s input#current-sort-name').val(),
                                                                                                                    sortOrder:$('#%(target)s input#current-sort-order').val(),
                                                                                                                    search:$('#%(target)s .gridy-search input#search').val(),
                                                                                                                                    }
                                                                                                                     );
                                                                                      }
                                                                                  });
                                                                               }
                                                                          }
                                                                        );
                                  
                                                                        $('.refreshmodal').nm({
                                                                                
                                                                                callbacks:{
                                                                          
                                                                          initElts:function(nm){
                                                                                    var minW = parseInt(nm.opener.attr('minW'));
                                                                                    var minH = parseInt(nm.opener.attr('minH'));
                                                                                    nm.sizes.minW = ((nm.opener.attr('minW') == undefined) ? %(minW)s : minW);
                                                                                    nm.sizes.minH = ((nm.opener.attr('minH') == undefined) ? %(minH)s : minH);
                                                                                  },
                                                                          size: function(nm){$('iframe').css('width','100%%').css('height', nm.sizes.minH - 5 +'px' );},
                                                                                filledContent: function(nm){
                                                                                                            $('.nyroModalIframe iframe').load( function(){
                                                                                                                  $('body', $('iframe').contents()).prepend('%(crudstyle)s');
                                                                                                                });
                                                                                                            },
                                                                                      close: function(nm){  
                                                                                                    $.fn.gridy.reload('#%(target)s',{
                                                                                                                    page:$('#%(target)s input#current-page').val(),
                                                                                                                    rows:$('#%(target)s .gridy-row-option select').val(),  
                                                                                                                    find:$('#%(target)s .gridy-search select').val(), 
                                                                                                                    sortName:$('#%(target)s input#current-sort-name').val(),
                                                                                                                    sortOrder:$('#%(target)s input#current-sort-order').val(),
                                                                                                                    search:$('#%(target)s .gridy-search input#search').val(),
                                                                                                                                    }
                                                                                                                     );  
                                                                                                    }
                                                                                          }
                                                                                        });
                                                                        $('.addmodal').nm({ 
                                                                                
                                                                                callbacks:{
                                                                          
                                                                          initElts:function(nm){
                                                                                    var minW = parseInt(nm.opener.attr('minW'));
                                                                                    var minH = parseInt(nm.opener.attr('minH'));
                                                                                    nm.sizes.minW = ((nm.opener.attr('minW') == undefined) ? %(minW)s : minW);
                                                                                    nm.sizes.minH = ((nm.opener.attr('minH') == undefined) ? %(minH)s : minH);
                                                                                  },
                                                                          size: function(nm){$('iframe').css('width','100%%').css('height', nm.sizes.minH - 30 +'px' );},
                                                                                       filledContent: function(nm){
                                                                                                            $('.nyroModalIframe iframe').load( function(){
                                                                                                                  $('body', $('iframe').contents()).prepend('%(crudstyle)s');

                                                                                                                });
                                                                                                            },

                                                                                      close: function(nm){  
                                                                                                    $.fn.gridy.reload('#%(target)s',{
                                                                                                                    page:'1',
                                                                                                                    rows:$('#%(target)s .gridy-row-option select').val(),  
                                                                                                                    find:$('#%(target)s .gridy-search select').val(), 
                                                                                                                    sortName:'id',
                                                                                                                    sortOrder:'desc',
                                                                                                                    search:$('#%(target)s .gridy-search input#search').val(),
                                                                                                                                    }
                                                                                                                     );  
                                                                                                    }
                                                                                          }
                                                                                        });

                                                                        
                                                                        $('.modal').nm({
                                                                          
                                                                           
                                                                          callbacks:{
                                                                          initElts:function(nm){
                                                                                    var minW = parseInt(nm.opener.attr('minW'));
                                                                                    var minH = parseInt(nm.opener.attr('minH'));
                                                                                    nm.sizes.minW = ((nm.opener.attr('minW') == undefined) ? %(minW)s : minW);
                                                                                    nm.sizes.minH = ((nm.opener.attr('minH') == undefined) ? %(minH)s : minH);
                                                                                  },
                                                                          size: function(nm){$('iframe').css('width','100%%').css('height', nm.sizes.minH - 5 +'px' );},
                                                                          filledContent: function(nm){      
                                                                                                    $('.nyroModalIframe iframe').load( function(){
                                                                                                           
                                                                                                          $('body', $('iframe').contents()).prepend('%(crudstyle)s');
                                                                                                    });
                                                                                            },
                                                                        }})


                                                                        ;}""" % self.attributes
                                                    ),
        'contentType':    self.attributes.options.get('contentType', 'application/x-www-form-urlencoded; charset=utf-8'),
        'dataType':       self.attributes.options.get('dataType', 'json'),
        'debug':          self.attributes.options.get('debug', False),
        'error':          self.attributes.options.get('error', None),
        'find':           self.attributes.options.get('find', ''),
        'findsName':      self.attributes.options.get('findsName', self.attributes.get('headers')),
        'findTarget':     self.attributes.options.get('findTarget', 'gridy-search'),
        'height':         self.attributes.options.get('height', 'auto'),
        'headersName':    self.attributes.options.get('headersName', self.attributes.get('headers')),
        'headersWidth':   self.attributes.options.get('headersWidth', []),
        'hoverFx':        self.attributes.options.get('hoverFx', True),
        'jsonp':          self.attributes.options.get('jsonp', False),
        'jsonpCallback':  self.attributes.options.get('jsonpCallback', 'callback'),
        'loadingIcon':    self.attributes.options.get('loadingIcon', 'gridy-loading'),
        'loadingOption':  self.attributes.options.get('loadingOption', True),
        'loadingText':    self.attributes.options.get('loadingText', str(T('Loading...'))),
        'messageOption':  self.attributes.options.get('messageOption', True),
        'messageTimer':   self.attributes.options.get('messageTimer', 4000),
        'noResultOption': self.attributes.options.get('noResultOption', True),
        'noResultText':   self.attributes.options.get('noResultText', str(T('No items found!'))),
        'page':           self.attributes.options.get('page', 1),
        'params':         params,
        'resultOption':   self.attributes.options.get('resultOption', True),
        'resultText':     self.attributes.options.get('resultText', str(T('Displaying {from} - {to} of {total} items'))),
        'rows':           self.attributes.options.get('rows', 5),
        'rowsNumber':     self.attributes.options.get('rowsNumber', [3, 5, 10, 25, 50, 100]),
        'rowsTarget':     self.attributes.options.get('rowsTarget', 'gridy-content'),
        'search':         self.attributes.options.get('search', ''),
        'searchFocus':    self.attributes.options.get('searchFocus', False),
        'searchOption':   self.attributes.options.get('searchOption', True),
        'searchButtonLabel':self.attributes.options.get('searchButtonLabel', str(T('search'))),
        'searchButtonTitle':self.attributes.options.get('searchButtonTitle', str(T('Start the search'))),
        'searchText':     self.attributes.options.get('searchText', str(T('type your search here...'))),
        'scroll':         self.attributes.options.get( 'scroll', False),
        'sortersName':    self.attributes.options.get('sortersName', []),
        'sortName':       self.attributes.options.get('sortName', ''),
        'sortOrder':      self.attributes.options.get('sortOrder', 'asc'),
        'sorterWidth':    self.attributes.options.get('sorterWidth', 'auto'),
        'success':        self.attributes.options.get('success', None),
        'template':       self.attributes.options.get('template', 'template'),
        'templateStyle':  self.attributes.options.get('templateStyle', 'gridy-default'),
        'type':           self.attributes.options.get('type', 'post'),
        'url':            self.attributes.get('callback'),
        'width':          self.attributes.options.get('width', 900),
        'resize':          self.attributes.options.get('resize', True)
        }
        
      
        script = """
        $(function() {
          $('#%(target)s').gridy( 
                %(options)s  
           ); 
        })""" % self.attributes
        self.append(PowerScript(script.replace('True','true').\
                                       replace('False','false').\
                                       replace('None','null').\
                                       replace('"function','function').\
                                       replace(';}"',';}').\
                                       replace(']js"',' ').\
                                       replace('"js[',' ').\
                                       replace('\\n','').\
                                       replace('arrownull','arrowNone'), 
                                       _type="text/javascript"))



        self.append(PowerScript(template, _id='template',_type='text/x-jquery-tmpl'))

        self.append(STYLE("""
                            div.gridy-default div.gridy-row { 
                                    border: 1px solid #CCC; 
                                    float: left; 
                                    margin-bottom: -1px;
                                    width:%spx;
                         }""" % self.attributes.options.get('width', 900)
                         ,
                         """
                         .%s {
                           position:relative;
                           float:right !important;   
                         }
                         """ % ('%s_buttons' % self.attributes['target'])
                         ,
                         """
                         #%(target)s {
                           width:%(width)spx;
                           margin:auto;  
                         }
                         """ % dict(target=self.attributes['target'],
                                    width=self.attributes.options.get('width', 900)
                                    )
                         ,
                         """
                         .gridy-footer {
                             line-height:0 !important;
                         }
                         .gridy-find-option select, .gridy-row-option select, .gridy-search select{
                             width:auto !important;
                         }
                         """
                        )
                    )
        

    def power_template(self, template='grid'):
        if template == 'grid':
            # auto generated jquery template
            template = DIV(_id="${id}")
            [template.append(DIV('{{html %s}}' % head[0])) \
                 if self.attributes['as_html'] \
                 else template.append(DIV('${%s}' % head[0])) \
                 for head in self.attributes.get('headers',[])
            ]

            if self.attributes.get('buttons', None):
                div = DIV(_class='%s_buttons' % self.attributes['target'])
                for button in self.attributes['buttons']:
                    try:
                        icon = SPAN(_class='%s icon' % button[5])
                    except:
                        icon = ''

                    button_attributes = {}
                    button_attributes['_href'] = button[1]
                    button_attributes['_target'] = button[2]
                    button_attributes['_title'] = button[3]
                    button_attributes['_class'] = button[4]
                    try:
                        button_attributes['_minW'] = button[6][0]
                    except:
                        'No width for button'
                    try:
                        button_attributes['_minH'] = button[6][1]
                    except:
                        'no height for button'
                    div.append(A(icon, button[0],**button_attributes))
                template.append(div)
        else:
            template = template
        return template

    def callback(self, datasource):
        from CallBack import CallBack
        #if current.request.extension == 'json':
        return CallBack(datasource)
