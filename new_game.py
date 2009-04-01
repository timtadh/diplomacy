#!/usr/bin/python

import config
import os, re, cgi, sys
from twik import *
import sql.new_game as q

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

def games_for_current_user(con):
    cur = db.DictCursor(con)
    cur.callproc('new_gam_id_for_usr', (user_dict['screen_name'],))
    r = cur.fetchall()
    cur.close()
    return r

def make_new_game(con):
    cur = db.DictCursor(con)
    gam_id = mapgen.dbexport.next_id('game', cur)
    cur.execute(q.new_game % user_dict['usr_id'])
    cur.execute(q.add_user % (user_dict['usr_id'], gam_id))
    cur.close()

def add_user_to_game(sn, game_data, con):
    cur = db.DictCursor(con)
    cur.callproc('user_data_bysn', (sn,))
    usr_data = cur.fetchall()
    cur.close()
    cur = db.DictCursor(con)
    cur.execute(q.add_user % (usr_data[0]['usr_id'], game_data['gam_id']))
    cur.close()

def del_user_from_game(sn, game_data, con):
    cur = db.DictCursor(con)
    cur.callproc('user_data_bysn', (sn,))
    usr_data = cur.fetchall()
    cur.close()
    cur = db.DictCursor(con)
    cur.execute(q.del_user % (usr_data[0]['usr_id'], game_data['gam_id']))
    cur.close()

def insert_default_orders(gam_id, con):
    cur = db.DictCursor(con)
    cur.callproc('pieces_for_game', (gam_id,))
    pieces = cur.fetchall()
    cur.close()
    for piece in pieces:
        cur = db.DictCursor(con)
        cur.callproc('new_order_for_piece', (piece['pce_id'], 5, None))
        cur.close()

def get_user_table(con, gam_id):    
    cur = db.DictCursor(con)
    cur.callproc('users_in_game', (gam_id,))
    user_table = cur.fetchall()
    cur.close()
    return user_table, (('screen_name', "Screen Name"),('remove_link', ""))

def print_new_game(user_dict, form, user_to_add="", user_to_remove=""):    
    error = ""
    con = db.connections.get_con()
    this_game = {}
    
    r = games_for_current_user(con)
    if not r:
        make_new_game(con)
        r = games_for_current_user(con)
    this_game = r[0]
    #'Existing image:<br><img src="map_images/%s.png">' % r[0]['pic']
    
    if user_to_add != "":
        try:
            add_user_to_game(user_to_add, this_game, con)
        except:
            error = "Could not add user "+user_to_add
    
    if user_to_remove != "":
        try:
            del_user_from_game(user_to_remove, this_game, con)
        except:
            error = "Could not remove user "+user_to_add

    screen_name = ""
    user_table, user_table_info = get_user_table(con, this_game['gam_id'])
    for usr in user_table:
        if usr['screen_name'] == user_dict['screen_name']:
            usr['remove_link'] = "--"
        else:
            usr['remove_link'] = "<a class='inline' href='new_game.py?rm_sn="+usr['screen_name']+"'>remove</a>"
    db.connections.release_con(con)
    templater.print_template("templates/new_game.html", locals())

def start_game(user_dict):    
    con = db.connections.get_con()
    
    r = games_for_current_user(con)
    
    cur = db.DictCursor(con)
    cur.callproc('users_in_game', (r[0]['gam_id'],))
    user_table = cur.fetchall()
    cur.close()
    
    gen = mapgen.behemoth.ContinentGenerator(num_countries=len(user_table), verbose=False)
    landmass = gen.generate()
    dest_real = mapgen.save_to_image(landmass)
    dest_saved = os.path.split(dest_real)[1]
    dest_saved = os.path.splitext(dest_saved)[0]
    
    #landmass.name = "Test World "+dest_saved[:5]
    
    user_table, user_table_info = get_user_table(con, r[0]['gam_id'])
    user_list = [i['usr_id'] for i in user_table]
    
    cur = db.DictCursor(con)
    mapgen.dbexport.export(cur, user_list, landmass, dest_saved, r[0]['gam_id'])
    cur.close()
    
    cur = db.DictCursor(con)
    cur.execute(q.give_map_to_game % (landmass.map_id, dest_saved, r[0]['gam_id']))
    cur.close()
    
    cur = db.DictCursor(con)
    for usr, cty in zip(user_table, landmass.countries):
        cur.execute(q.give_cty_to_usr % (usr['usr_id'], cty.cty_id, r[0]['gam_id']))
    cur.close()
    
    cur = db.DictCursor(con)
    cur.callproc('set_session_gam_id', (ses_dict['session_id'], user_dict['usr_id'], r[0]['gam_id']))
    user_table = cur.fetchall()
    cur.close()
    
    insert_default_orders(r[0]['gam_id'], con)
    
    db.connections.release_con(con)
    templater.print_template("templates/game_created.html", locals())

if user_dict == {}:
    target_page = 'new_game.py'
    templater.print_template("templates/login_template.html", locals())
else:
    import mapgen, os, mapgen.dbexport, templater
    import psyco
    psyco.full()
    if form.has_key('Start Game'):
        start_game(user_dict)
    else:
        add_sn = ""
        rm_sn = ""
        if form.has_key('Add User') and form.has_key('screen_name'):
            add_sn = form['screen_name'].value
        if form.has_key('sn'):
            add_sn = form['sn'].value
        if form.has_key('rm_sn'):
            rm_sn = form['rm_sn'].value
        print_new_game(user_dict, form, add_sn, rm_sn)
