#!/usr/bin/python

import config
import os, re, cgi, templater, db
import cookie_session, user_manager
import mapgen

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

con = db.connections.get_con()
landmass = mapgen.dbimport.get(con, 5)
db.connections.release_con(con)
new_map_path = mapgen.save_to_image(landmass)

templater.print_template("templates/map_test.html", locals())
