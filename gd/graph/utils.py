from math import sqrt

from typing import (
    Callable,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Tuple,
)

__all__ = (
    "Point",
    "Line",
    "number_range",
    "get_linear_formula",
    "perpendicular_distance",
    "douglas_peucker",
    "function_signature",
    "generate_coordinates",
)

Point = Tuple[float, float]
Line = Tuple[Point, Point]


def number_range(
    start: float,
    stop: Optional[float] = None,
    step: float = 1,
    *,
    inclusive: bool = True,
    rounding: Optional[int] = 15,
) -> Iterator[float]:
    """Return a generator over numbers in range from <start> to <stop> with <step>,
    optionally including <stop> if <inclusive> is True.

    If <rounding> is not None, round(value, rounding)
    will be applied for each value.

    number_range(stop) -> generator
    number_range(start, stop) -> generator
    number_range(start, stop, step) -> generator
    """
    if stop is None:
        start, stop = 0, start

    value = start

    while value < stop:
        if rounding is not None:
            value = round(value, rounding)

        yield value

        value += step

    if inclusive:
        yield stop


def get_linear_formula(line: Line) -> Tuple[float, float, float]:
    """For points (x1, y1) and (x2, y2) find line ax + by + c = 0,
    such that they belong to it.

    Returns coefficients a, b and c.
    """
    (x1, y1), (x2, y2) = line

    return y1 - y2, x2 - x1, x1 * y2 - x2 * y1


def perpendicular_distance(point: Point, line: Line) -> float:
    """Calculate perpendicular distance from (x_0, y_0) point
    to (ax + by + c = 0) line (determined by two points).
    This function uses formula: |ax_0 + by_0 + c|/sqrt(a^2 + b^2)
    """
    a, b, c = get_linear_formula(line)
    x, y = point

    return abs(a * x + b * y + c) / sqrt(a * a + b * b)


def douglas_peucker(
    point_array: Sequence[Point], epsilon: float = 0.01
) -> List[Point]:
    """Apply Ramer-Douglas-Peucker algorithm in order to decimate a curve
    composed of line segments to a similar curve with fewer points.
    """
    max_distance = 0.0
    max_index = 0

    first, last = point_array[0], point_array[-1]

    for index, point in enumerate(point_array):
        distance = perpendicular_distance(point, (first, last))

        if distance > max_distance:
            max_distance = distance
            max_index = index

    if max_distance > epsilon:
        recurse_left = douglas_peucker(point_array[: max_index + 1], epsilon)
        recurse_right = douglas_peucker(point_array[max_index:], epsilon)

        return [*recurse_left[:-1], *recurse_right]

    else:
        return [first, last]


def function_signature(input_value: float) -> Optional[float]:
    ...


def generate_coordinates(
    values: Iterable[float],
    function: Callable[[float], Optional[float]],
    scale: float = 1,
) -> Iterator[Point]:
    """Apply <function> for each value in <values>,
    multiplying input and output by <scale>.
    """
    for x in values:
        y = function(x)

        if y is not None:
            yield x * scale, y * scale
