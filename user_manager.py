#!/usr/bin/python

#Mascot Results Analyzer
#Programmer: Tim Henderson
#Contact: timothy.henderson@case.edu
#Case Center for Proteomics
#Case Western Reserve University
#Purpose: Functions for dealing with users

import os, time
from Crypto.Hash import SHA256
import Cookie
import nDDB
import MySQLdb
import cookie_session

HOST = "localhost"
PORT = 3306
USER = 'diplomacy'
PASSWD = "d!plomacy12"
DB = "diplomacy"

class DBError(Exception): pass

def get_dbConnection():
    '''returns the connection object from a MySQL database. The parameters are specified by module wide
    variables. If you would like to change them simply reset them before any connections are made by this
    module with the following syntax:
        import user_manager
        user_manager.HOST = 'myhost' 
        user_manager.PORT = 12312
        ...'''
    con = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DB)
    return con

def gen_userID():
    '''Generates exactly one userID using random information from /dev/urandom and the SHA256 hash
    algorithm.'''
    sha = SHA256.new()
    sha.update(os.urandom(64))
    for x in range(50):
        sha.update(sha.digest())
    return sha.hexdigest()
    
def hash_passwd(passwd):
    '''This function takes the plain text of the password as its input and returns the hash of the
    password.'''
    sha = SHA256.new()
    sha.update(passwd)
    for x in range(50):
        sha.update(sha.digest())
    return sha.hexdigest()
    
def make_user_dict(user_id, name, email, passwd, last_login, creation, status):
    '''Makes a dictionary from the passed in parameters. Used to make sure the user_dicts returned by
    several functions are standard across the entire module.'''
    return {'user_id':user_id, 'name':name, 'email':email, 'passwd':passwd, 'last_login':last_login, 'creation':creation, 'status':status}
    
def get_user(user_name):
    '''Gets the user information for the user with the name passed in the parameter user_name. Returns
    the information as a dictionary.'''
    con = get_dbConnection()
    cur = con.cursor()
    cur.execute("SELECT * FROM users\nWHERE name = '%s'" % (user_name,))
    rows = cur.fetchall()
    if len(rows) == 1: 
        cols = rows[0]
        if len(cols) == 8:
            user_id = str(cols[0])
            name = cols[1]
            email = cols[2]
            passwd = str(cols[3])
            salt = cols[4]
            last_login = str(cols[5])
            creation = str(cols[6])
            status = str(cols[7])
        else:
            raise DBError, "The row did not contain all expected number of cols: " + str(len(r))
    elif len(rows) == 0:
        return {}
    else:
        raise DBError, "An unexpected number of rows was returned: " + str(len(r))
    con.close()
    return make_user_dict(user_id, name, email, passwd, last_login, creation, status)

def get_user_byemail(email):
    '''Gets the user information for the user with the name passed in the parameter user_name. Returns
    the information as a dictionary.'''
    con = get_dbConnection()
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE email = '%s'" % (MySQLdb.escape_string(email),))
    rows = cur.fetchall()
    if len(rows) == 1: 
        cols = rows[0]
        if len(cols) == 8:
            user_id = str(cols[0])
            name = cols[1]
            email = cols[2]
            passwd = cols[3]
            salt = cols[4]
            last_login = str(cols[5])
            creation = str(cols[6])
            status = str(cols[7])
        else:
            raise DBError, "The row did not contain all expected number of cols: " + str(len(cols))
    elif len(rows) == 0:
        return {}
    else:
        raise DBError, "An unexpected number of rows was returned: " + str(len(rows))
    con.close()
    return make_user_dict(user_id, name, email, passwd, last_login, creation, status)

def get_user_byid(user_id):
    '''Gets the user information for the user with the id passed in the parameter user_id. Returns
    the information as a dictionary.'''
    con = get_dbConnection()
    cur = con.cursor()
    cur.execute("SELECT * FROM users\nWHERE user_id = '%s'" % (user_id,))
    rows = cur.fetchall()
    if len(rows) == 1: 
        cols = rows[0]
        if len(cols) == 8:
            user_id = str(cols[0])
            name = cols[1]
            email = cols[2]
            passwd = cols[3]
            salt = cols[4]
            last_login = str(cols[5])
            creation = str(cols[6])
            status = str(cols[7])
        else:
            raise DBError, "The row did not contain all expected number of cols: " + str(len(r))
    elif len(rows) == 0:
        return {}
    else:
        raise DBError, "An unexpected number of rows was returned: " + str(len(r))
    con.close()
    return make_user_dict(user_id, name, email, passwd, last_login, creation, status)

def update_last_login_time(user_id):
    '''Updates the users table. Specifically the row where user_id matches the user_id passed into
    this function. It only updates one column (last_login) in the users table with the current time.'''
    con = get_dbConnection()
    cur = con.cursor()
    timestr = time.strftime('%Y-%m-%d %H:%M:%S')
    
    q1 = '''UPDATE users
    SET last_login = '%(timestr)s' 
    WHERE user_id = '%(user_id)s'  ''' % locals()
    
    cur.execute(q1)
    
    con.close()

def add_user(user_id, name, email, passwd):
    '''Creates a new row in the user table with the passed in parameters and the current time.'''
    con = get_dbConnection()
    cur = con.cursor()
    timestr = time.strftime('%Y-%m-%d %H:%M:%S')
    passhash = hash_passwd(passwd)
    query = '''INSERT INTO users 
    VALUES ('%(user_id)s', '%(name)s', '%(email)s', '%(passhash)s', '', '%(timestr)s', '%(timestr)s', '') ''' % locals()
    
    cur.execute(query)
    con.close()
    
def logout_session():
    cookie = Cookie.SimpleCookie()
    cookieHdr = os.environ.get("HTTP_COOKIE", "") #get the cookie from the enviroment
    cookie.load(cookieHdr) #load it into a Cookie class
    
    c, ses_dict = cookie_session.init_session(cookie, '') #initializes the session returns the session dictionary and the cookie to push to browser
    con = get_dbConnection()
    cur = con.cursor()
    
    q = """DELETE ses
    FROM session AS ses
    WHERE (ses.session_id = '%s' AND ses.user = '%s')""" % (ses_dict['sessionID'], ses_dict['user'])
    
    cur.execute(q)
    
    con.close()

def verify_passwd(email, passwd):
    '''this takes the user_name (ie the string the user uses to log-in with) if and the plain text
    password. The password is hashed if there is a user by the name passed in then the hashes of the
    passwords are compared. If they match it returns True else it returns False.'''
    passhash = hash_passwd(passwd) #get the hash of the password because the plain text password is not stored
    user_dict = get_user_byemail(email) #get the user_dict from the database
    if user_dict and user_dict.has_key('passwd') and passhash == user_dict['passwd']: #if the user_dict actually has information in it check to see if the passwords are the same
        return True, user_dict #if they are return true and the user dictionary
    else: 
        return False, {} #else return false and an empty dictionary
    
def verify_login(form):
    '''This function takes a form (ie the return value of cgi.FieldStorage()) or an empty dictionary.
    If the dictionary is empty it simply returns None. If there is no user by the name passed in it 
    returns None. If the passwords do not match it returns None. If the username is valid and the 
    password validates then it returns the user_id.'''
    user_id = None #set a default value for the user_id
    if cookie_session.verify_session(): #check to see if there is a valid session. you cannot log in with out one.
        if form.has_key('email') and form.has_key('passwd'): #see if the correct form info got passed to the server
            email = form['email'].value #get the user_name
            passwd = form['passwd'].value #get the password
            valid, user_dict = verify_passwd(email, passwd) #verify the password and get the user_dict as well
            if valid:
                user_id = user_dict['user_id'] #if it is valid grab the user_id from the user_dict
    return user_id 

def init_user_session(form={}):
    '''Initiates a session using the cookie session module. If a form is passed in it trys to 
    log the user in. The function will return a session dictionary and a user dictionary. If
    the current session has no user information associated with it the user dictionary will be
    empty. Note this function prints the header information, if you need to set custom cookies
    then you cannot currently use this function.'''
    cookie = Cookie.SimpleCookie()
    cookieHdr = os.environ.get("HTTP_COOKIE", "") #get the cookie from the enviroment
    cookie.load(cookieHdr) #load it into a Cookie class
    
    user_id = verify_login(form) #only actually gives you a user_id if you are logging in
    c, ses_dict = cookie_session.init_session(cookie, user_id) #initializes the session returns the session dictionary and the cookie to push to browser
    cookie_session.print_header(c) #print the header
    
    if user_id == ses_dict['user']: #means you are logging in with good credentials
        update_last_login_time(user_id) #so update the time
    
    user_id = ses_dict['user'] #if you are logged in gives you the current user_id
    user_dict = get_user_byid(user_id) #get the user dictionary
    return ses_dict, user_dict
