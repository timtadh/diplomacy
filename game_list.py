#!/usr/bin/python

import config
import os, re, cgi, templater, db, sys
import cookie_session, user_manager

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

def update_ses_dict():
    global ses_dict
    ses_dict = cookie_session.get_session(ses_dict['session_id'])

def get_game_table(switch=False, ng=-1):
    con = db.connections.get_con()
    cur = db.DictCursor(con)
    if switch: 
        cur.callproc('set_session_gam_id', (ses_dict['session_id'], user_dict['usr_id'], ng))
    cur.callproc('usr_games', (user_dict['usr_id'],))
    game_table = cur.fetchall()
    cur.close()
    db.connections.release_con(con)
    update_ses_dict()
    return game_table

def print_game_list(user_dict, switch, ng): 
    game_table = get_game_table(switch, ng)
    
    for game in game_table:
        if game['gam_id'] == ses_dict['gam_id']:
            game['label'] = "<b>Game "+str(game['gam_id'])+"</b>"
            game['switch_link'] = "--"
        else:
            game['label'] = "Game "+str(game['gam_id'])
            game['switch_link'] = "<a class='inline' href='game_list.py?ng="+str(game['gam_id'])+"'>make active</a>"
    game_table_info = (('label', "id"),('switch_link', ""))
    templater.print_template("templates/game_list.html", locals())

if user_dict == {}:
    target_page = 'user_list.py'
    templater.print_template("templates/login_template.html", locals())
else:
    ng = -1
    switch = False
    if form.has_key('ng'):
        try:
            ng = int(form['ng'].value)
            switch = True
        except:
            templater.print_error('invalid value passed to this page')
            sys.exit()
    print_game_list(user_dict, switch, ng)