# coding: utf8

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = request.application
response.subtitle = T('Llamas, eels and destruction...')

##########################################
## this is the authentication menu
## remove if not necessary
##########################################

if 'auth' in globals():
    if not auth.is_logged_in():
       response.menu_auth = [
           [T('Login'), False, auth.settings.login_url,
            [
                   [T('Register'), False,
                    URL(request.application,'default','user/register')],
                   [T('Lost Password'), False,
                    URL(request.application,'default','user/retrieve_password')]]
            ],
           ]
    else:
        response.menu_auth = [
            ['Hi ' + auth.user.first_name + '!', False,None,
             [
                    [T('Logout'), False, 
                     URL(request.application,'default','user/logout')],
                    [T('Profile'), False, 
                     URL(request.application,'default','user/profile')],
                    [T('Password'), False,
                     URL(request.application,'default','user/change_password')]]
             ],
            ]
    if auth.has_membership(auth.id_group("Admin")):
        response.menu_post = [
            ['Posts', False, URL(request.application, 'default', 'index'),
                [
                    ['New Post', False, URL(request.application, 'posts', 'new')],
                    ['Manage Posts', False, URL(request.application, 'posts', 'manageposts')],
                    ['Manage Files', False, URL(request.application, 'posts', 'managefiles')]
                ],
            ],
        ]

##########################################
## this is the main application menu
## add/remove items as required
##########################################

response.menu = [
    [T('Index'), False, 
     URL(request.application,'default','index'), []],
    ]


##########################################
## this is here to provide shortcuts
## during development. remove in production 
##########################################

response.menu_edit=[
  [T('Edit'), False, URL('admin', 'default', 'design/%s' % request.application),
   [
            [T('Controller'), False, 
             URL('admin', 'default', 'edit/%s/controllers/default.py' \
                     % request.application)],
            [T('View'), False, 
             URL('admin', 'default', 'edit/%s/views/%s' \
                     % (request.application,response.view))],
            [T('Layout'), False, 
             URL('admin', 'default', 'edit/%s/views/layout.html' \
                     % request.application)],
            [T('Stylesheet'), False, 
             URL('admin', 'default', 'edit/%s/static/base.css' \
                     % request.application)],
            [T('DB Model'), False, 
             URL('admin', 'default', 'edit/%s/models/db.py' \
                     % request.application)],
            [T('Menu Model'), False, 
             URL('admin', 'default', 'edit/%s/models/menu.py' \
                     % request.application)],
            [T('Database'), False, 
             URL(request.application, 'appadmin', 'index')],
            ]
   ],
  ]
