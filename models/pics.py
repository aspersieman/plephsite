import datetime
now = datetime.datetime.today()

try:
    logged_in_user_id = auth.user.id
    logged_in_user_name = auth.user.firstname
except:
    logged_in_user_id = None
    logged_in_user_name = None
db.define_table('image',
   SQLField('title'),
   SQLField('addeddate', 'datetime',default = now),
   SQLField('user_id', db.auth_user, default = logged_in_user_id),
   SQLField('first_name', default = logged_in_user_name),
   SQLField('filename', 'upload', uploadfield = 'data'),
   SQLField('data','blob',default = ''))    
   
db.image.title.requires = IS_NOT_EMPTY()
db.image.addeddate.requires = IS_NOT_EMPTY()
db.image.user_id.requires = IS_NOT_EMPTY()
db.image.user_id.requires = IS_IN_DB(db, db.auth_user.id, "%(first_name)s")
#db.image.represent = lambda row: ("(" + str(row.id) + ")   ", A(row.title, _href = 'view/' + [row.id])))
