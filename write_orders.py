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

def get_user_table(con):
    user_table_info = (('screen_name', "Screen Name"), ('name', "Country"))
    user_table = get_table(con, 'users_in_running_game', (ses_dict['gam_id'],))
    return user_table, user_table_info

def get_ordersByTer_table(con):
    ordersByTer_table_info = (("pce_type", "type"), ("name", "territory"), ("abbrev","abbrev"), ("order_type","order"))
    ordersByTer_table = get_table(
        con, 'orders_by_ter', (ses_dict['gam_id'], user_dict['usr_id'])
    )
    return ordersByTer_table, ordersByTer_table_info

def get_terr_table(con):
    terr_table_info = (('abbrev', "Abbrev"), ('name', "Name"))
    terr_table = get_table(con, 'terrs_in_game', (ses_dict['gam_id'],))
    return terr_table, terr_table_info

def print_game_info(user_dict, ses_dict):
    game_found = False
    if ses_dict['gam_id'] != None:
        game_found = True
        con = db.connections.get_con()
        user_table, user_table_info = get_user_table(con)
        cur = db.DictCursor(con)
        cur.callproc('map_data_for_game', (ses_dict['gam_id'],))
        map_data = cur.fetchall()
        cur.close()
        db.connections.release_con(con)
        if len(map_data) > 0:
            map_data = map_data[0]
            map_name = map_data['world_name']
            map_path = map_data['pic']
            ordersByTer_table, ordersByTer_table_info = get_ordersByTer_table(con)
            terr_table, terr_table_info = get_terr_table(con)
        else:
            map_name = "No games in progress"
            map_path = "blank"
    templater.print_template("templates/write_orders.html", locals())

if user_dict == {}:
    target_page = 'user_list.py'
    templater.print_template("templates/login_template.html", locals())
else:
    print_game_info(user_dict, ses_dict)