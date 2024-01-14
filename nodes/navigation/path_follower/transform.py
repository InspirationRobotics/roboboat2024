from math import *
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


def map_hdg(hdg, map_orientation):
    return normalize_angle(hdg - map_orientation)


def map_pos(dp, map_orientation):
    mp = rotate(dp, [0, 0], -map_orientation)

    return mp


# position relative to the front of the robot to map coords
def obj_pos(dp, m_hdg, m_pos):
    op = rotate(dp, [0, 0], m_hdg - (PI / 2)) # subtract by PI because 0 radians points east

    return [op[0] + m_pos[0], op[1] + m_pos[1]]


def calc_rel_pose(d, c, fov, fw):
    angle = ((c - fw / 2) / fw) * fov
    print(angle)
    return [d * cos(angle), d * sin(angle)]