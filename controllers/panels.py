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
