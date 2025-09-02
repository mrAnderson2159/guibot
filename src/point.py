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
