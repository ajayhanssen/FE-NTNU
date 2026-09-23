import numpy as np

def eucl_dist(p1, p2):
    x1, z1 = p1
    x2, z2 = p2
    return np.sqrt((x2-x1)**2 + (z2-z1)**2)