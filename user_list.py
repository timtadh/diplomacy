#!/usr/bin/python

import config
import os, re, cgi, templater, db
import cookie_session, user_manager

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

if user_dict == {}:
    target_page = 'user_list.py'
    templater.print_template("templates/login_template.html", locals())
else:
    con = db.connections.get_con()
    cur = db.DictCursor(con)
    cur.callproc('users_table')
    users = cur.fetchall()
    cur.close()
    db.connections.release_con(con)
    templater.print_template("templates/user_list.html", locals())
