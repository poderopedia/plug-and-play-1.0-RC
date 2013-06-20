# -*- coding: utf-8 -*-
# This plugins is licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
# Authors: Kenji Hosoda <hosoda@s-cubism.jp>
from gluon import *
from gluon.sqlhtml import widget_class

# For referencing static and views from other application
import os
APP = os.path.basename(os.path.dirname(os.path.dirname(__file__)))

FILES = (URL(APP, 'static', 'plugin_anytime_widget/anytime.css'),
         URL(APP, 'static', 'plugin_anytime_widget/anytime.js'))


def _set_files(files):
    if current.request.ajax:
        current.response.js = (current.response.js or '') + """;(function ($) {
var srcs = $('script').map(function(){return $(this).attr('src');}),
    hrefs = $('link').map(function(){return $(this).attr('href');});
$.each(%s, function() {
    if ((this.slice(-3) == '.js') && ($.inArray(this.toString(), srcs) == -1)) {
        var el = document.createElement('script'); el.type = 'text/javascript'; el.src = this;
        document.body.appendChild(el);
    } else if ((this.slice(-4) == '.css') && ($.inArray(this.toString(), hrefs) == -1)) {
        $('<link rel="stylesheet" type="text/css" href="' + this + '" />').prependTo('head');
        if (/* for IE */ document.createStyleSheet){document.createStyleSheet(this);}
}});})(jQuery);""" % ('[%s]' % ','.join(["'%s'" % f.lower().split('?')[0] for f in files]))
    else:
        current.response.files[:0] = [f for f in files if f not in current.response.files]


def _get_date_option():
    return """{
labelYear: "%(year)s", labelMonth: "%(month)s", labelDay: "%(day)s",
labelDayOfMonth: "%(calendar)s",
monthAbbreviations: ["%(jan)s", "%(feb)s", "%(mar)s",
  "%(apr)s", "%(may)s", "%(jun)s",  "%(jul)s",
  "%(aug)s", "%(sep)s", "%(oct)s", "%(nov)s", "%(dec)s"],
dayAbbreviations: ["%(sun)s", "%(mon)s", "%(tue)s", "%(wed)s",
                   "%(thu)s", "%(fri)s", "%(sat)s"],
labelDismiss: "%(ok)s" }""" % dict(
        year=current.T('Year'), month=current.T('Month'), day=current.T('Day'),
        calendar=current.T('Calendar'),
        jan=current.T('Jan'), feb=current.T('Feb'), mar=current.T('Mar'),
        apr=current.T('Apr'), may=current.T('May'), jun=current.T('Jun'),
        jul=current.T('Jul'), aug=current.T('Aug'), sep=current.T('Sep'),
        oct=current.T('Oct'), nov=current.T('Nov'), dec=current.T('Dec'),
        sun=current.T('Sun'), mon=current.T('Mon'), tue=current.T('Tue'),
        wed=current.T('Wed'), thu=current.T('Thu'), fri=current.T('Fri'),
        sat=current.T('Sat'), ok=current.T('OK'),
    )


def anytime_widget(field, value, **attributes):
    _set_files(FILES)
    
    _id = '%s_%s' % (field._tablename, field.name)
    attr = dict(
            _type='text', value=(value != None and str(value)) or '',
            _id=_id, _name=field.name, requires=field.requires,
            _class='any%s' % widget_class.match(str(field.type)).group(),
            )
            
    script = SCRIPT("""
jQuery(function() { var t = 10; (function run() {if ((function() {
    var el = jQuery("#%(id)s");
    if (el.AnyTime_picker == undefined) { return true; }
    el.AnyTime_noPicker().AnyTime_picker(
        jQuery.extend({format: "%%H:%%i:%%S", labelTitle: "%(title)s",
            labelHour: "%(hour)s", labelMinute: "%(minute)s", labelSecond: "%(second)s"},
            %(date_option)s));
})()) {setTimeout(run, t); t = 2*t;}})();});
""" % dict(id=_id, title=current.T('Choose time'),
           hour=current.T('Hour'), minute=current.T('Minute'), second=current.T('Second'),
           date_option=_get_date_option()))
    
    return SPAN(script, INPUT(**attr), **attributes)

    
def anydate_widget(field, value, **attributes):
    _set_files(FILES)
    
    _id = '%s_%s' % (field._tablename, field.name)
    attr = dict(
            _type='text', value=(value != None and str(value)) or '',
            _id=_id, _name=field.name, requires=field.requires,
            _class='any%s' % widget_class.match(str(field.type)).group(),
            )
           
    script = SCRIPT("""
jQuery(function() { var t = 10; (function run() {if ((function() {
    var el = jQuery("#%(id)s");
    if (el.AnyTime_picker == undefined) { return true; }
    el.AnyTime_noPicker().AnyTime_picker(
    jQuery.extend({format: "%%Y-%%m-%%d", labelTitle: "%(title)s"},
                   %(date_option)s));
})()) {setTimeout(run, t); t = 2*t;}})();});
""" % dict(id=_id, title=current.T('Choose date'),
           date_option=_get_date_option()))
       
    return SPAN(script, INPUT(**attr), **attributes)


def anydatetime_widget(field, value, **attributes):
    _set_files(FILES)
    
    _id = '%s_%s' % (field._tablename, field.name)
    attr = dict(
            _type='text', value=(value != None and str(value)) or '',
            _id=_id, _name=field.name, requires=field.requires,
            _class='any%s' % widget_class.match(str(field.type)).group(),
            )

    script = SCRIPT("""
jQuery(function() { var t = 10; (function run() {if ((function() {
    var el = jQuery("#%(id)s");
    if (el.AnyTime_picker == undefined) { return true; }
    el.AnyTime_noPicker().AnyTime_picker(
        jQuery.extend({format: "%%Y-%%m-%%d %%H:%%i:00", labelTitle: "%(title)s",
                       labelHour: "%(hour)s", labelMinute: "%(minute)s"},
                       %(date_option)s));
})()) {setTimeout(run, t); t = 2*t;}})();});
""" % dict(id=_id, title=current.T('Choose date time'),
           hour=current.T('Hour'), minute=current.T('Minute'),
           date_option=_get_date_option()))
    
    return SPAN(script, INPUT(**attr), **attributes)
