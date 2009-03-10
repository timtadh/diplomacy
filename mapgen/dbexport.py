queries = {
    'land_terr': 'INSERT INTO territory '\
        '(map_id, name, abbrev, piece_x, piece_y, label_x, label_y, ter_type, supply, coastal)'\
        ' VALUES (%(map_id)s, "%(name)s", "%(abbrev)s", %(piece_x)s, %(piece_y)s, '\
        '%(label_x)s, %(label_y)s, "land", %(supply)s, %(coastal)s)',
    'sea_terr': 'INSERT INTO territory '\
        '(map_id, name, abbrev, piece_x, piece_y, label_x, label_y, ter_type, supply, coastal)'\
        ' VALUES (%(map_id)s, "%(name)s", "%(abbrev)s", %(piece_x)s, %(piece_y)s, '\
        '%(label_x)s, %(label_y)s, "sea", %(supply)s, %(coastal)s)'
}

def rgb_to_hex(rgb_tuple):
    rgb_tuple = tuple([int(255*i) for i in rgb_tuple[:3]])
    hexcolor = '#%02x%02x%02x' % rgb_tuple
    return hexcolor

def incrementor(i=0):
    while 1:
        yield i
        i += 1

def next_id(tab, cur):
    q = 'SELECT AUTO_INCREMENT FROM information_schema.TABLES WHERE TABLE_NAME = "%s";' % tab
    cur.execute(q)
    r = cur.fetchall()
    return r[0]['AUTO_INCREMENT']

def terr_to_dict(terr, map_id, get_id):
    terr_dict = {}
    terr.ter_id = get_id.next()
    terr_dict['ter_id'] = terr.ter_id
    terr_dict['map_id'] = map_id
    terr_dict['name'] = terr.abbreviation*3
    terr_dict['abbrev'] = terr.abbreviation
    terr_dict['piece_x'] = terr.pc_x
    terr_dict['piece_y'] = terr.pc_y
    terr_dict['label_x'] = terr.x
    terr_dict['label_y'] = terr.y
    if terr.has_supply_center:
        terr_dict['supply'] = 'TRUE'
    else:
        terr_dict['supply'] = 'FALSE'
    if terr.is_coastal:
        terr_dict['coastal'] = 'TRUE'
    else:
        terr_dict['coastal'] = 'FALSE'
    return terr_dict

def line_to_dict(line, get_id):
    line_dict = {}
    if hasattr(line, 'ln_id'): return None
    line.ln_id = get_id.next()
    line_dict['ln_id'] = line.ln_id
    line_dict['x1'] = line.a.x
    line_dict['y1'] = line.a.y
    line_dict['x2'] = line.b.x
    line_dict['y2'] = line.b.y
    return line_dict

def insert_countries(countries, usr_id, cur):
    q = 'INSERT INTO country (usr_id, name, color) VALUES '
    cty_fmt = '("%s", "%s", "%s")'
    cty_strs = []
    get_id = incrementor(next_id('country', cur))
    for country in countries:
        country.cty_id = get_id.next()
        cty_strs.append(cty_fmt % (usr_id, country.name, rgb_to_hex(country.color)))
        print "<br>"+str(country.cty_id)
    q += ",".join(cty_strs)
    #print q
    cur.execute(q)

def insert_territories(terrs, map_id, ter_id, cur):
    q = 'INSERT INTO territory (map_id, name, abbrev, piece_x, piece_y, '\
        'label_x, label_y, ter_type, supply, coastal) VALUES '
    terr_fmt =  '(%(map_id)s, "%(name)s", "%(abbrev)s", %(piece_x)s, %(piece_y)s, '\
                '%(label_x)s, %(label_y)s, "land", %(supply)s, %(coastal)s)'
    terr_strs = []
    for terr in terrs:
        terr_strs.append(terr_fmt % terr_to_dict(terr, map_id, ter_id))
    q += ",".join(terr_strs)
    print q
    cur.execute(q)

def export(cur, usr_id, game_map, pic):
    game_map.map_id = next_id("map", cur)
    q_map = 'INSERT INTO map (world_name, pic) VALUES ("%s", "%s");'
    print "Map ID: "+str(game_map.map_id)+"<br>"
    cur.execute(q_map % (game_map.name, pic))
    insert_countries(game_map.countries, usr_id, cur)
    
    all_terrs = game_map.land_terrs|game_map.sea_terrs
    ter_id = incrementor(next_id('territory', cur))
    insert_territories(all_terrs, game_map.map_id, ter_id, cur)
    return
    
    for terr in game_map.land_terrs:
        print queries['land_terr'] % terr_to_dict(terr, game_map.map_id, ter_id)
    
    for terr in game_map.sea_terrs:
        print queries['land_terr'] % terr_to_dict(terr, game_map.map_id, ter_id)
    
    for terr in game_map.land_terrs|game_map.sea_terrs:
        for terr2 in terr.adjacencies:
            print terr.ter_id, terr2.ter_id
    
    for terr in game_map.land_terrs:
        for tri in terr.triangles:
            print tri
    
    game_map.lines = set(game_map.lines)
    for ln in game_map.lines:
        print line_to_dict(ln)
    
    for terr in game_map.land_terrs|game_map.sea_terrs:
        for ln in terr.lines:
            if ln not in game_map.lines:
                print 'weirdness with', ln
            print terr.ter_id, ln.ln_id
