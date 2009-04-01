'''
Author: Tim Henderson

configures db module

Usage:
    import config_db_con
    import db
    con = db.connections.get_con()
    db.connections.release_con(con)
'''

import twik.db as db

HOST = "localhost"
PORT = 3306
USER = 'diplomacy'
PASSWD = "d!plomacy12"
DB = "diplomacy"

db.HOST = HOST
db.PORT = PORT
db.USER = USER
db.PASSWD = PASSWD
db.DB = DB
