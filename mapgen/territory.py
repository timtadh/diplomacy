import util, random

PICK_TRIANGLE = 0
AVERAGE_POINTS = 1
LARGEST_TRIANGLE = 2

class Territory(object):
    def __init__(self):
        super(Territory, self).__init__()
        self.country = None
        self.adjacencies = []
        self.lines = []
        self.is_coastal = False
        self.has_supply_center = False
        self.occupied = False
        self.x, self.y = 0.0, 0.0
        self.name = ""
        self.abbreviation = ""
        self.ter_id = 0
        self.is_sea = False
        self.pc_x, self.pc_y = 0, 0
        self.triangles = []
    

class SeaTerr(Territory):
    def __init__(self, line=None):
        super(SeaTerr, self).__init__()
        self.line = line
        self.size = 0
        self.is_sea = True
        if line != None:
            self.lines.append(line)
            self.x = (line.a.x + line.b.x) / 2
            self.y = (line.a.y + line.b.y) / 2
            self.pc_x = self.x
            self.pc_y = self.y - 10
        else:    
            self.x, self.y = 0, 0
            self.pc_x, self.pc_y = 0, 0
    

class LandTerr(Territory):
    def __init__(self, lines=[], color=(0.5,0.5,0.5,1)):
        super(LandTerr, self).__init__()
        for line in lines:
            self.add_line(line)
        self.color = color
        self.adjacent_countries = []
        self.dist = 0
        self.combinations = 0
        self.offset = (0,0)
        self.min_x, self.min_y, self.max_x, self.max_y = 0, 0, 0, 0
    
    def add_line(self, line):
        if line not in self.lines:
            self.lines.append(line)
            line.territories.append(self)
    
    def remove_line(self, line):
        self.lines.remove(line)
        line.territories.remove(self)
    
    def add_triangle(self, x1, y1, x2, y2, x3, y3):
        self.triangles.append((x1, y1, x2, y2, x3, y3))
    
    def find_adjacencies(self): 
        self.adjacent_countries = []
        self.adjacencies = []
        for line in self.lines:
            for terr in line.territories:
                if terr != self and terr not in self.adjacencies:
                    self.adjacencies.append(terr)
        for terr in self.adjacencies:
            if terr.country not in self.adjacent_countries:
                if terr.country != None:
                    self.adjacent_countries.append(terr.country)
    
    def find_bounding_box(self):
        self.min_x = self.lines[0].a.x
        self.min_y = self.lines[0].a.y
        self.max_x = self.min_x
        self.max_y = self.min_y
        for line in self.lines:
            self.min_x = min(line.a.x, self.min_x)
            self.min_x = min(line.b.x, self.min_x)
            self.min_y = min(line.a.y, self.min_y)
            self.min_y = min(line.b.y, self.min_y)
            self.max_x = max(line.a.x, self.max_x)
            self.max_x = max(line.b.x, self.max_x)
            self.max_y = max(line.a.y, self.max_y)
            self.max_y = max(line.b.y, self.max_y)
        self.min_x = int(self.min_x)
        self.min_y = int(self.min_y)
        self.max_x = int(self.max_x)
        self.max_y = int(self.max_y)
    
    def check_point(self, x, y, x_dist=12, y_dist=5):
        if not self.point_inside(x, y): return False
        if not self.point_inside(x+x_dist, y+y_dist): return False
        if not self.point_inside(x-x_dist, y+y_dist): return False
        if not self.point_inside(x+x_dist, y-y_dist): return False
        if not self.point_inside(x-x_dist, y+y_dist): return False
        return True
    
    def place_piece(self):
        self.pc_x = self.x
        self.pc_y = self.y-10
        if not self.point_inside(self.pc_x, self.pc_y-10):
            self.pc_x, self.pc_y = self.x+20, self.y
        if not self.point_inside(self.pc_x+10, self.pc_y):
            self.pc_x, self.pc_y = self.x, self.y+10
        if not self.point_inside(self.pc_x, self.pc_y+10):
            self.pc_x, self.pc_y = self.x-20, self.y
        if not self.point_inside(self.pc_x-10, self.pc_y):
            self.pc_x, self.pc_y = self.find_empty_space()
            if self.pc_x == 0 and self.pc_y == 0:
                self.pc_x, self.pc_y = self.x, self.y-10
    
    def check_avoid(self, x, y, avoid_x, avoid_y):
        if avoid_x == 0 and avoid_y == 0: return True
        if (x-avoid_x)*(x-avoid_x)+(y-avoid_y)*(y-avoid_y) < 20*20:
            return False
        else:
            return True
    
    def find_empty_space(self, avoid_x=0, avoid_y=0):
        x = random.randint(self.min_x, self.max_x)
        y = random.randint(self.min_y, self.max_y)
        i = 0
        while not self.check_point(x, y) and i < 200 and self.check_avoid(x, y, avoid_x, avoid_y):
            x = random.randint(self.min_x, self.max_x)
            y = random.randint(self.min_y, self.max_y)
            i += 1
        if i == 200:
            return 0, 0
        return x, y
    
    def place_text(self):
        self.find_bounding_box()
        self.x, self.y = self.find_empty_space()
        if self.x == 0 and self.y == 0:
            print self.abbreviation
            self.place_text_old()
            return
        else:
            self.place_piece()
    
    def place_text_old(self):
        #This is a complicated block of code which attempts to place the text
        #label in a sane place using a variety of methods.
        self.points = []
        for line in self.lines:
            if line.a not in self.points:
                self.points.append(line.a.get_tuple())
            if line.b not in self.points:
                self.points.append(line.b.get_tuple())
        self.x = 0.0
        self.y = 0.0
        for point in self.points:
            self.x += point[0]
            self.y += point[1]
        self.x /= len(self.points)
        self.y /= len(self.points)
        
        ok = True
        if not self.point_inside(self.x, self.y): ok = False
        if not self.point_inside(self.x+15, self.y): ok = False
        if not self.point_inside(self.x-15, self.y): ok = False
        if not self.point_inside(self.x, self.y+15): ok = False
        if not self.point_inside(self.x, self.y-15): ok = False
        if ok:
            self.place_piece()
            return
        
        chosen_tri = 0
        max_area = 0
        for i in range(1, len(self.triangles)):
            a = util.area_of_triangle(self.triangles[i])
            if a > max_area:
                max_area = a
                chosen_tri = i
        tri = self.triangles[chosen_tri]
        self.x = tri[0] + tri[2] + tri[4]
        self.y = tri[1] + tri[3] + tri[5]
        self.x /= 3.0
        self.y /= 3.0
        self.place_piece()
    
    def color_self(self):
        darken_amt = (1.0-random.random()*0.15)
        if self.country != None and (self.has_supply_center or self.occupied):
            col = self.country.color
        else:
            col = (1.0, 1.0, 1.0, 1.0)
        self.color = (
            col[0]*darken_amt,
            col[1]*darken_amt,
            col[2]*darken_amt,
            1.0
        )
        if self.color == (0.0, 0.0, 0.0, 1.0):
            self.color = self.country.color
    
    def point_inside(self, x, y):
        """Returns True if (x,y) is inside the territory."""
        for tri in self.triangles:
            if util.point_inside_polygon(x, y, tri):
                return True
        return False
    
    def __repr__(self):
        return str(self.ter_id)
    
