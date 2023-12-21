from enum import IntEnum


class Role(IntEnum):
    """
    class IntEnum for square role
    """
    NONE = 0
    ENEMY = 1
    ENTRANCE = 2
    EXIT = 3
    EXTERIOR = 4
    REWARD = 5
    WALL = 6


