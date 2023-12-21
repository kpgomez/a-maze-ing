import array
import pathlib
from typing import Iterator

from src.models.border import Border
from src.models.role import Role
from src.models.square import Square
from src.persistence.file_format import FileBody, FileHeader


FORMAT_VERSION: int = 1


def write_binary_maze_file(path: pathlib.Path, squares: tuple[Square, ...], width: int, height: int) -> None:
    """
    Input file path object, maze squares, width, and height to binary maze file.
    """
    header = FileHeader(FORMAT_VERSION, width, height)
    body = FileBody(array.array("B", map(compress, squares)))
    with path.open(mode="wb") as file:
        header.write(file)
        body.write(file)


def compress(square: Square) -> int:
    """
    Compress role and border values into an integer.
    """
    return (square.role << 4) | square.border.value



def load_binary_maze_file(path: pathlib.Path) -> Iterator[Square]:
    """
    Load maze data and return iterable of square elements.
    :param path: pathlib.Path
    :return: Iterator[Square]
    """
    with path.open("rb") as file:
        header = FileHeader.read(file)
        if header.format_version != FORMAT_VERSION:
            raise ValueError("Unsupported file format version.")
        body = FileBody.read(header, file)
        return deserializer(header, body)


def deserializer(header: FileHeader, body: FileBody) -> Iterator[Square]:
    """
    Input FileHeader instance and FileBody instance.
    Output is iterator generator.
    :param header:
    :param body:
    :return:
    """
    for index, square_value in enumerate(body.square_values):
        row, column = divmod(index, header.width)
        border, role = decompress(square_value)
        yield Square(index, row, column, border, role)


def decompress(square_value):
    """
    Input integer and extract binary values.
    :param square_value:
    :return:
    """
    border = Border(square_value & 15) # b'00001111'
    role = Role(square_value >> 4)
    return border, role


# if __name__ == "__main__":
