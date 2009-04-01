#!/usr/bin/python

import config
import os, re, cgi, sys
from twik import *
import mapgen

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

if user_dict == {}:
    templater.print_template("templates/login_template.html", {'target_page':'map_test.py'})
else:
    gen = mapgen.trigen.TriGen(num_countries=2)
    landmass = gen.generate()
    new_map_path = mapgen.save_to_image(landmass)
    
    templater.print_template("templates/map_test.html", locals())
