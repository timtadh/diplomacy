#!/usr/bin/python

import config
import os, re, cgi, sys
from twik import *

if __name__ == "__main__":
    form = cgi.FieldStorage()
    ses_dict, user_dict = user_manager.init_user_session(form)

def update_ses_dict():
    global ses_dict
    ses_dict = cookie_session.get_session(ses_dict['session_id'])

def check_switch(switch, ng):
    if switch:
        db.callproc('set_session_gam_id', ses_dict['session_id'], user_dict['usr_id'], ng)
        update_ses_dict()

def get_game_table(switch=False, ng=-1):
    game_table = db.callproc('usr_games', user_dict['usr_id'])
    game_table_info = (('label', "id"),('switch_link', ""))
    update_ses_dict()
    return game_table, game_table_info

def print_game_list(user_dict, ses_dict, switch, ng):
    game_table, game_table_info = get_game_table(switch, ng)
    
    for game in game_table:
        if game['gam_id'] == ses_dict['gam_id']:
            game['label'] = "<b>Game "+str(game['gam_id'])+"</b>"
            game['switch_link'] = "--"
        else:
            game['label'] = "Game "+str(game['gam_id'])
            game['switch_link'] = "<a class='inline' href='current_game.py?ng="+str(game['gam_id'])+"'>make active</a>"
    templater.print_template("templates/current_game_noneselected.html", locals())

def get_user_table():
    user_table_info = (('screen_name', "Screen Name"), ('name', "Country"))
    user_table = db.callproc('users_in_running_game', ses_dict['gam_id'])
    
    for usr in user_table:
        usr['name'] = '<div style="background-color:%s; padding-left:0.2em; padding-right:0.2em">%s</div>' % (usr['color'], usr['name'])
    
    return user_table, user_table_info

def get_supplier_table():
    supplier_table_info = (('abbrev', "Abbrev"), ('name', "Name"))  
    supplier_table = db.callproc('usr_suppliers_in_game', ses_dict['gam_id'], user_dict['usr_id'])
    return supplier_table, supplier_table_info

def get_terr_table():
    terr_table_info = (('abbrev', "Abbrev"), ('name', "Name"))
    terr_table = db.callproc('terrs_in_game', ses_dict['gam_id'])
    return terr_table, terr_table_info

def print_game_info(user_dict, ses_dict, switch, ng):
    if ses_dict['gam_id'] != None:
        map_data = db.callproc('map_data_for_game', ses_dict['gam_id'])
        user_table, user_table_info = get_user_table()
        supplier_table, supplier_table_info = get_supplier_table()
        terr_table, terr_table_info = get_terr_table()
        if len(map_data) > 0:
            map_data = map_data[0]
            map_name = map_data['world_name']
            map_path = map_data['pic']
            season = db.callproc('game_data', ses_dict['gam_id'])[0]['gam_season'].capitalize()
        else:
            map_name = "No games in progress"
            map_path = "blank"
            season = ""
    templater.print_template("templates/current_game.html", locals())

if __name__ == "__main__":
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
        check_switch(switch, ng)
        if form.has_key('new_game') and form['new_game'] or ses_dict['gam_id'] == None:
            print_game_list(user_dict, ses_dict, switch, ng)
        else:
            print_game_info(user_dict, ses_dict, switch, ng)
