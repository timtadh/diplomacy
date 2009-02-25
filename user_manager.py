#!/usr/bin/python

#Programmer: Tim Henderson
#Contact: timothy.henderson@case.edu
#Case Western Reserve University
#Purpose: Functions for dealing with users

import os, time, sys
from Crypto.Hash import SHA256
import Cookie
import nDDB
import db
from crypt_framework import authenticator as auth, qcrypt
import templater
import cookie_session
from logger import Logger
logger = Logger(__file__)

HOST = "localhost"
PORT = 3306
USER = 'diplomacy'
PASSWD = "d!plomacy12"
DB = "diplomacy"

class DBError(Exception): pass

def gen_userID():
    '''Generates exactly one userID using random information from /dev/urandom and the SHA256 hash
    algorithm.'''
    sha = SHA256.new()
    sha.update(os.urandom(64))
    for x in range(50):
        sha.update(sha.digest())
    return sha.hexdigest()
    
def make_user_dict(user_id, name, email, passwd, salt, last_login, creation, status):
    '''Makes a dictionary from the passed in parameters. Used to make sure the user_dicts returned by
    several functions are standard across the entire module.'''
    return {'usr_id':user_id, 'name':name, 'email':email, 'pass_hash':passwd, 'salt':salt, 
            'last_login':last_login, 'creation':creation, 'status':status}
    
def get_user_byemail(email):
    '''Gets the user information for the user with the name passed in the parameter user_name. Returns
    the information as a dictionary.'''
    con = db.connections.get_con()
    cur = db.DictCursor(con)
    cur.callproc('user_data_byemail', (email,))
    r = cur.fetchall()
    cur.close()
    db.connections.release_con(con)
    if len(r) > 0: return r[0]
    else: return dict()

def get_user_byid(usr_id):
    '''Gets the user information for the user with the id passed in the parameter user_id. Returns
    the information as a dictionary.'''
    con = db.connections.get_con()
    cur = db.DictCursor(con)
    cur.callproc('user_data_byid', (usr_id,))
    r = cur.fetchall()
    cur.close()
    db.connections.release_con(con)
    if len(r) > 0: return r[0]
    else: return dict()

def update_last_login_time(usr_id):
    '''Updates the users table. Specifically the row where user_id matches the user_id passed into
    this function. It only updates one column (last_login) in the users table with the current time.'''
    con = db.connections.get_con()
    cur = db.DictCursor(con)
    cur.callproc('update_user_login_time', (usr_id,))
    cur.close()
    db.connections.release_con(con)

def add_user(usr_id, name, email, screen_name, password):
    '''Creates a new row in the user table with the passed in parameters and the current time.'''
    
    salt = qcrypt.normalize(os.urandom(32))
    pass_hash = auth.saltedhash_hex(password, salt)
    
    con = db.connections.get_con()
    cur = db.DictCursor(con)
    cur.callproc('create_user', (usr_id, name, email, screen_name, pass_hash, salt))
    cur.close()
    db.connections.release_con(con)
    
    logger.writeln('added user: ', (usr_id, name, email, screen_name, pass_hash, salt))
    
def logout_session():
    cookie = Cookie.SimpleCookie()
    cookieHdr = os.environ.get("HTTP_COOKIE", "") #get the cookie from the enviroment
    cookie.load(cookieHdr) #load it into a Cookie class
    
    c, ses_dict = cookie_session.init_session(cookie) # initializes the session returns the session 
                                                      # dictionary and the cookie to push to browser
    logger.writeln('logging out -> usr_id:', ses_dict['usr_id'], '   session_id:', ses_dict['session_id'])
    
    con = db.connections.get_con()
    cur = db.DictCursor(con)
    cur.callproc('logout_session', (ses_dict['session_id'],ses_dict['usr_id']))
    cur.close()
    db.connections.release_con(con)

def verify_passwd(email, password):
    '''this takes the user_name (ie the string the user uses to log-in with) if and the plain text
    password. The password is hashed if there is a user by the name passed in then the hashes of the
    passwords are compared. If they match it returns True else it returns False.'''
    
    user_dict = get_user_byemail(email) #get the user_dict from the database
    logger.writeln('    user_dict:', user_dict)
    if user_dict: 
        pass_hash = auth.saltedhash_hex(password, user_dict['salt'])
        logger.writeln('    pass_hash:', pass_hash)
    else: return False, dict()
    if user_dict and user_dict.has_key('pass_hash') and pass_hash == user_dict['pass_hash']: #if the user_dict actually has information in it check to see if the passwords are the same
        return True, user_dict #if they are return true and the user dictionary
    else: 
        return False, dict() #else return false and an empty dictionary
    
def verify_login(form,  cookie):
    '''This function takes a form (ie the return value of cgi.FieldStorage()) or an empty dictionary.
    If the dictionary is empty it simply returns None. If there is no user by the name passed in it 
    returns None. If the passwords do not match it returns None. If the username is valid and the 
    password validates then it returns the user_id.'''
    usr_id = None #set a default value for the user_id
    if cookie_session.verify_session(): # check to see if there is a valid session. you cannot 
                                        # log in with out one.
        if form.has_key('email') and form.has_key('passwd'): # see if the correct form info got 
                                                             # passed to the server
            logger.writeln('about to try and log in')
            try:
                email = templater.validators.Email(resolve_domain=True,
                                                 not_empty=True).to_python(form["email"].value)
            except templater.formencode.Invalid, e:
                logger.writeln("email did not pass validation: ")
                c, ses_dict = cookie_session.init_session(cookie, None)
                cookie_session.print_header(c)
                templater.print_error("email: "+str(e))
                sys.exit()
            passwd = form['passwd'].value #get the password
            logger.writeln('    email:', email)
            valid, user_dict = verify_passwd(email, passwd) #verify the password and get the 
                                                            #user_dict as well
            logger.writeln('    valid:', valid)
            
            if valid:
                usr_id = user_dict['usr_id'] #if it is valid grab the user_id from the user_dict
            else:
                logger.writeln("Password or email not correct")
                c, ses_dict = cookie_session.init_session(cookie, None)
                cookie_session.print_header(c)
                templater.print_error("Password or email not correct")
                sys.exit(0)
        elif form.has_key('email') or form.has_key('passwd'):
            logger.writeln("All of the fields were not filled out.")
            c, ses_dict = cookie_session.init_session(cookie, None)
            cookie_session.print_header(c)
            templater.print_error("All fields must be filled out.")
            sys.exit(0)
    return usr_id 

def init_user_session(form={}):
    '''Initiates a session using the cookie session module. If a form is passed in it trys to 
    log the user in. The function will return a session dictionary and a user dictionary. If
    the current session has no user information associated with it the user dictionary will be
    empty. Note this function prints the header information, if you need to set custom cookies
    then you cannot currently use this function.'''
    cookie = Cookie.SimpleCookie()
    cookieHdr = os.environ.get("HTTP_COOKIE", "") #get the cookie from the enviroment
    cookie.load(cookieHdr) #load it into a Cookie class
    
    user_id = verify_login(form, cookie) #only actually gives you a user_id if you are logging in
    c, ses_dict = cookie_session.init_session(cookie, user_id) #initializes the session returns the session dictionary and the cookie to push to browser
    logger.writeln('ses_dict: ', ses_dict)
    cookie_session.print_header(c) #print the header
    
    if user_id == ses_dict['usr_id']: #means you are logging in with good credentials
        logger.writeln('logging in')
        update_last_login_time(user_id) #so update the time
    
    user_id = ses_dict['usr_id'] #if you are logged in gives you the current user_id
    logger.writeln('user_id: ', user_id)
    user_dict = get_user_byid(user_id) #get the user dictionary
    logger.writeln('user_dict: ', user_dict)
    return ses_dict, user_dict
