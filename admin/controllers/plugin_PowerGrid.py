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
# uncomment line below if you want to require user signature.
#@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id[
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs bust be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """

    if request.args(0) == 'deleted':
            return dict(message='Deleted')
        
    #crud.settings.formstyle = 'divs'
    crud.settings.controller = 'plugin_PowerGrid'
    crud.settings.download_url = URL('download')

    def updater(form):
        if not form.errors:
            form.append(SCRIPT('parent.$.nmTop().close();'))

    crud.settings.update_onaccept = lambda form: updater(form)
    crud.settings.create_onaccept = lambda form: updater(form)
    crud.settings.delete_next = URL('plugin_PowerGrid','data',args='deleted')

    return dict(form=crud())

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def testcallback(x):
    """
    THE JSON WHICH NEEDS TO BE RETURNED
    {"entityList": [{"id": 1, "name": "Washington Botelho", "email": "gridy@wbotelhos.com"}], "total": 1}

    ARGS RECEIVED

    search=__&page=__&sortname=__&sortorder=__&find=__&rows=__&searchBy__
    - search: the term you want to search;
    - page: the number of the page you want to view;
    - sortname: the name of the column of the database you want to sort by;
    - sortorder: the order you want to sort the result: ascending or descending;
    - find: the name of the column you want to search;
    - rows: the number of rows you want to display in each page;
    - You can append more attributes using the 'params' option.
    - searchBy is the kind of search to be done. like, equal, notequal, startswith, endswith, gt, lt, ge, le


    """
    return {"entityList": [
                       {"id": 1, "name": "wbotelhos", "email": "gridy@wbotelhos.com"},
                       {"id": 1, "name": "junb", "email": "gridy@wbotelhos.com"},
                       {"id": 1, "name": "erfb", "email": "gridy@wbotelhos.com"},
                       {"id": 1, "name": "bruno", "email": "gridy@wbotelhos.com"},
                       {"id": 1, "name": "uiolp", "email": "gridy@wbotelhos.com"},
                       
                      ],
             "total": 5,
             "headers":['id','name','email']}