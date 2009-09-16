#!/usr/bin/python
# -*- coding: utf-8 -*-

# settings
response.title= "Pleph"
response.subtitle= request.controller
response.author= "aspersieman"

response.menu=[
                ["home",False,"/"],
                ["pics",False, "/init/pics/index"],
                ["blog", False, "/init/blog/index"],
                ["rules",False, "/init/rules/index"],
                ["wiki",False, "/t3"]
              ]

response.sidebar = [
                ]

def user():
    return dict(form = auth())

def action():
    return dict(form = crud())

def download():
    return response.download(request, db)

def index():
    if auth.is_logged_in():
        form = SQLFORM(db.image, fields = ["title", "filename"])
        if form.accepts(request.vars, session):
            response.flash = "Image inserted"
    else:   
        form = []
    #images = db(left = db.image.on(db.image.user_id == db.auth_user.id)).select(limitby = 10)
    images = db().select(
        db.image.ALL,
        limitby = (0, 10),
        orderby =~ db.image.addeddate)
    return dict(form = form,images = images)
