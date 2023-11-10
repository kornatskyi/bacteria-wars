import math


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


def distance_between_two_points(point_one: Point, point_two: Point) -> float:
    """Calculated distance between two points

    Args:
        point_one (Point): coordinates of a first point
        point_two (Point): coordinates of a second point

    Returns:
        float: absolute distance between two points
    """
    return math.sqrt(
        (abs(point_one.x) - abs(point_two.x)) ** 2
        + (abs(point_one.y) - abs(point_two.y)) ** 2
    )


def angle_between_x_axis_and_line_through_points(
    point_a: Point, point_b: Point
) -> float:
    """Returns the angle (in radians) between the positive x-axis and the line passing through two points.

    Args:
        point_a: The first point.
        point_b: The second point.

    Returns:
        The angle (in radians) between the positive x-axis and the line passing through the two points.
    """
    dx = point_b.x - point_a.x
    dy = point_b.y - point_a.y
    return math.atan2(dy, dx)