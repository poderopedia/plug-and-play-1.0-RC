__author__ = 'Evolutiva'

def fechas(day,month,year):
    try:
        day=int(day)
    except ValueError:
        day=''
    try:
        month=int(month)
    except ValueError:
        month=''
    try:
        year=int(year)
    except ValueError:
        year=''

    if (day!='') & (month!='') & (year!=''):
        fecha_val=str(day).zfill(2)+'-'+str(month).zfill(2)+'-'+str(year)
    elif (month!='') & (year!=''):
        fecha_val=str(month).zfill(2)+'-'+str(year)
    elif year!='':
        fecha_val=str(year)
    else:
        fecha_val=''

    return fecha_val
