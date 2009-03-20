#!/usr/bin/python

import primitives

h = 2
w = 10
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
    mid_y = y_offset + tri_size/2
    top_y = y_offset
    bottom_y = y_offset + tri_size - 1
    
    mid_x_start = tri_size/2
    
    tri = set()
    for c in xrange(len(surface[0])/tri_size):
        mid_x = mid_x_start + tri_size*c
        
        x3 = x_offset + mid_x
        x2 = clamp(x_offset + (mid_x - tri_size), 0, len(surface[0]))
        x3 = clamp(x_offset + (mid_x + tri_size), 0, len(surface[0]))
        
        if flip: c += 1
        if c%2:
            print top_y, x3
            surface[top_y][x3] = n
            surface[bottom_y][x2] = n
            surface[bottom_y][x3] = n
            
            tri.add(((top_y, x_offset + mid_x), (bottom_y, x2), (bottom_y, x3)))
        else:
            surface[bottom_y][x3] = n
            surface[top_y][x2] = n
            surface[top_y][x3] = n
            
            tri.add(((bottom_y, x_offset + mid_x), (top_y, x2), (top_y, x3)))
    return tri


print len(make_tri_row(surface, 0, 0, tri_size, False))
print len(make_tri_row(surface, 0, tri_size-1, tri_size, True, 2))
#print len(make_tri_row(surface, 0, (tri_size*2)-2, tri_size, False, 3))
print_surface(surface)
