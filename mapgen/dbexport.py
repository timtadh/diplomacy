queries = {
    'map': 'INSERT INTO map (world_name, pic) VALUES ("%s", "%s");',
    'country': 'INSERT INTO country (usr_id, name, color) VALUES ("%s", "%s", "%s")',
    'land_terr': 'INSERT INTO territory '\
        '(map_id, name, abbrev, piece_x, piece_y, label_x, label_y, ter_type, supply, coastal)'\
        ' VALUES (%(map_id)s, "%(name)s", "%(abbrev)s", %(piece_x)s, %(piece_y)s, '\
        '%(label_x)s, %(label_y)s, "land", %(supply)s, %(coastal)s)',
    'sea_terr': 'INSERT INTO territory '\
        '(map_id, name, abbrev, piece_x, piece_y, label_x, label_y, ter_type, supply, coastal)'\
        ' VALUES (%(map_id)s, "%(name)s", "%(abbrev)s", %(piece_x)s, %(piece_y)s, '\
        '%(label_x)s, %(label_y)s, "sea", %(supply)s, %(coastal)s)',
    'last_insert': 'SELECT AUTO_INCREMENT FROM information_schema.TABLES WHERE TABLE_NAME = "%s";'
}

def rgb_to_hex(rgb_tuple):
    rgb_tuple = tuple([int(255*i) for i in rgb_tuple[:3]])
    hexcolor = '#%02x%02x%02x' % rgb_tuple
    return hexcolor

def incrementor():
    #SELECT LAST_INSERT_ID();
    i = 0
    while 1:
        i += 1
        yield i
get_id = incrementor()

def terr_to_dict(terr, map_id):
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

def line_to_dict(line):
    line_dict = {}
    if hasattr(line, 'ln_id'): return None
    line.ln_id = get_id.next()
    line_dict['ln_id'] = line.ln_id
    line_dict['x1'] = line.a.x
    line_dict['y1'] = line.a.y
    line_dict['x2'] = line.b.x
    line_dict['y2'] = line.b.y
    return line_dict

def export(game_map, name, pic):
    print queries['map'] % (name, pic)
    map_id = 10
    
    test_usr = "7dd468870481a588453c0dbd031376932d6adea90e088ab3b3d21afe9fd17a5b"
    cty_str = queries['country']
    cty_fmt = '("%s", "%s", "%s")'
    cty_fmt_strs = []
    for country in game_map.countries:
        #print queries['country'] % (test_usr, country.name, rgb_to_hex(country.color))
        country.cty_id = get_id.next()
        print country.cty_id, country.name, rgb_to_hex(country.color)
    
    all_terrs = game_map.land_terrs|game_map.sea_terrs
    
    for terr in game_map.land_terrs:
        print queries['land_terr'] % terr_to_dict(terr, map_id)
    
    for terr in game_map.sea_terrs:
        print queries['land_terr'] % terr_to_dict(terr, map_id)
    
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
