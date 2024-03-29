# coding: utf8

response.title = "Pleph - A blog about programming, comics, Thailand and wordsmithing"
response.subtitle = ""

def index():
    posts = db(db.post.private == False).select(orderby=~db.post.addeddate, limitby = (0, 5))
    categories = {}
    tags = {}
    comments = {}
    for post in posts:
        relations = db(db.relations.post == post.id).select()
        categories[post.id] = dict((relation.category.id, relation.categorytitle) for relation in relations if relation.relationtype == 'category')
        tags[post.id] = [relation.tag for relation in relations if relation.relationtype == 'tag']
        comments[post.id] = db(db.comment.post == post.id).count()
    return dict(posts=posts, categories = categories, tags = tags, comments = comments)

def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()

def dbadmin():
    redirect("https://" + request.env.http_host + "/" + request.application + "/appadmin")
