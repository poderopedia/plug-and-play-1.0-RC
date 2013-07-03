__author__ = 'Evolutiva'

def index():
    """
    Pre - populate Database

    :return:
    """
    from setup.setup import SetupPopulate
    next=''

    try:
        install_return = SetupPopulate(db=db,request=request)
        msg = T('Success in Pre -Populate Data')
        #create admin user
        next=A(T('Siguiente > Crear Super Admin'),_class='btn',_href=URL('install','create_superadmin'),_type='button')

    except:
        msg = T('Error to access module')

    response.flash = msg


    return dict(message=msg,next=next)

def create_superadmin():

    auth.settings.registration_requires_verification=False
    db.auth_user.username.default='super.admin'
    db.auth_user.username.readable=True
    db.auth_user.username.writable=False
    next=A(T('Volver'),_class='btn',_href=URL('install','index'))
    form=''
    #check if role is asigned
    if db(db.auth_membership.group_id==1).count()>0:
        redirect(URL('install','create_super_admin_response'))

    else:
        form=auth.register()

        if form.process().accepted:
            session.flash = T('form accepted')
            group_id = db(db.auth_group.role=='super_administrator').select(db.auth_group.id).first()
            db.auth_membership.validate_and_insert(
                user_id=form.vars.id,
                group_id=group_id
            )
            super_admin_user = db.auth_user(form.vars.id)
            super_admin_user.update_record(registration_key='')

            redirect(URL('install','create_super_admin_response'))

        elif form.errors:
           response.flash = T('form has errors')
        else:
           response.flash = T('please fill out the form')

    return dict(form=form)

def create_super_admin_response():
    next=A(T('Siguiente > Crear Admin'),_class='btn',_href=URL('install','create_admin'),_type='button')
    return dict(next=next)

def create_admin():
    auth.settings.registration_requires_verification=False
    db.auth_user.username.default='admin'
    db.auth_user.username.readable=True
    db.auth_user.username.writable=False

    form=''
    #check if role is asigned
    if db(db.auth_membership.group_id==2).count()>0:
        redirect(URL('install','create_admin_response'))

    else:

        form=auth.register()

        if form.process().accepted:
            session.flash = T('form accepted')
            group_id = db(db.auth_group.role=='administrator').select(db.auth_group.id).first()
            db.auth_membership.validate_and_insert(
                user_id=form.vars.id,
                group_id=group_id
            )
            admin_user = db.auth_user(form.vars.id)
            admin_user.update_record(registration_key='')
            redirect(URL('install','create_admin_response'))

        elif form.errors:
           response.flash = T('form has errors')
        else:
           response.flash = T('please fill out the form')


    return dict(form=form)

def create_admin_response():
    next=A(T('Volver a Menú'),_class='btn',_href=URL('default','index'),_type='button')
    return dict(next=next)