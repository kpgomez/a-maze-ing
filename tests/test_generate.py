import pytest
import textwrap

from src.models.maze import Maze
from src.models.square import Square
from src.models.role import Role
from src.models.border import Border
from src.generate.convert_api_maze import (
    string_to_list,
    find_dim,
    maze_to_dictionary,
    generate_maze,
    string_to_maze
)
from src.generate.create_maze import create_maze, create_api

################################################################################
# create_maze.py

# @pytest.mark.skip()
def test_create_api(create_maze_api):
    maze_list = create_maze_api.split("\n")
    char_bool = True
    for line in maze_list:
        for char in line:
            if char not in "# SE+":
                char_bool =False
                break
    assert len(maze_list) == 11
    assert len(maze_list[0]) == 11
    assert char_bool


#########################################################################################
# convert_api_maze.py

# @pytest.mark.skip()
def test_string_to_list(create_maze_string):
    maze_list = string_to_list(create_maze_string)
    assert len(maze_list) == 7
    assert len(maze_list[0]) == 7


# @pytest.mark.skip()
def test_find_dim(create_maze_string):
    maze_list = create_maze_string.split("\n")
    dim_dict = find_dim(maze_list)
    assert dim_dict.get("height") == 7
    assert dim_dict.get("width") == 7


# @pytest.mark.skip()
def test_maze_to_dictionary(create_maze_string):
    maze_list = create_maze_string.split("\n")
    maze_dict = maze_to_dictionary(maze_list)
    string_list = []
    for i in range(0,7):
        for j in range(0,7):
            string_list.append(f"{i},{j}")
    for item in string_list:
        assert maze_dict.get(item,False)
        assert maze_dict.get(item) in "# SE+"


# @pytest.mark.skip()
def test_generate_maze(create_maze_string, create_maze_generate):
    maze_list = string_to_list(create_maze_string)
    maze_dim = find_dim(maze_list)
    maze_dict = maze_to_dictionary(maze_list)
    maze_new = generate_maze(maze_dict, maze_dim)

    for sqr_actual in maze_new:
        sqr_expected = create_maze_generate[sqr_actual.index]
        assert sqr_actual == sqr_expected


# @pytest.mark.skip()
def test_string_to_maze(create_maze_string, create_maze_generate):
    maze_new = string_to_maze(create_maze_string)
    for sqr_actual in maze_new:
        sqr_expected = create_maze_generate[sqr_actual.index]
        assert sqr_actual == sqr_expected


@pytest.fixture
def create_maze_string():
    return textwrap.dedent("""#######
# #   #
# # # #
# # # S
# ### #
E     #
#######""")

@pytest.fixture
def create_maze_generate():
    return Maze(
        squares=(
                Square(0, 0, 0, 13, 0),
                Square(1, 0, 1, 5, 0),
                Square(2, 0, 2, 9, 0),
                Square(3, 1, 0, 12, 0),
                Square(4, 1, 1, 14, 0),
                Square(5, 1, 2, 4, Role.ENTRANCE),
                Square(6, 2, 0, 2, Role.EXIT),
                Square(7, 2, 1, 3, 0),
                Square(8, 2, 2, 10, 0)))

# TODO: remove after finishing everything just so you don't make excessive requests to the api
@pytest.fixture
def create_maze_api():
    return create_api()


