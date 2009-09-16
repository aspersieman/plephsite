#!/usr/bin/python
# -*- coding: utf-8 -*-
# settings
response.title = "Pleph"
response.subtitle = request.controller
response.author = "aspersieman"

response.sidebar = []

response.menu=[
                ["home",False,"/"],
                ["pics",False, "/init/pics/index"],
                ["blog", False, "/init/blog/index"],
                ["rules",False, "/init/rules/index"],
                ["wiki",False, "/t3"]
              ]

def register():
    form = FORM()
    #return dict(form = auth.register())
    response.flash = "Registration disabled!"
    return dict(form = form)

def login(): 
    return dict(form = auth.login())

def logout():
    auth.logout(next = "login")

@auth.requires_login()
def profile():
    return dict(form=auth.profile())

def error(): 
    auth.redirect("index",flash = "Not authorized to edit or comment.")

@auth.requires_login()
def index():
    #form = auth.create(db.rules)
    form = SQLFORM(db.rules, fields = ["title", "description", "proposed_order_number"])
    if form.accepts(request.vars, session):
        response.flash = "New rule created"

    itemize = auth.itemize(db.rules)
    return dict(form = form,rules = itemize)

@auth.requires_login()
def edit():
    form = auth.update(db.rules, next = "index")
    #form = SQLFORM(db.rules, fields = ["title", "description", "proposed_order_number"])
    #if form.accepts(request.vars, session):
    #    response.flash = "Rule updated"
    return dict(form=form)

@auth.requires_login()
def download():
    return auth.download()

@auth.requires_login()
def view():
    rules = auth.display(db.rules)
    return dict(rules = rules)

@auth.requires_login()
def search():
    search = auth.search(db.rules)
    return dict(search = search)

def rulesrss():
    rules = db(db.rules.id).select()
    return dict(rules = rules)

@auth.requires_login()
def rss():
    import datetime
    import gluon.contrib.rss2 as rss2
    import gluon.contrib.feedparser as feedparser
    url = "http://127.0.0.1:8000/"

    #entry = db().select(db.rules.id, db.rules.title, db.rules.description, orderby=~db.rules.addeddate)
    entries = db(db.rules.title <> "")
    entry = entries.select(
        db.rules.id,
        db.rules.title,
        db.rules.description,
        orderby=~db.rules.addeddate)

    d = feedparser.parse(XML(entry))
    rss = rss2.RSS2(title="Plephi - Rules",
       link = url,
       description = "We make the rules!",
       lastBuildDate = datetime.datetime.now(),
       items = [
          rss2.RSSItem(
            title = entry.title,
              link = url + "init/rules/view/" + str(entry.id),
            description = entry.rules.description,
            # guid = rss2.Guid('unkown'),
            pubDate = datetime.datetime.now()) for entry in d.entries]
       )
    response.headers['Content-Type']='application/rss+xml'
    return rss2.dumps(rss)
