from enum import IntFlag


class Border(IntFlag):
    """
    class IntFlag enum for square borders
    """
    EMPTY = 0
    TOP = 1
    RIGHT = 8
    BOTTOM = 2
    LEFT = 4

    @property
    def corner(self) -> bool:
        """
        will check self if square border is a corner
        """
        return self in (
            self.TOP | self.RIGHT,
            self.RIGHT | self.BOTTOM,
            self.BOTTOM | self.LEFT,
            self.LEFT | self.TOP
        )

    @property
    def dead_end(self) -> bool:
        """
        will check self if square border is a dead end
        """
        # return self.bit_count() == 3
        return self in (
            self.TOP | self.RIGHT | self.BOTTOM,
            self.RIGHT | self.BOTTOM | self.LEFT,
            self.BOTTOM | self.LEFT | self.TOP,
            self.LEFT | self.TOP | self.RIGHT
        )

    @property
    def intersection(self) -> bool:
        """
        will check self if square border is an intersection
        """
        # return self.bit_count() < 2
        return self in (
            self.TOP,
            self.RIGHT,
            self.BOTTOM,
            self.LEFT,
            self.EMPTY
        )