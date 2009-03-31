#!/usr/bin/python

import config
import os, re, cgi, templater, db, sys
import cookie_session, user_manager
import mapgen.dbimport

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

def resolve_orders():
    pass #do order magic here!

def get_table(con, name, args):
    cur = db.DictCursor(con)
    cur.callproc(name, args)
    table = cur.fetchall()
    cur.close()
    return table

def get_order_table(con):
    piece_table_info = (
        ("pce_type", "type"), ("name", "territory"), ("abbrev","abbrev"), ("order_type","order")
    )
    piece_table = get_table(con, 'pieces_for_user', (ses_dict['gam_id'], user_dict['usr_id']))
    order_table = get_table(con, 'orders_for_user', (ses_dict['gam_id'], user_dict['usr_id']))
    
    link_str = '<a href="change_orders.py?pce_id=%s">%s</a>'
    for piece in piece_table:
        piece['order_type'] = link_str % (piece['pce_id'], 'hold')
        for order in order_table:
            if piece['pce_id'] == order['pce_id']:
                piece['order_type'] = link_str % (piece['pce_id'], order['order_text'])
    return piece_table, piece_table_info

def get_terr_table(con):
    terr_table_info = (('abbrev', "Abbrev"), ('name', "Name"))
    terr_table = get_table(con, 'terrs_in_game', (ses_dict['gam_id'],))
    return terr_table, terr_table_info

def get_orders_given(con):
    cur = db.DictCursor(con)
    cur.callproc('game_membership_data', (ses_dict['gam_id'],))
    result = None
    all_given = True
    for m in cur.fetchall():
        if not m['orders_given']: all_given = False
        if m['usr_id'] == user_dict['usr_id']:
            result = m['orders_given']
    cur.close()
    return result, all_given

def update_map(con):
    landmass = mapgen.dbimport.get(con, ses_dict['gam_id'])
    dest_real = mapgen.save_to_image(landmass)
    dest_saved = os.path.split(dest_real)[1]
    return os.path.splitext(dest_saved)[0]

def insert_default_orders(gam_id, con):
    cur = db.DictCursor(con)
    cur.callproc('pieces_for_game', (gam_id,))
    pieces = cur.fetchall()
    cur.close()
    for piece in pieces:
        cur = db.DictCursor(con)
        cur.callproc('new_order_for_piece', (piece['pce_id'], 5, None))
        cur.close()

def roll_over_turn(con):
    resolve_orders()
    
    cur = db.DictCursor(con)
    cur.callproc('game_data', (ses_dict['gam_id'],))
    game_data = cur.fetchall()[0]
    cur.close()
    
    year = game_data['gam_year']
    season = game_data['gam_season']
    if season == 'fall':
        year += 1
        season = 'spring'
    else:
        season = 'fall'
    
    dest_saved = update_map(con)
    
    cur = db.DictCursor(con)
    cur.callproc('roll_over_turn', (ses_dict['gam_id'], dest_saved, season, year))
    cur.close()
    
    insert_default_orders(ses_dict['gam_id'], con)

def print_order_screen(user_dict, ses_dict, execute):
    game_found = False
    if ses_dict['gam_id'] != None:
        game_found = True
        con = db.connections.get_con()
        cur = db.DictCursor(con)
        cur.callproc('map_data_for_game', (ses_dict['gam_id'],))
        map_data = cur.fetchall()
        cur.close()
        
        if execute:
            cur = db.DictCursor(con)
            cur.callproc('set_orders_given', (user_dict['usr_id'], ses_dict['gam_id']))
            cur.close()
        
        orders_given, all_orders_given = get_orders_given(con)
        if all_orders_given:
            roll_over_turn(con)
            all_orders_given = False
            orders_given = False
        
        db.connections.release_con(con)
        
        map_data = map_data[0]
        map_name = map_data['world_name']
        map_path = map_data['pic']
        ter_orders_table, ter_orders_table_info = get_order_table(con)
        terr_table, terr_table_info = get_terr_table(con)
        
    templater.print_template("templates/write_orders.html", locals())

if user_dict == {}:
    target_page = 'user_list.py'
    templater.print_template("templates/login_template.html", locals())
else:
    execute = False
    if form.has_key('execute'):
        execute = form['execute'].value
    print_order_screen(user_dict, ses_dict, execute)