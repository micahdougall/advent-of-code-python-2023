import functools
from importlib import import_module
import logging
import os


logging.basicConfig(level=logging.INFO)
RESOURCES = "res"


def run(
    day: str,
    part: str,
    runtime: str,
    debug: bool,
):
    part_one = getattr(import_module(f"days.day_{day}"), "part_one")
    part_two = getattr(import_module(f"days.day_{day}"), "part_two")
    parts = (
        [part_one] if part == "one"
        else [part_two] if part == "two"
        else [part_one, part_two]
    )
    day_module = import_module(f"days.day_{day}", package=None)

    if debug:
        logging.getLogger().setLevel(logging.DEBUG)

    def decorator_test(func: callable):
        @functools.wraps(func)
        def wrapper_run():
            print(f"Running {day_module.__name__}...")
            results = func(parts)
            if not part:
                print(f"Part one: {results[0]}")
                print(f"Part two: {results[1]}")
            else:
                print(f"Part {part}: {results[0]}")
        return wrapper_run
    return decorator_test


@run(
    day=os.environ.get("DAY", "three"),
    part=os.environ.get("PART", "one"),
    runtime=os.environ.get("RUNTIME", "test"),
    debug=os.environ.get("DEBUG", False),
)
def run_day(funcs: list[callable]) -> any:
    return [func() for func in funcs]
