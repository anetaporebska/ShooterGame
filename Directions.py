from enum import Enum


class Direction(Enum):
    DOWN = (0, 1)
    UP = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
