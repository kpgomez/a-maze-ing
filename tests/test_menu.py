import pytest
from pathlib import Path
import json
from scripts.location_functions import import_data, create_menu_objects
from scripts.location_classes import is_valid_filename
from scripts.main import main

##################################################################################
# location_functions.py


# @pytest.mark.skip()
def test_is_valid_filename(create_path):
    actual = is_valid_filename(create_path.name.replace(".json", ""))
    assert actual is True


# @pytest.mark.skip()
def test_is_valid_filename_fail(create_path):
    actual = is_valid_filename(create_path.name.replace(".json", "?"))
    assert actual is False


# @pytest.mark.skip()
def test_import_data(create_path):
    actual = import_data()
    expected = "intro"
    assert actual.location == "intro"


# @pytest.mark.skip()
def test_create_menu_objects(create_path):
    with create_path.open("r") as file:
        data = json.load(file)
        intro_location = create_menu_objects(data)
    assert intro_location.location == "intro"
    main_location = intro_location.locations.get("main", False)
    assert main_location.location == "main"
    quitting_location = main_location.locations.get("quitting", False)
    assert quitting_location.location == "quitting"

###################################################################################
# location_classes.py
def compare_output_and_expected(captured_output, lines):
    captured_output = captured_output.split("\n")

    for actual_line, expected_line in zip(captured_output, lines):
        assert actual_line.strip() == expected_line.strip()

######################################################################################
# fixtures

@pytest.fixture
def create_path():
    path = Path.cwd().joinpath("resources", "text", "location_objects.json")
    return path


def get_inputs(lines):
    elements = []
    for line in lines:
        if ":" in line:
            index = line.find(":")+1
            element = line[index:].strip()
            element = element
            elements.append(element)
    return elements


@pytest.mark.parametrize(
    "test_input",
    [
        "quitting.txt",
        "main-quitting.txt",
        "create-quitting.txt",
    ],
)
def test_all(monkeypatch, capsys, test_input):
    path = Path.cwd().joinpath("tests", "sims", test_input)
    with path.open("r") as file:
        lines = file.readlines()
        inputs = get_inputs(lines)

    def mock_input(prompt, choices=None, show_choices=None):
        response = inputs.pop(0)
        print(prompt, response, sep=": ")
        return response

    monkeypatch.setattr("rich.prompt.Prompt.ask", mock_input)

    main()

    captured_output = capsys.readouterr().out
    compare_output_and_expected(captured_output, lines)
