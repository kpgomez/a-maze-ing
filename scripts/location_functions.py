import time
from pathlib import Path
import json
from scripts.location_classes import (
    Location,
    TransitMixin,
    SolveMazeMixin,
    CreateMazeMixin,
    LoadMazeMixin,
    SaveMazeMixin,
    QuittingMixin,
    GoodByeMixin,
    ViewMazeMixin,
    SaveImageMixin,
    # SaveSolutionMixin,
    DeleteMixin
)

sleep_in_seconds = 0.2

def sleep(multiple):
    """
    Causes a pause in the menu
    :param multiple:
    :return:
    """
    time.sleep(sleep_in_seconds*multiple)


def import_data() -> Location:
    """
    Import json file of Location objects and passes them to create_menu_objects.
    Returns Introduction Location instance.
    :return:
    """
    cwd = Path.cwd()
    path_messages = cwd.joinpath("resources", "text", "location_objects.json")
    with path_messages.open("r") as file:
        data = json.load(file)
        return_object = create_menu_objects(data)
    return return_object


def create_menu_objects(dict_import: dict) -> Location:
    """
    Take a dictionary of location objects and create graph of location instances.
    Return Intro Location instance
    :param dict_import:
    :return:
    """
    dict_menu = {}
    for key, value in dict_import.items():
        if value.get("mixin") == "TransitMixin":
            location_new = type("TransitLocation", (Location, TransitMixin), {})
            dict_menu[key] = location_new(**value)
        elif value.get("mixin") == "CreateMazeMixin":
            location_new = type("CreateMazeLocation", (Location, CreateMazeMixin), {})
            dict_menu[key] = location_new(**value)
        elif value.get("mixin") == "SolveMazeMixin":
            location_new = type("SolveMazeLocation", (Location, SolveMazeMixin), {})
            dict_menu[key] = location_new(**value)
        elif value.get("mixin") == "LoadMazeMixin":
            location_new = type("LoadMazeLocation", (Location, LoadMazeMixin), {})
            dict_menu[key] = location_new(**value)
        elif value.get("mixin") == "SaveMazeMixin":
            location_new = type("SaveMazeLocation", (Location, SaveMazeMixin), {})
            dict_menu[key] = location_new(**value)
        elif value.get("mixin") == "ViewMazeMixin":
            location_new = type("ViewMazeLocation", (Location, ViewMazeMixin), {})
            dict_menu[key] = location_new(**value)
        elif value.get("mixin") == "QuittingMixin":
            location_new = type("QuittingLocation", (Location, QuittingMixin), {})
            dict_menu[key] = location_new(**value)
        elif value.get("mixin") == "GoodByeMixin":
            location_new = type("GoodByeLocation", (Location, GoodByeMixin), {})
            dict_menu[key] = location_new(**value)
        elif value.get("mixin") == "SaveImageMixin":
            location_new = type("SaveImageLocation", (Location, SaveImageMixin), {})
            dict_menu[key] = location_new(**value)
        elif value.get("mixin") == "DeleteMixin":
            location_new = type("DeleteLocation", (Location, DeleteMixin), {})
            dict_menu[key] = location_new(**value)

    for menu in dict_menu.values():
        list_locations = {}
        for name, child in menu.locations.items():
            list_locations[name] = dict_menu.get(name)
        menu.locations = list_locations

    return dict_menu.get("intro")


# if __name__=="__main__":

