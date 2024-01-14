from math import *

PI = 3.1415926535

def normalize_angle(a):
    if a > 2 * PI:
        return a % 360
    
    if a < 0:
        return (2 * 3.14159) + (a % -(2 * PI))

    return a


def angle_between_points(p1, p2):
    angle = atan(abs(p2[1] - p1[1]) / abs(p2[0] - p1[0]))

    if p1[0] > p2[0]:
        angle = PI - angle
    if (p1[1] > p2[1]):
        angle = 2 * PI - angle;
	
    return angle;

    
def rotate(p, origin, r):
    magnitude = sqrt(pow(abs(p[1] - origin[1]), 2) + pow(abs(p[0] - origin[0]), 2))
    angle = angle_between_points(origin, p)
    r_angle = normalize_angle(r + angle)
    
    return [magnitude * cos(r_angle), magnitude * sin(r_angle)]


def gps_to_m(p, origin):
    ll_per_m = 111000
    m = [0, 0]
    
    m[0] = (p[0] - origin[0]) / (ll_per_m)
    m[1] = (p[1] - origin[1]) / (ll_per_m)

    return m

