# coding: utf8

response.title = "Pleph"
response.subtitle = "Exuding awesomage - NOW WITH MORE LLAMAS!"

def download():
    return response.download(request, db)

@auth.requires_membership('Admin')
def index():
    form = crud.create(db.images, message = "Image uploaded")
    images = db(db.images.addeddate != None).select(db.images.id, db.images.title, db.images.addeddate, orderby =~ db.images.addeddate)
    return dict(images = images, form = form)

def view():
    image = db(db.images.id == request.args(0)).select()[0]
    return dict(image = image)
