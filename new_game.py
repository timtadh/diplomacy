#!/usr/bin/python

import config
import os, re, cgi, templater, db
import cookie_session, user_manager

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

if user_dict == {}:
    target_page = 'new_game.py'
    templater.print_template("templates/login_template.html", locals())
else:
    import mapgen, os, mapgen.dbexport
    import psyco
    psyco.full()
    try:
        gen = mapgen.ContinentGenerator(num_countries=2, verbose=False)
        landmass = gen.generate()
        dest_real = mapgen.save_to_image(landmass)
        dest_saved = os.path.split(dest_real)[1]
        dest_saved = os.path.splitext(dest_saved)[0]
        
        #  This accesses the db from string query in the py file
        con = db.connections.get_con()
        cur = db.DictCursor(con)
        mapgen.dbexport.export(cur, landmass, "Test World "+dest_saved[:5], dest_saved)
        
        s = '<img src="map_images/%s.png">' % dest_saved
        
        cur.close()
        
    except Exception, e:
        print e
    
    templater.print_template("templates/new_game.html", locals())
