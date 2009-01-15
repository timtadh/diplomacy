#!/usr/bin/python

import sys
sys.stderr = sys.stdout
import os
import cgi
import cgitb; cgitb.enable( )
import os, re, data_parser, yaptu
from Masran import Masran
import Cookie, time
import cookie_session, user_manager, db_manager
import config_db_con

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

if user_dict == {}:
    if form.has_key("name") and form.has_key("email") and form.has_key("passwd1") and form.has_key("passwd2"):
        if form["passwd1"].value != form["passwd2"].value or user_manager.get_user_byemail(form["email"].value):
            if form["passwd1"].value != form["passwd2"].value:
                error = "passwords were not equal"
            else:
                error = "that email address already has a user registered to it"
            f = open("error_template.html", 'r')
            s = f.readlines()
            f.close()
            rex=re.compile('\<\%([^\<\%]+)\%\>')
            rbe=re.compile('\<\+')
            ren=re.compile('\-\>')
            rco=re.compile('\|= ')
            
            cop = yaptu.copier(rex, locals(), rbe, ren, rco)
            cop.copy(s)
            sys.exit()
        user_manager.add_user(user_manager.gen_userID(), form["name"].value, form["email"].value, form["passwd1"].value)
        target_page = "/masran2/main.py"
        f = open("login_template.html", 'r')
        #f = open("htmltest.html", 'r')
        s = f.readlines()
        f.close()
        rex=re.compile('\<\%([^\<\%]+)\%\>')
        rbe=re.compile('\<\+')
        ren=re.compile('\-\>')
        rco=re.compile('\|= ')
        cop = yaptu.copier(rex, globals(), rbe, ren, rco)
        cop.copy(s)
    else:
        target_page = "/masran2/register.py"
        f = open("register.html", 'r')
        #f = open("htmltest.html", 'r')
        s = f.readlines()
        f.close()
        rex=re.compile('\<\%([^\<\%]+)\%\>')
        rbe=re.compile('\<\+')
        ren=re.compile('\-\>')
        rco=re.compile('\|= ')
        cop = yaptu.copier(rex, globals(), rbe, ren, rco)
        cop.copy(s)
else:
    exp_mng = db_manager.Experiment_Manager(user_dict)
    if form.has_key("delete") and form.has_key("exp_id"):
        exp_id = form["exp_id"].value
        if exp_mng.my_exps.has_key(exp_id):
            exp_mng.del_exp(exp_id)
    
    target_page = "/masran2/main.py"
    f = open("start.html", 'r')
    #f = open("htmltest.html", 'r')
    s = f.readlines()
    f.close()
    rex=re.compile('\<\%([^\<\%]+)\%\>')
    rbe=re.compile('\<\+')
    ren=re.compile('\-\>')
    rco=re.compile('\|= ')
    cop = yaptu.copier(rex, globals(), rbe, ren, rco)
    cop.copy(s)