import pytest
import networkx as nx
from src.models.border import Border
from src.models.maze import Maze
from src.models.role import Role
from src.models.square import Square
from src.solve.solver import Edge, get_directed_edges, get_nodes, get_edges, make_graph, solve


# @pytest.mark.skip()
def test_flip(create_nodes):
    node_one, node_two = create_nodes
    actual = Edge(node_one, node_two).flip
    assert isinstance(actual, Edge)


# @pytest.mark.skip()
def test_distance(create_nodes):
    node_one, node_two = create_nodes
    actual = Edge(node_one, node_two).distance
    expected = 1.0
    assert actual == expected


# @pytest.mark.skip()
def test_solve(create_maze):
    maze = create_maze
    solved_maze = solve(maze)
    actual = [square.index for square in solved_maze]
    expected = [8, 9, 10, 11, 7, 6, 2]
    assert actual == expected


# @pytest.mark.skip()
def test_make_graph(create_maze):
    maze = create_maze
    actual = make_graph(maze)
    assert isinstance(actual, nx.DiGraph)


# @pytest.mark.skip()
def test_get_directed_edges(create_maze, create_nodes):
    maze = create_maze
    nodes = create_nodes
    actual = get_directed_edges(maze, nodes)
    expected = set()
    assert actual == expected


# @pytest.mark.skip()
def test_get_nodes(create_maze):
    maze = create_maze
    nodes = get_nodes(maze)
    actual = [node.index for node in nodes]
    expected = [5, 7, 0, 10, 6, 9, 11, 4, 1, 3, 8, 2]
    assert actual == expected


# @pytest.mark.skip()
def test_get_edges(create_maze, create_nodes):
    maze = create_maze
    nodes = create_nodes
    actual = get_edges(maze, nodes)
    expected = set()
    assert actual == expected


@pytest.fixture()
def create_maze():
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
    return maze


@pytest.fixture()
def create_nodes():
    squares = (Square(0, 0, 0, Border.TOP, Role.NONE), Square(1, 0, 1, Border.RIGHT, Role.NONE))
    return squares
