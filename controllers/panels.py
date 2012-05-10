# coding: utf8

def categories():
    category_links = ""
    categories = db(db.categories.title != "").select(db.categories.title, db.categories.id)
    if len(categories) > 0:
        for category in categories:
            category_post_link = db((db.relations.post != None) & (db.relations.categorytitle == category.title)).select()
            if category_post_link:
                category_links += "<a href='/" + request.application + "/categories/view/" + str(category.id) + "'>" + category.title + "</a> " 
        form = XML("<div class='sidepanelheading'>Post categories</div><div class='sidepanel'>" + category_links + "</div>")
    else:
        form = XML("<div></div>")
    return form

def feed_posts():
    post_feed_link = "<a href='/" + request.application + "/feeds/posts.rss'> Blog Feed RSS</a> " 
    form = XML("<div class='sidepanelheading'>Get The RSS Feed</div><div class='sidepanel'>" + post_feed_link + "</div>")
    return form

def post_archive():
    post_dates = db(db.post.private == False).select(db.post.addeddate, orderby=db.post.addeddate)
    MONTHS = {
        1: "Jan", 
        2: "Feb", 
        3: "Mar", 
        4: "Apr", 
        5: "May", 
        6: "Jun", 
        7: "Jul", 
        8: "Aug", 
        9: "Sep", 
        10: "Oct", 
        11: "Nov", 
        12: "Dec"
    }
    post_archive_html = ""
    import datetime
    if post_dates:
        posts_archive = {}
        for post_date in sorted(post_dates):
            currentmonth = int(post_date['post.addeddate'].month)
            currentyear = int(post_date['post.addeddate'].year)
            thismonthdate = datetime.datetime(currentyear, currentmonth, 1)
            if currentmonth < 12:
                followingmonthdate = datetime.datetime(currentyear, currentmonth + 1, 1)
            else:
                followingmonthdate = datetime.datetime(currentyear + 1, 1, 1)
            monthcounter = db((db.post.private == False) & (db.post.addeddate >= thismonthdate) & (db.post.addeddate < followingmonthdate)).count()
            posts_archive[str(currentyear) + " " + str(currentmonth)] = " (" + str(monthcounter) + ")"

        post_archive_html += "<div class='sidepanelheading'>Post Archives</div>"
        for post_arch in sorted(posts_archive, reverse = True):
            year = post_arch.split(" ")[0] 
            month = post_arch.split(" ")[1]
            monthname = MONTHS[int(month)]
            if len(str(month)) == 1:
                month = "0" + str(month)
            post_archive_html += "<div class='sidepanel'><a href='/" + request.application + "/posts/archive/" + str(year) + "/" + str(month) + "'>" + year + " " + monthname + posts_archive[post_arch] + "</a></div>"

    form = XML(post_archive_html)
    return form
