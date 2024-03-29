# coding: utf8
# vim:set filetype=python.web2py:

response.title = "Pleph - A blog about programming, comics, Thailand and wordsmithing"
response.subtitle = ""

def view():
    categoryid = request.args(0) or 0
    try:
        category = db(db.categories.id == categoryid).select()[0]
        categoryposts = db((db.relations.category == categoryid)).select(orderby =~ db.relations.post)
    except:
        category = None
        categoryposts = []
    posttitles = {}
    postinfo = {}
    postexcerpts = {}
    posttags = None
    categories = {}
    comments = {}
    for categorypost in categoryposts:
        post = db(db.post.id == categorypost.post).select(db.post.title, db.post.excerpt, db.post.id, db.post.username, db.post.addeddate)[0]
        posttitles[post.id] = post.title
        relations = db(db.relations.post == post.id).select()
        categories[post.id] = dict((relation.category.id, relation.categorytitle) for relation in relations if relation.relationtype == 'category')
        postexcerpts[post.id] = post.excerpt or ""
        posttags = db((db.relations.post == post.id) & (db.relations.tag != None)).select(db.relations.tag)
        postinfo[post.id] = "Posted by <strong>" + post.username + "</strong> on <strong>" + str(post.addeddate)[:10] + "</strong>"
        comments[post.id] = db(db.comment.post == post.id).count()
    return dict(categoryposts = categoryposts, category = category, posttitles = posttitles, postinfo = postinfo, postexcerpts = postexcerpts, posttags = posttags, categories = categories, comments = comments)
