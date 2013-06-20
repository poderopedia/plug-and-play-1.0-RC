# coding: utf8
__author__ = 'Evolutiva'

import uuid
import datetime
from gluon.sqlhtml import OptionsWidget
from gluon.sqlhtml import MultipleOptionsWidget

bootstrap_select_min_js = URL(c='static/js',f='bootstrap-select.min.js')
bootstrap_select_min_css = URL(c='static/css',f='bootstrap-select.min.css')

class GroupOptions_widget(OptionsWidget):
    """
      An GroupOptions using BootStrap
    """
    def __init__(self, groups, ui_js = bootstrap_select_min_js,
                       ui_css = bootstrap_select_min_css):
        if not ui_js in response.files:
            response.files.append(ui_js)
        if not ui_css in response.files:
            response.files.append(ui_css)
        self.groups = groups

    def widget(self, field, value,**attributes):
        attr = OptionsWidget._attributes(field, {'value':value}, **attributes)
        opts = [OPTION('')] + [ OPTGROUP(
            _label=group, *[OPTION(v, _value=k) for (k, v) in options.items()])
                for group, options in self.groups.items() ]
        #d_id = "multiselect-" + str(uuid.uuid4())[:8]
        #wrapper = DIV(_id=d_id)
        wrapper = SELECT(*opts, **attr)

        #inp = SELECT(*opts, **attr)
        scr = SCRIPT('$(".selectpicker").selectpicker();')
        #opts = 'minLength: %s, delay: %s, disabled: %s' % \
        #       (self.min_length,self.delay,str(self.disabled).lower())
        #if self.url:
            #scr = SCRIPT('jQuery("#%s input").autocomplete({source: "%s", %s});' % \
            #      (d_id, self.url, opts))
        #else:
        #    rows = f._db(f._table['id']>0).select(f,distinct=True)
        #   itms = [str(t[f.name]) for t in rows]
        #    scr = SCRIPT('var data = "%s".split("|");'\
        #                 'jQuery("#%s input").autocomplete({source: data, %s});' % \
        #                       ("|".join(itms),d_id,opts))
        #wrapper.append(inp)
        wrapper.append(scr)
        return wrapper

class SELECT_OR_ADD_OPTION(object):

    def __init__(self, controller=None, function=None, form_title=None, button_text = None, dialog_width=500,multiple=True):
        if form_title == None:
            self.form_title = T('Add New')
        else:
            self.form_title = T(form_title)
        if button_text == None:
            self.button_text = T('Add')
        else:
            self.button_text = T(button_text)
        self.dialog_width = dialog_width
        self.multiple = multiple

        self.controller = controller
        self.function = function
    def widget(self, field, value,**attributes):



        #generate the standard widget for this field
        if self.multiple == True:
            select_widget = MultipleOptionsWidget.widget(field, value, size=7)
            attr =  MultipleOptionsWidget._attributes(field, {'value':value}, **attributes)
        else:
            select_widget = OptionsWidget.widget(field, value)
            attr = OptionsWidget._attributes(field, {'value':value}, **attributes)

        #get the widget's id (need to know later on so can tell receiving controller what to update)
        my_select_id = select_widget.attributes.get('_id', None)
        add_args = [my_select_id]
        #create a div that will load the specified controller via ajax
        form_loader_div = DIV(LOAD(c=self.controller, f=self.function, args=add_args,ajax=True), _id=my_select_id+"_dialog-form", _title=self.form_title)
        #generate the "add" button that will appear next the options widget and open our dialog

        activator_button = A(XML('<button type="button" class="btn btn-primary" data-toggle="button">'+T(self.button_text)+'</button>'), _id=my_select_id+"_option_add_trigger")
        #create javascript for creating and opening the dialog
        js = '$( "#%s_dialog-form" ).dialog({autoOpen: false, show: "blind", hide: "explode", width: %s});' % (my_select_id, self.dialog_width)
        js += '$( "#%s_option_add_trigger" ).click(function() { $( "#%s_dialog-form" ).dialog( "open" );return false;}); ' % (my_select_id, my_select_id)        #decorate our activator button for good measure
        js += '$(function() { $( "#%s_option_add_trigger" ).button({text: true, icons: { primary: "ui-icon-circle-plus"} }); });' % (my_select_id)
        jq_script=SCRIPT(js, _type="text/javascript")

        wrapper = DIV(_id=my_select_id+"_adder_wrapper")
        wrapper.components.extend([select_widget, form_loader_div, activator_button, jq_script])
        return wrapper



