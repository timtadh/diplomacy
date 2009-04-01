#!/usr/bin/python
# -*- coding: utf-8 -*-

import config
import os, re, cgi, templater, db
import cookie_session, user_manager

def print_messages(user_dict, page=0):
    #con = db.connections.get_con()
    #cur = db.DictCursor(con)
    #cur.callproc('usr_messages', (user_dict['usr_id'],))
    #msgs = cur.fetchall()
    #cur.close()
    #db.connections.release_con(con)
    
    msgs = db.connections.callproc('usr_messages', user_dict['usr_id'])
    
    table_info = (("from", "from"), ("subject", "subject"), ("msg", "message"),
                  ("time", "time sent"), ("delete", ""))
    table = list()
    for msg in msgs:
        msg_from = msg['from']
        
        if not int(msg['have_read']):
            subject = "<a class='inline' href='msg.py?view=" + str(msg['msg_id']) + "'>"
        else:
            subject = "<a class='inline' style='font-weight:100' href='msg.py?view="
            subject += str(msg['msg_id'])+"'>"
        try: sub_text = templater.Text().hide_all_tags(templater.Text().from_python(msg['subject']))
        except: sub_text = templater.Text().hide_all_tags(msg['subject'])
        subject += sub_text[:40]
        if len(sub_text) > 40: subject += ' ... '
        subject += '</a>'
        
        if not int(msg['have_read']): message = "<span style='font-weight:900;'>"
        else: message = "<span>"
        try: msg_text = templater.Text().hide_all_tags(templater.Text().from_python(msg['msg']))
        except: msg_text = templater.Text().hide_all_tags(msg['msg'])
        message += msg_text[:30]
        if len(msg_text) > 30: message += ' ... '
        message += '</span>'
        
        time = str(msg['time_sent'])
        
        delete = "<a class='inline' href='msg.py?del="+str(msg['msg_id'])+"'>delete</a>"
        
        table.append({"from":msg_from, "subject":subject, "msg":message,"time":time,"delete":delete})
    
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
    try:
        msg['msg'] = templater.Text().from_python(msg['msg'])
        msg['subject'] = templater.Text().from_python(msg['subject'])
    except:
        pass
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
        target_page = 'msg.py'
        templater.print_template("templates/login_template.html", locals())
    else:
        try:
            if form.has_key('view'):  print_message(user_dict, int(form['view'].value))
            elif form.has_key('del'): delete_message(user_dict, int(form['del'].value))
            elif form.has_key('page'): print_messages(user_dict, int(form['page'].value))
            else: print_messages(user_dict)
        except:
            print_messages(user_dict)
