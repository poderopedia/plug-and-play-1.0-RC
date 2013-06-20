# coding: utf8

def download():
    return response.download(request,db)

def fast_download():
    # very basic security (only allow fast_download on your_table.upload_field):
    if not request.args(0).startswith("persona.depiction"):
        return download()
        # remove/add headers that prevent/favors client-side caching
    response.headers['Cache-Control']=''
    response.headers['Pragma']=''
    response.headers['Expires']=''
    filename = os.path.join(request.folder,'uploads',request.args(0))
    # send last modified date/time so client browser can enable client-side caching
    response.headers['Last-Modified'] = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(os.path.getmtime(filename)))
    return response.stream(open(filename,'rb'))

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def index(): 
    return dict(message="hello from directorio.py")

@cache(request.env.path_info,time_expire=10,cache_model=cache.ram)
def general():
    url =request.env.http_host + request.env.request_uri
    tab='general'
    if len(request.args)>0: tab=request.args(0)

    return dict(_id=0,tab=tab,url=url)

@cache(request.env.path_info,time_expire=10,cache_model=cache.ram)
def persona():
    tab='persona'
    response.view='directorio/general.html'
    return dict(_id=0,tab=tab)

@cache(request.env.path_info,time_expire=10,cache_model=cache.ram)
def empresa():
    tab='empresa'
    response.view='directorio/general.html'
    return dict(_id=0,tab=tab)

@cache(request.env.path_info,time_expire=10,cache_model=cache.ram)
def organizacion():
    tab='organizacion'
    response.view='directorio/general.html'
    return dict(_id=0,tab=tab)

##TODO
def casos():
    return locals()

##TODO
def mapas():
    return locals()


##directorio components
##TODO
def service_general():
    return locals()


def service_persona():

    if len(request.args)>0: alphapage=int(request.args[0])
    else: alphapage=0
    if len(request.args)>1: page=int(request.args[1])
    else: page=0
    if len(request.args)>2: sort=request.args(2)
    else: sort='false'
    if len(request.args)>3: letter=request.args(3)
    else: letter='A'
    if len(request.args)>4: target=request.args(4)
    elif (request.vars['target']!=None) & (len(request.vars['target'])>0):
        target=request.vars['target']
    else: target='service_persona'

    function="service_personselect"
    if(target=='service_persona'):
        function='service_personselect'
    elif target=='service_empresa':
        function='service_empresaselect'
    elif target=='service_organizacion':
        function='service_organizacionselect'

    items_per_page=4
    begin=page*items_per_page
    end=(page+1)*items_per_page
    if end>26:
        end=26


    length=26-(begin)
    entity=[i for i in range(length)]

    return dict(_id=0,letter=letter,function=function,sort=sort,target=target,page=page,alphapage=alphapage,items_per_page=items_per_page,entity=entity,begin=begin,end=end)

def service_personselect():
    if (request.cid==None) | (request.cid==''):
        redirect(URL('error','error404'))

    if len(request.args)>0: alphapage=int(request.args[0])
    else: alphapage=0
    if len(request.args)>1: number=int(request.args[1])
    else: number=0
    if len(request.args)>2: sort=request.args(2)
    else: sort='false'
    target='service_personselect_'+chr(ord('a')+number)

    if(sort!='false'):
        reverse=False
        orderby=~db.persona.firstLastName
    else:
        reverse=True
        orderby=db.persona.firstLastName

    alpha_length=9; letter=chr(ord('a')+number)
    limitby=(alphapage*alpha_length,(alphapage+1)*alpha_length+1)

    total=len(db((db.persona.firstLastName.like(letter+'%')) & (db.persona.is_active==True)).select(cache=(cache.ram,3600)))
    personas=db((db.persona.firstLastName.like(letter+'%')) & (db.persona.is_active==True)).select(orderby=orderby,limitby=limitby,cache=(cache.ram,3600))


    return dict(personas=personas,target=target,key=number,alphapage=alphapage,alpha_length=alpha_length,total=total)

def service_personselect_letter():
    if len(request.args)>0: _id=int(request.args[0])
    else: _id=0
    if len(request.args)>1: page=int(request.args[1])
    else: page=0
    if len(request.args)>2: sort=request.args(2)
    else: sort='false'
    if len(request.args)>3: letter=request.args(3)
    else: letter=' '

    target='service_persona'; function="service_personselect"

    items_per_page=30
    limitby=(page*items_per_page,(page+1)*items_per_page+1)

    if(sort!='false'):
        reverse=False
        orderby=~db.persona.firstLastName
    else:
        reverse=True
        orderby=db.persona.firstLastName

    total=len(db((db.persona.firstLastName.like(letter+'%')) & (db.persona.is_active==True)).select(cache=(cache.ram,3600)))

    personas=db((db.persona.firstLastName.like(letter+'%')) & (db.persona.is_active==True)).select(orderby=orderby,limitby=limitby,cache=(cache.ram,3600))

    return dict(function=function,total=total,personas=personas,page=page,items_per_page=items_per_page,target=target,entity=personas,_id=_id, sort=sort,letter=letter)

def service_empresaselect_letter():
    if len(request.args)>0: _id=int(request.args[0])
    else: _id=0
    if len(request.args)>1: page=int(request.args[1])
    else: page=0
    if len(request.args)>2: sort=request.args(2)
    else: sort='false'
    if len(request.args)>3: letter=request.args(3)
    else: letter=' '

    target='service_empresa'; function="service_empresaselect"

    items_per_page=30
    limitby=(page*items_per_page,(page+1)*items_per_page+1)

    if(sort!='false'):
        reverse=False
        orderby=~db.Organizacion.alias
    else:
        reverse=True
        orderby=db.Organizacion.alias

    total=len(db((db.Organizacion.alias.like(letter+'%')) & (db.Organizacion.tipoOrg==2) & (db.Organizacion.is_active==True)).select(cache=(cache.ram,3600)))

    empresas=db((db.Organizacion.alias.like(letter+'%')) & (db.Organizacion.tipoOrg==2) & (db.Organizacion.is_active==True)).select(orderby=orderby,limitby=limitby,cache=(cache.ram,3600))

    return dict(function=function,total=total,empresas=empresas,page=page,items_per_page=items_per_page,target=target,entity=empresas,_id=_id, sort=sort,letter=letter)

def service_organizacionselect_letter():
    if len(request.args)>0: _id=int(request.args[0])
    else: _id=0
    if len(request.args)>1: page=int(request.args[1])
    else: page=0
    if len(request.args)>2: sort=request.args(2)
    else: sort='false'
    if len(request.args)>3: letter=request.args(3)
    else: letter=' '

    target='service_organizacion'; function="service_organizacionselect"

    items_per_page=30
    limitby=(page*items_per_page,(page+1)*items_per_page+1)

    if(sort!='false'):
        reverse=False
        orderby=~db.Organizacion.alias
    else:
        reverse=True
        orderby=db.Organizacion.alias

    total=len(db((db.Organizacion.alias.like(letter+'%')) & (db.Organizacion.tipoOrg!=2) & (db.Organizacion.is_active==True)).select(cache=(cache.ram,3600)))

    organizaciones=db((db.Organizacion.alias.like(letter+'%')) & (db.Organizacion.tipoOrg!=2) & (db.Organizacion.is_active==True)).select(orderby=orderby,limitby=limitby,cache=(cache.ram,3600))

    return dict(function=function,total=total,organizaciones=organizaciones,page=page,items_per_page=items_per_page,target=target,entity=organizaciones,_id=_id, sort=sort,letter=letter)


def service_empresaselect():
    if (request.cid==None) | (request.cid==''):
        redirect(URL('error','error404'))
    empresas=""

    if len(request.args)>0: alphapage=int(request.args[0])
    else: alphapage=0
    if len(request.args)>1: number=int(request.args[1])
    else: number=0
    if len(request.args)>2: sort=request.args(2)
    else: sort='false'
    target='service_empresaselect_'+chr(ord('a')+number)

    if(sort!='false'):
        reverse=False
        orderby=~db.Organizacion.alias
    else:
        reverse=True
        orderby=db.Organizacion.alias

    alpha_length=9; letter=chr(ord('a')+number)
    limitby=(alphapage*alpha_length,(alphapage+1)*alpha_length+1)

    total=len(db((db.Organizacion.alias.like(letter+'%')) & (db.Organizacion.tipoOrg==2) & (db.Organizacion.is_active==True)).select(cache=(cache.ram,3600)))
    empresas=db((db.Organizacion.alias.like(letter+'%')) & (db.Organizacion.tipoOrg==2) & (db.Organizacion.is_active==True)).select(orderby=orderby,limitby=limitby,cache=(cache.ram,3600))

    return dict(empresas=empresas,target=target,key=number,alphapage=alphapage,alpha_length=alpha_length,total=total)



def service_organizacionselect():
    if (request.cid==None) | (request.cid==''):
        redirect(URL('error','error404'))

    if len(request.args)>0: alphapage=int(request.args[0])
    else: alphapage=0
    if len(request.args)>1: number=int(request.args[1])
    else: number=0
    if len(request.args)>2: sort=request.args(2)
    else: sort='false'
    target='service_organizacionselect_'+chr(ord('a')+number)

    if(sort!='false'):
        reverse=False
        orderby=~db.Organizacion.alias
    else:
        reverse=True
        orderby=db.Organizacion.alias

    alpha_length=9; letter=chr(ord('a')+number)
    limitby=(alphapage*alpha_length,(alphapage+1)*alpha_length+1)

    total=len(db((db.Organizacion.alias.like(letter+'%')) & (db.Organizacion.tipoOrg!=2) & (db.Organizacion.is_active==True)).select(cache=(cache.ram,3600)))
    organizaciones=db((db.Organizacion.alias.like(letter+'%')) & (db.Organizacion.tipoOrg!=2) & (db.Organizacion.is_active==True)).select(orderby=orderby,limitby=limitby,cache=(cache.ram,3600))

    return dict(organizaciones=organizaciones,target=target,key=number,alphapage=alphapage,alpha_length=alpha_length,total=total)
