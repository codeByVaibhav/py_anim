from copy import deepcopy

from lib.material.color import *
from lib.math.interpolation import lerp
from lib.math.vector import *


class Material(object):
    def __init__(
            self,
            fill: np.ndarray = DARK_BLUE,
            stroke: np.ndarray = DARK_BLUE,
            stroke_width: float = 2,
            stroke_dasharray: np.ndarray = VEC2_ZERO,
            fill_opacity: float = 0.4,
            stroke_opacity: float = 1.0
    ):
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.stroke_dasharray = stroke_dasharray
        self.fill_opacity = fill_opacity
        self.stroke_opacity = stroke_opacity

    def __str__(self):
        mat_str = f'stroke="rgb({self.stroke[0]}, {self.stroke[1]}, {self.stroke[2]})" '
        mat_str += f'fill="rgb({self.fill[0]}, {self.fill[1]}, {self.fill[2]})" '
        mat_str += f'fill-opacity="{self.fill_opacity}" '
        mat_str += f'stroke-opacity="{self.stroke_opacity}" '
        mat_str += f'stroke-width="{self.stroke_width}" '
        mat_str += f'stroke-dasharray="{str(self.stroke_dasharray)[1:-1]}"' if self.stroke_dasharray.all() != VEC2_ZERO.all() else ''
        return mat_str

    def __eq__(self, o):
        return self.__dict__ == o.__dict__

    def __ne__(self, o):
        return not self == o

    def copy(self):
        return deepcopy(self)

    def lerp(self, o, percentage):
        if percentage <= 0:
            return self.copy()
        elif percentage >= 1:
            return o.copy()
        else:
            fill = lerp(self.fill, o.fill, percentage)
            stroke = lerp(self.stroke, o.stroke, percentage)
            stroke_dasharray = lerp(self.stroke_dasharray, o.stroke_dasharray, percentage)

            fill_opacity = lerp(self.fill_opacity, o.fill_opacity, percentage)
            stroke_opacity = lerp(self.stroke_opacity, o.stroke_opacity, percentage)
            stroke_width = lerp(self.stroke_width, o.stroke_width, percentage)

        return Material(
            fill=fill,
            fill_opacity=fill_opacity,
            stroke=stroke,
            stroke_opacity=stroke_opacity,
            stroke_dasharray=stroke_dasharray,
            stroke_width=stroke_width
        )


DEFAUT_MAT = Material()
