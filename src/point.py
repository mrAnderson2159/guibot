class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @property
    def tuple(self):
        return (self.x, self.y)

    @property
    def tuple_int(self):
        return (int(self.x), int(self.y))

    @property
    def int_x(self):
        return int(self.x)

    @property
    def int_y(self):
        return int(self.y)

    def __repr__(self):
        return f"Point({{x: {self.x}, y: {self.y}}})"
