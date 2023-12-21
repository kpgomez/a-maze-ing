import tempfile
import textwrap
import webbrowser
from dataclasses import dataclass
from pathlib import Path

from src.models.maze import Maze
from src.models.role import Role
from src.models.solution import Solution
from src.models.square import Square
from src.view.decomposer import decompose
from src.view.primitives import Point, Polyline, Rect, Text, tag

ROLE_EMOJI = {
    # Role.ENTRANCE: "\N{pedestrian}",
    # Role.EXIT: "\N{chequered flag}",
    Role.ENTRANCE: "&#128694;",
    Role.EXIT: "&#127937;",
    Role.ENEMY: "\N{ghost}",
    Role.REWARD: "\N{white medium star}",
}


@dataclass(frozen=True)
class SVG:
    """

    """

    xml_content: str

    @property
    def html_content(self) -> str:
        """"""
        return textwrap.dedent(
            """\
                <!DOCTYPE html>
                <html lang="en">
                <head>
                  <meta charset="utf-8">
                  <meta name="viewport" content="width=device-width, initial-scale=1">
                  <title>SVG Preview</title>
                </head>
                <body>
                {0}
                </body>
                </html>""").format(self.xml_content)

    def preview(self) -> None:
        """
        Takes xml content from class instance, opens a temporary file, calls html_content method to convert xml to html,
        writes to file, opens browser
        """
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".html", delete=False) as file:
            file.write(self.html_content)
        webbrowser.open(f"file://{file.name}")

    def write_file(self, path: Path) -> None:
        with path.open(mode="w") as file:
            file.write(self.xml_content)


@dataclass(frozen=True)
class SVGRenderer:
    """"""
    square_size: int = 50
    line_width: int = 20

    @property
    def offset(self) -> int:
        """

        """
        return self.line_width // 2

    def render(self, maze: Maze, solution: Solution | None = None) -> SVG:
        """

        """
        margin = 2 * (self.offset + self.line_width)
        width = margin + maze.width * self.square_size
        height = margin + maze.height * self.square_size

        return SVG(
            tag("svg",
                self._get_body(maze, solution),
                xmlns="http://www.w3.org/2000/svg",
                stroke_linejoin="round",
                width=width,
                height=height,
                viewBox=f"0 0 {width} {height}",))

    def _get_body(self, maze: Maze, solution: Solution | None) -> str:
        """

        """
        return "".join([
            background(),
            *map(self._draw_square, maze),
            self._draw_solution(solution) if solution is not None else ""
        ])

    def _draw_square(self, square: Square) -> str:
        """"""
        top_left = self._transform(square)
        collective_xml = []
        if square.role is Role.EXTERIOR:
            exterior_xml = exterior(top_left, self.square_size, self.line_width)
            collective_xml.append(exterior_xml)
        elif square.role is Role.WALL:
            wall_xml = wall(top_left, self.square_size, self.line_width)
            collective_xml.append(wall_xml)
        elif emoji := ROLE_EMOJI.get(square.role):
            emoji_xml = label(emoji, top_left, self.square_size//2)
            collective_xml.append(emoji_xml)
        border_xml = self._draw_border(square, top_left)
        collective_xml.append(border_xml)
        return "".join(collective_xml)

    def _draw_solution(self, solution: Solution) -> str:
        """

        """
        return Polyline([self._transform(square, extra_offset=self.square_size//2) for square in solution]).draw(
            stroke_width=self.line_width * 2,
            stroke_opacity="50%",
            stroke="red",
            fill="none",
            marker_end="url(#arrow)",
        )

    def _transform(self, square: Square, extra_offset: int=0) -> Point:
        """
        """
        x = square.column * self.square_size
        y = square.row * self.square_size
        top_left_point = Point(x, y).translate(offset_x=self.offset+extra_offset, offset_y=self.offset+extra_offset)
        return top_left_point

    def _draw_border(self, square: Square, point: Point) -> str:
        """

        """
        return decompose(square.border, point, self.square_size).draw(
            stroke_width=self.line_width,
            stroke="black",
            fill="none")


def background():
    """

    """
    return Rect().draw(width="100%", height="100%", fill="white")


def exterior(top_left: Point, size: int, line_width: int) -> str:
    """

    """
    return Rect(top_left).draw(
        width=size,
        height=size,
        stroke_width=line_width,
        stroke="none",
        fill="white",)


def wall(top_left: Point, size: int, line_width: int) -> str:
    """

    """
    return Rect(top_left).draw(
        width=size,
        height=size,
        stroke_width=line_width,
        stroke="none",
        fill="lightgray", )


def label(emoji: str, top_left: Point, off_set: int) -> str:
    """

    """
    return Text(emoji, top_left.translate(offset_x=off_set, offset_y=off_set)).draw(
        font_size=f"{off_set}px",
        text_anchor="middle",
        dominant_baseline="middle",
    )



# if __name__ == "__main__":














