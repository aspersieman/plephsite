# coding: utf8

import gluon.contrib.markdown

@service.rss
def posts():
    posts = db(db.post.private == False).select(limitby = (0, 10), orderby =~ db.post.addeddate)
    urlbase = request.env.wsgi_url_scheme + "://" + request.env.http_host
    items = []
    for post in posts:
        desc = str(XML(gluon.contrib.markdown.WIKI(post.body[0:500]))) + "..." + str(A(" [more]", _href = urlbase + URL(request.application, c = "posts", f = "view", args = post.id))) if len(post.body) > 0 else XML(gluon.contrib.markdown.WIKI(post.body))
        items.append(
            dict(
                title = post.title,
                pubDate = post.addeddate,
                link = urlbase + URL(request.application, c = "posts", f = "view", args = post.id), 
                description = desc
            )
        )
    return dict(
        title= "Pleph",
        link = urlbase + URL(request.application, c = "default", f = "index"), 
        description = "Exuding awesomage - NOW WITH MORE LLAMAS!",
        items = items
    )
