import sys, os, hashlib, shutil
import render
import behemoth, trigen, skeleton
import dbimport, dbexport

"""
All colors are 4-tuples in the format (r,g,b,a), each value range 0.0-1.0
skeleton
    Map(lines, outside_lines, land_terrs, sea_terrs, countries=[])
        lines
            set of Lines. Renderer requires that it be a set, not a list.
        outside_lines
            Subset of lines that border water. Useful for optimizing thinsg like determining
            map size and for finding coastal land territories. See Line.left and Line.right.
        land_terrs
            land territories
        sea_terrs
            sea territories
        width, height, offset
            used for rendering
        find_bounds()
            
    Generator
        num_countries
        lines
            a set() by default
        outside_lines
        land_terrs
        sea_terrs
        width, height
            bounding box. optional.
        verify_data()
            checks adjacencies, makes sure line list is complete
    
    Country(color, name="America")
        cty_id, name, color, territories[], adjacencies[]
        size()
            returns length of territories list
        add(new_terr)
        remove(old_terr)
        absorb(new_terr)
        find_adjacent_countries()
        territory_bordering(other)
            returns a territory adjacent to other if country contains one
            otherwise return none

territory
    Territory
        country
            default None
        adjacencies, lines
            lists
        is_coastal, has_supply_center, is_sea
            booleans
        x, y
            text position
        pc_x, pc_y
            icon position
        ter_id
        name
        abbreviation
    
    SeaTerr(line)
        Pass it a single line. Reason: bay-generating code in behemoth uses it to check
        intersections and then bows it outward later.
    
    LandTerr(lines, color=(0.5, 0.5, 0.5, 1.0))
        color
        add_line(line)
        remove_line(line)
        add_triangle(x1...y3)
        find_adjacencies()
            Call when map is generated; finds adjacent territories via its lines
        place_piece()
            place icon based on text position
        place_text()
            Places the text label and icon. This will probably work well enough for
            sane shapes.
        color_self()
            set color to a variation of country's color
        point_inside()
            determine if a point is inside the territory

primitives
    Point(x, y)
        x, y
        get_tuple()
            returns (x, y)
        You can refer to point like p[0], p[1] as well.
    
    Line(a, b, left=None, right=None, color=(0,0,0,1))
        a, b
            end points
        left, right
            Neighboring lines. Only meaningful for border lines.
        normal
            angle perpendicular to angle formed by line against horizontal
        midpoint
        outside
            boolean, determines if line borders sea
        territories
            list containing one or two territories
        length
            starts at zero, set when get_length() called
        favored
            used in behemoth.py
        get_length()
            sets length if unset, returns it regardless

util
    point_inside_polygon(x, y, (x1, y1, x2, y2, x3, y3...))
    area_of_triangle(x1...y3)
    intersect(p1, p2, p3, p4)
        line 1 is p1 to p2, line 2 is p3 to p4
        There are more efficient ways to do this, but I could never make them work.
        
"""

def copy_to_unique_name(path, dest_dir=''):
    f = open(path)
    file_ext = os.path.splitext(path)[1]
    h = hashlib.sha1()
    h.update(f.read())
    hash = h.hexdigest()
    f.close()
    dest = os.path.join(dest_dir, hash+file_ext)
    shutil.copy(path, dest)
    return dest

def save_to_image(landmass):
    render.basic(landmass, "map_temp.png", True)
    return copy_to_unique_name("map_temp.png", 'map_images')    

if __name__ == "__main__":
    gen = behemoth.ContinentGenerator()
    if len(sys.argv) > 1:
        gen.base_distance = 40
        gen.verbose = False
        render.basic(gen.generate(), sys.argv[1])
        copy_to_unique_name(sys.argv[1])
        quit()
    import demo
    gen.verbose = True
    main_window = demo.MapGenWindow(gen)

