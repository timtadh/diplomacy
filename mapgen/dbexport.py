"""
PyWorldGen dbexport
by Steve Johnson

This module provides methods to put a Map object into the diplomacy database.
"""

import queries as q

def rgb_to_hex(rgb_tuple):
    """Convert a tuple of 0-255 valued colors into #ffffff valued colors"""
    rgb_tuple = tuple([int(255*i) for i in rgb_tuple[:3]])
    hexcolor = '#%02x%02x%02x' % rgb_tuple
    return hexcolor

def incrementor(i=0):
    """Generator that yields increasing integers starting with i"""
    while 1:
        yield i
        i += 1

def next_id(tab, cur):
    """Get the next auto-incremented id from table 'tab'"""
    q = 'SELECT AUTO_INCREMENT FROM information_schema.TABLES WHERE TABLE_NAME = "%s";' % tab
    cur.execute(q)
    r = cur.fetchall()
    return r[0]['AUTO_INCREMENT']

def terr_to_dict(terr, map_id, get_id):
    """Put relevant Territory attributes in a dictionary"""
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
    """Put relevant Line attributes in a dictionary"""
    line_dict = {}
    if hasattr(line, 'ln_id'): return None
    line.ln_id = get_id.next()
    line_dict['ln_id'] = line.ln_id
    line_dict['x1'] = line.a.x
    line_dict['y1'] = line.a.y
    line_dict['x2'] = line.b.x
    line_dict['y2'] = line.b.y
    return line_dict

#The insert functions all work the same way. They build a string of comma-delimited data tuples
#from the relevant data and pass it to cur.execute() as part of a query string.
def insert_countries(countries, users, gam_id, cur):
    cty_fmt = '("%s", %s, "%s", "%s")'
    cty_strs = []
    get_id = incrementor(next_id('country', cur))
    print users
    for country, usr_id in zip(countries, users):
        country.cty_id = get_id.next()
        cty_strs.append(cty_fmt % (usr_id, gam_id, country.name, rgb_to_hex(country.color)))
    cur.execute(q.country + ",".join(cty_strs) + ";")

def insert_territories(terrs, map_id, ter_id, cur):
    terr_strs = []
    for terr in terrs:
        terr_strs.append(q.terr_fmt % terr_to_dict(terr, map_id, ter_id))
    cur.execute(q.territory + ",".join(terr_strs) + ";")

def insert_adjacencies(terrs, cur):
    adj_fmt = '(%s, %s)'
    adj_strs = []
    
    for terr in terrs:
        for terr2 in terr.adjacencies:
            adj_strs.append(adj_fmt % (terr.ter_id, terr2.ter_id))
    cur.execute(q.adjacent + ",".join(adj_strs) + ";")

def insert_triangles(terrs, cur):
    tri_fmt = '(%s, %s, %s, %s, %s, %s, %s)'
    tri_strs = []
    
    for terr in terrs:
        for tri in terr.triangles:
            tri_strs.append(tri_fmt % tuple([terr.ter_id]+list(tri)))
    cur.execute(q.triangle + ",".join(tri_strs) +";")

def insert_lines(lines, terrs, cur):
    """Handles both lines and the line-in-terr relation"""
    ln_fmt = '(%(x1)s, %(y1)s, %(x2)s, %(y2)s)'
    ln_strs = []
    get_id = incrementor(next_id('line', cur))
    
    for ln in lines:
        ln_strs.append(ln_fmt % line_to_dict(ln, get_id))
    cur.execute(q.line + ",".join(ln_strs) + ";")
    
    ln_fmt = '(%s, %s)'
    ln_strs = []
    for terr in terrs:
        for ln in terr.lines:
            if ln not in lines:
                print 'weirdness with', ln
            ln_strs.append(ln_fmt % (terr.ter_id, ln.ln_id))
    cur.execute(q.ln_terr + ",".join(ln_strs) + ";")

def insert_suppliers(terrs, cur):
    sup_fmt = "(%s, %s)"
    sup_strs = []
    
    for terr in terrs:
        if terr.has_supply_center and terr.country != None:
            sup_strs.append(sup_fmt % (terr.ter_id, terr.country.cty_id))
    cur.execute(q.supplier + ",".join(sup_strs) + ";")

def export(cur, users, game_map, pic, gam_id):
    game_map.map_id = next_id("map", cur)
    cur.execute(q.gmap % (game_map.name, pic))
    insert_countries(game_map.countries, users, gam_id, cur)
    
    all_terrs = game_map.land_terrs|game_map.sea_terrs
    ter_id = incrementor(next_id('territory', cur))
    insert_territories(all_terrs, game_map.map_id, ter_id, cur)
    insert_adjacencies(all_terrs, cur)
    insert_triangles(game_map.land_terrs, cur)
    insert_lines(set(game_map.lines), all_terrs, cur)
    insert_suppliers(all_terrs, cur)
