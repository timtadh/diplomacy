import cookie_session, user_manager
import db

HOST = "localhost"
PORT = 3306
USER = 'diplomacy'
PASSWD = "d!plomacy12"
DB = "diplomacy"

cookie_session.HOST = HOST
cookie_session.PORT = PORT
cookie_session.USER = USER
cookie_session.PASSWD = PASSWD
cookie_session.DB = DB

user_manager.HOST = HOST
user_manager.PORT = PORT
user_manager.USER = USER
user_manager.PASSWD = PASSWD
user_manager.DB = DB

db.HOST = HOST
db.PORT = PORT
db.USER = USER
db.PASSWD = PASSWD
db.DB = DB
