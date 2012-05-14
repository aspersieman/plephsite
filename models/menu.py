# coding: utf8

response.title = request.application
response.subtitle = T('Llamas, eels and destruction...')

if 'auth' in globals():
    response.menu_about = [
        ['About This Site', False, URL(request.application, 'about', 'index'),
            [
            ],
        ],
    ]
    if not auth.is_logged_in():
        response.menu_login = [
            [T('Login'), False, auth.settings.login_url,
             [],
            ]
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
            ['Home', False, URL(request.application, 'default', 'index'),
                [
                    ['New Post', False, URL(request.application, 'posts', 'new')],
                    ['Manage Posts', False, URL(request.application, 'posts', 'manageposts')],
                    ['Manage Images', False, URL(request.application, 'images', 'index')],
                    ['Manage Categories', False, URL(request.application, 'posts', 'data/create/categories')],
                    ['Manage DB', False, URL(request.application, "default", "dbadmin")]
                ],
            ],
        ]
