#!/usr/bin/python

import config
import os, re, cgi, sys
from twik import *

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

c = db.connections
moving_orders = [1, 2, 3, 4, 6] #order_types that use destinations

def get_order_table(pce_id, piece_order):
    piece_order = c.callproc('orders_for_piece', pce_id)[0]
    which_order = piece_order['order_type']
    
    type_table_info = (("order_link", "Order"),)
    type_table = c.callproc('order_types')
    order_string = '<a href="change_orders.py?pce_id=%s&odt_id=%s">%s</a>'
    for o in type_table:
        if o['odt_id'] == which_order:
            o['order_link'] = o['order_text']
        else:
            o['order_link'] = order_string % (pce_id, o['odt_id'], o['order_text'])
    return type_table, type_table_info, which_order

def get_order_dest_table(pce_id, ter_id):
    terr_table_info = (('abbrev', "Abbrev"), ('name', "Name"))
    terr_table = c.callproc('terrs_in_game', ses_dict['gam_id'])
    
    link_string = '<a href="change_orders.py?pce_id=%s&ter_id=%s">%s</a>'
    for terr in terr_table:
        if terr['ter_id'] != ter_id:
            terr['abbrev'] = link_string % (pce_id, terr['ter_id'], terr['abbrev'])
            terr['name'] = link_string % (pce_id, terr['ter_id'], terr['name'])
    
    return terr_table, terr_table_info

def print_change_orders(user_dict, ses_dict, pce_id, odt_id=None, ter_id=None):
    game_found = False
    if ses_dict['gam_id'] != None:
        game_found = True
        map_data = c.callproc('map_data_for_game', ses_dict['gam_id'])
        
        existing_orders = c.callproc('orders_for_piece', pce_id)[0]
        update = False
        if ter_id == None:
            ter_id = existing_orders['destination']
        else:
            ter_id = int(ter_id)
            update = True
        if odt_id == None:
            odt_id = existing_orders['order_type']
        else:
            odt_id = int(odt_id)
            update = True
        
        if update:
            c.callproc('new_order_for_piece', pce_id, odt_id, ter_id)
            existing_orders = c.callproc('orders_for_piece', pce_id)[0]
        
        show_done_link = existing_orders['executed']
        
        p = c.callproc('piece_info', pce_id)[0]
        abbrev = p['abbrev']
        if p['usr_id'] != user_dict['usr_id']:
            print "Naught naughty!"
            return
        
        map_path = map_data[0]['pic']
        order_table, order_table_info, which_order = get_order_table(pce_id, existing_orders)
        
        print_terr_table = False
        if which_order in moving_orders:
            print_terr_table = True
            terr_table, terr_table_info = get_order_dest_table(pce_id, ter_id)
    templater.print_template("templates/change_orders.html", locals())

if user_dict == {}:
    target_page = 'user_list.py'
    templater.print_template("templates/login_template.html", locals())
else:
    odt_id = None
    ter_id = None
    if form.has_key('odt_id'):
        odt_id = form['odt_id'].value
    if form.has_key('ter_id'):
        ter_id = form['ter_id'].value
    if form.has_key('pce_id'):
        print_change_orders(user_dict, ses_dict, form['pce_id'].value, odt_id, ter_id)
    else:
        print '<a href="write_orders.py">You want to be here.</a>'
