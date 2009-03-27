#!/usr/bin/python

import config
import os, re, cgi, templater, db
import cookie_session, user_manager
import mapgen
import sql.execute_orders as q

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

def execute_orders(user_dict, ses_dict):
    game_found = False
    if ses_dict['gam_id'] == None:
        game_found = False
    else:
        game_found = True
        con = db.connections.get_con()
        landmass = mapgen.dbimport.get(con, ses_dict['gam_id'])
        dest_real = mapgen.save_to_image(landmass)
        dest_saved = os.path.split(dest_real)[1]
        dest_saved = os.path.splitext(dest_saved)[0]
        cur = db.DictCursor(con)
        cur.execute(q.update_map % (dest_saved, ses_dict['gam_id']))
        cur.close()
        map_path = dest_saved
        db.connections.release_con(con)

    templater.print_template("templates/execute_orders.html", locals())

if user_dict == {}:
    target_page = 'user_list.py'
    templater.print_template("templates/login_template.html", locals())
else:
    execute_orders(user_dict, ses_dict)
