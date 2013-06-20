# -*- coding: utf-8 -*-
from plugin_anytime_widget import anytime_widget, anydate_widget, anydatetime_widget

db = DAL('sqlite:memory:')
db.define_table('product',
    Field('event_time', 'time'), Field('publish_date', 'date'),
    Field('created_at', 'datetime'),
    Field('updated_at', 'datetime'),
)
################################ The core ######################################
# Inject the corresponding anytime widgets for time, date, and datetime fields
db.product.event_time.widget = anytime_widget
db.product.publish_date.widget = anydate_widget
db.product.created_at.widget = anydatetime_widget
db.product.updated_at.widget = anydatetime_widget
################################################################################


def index():
    form = SQLFORM(db.product)
    if form.accepts(request.vars, session):
        session.flash = 'submitted %s' % form.vars
        redirect(URL('index'))
    return dict(form=form, tests=[A('test_with_jquery_ui', _href=URL('test', args='with_jquery_ui')),
                                 A('test_load', _href=URL('test', args=['_', 'load'])),
                                 A('test_load_with_jquery_ui', _href=URL('test', args=['with_jquery_ui', 'load'])),
                                 ])


def test():
    if request.args(0) == 'ajax':
        form = SQLFORM(db.product)
        if form.accepts(request.vars, session):
            response.flash = DIV('submitted %s' % form.vars).xml()
        return form
    elif request.args(0) == 'with_jquery_ui':
        response.files += (
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.16/themes/base/jquery-ui.css',
            'http://static.jquery.com/ui/css/demo-docs-theme/ui.theme.css',
            URL('static', 'js/jquery-ui.min.js'), URL('static', 'js/jquery.ui.dialog.js'),
            URL('static', 'js/jquery.ui.tabs.js'), URL('static', 'js/jquery.ui.themeswitcher.js'))
        jquery_ui = DIV(
            DIV(_id='switcher'), BR(),
            DIV(UL(LI(A('xxx', _href='#xxx')), LI(A('yyy', _href='#yyy'))),
                DIV(P('xxx'), _id='xxx'), DIV(P('yyy'), _id='yyy'),
                _id='example'),
            SCRIPT("$().ready(function(){var $tabs = $('#example').tabs();});"))
    else:
        jquery_ui = ''
    if request.args(1) == 'load':
        form = LOAD('plugin_anytime_widget', 'test', args='ajax', ajax=True)
    else:
        form = SQLFORM(db.product)
        if form.accepts(request.vars, session):
            session.flash = 'submitted %s' % form.vars
            redirect(URL('index'))
        
    return dict(back=A('back', _href=URL('index')), jquery_ui=jquery_ui, form=form)
