import random
from skeleton import *
from territory import *
from primitives import *

class TriGen(Generator):
    def __init__(self, num_countries):
        super(Generator, self).__init__(num_countries)
        self.land_terrs = set()
        self.sea_terrs = set()
    
    def generate(self):
        p1 = Point(00, 40)
        p2 = Point(30, -20)
        p3 = Point(-30, -20)
        
        line1 = Line(p1, p2)
        line2 = Line(p2, p3)
        line3 = Line(p3, p1)
        
        line1.left = line3
        line1.right = line2
        line2.left = line1
        line2.right = line3
        line3.left = line2
        line3.right = line1
        
        linelist = [line1, line2, line3]
        self.lines = set(linelist)
        self.outside_lines = set(linelist)
        
        terr = LandTerr(linelist)
        terr.add_triangle(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1])
        self.land_terrs.add(terr)
        
        new_map = Map(self.lines, self.outside_lines, self.land_terrs, self.sea_terrs)
        new_map.find_bounds()
        return new_map
    
