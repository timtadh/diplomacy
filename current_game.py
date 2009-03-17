#!/usr/bin/python

import config
import os, re, cgi, templater, db, sys
import cookie_session, user_manager

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

def update_ses_dict():
    global ses_dict
    ses_dict = cookie_session.get_session(ses_dict['session_id'])

def check_switch(switch, ng):
    if switch:
        con = db.connections.get_con()
        cur = db.DictCursor(con)
        cur.callproc('set_session_gam_id', (ses_dict['session_id'], user_dict['usr_id'], ng))
        db.connections.release_con(con)
        update_ses_dict()

def get_game_table(switch=False, ng=-1):
    con = db.connections.get_con()
    cur = db.DictCursor(con)
    #check_switch(cur, switch, ng)
    cur.callproc('usr_games', (user_dict['usr_id'],))
    game_table = cur.fetchall()
    cur.close()
    db.connections.release_con(con)
    update_ses_dict()
    return game_table

def print_game_list(user_dict, ses_dict, switch, ng):
    choose_game = True
    game_table = get_game_table(switch, ng)
    
    for game in game_table:
        if game['gam_id'] == ses_dict['gam_id']:
            game['label'] = "<b>Game "+str(game['gam_id'])+"</b>"
            game['switch_link'] = "--"
        else:
            game['label'] = "Game "+str(game['gam_id'])
            game['switch_link'] = "<a class='inline' href='current_game.py?ng="+str(game['gam_id'])+"'>make active</a>"
    game_table_info = (('label', "id"),('switch_link', ""))
    templater.print_template("templates/current_game.html", locals())

def get_user_table(con):
    cur = db.DictCursor(con)
    cur.callproc('users_in_game', (ses_dict['gam_id'],))
    user_table = cur.fetchall()
    user_table_info = (('screen_name', "Screen Name"),)
    cur.close()
    return user_table, user_table_info

def print_game_info(user_dict, ses_dict, switch, ng):
    choose_game = False
    if ses_dict['gam_id'] != None:
        con = db.connections.get_con()
        user_table, user_table_info = get_user_table(con)
        cur = db.DictCursor(con)
        #check_switch(cur, switch, ng)
        cur.callproc('map_data_for_game', (ses_dict['gam_id'],))
        map_data = cur.fetchall()
        cur.close()
        db.connections.release_con(con)
        if len(map_data) > 0:
            map_name = map_data[0]['world_name']
            map_path = map_data[0]['pic']
        else:
            map_name = "No games in progress"
            map_path = "blank"
    templater.print_template("templates/current_game.html", locals())

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
            #Fix the session dictionary, which will not be updated until later
            #after one of the page printing funcs checks the switch var
            # ses_dict['gam_id'] = ng
        except:
            templater.print_error('invalid value passed to this page')
            sys.exit()
    check_switch(switch, ng)
    if form.has_key('new_game') and form['new_game'] or ses_dict['gam_id'] == None:
        print_game_list(user_dict, ses_dict, switch, ng)
    else:
        print_game_info(user_dict, ses_dict, switch, ng)