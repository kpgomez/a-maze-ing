from dataclasses import dataclass
import importlib
import re
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from src.models.maze import Maze
from src.models.solution import Solution
from src.view.renderer import SVG

console = Console()
prompt = Prompt()


@dataclass
class Location:
    """"""
    location: str
    locations: dict
    message_pitch: str
    message_prompt: str
    parameters: dict
    value: dict
    previous_location: str
    next_location: str
    mixin: str
    maze: Maze | None = None
    solution: Solution | None = None
    svg: SVG | None = None

    def __str__(self):
        """"""
        return f"{self.message_pitch}"

    def __repr__(self):
        """"""
        return f"{self.message_pitch}"

    def __next__(self):
        """"""
        return self.locations.get(self.next_location, self)

    @staticmethod
    def what_to_do_with_current_maze() -> str:
        console.print("You have an maze on hand. Would you like to save it first?", style="green")
        console.print("[1] Yes\n[2] No", style="white")
        return Prompt.ask("Choose by number", choices=["1", "2"], show_choices=False)

    @staticmethod
    def what_to_do_with_current_svg() -> str:
        console.print("You have an image on hand. Would you like to save it first?", style="green")
        console.print("[1] Yes\n[2] No", style="white")
        return Prompt.ask("Choose by number", choices=["1", "2"], show_choices=False)

    @staticmethod
    def what_to_do_with_current_solution() -> str:
        console.print("You have an solution on hand. Would you like to save it first?", style="green")
        console.print("[1] Yes\n[2] No", style="white")
        return Prompt.ask("Choose by number", choices=["1", "2"], show_choices=False)

    @staticmethod
    def transfer_maze_and_or_solution(location_next, maze: Maze | None = None, solution: Solution | None = None, svg: SVG | None = None):
        location_next.maze = maze
        location_next.solution = solution
        location_next.svg = svg
        return location_next

    @staticmethod
    def import_callable(module: str, callable: str):
        return getattr(importlib.import_module(module), callable)

    def status_update(self):
        location_str = self.location.replace("_", " ").title()
        maze_exists = "\n[√] maze" if self.maze is not None else ""
        solution_exists = "\n[√] solution" if self.solution is not None else ""
        svg_exists = "\n[√] image" if self.svg is not None else ""
        console.print(f"{location_str}{maze_exists}{solution_exists}{svg_exists}\n", style="white")

    def prompt_for_path(self) -> Path:
        console.print(self.message_prompt, style="green")
        console.print(r'Must avoid the following characters: <>:"/\.|?*', style="white")
        console.print("[1] Cancel")
        input_str = Prompt.ask("Input here")
        return input_str


class CreateMazeMixin:
    def action(self):
        try:
            self.status_update()
            # if a maze already exists
            if self.maze is not None:
                input_str = self.what_to_do_with_current_maze()
                if input_str == "1":
                    return self.transfer_maze_and_or_solution(self.locations.get("save_maze"), self.maze, self.solution, self.svg)

            # otherwise create a new maze
            location_callable = self.import_callable(self.value.get("module"), self.value.get("callable"))
            # gather user input
            input_dict = {}
            for key, value in self.parameters.items():
                console.print(f"{key}", style="green")
                # if selecting integer
                if value.get("type") == "int":
                    lower = int(value.get("value").get("lower"))
                    upper = int(value.get("value").get("upper"))
                    increment = int(value.get('value').get("increment"))
                    options = [str(i) for i in range(lower, upper+1, increment)]
                    input_user = int(Prompt.ask("Choose by number", choices=options, show_choices=False))
                    input_dict[value.get("kwarg")] = input_user
                # if selecting callable function or class
                elif value.get("type") == "dict":
                    value_dict = value.get("value")
                    options_dict = {}
                    for index, choice in enumerate([key for key in value_dict.keys()]):
                        index += 1
                        options_dict[str(index)] = value_dict.get(choice)
                        console.print(f"[{index}] {choice}.", style="white")
                    options_keys = [i for i in options_dict.keys()]
                    input_int = Prompt.ask("Choose by number", choices=options_keys, show_choices=False)
                    input_module_callable = options_dict.get(input_int)
                    input_callable = self.import_callable(input_module_callable.get("module"), input_module_callable.get("callable"))
                    input_dict[value.get("kwarg")] = input_callable
            # create maze
            maze = location_callable(**input_dict)
            console.print("Successfully created new maze!", style="yellow")
            return self.transfer_maze_and_or_solution(self.locations.get("main"), maze, None, None)
        except Exception as error:
            console.print("Something went wrong, please look under the hood and try again.", style="red")
            console.print(f"{error}", style="red")
            return self.transfer_maze_and_or_solution(self.locations.get(self.previous_location), self.maze, self.solution, self.svg)


class LoadMazeMixin:
    def action(self):
        try:
            self.status_update()
            # if maze already exists
            if self.maze is not None:
                input_str = self.what_to_do_with_current_maze()
                if input_str == "1":
                    return self.transfer_maze_and_or_solution(self.locations.get("save_maze"), self.maze, self.solution, self.svg)

            console.print(self.message_prompt, style="green")
            root_dir = Path.cwd()
            maze_dir = root_dir.joinpath("resources", "mazes")
            maze_paths = sorted([item for item in maze_dir.iterdir() if item.is_file() and item.suffix == ".maze"])
            maze_paths.append(root_dir.joinpath("Cancel"))
            options = []
            for index, path in enumerate(maze_paths):
                index += 1
                options.append(str(index))
                console.print(f"[{index}] {str(path.name)}", style="white")
            input_index = int(Prompt.ask("Choose by number", choices=options, show_choices=False))-1
            input_path = maze_paths[input_index]
            if str(input_path.name) == "Cancel":
                console.print("Leaving Load Maze.", style="yellow")
                return self.transfer_maze_and_or_solution(
                    self.locations.get(self.previous_location), self.maze, self.solution, self.svg)
            maze = Maze.read_file(input_path) or self.maze
            return self.transfer_maze_and_or_solution(
                self.locations.get(self.previous_location), maze, None, None)
        except Exception as error:
            console.print("Something went wrong, please look under the hood and try again.", style="red")
            console.print(f"{error}", style="red")
            return self.transfer_maze_and_or_solution(
                self.locations.get(self.previous_location), self.maze, self.solution, self.svg)


class SaveMazeMixin:
    def action(self):
        try:
            self.status_update()
            # if user doesn't have maze to save, take back to main
            if self.maze is None:
                console.print("Must have maze to save first.", style="yellow")
                return self.transfer_maze_and_or_solution(
                    self.locations.get(self.previous_location), self.maze, self.solution, self.svg)
            root_dir = Path.cwd()
            maze_dir = root_dir.joinpath("resources", "mazes")
            input_str =self.prompt_for_path()
            # if user wishes to cancel
            if input_str == "1":
                return self.transfer_maze_and_or_solution(
                    self.locations.get(self.previous_location), self.maze, self.solution, self.svg)
            # if filename is valid proceed
            if is_valid_filename(input_str):
                path = maze_dir.joinpath(f"{input_str}.maze")
                # if filename already exists take user back to main
                if path.exists():
                    console.print("File exists already. Please choose another filename.", style="yellow")
                    return self.transfer_maze_and_or_solution(self, self.maze, self.solution, self.svg)
                self.maze.write_file(path)
                console.print(f"{input_str} was successfully saved!", style="yellow")
                return self.transfer_maze_and_or_solution(
                    self.locations.get(self.previous_location), self.maze, self.solution, self.svg)
            # if file name is invalid, take user back to main
            else:
                console.print("Invalid file name please try again.", style="yellow")
                return self.transfer_maze_and_or_solution(self, self.maze, self.solution, self.svg)
        except Exception as error:
            console.print("Something went wrong, please look under the hood and try again.", style="red")
            console.print(f"{error}", style="red")
            return self.transfer_maze_and_or_solution(
                self.locations.get(self.previous_location), self.maze, self.solution, self.svg)


class SolveMazeMixin:
    def action(self):
        try:
            self.status_update()
            # if maze doesn't exist, pass back to main location
            if self.maze is None:
                console.print("Must have maze to save first.", style="yellow")
                return self.transfer_maze_and_or_solution(self.locations.get(self.previous_location), self.maze, self.solution, self.svg)
            # generate new solution and pass back to main location
            location_callable = self.import_callable(self.value.get("module"),self.value.get("callable"))
            solution = location_callable(self.maze)
            console.print("Solution successfully created", style="yellow")
            return self.transfer_maze_and_or_solution(self.locations.get(self.previous_location), self.maze,
                                                      solution or None, None)
        except Exception as error:
            console.print("Something went wrong, please look under the hood and try again.", style="red")
            console.print(f"{error}", style="red")
            return self.transfer_maze_and_or_solution(
                self.locations.get(self.previous_location), self.maze, self.solution, self.svg)


class TransitMixin:
    def action(self):
        try:
            self.status_update()
            console.print(self.message_prompt, style="green")
            options_dict = {}
            for index, choice in enumerate([i for i in self.locations.values()]):
                index += 1
                options_dict[str(index)] = choice
                console.print(f"[{index}] {choice}", style="white")
            options_keys = [i for i in options_dict.keys()]
            input_str = Prompt.ask("Choose by number", choices=options_keys, show_choices=False)

            return self.transfer_maze_and_or_solution(options_dict.get(input_str), self.maze, self.solution, self.svg)
        except Exception as error:
            console.print("Something went wrong, please look under the hood and try again.", style="red")
            console.print(f"{error}", style="red")
            return self.transfer_maze_and_or_solution(
                self.locations.get(self.previous_location), self.maze, self.solution, self.svg)


class ViewMazeMixin:
    def action(self):
        try:
            self.status_update()
            # svg already exists, pass to save image if user wishes to save it
            if self.svg:
                input_str = self.what_to_do_with_current_svg()
                if input_str == "1":
                    return self.transfer_maze_and_or_solution(
                        self.locations.get("save_image", "main"), self.maze, self.solution, self.svg)
            # if maze doesn't exist, pass back to main location
            if self.maze is None:
                console.print("Must have maze to save first.", style="yellow")
                return self.transfer_maze_and_or_solution(self.locations.get(self.previous_location), self.maze,
                                                          self.solution, self.svg)
            # generate new solution and pass back to main location
            location_callable = self.import_callable(self.value.get("module"), self.value.get("callable"))
            if self.solution is None:
                svg = location_callable().render(self.maze)
            else:
                console.print("Would you like to include the solution in the image?", style="green")
                console.print("[1] Yes\n[2] No\n[3] Cancel", style="white")
                input_str = Prompt.ask("Choose by number", choices=["1","2"], show_choices=False)
                if input_str == "1":
                    svg = location_callable().render(self.maze, self.solution)
                elif input_str == "3":
                    return self.transfer_maze_and_or_solution(self.locations.get(self.previous_location), self.maze,
                                                              self.solution, self.svg)
                else:
                    svg = location_callable().render(self.maze)
            svg.preview()
            console.print("Image was successfully created, check browser to view.", style="yellow")
            return self.transfer_maze_and_or_solution(self.locations.get(self.previous_location), self.maze,
                                                      self.solution, svg or None)
        except Exception as error:
            console.print("Something went wrong, please look under the hood and try again.", style="red")
            console.print(f"{error}", style="red")
            return self.transfer_maze_and_or_solution(
                self.locations.get(self.previous_location), self.maze, self.solution, self.svg)


class SaveImageMixin:
    def action(self):
        try:
            self.status_update()
            # if svg doesn't exist, pass back to main location
            if self.svg is None:
                console.print("Must have image to save first.", style="yellow")
                return self.transfer_maze_and_or_solution(self.locations.get(self.previous_location), self.maze,
                                                          self.solution, self.svg)
            # save svg
            root_dir = Path.cwd()
            maze_dir = root_dir.joinpath("resources", "mazes")
            input_str = self.prompt_for_path()
            # if user wishes to cancel
            if input_str == "1":
                return self.transfer_maze_and_or_solution(
                    self.locations.get(self.previous_location), self.maze, self.solution, self.svg)
            # if filename is valid proceed
            if is_valid_filename(input_str):
                path = maze_dir.joinpath(f"{input_str}.svg")
                # if filename already exists take user back to main
                if path.exists():
                    console.print("File exists already. Please choose another filename.", style="yellow")
                    return self.transfer_maze_and_or_solution(self, self.maze, self.solution, self.svg)
                # save image to file
                self.svg.write_file(path)
                console.print(f"{input_str} was successfully saved!", style="yellow")
                return self.transfer_maze_and_or_solution(
                    self.locations.get(self.previous_location), self.maze, self.solution, self.svg)
            else:
                # if filename is invalid
                console.print("Filename is not valid. Please try again.", style="yellow")
                return self.transfer_maze_and_or_solution(self.locations.get(self.previous_location), self.maze,
                                                      self.solution, self.svg)
        except Exception as error:
            console.print("Something went wrong, please look under the hood and try again.", style="red")
            console.print(f"{error}", style="red")
            return self.transfer_maze_and_or_solution(
                self.locations.get(self.previous_location), self.maze, self.solution, self.svg)


class DeleteMixin:
    def action(self):
        try:
            self.status_update()
            # make list of maze, solution, and svg filtering out those that are None
            state_list = [("Maze", self.maze), ("Solution", self.solution), ("Image", self.svg)]
            state_list = [item for item in state_list if item[1] is not None]
            # if non exist that return to main
            if len(state_list) == 0:
                console.print("Nothing to delete.", style="yellow")
                return self.transfer_maze_and_or_solution(self.locations.get(self.previous_location), self.maze, self.solution, self.svg)
            else:
                # otherwise prompt user which they would like to delete
                console.print("Type the number for each you would like to delete.", style="green")
                state_list.append(("Cancel",None))
                state_dict = {f"{index+1}": value[0] for index, value in enumerate(state_list)}
                for key, value in state_dict.items():
                    console.print(f"[{key}] {value}")
                input_str = Prompt.ask("Choose by numbers")
                input_conc = ""
                for i in input_str:
                    input_conc += state_dict.get(i,"")
                # cancel and return to main if user chooses
                if len(input_conc) == 0 or "Cancel" in input_conc:
                    console.print("Cancelling.", style="yellow")
                    return self.transfer_maze_and_or_solution(self.locations.get(self.previous_location), self.maze,
                                                       self.solution, self.svg)
                # delete user specified attributes
                return_message = ""
                if "Maze" in input_conc:
                    self.maze = None
                    return_message += ",maze"
                if "Solution" in input_conc:
                    self.solution = None
                    return_message += ",solution"
                if "Image" in input_conc:
                    self.svg = None
                    return_message += ",image"
                # tell user what was deleted before returning to main
                console.print(f"Successfully deleted...{return_message.replace(',','', 1)}", style="yellow")
                return self.transfer_maze_and_or_solution(self.locations.get(self.previous_location), self.maze,
                                                   self.solution, self.svg)
        except Exception as error:
            console.print("Something went wrong, please look under the hood and try again.", style="red")
            console.print(f"{error}", style="red")
            return self.transfer_maze_and_or_solution(
                self.locations.get(self.previous_location), self.maze, self.solution, self.svg)


class QuittingMixin:
    def action(self):
        try:
            self.status_update()
            if self.maze is not None:
                input_str = self.what_to_do_with_current_maze()
                # if cancelled
                if input_str == "1":
                    return self.transfer_maze_and_or_solution(self.locations.get("save_maze"), self.maze, self.solution, self.svg)
            console.print(self.message_prompt, style="green")
            input_dict = {}
            options = []
            index = 1
            for key, value in self.parameters.items():
                options.append(str(index))
                input_dict[str(index)] = value.get("value")
                console.print(f"[{index}] {key}", style="white")
                index += 1
            input_str = Prompt.ask("Choose by number", choices=options, show_choices=False)
            input_level = input_dict[input_str]
            return self.transfer_maze_and_or_solution(self.locations.get(input_level), self.maze, self.solution, self.svg)
        except Exception as error:
            console.print("Something went wrong, please look under the hood and try again.", style="red")
            console.print(f"{error}", style="red")
            return self.transfer_maze_and_or_solution(self.locations.get(self.next_location), self.maze, self.solution, self.svg)


class GoodByeMixin:
    def action(self):
        console.print(self, style="magenta")
        return self


def is_valid_filename(filename: str) -> bool:
    try:
        Path(filename)
        if re.search(r"[<*>?:/\.|]", filename):
            return False
        else:
            return True
    except (OSError, ValueError):
        return False


# if __name__=="__main__":
