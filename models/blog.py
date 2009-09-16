import datetime
now=datetime.datetime.today()

try:
    logged_in_user_id = auth.user.id
except:
    logged_in_user_id = None
db.define_table('blogposts',
                SQLField('title', length=64),
                SQLField('user_id', db.auth_user, default = logged_in_user_id),
                SQLField('addeddate', 'datetime',default=now),
                SQLField('post', 'text'),
                )

db.blogposts.title.requires = IS_NOT_EMPTY()
db.blogposts.user_id.requires = IS_NOT_EMPTY()
db.blogposts.post.requires = IS_NOT_EMPTY()
