#!/usr/bin/python

import config
import os, re, cgi, templater, db
import cookie_session, user_manager
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
    cur.execute(q.new_game)
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

def print_new_game(user_dict, form, user_to_add=""):    
    error = ""
    con = db.connections.get_con()
    this_game = {}
    
    r = games_for_current_user(con)
    if not r: make_new_game(con)
    this_game = r[0]
    #'Existing image:<br><img src="map_images/%s.png">' % r[0]['pic']
    
    if user_to_add != "":
        try:
            add_user_to_game(user_to_add, this_game, con)
        except:
            error = "Could not add user "+user_to_add
    screen_name = ""
    cur = db.DictCursor(con)
    cur.callproc('users_in_game', (this_game['gam_id'],))
    user_table = cur.fetchall()
    user_table_info = (('screen_name', "Screen Name"),)
    cur.close()
    db.connections.release_con(con)
    templater.print_template("templates/new_game.html", locals())

def start_game(con):
    cur = db.DictCursor(con)
    gen = mapgen.ContinentGenerator(num_countries=2, verbose=False)
    landmass = gen.generate()
    dest_real = mapgen.save_to_image(landmass)
    dest_saved = os.path.split(dest_real)[1]
    dest_saved = os.path.splitext(dest_saved)[0]
    
    landmass.name = "Test World "+dest_saved[:5]
    map_id = mapgen.dbexport.export(cur, user_dict['usr_id'], landmass, dest_saved)
    cur.close()
    print 'start'
    templater.print_template("templates/main.html", locals())

if user_dict == {}:
    target_page = 'new_game.py'
    templater.print_template("templates/login_template.html", locals())
else:
    import mapgen, os, mapgen.dbexport, templater
    import psyco
    psyco.full()
    if form.has_key('Start Game'):
        #THIS IS BROKEN
        this_game = start_game(con)
    else:
        if form.has_key('Add User') and form.has_key('screen_name'):
            print_new_game(user_dict, form, form['screen_name'].value)
        if form.has_key('sn'):
            print_new_game(user_dict, form, form['sn'].value)
        else:
            print_new_game(user_dict, form)
