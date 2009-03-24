import math, primitives

def median(countries):
    values = sorted([len(country.territories) for country in countries])
    if len(values) % 2 == 1:
        return values[(len(values)+1)/2-1]
    else:
        lower = values[len(values)/2-1]
        upper = values[len(values)/2]
        return float(lower+upper)/2

def point_inside_polygon(x,y,poly_list):
    poly = []
    for i in range(len(poly_list)/2):
        poly.append((poly_list[i*2], poly_list[i*2+1]))
    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    if x == p1x and y == p1y: return False
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if x == p2x and y == p2y: return False
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

def area_of_triangle(tri):
    x1 = min(tri[0], tri[2], tri[4])
    y1 = min(tri[1], tri[3], tri[5])
    x2 = max(tri[0], tri[2], tri[4])
    y2 = max(tri[1], tri[3], tri[5])
    w = x2 - x1
    h = y2 - y1
    return w*h/2.0

def intersect(p1, p2, p3, p4, allow_points=True):
    if allow_points:
        if p1.x == p3.x and p1.y == p3.y or \
            p2.x == p4.x and p2.y == p4.y or \
            p1.x == p4.x and p1.y == p4.y or \
            p2.x == p3.x and p2.y == p3.y:
            return False
    else:
        if p1.x == p3.x and p1.y == p3.y or \
            p2.x == p4.x and p2.y == p4.y or \
            p1.x == p4.x and p1.y == p4.y or \
            p2.x == p3.x and p2.y == p3.y:
            return True
    """
    min_x1, max_x1 = sorted([p1.x, p2.x])    
    min_y1, max_y1 = sorted([p1.y, p2.y])
    min_x2, max_x2 = sorted([p3.x, p4.x])    
    min_y2, max_y2 = sorted([p3.y, p4.y])
    if min_x1 >= max_x2: return False
    if max_x1 <= min_x2: return False
    if min_y1 >= max_y2: return False
    if max_y1 <= min_y2: return False
    """
    xD1 = p2.x-p1.x
    xD2 = p4.x-p3.x
    yD1 = p2.y-p1.y
    yD2 = p4.y-p3.y
    xD3 = p1.x-p3.x
    yD3 = p1.y-p3.y
    
    len1 = math.sqrt(xD1*xD1+yD1*yD1)
    len2 = math.sqrt(xD2*xD2+yD2*yD2)
    if len1 == 0:
        print p1, p2
    if len2 == 0:
        print p3, p4
    dot = (xD1*xD2+yD1*yD2)
    if len1*len2 == 0:
        deg = 0
    else:
        deg = dot/(len1*len2)
    
    if abs(deg) == 1:
        return False
        
    pt = primitives.Point(0,0);
    div = yD2*xD1-xD2*yD1
    if div == 0: return True
    ua = (xD2*yD3-yD2*xD3)/div
    ub = (xD1*yD3-yD1*xD3)/div
    pt.x = p1.x+ua*xD1
    pt.y = p1.y+ua*yD1
    xD1 = pt.x-p1.x
    xD2 = pt.x-p2.x
    yD1 = pt.y-p1.y
    yD2 = pt.y-p2.y
    segmentLen1 = math.sqrt(xD1*xD1+yD1*yD1)+math.sqrt(xD2*xD2+yD2*yD2)
    
    xD1 = pt.x-p3.x
    xD2 = pt.x-p4.x
    yD1 = pt.y-p3.y
    yD2 = pt.y-p4.y
    segmentLen2 = math.sqrt(xD1*xD1+yD1*yD1)+math.sqrt(xD2*xD2+yD2*yD2);
    
    if abs(len1-segmentLen1) > 0.01 or abs(len2-segmentLen2) > 0.01:
        return False
    return True
