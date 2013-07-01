# coding: utf8
db.define_table('plugin_stats',
        Field('page_key'),
        Field('page_subkey'),
        Field('hits', 'integer'),
        Field('dia','date', default=request.now),
        Field('week','integer'),
        Field('month','integer'),
        Field('year','integer')
    )
