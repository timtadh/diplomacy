#!/usr/bin/python

import config
import os, re, cgi, templater, db
import cookie_session, user_manager

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

def print_main(user_dict):
    num_users = 9001
    num_online = 9001
    num_games_total = 9001
    num_games_active = 9001
    num_games_usr = 9001
    unread_msgs = 9001
    templater.print_template("templates/main.html", locals())

if __name__ == "__main__":
    if user_dict == {}:
        target_page = 'main.py'
        templater.print_template("templates/login_template.html", locals())
    else:
        print_main(user_dict)
