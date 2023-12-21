import pytest
from collections.abc import Iterable


from src.models.border import Border
from src.models.maze import Maze
from src.models.role import Role
from src.models.solution import Solution, validate_solution_corridor
from src.models.square import Square



################################################################################################################
# Role


# @pytest.mark.skip("TODO")
# def test_role_exists():
#     assert Role


# @pytest.mark.skip("TODO")
def test_role_values():
    variable_list = ["NONE", "ENEMY", "ENTRANCE", "EXIT", "EXTERIOR", "REWARD", "WALL"]
    for index, name in enumerate(variable_list):
        assert Role[name] == index


###############################################################################################################
# Border

#@pytest.mark.skip("TODO")
# def test_border_exists():
#     assert Border


#@pytest.mark.skip("TODO")
def test_border_values():
    variable_list = ["EMPTY", "TOP", "RIGHT", "BOTTOM", "LEFT"]
    index_list = [0, 1, 8, 2, 4]
    for index, name in enumerate(variable_list):
        assert Border[name] == index_list[index]


# @pytest.mark.skip("TODO")
def test_border_corner():
    top_right = Border(Border.TOP | Border.RIGHT).corner
    right_bottom = Border(Border.RIGHT | Border.BOTTOM).corner
    bottom_left = Border(Border.BOTTOM | Border.LEFT).corner
    left_top = Border(Border.LEFT | Border.TOP).corner
    assert top_right and right_bottom and bottom_left and left_top


# @pytest.mark.skip("TODO")
def test_dead_end():
    assert all([Border(Border.TOP | Border.RIGHT | Border.BOTTOM).dead_end,
                Border(Border.RIGHT | Border.BOTTOM | Border.LEFT).dead_end,
                Border(Border.BOTTOM | Border.LEFT | Border.TOP).dead_end,
                Border(Border.LEFT | Border.TOP | Border.RIGHT).dead_end])


# @pytest.mark.skip("TODO")
def test_intersection():
    assert all([Border(Border.EMPTY).intersection, Border(Border.TOP).intersection, Border(Border.RIGHT).intersection,
                Border(Border.BOTTOM).intersection, Border(Border.LEFT).intersection])


######################################################################################################################
# Square

# @pytest.mark.skip("TODO")
def test_square_creation():
    square = Square(1, 2, 3, Border.TOP, Role.EXIT)
    assert square.index == 1
    assert square.row == 2
    assert square.column == 3
    assert square.border is Border.TOP
    assert square.role is Role.EXIT


# @pytest.mark.skip("TODO")
def test_square_immutable():
    square = Square(1, 2, 3, Border.TOP, Role.EXIT)
    with pytest.raises(Exception):
        square.index = 2


######################################################################################################################
# Maze

# @pytest.mark.skip("TODO")
def test_maze_creation():
    maze = Maze(
         squares=(
             Square(0, 0, 0, Border.TOP | Border.LEFT),
             Square(1, 0, 1, Border.TOP | Border.RIGHT),
             Square(2, 0, 2, Border.LEFT | Border.RIGHT, Role.EXIT),
             Square(3, 0, 3, Border.TOP | Border.LEFT | Border.RIGHT),
             Square(4, 1, 0, Border.BOTTOM | Border.LEFT | Border.RIGHT),
             Square(5, 1, 1, Border.LEFT | Border.RIGHT),
             Square(6, 1, 2, Border.BOTTOM | Border.LEFT),
             Square(7, 1, 3, Border.RIGHT),
             Square(8, 2, 0, Border.TOP | Border.LEFT, Role.ENTRANCE),
             Square(9, 2, 1, Border.BOTTOM),
             Square(10, 2, 2, Border.TOP | Border.BOTTOM),
             Square(11, 2, 3, Border.BOTTOM | Border.RIGHT),
         )
     )
    assert isinstance(maze, Maze)

# @pytest.mark.skip("TODO")
def test_maze_method():
    maze = Maze(
         squares=(
             Square(0, 0, 0, Border.TOP | Border.LEFT),
             Square(1, 0, 1, Border.TOP | Border.RIGHT),
             Square(2, 0, 2, Border.LEFT | Border.RIGHT, Role.EXIT),
             Square(3, 0, 3, Border.TOP | Border.LEFT | Border.RIGHT),
             Square(4, 1, 0, Border.BOTTOM | Border.LEFT | Border.RIGHT),
             Square(5, 1, 1, Border.LEFT | Border.RIGHT),
             Square(6, 1, 2, Border.BOTTOM | Border.LEFT),
             Square(7, 1, 3, Border.RIGHT),
             Square(8, 2, 0, Border.TOP | Border.LEFT, Role.ENTRANCE),
             Square(9, 2, 1, Border.BOTTOM),
             Square(10, 2, 2, Border.TOP | Border.BOTTOM),
             Square(11, 2, 3, Border.BOTTOM | Border.RIGHT),
         )
     )
    # testing width property
    assert maze.width == 4
    # testing height property
    assert maze.height == 3
    # testing subscriptable
    assert maze[3].row == 0
    # testing entrance property
    assert maze.entrance.role is Role.ENTRANCE
    # testing exit property
    assert maze.exit.role is Role.EXIT


#######################################################################################################################
# Solution

# @pytest.mark.skip("TODO")
def test_solution_creation():
    solution = Solution(
        squares = (
            Square(8, 2, 0, Border.TOP | Border.LEFT, Role.ENTRANCE),
            Square(9, 2, 1, Border.BOTTOM),
            Square(10, 2, 2, Border.TOP | Border.BOTTOM),
            Square(11, 2, 3, Border.BOTTOM | Border.RIGHT),
            Square(7, 1, 3, Border.RIGHT),
            Square(6, 1, 2, Border.BOTTOM | Border.LEFT),
            Square(2, 0, 2, Border.LEFT | Border.RIGHT, Role.EXIT),
        )
    )
    assert isinstance(solution, Solution)

# @pytest.mark.skip("TODO")
def test_solution_methods():
    solution0 = Solution(
        squares = (
            Square(8, 2, 0, Border.TOP | Border.LEFT, Role.ENTRANCE),
            Square(9, 2, 1, Border.BOTTOM),
            Square(10, 2, 2, Border.TOP | Border.BOTTOM),
            Square(11, 2, 3, Border.BOTTOM | Border.RIGHT),
            Square(7, 1, 3, Border.RIGHT),
            Square(6, 1, 2, Border.BOTTOM | Border.LEFT),
            Square(2, 0, 2, Border.LEFT | Border.RIGHT, Role.EXIT),
        )
    )
    solution1 = Solution(
        squares=(
            Square(8, 2, 0, Border.TOP | Border.LEFT, Role.ENTRANCE),
            Square(9, 2, 1, Border.BOTTOM),
            Square(10, 2, 2, Border.TOP | Border.BOTTOM),
            Square(11, 2, 3, Border.BOTTOM | Border.RIGHT),
            Square(7, 1, 3, Border.RIGHT),
            Square(6, 1, 2, Border.BOTTOM | Border.LEFT),
            Square(2, 0, 2, Border.LEFT | Border.RIGHT, Role.EXIT),
        )
    )
    assert len(solution0) == 7
    assert isinstance(solution0, Iterable)
    assert solution0[3].index == 11
    assert solution0 == solution1

# @ pytest.mark.skip("TODO")
def test_validate_solution_corridor_fail():
    solution = Solution(
        squares=(
            Square(8, 2, 0, Border.TOP | Border.LEFT, Role.ENTRANCE),
            Square(9, 2, 1, Border.BOTTOM),
            Square(10, 2, 2, Border.TOP | Border.BOTTOM),
            Square(11, 2, 3, Border.BOTTOM | Border.RIGHT),
            Square(7, 0, 0, Border.RIGHT),
            Square(6, 1, 2, Border.BOTTOM | Border.LEFT),
            Square(2, 0, 2, Border.LEFT | Border.RIGHT, Role.EXIT),
        )
    )

    with pytest.raises(ValueError):
        validate_solution_corridor(solution)



