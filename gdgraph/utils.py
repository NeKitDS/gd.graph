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

__all__ = (
    "N",
    "Point",
    "Line",
    "number_range",
    "get_linear_formula",
    "perpendicular_distance",
    "douglas_peucker",
    "func_stub",
    "iter_coorinates",
)

N = TypeVar("N", float, int)
Point = Tuple[N, N]
Line = Tuple[Point, Point]


def number_range(
    start: N,
    stop: Optional[N] = None,
    step: N = 1,
    *,
    inclusive: bool = True,
    rounding: Optional[int] = 15,
) -> Generator[N, None, None]:
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


def get_linear_formula(line: Line) -> Tuple[N, N, N]:
    """For points (x1, y1) and (x2, y2) find line ax + by + c = 0,
    such that they belong to it.

    Returns coefficients a, b and c.
    """
    (x1, y1), (x2, y2) = line

    return y1 - y2, x2 - x1, x1 * y2 - x2 * y1


def perpendicular_distance(point: Point, line: Line) -> N:
    """Calculate perpendicular distance from (x0, y0) point
    to (ax + by + c = 0) line (determined by two points).
    This function uses formula: |ax0 + by0 + c|/sqrt(a^2 + b^2)
    """
    a, b, c = get_linear_formula(line)
    x, y = point

    return abs(a * x + b * y + c) / math.sqrt(a * a + b * b)


def douglas_peucker(
    point_array: Sequence[Point], epsilon: N = 0.01
) -> Sequence[Point]:
    """Apply Ramer-Douglas-Peucker algorithm in order to decimate a curve
    composed of line segments to a similar curve with fewer points.
    """
    max_distance = 0
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

        return recurse_left[:-1] + recurse_right

    else:
        return [first, last]


def func_stub(input_value: N) -> Optional[N]:
    ...


def iter_coorinates(
    values: Iterable[N],
    func: Callable[[N], Optional[N]],
    scale: N = 1,
    shift: bool = False,
) -> Generator[Point, None, None]:
    """Apply <func> for each value in <values>,
    multiplying input and output by <scale>.
    """
    for x in values:
        y = func(x)

        if y is not None:
            yield x * scale, y * scale
