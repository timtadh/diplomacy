#!/usr/bin/python

import primitives
import territory
import render
import skeleton
import sys
import os
import graph_algorithms
import cPickle as pickle
import random

#os.chdir('..')
country_colors = [
    (1.0, 0.0, 0.0, 1.0), (1.0, 0.5, 0.0, 1.0), (1.0, 1.0, 0.0, 1.0), 
    (0.0, 1.0, 0.0, 1.0), (0.0, 1.0, 1.0, 1.0), (0.7, 0.0, 1.0, 1.0), 
    (1.0, 0.5, 1.0, 1.0), (0.7, 0.3, 0.0, 1.0),
    (7.0, 0.0, 0.0, 1.0), (7.0, 0.5, 0.0, 1.0), (7.0, 7.0, 0.0, 1.0), 
    (0.0, 7.0, 0.0, 1.0), (0.0, 7.0, 1.0, 1.0), (0.7, 0.0, 7.0, 1.0), 
    (7.0, 0.5, 7.0, 1.0), (0.4, 0.3, 0.0, 1.0)
]

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

def make_tri_row(h, w, x_offset, y_offset, tri_size, points, flip=False, n=1):
    top_y = y_offset
    mid_y = y_offset + tri_size/2
    bottom_y = y_offset + tri_size - 1
    
    mid_x_start = tri_size/2
    
    def add_point(pts, p, t):
        if not pts.has_key(p): 
            pts.update({p:set([])})
        pts[p].add(t)
    
    triangles = list()
    for c in xrange(w/tri_size):
        mid_x = mid_x_start + tri_size*c
        
        x1 = x_offset + mid_x
        x2 = clamp(x_offset + (mid_x - tri_size), 0, w)
        x3 = clamp(x_offset + (mid_x + tri_size), 0, w)
        
        if flip: c += 1
        if c%2:
            p1 = primitives.Point(x1, top_y)
            p2 = primitives.Point(x2, bottom_y)
            p3 = primitives.Point(x3, bottom_y)
            
        else:
            p1 = primitives.Point(x1, bottom_y)
            p2 = primitives.Point(x2, top_y)
            p3 = primitives.Point(x3, top_y)
        
        #surface[p1.y][p1.x] = n
        #surface[p2.y][p2.x] = n
        #surface[p3.y][p3.x] = n
        
        tri = primitives.Triangle(p1, p2, p3, primitives.Point(mid_x, mid_y))
        add_point(points, p1, tri.get_tuple())
        add_point(points, p2, tri.get_tuple())
        add_point(points, p3, tri.get_tuple())
        
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
    #surface = [[0 for x in xrange(width)] for y in xrange(height)]
    surface = None
    start_tri = None
    
    triangles = set()
    points = dict()
    for i in xrange(rows):
        flip = (i + 1)%2
        tris, pts = make_tri_row(height, width, 0, (size*i) - i, size, points, flip, i+1)
        if not start_tri: start_tri = tris[0]
        triangles = triangles | set(tris)
        points.update(pts)
        
    #print_surface(surface)
    
    build_graph(triangles, points)
    return triangles

def gen(triangles):
    territories = set()
    lines = set([])
    for tri in triangles:
        terr = territory.LandTerr(tri.lines)
        terr.add_triangle(tri.p1.x, tri.p1.y, tri.p2.x, tri.p2.y, tri.p3.x, tri.p3.y)
        territories.add(terr)
        lines = lines | set(tri.lines)
    new_map = skeleton.Map(lines, lines, territories, set())
    new_map.find_bounds()
    render.basic(new_map, 't.png')

def make_image(territories, lines):
    new_map = skeleton.Map(lines, lines, territories, set())
    new_map.find_bounds()
    render.basic(new_map, 't2.png')
    

def get_sep(a, b, G, path='mapgen/seperation-100'):
    import db
    con = db.connections.get_con()
    cur = con.cursor()
    cur.execute('''SELECT sep FROM seperation.sep_100 WHERE a = %s AND b = %s''', (G[a][0], G[b][0]))
    r = cur.fetchone()
    if r: sep = r[0]
    else: raise Exception(), 'Triangles not in DB'
    cur.close()
    db.connections.release_con(con)
    
    return sep

def load_graph():
    tris = pickle.load(open('mapgen/triangles-100', 'rb'))
    G = graph_algorithms.map_triangles(tris)
    return tris, G

def choose_start_triangles(triangles, G, number=60, min_sep=1500):
    available = list(triangles)
    chosen = set()
    for i in xrange(number):
        while True:
            c = random.choice(available)
            good = True
            for tri in chosen:
                if get_sep(tri, c, G) <= min_sep:
                    good = False
                    break
            if good: 
                chosen.add(c)
                available.remove(c)
                break
    return chosen, available

def build_map(triangles, G, chosen, available):
    territories = list()
    lines = set([])
    for i, tri in enumerate(chosen):
        terr = territory.LandTerr(tri.lines)
        terr.id = i
        terr.add_triangle(tri.p1.x, tri.p1.y, tri.p2.x, tri.p2.y, tri.p3.x, tri.p3.y)
        terr.adjacencies += tri.adj
        terr.done = False
        terr.color = (random.random(), random.random(), random.random(), 1.0)
        territories.append(terr)
        lines = lines | set(tri.lines)
    print len(available)
    while len(available) > 0:
        print len(available)
        for terr in territories:
            if terr.done: continue
            a = list(terr.adjacencies)
            good = False
            while True:
                c = random.choice(a)
                a.remove(c)
                good = True
                if c in chosen: good = False
                if not good and len(a) <= 0: 
                    terr.done = True
                    break
                if good:
                    c = G[c][1]
                    chosen.add(c.get_tuple())
                    available.remove(c)
                    terr.add_triangle(c.p1.x, c.p1.y, c.p2.x, c.p2.y, c.p3.x, c.p3.y)
                    terr.adjacencies = list((set(terr.adjacencies) | set(c.adj)) - set([c]))
                    lines = lines | set(c.lines)
                    break
    return territories, lines

tris, G = load_graph()
print 'loaded'
chosen, available = choose_start_triangles(tris, G)
print chosen
territories, lines = build_map(tris, G, chosen, available)
print territories, len(available)
make_image(territories, lines)
print 'done'

#def rm(path='mapgen/seperation-100'):
    #try: os.remove(path)
    #except: pass

#def save_seperation(seperation, path='mapgen/seperation-100'):
    #con = sqlite3.connect(path)
    #cur = con.cursor()
    #cur.execute('''create table seperation (a, b, sep)''')
    #cur.close()
    #cur = con.cursor()
    #cur.execute('insert into seperation (a, b, sep) values (5,5,5)')
    #cur.close()
    #n = len(seperation)
    #for i in xrange(n):
        #for j in xrange(n):
            #cur = con.cursor()
            #cur.execute('INSERT INTO seperation (a, b, sep) values (?,?,?)', (i, j, seperation[i][j]))
            #cur.close()
    #con.commit()
    #con.close()

#def print_seperation(path='mapgen/seperation-100'):
    #con = sqlite3.connect(path)
    #cur = con.cursor()
    #cur.execute('''SELECT * FROM seperation''')
    #r = cur.fetchone()
    #while r:
        #print ', '.join((str(r[0]), str(r[1]), str(r[2])))
        #r = cur.fetchone()
    #cur.close()
    #con.close()

                #tris = list(make_triangles(100, 100, 9))
                #tris.sort()
                #print 'triangles made'
                #seperation = graph_algorithms.seperation(tris)
                #graph_algorithms.print_matrix(graph_algorithms.make_adj_matrix(tris))
                #graph_algorithms._print_matrix(seperation)
                #print 'seperation calculated'
                #spap = graph_algorithms.floyd_warshall(tris)
                #graph_algorithms.print_matrix(spap)
                #sys.setrecursionlimit(2000)
                #pickle.dump(tris, open('mapgen/triangles-100', 'wb'))
                #rm()
                #save_seperation(seperation)
                #print_seperation()
