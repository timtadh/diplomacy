import sys
sys.stderr = sys.stdout
import cgitb; cgitb.enable()
import config_db_con
import warnings
warnings.simplefilter('ignore', UserWarning)
import twik.db as db
import mapgen.db as db2
for attr in dir(db):
    db2.__setattr__(attr, db.__getattribute__(attr))

