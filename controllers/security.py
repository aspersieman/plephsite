#!/usr/bin/python
# -*- coding: utf-8 -*-
import md5, random

# settings
response.title= A('Pleph',_href='/')
response.subtitle= request.controller
response.author="aspersieman"

response.menu=[
                ["home",False,"/"],
                ["pics",False, "/init/plephipics/index"],
                ["blog", False, "/init/plephblog/index"],
                ["rules",False, "/init/rules/index"]
              ]

if t2.logged_in:
    response.sidebar = [
                    ]
else:
    response.sidebar = None

def index():
    response.flash = "Please select an option from the list on the right."
    form = FORM()
    return dict(form = form)

@t2.requires_login(next="login")
def register():
    form = FORM()
    #return dict(form = t2.register())
    response.flash = "Registration disabled!"
    return dict(form = form)

@t2.requires_login(next="login")
def profile():
    return dict(form=t2.profile())

def login(): 
    return dict(form = t2.login())

def logout():
    t2.logout(next = "login")
