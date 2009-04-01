#!/usr/bin/python

import config
import os, re, cgi
from twik import *

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

def print_main(user_dict):
    num_users = db.callproc('count_users', user_dict['usr_id'])[0]['num_users']
    num_games_total = db.callproc('count_games')[0]['num_games_total']
    num_games_active = db.callproc('count_active_games')[0]['num_games_active']
    num_games_usr = len(db.callproc('usr_games', user_dict['usr_id']))
    unread_msges = db.callproc('count_unread_msges', user_dict['usr_id'])[0]['unread_msges']
    
    templater.print_template("templates/main.html", locals())

if __name__ == "__main__":
    if user_dict == {}:
        target_page = 'main.py'
        templater.print_template("templates/login_template.html", locals())
    else:
        print_main(user_dict)
