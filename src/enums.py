from enum import Enum

class Interval(Enum):
    """ Enum for different time intervals used in mouse/keyboard control operations. """
    INSTANT = 0.1
    SHORT = 0.3
    MEDIUM = 0.5
    LONG = 1.0
