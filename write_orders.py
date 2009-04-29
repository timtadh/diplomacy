#!/usr/bin/python

import config
import os, re, cgi, sys
from twik import *
import mapgen.dbimport

import resolution_engine

def resolve_orders(gam_id):
    resolution_engine.resolve(gam_id)

def get_order_table(usr_id, gam_id):
    piece_table_info = (
        ("pce_type", "type"), ("name", "territory"), ("abbrev","abbrev"), ("order_type","order"),
        ("destination", "destination"), ('op', 'operands')
    )
    piece_table = db.callproc('pieces_for_user', gam_id, usr_id)
    order_table = db.callproc('orders_for_user', gam_id, usr_id)
    
    link_str = '<a href="change_orders.py?pce_id=%s">%s</a>'
    for piece in piece_table:
        piece['order_type'] = link_str % (piece['pce_id'], 'hold')
        for order in order_table:
            if piece['pce_id'] == order['pce_id']:
                piece['order_type'] = link_str % (piece['pce_id'], order['order_text'])
                if order['has_dst'] == 1:
                    if order['destination']: piece['destination'] = order['dst_name']
                    else: piece['destination'] = ''
                else: piece['destination'] = ''
        if resolution_engine.has_op(piece['pce_id']):
            s = ', '.join([op['name'] for op in db.callproc('operands_for_piece', piece['pce_id'])])
            piece['op'] = s
        else: piece['op'] = ''
    return piece_table, piece_table_info

def get_terr_table(gam_id):
    terr_table_info = (('abbrev', "Abbrev"), ('name', "Name"))
    terr_table = db.callproc('terrs_in_game', gam_id)
    return terr_table, terr_table_info

def get_orders_given(usr_id, gam_id):
    game_membership_data = db.callproc('game_membership_data', gam_id)
    result = None
    all_given = True
    for m in game_membership_data:
        if not m['orders_given']: all_given = False
        if m['usr_id'] == usr_id:
            result = m['orders_given']
    return result, all_given

def update_map(gam_id=0):
    if gam_id == 0:
        gam_id = ses_dict['gam_id']
    con = db.connections.get_con()
    landmass = mapgen.dbimport.get(con, gam_id)
    dest_real = mapgen.save_to_image(landmass)
    dest_saved = os.path.split(dest_real)[1]
    db.connections.release_con(con)
    return os.path.splitext(dest_saved)[0]

def insert_default_orders(gam_id):
    pieces = db.callproc('pieces_for_game', gam_id)
    for piece in pieces:
        db.callproc('new_order_for_piece', piece['pce_id'], 3, None)

def roll_over_turn(gam_id):
    resolve_orders(gam_id)
    
    game_data = db.callproc('game_data', gam_id)[0]
    
    year = game_data['gam_year']
    season = game_data['gam_season']
    if season == 'fall':
        year += 1
        season = 'spring'
    else:
        season = 'fall'
    
    dest_saved = update_map()
    
    db.callproc('roll_over_turn', gam_id, dest_saved, season, year)
    
    insert_default_orders(gam_id)

def print_order_screen(user_dict, ses_dict, execute):
    game_found = False
    if ses_dict['gam_id'] != None:
        game_found = True
        map_data = db.callproc('map_data_for_game', ses_dict['gam_id'])
        
        if execute: db.callproc('set_orders_given', user_dict['usr_id'], ses_dict['gam_id'])
        
        orders_given, all_orders_given = get_orders_given(user_dict['usr_id'], ses_dict['gam_id'])
        
        if orders_given and all_orders_given:
            roll_over_turn(ses_dict['gam_id'])
            all_orders_given = False
            orders_given = False
        
        map_data = map_data[0]
        map_name = map_data['world_name']
        map_path = map_data['pic']
        ter_orders_table, ter_orders_table_info = get_order_table(user_dict['usr_id'], ses_dict['gam_id'])
        terr_table, terr_table_info = get_terr_table(ses_dict['gam_id'])
        
    templater.print_template("templates/write_orders.html", locals())

if __name__ == '__main__':
    
    form = cgi.FieldStorage()
    ses_dict, user_dict = user_manager.init_user_session(form)
    
    if user_dict == {}:
        target_page = 'user_list.py'
        templater.print_template("templates/login_template.html", locals())
    else:
        execute = False
        if form.has_key('execute'):
            execute = form['execute'].value
        print_order_screen(user_dict, ses_dict, execute)