import math

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
    
    def get_tuple(self):
        return (self.x, self.y)
    

class Line(object):
    def __init__(self, a, b, left=None, right=None, color=(0,0,0,1)):
        self.a = a
        self.b = b
        self.left = left    #line connecting to self.a
        self.right = right  #line connecting to self.b
        self.normal = math.atan2(b.y-a.y, b.x-a.x) - math.pi/2
        self.midpoint = Point((a.x+b.x)/2, (a.y+b.y)/2)
        self.outside = True #line is on outside of shape
        self.color = color
        self.territories = []
        self.combinations = 0
        self.id = 0
        self.length = 0     #calculated when requested
        self.favored = False
    
    def get_length(self):
        if self.length == 0:
            self.length = math.sqrt(
                (self.a.x-self.b.x)*(self.a.x-self.b.x) \
                + (self.a.y-self.b.y)*(self.a.y-self.b.y)
            )
        return self.length
    
    def next(self, origin_line):
        if origin_line != self.left: return self.left
        return self.right
    
    def __repr__(self):
        return "Line((%r, %r), (%r, %r))" % (
            self.a.x, self.a.y, self.b.x, self.b.y
        )