import datetime
now=datetime.datetime.today()

try:
    logged_in_user_id = auth.user.id
    logged_in_user_name = auth.user.firstname
except:
    logged_in_user_id = None
    logged_in_user_name = None
db.define_table('news',
    SQLField('title', length=64),
    SQLField('user_id', db.auth_user, default = logged_in_user_id),
    SQLField('first_name', default = logged_in_user_name),
    SQLField('addeddate', 'datetime',default=now),
    SQLField('post', 'text'),
    )

db.news.title.requires = IS_NOT_EMPTY()
db.news.user_id.requires = IS_NOT_EMPTY()
db.news.user_id.requires = IS_IN_DB(db, db.auth_user.id ,"%(first_name)s")
db.news.post.requires = IS_NOT_EMPTY()
