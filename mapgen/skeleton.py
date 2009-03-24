import random

country_colors = [
    (1.0, 0.0, 0.0, 1.0), (1.0, 0.5, 0.0, 1.0), (1.0, 1.0, 0.0, 1.0), 
    (0.0, 1.0, 0.0, 1.0), (0.0, 1.0, 1.0, 1.0), (0.7, 0.0, 1.0, 1.0), 
    (1.0, 0.5, 1.0, 1.0), (0.7, 0.3, 0.0, 1.0)
]
random.shuffle(country_colors)

class Country(object):
    def __init__(self, color, name="America", cty_id=0):
        self.name = name
        self.color = color
        self.territories = []
        self.adjacencies = []
        self.cty_id = cty_id
    
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
        return str(self.color) + " #" + self.name
    

class Map(object):
    def __init__(self, lines, outside_lines, land_terrs, sea_terrs, countries=[]):
        super(Map, self).__init__()
        self.lines = lines
        self.outside_lines = outside_lines
        self.land_terrs = land_terrs
        self.sea_terrs = sea_terrs
        self.countries = countries
        self.name = "Untitled"
        self.map_id = 0
        self.width, self.height = 0, 0
        self.offset = (0,0)
    
    def find_bounds(self):
        min_x = 0
        min_y = 0
        max_x = 0
        max_y = 0
        for line in self.outside_lines:
            min_x = min(line.a.x, min_x)
            min_x = min(line.b.x, min_x)
            min_y = min(line.a.y, min_y)
            min_y = min(line.b.y, min_y)
            max_x = max(line.a.x, max_x)
            max_x = max(line.b.x, max_x)
            max_y = max(line.a.y, max_y)
            max_y = max(line.b.y, max_y)
        self.offset = (-min_x, -min_y)
        self.width = max_x - min_x
        self.height = max_y - min_y
    

class Generator(object):
    def __init__(self, num_countries):
        super(Generator, self).__init__()
        self.num_countries = num_countries
        self.lines = set()
        self.outside_lines = set()
        self.land_terrs = set()
        self.sea_terrs = set()
        self.width, self.height = 0, 0
        self.offset = (0, 0)
    
    def generate(self):
        return None
    
    def verify_data(self):
        for terr in self.land_terrs|self.sea_terrs:
            for ln in terr.lines:
                self.lines.add(ln)
            terr.adjacencies = [t for t in terr.adjacencies if t in self.land_terrs|self.sea_terrs]
    
