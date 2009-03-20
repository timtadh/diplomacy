#!/usr/bin/python

import primitives
import sys

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

def make_tri_row(surface, x_offset, y_offset, tri_size, points, flip=False, n=1):
    top_y = y_offset
    bottom_y = y_offset + tri_size - 1
    
    mid_x_start = tri_size/2
    
    def add_point(pts, p, t):
        if not pts.has_key(p): 
            pts.update({p:set([])})
        pts[p].add(t)
    
    triangles = list()
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
        
        triangles.append(tri)
        
    return triangles, points

def build_graph(triangles, points):
    for tri in triangles:
        p1 = points[tri.p1]
        p2 = points[tri.p2]
        p3 = points[tri.p3]
        
        a = (p1 & p2)
        b = (p2 & p3)
        c = (p3 & p1)
        
        tri.adj.extend((a | b | c) - set([tri]))

def make_triangles(rows, cols, size):
    height = size * rows - (rows-1)
    width = size * cols
    surface = [[0 for x in xrange(width)] for y in xrange(height)]
    
    start_tri = None
    
    triangles = set()
    points = dict()
    for i in xrange(rows):
        flip = (i + 1)%2
        tris, pts = make_tri_row(surface, 0, (size*i) - i, size, points, flip, i+1)
        if not start_tri: start_tri = tris[0]
        triangles = triangles | set(tris)
        points.update(pts)
        
    print_surface(surface)
    
    build_graph(triangles, points)
    print
    for tri in triangles:
        print tri, ' '*6, tri.adj
    print
    dfs(start_tri, triangles)

def dfs(root, triangles):
    color = dict(); path = dict();
    print
    for tri in triangles:
        color.update({tri:0})
        path.update({tri:None})
    
    def dfs_visit(v):
        color[v] = 1
        print v
        for u in v.adj:
            if color[u] == 0:
                path[u] = v 
                dfs_visit(u)
        color[v] = 2
    
    dfs_visit(root)
    
    print
    for tri in path.keys():
        print tri, path[tri]
    print
    for tri in color.keys():
        print tri, color[tri]
    print
    print
    matrix = make_adj_matrix(triangles)
    print_matrix(matrix)
    print_matrix(floyd_warshall(matrix))

def print_matrix(matrix):
    s = '  '
    for x in xrange(len(matrix)):
        s += str(x) + ' '*(3-len(str(x)))
    print s
    keys = matrix.keys()
    keys.sort()
    for i, row in enumerate(keys):
        s = str(i) + ' '*(3-len(str(i)))
        for col in keys:
            s += str(matrix[row][col]) + ' '*(3-len(str(matrix[row][col])))
        print s

def _print_matrix(m):
    s = '  '
    for x in xrange(len(m)):
        s += str(x) + ' '
    print s
    for i, row in enumerate(m):
        s = str(i) + ' '
        for col in row:
            s += str(col) + ' '
        print s

def make_adj_matrix(triangles):
    matrix = dict()
    for a in triangles:
        for b in triangles:
            if not matrix.has_key(a): matrix.update({a:dict()})
            matrix[a].update({b:0})
    
    for row in matrix.keys():
        for col in matrix.keys():
            if row in col.adj: matrix[row][col] = 1
            elif row == col: matrix[row][col] = 1
    
    return matrix

def floyd_warshall(matrix):
    d = list()
    keys = matrix.keys()
    keys.sort()
    for k in xrange(len(matrix)+1):
        d.append(list())
        for i,a in enumerate(keys):
            d[-1].append(list())
            for j,b in enumerate(keys):
                d[-1][i].append(0)
    
    for i,row in enumerate(keys):
        for j,col in enumerate(keys):
            d[0][i][j] = matrix[row][col]
            if i == j: d[0][i][j] = 0
            elif d[0][i][j] == 0: d[0][i][j] = sys.maxint
    
    for k in xrange(1, len(matrix)+1):
        for i in xrange(len(matrix)):
            for j in xrange(len(matrix)):
                d[k][i][j] = min(d[k-1][i][j], d[k-1][i][k-1] + d[k-1][k-1][j])
     
    m = dict()
    for i,a in enumerate(keys):
        for j,b in enumerate(keys):
            if not m.has_key(a): m.update({a:dict()})
            m[a].update({b:d[-1][i][j]})
    
    return m

make_triangles(4, 12, 9)



#print make_tri_row(surface, 0, 0, tri_size, False)
#print make_tri_row(surface, 0, tri_size-1, tri_size, True, 2)
#print len(make_tri_row(surface, 0, (tri_size*2)-2, tri_size, False, 3))
