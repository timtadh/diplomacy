#!/usr/bin/python

import config
import os, re, cgi, sys
from twik import *

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

if user_dict == {}:
    target_page = 'db_example.py'
    templater.print_template("templates/login_template.html", locals())
else:
    
    s = ''
    try:
        
        #  This accesses the db from string query in the py file
        con = db.connections.get_con()
        
        cur = db.DictCursor(con)
        q = 'SELECT * FROM Praskac_countries;'
        cur.execute(q)
        r = cur.fetchall()
        s += str(r)
        for row in r:
            print 'country: ', str(row['name']), 'capitol: ', str(row['capitol'])
        cur.close()
        
        print
        print 
        
        # This accesses the db from a stored procedure
        cur = db.DictCursor(con)
        cur.callproc('example_stored_procedure')
        r = cur.fetchall()
        s += str(r)
        for row in r:
            print 'country: ', str(row['name']), 'capitol: ', str(row['capitol'])
        cur.close()
        
        print
        print
        
        cur = db.DictCursor(con)
        cur.callproc('example2', ('Algeria',))
        r = cur.fetchall()
        s += str(r)
        for row in r:
            print 'capitol: ', str(row['capitol'])
        cur.close()
        
        
        print
        print
        
        x = None
        cur = db.DictCursor(con)
        cur.callproc('example3', ('Algeria', x))
        print 'x: ', x
        cur.callproc('example3_results')
        r = cur.fetchall()
        s += str(r)
        for row in r:
            print 'capitol: ', str(row['capitol'])
        cur.close()
        # need these statement
        db.connections.release_con(con)
        
    except Exception, e:
        print e
    
    templater.print_template("templates/db_example.html", locals())
