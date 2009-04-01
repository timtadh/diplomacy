#!/usr/bin/python

import config
import os, re, cgi
from twik import *

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

def quick_query(con, procname, user_dict=None):
    cur = db.DictCursor(con)
    if user_dict == None:
        cur.callproc(procname)
    else:
        cur.callproc(procname, (user_dict['usr_id'],))
    r = cur.fetchall()
    cur.close()
    return r

def print_main(user_dict):
    con = db.connections.get_con()
    num_users = quick_query(con, 'count_users', user_dict)[0]['num_users']
    num_games_total = quick_query(con, 'count_games')[0]['num_games_total']
    num_games_active = quick_query(con, 'count_active_games')[0]['num_games_active']
    num_games_usr = len(quick_query(con, 'usr_games', user_dict))
    unread_msges = quick_query(con, 'count_unread_msges', user_dict)[0]['unread_msges']
    
    db.connections.release_con(con)
    templater.print_template("templates/main.html", locals())

if __name__ == "__main__":
    if user_dict == {}:
        target_page = 'main.py'
        templater.print_template("templates/login_template.html", locals())
    else:
        print_main(user_dict)
