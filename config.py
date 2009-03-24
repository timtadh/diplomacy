import sys
sys.stderr = sys.stdout
import cgitb; cgitb.enable()
import config_db_con
import warnings
warnings.simplefilter('ignore', UserWarning)
import db
import mapgen.db as db2

db2.connections = db.connections


