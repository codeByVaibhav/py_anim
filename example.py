from lib.animation.animation import *
from lib.geometry.shapes import *
from lib.scene.scene import *
from lib.tex.text import *
from lib.tex.equation import *
import math
from lib.svg.svg import Svg


class StartScene(Scene):
    def __init__(self, width=1920, height=1080, fps=60):
        super().__init__(width=width, height=height, fps=fps)

    def begin(self):
        # cube = Cuboid(1, 1, 1, mat=Material(
        #     stroke=DARK_BLUE, stroke_width=8))
        # eq = TexEquation(
        #     r'\zeta(s)=\int_1^\infty\sum_{n=1}^\infty e^{-\pi n^2x}(x^{s/2}+x^{(1-s)/2})\frac{dx}{x}-\frac{1}{'
        #     r's}-\frac{1}{1-s}',
        #     mat=Material(stroke=DARK_BLUE, fill_opacity=0.3, fill=DARK_BLUE),
        #     scale=VEC3_NSCALE * 0.04
        # )
        india = TexText('This is India',
                        mat=Material(stroke=GREY_BROWN, fill_opacity=1, fill=GREY_BROWN),
                        # pos=VEC3_DOWN * 2
                        scale=VEC3_NSCALE * 0.1
                        )

        self.render(
            ShowShape(india),
            RotateShape(
                VEC3_Y_AXIS, 360,
                india,
                speed=0.01
            )
            # MorphShape(india_map, india, speed=0.02),
            # RotateShape(
            #     VEC3_Y_AXIS, 360,
            #     pac,
            #     speed=0.01
            # ),
            # MorphShape(pac, spek),
            # RotateShape(
            #     VEC3_Y_AXIS, 360,
            #     spek,
            #     speed=0.01
            # ),
            # Translate(github, VEC3_DOWN * 2),
        )
        self.add_objs_to_background(india)
        self.pause(0.2)


if __name__ == "__main__":
    StartScene()
