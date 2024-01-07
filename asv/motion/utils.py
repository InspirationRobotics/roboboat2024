from typing import Tuple
import math


def heading_error(heading, target):
    """
    Calculate heading error
    handling the case where 359 and 0 are close
    """
    error = target - heading
    if abs(error) > 180:
        error = (error + 360) % 360
    return error


def get_norm(x, y) -> float:
    """
    Calculate norm of a vector
    """
    norm: float = math.sqrt(x**2 + y**2)
    return norm

def get_distance(v1, v2) -> float:
    """
    Calculate distance between two points
    """
    dist = math.sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2)
    return dist


def rotate_vector(x, y, heading) -> Tuple[float,float]:
    """
    Rotate a vector by heading
    """
    x_rot = x * math.cos(math.radians(heading)) + y * math.sin(math.radians(heading))
    y_rot = y * math.cos(math.radians(heading)) - x * math.sin(math.radians(heading))
    return x_rot, y_rot


def inv_rotate_vector(x, y, heading) -> Tuple[float,float]:
    """
    Inverse Rotate a vector by heading
    """
    x_rot = x * math.cos(math.radians(heading)) - y * math.sin(math.radians(heading))
    y_rot = y * math.cos(math.radians(heading)) + x * math.sin(math.radians(heading))
    return x_rot, y_rot


def get_heading_from_coords(x, y) -> float:
    """
    Get heading from coordinates

    Parameters
    ----------
    x: East
    y: North

    Returns
    -------
    Bearing/Heading Angle
    """
    return math.degrees(math.atan2(x, y))
