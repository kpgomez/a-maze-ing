from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Iterator

from src.models.role import Role
from src.models.square import Square
from src.models.solution import Solution
# from src.solve.solver import solve
from src.persistence.serializer import write_binary_maze_file, load_binary_maze_file


@dataclass(frozen=True)
class Maze:
    """
    dataclass Maze represents maze as tuple of squares
    """
    squares: tuple[Square, ...]

    def __post_init__(self) -> None:
        """
        raises exception if maze fails validation
        """
        validate_maze_entrance(self)
        validate_maze_exit(self)
        validate_maze_indices(self)
        validate_maze_rows_and_columns(self)

    def __iter__(self) -> Iterator[Square]:
        """
        transform maze into iterable
        """
        return iter(self.squares)

    def __getitem__(self, index: int) -> Square:
        """
        input index return square from maze
        """
        return self.squares[index]


    @cached_property
    def width(self) -> int:
        """
        returns max width of the maze
        """
        return max([square.column for square in self]) + 1

    @cached_property
    def height(self) -> int:
        """
        returns max height of the maze
        """
        return max([square.row for square in self]) + 1

    @cached_property
    def entrance(self) -> Square:
        """
        returns entrance of maze
        """
        for square in self:
            if square.role is Role.ENTRANCE:
                return square

    @cached_property
    def exit(self) -> Square:
        """
        returns exit of maze
        """
        for square in self:
            if square.role is Role.EXIT:
                return square

    def write_file(self, path: Path) -> None:
        """
        Accepts file path object and writes maze as binary file.
        """
        write_binary_maze_file(path, self.squares, self.width, self.height)

    @classmethod
    def read_file(cls, path: Path) -> "Maze":
        """
        Input file path and output maze instance with data from binary maze file.
        :param path:
        :return:
        """
        return Maze(tuple(load_binary_maze_file(path)))


def validate_maze_entrance(maze: Maze) -> None:
    """
    raises exception if maze doesn't have exactly one entrance
    """
    count = 0
    for square in maze:
        if square.role is Role.ENTRANCE:
            count += 1
    assert count == 1, "Maze must have exactly one entrance"


def validate_maze_exit(maze: Maze) -> None:
    """
    raises exception if maze doesn't have exactly one exit
    """
    count = 0
    for square in maze:
        if square.role is Role.EXIT:
            count += 1
    assert count == 1, "Maze must have exactly one exit"


def validate_maze_indices(maze: Maze) -> None:
    """
    raises exception if maze squares don't have valid indices
    """
    actual_maze_indices = [square.index for square in maze]
    expected_maze_indices = [i for i in range(len(maze.squares))]
    assert actual_maze_indices == expected_maze_indices, "One or more maze square index value is invalid"


def validate_maze_rows_and_columns(maze: Maze) -> None:
    """
    raises exception if maze squares don't have valid row and column attributes
    """
    for i in range(0, maze.height):
        for j in range(0, maze.width):
            index = i * maze.width + j
            square = maze[index]
            assert square.row == i, f"maze square at {i, j} contains invalid row value"
            assert square.column == j, f"maze square at {i, j} contains invalid column value"


# if __name__ == "__main__":
