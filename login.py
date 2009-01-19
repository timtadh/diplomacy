#!/usr/bin/python

import sys
sys.stderr = sys.stdout
import os
import cgi
import cgitb; cgitb.enable( )
import os, re, yaptu
import Cookie, time
import cookie_session, user_manager
import config_db_con
import MySQLdb
import db
from MySQLdb.cursors import DictCursor

form = cgi.FieldStorage()

#print cookie_session.get_dbConnection()

ses_dict, user_dict = user_manager.init_user_session(form)

print ses_dict, '<br>', user_dict

print '<br>'
print db.connections.in_use
print db.connections.free

if user_dict == {}:
    target_page = "login.py"
    f = open("templates/login_template.html", 'r')
    #f = open("htmltest.html", 'r')
    s = f.readlines()
    f.close()
    rex=re.compile('\<\%([^\<\%]+)\%\>')
    rbe=re.compile('\<\+')
    ren=re.compile('\-\>')
    rco=re.compile('\|= ')
    cop = yaptu.copier(rex, globals(), rbe, ren, rco)
    cop.copy(s)
else:
    print '<br>user_dict:<br>'
    for key in user_dict.keys():
        print key + ':' + '&nbsp;'*5 + str(user_dict[key]) + '<br>'
    
    print '<br>'*3
    print 'ses_dict:<br>'
    for key in ses_dict.keys():
        print key + ':' + '&nbsp;'*5 + str(ses_dict[key]) + '<br>'