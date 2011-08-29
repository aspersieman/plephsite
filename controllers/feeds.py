# coding: utf8

from markdown import WIKI
response.generic_patterns = ['*']

@service.rss
def posts():
    posts = db(db.post.private == False).select(limitby = (0, 10), orderby =~ db.post.addeddate)
    urlbase = request.env.wsgi_url_scheme + "://" + request.env.http_host
    items = []
    for post in posts:
        desc = str(XML(WIKI(post.excerpt))) + "..." + str(A("[read more]", _href = urlbase + URL(request.application, c = "posts", f = "view", args = post.id))) if len(post.excerpt) > 0 else XML(WIKI(post.body))
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
        description = "A blog about programming, comics, Thailand and wordsmithing",
        items = items
    )

def feed():
    return dict(title="my feed",
                link="http://feed.example.com", 
                description="my first feed",
                items=[
                  dict(title="my feed",
                       link="http://feed.example.com", 
                       description="my first feed")
                ])

