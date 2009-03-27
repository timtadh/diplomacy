#!/usr/bin/python

import config
import os, re, cgi, templater, db
import cookie_session, user_manager

def check_switch(switch, ng):
    if switch:
        con = db.connections.get_con()
        cur = db.DictCursor(con)
        cur.callproc('set_session_gam_id', (ses_dict['session_id'], user_dict['usr_id'], ng))
        db.connections.release_con(con)
        update_ses_dict()

def get_table(con, name, args):
    cur = db.DictCursor(con)
    cur.callproc(name, args)
    table = cur.fetchall()
    cur.close()
    return table

def print_supplycenters(user_dict):
    supplier_table_info = (('abbrev', "Abbrev"), ('name', "Name"))  
    supplier_table = get_table(
        con, 'usr_suppliers_in_game', (ses_dict['gam_id'], user_dict['usr_id'])
    )
    return supplier_table, supplier_table_info

if __name__ == '__main__':
    
    form = cgi.FieldStorage()
    ses_dict, user_dict = user_manager.init_user_session(form)
   
    if user_dict == {}:
        target_page = 'supply_count.py'
        templater.print_template("templates/login_template.html", locals())
    else:
        print_supplycenters(user_dict)
