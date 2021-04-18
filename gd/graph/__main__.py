import math
import time

from operator import attrgetter as get_attr_factory

from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
)

import click
import import_expression  # type: ignore

import gd
import gd.api

from gd.graph.utils import (
    Line,
    Point,
    douglas_peucker,
    generate_coordinates,
    number_range,
)

# THESE CAN BE CHANGED
BACKGROUND_COLOR = 0x252525
GROUND_COLOR = 0x000000
GROUND_2_COLOR = 0x000000
BACKGROUND_ID = 13  # empty background

# DO NOT CHANGE THESE
GRID_UNITS = 30
LINE_OBJECT_ID = 579
LINE_OBJECT_SCALE = 0.5 * 0.1
LINE_OBJECT_LENGTH = GRID_UNITS * LINE_OBJECT_SCALE
HALF_LINE_OBJECT_LENGTH = LINE_OBJECT_LENGTH / 2
POINT_OBJECT_ID = 1764
POINT_OBJECT_SCALE = 0.65 * 0.1
POINT_OBJECT_DIAMETER = GRID_UNITS * POINT_OBJECT_SCALE * 0.25
ORIGIN_SCALE = 0.5
SETUP = "from math import *"

# THESE CAN ALSO BE CHANGED
DEFAULT_COLOR = "0xFFFFFF"
DEFAULT_VARIABLE = "x"
DEFAULT_FUNCTION = f"{DEFAULT_VARIABLE}"  # identity function
DEFAULT_START = -5
DEFAULT_STOP = 5
DEFAULT_STEP = 0.001
DEFAULT_EPSILON = 0.01
DEFAULT_SCALE = GRID_UNITS
DEFAULT_ROUNDING = 15
DEFAULT_Y_LIMIT = 90

get_x = get_attr_factory("x")
T = TypeVar("T")


def wrap_failsafe(function: Callable[..., T]) -> Callable[..., Optional[T]]:
    def inner(*args: Any, **kwargs: Any) -> Optional[T]:
        try:
            return function(*args, **kwargs)

        except Exception:  # noqa
            return None

    return inner


def prepare_database_and_levels() -> Tuple[
    gd.api.Database, gd.api.LevelCollection
]:
    database = gd.api.save.load()
    levels = database.get_created_levels()

    return database, levels


def add_colors_and_background(
    editor: gd.api.Editor, color_id: int, color: int
) -> None:
    colors = editor.get_colors()

    colors.get("BG").set_color(BACKGROUND_COLOR)
    colors.get("G").set_color(GROUND_COLOR)
    colors.get("G2").set_color(GROUND_2_COLOR)

    colors.add(gd.api.ColorChannel(id=color_id).set_color(color))

    editor.get_header().background = BACKGROUND_ID


def prepare_level_and_editor(
    level_name: str,
) -> Tuple[gd.api.LevelAPI, gd.api.Editor]:
    level = gd.api.LevelAPI(
        name=level_name, level_type=gd.api.LevelType.EDITOR
    )
    editor = level.open_editor()

    return level, editor


def dump_entities(
    database: gd.api.Database,
    levels: gd.api.LevelCollection,
    level: gd.api.LevelAPI,
    editor: gd.api.Editor,
    position: int = 0,
) -> None:
    editor.to_callback()
    levels.insert(position, level)
    levels.dump()
    database.dump()


def generate_objects(
    points: Sequence[Point], color_id: int, skip: Iterable[float]
) -> Iterator[gd.api.Object]:
    previous_point: Optional[Point] = None

    for point in points:
        x, y = point

        yield gd.api.Object(
            id=POINT_OBJECT_ID,
            x=x,
            y=y,
            color_1_id=color_id,
            color_2_id=color_id,
            scale=POINT_OBJECT_SCALE,
        )

        if previous_point is not None:
            line: Line = (previous_point, point)

            (x1, y1), (x2, y2) = line
            a, b = y1 - y2, x2 - x1

            length = math.sqrt(a * a + b * b)

            if length > POINT_OBJECT_DIAMETER and not any(
                x1 < skip_x < x2 for skip_x in skip
            ):
                rotation = math.degrees(math.atan(a / b))

                dx, dy = (x2 - x1) / length, (y2 - y1) / length

                for line_object_distance in number_range(
                    HALF_LINE_OBJECT_LENGTH,
                    length - HALF_LINE_OBJECT_LENGTH,
                    LINE_OBJECT_LENGTH,
                ):
                    x, y = (
                        x1 + line_object_distance * dx,
                        y1 + line_object_distance * dy,
                    )

                    yield gd.api.Object(
                        id=LINE_OBJECT_ID,
                        x=x,
                        y=y,
                        color_1_id=color_id,
                        color_2_id=color_id,
                        rotation=rotation,
                        scale=LINE_OBJECT_SCALE,
                    )

        previous_point = point


@click.command()
@click.option(
    "--color",
    "-c",
    default=DEFAULT_COLOR,
    help="Color to use, written in hex format.",
)
@click.option(
    "--variable",
    "-var",
    "-v",
    default=DEFAULT_VARIABLE,
    help=(
        f"Variable name to use, which should be valid as an identifier. "
        f"Default is {DEFAULT_VARIABLE}."
    ),
)
@click.option(
    "--function",
    "-func",
    "-f",
    default=DEFAULT_FUNCTION,
    help="Mathematical function to graph, like sin(x).",
)
@click.option(
    "--level-name",
    "-name",
    "-l",
    prompt="Level name",
    help="Name of the level to save graph to.",
)
@click.option(
    "--start",
    default=DEFAULT_START,
    type=float,
    help="Value of the argument to start plotting from.",
)
@click.option(
    "--stop",
    default=DEFAULT_STOP,
    type=float,
    help="Value of the argument to stop plotting at.",
)
@click.option(
    "--step",
    default=DEFAULT_STEP,
    type=float,
    help="Value of the step to add to the argument.",
)
@click.option(
    "--y-limit",
    "-y",
    default=DEFAULT_Y_LIMIT,
    type=float,
    help="Limit of absolute y value of any point.",
)
@click.option(
    "--epsilon",
    "-e",
    default=DEFAULT_EPSILON,
    type=float,
    help=(
        "Epsilon to use for decimating function a curve "
        "to a similar curve with fewer points."
    ),
)
@click.option(
    "--scale",
    "-s",
    default=DEFAULT_SCALE,
    type=float,
    help="Scale constant used to enlarge the graph.",
)
@click.option(
    "--rounding",
    "-r",
    default=DEFAULT_ROUNDING,
    type=int,
    help="Number of decimal places to round each argument to.",
)
@click.option(
    "--inclusive",
    "-i",
    is_flag=True,
    type=bool,
    help="Whether last argument in given range should be included.",
)
def main(
    color: str,
    variable: str,
    function: str,
    level_name: str,
    start: float,
    stop: float,
    step: float,
    y_limit: float,
    epsilon: float,
    scale: float,
    rounding: int,
    inclusive: bool,
) -> None:
    time_start = time.perf_counter()

    print("Processing...")

    try:
        color_value = int(color.replace("#", "0x"), 16)

    except ValueError:
        return click.echo(f"Can not parse color: {color!r}.")

    print("Parsing and compiling function...")

    try:
        environment: Dict[str, Any] = {}

        exec(SETUP, environment)

        function_to_call = import_expression.eval(
            f"lambda {variable}: {function}", environment
        )

    except SyntaxError:
        return click.echo(f"Can not parse function: {function!r}.")

    y_limit *= GRID_UNITS

    print("Preparing database and levels...")

    database, levels = prepare_database_and_levels()

    print("Preparing the level and the editor...")

    level, editor = prepare_level_and_editor(level_name)

    color_id = editor.get_free_color_id()

    if color_id is None:
        print("Can not find free color ID to use.")

        exit(1)

    print(f"Free color ID: {color_id}.")

    origin = gd.api.Object(
        id=POINT_OBJECT_ID,
        x=0,
        y=0,
        color_1_id=color_id,
        color_2_id=color_id,
        scale=ORIGIN_SCALE,
    )

    editor.add_objects(origin)

    add_colors_and_background(editor, color_id, color_value)

    point_iterator = generate_coordinates(
        number_range(
            start, stop, step, inclusive=inclusive, rounding=rounding
        ),
        wrap_failsafe(function_to_call),
        scale,
    )

    print("Generating points...")

    points = [(x, y) for (x, y) in point_iterator if abs(y) < y_limit]

    print("Generating points to be skipped...")

    skip = {
        n * scale
        for n in number_range(
            start, stop, step, inclusive=inclusive, rounding=rounding
        )
    }.difference(x for x, y in points)

    print("Applying Ramer-Douglas-Peucker (RDP) algorithm...")

    actual_points = douglas_peucker(points, epsilon)

    print("Generating objects...")

    editor.objects.extend(generate_objects(actual_points, color_id, skip))

    print("Shifting objects to the right...")

    lowest_x = abs(min(map(get_x, editor.get_objects()), default=0.0))

    for gd_object in editor.get_objects():
        gd_object.move(x=lowest_x)

    print("Saving...")

    dump_entities(database, levels, level, editor)

    time_stop = time.perf_counter()

    time_spent = time_stop - time_start

    if time_spent > 1:
        time_spent = round(time_spent, 2)
        time_string = f"{time_spent}s"

    else:
        time_spent = round(time_spent * 1000, 2)
        time_string = f"{time_spent}ms"

    print(
        f"Done. Objects used: {len(editor.get_objects())}. "
        f"Time spent: {time_string}."
    )


if __name__ == "__main__":
    main()
