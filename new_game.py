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
    import mapgen, os, mapgen.dbexport, templater
    import psyco
    psyco.full()
    con = db.connections.get_con()
    cur = db.DictCursor(con)
    if form.has_key('Start Game'):
        gen = mapgen.ContinentGenerator(num_countries=2, verbose=False)
        landmass = gen.generate()
        dest_real = mapgen.save_to_image(landmass)
        dest_saved = os.path.split(dest_real)[1]
        dest_saved = os.path.splitext(dest_saved)[0]

        landmass.name = "Test World "+dest_saved[:5]
        map_id = mapgen.dbexport.export(cur, user_dict['usr_id'], landmass, dest_saved)
        cur.close()
        s = "Game started!"
    else:
        cur.callproc('new_gam_id_for_usr', (user_dict['screen_name'],))
        r = cur.fetchall()
        cur.close()
        cur = db.DictCursor(con)
        if not r:
            gam_id = mapgen.dbexport.next_id('game', cur)
            q = 'INSERT INTO game (map_id) VALUES (NULL);'
            cur.execute(q)
            q = 'INSERT INTO game_membership (usr_id, gam_id) VALUES ("%s", %s);' % \
                (user_dict['usr_id'], gam_id)
            cur.execute(q)
        #s = 'Existing image:<br><img src="map_images/%s.png">' % r[0]['pic']
        
        if form.has_key('Add User'):
            if form.has_key('screen_name'):
                cur.callproc('user_data_bysn', (form['screen_name'].value,))
                usr_data = cur.fetchall()
                cur.close()
                cur = db.DictCursor(con)
                q = 'INSERT INTO game_membership (usr_id, gam_id) VALUES ("%s", %s);' % \
                    (usr_data[0]['usr_id'], r[0]['gam_id'])
                cur.execute(q)
        cur.close()
        cur = db.DictCursor(con)
        cur.callproc('users_in_game', (r[0]['gam_id'],))
        r = cur.fetchall()
        s = str(r)
        cur.close()
    screen_name = ""
    if form.has_key('sn'): screen_name = form['sn'].value
    templater.print_template("templates/new_game.html", locals())
