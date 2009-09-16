#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

# settings
response.title= "Pleph"
response.subtitle= request.controller
response.author="aspersieman"

response.menu=[
                ["home",False,"/"],
                ["pics",False, "/init/pics/index"],
                ["blog", False, "/init/blog/index"],
                ["rules",False, "/init/rules/index"],
                ["wiki",False, "/t3"]
              ]

response.sidebar = []
response.submenus = {}
if auth.has_membership(auth.id_group("Administrator")):
    response.submenus["blog"] = [A("Create a new post", _href="/init/blog/create")]

def error(): 
    auth.redirect("index",flash = "Not authorized to edit or comment.")

def view():
    blogpost = db(db.blogposts.id == request.args[0]).select(
        db.blogposts.id,
        db.blogposts.title,
        db.blogposts.user_id,
        db.blogposts.addeddate,
        db.blogposts.post,
        db.blogposts.first_name)
    return dict(blogpost = blogpost)

def index():
    response.pageinfo = "A blog that smells like an asparagus, a sausage and a llama...glorious."
    blogposts = db(db.blogposts.id).select(
        db.blogposts.id,
        db.blogposts.title,
        db.blogposts.user_id,
        db.blogposts.addeddate,
        db.blogposts.post,
        orderby=~db.blogposts.addeddate)
    """
    blogposts_numcomments = {}
    for blogpost in blogposts:
        blogposts_numcomments[blogpost.id] = len(db((db.auth_comment.record_id == blogpost.id) & (db.auth_comment.table_name == "blogposts")).select()) or 0
    hascomments = False
    highest = 0
    highestkey = ""
    for k, v in blogposts_numcomments.items():
        if v > highest:
            highest = v
            highestkey = k
            hascomments = True
    if hascomments:
        mostcommentedon = db(db.blogposts.id == int(highestkey)).select()
        for blogpost in mostcommentedon:
            response.sidebar.append(["Most commented on", HTML(A(blogpost.title, _href = "/init/blog/view/" + str(blogpost.id)), " ", A("(" + str(highest) + ")", _href = "/init/blog/view/" + str(blogpost.id) + "#comments"))])
    comments = db((db.auth_comment.record_id == db.blogposts.id) & (db.auth_comment.created_by == db.auth_user.id) & (db.auth_comment.table_name == "blogposts")).select(
        db.blogposts.id,
        db.blogposts.title,
        db.blogposts.addeddate,
        db.blogposts.post,
        db.auth_user.first_name,
        orderby=~db.blogposts.addeddate)
    recentcomments = db((db.auth_comment.record_id == db.blogposts.id) & (db.auth_comment.created_by == db.auth_user.id) & (db.auth_comment.table_name == "blogposts")).select(
        db.blogposts.id,
        db.blogposts.title,
        db.blogposts.addeddate,
        db.blogposts.post,
        db.auth_user.first_name,
        orderby=~db.blogposts.addeddate, limitby = (0, 5))
    if recentcomments:
        sidebarheaderpresent = True
        for comment in recentcomments:
            if sidebarheaderpresent:
                response.sidebar.append(["Recent Comments", A(comment.auth_user.first_name + " on '" + comment.blogposts.title + "'", _href = "/init/blog/view/" + str(comment.blogposts.id) + "#comments")])
                sidebarheaderpresent = False
            else:
                response.sidebar.append(["", A(comment.auth_user.first_name + " on " + comment.blogposts.title, _href = "/init/blog/view/" + str(comment.blogposts.id) + "#comments")])
    """
    return dict(blogposts = blogposts)

@auth.requires_login()
def create():
    if response.admin == True:
        blogposts = db(db.blogposts.id).select(
            db.blogposts.id,
            db.blogposts.title,
            db.blogposts.user_id,
            db.blogposts.addeddate,
            db.blogposts.post,
            db.blogposts.first_name,
            orderby=~db.blogposts.addeddate)
        form=SQLFORM(db.blogposts,fields=["title","post"])
        if form.accepts(request.vars,session):
            response.flash="New blogpost inserted"
            redirect("/" + request.application + "/blog/index")
        return dict(form = form, blogposts = blogposts)
    else: redirect("/" + request.application + "/blog/login")

@auth.requires_login()
def update():
    blogpost = auth.update(db.blogposts, next = "index")
    return dict(blogpost = blogpost)

def sortedDictValues(adict):
    items = adict.items()
    items.sort()
    return [value for key, value in items]

def sortbyvalue(dict):
    """ Return a list of (key, value) pairs, sorted by value. """
    mdict = map(_swap2, dict.items())
    mdict.sort()
    mdict = map(_swap2, mdict)
    return mdict
