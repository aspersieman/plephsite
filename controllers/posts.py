# coding: utf8

from applications.init.modules.markdown import WIKI

response.title = "Pleph - A blog about programming, comics, Thailand and wordsmithing"
response.subtitle = ""

def data():
    form = crud()
    categories = db(db.categories.title != "").select()
    return dict(form = form, categories = categories)

@auth.requires_membership('Admin')
def new():
    postform = SQLFORM(db.post)
    categorylist = db(db.categories.id > 0).select()
    categorycheckboxes = []
    for category in categorylist:
		categorycheckboxes.append(str(INPUT(_type = "checkbox", _name = "category", _value = category.id)) + category.title)
    postform[0].insert(-1, ("Categories: ", XML("".join(categorycheckboxes))))
    postform[0].insert(-1, ("Tags:", INPUT(_type="textbox", _name="tags", _size="64", _value="")))
    postform[0].insert(-1,
        (
            "",
            INPUT(_type = "button", _name = "preview", _value = "Preview", _onclick = "ajax('/init/posts/post_preview', ['post_body'], 'preview')"),
        )
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
    categorycheckboxes = []
    for category in categorylist:
        checked = "True" if int(category.id) in postcategories else ""
        if checked == "True":
            categorycheckboxes.append(str(INPUT(_type = "checkbox", _name = "category", _value = category.id, value = True)) + category.title)
        else:
            categorycheckboxes.append(str(INPUT(_type = "checkbox", _name = "category", _value = category.id)) + category.title)
    editform[0].insert(-1, ("Categories: ", XML("".join(categorycheckboxes))))
    editform[0].insert(-1, ("Tags:", INPUT(_type="textbox", _name="tags", _size="64", _value=", ".join(posttags))))
    editform[0].insert(-1,
        (
            "",
            INPUT(_type = "button", _name = "preview", _value = "Preview", _onclick = "ajax('/init/posts/post_preview', ['post_body'], 'preview')"),
        )
    )
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
    post = db((db.post.id == postid)).select()
    bpost_is_valid = True
    if len(post) == 0:
        bpost_is_valid = False
    elif post[0].private == True:
        bpost_is_valid = False
    if bpost_is_valid:
        if auth.has_membership('Admin'):
            html_edit_post_link = A("[Edit Post]", _href = URL(r = request, f = "edit", args = postid))
        else:
            html_edit_post_link = None
        post = post[0]
        response.title = "Pleph - " + str(post.title)
        relations = db(db.relations.post == postid).select()
        categories = dict((relation.category.id, relation.categorytitle) for relation in relations if relation.relationtype == 'category')
        tags = [relation.tag for relation in relations if relation.relationtype == 'tag']
        comments = db(db.comment.post == postid).select(orderby =~ db.comment.addeddate)
        db.comment.post.default = postid
        commentform = SQLFORM(db.comment)
        commentform[0].insert(-1, TR('',  Recaptcha(request, "6Lc2LgoAAAAAAL_Dkqubx50GS4gq2zlKg-PibzQ0", "6Lc2LgoAAAAAAKwJ3SD7B6KVsz195xTmIb9yh31K", error_message = "The text entered does not match.")))
        if commentform.accepts(request.vars, session):
            to = [mail.settings.sender]
            subject = "New comment on post: '" + str(post.title) + "'"
            message = "A new comment was posted to the blog at 'http://pleph.appspot.com'\r\rThe comment body:\r\r" + str(commentform.vars.commentbody) + "\r\r\rYou can view the comment here: http://pleph.appspot.com/" + str(request.application) + "/posts/view/" + str(postid) + "#Comments."
            mail.send(to = to, subject = subject, message = message)
            response.flash = "Comment posted succesfully."
            redirect(URL(r=request, f="view", args=postid))
        elif commentform.errors:
            response.flash = "There was an error saving your comment. Please try again."
    else:
        post = None
        relations = None
        categories = None
        tags = None
        commentform = None
        comments = None
    return dict(post=post, commentform = commentform, categories = categories, tags = tags, comments = comments, html_edit_post_link = html_edit_post_link)

def archive():
    MONTHS = {
        1: "January", 
        2: "February", 
        3: "March", 
        4: "April", 
        5: "May", 
        6: "June", 
        7: "July", 
        8: "August", 
        9: "September", 
        10: "October", 
        11: "November", 
        12: "December"}
    import datetime
    from dateutil.relativedelta import relativedelta
    year = int(request.args(0))
    month = int(request.args(1))
    thismonthdate = datetime.datetime(year, month, 1)
    if month < 12:
        followingmonthdate = thismonthdate + relativedelta(month =+ (month + 1))
    else:
        followingmonthdate = datetime.datetime(year + 1, 1, 1)
    posts = db((db.post.private == False) & (db.post.addeddate >= thismonthdate) & (db.post.addeddate < followingmonthdate)).select(orderby=db.post.addeddate)
    categories = {}
    tags = {}
    comments = {}
    for post in posts:
        relations = db(db.relations.post == post.id).select()
        categories[post.id] = dict((relation.category.id, relation.categorytitle) for relation in relations if relation.relationtype == 'category')
        tags[post.id] = [relation.tag for relation in relations if relation.relationtype == 'tag']
        comments[post.id] = db(db.comment.post == post.id).count()
    return dict(posts=posts, categories = categories, tags = tags, year = year, monthname = MONTHS[int(month)], comments = comments)

@auth.requires_membership('Admin')
def manageposts():
    if not request.vars.delete is None:
        deleteposts(request.vars.delete)
        redirect(URL(r=request, f="manageposts"))
    posts = db(db.post.id > 0).select(orderby=~db.post.addeddate)
    return dict(posts=posts)

@auth.requires_membership('Admin')
def deleteposts(posts_delete = None):
    if isinstance(posts_delete, str):
        posts_delete = [posts_delete]
    for postid in posts_delete:
        if postid > 0:
            db(db.post.id == int(postid)).delete()
            db(db.comment.post == int(postid)).delete()
            db(db.relations.post == int(postid)).delete()

@auth.requires_membership('Admin')
def post_preview():
    return WIKI(request.vars.post_body, safe_mode = "safe").xml()
