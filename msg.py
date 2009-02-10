#!/usr/bin/python

import config
import os, re, cgi, templater, db
import cookie_session, user_manager

def print_messages(user_dict):
    con = db.connections.get_con()
    cur = db.DictCursor(con)
    cur.callproc('usr_messages', (user_dict['usr_id'],))
    msgs = cur.fetchall()
    cur.close()
    db.connections.release_con(con)
    templater.print_template("templates/msg.html", locals())
    

def print_message(user_dict, msg_id):
    con = db.connections.get_con()
    cur = db.DictCursor(con)
    cur.callproc('message_data', (user_dict['usr_id'],msg_id))
    msg = cur.fetchall()[0]
    cur.close()
    cur = db.DictCursor(con)
    cur.callproc('read_msg', (msg_id,))
    cur.close()
    db.connections.release_con(con)
    templater.print_template("templates/view_msg.html", locals())

def delete_message(user_dict, msg_id):
    con = db.connections.get_con()
    cur = db.DictCursor(con)
    cur.callproc('delete_msg', (user_dict['usr_id'], msg_id))
    cur.close()
    db.connections.release_con(con)
    print_messages(user_dict)

if __name__ == '__main__':

    form = cgi.FieldStorage()
    ses_dict, user_dict = user_manager.init_user_session(form)
    
    if user_dict == {}:
        target_page = 'user_list.py'
        templater.print_template("templates/login_template.html", locals())
    else:
        if form.has_key('view'):  print_message(user_dict, int(form['view'].value))
        elif form.has_key('del'): delete_message(user_dict, int(form['del'].value))
        else: print_messages(user_dict)
