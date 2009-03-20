import sys

def dfs(root, triangles):
    color = dict(); path = dict();
    #print
    for tri in triangles:
        color.update({tri:0})
        path.update({tri:None})
    
    def dfs_visit(v):
        color[v] = 1
        #print v
        for u in v.adj:
            if color[u] == 0:
                path[u] = v 
                dfs_visit(u)
        color[v] = 2
    
    dfs_visit(root)
    
    #print
    #for tri in path.keys():
        #print tri, path[tri]
    #print
    #for tri in color.keys():
        #print tri, color[tri]
    #print
    #print

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

def floyd_warshall(triangles):
    keys = list(triangles)
    keys.sort()
    a = [0 for x in xrange(len(keys))]
    b = [a for y in xrange(len(keys))]
    d = [b for k in xrange(len(keys)+1)]
    
    for i,row in enumerate(keys):
        for j,col in enumerate(keys):
            if row in col.adj: d[0][i][j] = 1 
            elif i == j: d[0][i][j] = 0
            else: d[0][i][j] = sys.maxint
    
    for k in xrange(1, len(keys)+1):
        for i in xrange(len(keys)):
            for j in xrange(len(keys)):
                d[k][i][j] = min(d[k-1][i][j], d[k-1][i][k-1] + d[k-1][k-1][j])
     
    m = dict()
    for i,a in enumerate(keys):
        for j,b in enumerate(keys):
            if not m.has_key(a): m.update({a:dict()})
            m[a].update({b:d[-1][i][j]})
    
    return m