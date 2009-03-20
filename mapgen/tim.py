#!/usr/bin/python

import primitives

h = 2
w = 12
tri_size = 9

height = tri_size * h - (h-1)
width = tri_size * w

surface = [[0 for x in xrange(width)] for y in xrange(height)]

def print_surface(surface):
    for row in surface:
        s = ''
        for col in row:
            if col: s += str(col)
            else: s += '.'
        print s

def clamp(x, base, top):
    if x < base: x = base
    if x >= top: x = top - 1
    return x

def make_tri_row(surface, x_offset, y_offset, tri_size, flip=False, n=1):
    top_y = y_offset
    bottom_y = y_offset + tri_size - 1
    
    mid_x_start = tri_size/2
    
    def add_point(pts, p, t):
        if pts.has_key(p): pts.append(t)
        else: pts.update({p:[t]})
    
    triangles = set()
    points = dict()
    for c in xrange(len(surface[0])/tri_size):
        mid_x = mid_x_start + tri_size*c
        
        x1 = x_offset + mid_x
        x2 = clamp(x_offset + (mid_x - tri_size), 0, len(surface[0]))
        x3 = clamp(x_offset + (mid_x + tri_size), 0, len(surface[0]))
        
        if flip: c += 1
        if c%2:
            p1 = primitives.Point(x1, top_y)
            p2 = primitives.Point(x2, bottom_y)
            p3 = primitives.Point(x3, bottom_y)
            
        else:
            p1 = primitives.Point(x1, bottom_y)
            p2 = primitives.Point(x2, top_y)
            p3 = primitives.Point(x3, top_y)
        
        surface[p1.y][p1.x] = n
        surface[p2.y][p2.x] = n
        surface[p3.y][p3.x] = n
        
        tri = primitives.Triangle(p1, p2, p3)
        add_point(points, p1, tri)
        add_point(points, p2, tri)
        add_point(points, p3, tri)
        
        triangles.add(tri)
        
    return triangles


print make_tri_row(surface, 0, 0, tri_size, False)
print make_tri_row(surface, 0, tri_size-1, tri_size, True, 2)
#print len(make_tri_row(surface, 0, (tri_size*2)-2, tri_size, False, 3))
print_surface(surface)
