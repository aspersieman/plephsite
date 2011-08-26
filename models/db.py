# coding: utf8

if request.env.web2py_runtime_gae:            
    db = DAL("gae")                          
    session.connect(request, response, db=db)
else:                                         
    db = DAL("sqlite://storage.sqlite")     

from gluon.tools import *

auth = Auth(globals(),db)                    
auth.settings.hmac_key = "sha512:2c209fe2-5c5a-4400-a98a-4e4d4cf04c9c"
auth.define_tables()                         
auth.settings.captcha = Recaptcha(request, "6Lc2LgoAAAAAAL_Dkqubx50GS4gq2zlKg-PibzQ0", "6Lc2LgoAAAAAAKwJ3SD7B6KVsz195xTmIb9yh31K", error_message = "Text does not match.")
crud = Crud(globals(),db)                    
service = Service(globals())                   

crud.settings.auth = auth 
mail = Mail()  
mail.settings.server = "gae"  
mail.settings.sender = "" 
mail.settings.login = ""
auth.settings.mailer = mail 
#auth.settings.registration_requires_verification = True
#auth.settings.registration_requires_approval = True
#auth.messages.verify_email = 'Click on the link http://.../user/verify_email/%(key)s to verify your email'

db.define_table("post",
    Field("user", db.auth_user, readable=False, writable=False),
    Field("username"),
    Field("private", "boolean", default = False),
    Field("title"),
    Field("body", "text"),
    Field("addeddate", "datetime", default=request.now, readable=False, writable=False),
    Field("file", "upload")
)

db.post.id.readable = False
db.post.id.writable = False
db.post.username.readable = False
db.post.username.writable = False

if auth.user:
    db.post.user.default = auth.user.id
    db.post.username.default = auth.user.first_name

db.define_table("comment",
    Field("post", db.post, readable=False, writable=False),
    Field("name", requires=IS_NOT_EMPTY(error_message="Please enter your name.")),
    Field("email"),
    Field("commentbody", "text", requires=IS_NOT_EMPTY(error_message="Please enter your comment.")),
    Field("addeddate", "datetime", default=request.now, readable=False, writable=False)
)

db.define_table("categories",
    Field("title", requires = IS_NOT_EMPTY(error_message = "Enter a title."))
)

db.categories.title.requires = IS_NOT_IN_DB(db, db.categories.title)

db.define_table("relations",
    Field("post", db.post),
    Field("category", db.categories),
    Field("categorytitle"),
    Field("tag"),
    Field("relationtype")
)

db.define_table("images",
    Field("title"),
    Field("filename", "upload"),
    Field("addeddate", "datetime", default=request.now, readable=False, writable=False)
)

db.images.title.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, db.images.title)]

# Initial setup
admin = db(db.auth_user.email == "aspersieman@gmail.com").select()
if admin:
    admingroup = db(db.auth_group.role == "Admin").select()
    if not admingroup:
        admingroup_id = auth.add_group(role = "Admin", description = "Administrator group.")
    else:
        admingroup_id = admingroup[0].id

    admingroup_membership = db((db.auth_membership.user_id == admin[0].id)&(db.auth_membership.group_id == admingroup_id)).select()
    if not admingroup_membership:
        auth.add_membership(admingroup_id, admin[0].id)
    adminpermission_categories = db((db.auth_permission.group_id == admingroup_id)&(db.auth_permission.table_name == "categories")).select(db.auth_permission.id)
    if not adminpermission_categories:
        auth.add_permission(admingroup_id, "create", "categories")
    adminpermission_images = db((db.auth_permission.group_id == admingroup_id)&(db.auth_permission.table_name == "images")).select(db.auth_permission.id)
    if not adminpermission_images:
        auth.add_permission(admingroup_id, "create", "images")
