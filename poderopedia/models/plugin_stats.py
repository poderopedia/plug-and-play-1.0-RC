__author__ = 'Evolutiva'

#!/usr/bin/env python
# -*- coding: utf-8 -*-

def _(db,                      # reference to DAL obj.
      page_key,                # string to id page
      page_subkey='',          # string to is subpages
      initial_hits=0,          # hits initial value
      tablename="plugin_stats" # table where to store data
):
    from gluon.storage import Storage
    table = db.define_table(tablename,
        Field('page_key'),
        Field('page_subkey'),
        Field('hits', 'integer'),
        Field('dia','date', default=request.now),
        Field('week','integer'),
        Field('month','integer'),
        Field('year','integer')
    )
    hits=total=0; widget=""
    if 'load' not in page_key:
        dia=request.now
        week=int(dia.strftime('%W'))
        month=int(dia.strftime('%m'))
        year=int(dia.strftime('%Y'))
        record = table(page_key=page_key,page_subkey=page_subkey,dia=dia,week=week,month=month,year=year)
        if record:
            new_hits = record.hits + 1
            record.update_record(hits=new_hits)
            hits = new_hits
        else:
            table.insert(page_key=page_key,
                page_subkey=page_subkey,
                hits=initial_hits,
                dia=dia,week=week,month=month,year=year
            )
            hits = initial_hits
        hs = table.hits.sum()
        total = db(table.page_key==page_key).select(hs).first()(hs)
        widget = SPAN('Hits:',hits,'/',total)
    return Storage(dict(hits=hits,total=total,widget=widget))

plugin_stats = _(db,
    page_key=request.env.path_info,
    page_subkey=request.query_string)
