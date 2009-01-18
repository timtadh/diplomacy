import MySQLdb
from crypt_framework import authenticator as auth

HOST = "masran.case.edu"
PORT = 3306
USER = 'diplomacy'
PASSWD = "d!plomacy12"
DB = "diplomacy"

class Connection(object):
    
    self __init__(self):
        pass

    def make_db_connection():
        '''returns the connection object from a MySQL database. The parameters are specified by module wide
        variables. If you would like to change them simply reset them before any connections are made by this
        module with the following syntax:
            import cookie_session
            cookie_session.HOST = 'myhost' 
            cookie_session.PORT = 12312
            ...'''
        con = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DB)
        return con