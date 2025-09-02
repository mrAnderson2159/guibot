from typing import Optional

class Point:
    """ Represents a point in 2D space with x and y coordinates."""
    def __init__(self, x: float, y: float):
        """ Initializes a Point with x and y coordinates.
        :param x: The x-coordinate of the point.
        :param y: The y-coordinate of the point.
        """
        self.x = x
        self.y = y

    @property
    def tuple(self):
        """ Returns the coordinates as a tuple of floats (x, y). """
        return (self.x, self.y)

    @property
    def tuple_int(self):
        """ Returns the coordinates as a tuple of integers (x, y). """
        return (int(self.x), int(self.y))

    @property
    def int_x(self):
        """ Returns the x-coordinate as an integer. """
        return int(self.x)

    @property
    def int_y(self):
        """ Returns the y-coordinate as an integer. """
        return int(self.y)

    def __repr__(self):
        return f"Point({{x: {self.x}, y: {self.y}}})"

    def __add__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float):
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Point(self.x * scalar, self.y * scalar)

    def __iter__(self):
        yield self.x
        yield self.y

    def __round__(self, ndigits=None) -> "Point":
        return Point(round(self.x, ndigits), round(self.y, ndigits))

    def scale(self, factor_x: float, factor_y: Optional[float] = None) -> "Point":
        """ Scales the point by the given factors.
        :param factor_x: The factor to scale the x-coordinate.
        :param factor_y: The factor to scale the y-coordinate. If None, factor_y will be set to factor_x.
        """
        if factor_y is None:
            factor_y = factor_x
        return Point(self.x * factor_x, self.y * factor_y)
