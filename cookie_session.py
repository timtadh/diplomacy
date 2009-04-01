#!/usr/bin/python

#Programmer: Tim Henderson
#Contact: timothy.henderson@case.edu
#Case Western Reserve University
#Purpose: Functions for dealing with session cookies

import os, time
from Crypto.Hash import SHA256
import Cookie
import nDDB
import db
from logger import Logger
logger = Logger(__file__)

HOST = "masran.case.edu"
PORT = 3306
USER = 'diplomacy'
PASSWD = "d!plomacy12"
DB = "diplomacy"

class DBError(Exception): pass

#time.strftime('%Y-%m-%d %H:%M:%S')

count = 0

def genSessionID(prounds=50):
    '''Generates a new sessionID based on the seed, some random information from /dev/urandom and the
    current time since the epoch.'''
    randata = os.urandom(32)
    sha = SHA256.new()
    sha.update(randata)
    sha.update(str(time.time()))
    for x in range(prounds):
        sha.update(sha.digest())
    return sha.hexdigest()

def signMsg(sigID, time, ip_addr, msg):
    '''Signs a msg using the passed in parameters.'''
    sha = SHA256.new()
    sha.update(msg)
    sha.update(ip_addr)
    sha.update(time)
    sha.update(sigID)
    for x in range(1000):
        sha.update(sha.digest())
    return sha.hexdigest()

def genSigID():
    '''Generates a new and random signatureID used for signing cookies.'''
    sha = SHA256.new()
    sha.update(os.urandom(64))
    for x in range(50):
        sha.update(sha.digest())
    return sha.hexdigest()
    
def create_cookie(session_id, sig_id, epochtime):
    '''Creates a cookie from the passed in parameters and signs it with the sigID and returns the
    cookie and the msg_sig.'''
    c = Cookie.SimpleCookie()
    msg = nDDB.makeAdvanceDDB({'sessionID':session_id, 'time':epochtime})
    msg_sig = signMsg(sig_id, epochtime, os.environ['REMOTE_ADDR'], msg)
    c['session'] = msg
    c['session_sig'] = msg_sig
    return c, msg_sig

def check_cookie(sig, sig_id, time_signed, msg):
    '''Checks to see if the cookie is valid from the passed in parameters. sig is the signature of 
    the cookie that was saved in the database. SignatureID is the ID used to sign the cookie. time_signed
    is the time since the epoch that the cookie was signed and the msg is of course what was actually
    signed. Returns True if the cookie is valid, False otherwise.'''
    sig2 = signMsg(sig_id, time_signed, os.environ['REMOTE_ADDR'], msg)
    if sig2 == sig: return True
    else: return False

def create_session(session_id, sig_id, msg_sig, usr_id):
    '''Creates a new row in the session table with the passed in parameters and the current time.'''
    con = db.connections.get_con()
    cur = db.DictCursor(con)
    timestr = time.strftime('%Y-%m-%d %H:%M:%S')
    cur.callproc('create_session', (session_id, sig_id, msg_sig, usr_id))
    cur.close()
    db.connections.release_con(con)
    return get_session(session_id)

def update_session(session_id, sig_id, msg_sig, usr_id):
    '''Updates the session identified by the session ID, with passed in parameters and the current
    time.'''
    con = db.connections.get_con()
    cur = db.DictCursor(con)
    timestr = time.strftime('%Y-%m-%d %H:%M:%S')
    cur.callproc('update_session', (session_id, sig_id, msg_sig, usr_id))
    cur.close()
    db.connections.release_con(con)
    return get_session(session_id)

def get_session(session_id):
    '''Get the session from the session table in the database identified by the sessionID. It returns
    the session in the session dictionary format.'''
    
    con = db.connections.get_con()
    cur = db.DictCursor(con)
    cur.callproc('session_data', (session_id,))
    r = cur.fetchall()
    cur.close()
    db.connections.release_con(con)
    if len(r) > 0: d = r[0]
    else: return dict()
    return d

def clear_old_sessions():
    '''This method goes through all the rows in in the table session and checks to see if they have
    expire or if there are duplicates. If either is the case it deletes them from the table.'''
    con = db.connections.get_con()
    cur = db.DictCursor(con)
    cur.callproc('clear_old_sessions')
    cur.close()
    db.connections.release_con(con)

def delete_session(sessionID):
    '''This removes the session identified by its sessionID from the database in the table session'''
    con = db.connections.get_con()
    cur = db.DictCursor(con)
    cur.callproc('delete_session', (session_id,))
    cur.close()
    db.connections.release_con(con)

def make_new_session():
    '''This creates a new session. This means it creates a new row in the session table of the database.
    It also generates a session cookie for the new session. The function returns the cookie and the
    session dictionary.'''
    sigID = genSigID()
    sessionID = genSessionID()
    epochtime = str(time.time())
    c, msg_sig = create_cookie(sessionID, sigID, epochtime)
    ses_dict = create_session(sessionID, sigID, msg_sig, 'unknown')
    logger.writeln('made new session', sessionID)  
    return c, ses_dict


def init_session(cookie, user=None):
    '''Initiates the session. It uses the cookie passed in (ie the value of 
    os.environ.get("HTTP_COOKIE", "") loaded into a Cookie.SimpleCookie). Before trying to validate
    the session and generating a new session cookie the function first calls clear_old_sessions(), 
    ensuring only non-expired sessions are validated. If the session validates then it generates
    a new session cookie for that session. If anything else happens it creates a new session and
    generates a new cookie. The method returns the generated cookie and the session dictionary.'''
    clear_old_sessions()
    c = cookie
    ses_dict = {}
    if cookie.has_key('session') and cookie.has_key('session_sig'):
        
        cook = cookie['session'].value
        cook_dict = nDDB.decodeDDB(cook)
        try:
            #print "Content-type: text/html"
            #print
            logger.writeln('session_id: ', cook_dict['sessionID'])
            session = get_session(cook_dict['sessionID'])
            logger.writeln('database_session_dict: ', session)
            if session: 
                cookie_check = check_cookie(session['msg_sig'], session['sig_id'], 
                                                                          cook_dict['time'], cook)
            else: cookie_check = None
            logger.writeln('cookie_check: ', cookie_check)
            if cookie_check:
                sigID = genSigID()
                logger.writeln('sigID: ', sigID)
                epochtime = str(time.time())
                logger.writeln('epochtime: ', epochtime)
                if user == None: user = session['usr_id']
                logger.writeln('user: ', user)
                c, msg_sig = create_cookie(session['session_id'], sigID, epochtime)
                logger.writeln('c: ', c)
                logger.writeln('msg_sig: ', msg_sig)
                ses_dict = update_session(session['session_id'], sigID, msg_sig, user)
                logger.writeln('ses_dict: ', ses_dict)
            else:
                c, ses_dict = make_new_session()
        except Exception, e:
            print "Content-type: text/html"
            print
            print '<h1>Cookie Session Error</h1>'
            print e, '<br>'*5
            logger.writeln()
            logger.writeln('COOKIE SESSION ERROR: ', e)
            c, ses_dict = make_new_session()
    else:
        c, ses_dict = make_new_session()
    return c, ses_dict

def verify_session():
    '''This method returns True if the current session is valid, False otherwise.'''
    cookie = Cookie.SimpleCookie()
    cookieHdr = os.environ.get("HTTP_COOKIE", "")
    cookie.load(cookieHdr)
    
    if cookie.has_key('session') and cookie.has_key('session_sig'):
        cook = cookie['session'].value
        cook_dict = nDDB.decodeDDB(cook)
        try:
            session = get_session(cook_dict['sessionID'])
            if session: 
                return check_cookie(session['msg_sig'], session['sig_id'], 
                                                                    cook_dict['time'], cook)
            return False
        except:
            return False
    else:
        return False
    
def print_header(cookie):
    '''Prints the header with the cookie passed in.'''
    print "Content-type: text/html"
    print cookie
    print