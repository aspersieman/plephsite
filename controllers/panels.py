# coding: utf8

def categories():
    category_links = ""
    categories = db(db.categories.title != "").select(db.categories.title, db.categories.id)
    if len(categories) > 0:
        for category in categories:
            category_links += "<a href='/" + request.application + "/categories/view/" + str(category.id) + "'>" + category.title + "</a> " 
        form = XML("<div class='sidepanelheading'>Post categories</div><div class='sidepanel'>" + category_links + "</div>")
    else:
        form = XML("<div></div>")
    return form

def feed_posts():
    post_feed_link = "<a href='/" + request.application + "/feeds/posts.rss'> Blog</a> " 
    form = XML("<div class='sidepanelheading'><img src='/" + request.application + "/static/images/feed-icon-small.png' />" + "&nbsp;" * 13 + "Feeds</div><div class='sidepanel'>" + post_feed_link + "</div>")
    return form

def google_reader_shared_items():
    reader_shared_items = """
    <div>
    <script type="text/javascript" src="http://www.google.co.za/reader/ui/publisher-en.js"></script>
    <script type="text/javascript" src="http://www.google.co.za/reader/public/javascript/user/05176344199512550335/state/com.google/broadcast?n=5&callback=GRC_p(%7Bc%3A%22blue%22%2Ct%3A%22aspersieman's%20shared%20items%22%2Cs%3A%22false%22%2Cn%3A%22true%22%2Cb%3A%22false%22%7D)%3Bnew%20GRC"></script>
    </div>
    """
    form = XML(reader_shared_items)
    return form
