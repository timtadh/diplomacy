#!/usr/bin/python

import config
import os, re, cgi, templater, db, sys
import cookie_session, user_manager

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

def get_user_table(con):
    cur = db.DictCursor(con)
    cur.callproc('users_in_game', (ses_dict['gam_id'],))
    user_table = cur.fetchall()
    user_table_info = (('screen_name', "Screen Name"),)
    cur.close()
    return user_table, user_table_info

def print_game_info(user_dict, ses_dict):
    con = db.connections.get_con()
    user_table, user_table_info = get_user_table(con)
    cur = db.DictCursor(con)
    cur.callproc('map_data_for_game', (ses_dict['gam_id'],))
    map_data = cur.fetchall()
    cur.close()
    db.connections.release_con(con)
    map_name = map_data[0]['world_name']
    map_path = map_data[0]['pic']
    templater.print_template("templates/game_info.html", locals())

if user_dict == {}:
    target_page = 'user_list.py'
    templater.print_template("templates/login_template.html", locals())
else:
    print_game_info(user_dict, ses_dict)