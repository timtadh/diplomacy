"""
PyWorldGen dbimport
by Steve Johnson

This module provides methods to get a Landmass from the database. It does not fill in all data, just the things you need for drawing.
"""

import db, skeleton, territory, primitives

def hex_to_rgb(colorstring):
    """ convert #RRGGBB to an (R, G, B) tuple """
    colorstring = colorstring.strip()
    if colorstring[0] == '#': colorstring = colorstring[1:]
    if len(colorstring) != 6:
        raise ValueError, "input #%s is not in #RRGGBB format" % colorstring
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    r, g, b = [n/255.0 for n in (r, g, b)]
    return (r, g, b, 1.0)

def get_countries(con, gam_id):    
    countries = {}
    cur = db.DictCursor(con)
    cur.callproc('countries_in_game', (gam_id,))
    r = cur.fetchall()
    for country in r:
        new_country = skeleton.Country(
            hex_to_rgb(country['color']), country['name'], country['cty_id'])
        countries[new_country.cty_id] = new_country
    cur.close()
    return countries

def get_terrs(con, gam_id, countries):
    terrs = {}
    cur = db.DictCursor(con)
    cur.callproc('terrs_in_game', (gam_id,))
    r = cur.fetchall()
    for terr in r:
        new_terr = dict_to_terr(terr, countries)
        terrs[terr['ter_id']] = new_terr
    cur.close()
    return terrs

def dict_to_terr(terr_dict, countries):
    """Put relevant Territory attributes in a dictionary"""
    if terr_dict['ter_type'] == 'land':
        new_terr = territory.LandTerr()
    else:
        new_terr = territory.SeaTerr()
    new_terr.ter_id = terr_dict['ter_id']
    new_terr.name = terr_dict['name']
    new_terr.abbreviation = terr_dict['abbrev']
    new_terr.pc_x = terr_dict['piece_x']
    new_terr.pc_y = terr_dict['piece_y']
    new_terr.x = terr_dict['label_x']
    new_terr.y = terr_dict['label_y']
    new_terr.has_supply_center = terr_dict['supply']
    new_terr.is_coastal = terr_dict['coastal']
    return new_terr

def add_shapes_to_terr(con, terr):
    cur = db.DictCursor(con)
    cur.callproc('lines_in_terr', (terr.ter_id,))
    r = cur.fetchall()
    for line in r:
        terr.lines.append(
            primitives.Line(
                primitives.Point(line['x1'], line['y1']),
                primitives.Point(line['x2'], line['y2'])
            )
        )
    cur.close()
    cur = db.DictCursor(con)
    cur.callproc('triangles_in_terr', (terr.ter_id,))
    r = cur.fetchall()
    for tri in r:
        terr.add_triangle(tri['x1'], tri['y1'], tri['x2'], tri['y2'], tri['x3'], tri['y3'])
    cur.close()

def get(con, gam_id):
    cur = db.DictCursor(con)
    cur.callproc('map_data_for_game', (gam_id,))
    map_id = cur.fetchall()[0]['map_id']
    cur.close()
    
    countries = get_countries(con, gam_id)
    terrs = get_terrs(con, gam_id, countries)
    
    lines = []
    for ter_id, terr in terrs.iteritems():
        add_shapes_to_terr(con, terr)
        lines.extend(terr.lines)
    
    for cty_id, country in countries.iteritems():
        cur = db.DictCursor(con)
        cur.callproc('suppliers_for_country', (cty_id,))
        r = cur.fetchall()
        for tdict in r:
            terrs[tdict['ter_id']].country = country
        cur.close()

    land_terrs = []
    sea_terrs = []
    for ter_id, terr in terrs.iteritems():
        if terr.is_sea:
            sea_terrs.append(terr)
        else:
            land_terrs.append(terr)
    
    for terr in land_terrs:
        terr.color_self()
    new_map = skeleton.Map(lines, lines, land_terrs, sea_terrs, countries.values())
    new_map.find_bounds()
    return new_map
