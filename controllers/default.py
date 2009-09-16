#!/usr/bin/python
# -*- coding: utf-8 -*-
response.title= "Pleph"
response.subtitle= "home"
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

def user():
    return dict(form = auth())

def action():
    return dict(form = crud())

def error(): 
    auth.redirect("index",flash = "Not Authorised to edit or comment.")

def newsposts():
    news = db().select(
        db.news.ALL,
        orderby =~ db.news.addeddate, limitby = (0, 10))
    #r=db().select(db.cas_user.ALL,orderby=~db.cas_user.first_name)
    """
    if news_numcomments:
        if len(news_numcomments) > 0:
            response.sidebar.append(["Most Commented On", False, ""])
            for news in news_numcomments:
                response.sidebar.append([news.title + " (" + str(news.numcomments) + ")", False, "/" + request.application + "/plephblog/shownews/" + str(news.id)])
    allcomments = db((db.auth_comment.record_id = db.news.id) & (db.auth_comment.table_name == "news"))
    comments = allcomments.select(
        db.news.id,
        db.news.title,
        db.news.author,
        db.news.addeddate,
        db.news.post,
        db.auth_person.name,
        orderby=~db.news.addeddate)
    if comments:
        if len(comments) > 0:
            response.sidebar.append(["Recent Comments", False, ""])
            for comment in comments:
                response.sidebar.append([comment.blogcomments.author + " on " + comment.news.title + "", False, "/" + request.application + "/plephblog/shownews/" + str(comment.blogcomments.news_id) + "#Reader_Comments"])
    """
    news_numcomments = 0
    return dict(news = news, news_numcomments = news_numcomments)

def index():
    response.pageinfo = "<h1>News</h1>"
    return newsposts()

def read():
    news = db(db.news.id == request.args[0]).select(
        db.news.id,
        db.news.title,
        db.news.user_id,
        db.news.addeddate,
        db.news.post,
        db.news.first_name)
    return dict(news = news)

@auth.requires_login()
def create():
    #if response.admin == True:
    myd = newsposts()
    form=SQLFORM(db.news, fields = ["title","post"])
    if form.accepts(request.vars,session):
        response.flash="New news inserted"
        redirect("/" + request.application + "/default/index")

    myd["form"] = form
    return (myd)
    #else: redirect("/" + request.application + "/default/login")

@auth.requires_login()
def update():
    news = auth.update(db.news, next = "index")
    return dict(news = news)

def generatebloginfoframe():
    """
    blogposts_numcomments = {}
    blogposts = db(db.blogposts.id).select(
        db.blogposts.id,
        db.blogposts.title,
        db.blogposts.user_id,
        db.blogposts.addeddate,
        db.blogposts.post,
        db.blogposts.first_name,
        orderby=~db.blogposts.addeddate)

    recentblogposts = db().select(
        db.blogposts.id,
        db.blogposts.title,
        db.blogposts.addeddate,
        limitby = (0, 10),
        orderby=~db.blogposts.addeddate)
    sidebarheaderpresent = True
    for rb in recentblogposts:
        if sidebarheaderpresent:
            response.bloginfo.append(["Recent blogposts", A(rb.title + " [" + str(rb.addeddate)[:10] + "]", _href = "/init/blog/read/" + str(rb.id))])
            sidebarheaderpresent = False
        else:
            response.bloginfo.append(["", A(rb.title + " [" + str(rb.addeddate)[:10] + "]", _href = "/init/blog/read/" + str(rb.id))])
    """
    """
    for blogpost in blogposts:
        blogposts_numcomments[blogpost.id] = len(db((db.auth_comment.record_id == blogpost.id) & (db.auth_comment.table_name == "blogposts")).select()) or 0
    """
    """
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
            response.bloginfo.append(["Most commented on", HTML(A(blogpost.title, _href = "/init/blog/read/" + str(blogpost.id)), " ", A("(" + str(highest) + ")", _href = "/init/blog/read/" + str(blogpost.id) + "#comments"))])
    """
    """
    comments = db((db.auth_comment.record_id == db.blogposts.id) & (db.auth_comment.created_by == db.auth_person.id) & (db.auth_comment.table_name == "blogposts")).select(
        db.blogposts.id,
        db.blogposts.title,
        db.blogposts.addeddate,
        db.blogposts.post,
        db.auth_person.name,
        orderby=~db.blogposts.addeddate)
    """
    """
    comments = []
    """
    """
    recentcomments = db((db.auth_comment.record_id == db.blogposts.id) & (db.auth_comment.created_by == db.auth_person.id) & (db.auth_comment.table_name == "blogposts")).select(
        db.blogposts.id,
        db.blogposts.title,
        db.blogposts.addeddate,
        db.blogposts.post,
        db.auth_person.name,
        orderby=~db.blogposts.addeddate, limitby = (0, 5))
    """
    """
    recentcomments = ""
    if recentcomments:
        sidebarheaderpresent = True
        for comment in recentcomments:
            if sidebarheaderpresent:
                response.bloginfo.append(["Recent Comments", A(comment.auth_person.name + " on '" + comment.blogposts.title + "'", _href = "/init/blog/read/" + str(comment.blogposts.id) + "#comments")])
                sidebarheaderpresent = False
            else:
                response.bloginfo.append(["", A(comment.auth_person.name + " on " + comment.blogposts.title, _href = "/init/blog/read/" + str(comment.blogposts.id) + "#comments")])
    """
