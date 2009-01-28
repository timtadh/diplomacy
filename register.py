#!/usr/bin/python

import config
import os, re, cgi, templater, db
import cookie_session, user_manager
import sys

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

if user_dict == {}:
    if form.has_key("name") and form.has_key("email") and form.has_key("passwd1") and form.has_key("passwd2"):
        if form["passwd1"].value != form["passwd2"].value or user_manager.get_user_byemail(form["email"].value):
            if form["passwd1"].value != form["passwd2"].value:
                error = "passwords were not equal"
            else:
                error = "that email address already has a user registered to it"
            templater.print_error(error)
            sys.exit()
        print 'heyhey<br><br>'
        user_manager.add_user(user_manager.gen_userID(), form["name"].value, form["email"].value, form["passwd1"].value)
        templater.print_template("templates/login_template.html", {'target_page':'login.py'})
    else:
        templater.print_template("templates/register.html", {'target_page':'register.py'})
else:
    templater.print_template("templates/login_template.html", {'target_page':'login.py'})