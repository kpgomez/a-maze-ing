from rich.console import Console
from scripts.location_functions import sleep, import_data

# global
console = Console()


def main() -> None:
    location = import_data()
    # console.print(location, style="bold green")
    # location = location.transfer_maze_and_or_solution(location.locations.get("main"))

    while True:
        print("")
        if location.location == "good_bye":
            print("\n" * 70)
            location.action()
            break
        print("\n"*70)
        location = location.action()
        sleep(5)


if __name__ == "__main__":
    main()
