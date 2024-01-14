# verify this

import math

PI = 3.1415926535

def normalize_angle(a):
    if a > 2 * PI:
        return a % 360
    if a < 0:
        return (2 * 3.14159) + (a % -(2 * PI))

    return a


def angle_between_points(p1, p2):
	
    if (p2[0] - p1[0] == 0)
        return PI / 2

    angle = atan(abs(p2[1] - p1[1]) / abs(p2[0] - p1[0]))

    if p1[0] > p2[0]:
        angle = PI - angle
    if (p1[1] > p2[1]):
        angle = 2 * PI - angle;
	
    return angle

# rotate p about origin by +r degrees (0 is east)
def rotate(p, origin, r):
    magnitude = sqrt(pow(abs(p[1] - origin[1]), 2) + pow(abs(p[0] - origin[0]), 2))
    angle = angle_between_points(origin, p)
    r_angle = normalize_angle(r + angle)
    
    return [magnitude * cos(r_angle), magnitude * sin(r_angle)]


def gps_trans(gps, heading, n):
	new_pose = gps
	new_pose[0] += n
	new_pose = rotate(new_pose, gps, heading) 

	return new_pose
