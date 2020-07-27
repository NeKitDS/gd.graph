import math
from typing import (
    Callable,
    Generator,
    Iterable,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
)

import click
import gd
import import_expression

from gdgraph.utils import (
    Line,
    N,
    Point,
    douglas_peucker,
    iter_coorinates,
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
DEFAULT_FUNCTION = "x"
DEFAULT_START = -5
DEFAULT_STOP = 5
DEFAULT_STEP = 0.001
DEFAULT_EPSILON = 0.01
DEFAULT_SCALE = GRID_UNITS
DEFAULT_ROUNDING = 15
DEFAULT_Y_LIMIT = 90

T = TypeVar("T")


def wrap_failsafe(function: Callable[..., T]) -> Callable[..., Optional[T]]:
    def inner(*args, **kwargs) -> Optional[T]:
        try:
            return function(*args, **kwargs)
        except Exception:  # noqa
            return  # None

    return inner


def prepare_db_and_levels() -> Tuple[gd.api.Database, gd.api.LevelCollection]:
    db = gd.api.save.load()
    levels = db.load_my_levels()

    return db, levels


def add_colors_and_background(
    editor: gd.api.Editor, color_id: int, color: int
) -> None:
    background_color = gd.api.ColorChannel("BG").set_color(BACKGROUND_COLOR)
    ground_color = gd.api.ColorChannel("GRND").set_color(GROUND_COLOR)
    ground_2_color = gd.api.ColorChannel("GRND2").set_color(GROUND_2_COLOR)
    graph_color = gd.api.ColorChannel(id=color_id).set_color(color)

    editor.add_colors(
        background_color, ground_color, ground_2_color, graph_color
    )

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
    db: gd.api.Database,
    levels: gd.api.LevelCollection,
    level: gd.api.LevelAPI,
    editor: gd.api.Editor,
) -> None:
    editor.dump_back()
    levels.insert(0, level)
    levels.dump()
    db.dump()


def generate_objects(
    points: Sequence[Point], color_id: int, skip: Iterable[N]
) -> Generator[gd.api.Object, None, None]:
    previous_point: Optional[Point] = None

    for point in points:
        x, y = point

        yield gd.api.Object(
            id=POINT_OBJECT_ID,
            x=x,
            y=y,
            color_1=color_id,
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
                        color_1=color_id,
                        rotation=rotation,
                        scale=LINE_OBJECT_SCALE,
                    )

        previous_point = point


@click.command()
@click.option(
    "--color",
    "-color",
    "-c",
    default=DEFAULT_COLOR,
    help="Color to use, written in hex format.",
)
@click.option(
    "--func",
    "-func",
    "-f",
    default=DEFAULT_FUNCTION,
    help="Mathematical function to graph, like sin(x).",
)
@click.option(
    "--level-name",
    "-level-name",
    "-l",
    prompt="Level name",
    help="Name of the level to save graph to.",
)
@click.option(
    "--start",
    "-start",
    default=DEFAULT_START,
    type=float,
    help="Value of the argument to start plotting from.",
)
@click.option(
    "--stop",
    "-stop",
    default=DEFAULT_STOP,
    type=float,
    help="Value of the argument to stop plotting at.",
)
@click.option(
    "--step",
    "-step",
    default=DEFAULT_STEP,
    type=float,
    help="Value of the step to add to the argument.",
)
@click.option(
    "--y-limit",
    "-y-limit",
    "-y",
    default=DEFAULT_Y_LIMIT,
    type=float,
    help="Limit of absolute y value of any point.",
)
@click.option(
    "--epsilon",
    "-epsilon",
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
    "-scale",
    "-s",
    default=DEFAULT_SCALE,
    type=float,
    help="Scale constant used to enlarge the graph.",
)
@click.option(
    "--rounding",
    "-rounding",
    "-r",
    default=DEFAULT_ROUNDING,
    type=int,
    help="Number of decimal places to round each argument to.",
)
@click.option(
    "--inclusive",
    "-inclusive",
    "-i",
    is_flag=True,
    type=bool,
    help="Whether last argument in given range should be included.",
)
def gdgraph(
    color: str,
    func: str,
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
    try:
        color = int(color.replace("#", "0x"), 16)
    except ValueError:
        return click.echo(f"Can not parse color: {color!r}.")

    try:
        environment = {}
        exec(SETUP, environment)
        func = import_expression.eval(f"lambda x: {func}", environment)

    except SyntaxError:
        return click.echo(f"Can not parse function: {func!r}.")

    y_limit *= GRID_UNITS

    print("Preparing database and levels...")

    db, levels = prepare_db_and_levels()

    print("Preparing the level and the editor...")

    level, editor = prepare_level_and_editor(level_name)

    color_id = editor.get_free_color_id()

    print(f"Free color ID: {color_id}.")

    origin = gd.api.Object(
        id=POINT_OBJECT_ID, x=0, y=0, color_1=color_id, scale=ORIGIN_SCALE
    )

    editor.add_objects(origin)

    add_colors_and_background(editor, color_id, color)

    point_iterator = iter_coorinates(
        number_range(
            start, stop, step, inclusive=inclusive, rounding=rounding
        ),
        wrap_failsafe(func),
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

    points = douglas_peucker(points, epsilon)

    print("Generating objects...")

    editor.objects.extend(generate_objects(points, color_id, skip))

    print("Shifting objects to the right...")

    lowest_x = abs(
        min((gd_object.x for gd_object in editor.get_objects()), default=0)
    )

    for gd_object in editor.get_objects():
        gd_object.move(x=lowest_x)

    print("Saving...")

    dump_entities(db, levels, level, editor)

    print(f"Done. Objects used: {len(editor.get_objects())}.")


if __name__ == "__main__":
    gdgraph()
