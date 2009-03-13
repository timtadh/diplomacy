#!/usr/bin/python

import config
import os, re, cgi, templater, db, sys
import cookie_session, user_manager

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

def switch_game(ng, con):
    cur = db.DictCursor(con)
    cur.callproc('set_session_gam_id', (ses_dict['session_id'], user_dict['usr_id'], ng))
    cur.close()

def print_game_list(user_dict, con):
    cur = db.DictCursor(con)
    cur.callproc('usr_games', (user_dict['usr_id'],))
    game_table = cur.fetchall()
    for game in game_table:
        if game['gam_id'] == ses_dict['gam_id']:
            game['label'] = "<b>Game "+str(game['gam_id'])+"</b>"
            game['switch_link'] = "--"
        else:
            game['label'] = "Game "+str(game['gam_id'])
            game['switch_link'] = "<a class='inline' href='game_list.py?ng="+str(game['gam_id'])+"'>make active</a>"
    game_table_info = (('label', "id"),('switch_link', ""))
    cur.close()
    templater.print_template("templates/game_list.html", locals())

if user_dict == {}:
    target_page = 'user_list.py'
    templater.print_template("templates/login_template.html", locals())
else:
    con = db.connections.get_con()
    if form.has_key('ng'):
        switch_game(form['ng'].value, con)
    print_game_list(user_dict, con)
    db.connections.release_con(con)