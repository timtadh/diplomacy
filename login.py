#!/usr/bin/python

import config
import os, re, cgi, templater, db
import cookie_session, user_manager

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

print ses_dict, '<br>', user_dict

print '<br>'
print db.connections.in_use
print db.connections.free

print '<br>'*3, str(os.getgroups())

if user_dict == {}:
    templater.print_template("templates/login_template.html", {'target_page':'login.py'})
else:
    print '<br>user_dict:<br>'
    for key in user_dict.keys():
        print key + ':' + '&nbsp;'*5 + str(user_dict[key]) + '<br>'
    
    print '<br>'*3
    print 'ses_dict:<br>'
    for key in ses_dict.keys():
        print key + ':' + '&nbsp;'*5 + str(ses_dict[key]) + '<br>'

    print '<br>'*3
    print 'os.environ:<br>'
    for key in os.environ.keys():
        print key + ':' + '&nbsp;'*5 + str(os.environ[key]) + '<br>'