#!/usr/bin/python

import config
import os, re, cgi, templater, db
import cookie_session, user_manager

def print_supplycenters(user_dict):
    con = db.connections.get_con()
    cur = db.DictCursor(con)
    cur.callproc('orders', ses_dict['gam_id'])
    suppliers = cur.fetchall()
    cur.close()
    db.connections.release_con(con)

    table_info = (("tname", "Territory"), ("cname", "Occupier"))
    table = suppliers
	
    templater.print_template("templates/orders.html", locals())
 
if __name__ == '__main__':
    
    form = cgi.FieldStorage()
    ses_dict, user_dict = user_manager.init_user_session(form)
   
    if user_dict == {}:
        target_page = 'orders.py'
        templater.print_template("templates/login_template.html", locals())
    else:
        print_supplycenters(user_dict)
