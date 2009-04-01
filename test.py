import twik.db as db
import config_db_con
from MySQLdb.cursors import DictCursor

con = db.connections.get_con()
cur = DictCursor(con)
cur.callproc('user_data_byemail', ('tim.tadh@gmail.com',))
r = cur.fetchall()
print r



cur.close()
db.connections.release_con(con)
