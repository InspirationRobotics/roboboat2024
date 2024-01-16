from typing import Tuple
import math


def heading_error(heading, target):
    """
    Calculate heading error
    handling the case where 359 and 0 are close
    """
    # Calculate the initial error
    error = target - heading

    # Check if the absolute value of the error is greater than 180 degrees
    if abs(error) > 180:
        # Adjust the error to be within the range of -180 to 180 degrees
        error = (error + 360) % 360

    # Return the adjusted error
    return error


def get_norm(x, y) -> float:
    """
    Calculate norm of a vector

    Parameters
    ----------
    x: x component of the vector
    y: y component of the vector

    Returns
    -------
    norm of the vector
    """
    norm: float = math.sqrt(x**2 + y**2)
    return norm


def get_distance(v1, v2) -> float:
    """
    Calculate distance between two points

    Parameters
    ---------
    v1: point 1
    v2: point 2

    Returns
    -------
    Distance between v1 and v2
    """
    dist = math.sqrt((v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2)
    return dist


def rotate_vector(x, y, heading) -> Tuple[float, float]:
    """
    Rotate a vector by heading
    Clockwise rotation

    Parameters
    ----------
    x: x component
    y: y component
    heading: heading/bearing angle

    Returns
    -------
    x_rot: x component after clockwise rotation
    y_rot: y component after clockwise rotation
    """
    x_rot = x * math.cos(math.radians(heading)) + y * math.sin(math.radians(heading))
    y_rot = y * math.cos(math.radians(heading)) - x * math.sin(math.radians(heading))
    return x_rot, y_rot


def inv_rotate_vector(x, y, heading) -> Tuple[float, float]:
    """
    Rotate a vector by heading
    Counterclockwise rotation

    Parameters
    ----------
    x: x component
    y: y component
    heading: heading/bearing angle

    Returns
    -------
    x_rot: x component after counterclockwise rotation
    y_rot: y component after counterclockwise rotation
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
    Heading/Bearing Angle
    """
    return math.degrees(math.atan2(x, y))
