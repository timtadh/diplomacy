#!/usr/bin/python

import config
import os, re, cgi, templater, db, sys
import cookie_session, user_manager

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

def sendmsg(user_dict, sn, subject, msg):
    try: sn = templater.SN_Exists().to_python(sn)
    except templater.formencode.Invalid, e:
        templater.print_error("to: "+str(e))
        sys.exit()
    try: msg = templater.Text(10000).to_python(msg)
    except templater.formencode.Invalid, e:
        templater.print_error("Message: "+str(e)+" your message was "+str(len(msg))+" characters long")
        sys.exit()
    try:
        subject = templater.Text(256).to_python(subject)
    except templater.formencode.Invalid, e:
        templater.print_error("Subject: "+str(e))
        sys.exit()
    con = db.connections.get_con()
    cur = db.DictCursor(con)
    cur.callproc('send_msg', (sn, user_dict['usr_id'], subject, msg))
    cur.close()
    db.connections.release_con(con)

def print_sendmsg(user_dict, screen_name='', subject=''):
    templater.print_template("templates/send_msg.html", locals())

if user_dict == {}:
    target_page = 'user_list.py'
    templater.print_template("templates/login_template.html", locals())
else:
    
    if form.has_key('Send Message'):
        if form.has_key('msg') and form.has_key('subject') and form.has_key('screen_name'):
            sendmsg(user_dict, form['screen_name'].value, form['subject'].value, form['msg'].value)
            import msg
            msg.print_messages(user_dict)
        else:
            templater.print_error("You must fill out all fields to send a message.")
    else:
        screen_name = ''
        subject = ''
        if form.has_key('sn'): screen_name = form['sn'].value
        if form.has_key('rep'):
            try:
                con = db.connections.get_con()
                cur = db.DictCursor(con)
                cur.callproc('message_data', (user_dict['usr_id'], int(form['rep'].value)))
                msg = cur.fetchall()[0]
                cur.close()
                db.connections.release_con(con)
                screen_name = msg['from']
                subject = 're: ' + msg['subject']
            except:
                pass
        print_sendmsg(user_dict, screen_name, subject)
