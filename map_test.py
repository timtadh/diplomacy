#!/usr/bin/python

import config
import os, re, cgi, templater, db
import cookie_session, user_manager
import mapgen

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

if user_dict == {}:
    templater.print_template("templates/login_template.html", {'target_page':'map_test.py'})
else:
    gen = mapgen.ContinentGenerator()
    landmass = gen.generate()
    new_map_path = mapgen.save_to_image(landmass)
    
    #new_map_path = "map_temp.png"
    
    con = db.connections.get_con()
    cur = db.DictCursor(con)
    #cur.callproc('name', (arg1, arg2...))
    cur.close()
    db.connections.release_con(con)
    
    templater.print_template("templates/map_test.html", locals())
