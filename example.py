from lib.animation.animation import *
from lib.geometry.shapes import *
from lib.scene.scene import *
from lib.tex.text import *
from lib.tex.equation import *
import math
from lib.svg.svg import Svg


# import mpmath


def complex_func(vec, inp=2):
    comp = complex(vec[0], vec[1]) ** inp
    return vector(comp.real, comp.imag, 0)


def my_sin(p, inp=None):
    return vector(p[0], math.sin(p[0]), p[2])


class StartScene(Scene):
    def __init__(self, width=1920, height=1080, fps=60):
        super().__init__(width=width, height=height, fps=fps)

    def begin(self):
        # cube = Cuboid(1, 1, 1, mat=Material(
        #     stroke=DARK_BLUE, stroke_width=8))

        # support_latex = TexText(
        #     r'py anim supports \LaTeX{}',
        #     mat=Material(stroke=DARK_BLUE)
        # )
        #
        # intro_eq = TexText(
        #     r'This is a Equation',
        #     mat=Material(stroke=DARK_BLUE),
        #     pos=VEC3_UP * 4
        # )
        #
        eq = TexEquation(
            r'\zeta(s)=\int_1^\infty\sum_{n=1}^\infty e^{-\pi n^2x}(x^{s/2}+x^{(1-s)/2})\frac{dx}{x}-\frac{1}{'
            r's}-\frac{1}{1-s}',
            mat=Material(stroke=DARK_BLUE, fill_opacity=0.3, fill=DARK_BLUE),
            scale=VEC3_NSCALE * 0.04
        )
        github = TexText('Github',
                         mat=Material(stroke=GREY_BROWN, fill_opacity=1, fill=GREY_BROWN),
                         # pos=VEC3_DOWN * 2
                         scale=VEC3_NSCALE * 0.1
                         )
        svg_f = Svg('test.svg',
                    mat=Material(stroke=DARK_BLUE, fill_opacity=0.3, fill=DARK_BLUE),
                    scale=VEC3_NSCALE * 0.01
                    )
        self.render(
            ShowCreation(svg_f, speed=0.01),
            MorphShape(svg_f, eq, speed=0.04)
            # Translate(github, VEC3_DOWN * 2),
            # MorphShape(eq, svg_f)
            # RotateFrame(
            #     VEC3_Y_AXIS, 360,
            #     self.get_objs_frame(svg_f),
            #     speed=0.01
            # ),
        )
        self.add_objs_to_background(eq)
        self.pause(0.5)
        # self.render(ShowCreation(svg_f))
        # self.add_objs_to_background(svg_f)
        # self.pause(0.2)
        # self.add_objs_to_background(svg_f)
        # self.render(
        #     Translate(github, VEC3_DOWN * 1.5),
        # )


if __name__ == "__main__":
    StartScene()
