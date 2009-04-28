#!/usr/bin/python

import config
import os, re, cgi, sys
from twik import *

import write_orders
import resolution_engine

moving_orders = [1, 2, 3, 4, 6] #order_types that use destinations


def get_order_table(gam_id, pce_id, piece_order):
    orders_for_piece = db.callproc('orders_for_piece', pce_id)
    if orders_for_piece: 
        piece_order = orders_for_piece[0]
        which_order = piece_order['order_type']
    else: 
        piece_order = list()
        which_order = 'hold'
    
    game_data = db.callproc('game_data', gam_id)
    if game_data: game_data = game_data[0]
    else: raise Exception
    
    type_table_info = (("order_link", "Order"),)
    type_table = db.callproc('order_types', game_data['turn_stage'])
    order_string  = '<form action="change_orders.py" method="post">\n'
    order_string += '<input type="hidden" value="%s" name="pce_id"/>'
    order_string += '<input type="hidden" value="%s" name="odt_id"/>'
    order_string += '<input type="submit" value="%s"/>'
    order_string += '</form>'
    
    for o in type_table:
        if o['odt_id'] == which_order:
            o['order_link'] = o['order_text']
        else:
            o['order_link'] = order_string % (pce_id, o['odt_id'], o['order_text'])
    return type_table, type_table_info, which_order

def get_order_dest_table(pce_id, ter_id):
    terr_table_info = (('abbrev', "Abbrev"), ('name', "Name"))
    terr_table = db.callproc('terr_adj', ter_id)
    
    order_string  = '<form action="change_orders.py" method="post">\n'
    order_string += '<input type="hidden" value="%s" name="pce_id"/>'
    order_string += '<input type="hidden" value="%s" name="ter_id"/>'
    order_string += '<input type="submit" value="%s"/>'
    order_string += '</form>'
    for terr in terr_table:
        if terr['ter_id'] != ter_id:
            terr['abbrev'] = order_string % (pce_id, terr['ter_id'], terr['abbrev'])
    
    return terr_table, terr_table_info
        
        
def get_order_op_table(pce_id, into, ter_id):
    terr_table_info = (('abbrev', "Abbrev"), ('name', "Name"))
    terr_table = db.callproc('terr_adj', into)
    
    order_string  = '<form action="change_orders.py" method="post">\n'
    order_string += '<input type="hidden" value="%s" name="pce_id"/>'
    order_string += '<input type="hidden" value="%s" name="op_id"/>'
    order_string += '<input type="submit" value="%s"/>'
    order_string += '</form>'
    for terr in terr_table:
        if terr['ter_id'] != ter_id:
            terr['abbrev'] = order_string % (pce_id, terr['ter_id'], terr['abbrev'])
    
    return terr_table, terr_table_info

def update_orders(pce_id, odt_id=None, ter_id=None):
    orders_for_piece = db.callproc('orders_for_piece', pce_id)
    if orders_for_piece: existing_orders = orders_for_piece[0]
    else: return
    
    update = False
    if ter_id == None:
        ter_id = None
    else:
        ter_id = int(ter_id)
        update = existing_orders['destination'] != ter_id
    
    if odt_id == None:
        odt_id = existing_orders['order_type']
    else:
        odt_id = int(odt_id)
        update = existing_orders['order_type'] != odt_id
    
    if update:
        db.callproc('new_order_for_piece', pce_id, odt_id, ter_id)
        existing_orders = db.callproc('orders_for_piece', pce_id)[0]
    
    return bool(existing_orders['executed'])

def get_db_data(gam_id, pce_id):
    map_data = db.callproc('map_data_for_game', gam_id)
    orders_for_piece = db.callproc('orders_for_piece', pce_id)
    if orders_for_piece: existing_orders = orders_for_piece[0]
    else: existing_orders = list()
    piece_info = db.callproc('piece_info', pce_id)[0]
    
    if piece_info['usr_id'] != user_dict['usr_id']:
        templater.print_error("This page was not accessed in the correct manner.")
        sys.exit(0)
        
    return piece_info, map_data, existing_orders


def print_choose_op(user_dict, piece_info, map_data, existing_orders, ter_id):
    abbrev = piece_info['abbrev']
    
    map_path = map_data[0]['pic']
    terr_table, terr_table_info = get_order_op_table(pce_id, existing_orders['destination'], piece_info['ter_id'])
    
    templater.print_template("templates/change_orders/choose_op.html", locals())
    
def print_choose_dst(user_dict, piece_info, map_data, existing_orders, ter_id):
    abbrev = piece_info['abbrev']
    
    map_path = map_data[0]['pic']
    terr_table, terr_table_info = get_order_dest_table(pce_id, piece_info['ter_id'])
    
    templater.print_template("templates/change_orders/choose_dst.html", locals())
    

def print_choose_orders(user_dict, gam_id, piece_info, map_data, existing_orders):
    abbrev = piece_info['abbrev']
    
    map_path = map_data[0]['pic']
    order_table, order_table_info, which_order = get_order_table(gam_id, pce_id, ter_id)
    
    templater.print_template("templates/change_orders/choose_order.html", locals())

if __name__ == '__main__':
    
    form = cgi.FieldStorage()
    ses_dict, user_dict = user_manager.init_user_session(form)

    if user_dict == {}:
        target_page = 'user_list.py'
        templater.print_template("templates/login_template.html", locals())
    else:
        if ses_dict['gam_id'] == None:
            templater.print_error("please choose a game first")
            sys.exit(0)
        
        gam_id = ses_dict['gam_id']
        
        if form.has_key('pce_id'):
            odt_id = None
            ter_id = None
            pce_id = None
            operand = None
            
            try: pce_id = templater.validators.Int.to_python(form['pce_id'].value)
            except templater.formencode.Invalid, e: 
                templater.print_error("pce_id invalid")
                sys.exit(0)
            
            
            if form.has_key('odt_id'):
                try: odt_id = templater.validators.Int.to_python(form['odt_id'].value)
                except templater.formencode.Invalid, e: 
                    templater.print_error("odt_id invalid")
                    sys.exit(0)
                update_orders(pce_id, odt_id, ter_id)
                db.callproc('clear_piece_operands', pce_id)
                piece_info, map_data, existing_orders = get_db_data(gam_id, pce_id)
                if resolution_engine.has_dst(pce_id):
                    print_choose_dst(user_dict, piece_info, map_data, existing_orders, ter_id)
                else:
                    write_orders.print_order_screen(user_dict, ses_dict, False)
                    
                #print_choose_dst(user_dict, piece_info, map_data, existing_orders)
            elif form.has_key('ter_id'):
                try: ter_id = templater.validators.Int.to_python(form['ter_id'].value)
                except templater.formencode.Invalid, e: 
                    templater.print_error("ter_id invalid")
                    sys.exit(0)
                update_orders(pce_id, odt_id, ter_id)
                piece_info, map_data, existing_orders = get_db_data(gam_id, pce_id)
                if resolution_engine.has_op(pce_id):
                    print_choose_op(user_dict, piece_info, map_data, existing_orders, ter_id)
                else:
                    write_orders.print_order_screen(user_dict, ses_dict, False)
            elif form.has_key('op_id'):
                try: op_id = templater.validators.Int.to_python(form['op_id'].value)
                except templater.formencode.Invalid, e: 
                    templater.print_error("op_id invalid")
                    sys.exit(0)
                db.callproc('insert_operand', pce_id, op_id)
                piece_info, map_data, existing_orders = get_db_data(gam_id, pce_id)
                write_orders.print_order_screen(user_dict, ses_dict, False)
            else:
                update_orders(pce_id, odt_id, ter_id)
                piece_info, map_data, existing_orders = get_db_data(gam_id, pce_id)
                print_choose_orders(user_dict, gam_id, piece_info, map_data, existing_orders)
        else:
            templater.print_error('<a href="write_orders.py">You want to be here.</a>')
