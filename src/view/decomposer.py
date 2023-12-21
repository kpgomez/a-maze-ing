from src.models.border import Border
from src.view.primitives import (
    NullPrimitive,
    Primitive,
    Point,
    Line,
    Polyline,
    Polygon,
    DisjointedLines
)


def decompose(border: Border, top_left: Point, square_size: int) -> Primitive:
    """
    Will return instance of square shape based on square border
    """
    top_right = top_left.translate(offset_x=square_size)
    bottom_right = top_left.translate(offset_x=square_size, offset_y=square_size)
    bottom_left = top_left.translate(offset_y=square_size)

    top = Line(top_left, top_right)
    right = Line(top_right, bottom_right)
    bottom = Line(bottom_left, bottom_right)
    left = Line(bottom_left, top_left)

    # catching 4 borders
    if border is Border.TOP | Border.RIGHT | Border.BOTTOM | Border.LEFT:
        return Polygon([top_left, top_right, bottom_right, bottom_left])

    # catching 3 borders
    if border is Border.TOP | Border.RIGHT | Border.BOTTOM: # does not have left
        return Polyline([top_left, top_right, bottom_right, bottom_left])
    if border is Border.RIGHT | Border.BOTTOM | Border.LEFT: # does not have top
        return Polyline([top_right, bottom_right, bottom_left, top_left])
    if border is Border.TOP | Border.BOTTOM | Border.LEFT: # does not have right
        return Polyline([bottom_right, bottom_left, top_left, top_right])
    if border is Border.TOP | Border.RIGHT | Border.LEFT: # does not have bottom
        return Polyline([bottom_left, top_left, top_right, bottom_right])

    # catching 2 borders, corners
    if border is Border.TOP | Border.RIGHT:
        return Polyline([top_left, top_right, bottom_right])
    if border is Border.RIGHT | Border.BOTTOM:
        return Polyline([top_right, bottom_right, bottom_left])
    if border is Border.BOTTOM | Border.LEFT:
        return Polyline([bottom_right, bottom_left, top_left])
    if border is Border.LEFT | Border.TOP:
        return Polyline([bottom_left, top_left, top_right])

    # catching 2 borders, disjointed
    if border is Border.TOP | Border.BOTTOM:
        return DisjointedLines([top, bottom])
    if border is Border.LEFT | Border.RIGHT:
        return DisjointedLines([left, right])

    # catching single borders
    if border is Border.TOP:
        return top
    if border is Border.RIGHT:
        return right
    if border is Border.BOTTOM:
        return bottom
    if border is Border.LEFT:
        return left

    # no borders
    return NullPrimitive()
