import sys, os, math, random, sets, util, render, hashlib, shutil
from primitives import *
from territory import *

PICK_TRIANGLE = 0
AVERAGE_POINTS = 1
LARGEST_TRIANGLE = 2
country_colors = [
    (1.0, 0.0, 0.0, 1.0), (1.0, 0.5, 0.0, 1.0), (1.0, 1.0, 0.0, 1.0), 
    (0.0, 1.0, 0.0, 1.0), (0.0, 1.0, 1.0, 1.0), (0.7, 0.0, 1.0, 1.0), 
    (1.0, 0.5, 1.0, 1.0), (0.7, 0.3, 0.0, 1.0)
]

random.shuffle(country_colors)

grey_colors = []
c = 1.0
while c > 0.5:
    grey_colors.append((c,c,c,1.0))
    c -= 0.015
    
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
    render.basic(landmass, "map_temp.png")
    return copy_to_unique_name("map_temp.png", 'map_images')

class Country(object):
    def __init__(self, color):
        self.color = color
        self.territories = []
        self.adjacencies = []
    
    def size(self):
        return len(self.territories)
    
    def add(self, new_terr):
        if new_terr in self.territories: return
        self.territories.append(new_terr)
        new_terr.country = self
    
    def remove(self, old_terr):
        if old_terr in self.territories:
            self.territories.remove(old_terr)
    
    def absorb(self, new_terr):
        new_terr.country.remove(new_terr)
        self.add(new_terr)
    
    def find_adjacent_countries(self):
        self.adjacencies = []
        for terr in self.territories:
            terr.country = self
            for terr2 in terr.adjacencies:
                if terr2.country not in self.adjacencies:
                    if terr2.country != self:
                        self.adjacencies.append(terr2.country)
        self.adjacencies.sort()
    
    def territory_bordering(self, other):
        if other not in self.adjacencies:
            return None
        possibilities = []
        for terr in self.territories:
            for terr2 in terr.adjacencies:
                if other == terr2.country:
                    return terr
                    if terr in possibilities:
                        terr.awesomeness += 1
                    else:
                        possibilities.append(terr)
                        terr.awesomeness = 1
        random.shuffle(possibilities)
        r = None
        for p in possibilities:
            r = p
            if p.awesomeness > 1: return p
        return r
    
    def __repr__(self):
        return str(self.color)
    

class LandMass(object):
    def __init__(self, lines, outside_lines, territories, valid=True):
        super(LandMass, self).__init__()
        self.lines = lines
        self.outside_lines = outside_lines
        self.territories = territories
        self.valid = valid
    

class ContinentGenerator(object):
    def __init__(self, num_countries=7, verbose=False):
        self.num_countries = num_countries
        self.balance_countries = True
        self.territories_per_player = 10
        self.verbose = verbose
        self.wiggle = math.pi/6
        self.base_distance = 30.0
        self.primitive_ratio = 0.7
        self.lines = []
        self.outside_lines = []
        self.territories = []
        self.num_lines = 128*num_countries
        self.check_collisions = True
        self.offset = (0,0)
        self.width, self.height = 0, 0
    
    def generate(self):
        if self.num_lines <= 0:
            self.num_lines = 900
        self.lines = []
        self.outside_lines = []
        self.territories = []
        self.which_color = 0
        
        if self.verbose: print "generating..."
        self.generate_initial_polygon()
        self.generate_iteratively()
        
        if self.verbose: print "combining primitives..."
        len_outside = len(self.outside_lines)
        self.inside_lines = [
            line for line in self.lines if line not in self.outside_lines
        ]
        i = 0
        while len(self.territories) > len_outside * self.primitive_ratio:
            self.combine_random()
        
        self.remove_floating_lines()
        self.check_map()
        self.process_objects()
        self.make_countries()
        self.make_seas()
        
        if self.verbose: print "done"
        return self.get_landmass()
    
    def get_landmass(self, valid=True):
        lm = LandMass(self.lines, self.outside_lines, self.territories, valid)
        lm.width, lm.height = int(self.width), int(self.height)
        lm.offset = self.offset
        return lm
    
    def generate_iteratively(self):
        while self.num_lines > 0:
            base_line = random.choice(self.outside_lines)
            if not base_line.favored:
                base_line = random.choice(self.outside_lines)
            if self.check_concave(base_line):
                if self.check_concave(base_line.left):
                    self.expand_line(base_line)
    
    def generate_initial_polygon(self):
        a = 0
        r = self.get_radius()
        first_point = Point(r, 0)
        last_point = first_point
        line_num = 0
        triangles = []
        while a < math.pi*2-math.pi/5:
            a += random.random()*math.pi*(0.666-0.2)+math.pi/5
            if a < math.pi*2-math.pi/5:
                r = self.get_radius()
                new_point = Point(r*math.cos(a), r*math.sin(a))
                self.num_lines -= 1
            else:
                new_point = first_point
            new_line = Line(last_point, new_point)
            if line_num > 0:
                new_line.left = self.lines[line_num-1]
                self.lines[line_num-1].right = new_line
            self.lines.append(new_line)
            self.outside_lines.append(new_line)
            triangles.append(
                (0, 0, last_point.x, last_point.y, new_point.x, new_point.y)
            )
            last_point = new_point
            line_num += 1
        self.lines[line_num-1].right = self.lines[0]    
        self.lines[0].left = self.lines[line_num-1]
        self.territories = [LandTerr(self.lines, self.get_color(0))]
        self.territories[0].triangles = triangles
    
    def get_radius(self):
        return random.random()*self.base_distance*0.3 + self.base_distance*0.7
    
    def get_color(self, n=-1):
        if n == -1: n = self.which_color
        n = n % len(grey_colors)
        c = grey_colors[n]
        self.which_color += 1
        return c
    
    def angle_between_line_and_next(self, line):    
        a1 = math.atan2(line.right.b.y-line.b.y, line.right.b.x-line.b.x)
        a2 = math.atan2(line.a.y-line.b.y, line.a.x-line.b.x)
        return (a1 - a2) % (math.pi*2)
    
    def get_largest_territory(self):
        largest = self.territories[0]
        largest_count = len(self.territories[0].triangles)
        for terr in self.territories:
            if len(terr.triangles) > largest_count:
                largest = terr
        return largest
    
    def sort_countries(self):
        self.countries.sort(lambda x, y: x.size()-y.size())
    
    def check_intersections(self, a, b):
        if not self.check_collisions: return True
        for line in self.outside_lines:
            if util.intersect(a, b, line.a, line.b):
                return False
        return True
    
    def check_point(self, point):
        if not self.check_collisions: return True
        for territory in self.territories:
            for tri in territory.triangles:
                if util.point_inside_polygon(point.x, point.y, tri):
                    return False
        return True
    
    def check_concave(self, line):
        if line.a == line.right.b:
            self.remove_floating_lines()
            if self.verbose: print 'weird line error'
            return False
        if not self.check_intersections(line.a, line.right.b): return False
        if self.angle_between_line_and_next(line) > math.pi*0.75: return True
        new_line = Line(line.a, line.right.b, line.left, line.right.right)
        #if not self.check_point(new_line.midpoint): return False
        line.left.right = new_line
        line.right.right.left = new_line
        self.lines.append(new_line)
        self.outside_lines.append(new_line)
        self.outside_lines.remove(line)
        self.outside_lines.remove(line.right)
        self.num_lines -= 1
        
        rn = random.randint(0, 100)
        can_expand = True
        can_expand = False
        for s in line.territories:
            if len(s.lines) > 8: can_expand = False
        if rn >= 50 and can_expand:
            self.lines.remove(line)
            for s in line.territories:
                s.remove_line(line)
                s.add_line(new_line)
                s.add_line(line.right)
                s.add_triangle(
                    line.a.x, line.a.y, line.b.x, line.b.y, 
                    line.right.b.x, line.right.b.y
                )
        else:
            rn = random.randint(0, 100)
            can_expand = True
            for s in line.right.territories:
                if len(s.lines) > 8: can_expand = False
            if rn >= 50 and can_expand:
                self.lines.remove(line.right)
                for s in line.right.territories:
                    s.remove_line(line.right)
                    s.add_line(new_line)
                    s.add_line(line)
                    s.add_triangle(
                        line.a.x, line.a.y, line.b.x, line.b.y, 
                        line.right.b.x, line.right.b.y
                    )
            else:
                new_territory = LandTerr(
                    [line, line.right, new_line], self.get_color()
                )
                new_territory.dist = line.territories[0].dist
                new_territory.dist += line.right.territories[0].dist
                new_territory.dist = int(new_territory.dist/2) + 1
                new_territory.color = self.get_color(new_territory.dist)
                self.territories.append(new_territory)
                new_territory.add_triangle(
                    line.a.x, line.a.y, line.b.x, line.b.y, 
                    line.right.b.x, line.right.b.y
                )
        return False
    
    def make_new_tri(self, base_line, new_point, erase_old=False):
        nl1 = Line(base_line.a, new_point, base_line.left)
        nl2 = Line(new_point, base_line.b, nl1, base_line.right)
        nl1.right = nl2
        base_line.left.right = nl1
        base_line.right.left = nl2
        self.outside_lines.remove(base_line)
        self.outside_lines.append(nl1)
        self.outside_lines.append(nl2)
        self.lines.append(nl1)
        self.lines.append(nl2)
        self.num_lines -= 2
        
        if erase_old:
            self.lines.remove(base_line)
            for s in base_line.territories:
                s.remove_line(base_line)
                s.add_line(nl1)
                s.add_line(nl2)
                s.add_triangle(
                    base_line.a.x, base_line.a.y, base_line.b.x, base_line.b.y, 
                    new_point.x, new_point.y
                )
        else:
            new_territory = LandTerr([nl1, nl2, base_line], self.get_color())
            self.territories.append(new_territory)
            new_territory.add_triangle(
                base_line.a.x, base_line.a.y, base_line.b.x, base_line.b.y, 
                new_point.x, new_point.y
            )
            new_territory.dist = base_line.territories[0].dist+1
            new_territory.color = self.get_color(new_territory.dist)
        return nl1, nl2
    
    def expand_to_triangle(self, base_line):
        r = self.get_radius()
        a = base_line.normal + random.random()*self.wiggle-self.wiggle/2
        nx = r*math.cos(a)
        ny = r*math.sin(a)
        new_point = Point(
            base_line.midpoint.x+nx,
            base_line.midpoint.y+ny
        )
        test_point = Point(
            base_line.midpoint.x+nx*2, 
            base_line.midpoint.y+ny*2
        )
        if not self.check_intersections(base_line.a, test_point): return
        if not self.check_intersections(test_point, base_line.b): return
        
        rn = random.randint(0, 100)
        can_expand = True
        can_expand = False
        for s in base_line.territories:
            if len(s.lines) > 8: can_expand = False
        
        self.make_new_tri(base_line, new_point, (rn >= 50 and can_expand))
    
    def expand_to_trapezoid(self, line):
        r = self.get_radius()
        l = line.get_length() * 0.8 + random.random()*0.4
        l = max(l, 10)
        nx = r*math.cos(line.normal)
        ny = r*math.sin(line.normal)
        mx = line.midpoint.x + nx
        my = line.midpoint.y + ny
        mxb = line.midpoint.x + nx*2
        myb = line.midpoint.y + ny*2
        ax = l*0.5*math.cos(line.normal+math.pi/2)
        ay = l*0.5*math.sin(line.normal+math.pi/2)
        p1 = Point(mx - ax, my - ay)
        p2 = Point(mx + ax, my + ay)
        p1b = Point(mxb - ax*1.25, myb - ay*1.25)
        p2b = Point(mxb + ax*1.25, myb + ay*1.25)
        
        if not self.check_intersections(line.a, p1): return
        if not self.check_intersections(line.b, p2): return
        if not self.check_intersections(p1, p2): return
        
        nl1, nl2 = self.make_new_tri(line, p1, False)
        nl3, nl4 = self.make_new_tri(nl2, p2, True)
        nl3.favored = True
    
    def expand_line(self, base_line):
        expand_dict = {
            0: self.expand_to_triangle,
            1: self.expand_to_trapezoid,
            2: self.expand_to_trapezoid
        }
        expand_dict[random.randint(0,len(expand_dict)-1)](base_line)
    
    def find_adjacent_territory(self, terr):
        for line in terr.lines:
            for terr2 in line.territories:
                if terr2 != terr:
                    return terr2
    
    def check_map(self):
        if self.verbose: print "checking..."
        #Removes territories that are entirely surrounded by a single territory
        #or are made of only one triangle
        absorbed = []
        for terr in self.territories:
            check = True
            for line in terr.lines:
                if len(line.territories) != 2:
                    check = False
            if check:
                absorb = True
                surr_terr = terr.lines[0].territories[1]
                for line in terr.lines:
                    if line.territories[1] != surr_terr:
                        absorb = False
                if absorb:
                    if terr.lines[0] not in absorbed:
                        self.combine(surr_terr, terr)
                        absorbed.append(terr)
        to_kill = [
            terr for terr in self.territories if len(terr.triangles) == 1
        ]
        li = len(self.territories)
        for terr in to_kill:
            self.combine(self.find_adjacent_territory(terr), terr)
        if self.verbose: print "removed", len(to_kill), "tiny territories"
    
    def process_objects(self):
        #Place ids and set bounding box
        ids = range(0, len(self.territories))
        for territory, t_id in zip(self.territories, ids):
            territory.place_capital()
            territory.id = t_id
        l_id = 0
        min_x = 0
        min_y = 0
        max_x = 0
        max_y = 0
        for line in self.lines:
            line.id = l_id
            min_x = min(line.a.x, min_x)
            min_x = min(line.b.x, min_x)
            min_y = min(line.a.y, min_y)
            min_y = min(line.b.y, min_y)
            max_x = max(line.a.x, max_x)
            max_x = max(line.b.x, max_x)
            max_y = max(line.a.y, max_y)
            max_y = max(line.b.y, max_y)
            l_id += 1
        self.offset = (-min_x, -min_y)
        self.width = max_x - min_x
        self.height = max_y - min_y
        
        if self.verbose: print "generating adjacencies..."
        for terr in self.territories:
            terr.find_adjacencies()
    
    def territory_is_outside(self, terr):
        for line in terr.lines:
            if line in self.outside_lines:
                return True
        return False
    
    def unbalanced_countries(self):
        self.sort_countries()
        q1 = self.num_countries/4.0
        q2 = int(q1*2)
        q3 = int(q1*3)
        q1 = int(q1)
        quant1 = self.countries[:q1]
        quant2 = self.countries[q1:q2]
        quant3 = self.countries[q2:q3]
        median = util.median(self.countries)
        mid50 = len(quant2[-1].territories) - len(quant2[0].territories)
        min_terrs = median - mid50*1.5
        max_terrs = median + mid50*1.5
        small = [c for c in self.countries if len(c.territories) < min_terrs]
        large = [c for c in self.countries if len(c.territories) > max_terrs]
        
        if len(self.countries[0].territories)*1.5 \
                < len(self.countries[-1].territories):
            if self.countries[0] not in small:
                small.append(self.countries[0])
            if self.countries[-1] not in large:
                large.append(self.countries[-1])
        return small, large
    
    def remove_lone_territories(self):
        worked = False
        for terr in self.territories:
            terr.find_adjacencies()
            if not terr.country in terr.adjacent_countries:
                for country in terr.adjacent_countries:
                    if country != terr.country:
                        country.absorb(terr)
                        worked = True
                        break
        return worked
    
    def make_countries(self):
        if self.verbose: print 'forming countries...'
        remaining_terrs = list(sets.Set(self.territories))
        
        self.countries = [
            Country(country_colors[i]) for i in range(self.num_countries)
        ]
        start_line = self.outside_lines[0]
        this_terr = start_line.territories[0]
        outside_terrs = [this_terr]
        this_line = start_line.right
        while this_line != start_line:
            if this_line.territories[0] != this_terr:
                this_terr = this_line.territories[0]
                outside_terrs.append(this_terr)
            this_line = this_line.right
        
        terrs_per_country = len(outside_terrs)/self.num_countries
        i = 0
        for country in self.countries:
            this_terr = outside_terrs[i]
            j = 0
            while this_terr not in remaining_terrs:
                this_terr = outside_terrs[i + j]
                j += 1
            country.add(this_terr)
            remaining_terrs.remove(this_terr)
            i += terrs_per_country
        
        terrs_left = len(remaining_terrs)
        
        worked = True
        while terrs_left > 0 and worked:
            worked = False
            self.sort_countries()
            for country in self.countries:
                adjacencies = []
                for terr in country.territories:
                    adjacencies.extend(terr.adjacencies)
                adjacencies = list(sets.Set(adjacencies))
                random.shuffle(adjacencies)
                country.expand_options = []
                for terr in adjacencies:
                    if terr in remaining_terrs and terr.country == None:
                        if terr not in country.territories:
                            remaining_terrs.remove(terr)
                            country.add(terr)
                            terrs_left -= 1
                            worked = True
                            break
        
        small, large = self.unbalanced_countries()
        i = 0
        while len(small) > 0 and i < 1000:
            i += 1
            for country in small:
                try:
                    country.find_adjacent_countries()
                    if len(large) > 0:
                        if random.randint(0,1) == 0:
                            target = large[-1]
                            to_take = target.territories[0]
                        else:
                            target = country.adjacencies[-1]
                            target.find_adjacent_countries()
                            to_take = target.territory_bordering(country)
                    else:
                        target = country.adjacencies[-1]
                        target.find_adjacent_countries()
                        to_take = target.territory_bordering(country)
                    if to_take != None:
                        target.remove(to_take)
                        country.add(to_take)
                except:
                    pass #fail silently, mrawrg
            small, large = self.unbalanced_countries()
        if i == 1000: print 'balance fail'
        
        worked = True
        while worked:
            worked = self.remove_lone_territories()
        
        self.merge_in_countries()
        self.color_territories()
        self.place_supply_centers()
    
    def merge_in_countries(self):
        self.sort_countries()
        country = self.countries[-1]
        bad_countries = [
            c for c in self.countries if c.size() > self.territories_per_player
        ]
        for country in bad_countries:
            while country.size() > self.territories_per_player:
                for terr in self.territories:
                    terr.find_adjacencies()
                country.territories.sort(
                    lambda x, y: len(x.adjacencies) - len(y.adjacencies)
                )
                to_remove = country.territories[0]
                to_remove.adjacencies.sort(
                    lambda x, y: len(x.adjacencies) - len(y.adjacencies)
                )
                absorb_candidates = [
                    t for t in to_remove.adjacencies if t.country == country
                ]
                if len(absorb_candidates) > 0:
                    to_absorb = absorb_candidates[0]
                    if self.verbose:
                        print to_remove, absorb_candidates, country
                    self.combine(to_absorb, to_remove)
                    country.territories.remove(to_remove)
                else:
                    self.remove_lone_territories()
    
    def place_supply_centers(self):
        total_supply_centers = int(5.14*self.num_countries)+1
        centers_per_country = total_supply_centers/self.num_countries
        this_country = 0
        random.shuffle(self.countries)
        this_terr = random.choice(self.countries[0].territories)
        while total_supply_centers > 0:
            while this_terr.has_supply_center:
                this_terr = random.choice(
                    self.countries[this_country].territories
                )
            this_terr.has_supply_center = True
            total_supply_centers -= 1
            this_country = (this_country + 1) % len(self.countries)
    
    def make_seas(self):
        if self.verbose: print 'finding bays...'
        stupid_terr = LandTerr([])
        self.territories.append(stupid_terr)
        max_seeks = len(self.outside_lines)/3
        start_line = self.outside_lines[0]
        line = start_line.right
        bay_starts = []
        bay_lines = []
        while line != start_line:
            if self.angle_between_line_and_next(line) < math.pi*0.4:
                bay_starts.append(line)
            line = line.right
        for line in bay_starts:
            line_left = line
            line_right = line
            best_line_left = None
            best_line_right = None
            i = 0
            last_i = 0
            while i < max_seeks:
                i += 1
                line_right = line_right.right
                test_line = Line(line_left.a, line_right.a)
                if self.check_intersections(test_line.a, test_line.b) and \
                        self.check_point(test_line.midpoint):
                    best_line_left, best_line_right = line_left, line_right
                    last_i = i
                line_left = line_left.left
                test_line = Line(line_left.a, line_right.a)
                if self.check_intersections(test_line.a, test_line.b) and \
                        self.check_point(test_line.midpoint):
                    best_line_left, best_line_right = line_left, line_right
                    last_i = i
            if best_line_left != None:
                left = best_line_left
                right = best_line_right
                last_i_2 = 0
                worked = True
                while worked:
                    worked = False
                    i = 0
                    while i < 5:
                        left = left.left
                        test_line = Line(left.a, best_line_right.a)
                        if self.check_intersections(test_line.a, test_line.b) \
                                and self.check_point(test_line.midpoint):
                                best_line_left = left
                                last_i_2 = last_i + i
                                worked = True
                        i += 1
                    last_i = last_i_2
                    i = 0
                    while i < 5:
                        right = right.right
                        test_line = Line(best_line_left.a, right.a)
                        if self.check_intersections(test_line.a, test_line.b) \
                                    and self.check_point(test_line.midpoint):
                                best_line_right = right
                                last_i_2 = last_i + i
                                worked = True
                        i += 1
                new_line = Line(
                    best_line_left.a, best_line_right.a, 
                    best_line_left.left, best_line_right
                )
                new_line.size = last_i_2
                bay_lines.append(new_line)
        removal_queue = []
        persistent_lines = []
        for line in bay_lines:
            if line not in removal_queue:
                moving_line = line.left.right
                while moving_line != line.right.left:
                    moving_line = moving_line.right
                    for line2 in bay_lines:
                        if line2 != self:
                            if moving_line == line2.left or \
                                    moving_line == line2.right:
                                if line2.size < line.size:
                                    if line2 not in removal_queue:
                                        removal_queue.append(line2)
                for line2 in bay_lines:
                    if line2 not in removal_queue and line2 != line:
                        if line.size == line2.size:
                            line2.size += 1
                        if util.intersect(
                            line.a, line.b, line2.a, line2.b):
                            if self.check_intersections(line.a, line2.b):
                                new_line = Line(
                                    line.a, line2.b, line.left, line2.right
                                )
                                new_line.size = line.size + line2.size
                                bay_lines.append(new_line)
                                removal_queue.append(line)
                                removal_queue.append(line2)
                            elif line.size < line2.size:
                                removal_queue.append(line)
                            elif line.size > line2.size:
                                removal_queue.append(line2)
                            else:
                                removal_queue.append(line)
                        else:
                            if line.left == line2.left or \
                                line.right == line2.right:
                                if line.size < line2.size:
                                    removal_queue.append(line)
                                else:
                                    removal_queue.append(line2)
        for line in bay_lines:
            for line2 in bay_lines:
                if line != line2:
                    if line.a == line2.a and line.b == line2.b:
                        if line.size == line2.size:
                            line2.size += 1
                        if line.size > line2.size:
                            removal_queue.append(line2)
        removal_queue = list(sets.Set(removal_queue))
        for line in removal_queue:
            bay_lines.remove(line)
            #line.color = (1,1,0,1)
        for line in bay_lines:        
            stupid_terr.lines.append(line)
            self.lines.append(line)
            line2 = line.left.right
            while line2 != line.right:
                line2.color = (1,1,1,1)
                line2 = line2.right
    
    def color_territories(self):
        self.sort_countries()
        for country in self.countries:
            for terr in country.territories:
                terr.color_self()
            if self.verbose:
                print country.color, country.size()
    
    def combine(self, absorber, to_remove):
        absorber.color = [
            (absorber.color[i]+to_remove.color[i])/2 for i in range(4)
        ]
        if absorber == to_remove: 
            if self.verbose:
                print 'bad combine attempt: territories are the same'
            return
        if to_remove not in self.territories:
            if self.verbose:
                print 'bad combine attempt: territory not in list'
            return
        self.territories.remove(to_remove)
        absorber.triangles.extend(to_remove.triangles)
        for l in to_remove.lines:
            if l not in absorber.lines:
                absorber.add_line(l)
            else:
                absorber.remove_line(l)
                self.lines.remove(l)
        for l in to_remove.lines[:]:
            to_remove.remove_line(l)
        absorber.place_capital()
        absorber.combinations += 1
    
    def combine_random(self):
        if len(self.territories) < 2: return
        if len(self.outside_lines) == len(self.lines): return
        avg_combos = 0
        for terr in self.territories:
            avg_combos += terr.combinations
        avg_combos /= float(len(self.territories))
        
        largest_terr = self.get_largest_territory()
        
        candidates_1 = [
            line for line in self.inside_lines \
            if len(line.territories) > 1 \
            and not largest_terr in line.territories
        ]
        candidates_2 = [
            line for line in candidates_1 \
            if (len(line.territories[0].triangles) == 1 \
            or len(line.territories[1].triangles) == 1) \
            and not largest_terr in line.territories
        ]
        if len(candidates_2) > 0:
            candidates = candidates_2
        else:
            candidates = candidates_1
        found = False
        i = 0
        while not found and i < 200:
            i += 1
            line = random.choice(self.inside_lines)
            found = True
            if len(line.territories) <= 1:
                found = False
            else:
                for terr in line.territories:
                    if terr.combinations > avg_combos:
                        found = False
        try:
            absorber = line.territories[0]
            to_remove = line.territories[1]
        except:
            return
        self.combine(absorber, to_remove)
    
    def remove_floating_lines(self):
        if self.verbose: print "removing lone lines..."
        deletion_queue = []
        finished = False
        while not finished:
            finished = True
            for line in self.lines:
                a = False
                b = False
                if line not in self.outside_lines:
                    for line2 in self.lines:
                        if line != line2:
                            if line.a == line2.b or line.a == line2.a:
                                a = True
                            elif line.b == line2.a or line.b == line2.b:
                                b = True
                else:
                    a = True
                    b = True
                if not a or not b:
                    deletion_queue.append(line)
                    finished = False
            for line in deletion_queue:
                try:
                    self.lines.remove(line)
                    terrs = line.territories[:]
                    for terr in terrs:
                        terr.remove_line(line)
                except:
                    if self.verbose: print 'line remove fail'
    

if __name__ == "__main__":
    gen = ContinentGenerator()
    if len(sys.argv) > 1:
        gen.base_distance = 40
        gen.verbose = False
        render.basic(gen.generate(), sys.argv[1])
        copy_to_unique_name(sys.argv[1])
        quit()
    import demo
    gen.verbose = True
    main_window = demo.MapGenWindow(gen)

