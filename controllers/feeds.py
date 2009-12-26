# coding: utf8

@service.rss
def posts():
    posts = db(db.post.id > 0).select(limitby = (0, 10), orderby =~ db.post.addeddate)
    urlbase = request.env.wsgi_url_scheme + "://" + request.env.http_host
    items = []
    for post in posts:
        desc = (post.body[0:100] + "...") if len(post.body) > 0 else post.body
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
        description = "Llamas, Eels, Meese...glorious",
        items = items
    )
