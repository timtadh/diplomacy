import config, db, functools

moving_orders = [1, 2, 3, 4, 6] #order_types that use destinations

get_con = db.connections.get_con
release = db.connections.release_con
dict_cursor = db.DictCursor