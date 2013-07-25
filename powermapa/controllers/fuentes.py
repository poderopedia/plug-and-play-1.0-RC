__author__ = 'Evolutiva'

def create():
    #This is the main function, the one your users go to

    #Initialize the widget
    add_option = SELECT_OR_ADD_OPTION(form_title=T("Agregar Fuentes"), controller="fuentes", function="add_source", button_text = T("Nueva Fuente"))
    #assign widget to field
    db.persona.documentSource.widget = add_option.widget

    form = SQLFORM(db.product)
    if form.accepts(request.vars, session):
        response.flash = "New product created"
    elif form.errors:
        response.flash = "Please fix errors in form"
    else:
        response.flash = "Please fill in the form"

    #you need jquery for the widget to work, include here or just put in your master layout.html
    response.files.append("http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.9/jquery-ui.js")
    response.files.append("http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.9/themes/smoothness/jquery-ui.css")
    return dict(message="Create your product",
            form = form)

def add_source():
    #this is the controller function that will appear in our dialog
    form = SQLFORM(db.document)

    multiselect_js= URL('static','js/jquery.multiselect.min.js')

    if form.accepts(request.vars):
        #Successfully added new item
        #do whatever else you may want

        #Then let the user know adding via our widget worked
        response.flash = T("Added")
        target= request.args[0]
        #close the widget's dialog box
        response.js = '$( "#%s_dialog-form" ).dialog( "close" ); ' %(target)

        #update the options they can select their new category in the main form
        response.js += """$("#%s").append("<option value='%s'>%s</option>");""" \
                % (target, form.vars.id, form.vars.name)
        #and select the one they just added

        response.js += """var selected=$("#%s").val();""" %(target)
        response.js += """if (selected==null) { selected = [] }"""
        response.js += """selected.push("%s");""" %(form.vars.id)
        response.js += """$("#%s").val(selected);""" %(target)
        ##for multiselect jquery plugin
        #response.js += """console.log('maluenda');"""
        response.js += """$("#%s").multiselect('refresh');""" % target
        #finally, return a blank form incase for some reason they wanted to add another option
        return form
    elif form.errors:
        #silly user, just send back the form and it'll still be in our dialog box complete with error messages
        return form
    else:
        #hasn't been submitted yet, just give them the fresh blank form
        return form
