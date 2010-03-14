# coding: utf8

response.title = request.application
response.subtitle = T('Llamas, eels and destruction...')

if 'auth' in globals():
    if not auth.is_logged_in():
        """
        response.menu_auth = [
           [T('Login'), False, auth.settings.login_url,
            [
                   [T('Register'), False,
                    URL(request.application,'default','user/register')],
                   [T('Lost Password'), False,
                    URL(request.application,'default','user/retrieve_password')]]
            ],
           ]
        """
        response.menu_auth = [
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
            ['Posts', False, URL(request.application, 'default', 'index'),
                [
                    ['New Post', False, URL(request.application, 'posts', 'new')],
                    ['Manage Posts', False, URL(request.application, 'posts', 'manageposts')],
                    ['Manage Images', False, URL(request.application, 'images', 'index')],
                    ['Manage Categories', False, URL(request.application, 'posts', 'data/create/categories')],
                    ['Manage DB', False, URL(request.application, 'appadmin', "index")]
                ],
            ],
        ]
    else:
        response.menu_post = [
            ['Posts', False, URL(request.application, 'default', 'index'),
                [
                ],
            ],
        ]
