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
mail.settings.login='username:password'
auth.settings.mailer=mail 
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = True
auth.messages.verify_email = 'Click on the link http://.../user/verify_email/%(key)s to verify your email'
