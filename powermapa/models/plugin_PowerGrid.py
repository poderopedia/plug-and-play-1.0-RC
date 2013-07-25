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
#remove comment below if any problem
from gluon.custom_import import track_changes
track_changes()

if not response.generic_patterns:	
    response.generic_patterns = ['*.json','*.load','*.html']

import copy
global_env = copy.copy(globals())
def get_databases(request):
    dbs = {}
    for (key, value) in global_env.items():
        cond = False
        try:
            cond = isinstance(value, GQLDB)
        except:
            cond = isinstance(value, SQLDB)
        if cond:
            dbs[key] = value
    return dbs


databases = get_databases(None)

if not 'db' in globals():
    db = databases.values()[0]
else:
    db = globals()['db']

if  not 'crud' in globals():
    crud = Crud(db)

