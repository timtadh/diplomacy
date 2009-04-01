import twik.default_config
import twik.db as db
import mapgen.db as db2
for attr in dir(db):
    db2.__setattr__(attr, db.__getattribute__(attr))

