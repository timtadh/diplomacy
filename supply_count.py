#!/usr/bin/python

import config
import os, re, cgi, templater, db
import cookie_session, user_manager

def print_supplycenters(user_dict):
    con = db.connections.get_con()
    cur = db.DictCursor(con)
    cur.callproc('supply_count')
    suppliers = cur.fetchall()
    cur.close()
    db.connections.release_con(con)

    table_info = (("screen_name", "Territory"), ("email", "Occupier"))
    table = suppliers
	
    templater.print_template("templates/supply_count.html", locals())

if __name__ == '__main__':
    
    form = cgi.FieldStorage()
    ses_dict, user_dict = user_manager.init_user_session(form)
   
    if user_dict == {}:
        target_page = 'supply_count.py'
        templater.print_template("templates/login_template.html", locals())
    else:
        print_supplycenters(user_dict)
