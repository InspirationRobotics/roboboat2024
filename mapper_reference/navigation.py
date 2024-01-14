# to contain all of the navigation waypoint plotting functions
import numpy as np

def mapper_points(coord1, coord2):
    #bouy1 coord (x,y), bouy2 coord (x,y)
    x1 = coord1[0]
    x2 = coord2[0]
    y1 = coord1[1]
    y2 = coord2[1]
    dist = np.sqrt(np.square(x1-x2) + np.square(y1-y2))
    halfway = dist/2
    waypoint_coord = [halfway,y1]
    return waypoint_coord
