#!/usr/bin/python

#Mascot Results Analyzer
#Programmer: Tim Henderson
#Contact: timothy.henderson@case.edu
#Case Center for Proteomics
#Case Western Reserve University
#Purpose: Functions for dealing with session cookies

import os, time
from Crypto.Hash import SHA256
import Cookie
import nDDB
import MySQLdb

SEED = 'myseed'
MAX_TIME = 60.0*45.0

HOST = "localhost"
PORT = 3306
USER = 'root'
PASSWD = "gurkan12"
DB = "hendersont"

class DBError(Exception): pass

#time.strftime('%Y-%m-%d %H:%M:%S')

def get_dbConnection():#host="serine.case.edu", port=3306, user="root", passwd="gurkan12", db="hendersont"):
    '''returns the connection object from a MySQL database. The parameters are specified by module wide
    variables. If you would like to change them simply reset them before any connections are made by this
    module with the following syntax:
        import cookie_session
        cookie_session.HOST = 'myhost' 
        cookie_session.PORT = 12312
        ...'''
    con = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DB)
    return con

def genSessionID(seed, prounds=50):
    '''Generates a new sessionID based on the seed, some random information from /dev/urandom and the
    current time since the epoch.'''
    randata = os.urandom(32)
    sha = SHA256.new()
    sha.update(randata)
    sha.update(str(time.time()))
    sha.update(seed)
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
    return sha.hexdigest()

def genSigID():
    '''Generates a new and random signatureID used for signing cookies.'''
    sha = SHA256.new()
    sha.update(os.urandom(64))
    for x in range(50):
        sha.update(sha.digest())
    return sha.hexdigest()
    
def create_cookie(sessionID, sigID, epochtime, user):
    '''Creates a cookie from the passed in parameters and signs it with the sigID and returns the
    cookie and the msg_sig.'''
    c = Cookie.SimpleCookie()
    msg = nDDB.makeAdvanceDDB({'sessionID':sessionID, 'user':user, 'time':epochtime})
    msg_sig = signMsg(sigID, epochtime, os.environ['REMOTE_ADDR'], msg)
    c['session'] = msg
    c['session_sig'] = msg_sig
    return c, msg_sig

def check_cookie(sig, signatureID, time_signed, msg):
    '''Checks to see if the cookie is valid from the passed in parameters. sig is the signature of 
    the cookie that was saved in the database. SignatureID is the ID used to sign the cookie. time_signed
    is the time since the epoch that the cookie was signed and the msg is of course what was actually
    signed. Returns True if the cookie is valid, False otherwise.'''
    sig2 = signMsg(signatureID, time_signed, os.environ['REMOTE_ADDR'], msg)
    if sig2 == sig: return True
    else: return False

def create_session(sessionID, cur_sigID, cur_msgSig, user):
    '''Creates a new row in the session table with the passed in parameters and the current time.'''
    con = get_dbConnection()
    cur = con.cursor()
    timestr = time.strftime('%Y-%m-%d %H:%M:%S')
    query = '''INSERT INTO session 
    VALUES ('%s', '%s', '%s', '%s', '%s') ''' % (sessionID, cur_sigID, cur_msgSig, user, timestr)
    
    cur.execute(query)
    con.close()
    return make_session_dict(sessionID, cur_sigID, cur_msgSig, user, timestr)

def update_session(sessionID, sigID, msg_sig, user):
    '''Updates the session identified by the session ID, with passed in parameters and the current
    time.'''
    con = get_dbConnection()
    cur = con.cursor()
    timestr = time.strftime('%Y-%m-%d %H:%M:%S')
    
    q1 = '''UPDATE session
    SET sig_id = '%(sigID)s' 
    WHERE session_id = '%(sessionID)s'  ''' % locals()
    
    q2 = '''UPDATE session
    SET msg_sig = '%(msg_sig)s' 
    WHERE session_id = '%(sessionID)s'  ''' % locals()
    
    q3 = '''UPDATE session
    SET user = '%(user)s' 
    WHERE session_id = '%(sessionID)s'  ''' % locals()
    
    q4 = '''UPDATE session
    SET last_update = '%(timestr)s'
    WHERE session_id = '%(sessionID)s'  ''' % locals()
    
    cur.execute(q1)
    cur.execute(q2)
    cur.execute(q3)
    cur.execute(q4)
    
    con.close()
    return make_session_dict(sessionID, sigID, msg_sig, user, timestr)

def get_session(sessionID):
    '''Get the session from the session table in the database identified by the sessionID. It returns
    the session in the session dictionary format.'''
    con = get_dbConnection()
    cur = con.cursor()
    cur.execute("SELECT * FROM session\nWHERE session_id = '%s'" % (sessionID,))
    r = cur.fetchall()
    if len(r) == 1: 
        r = r[0]
        if len(r) == 5:
            sig_id = str(r[1])
            msg_sig = str(r[2])
            user = str(r[3])
            timestr = str(r[4])
        else:
            raise DBError, "The row did not contain all expected number of cols: " + str(len(r))
    else:
        raise DBError, "An unexpected number of rows was returned: " + str(len(r))
    con.close()
    return make_session_dict(sessionID, sig_id, msg_sig, user, timestr)

def make_session_dict(sess_id, sig_id, msg_sig, user, timestr):
    '''Makes a dictionary from the passed in parameters. Used to make sure the sess_dicts returned by
    several functions are standard across the entire module.'''
    return {'sessionID':sess_id, 'sigID':sig_id, 'msg_sig':msg_sig, 'user':user, 'time':timestr}

def session_old(sessionDict):
    '''Returns True of the session passed in the session dictionary format is old. False otherwise'''
    dif = time.time() - time.mktime(time.strptime(sessionDict['time'],'%Y-%m-%d %H:%M:%S'))
    if dif > MAX_TIME:
        return True
    else:
        return False

def clear_old_sessions():
    '''This method goes through all the rows in in the table session and checks to see if they have
    expire or if there are duplicates. If either is the case it deletes them from the table.'''
    con = get_dbConnection()
    cur = con.cursor()
    cur.execute("SELECT * FROM session ")
    rows = cur.fetchall()
    
    session_ids = set([])
    
    for row in rows:
        if len(row) == 5:
            sess_id = str(row[0])
            sig_id = str(row[1])
            msg_sig = str(row[2])
            user = str(row[3])
            timestr = str(row[4])
            sess_dict = make_session_dict(sess_id, sig_id, msg_sig, user, timestr)
            if (session_old(sess_dict)):
                query = "DELETE FROM session\nWHERE session_id = '%s'" % (sess_id,)
                cur.execute(query)
            else:
                if sess_id in session_ids:
                    query = "DELETE FROM session\nWHERE session_id = '%s'" % (sess_id,)
                    cur.execute(query)
                else:
                    session_ids.add(sess_id)
        else:
            raise DBError, "The row did not contain all expected number of cols: " + str(len(row))
    
    con.close()

def delete_session(sessionID):
    '''This removes the session identified by its sessionID from the database in the table session'''
    con = get_dbConnection()
    cur = con.cursor()
    query = "DELETE FROM session\nWHERE session_id = '%(sessionID)s'" % locals()
    cur.execute(query)
    con.close()

def make_new_session():
    '''This creates a new session. This means it creates a new row in the session table of the database.
    It also generates a session cookie for the new session. The function returns the cookie and the
    session dictionary.'''
    sigID = genSigID()
    sessionID = genSessionID(SEED)
    epochtime = str(time.time())
    c, msg_sig = create_cookie(sessionID, sigID, epochtime, 'unknown')
    ses_dict = create_session(sessionID, sigID, msg_sig, 'unknown')
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
            session = get_session(cook_dict['sessionID'])
            cookie_check = check_cookie(session['msg_sig'], session['sigID'], cook_dict['time'], cook)
            if cookie_check:
                sigID = genSigID()
                epochtime = str(time.time())
                if user == None: user = session['user']
                c, msg_sig = create_cookie(session['sessionID'], sigID, epochtime, user)
                ses_dict = update_session(session['sessionID'], sigID, msg_sig, user)
            else:
                c, ses_dict = make_new_session()
        except DBError:
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
            cookie_check = check_cookie(session['msg_sig'], session['sigID'], cook_dict['time'], cook)
            return cookie_check
        except DBError:
            return False
    else:
        return False
    
def print_header(cookie):
    '''Prints the header with the cookie passed in.'''
    print "Content-type: text/html"
    print cookie
    print