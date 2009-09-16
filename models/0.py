#!/usr/bin/python
# -*- coding: utf-8 -*-
try:
    from gluon.contrib.gql import *
    db=GQLDB()
    platform = "GAE"
except:
    db=SQLDB("sqlite://db.db")
session.connect(request, response, db=db)

from gluon.tools import Mail, Auth, Recaptcha, Crud
mail = Mail()
mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'aspersieman@gmail.com'
mail.settings.login = 'aspersieman:H0ndt44s'
auth = Auth(globals(), db)
auth.settings.mailer = mail
auth.define_tables()
# auth.settings.captcha = Recaptcha(request, public_key = 'RECAPTCHA_PUBLIC_KEY',private_key='RECAPTCHA_PRIVATE_KEY')
# auth.settings.on_failed_authorization = redirect("/init/default/user/login")
crud = Crud(globals(),db)
# crud.settings.auth = auth

response.menu_edit=[
  ['Edit', False, URL('admin', 'default', 'design/%s' % request.application),
   [
            ['Controller', False, 
             URL('admin', 'default', 'edit/%s/controllers/default.py' \
                     % request.application)],
            ['View', False, 
             URL('admin', 'default', 'edit/%s/views/%s' \
                     % (request.application,response.view))],
            ['Layout', False, 
             URL('admin', 'default', 'edit/%s/views/layout.html' \
                     % request.application)],
            ['Stylesheet', False, 
             URL('admin', 'default', 'edit/%s/static/base.css' \
                     % request.application)],
            ['DB Model', False, 
             URL('admin', 'default', 'edit/%s/models/db.py' \
                     % request.application)],
            ['Menu Model', False, 
             URL('admin', 'default', 'edit/%s/models/menu.py' \
                     % request.application)],
            ['Database', False, 
             URL(request.application, 'appadmin', 'index')],
            ]
   ],
  ]

#####################################################################################
# Setup Root user : aspersieman@gmail.com                                           #
# Add aspersieman to the 'administrator' group                                      #
# create the group if not exists                                                    #
#####################################################################################
admin_email = None
try:
    admin_email = auth.user.email
except:
    admin_email = None

admin_role_id = db((db.auth_group.role == "Administrator")).select(db.auth_group.id)
try:
    admin_role_id = admin_role_id[0]["id"]
except:
    admin_role_id = None
if not admin_role_id:
    admin_role_id = auth.add_group("Administrator","Root - Administrator")

if admin_email == "aspersieman@gmail.com":
    if not auth.has_membership(admin_role_id):
        auth.add_membership(admin_role_id, auth.user.id)
