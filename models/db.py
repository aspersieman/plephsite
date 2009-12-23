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
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = True
auth.messages.verify_email = 'Click on the link http://.../user/verify_email/%(key)s to verify your email'

db.define_table('post',
    Field('user', db.auth_user, readable=False, writable=False),
    Field('username'),
    Field('private', "boolean", default = False),
    Field('title'),
    Field('body', 'text'),
    Field('dateline', 'datetime', default=request.now, readable=False, writable=False),
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
    Field('dateline', 'datetime', default=request.now, readable=False, writable=False)
)

db.define_table('category',
    Field('title')
)

db.define_table('relations',
    Field('post', db.post),
    Field('category', db.category),
    Field('tag'),
    Field('relationtype')
)
