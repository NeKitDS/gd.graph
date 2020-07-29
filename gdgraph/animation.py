from typing import Iterable, Sequence, TypeVar

import manimlib.imports as manim
import numpy as np

N = TypeVar("N", float, int)
Point = Sequence[N]


def create_lines(points: Iterable[Point], **kwargs) -> Sequence[manim.Line]:
    lines = []

    previous_point = None

    for point in points:  # create lines from points
        if previous_point is not None:
            lines.append(manim.Line(previous_point, point, **kwargs))

        previous_point = point

    return lines


class Introduction(manim.Scene):
    def construct(self) -> None:
        text = manim.TextMobject(
            "What if we plotted ", "graphs ", "in ", "Geometry Dash", "?"
        )
        text.set_color_by_tex_to_color_map(
            {"graphs": manim.RED, "Geometry Dash": manim.BLUE}
        )

        other_text = manim.TextMobject("Let's do just that!", color=manim.GREEN)

        self.play(manim.Write(text))

        self.wait()

        self.play(manim.Transform(text, other_text))

        self.wait()


class LinearInterpolation(manim.GraphScene):
    CONFIG = {
        "x_min": -10,
        "x_max": 10,
        "y_min": -2,
        "y_max": 2,
        "function_color": manim.BLUE,
        "graph_origin": manim.ORIGIN,
        "axes_color": manim.WHITE,
        "graph_function": np.sin,
        "graph_name": "\\sin(x)",
        "step_to_color": {
            1.4: manim.DARK_BROWN,
            1.0: manim.RED,
            0.8: manim.ORANGE,
            0.5: manim.YELLOW,
            0.2: manim.GREEN,
            0.1: manim.PURPLE,
        }
    }

    def construct(self) -> None:
        text = manim.TextMobject("Linear Interpolation")
        text.shift(manim.UP * 3 + manim.LEFT * 4)

        self.play(manim.Write(text))

        self.setup_axes(animate=True)

        sine_graph = self.get_graph(self.graph_function, self.function_color)

        sine_label = self.get_graph_label(sine_graph, label=self.graph_name)

        self.play(manim.ShowCreation(sine_graph), manim.ShowCreation(sine_label))

        self.wait()

        for step, color in self.step_to_color.items():
            points = [  # calculate points on the graph
                self.coords_to_point(n, self.graph_function(n))
                for n in np.arange(self.x_min, self.x_max + step, step)
            ]

            lines = manim.VGroup(*create_lines(points, color=color))

            step_text = manim.TextMobject(f"step = {step}", color=color)
            n_text = manim.TextMobject(f"n = {len(points) - 1}", color=color)

            step_text.shift((manim.UP + manim.RIGHT) * 3)
            n_text.next_to(step_text, manim.DOWN)

            self.add(step_text, n_text)
            self.add(lines)

            self.wait()

            self.remove(lines)
            self.remove(step_text, n_text)

        self.wait()


class RamerDouglasPeucker(manim.GraphScene):
    CONFIG = {
        "points": (
            (1, 5), (2, 2), (3, 1), (4, 2), (5, 1), (6, 3), (7, 4), (8, 2), (9, 5)
        ),
        "lines_color": manim.RED,
        "point_color": manim.BLUE,
        "max_point_color": manim.GREEN,
        "axes_color": manim.WHITE,
        "better_path_color": manim.PURPLE,
        "epsilon": 1,
    }

    def construct(self) -> None:
        self.setup_axes(animate=True)

        points = [self.coords_to_point(x, y) for x, y in self.points]

        dots = manim.VGroup(*(
            manim.Dot(point, color=self.lines_color) for point in points
        ))

        lines = manim.VGroup(*create_lines(points, color=self.lines_color))

        self.play(manim.ShowCreation(dots))
        self.play(manim.ShowCreation(lines))

        self.ramer_douglas_peucker(points, epsilon=self.epsilon)

        self.wait()

    def ramer_douglas_peucker(self, points: Sequence[Point], epsilon: N) -> Sequence[Point]:
        max_distance = 0
        max_index = 0
        max_point = None

        first, last = points[0], points[-1]
        first_dot = manim.Dot(first, color=self.point_color)
        last_dot = manim.Dot(last, color=self.point_color)

        line = manim.Line(first, last, color=self.point_color)

        # epsilon_rectangle = manim.Rectangle(width=line.get_width(), height=epsilon)
        # epsilon_rectangle.move_to(line)

        self.add(first_dot, last_dot, line)

        for index, point in enumerate(points):
            distance = np.linalg.norm(
                np.cross(last - first, point - first)
            ) / np.linalg.norm(last - first)

            if distance > max_distance:
                max_distance = distance
                max_index = index
                max_point = point

        if max_point is not None:
            dot = manim.Dot(max_point, color=self.max_point_color)

            self.add(dot)

        self.wait(0.5)

        if max_point is not None:
            self.remove(dot)

        if max_distance > epsilon:
            self.remove(first_dot, last_dot, line)

            recurse_left = self.ramer_douglas_peucker(points[: max_index + 1], epsilon)
            recurse_right = self.ramer_douglas_peucker(points[max_index:], epsilon)

            return recurse_left[:-1] + recurse_right

        else:
            for mobject in (first_dot, last_dot, line):
                mobject.set_color(self.better_path_color)

            return [first, last]


class PerpendicularLine(manim.Scene):
    CONFIG = {
        "line": ((-2.0, -3.0), (3.0, 2.0)),
        "point": (-1.0, 3.0),
        "text_shift": (-4, 0, 0),
        "formula_color": manim.GREEN,
        "line_color": manim.RED,
        "point_color": manim.BLUE,
    }

    def construct(self) -> None:
        x0, y0 = self.point
        (x1, y1), (x2, y2) = self.line

        dx, dy = x2 - x1, y2 - y1
        length = np.sqrt(dx * dx + dy * dy)
        dx /= length
        dy /= length

        translate = (dx * (x0 - x1)) + (dy * (y0 - y1))
        vx, vy = (dx * translate) + x1, (dy * translate) + y1

        p0, p1, p2, pv = (
            np.array((x0, y0, 0)),
            np.array((x1, y1, 0)),
            np.array((x2, y2, 0)),
            np.array((vx, vy, 0)),
        )

        line = manim.Line(p1, p2, color=self.line_color)
        dots = manim.VGroup(
            manim.Dot(p1, color=self.line_color), manim.Dot(p2, color=self.line_color)
        )

        dot, vdot = manim.Dot(p0, color=self.point_color), manim.Dot(pv, color=self.point_color)
        perpendicular_line = manim.Line(p0, pv, color=self.point_color)

        self.play(manim.ShowCreation(dots))
        self.play(manim.ShowCreation(line))
        self.play(manim.ShowCreation(dot))
        self.play(manim.ShowCreation(perpendicular_line), manim.ShowCreation(vdot))

        line_tex = manim.TexMobject("ax + by + c = 0", color=self.line_color)
        line_tex.next_to(perpendicular_line, manim.DOWN + manim.RIGHT)

        point_tex = manim.TexMobject("(m, n)", color=self.point_color)
        point_tex.next_to(dot)

        length_tex = manim.TexMobject("l", color=self.point_color)
        length_tex.next_to(perpendicular_line, manim.LEFT)

        length_formula = manim.TexMobject(
            "l = \\frac{|am + bn + c|}{\\sqrt{a^2 + b^2}}", color=self.formula_color
        )
        length_formula.shift(self.text_shift)

        self.play(manim.Write(line_tex), manim.Write(point_tex), manim.Write(length_tex))
        self.play(manim.Write(length_formula))

        self.wait()
