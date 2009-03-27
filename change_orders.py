#!/usr/bin/python

import config
import os, re, cgi, templater, db, sys
import cookie_session, user_manager

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

def get_table(con, name, args):
    cur = db.DictCursor(con)
    cur.callproc(name, args)
    table = cur.fetchall()
    cur.close()
    return table

def get_order_table(con, pce_id):
    cur = db.DictCursor(con)
    cur.close()
    piece_order = get_table(con, 'orders_for_piece', (pce_id,))[0]
    which_order = piece_order['order_type']
    
    type_table_info = (("order_link", "Order"),)
    type_table = get_table(con, 'order_types', ())
    order_string = '<a href="change_orders.py?pce_id=%s&odt_id=%s">%s</a>'
    for o in type_table:
        if o['odt_id'] == which_order:
            o['order_link'] = o['order_text']
        else:
            o['order_link'] = order_string % (pce_id, o['odt_id'], o['order_text'])
    return type_table, type_table_info

def print_change_orders(user_dict, ses_dict, pce_id, odt_id=None):
    game_found = False
    if ses_dict['gam_id'] != None:
        game_found = True
        con = db.connections.get_con()
        cur = db.DictCursor(con)
        cur.callproc('map_data_for_game', (ses_dict['gam_id'],))
        map_data = cur.fetchall()
        cur.close()
        
        if odt_id != None:
            cur = db.DictCursor(con)
            cur.callproc('new_order_for_piece', (pce_id, odt_id))
            cur.close()
            print odt_id
        
        cur = db.DictCursor(con)
        cur.callproc('piece_info', (pce_id,))
        p = cur.fetchall()[0]
        abbrev = p['abbrev']
        cur.close()
        if p['usr_id'] != user_dict['usr_id']:
            print "Naught naughty!"
            return
        
        map_path = map_data[0]['pic']
        order_table, order_table_info = get_order_table(con, pce_id)
        #terr_table, terr_table_info = get_terr_table(con)
        db.connections.release_con(con)
    templater.print_template("templates/change_orders.html", locals())

if user_dict == {}:
    target_page = 'user_list.py'
    templater.print_template("templates/login_template.html", locals())
else:
    odt_id = None
    if form.has_key('odt_id'):
        odt_id = form['odt_id'].value
    if form.has_key('pce_id'):
        print_change_orders(user_dict, ses_dict, form['pce_id'].value, odt_id)
    else:
        print '<a href="write_orders.py">You want to be here.</a>'
