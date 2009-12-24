# coding: utf8

if request.env.web2py_runtime_gae:            
    db = DAL('gae')                          
    session.connect(request, response, db=db)
else:                                         
    db = DAL('sqlite://storage.sqlite')     

from gluon.tools import *
auth=Auth(globals(),db)                    
auth.settings.hmac_key='sha512:2c209fe2-5c5a-4400-a98a-4e4d4cf04c9c'
auth.define_tables()                         
crud=Crud(globals(),db)                    
service=Service(globals())                   

crud.settings.auth=auth 
mail=Mail()  
mail.settings.server='smtp.gmail.com:587'  
mail.settings.sender='aspersieman@gmail.com' 
mail.settings.login='aspersieman:H0ndt44s'
auth.settings.mailer=mail 
#auth.settings.registration_requires_verification = True
#auth.settings.registration_requires_approval = True
#auth.messages.verify_email = 'Click on the link http://.../user/verify_email/%(key)s to verify your email'

db.define_table('post',
    Field('user', db.auth_user, readable=False, writable=False),
    Field('username'),
    Field('private', "boolean", default = False),
    Field('title'),
    Field('body', 'text'),
    Field('addeddate', 'datetime', default=request.now, readable=False, writable=False),
    Field('file', 'upload')
)

db.post.id.readable = False
db.post.id.writable = False
db.post.username.readable = False
db.post.username.writable = False

if auth.user:
    db.post.user.default = auth.user.id
    db.post.username.default = auth.user.first_name

db.define_table('comment',
    Field('post', db.post, readable=False, writable=False),
    Field('name', requires=IS_NOT_EMPTY(error_message="Please enter your name.")),
    Field('email'),
    Field('commentbody', 'text', requires=IS_NOT_EMPTY(error_message="Please enter your comment.")),
    Field('addeddate', 'datetime', default=request.now, readable=False, writable=False)
)

db.define_table('categories',
    Field('title', requires = IS_NOT_EMPTY(error_message = "Enter a title."))
)

db.categories.title.requires = IS_NOT_IN_DB(db, db.categories.title)

db.define_table('relations',
    Field('post', db.post),
    Field('category', db.categories),
    Field('categorytitle'),
    Field('tag'),
    Field('relationtype')
)

db.define_table("images",
    Field("title"),
    Field("filename", "upload"),
    Field('addeddate', 'datetime', default=request.now, readable=False, writable=False)
)

db.images.title.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, db.images.title)]

# Initial setup
admingroup = db(db.auth_group.role == "Admin").select()
if admingroup:
    admin = db(db.auth_user.email == "aspersieman@gmail.com").select()
    if admin:
        auth.add_membership(admingroup[0].id, admin[0].id)
        auth.add_permission(admingroup[0].id, 'create', 'categories')
        auth.add_permission(admingroup[0].id, 'create', 'images')
else:
    admingroup_id = auth.add_group(role = "Admin", description = "Administrator group.")
    admin = db(db.auth_user.email == "aspersieman@gmail.com").select()
    if admin:
        auth.add_membership(admingroup_id, admin[0].id)
        auth.add_permission(admingroup_id, 'create', 'categories')
        auth.add_permission(admingroup_id, 'create', 'images')
