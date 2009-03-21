#!/usr/bin/python

import config
import os, re, cgi, templater, db
import cookie_session, user_manager
import mapgen

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

gen = mapgen.behemoth.ContinentGenerator(num_countries=2)
landmass = gen.generate()
new_map_path = mapgen.save_to_image(landmass)

templater.print_template("templates/map_test.html", locals())
