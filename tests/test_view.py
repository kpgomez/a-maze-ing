import pytest
import random

from pathlib import Path
from src.models.border import Border
from src.models.maze import Maze
from src.models.maze import Role
from src.models.maze import Solution
from src.models.square import Square
from src.view.decomposer import decompose
from src.view.primitives import NullPrimitive, Point, Line, Polyline, Polygon, DisjointedLines, Rect, Text
from src.view.renderer import SVG, SVGRenderer, background, exterior, wall, label

########################################################################################################################
# primitives

# @pytest.mark.skip()
def test_null_primitive():
    assert "" == NullPrimitive().draw(x=1, y=2)


# @pytest.mark.skip()
def test_point():
    actual = Point(100, 200).translate(100, 200).draw()
    expected = f"{200}, {400}"
    assert actual == expected


# @pytest.mark.skip()
def test_line(create_line):
    actual = create_line.draw(a=1, b=2)
    expected = "<line  x1='1' y1='1' x2='2' y2='1' a='1' b='2' />"
    assert actual == expected


# @pytest.mark.skip()
def test_polyline(create_polyline):
    actual = create_polyline.draw(a=1, b=2)
    expected = "<polyline  points='1, 1 2, 1 2, 2' a='1' b='2' />"
    assert actual == expected


# @pytest.mark.skip()
def test_polygon(create_polygon):
    actual = create_polygon.draw(a=1, b=2)
    expected = "<polygon  points='1, 1 2, 1 2, 2' a='1' b='2' />"
    assert actual == expected


# @pytest.mark.skip()
def test_disjointed_lines(create_disjointed_lines):
    actual = create_disjointed_lines.draw(a=1)
    expected = "<line  x1='1' y1='1' x2='2' y2='1' a='1' /><line  x1='1' y1='2' x2='2' y2='2' a='1' />"
    assert actual == expected


# @pytest.mark.skip()
def test_rect(create_rect):
    actual_zero = create_rect[0].draw(width="100%", height="100%", fill="white")
    expected_zero = "<rect  width='100%' height='100%' fill='white' x='1' y='1' />"
    actual_one = create_rect[1].draw(width="100%", height="100%", fill="white")
    expected_one = "<rect  width='100%' height='100%' fill='white' />"
    assert actual_zero == expected_zero
    assert actual_one == expected_one


# @pytest.mark.skip()
def test_text(create_text):
    actual = create_text.draw(a=1, b=2)
    expected = "<text  x='1' y='1' a='1' b='2'>🚶</text>"
    assert actual == expected

########################################################################################################################
# decomposer


# @pytest.mark.skip()
def test_single_border(create_borders, create_point):
    random_index = random.randint(0, len(create_borders) - 1)
    random_border = create_borders[random_index]
    actual = decompose(random_border, create_point, 1)
    assert isinstance(actual, Line)


# @pytest.mark.skip()
def test_disjointed_borders(create_borders, create_point):
    top_bottom = Border.TOP | Border.BOTTOM
    left_right = Border.LEFT | Border.RIGHT
    disjointed_borders = [top_bottom, left_right]
    random_borders = random.choice(disjointed_borders)
    actual = decompose(random_borders, create_point, 1)
    assert isinstance(actual, DisjointedLines)


# @pytest.mark.skip()
def test_corner(create_borders, create_point):
    top_right = Border.TOP | Border.RIGHT
    bottom_right = Border.RIGHT | Border.BOTTOM
    bottom_left = Border.BOTTOM | Border.LEFT
    top_left = Border.LEFT | Border.TOP

    corners = [top_right, bottom_right, bottom_left, top_left]
    random_corner = random.choice(corners)
    actual = decompose(random_corner, create_point, 1)
    assert isinstance(actual, Polyline)


# @pytest.mark.skip()
def test_dead_end(create_borders, create_point):
    top_right_bottom = Border.TOP | Border.RIGHT | Border.BOTTOM
    right_bottom_left = Border.RIGHT | Border.BOTTOM | Border.LEFT
    bottom_left_top = Border.BOTTOM | Border.LEFT | Border.TOP
    left_top_right = Border.LEFT | Border.TOP | Border.RIGHT

    dead_ends = [top_right_bottom, right_bottom_left, bottom_left_top, left_top_right]
    random_dead_end = random.choice(dead_ends)
    actual = decompose(random_dead_end, create_point, 1)
    assert isinstance(actual, Polyline)


# @pytest.mark.skip()
def test_four_borders(create_borders, create_point):
    borders = Border.TOP | Border.RIGHT | Border.BOTTOM | Border.LEFT
    actual = decompose(borders, create_point, 1)
    assert isinstance(actual, Polygon)

########################################################################################################################
# renderer


# @pytest.mark.skip()
def test_html_content():
    actual = SVG("test content").html_content
    expected = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="utf-8">\n  '
                '<meta name="viewport" content="width=device-width, initial-scale=1">\n  '
                '<title>SVG Preview</title>\n</head>\n<body>\ntest content\n</body>\n</html>')
    assert actual == expected

# TODO: if you want to test the preview functionality
# @pytest.mark.skip()
# def test_preview():
#     actual = SVG("test content").preview()
#     expected = None
#     assert actual == expected


# @pytest.mark.skip()
def test_write_file():
    path = Path.cwd().joinpath("resources","test_file")
    SVG("test content").write_file(path)
    if not path.exists():
        assert False, "SVG write_file method broken."
    else:
        path.unlink()


# @pytest.mark.skip()
def test_offset():
    actual = SVGRenderer(100, 6).offset
    expected = 3
    assert actual == expected


# @pytest.mark.skip()
def test_render(create_maze):
    maze = create_maze
    actual = SVGRenderer(100, 6).render(maze)
    expected = SVG(xml_content="<svg  xmlns='http://www.w3.org/2000/svg' stroke_linejoin='round' "
                               "width='418' height='318' viewBox='0 0 418 318'><rect  width='100%' "
                               "height='100%' fill='white' /><polyline  points='3, 103 3, 3 103, 3' "
                               "stroke_width='6' stroke='black' fill='none' /><polyline  "
                               "points='103, 3 203, 3 203, 103' stroke_width='6' stroke='black' "
                               "fill='none' /><text  x='253' y='53' font_size='50px' text_anchor='middle' "
                               "dominant_baseline='middle'>&#127937;</text><line  x1='203' y1='103' x2='203' "
                               "y2='3' stroke_width='6' stroke='black' fill='none' />"
                               "<line  x1='303' y1='3' x2='303' y2='103' stroke_width='6' "
                               "stroke='black' fill='none' /><polyline  "
                               "points='303, 103 303, 3 403, 3 403, 103' stroke_width='6' "
                               "stroke='black' fill='none' /><polyline  "
                               "points='103, 103 103, 203 3, 203 3, 103' "
                               "stroke_width='6' stroke='black' fill='none' />"
                               "<line  x1='103' y1='203' x2='103' y2='103' stroke_width='6' "
                               "stroke='black' fill='none' /><line  x1='203' y1='103' x2='203' "
                               "y2='203' stroke_width='6' stroke='black' fill='none' />"
                               "<polyline  points='303, 203 203, 203 203, 103' stroke_width='6' "
                               "stroke='black' fill='none' /><line  x1='403' y1='103' x2='403' y2='203' "
                               "stroke_width='6' stroke='black' fill='none' /><text  x='53' y='253' "
                               "font_size='50px' text_anchor='middle' dominant_baseline='middle'>"
                               "&#128694;</text><polyline  points='3, 303 3, 203 103, 203' "
                               "stroke_width='6' stroke='black' fill='none' />"
                               "<line  x1='103' y1='303' x2='203' y2='303' stroke_width='6' "
                               "stroke='black' fill='none' /><line  x1='203' y1='203' x2='303' y2='203' "
                               "stroke_width='6' stroke='black' fill='none' />"
                               "<line  x1='203' y1='303' x2='303' y2='303' stroke_width='6' "
                               "stroke='black' fill='none' /><polyline  points='403, 203 403, 303 303, 303' "
                               "stroke_width='6' stroke='black' fill='none' /></svg>")
    assert actual == expected


# @pytest.mark.skip()
def test_get_body(create_maze):
    maze = create_maze
    actual = SVGRenderer(100, 6)._get_body(maze, None)
    expected = ("<rect  width='100%' height='100%' fill='white' /><polyline  "
                "points='3, 103 3, 3 103, 3' stroke_width='6' stroke='black' "
                "fill='none' /><polyline  points='103, 3 203, 3 203, 103' "
                "stroke_width='6' stroke='black' fill='none' /><text  x='253' y='53' "
                "font_size='50px' text_anchor='middle' dominant_baseline='middle'>&#127937;</text>"
                "<line  x1='203' y1='103' x2='203' y2='3' stroke_width='6' stroke='black' "
                "fill='none' /><line  x1='303' y1='3' x2='303' y2='103' stroke_width='6' "
                "stroke='black' fill='none' /><polyline  points='303, 103 303, 3 403, 3 403, 103' "
                "stroke_width='6' stroke='black' fill='none' /><polyline  "
                "points='103, 103 103, 203 3, 203 3, 103' stroke_width='6' "
                "stroke='black' fill='none' /><line  x1='103' y1='203' x2='103' y2='103' "
                "stroke_width='6' stroke='black' fill='none' /><line  x1='203' y1='103' x2='203' y2='203' "
                "stroke_width='6' stroke='black' fill='none' /><polyline  "
                "points='303, 203 203, 203 203, 103' stroke_width='6' stroke='black' fill='none' />"
                "<line  x1='403' y1='103' x2='403' y2='203' stroke_width='6' stroke='black' fill='none' />"
                "<text  x='53' y='253' font_size='50px' text_anchor='middle' "
                "dominant_baseline='middle'>&#128694;</text><polyline  points='3, 303 3, 203 103, 203' "
                "stroke_width='6' stroke='black' fill='none' /><line  x1='103' y1='303' x2='203' y2='303' "
                "stroke_width='6' stroke='black' fill='none' /><line  x1='203' y1='203' x2='303' y2='203' "
                "stroke_width='6' stroke='black' fill='none' /><line  x1='203' y1='303' x2='303' y2='303' "
                "stroke_width='6' stroke='black' fill='none' /><polyline  points='403, 203 403, 303 303, 303' "
                "stroke_width='6' stroke='black' fill='none' />")
    assert actual == expected


# @pytest.mark.skip()
def test_draw_square(create_square):
    actual = SVGRenderer(100, 6)._draw_square(create_square)
    expected = "<line  x1='3' y1='3' x2='103' y2='3' stroke_width='6' stroke='black' fill='none' />"
    assert actual == expected


# @pytest.mark.skip()
def test_draw_solution(create_solution):
    solution = create_solution
    actual = SVGRenderer(100, 6)._draw_solution(solution)
    expected = ("<polyline  points='53, 253 153, 253 253, 253 353, 253 353, 153 253, 153 253, 53' "
                "stroke_width='12' stroke_opacity='50%' stroke='red' fill='none' "
                "marker_end='url(#arrow)' />")
    assert actual == expected


# @pytest.mark.skip()
def test_transform(create_square):
    square = create_square
    actual = SVGRenderer(100, 6)._transform(square, 3)
    expected = Point(x=6, y=6)
    assert actual == expected


# @pytest.mark.skip()
def test_draw_border(create_square, create_point):
    square = create_square
    point = create_point
    actual = SVGRenderer(100, 6)._draw_border(square, point)
    expected = "<line  x1='1' y1='1' x2='101' y2='1' stroke_width='6' stroke='black' fill='none' />"
    assert actual == expected


# @pytest.mark.skip()
def test_background():
    actual = background()
    expected = "<rect  width='100%' height='100%' fill='white' />"
    assert actual == expected


# @pytest.mark.skip()
def test_exterior(create_point):
    point = create_point
    actual = exterior(point, 5, 5)
    expected = "<rect  width='5' height='5' stroke_width='5' stroke='none' fill='white' x='1' y='1' />"
    assert actual == expected


# @pytest.mark.skip()
def test_wall(create_point):
    point = create_point
    actual = wall(point, 5, 5)
    expected = "<rect  width='5' height='5' stroke_width='5' stroke='none' fill='lightgray' x='1' y='1' />"
    assert actual == expected


# @pytest.mark.skip()
def test_label(create_emoji, create_point):
    emoji = create_emoji
    point = create_point
    actual = label(emoji, point, 2)
    expected = "<text  x='3' y='3' font_size='2px' text_anchor='middle' dominant_baseline='middle'>🚶</text>"
    assert actual == expected


########################################################################################################################
# fixtures

@pytest.fixture
def create_borders():
    return Border.TOP, Border.RIGHT, Border.BOTTOM, Border.LEFT


@pytest.fixture
def create_point():
    return Point(1, 1)


@pytest.fixture
def create_line():
    # line
    return Line(Point(1, 1), Point(2, 1))


@pytest.fixture
def create_polyline():
    return Polyline([Point(1, 1), Point(2, 1), Point(2, 2)])


@pytest.fixture
def create_polygon():
    return Polygon([Point(1, 1), Point(2, 1), Point(2, 2)])


@pytest.fixture
def create_disjointed_lines():
    return DisjointedLines([Line(Point(1, 1), Point(2, 1)), Line(Point(1, 2), Point(2, 2))])


@pytest.fixture
def create_rect():
    return Rect(Point(1, 1)), Rect()


@pytest.fixture()
def create_text():
    return Text("\N{pedestrian}", Point(1, 1))


@pytest.fixture()
def create_square():
    return Square(0, 0, 0, Border.TOP)


@pytest.fixture()
def create_solution(create_maze):
    maze = create_maze
    return Solution(squares=tuple(maze[i] for i in (8, 9, 10, 11, 7, 6, 2)))


@pytest.fixture()
def create_maze():
    maze = Maze(
        squares=(
            Square(0, 0, 0, Border.TOP | Border.LEFT),
            Square(1, 0, 1, Border.TOP | Border.RIGHT),
            Square(2, 0, 2, Border.LEFT | Border.RIGHT, role=Role.EXIT),
            Square(3, 0, 3, Border.TOP | Border.LEFT | Border.RIGHT),
            Square(4, 1, 0, Border.BOTTOM | Border.LEFT | Border.RIGHT),
            Square(5, 1, 1, Border.LEFT | Border.RIGHT),
            Square(6, 1, 2, Border.BOTTOM | Border.LEFT),
            Square(7, 1, 3, Border.RIGHT),
            Square(8, 2, 0, Border.TOP | Border.LEFT, role=Role.ENTRANCE),
            Square(9, 2, 1, Border.BOTTOM),
            Square(10, 2, 2, Border.TOP | Border.BOTTOM),
            Square(11, 2, 3, Border.BOTTOM | Border.RIGHT),
        )
    )
    return maze


@pytest.fixture()
def create_emoji():
    return "\N{pedestrian}"
