import MySQLdb
from crypt_framework import authenticator as auth

HOST = "masran.case.edu"
PORT = 3306
USER = 'diplomacy'
PASSWD = "d!plomacy12"
DB = "diplomacy"

class Connections(object):
    
    def __init__(self):
        self.free = set()
        self.in_use = set()
    
    def __del__(self):
        self.close_all();
    
    def close_all(self):
        for con in self.free:
            try: con.close()
            except: pass
        
        for con in self.in_use:
            try: con.close()
            except: pass
    
    def __make(self):
        '''returns the connection object from a MySQL database. The parameters are specified by module wide
        variables. If you would like to change them simply reset them before any connections are made by this
        module with the following syntax:
            import cookie_session
            cookie_session.HOST = 'myhost' 
            cookie_session.PORT = 12312
            ...'''
        con = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DB)
        return con
    
    def get_con(self):
        if len(self.free) > 0:
            con = self.free.pop()
            self.in_use.add(con)
            return con
        
        con = self.__make()
        self.in_use.add(con)
        return con
    
    def release_con(self, con):
        if con in self.in_use: self.in_use.remove(con)
        self.free.add(con)

connections = Connections()