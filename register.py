#!/usr/bin/python

import config
import os, re, cgi, templater, db
import cookie_session, user_manager
import sys
from formencode import validators

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

if user_dict == {}:
    
    
    
    
    if form.has_key("name") and form.has_key("screen_name") and form.has_key("email") and\
       form.has_key("passwd1") and form.has_key("passwd2"):
        try:
            email = validators.Email(resolve_domain=True, not_empty=True).to_python(form["email"].value)
            name = validators.PlainText(r"^[a-zA-Z_\-0-9 ]*$", not_empty=True).to_python(form["name"].value)
            screen_name = validators.PlainText(not_empty=True).to_python(form["screen_name"].value)
            ps_validators = validators.FieldsMatch('p1', 'p2')
            ps = ps_validators.to_python({'p1':form["passwd1"].value, 'p2':form["passwd2"].value})['p1']
        except formencode.Invalid, e:
            templater.print_error(repr(e))
            sys.exit()
        
        if user_manager.get_user_byemail(form["email"].value):
            templater.print_error("that email address already has a user registered to it")
            sys.exit()
        
        print 'heyhey<br><br>'
        user_manager.add_user(user_manager.gen_userID(), name, email,
                              screen_name, ps)
        templater.print_template("templates/login_template.html", {'target_page':'login.py'})
    else:
        templater.print_template("templates/register.html", {'target_page':'register.py'})
else:
    templater.print_template("templates/login_template.html", {'target_page':'login.py'})