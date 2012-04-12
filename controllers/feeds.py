# coding: utf8

import applications.init.modules.markdown as markdown
response.generic_patterns = ['*']

@service.rss
def posts():
    posts = db(db.post.private == False).select(limitby = (0, 10), orderby =~ db.post.addeddate)
    urlbase = request.env.wsgi_url_scheme + "://" + request.env.http_host
    items = []
    for post in posts:
        if post.excerpt:
            desc = str(markdown.WIKI(post.excerpt, safe_mode = "safe")) + "..." + str(A("[read more]", _href = urlbase + URL(request.application, c = "posts", f = "view", args = post.id))) if len(post.excerpt) > 0 else XML(markdown.WIKI(post.body))
        else:
            desc = str(XML(markdown.WIKI(post.body[0:500]))) + "..." + str(A(" [more]", _href = urlbase + URL(request.application, c = "posts", f = "view", args = post.id))) if len(post.body) > 0 else XML(markdown.WIKI(post.body))
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

