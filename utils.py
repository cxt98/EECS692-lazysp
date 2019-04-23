from scipy.spatial import distance
import numpy as np

def random_edgelen():
    distance = 0.0
    if np.random.uniform(low=0.0, high=1.0) <= 0.5:
        distance = float('inf')
    else:
        distance = np.random.uniform(low=1.0, high=2.0)
    return distance

def obstacle_edgelen(u, v, rects): # check whether line from u to v intersects with any rectangle,
    # if intersects, edge weight is inf; else its euclidean distance, assumes 2D, rectangle aligns with axis
    X1, Y1 = u
    X2, Y2 = v
    intersects = False
    for r in rects:
        X3, Y3 = r[:2]
        X4, Y4 = r[2:]
        if line_segment_intersect(X1, Y1, X2, Y2, X3, Y3, X4, Y4):
            intersects = True
            break
    if intersects:
        return float('inf')
    else:
        return distance.euclidean(u, v)
    return 0

def line_segment_intersect(X1, Y1, X2, Y2, X3, Y3, X4, Y4):
    # two lines: (x1, y1)--(x2, y2) and (x3, y3)--(x4, y4)
    I1 = [min(X1,X2), max(X1,X2)]
    I2 = [min(X3,X4), max(X3,X4)]
    Ia = [max( min(X1,X2), min(X3,X4) ), min( max(X1,X2), max(X3,X4) )]
    if (max(X1,X2) < min(X3,X4)):
        return False
    A1 = (Y1-Y2)/(X1-X2)
    A2 = (Y3-Y4)/(X3-X4)
    b1 = Y1-A1*X1
    b2 = Y3-A2*X3
    Xa = (b2 - b1) / (A1 - A2)
    if ( (Xa < max( min(X1,X2), min(X3,X4) )) or (Xa > min( max(X1,X2), max(X3,X4) )) ):
        return False # intersection is out of bound
    else:
        return True

def generate_obstacles(): # obstacles are random rectangles in unit square
    n_rect = 10
    rects = []
    for i in range(n_rect):
        lx = np.random.uniform(low=0.1, high=0.3)
        ly = np.random.uniform(low=0.1, high=0.3)
        x = np.random.uniform(low=0.0, high=1.0-lx)
        y = np.random.uniform(low=0.0, high=1.0-ly)
        rects.append([x, x + lx, y, y + ly])
    return rects