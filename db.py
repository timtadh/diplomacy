'''
Author: Tim Henderson
Date Started: January 28, 2008

This module does connection pooling for mysql connections. Handles connecting and and closing 
connections for the user. Must be configured by user before use.

Usage:
    setup:
        import db
        db.HOST = HOST
        db.PORT = PORT
        db.USER = USER
        db.PASSWD = PASSWD
        db.DB = DB
    
    get connection:
        con = db.connections.get_con()
    
    relase connection:
        db.connections.release_con(con)
'''

import MySQLdb
from MySQLdb.cursors import DictCursor

def _results_gen(cur):
    r = cur.fetchall()
    if r: yield r
    else: return
    n = cur.nextset()
    while n: 
        r = cur.fetchall()
        if r: yield r
        else: return
        n = cur.nextset()

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
            import db
            db.HOST = 'myhost' 
            db.PORT = 12312
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
        
    def callproc(self, name, *args):
        connection = self.get_con()
        cursor = DictCursor(connection)
        cursor.callproc(name, args)
        results = tuple(_results_gen(cursor))
        cursor.close()
        self.release_con(connection)
        
        if not results: return None
        elif len(results) == 1: return results[0]
        else: return results
    
    def execute(self, query, *args):
        connection = self.get_con()
        cursor = DictCursor(connection)
        cursor.execute(query, args)
        results = tuple(_results_gen(cursor))
        cursor.close()
        self.release_con(connection)
        
        if not results: return None
        elif len(results) == 1: return results[0]
        else: return results
        

connections = Connections()
