# coding: utf8

response.title = "Pleph"
response.subtitle = "Exuding awesomage - NOW WITH MORE LLAMAS!"

def view():
    categoryid = request.args(0)
    category = db(db.categories.id == categoryid).select()[0]
    categoryposts = db((db.relations.category == categoryid)).select(orderby =~ db.relations.post)
    posttitles = {}
    postinfo = {}
    for categorypost in categoryposts:
        post = db(db.post.id == categorypost.post).select(db.post.title, db.post.id, db.post.username, db.post.addeddate)[0]
        posttitles[post.id] = post.title
        postinfo[post.id] = "Posted by " + post.username + " on " + str(post.addeddate)
    relations = db((db.relations.category == categoryid)).select(db.relations.post, db.relations.id)
    relationlist = []
    for relation in relations:
        relationlist.append(relation.id)
    return dict(categoryposts=categoryposts, category=category, posttitles = posttitles, postinfo = postinfo)
