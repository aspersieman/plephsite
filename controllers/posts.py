# coding: utf8

from gluon.contrib.markdown import WIKI

response.title = "Pleph"
response.subtitle = "Exuding awesomage - NOW WITH MORE LLAMAS!"

def data():
    form = crud()
    categories = db(db.categories.title != "").select()
    return dict(form = form, categories = categories)

@auth.requires_membership('Admin')
def new():
    postform = SQLFORM(db.post)
    categorylist = db(db.categories.id > 0).select()
    for category in categorylist:
        postform[0].append(XML(str(INPUT(_type="checkbox", _name="category", _value=category.id))+category.title))
    postform[0].append(
        DIV(
            "Tags:", 
            INPUT(_type="textbox", _name="tags", _size="50")
        )
    )
    postform[0].append(
        DIV(
            INPUT(_type = "button", _name = "preview", _value = "Preview", _onclick = "ajax('post_preview', ['post_body'], 'preview')"))
    )
    if postform.accepts(request.vars, session):
        if 'category' in request.vars:
            if isinstance(request.vars.category, list):
                postedcategories = [postedcategory for postedcategory in request.vars.category]
            else:
                postedcategories = [request.vars.category]
            for postedcategory in postedcategories:
                category_title = db(db.categories.id == postedcategory).select()[0]
                db.relations.insert(post = postform.vars.id, category = postedcategory, relationtype='category', categorytitle = category_title["title"])
        if 'tags' in request.vars:
            for tag in request.vars.tags.split(", "):
                db.relations.insert(post=postform.vars.id, tag=tag, relationtype='tag')
        redirect(URL(r=request, f="view", args=postform.vars.id))
    return dict(postform=postform)

@auth.requires_membership('Admin')
def edit():
    postid = int(request.args(0))
    post = db(db.post.id == postid).select()[0]
    relations = db(db.relations.post == postid).select() #post.relations.select()
    postcategories = [int(relation.category) for relation in relations if relation.relationtype == 'category']
    posttags = [relation.tag for relation in relations if relation.relationtype == 'tag']
    editform = SQLFORM(db.post, post, deletable=True)
    categorylist = db(db.categories.id > 0).select()
    for category in categorylist:
        checked = "on" if int(category.id) in postcategories else ""
        editform[0].append(XML(str(INPUT(_type="checkbox", _name="category", _value=category.id, value=checked))+category.title))
    editform[0].append(
        DIV(
            INPUT(_type = "button", _name = "preview", _value = "Preview", _onclick = "ajax('/init/posts/post_preview', ['post_body'], 'preview')"))
    )
    editform[0].append(DIV(XML("<strong>Tags:</strong>"), INPUT(_type="textbox", _name="tags", _size="50", _value=", ".join(posttags), _style="margin-left: 100px;")))
    if editform.accepts(request.vars, session):
        if 'category' in request.vars:
            if isinstance(request.vars.category, list):
                postedcategories = [postedcategory for postedcategory in request.vars.category]
            else:
                postedcategories = [request.vars.category]
            for postedcategory in postedcategories:
                if int(postedcategory) not in postcategories:
                    category_title = db(db.categories.id == postedcategory).select(db.categories.title)[0]
                    db.relations.insert(post=postid, category=postedcategory, relationtype='category', categorytitle = category_title["title"])
            for postcategory in postcategories:
                if str(postcategory) not in postedcategories:
                    db((db.relations.category == postcategory)&(db.relations.post == postid)).delete()
        if 'tags' in request.vars:
            for tag in request.vars.tags.split(", "):
                if tag not in posttags:
                    db.relations.insert(post=postid, tag=tag, relationtype='tag')
            for posttag in posttags:
                if posttag not in request.vars.tags.split(", "):
                    db((db.relations.post == postid)&(db.relations.tag == posttag)).delete()
        redirect(URL(r=request, f="view", args=postid))
    return dict(editform=editform, post=post, posttags=posttags)

def view():
    postid = request.args(0)
    post = db((db.post.id == postid)&(db.post.private == False)).select()
    if len(post) > 0:
        post = post[0]
        relations = db(db.relations.post == postid).select()
        categories = dict((relation.category.id, relation.categorytitle) for relation in relations if relation.relationtype == 'category')
        tags = [relation.tag for relation in relations if relation.relationtype == 'tag']
        comments = db(db.comment.post == postid).select()
        db.comment.post.default = postid
        if auth.is_logged_in():
            commentform = SQLFORM(db.comment)
            commentform[0].insert(-1, TR('',  Recaptcha(request, "6Lc2LgoAAAAAAL_Dkqubx50GS4gq2zlKg-PibzQ0", "6Lc2LgoAAAAAAKwJ3SD7B6KVsz195xTmIb9yh31K", error_message = "The text entered does not match.")))
        else:
            commentform = FORM()
        if commentform.accepts(request.vars, session):
            redirect(URL(r=request, f="view", args=postid))
    else:
        post = None
        relations = None
        categories = None
        tags = None
        commentform = None
        comments = None
    return dict(post=post, commentform = commentform, categories = categories, tags = tags, comments = comments)

@auth.requires_membership('Admin')
def manageposts():
    posts = db(db.post.id > 0).select()
    return dict(posts=posts)

@auth.requires_membership('Admin')
def deleteposts():
    for postid in request.vars.delete:
        db(db.post.id == int(postid)).delete()
        db(db.comment.post == int(postid)).delete()
        db(db.relations.post == int(postid)).delete()
    redirect(URL(r=request, f="manageposts"))

@auth.requires_membership('Admin')
def post_preview():
    return WIKI(request.vars.post_body).xml()
