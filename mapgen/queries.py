gmap =      'INSERT INTO map (world_name, pic) VALUES ("%s", "%s");'

country =   'INSERT INTO country (usr_id, name, color) VALUES '

territory = 'INSERT INTO territory (map_id, name, abbrev, piece_x, piece_y, '\
            'label_x, label_y, ter_type, supply, coastal) VALUES '
terr_fmt =  '(%(map_id)s, "%(name)s", "%(abbrev)s", %(piece_x)s, %(piece_y)s, '\
            '%(label_x)s, %(label_y)s, "land", %(supply)s, %(coastal)s)'

adjacent =  'INSERT INTO adjacent (ter_id, adj_ter_id) VALUES '

triangle =  'INSERT INTO triangle (ter_id, x1, y1, x2, y2, x3, y3) VALUES '

line =      'INSERT INTO line (x1, y1, x2, y2) VALUES '

ln_terr =   'INSERT INTO ter_ln_relation (ter_id, ln_id) VALUES '

supplier =  'INSERT INTO supplier (ter_id, cty_id) VALUES '