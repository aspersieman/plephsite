import datetime
now=datetime.datetime.today()

db.define_table('rules',
                SQLField('title', length=64),
                SQLField('user_id', db.auth_user),
                SQLField('addeddate', 'datetime',default=now),
                SQLField('description', 'text'),
                SQLField('proposed_order_number', 'integer'),
                )
db.rules.title.requires = IS_NOT_EMPTY()
db.rules.user_id.requires = IS_NOT_EMPTY()
db.rules.user_id.requires=IS_IN_DB(db,"auth_user.id","auth_user.name")
#db.rules.user_id.requires=IS_IN_DB(db,'auth_user.id','%(name)s')
db.rules.description.requires = IS_NOT_EMPTY()
#db.rules.represent = lambda row: P("# " + str(row.id) + " ", A(row.title, _href = t2.action('view', [row.id])))
