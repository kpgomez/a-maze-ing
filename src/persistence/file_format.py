import array
import struct

from dataclasses import dataclass
from typing import BinaryIO

MAGIC_NUMBER: bytes = b"MAZE"


@dataclass(frozen=True)
class FileHeader:
    """
    Dataclass to create binary file header for maze.
    """
    format_version: int
    width: int
    height: int

    @classmethod
    def read(cls, file: BinaryIO):
        """
        Input file path to create instance of fileheader from binary maze file.
        """
        assert(file.read(len(MAGIC_NUMBER)) == MAGIC_NUMBER), "Unknown file type"
        (format_version, ) = struct.unpack("B", file.read(1))
        width, height = struct.unpack("<2I", file.read(2*4))
        return cls(format_version, width, height)

    def write(self, file: BinaryIO) -> None:
        """
        Input file to write header to binary maze file.
        """
        file.write(MAGIC_NUMBER)
        file.write(struct.pack("B", self.format_version))
        file.write(struct.pack("<2I", self.width, self.height))


@dataclass(frozen=True)
class FileBody:
    """
    Dataclass to create binary file body for maze.
    """
    square_values: array.array

    @classmethod
    def read(cls, header: FileHeader, file: BinaryIO) -> "FileBody":
        """
        Reads maze binary file and returns FileBody.
        :param header: FileHeader
        :param file: BinaryIO
        :return: FileBody
        """
        return cls(array.array("B", file.read(header.width * header.height)))

    def write(self, file: BinaryIO) -> None:
        """
        Input file to write body of binary maze file.
        """
        file.write(self.square_values.tobytes())
