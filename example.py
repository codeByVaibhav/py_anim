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
        self.camera.pos = vector(0, 0, 4)

        # text = TexEquation(
        #     r'Integral $\int_{a}^{b} x^2 \,dx$ inside text',
        #     mat=Material(stroke=DARK_BLUE, stroke_width=2, fill_opacity=1.0, fill=DARK_BLUE),
        # )
        cube = Cuboid(1, 1, 1, mat=Material(
            stroke=DARK_BLUE, stroke_width=8))

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
            r'\zeta(s)=\int_1^\infty\sum_{n=1}^\infty e^{-\pi n^2x}(x^{s/2}+x^{(1-s)/2})\frac{dx}{x}-\frac{1}{s}-\frac{1}{1-s}',
            mat=Material(stroke=DARK_BLUE, fill_opacity=1, fill=DARK_BLUE),
            scale=VEC3_NSCALE*0.04
        )
        github = TexText('Github',
                         mat=Material(stroke=GREY_BROWN, fill_opacity=1, fill=GREY_BROWN),
                         # pos=VEC3_DOWN * 2
                         scale=VEC3_NSCALE * 0.1
                         )
        svg_f = Svg('elephant.svg',
                    mat=Material(stroke=DARK_BLUE, fill_opacity=1, fill=DARK_BLUE),
                    scale=VEC3_NSCALE * 0.01
                    )
        self.render(
            ShowCreation(github, speed=0.05),
            # Translate(github, VEC3_DOWN * 2),
            # MorphShape(svg_f, eq)
            # RotateFrame(
            #     VEC3_Y_AXIS, 360,
            #     self.get_objs_frame(svg_f),
            #     speed=0.01
            # ),
        )
        self.add_objs_to_background(github)
        # self.render(ShowCreation(svg_f))
        # self.add_objs_to_background(svg_f)
        self.pause(0.8)
        # self.add_objs_to_background(svg_f)
        # self.render(
        #     Translate(github, VEC3_DOWN * 1.5),
        # )
        # self.clear_background()
        # self.add_objs_to_background(github)
        #
        # self.render(
        #     RotateFrame(
        #         VEC3_Y_AXIS, 360,
        #         self.get_objs_frame(svg_f),
        #         speed=0.01
        #     ),
        # )
        #
        # self.add_objs_to_background(svg_f)
        #
        # self.pause(time=1.0)

        # self.render(
        #     ShowCreation(cube),
        #     # Translate(intro_eq, VEC3_UP * 2),
        #     RotateFrame(
        #         VEC3_Y_AXIS, 360,
        #         self.get_objs_frame(cube),
        #         speed=0.1
        #     ),
        # )

        # self.render(
        #     MorphShape(support_latex, eq, speed=0.01),
        # )
        #
        # self.add_objs_to_background(eq)
        #
        # self.render(
        #     Translate(intro_eq, VEC3_UP * 2),
        # )
        #
        # self.add_objs_to_background(intro_eq)
        # self.pause(1)
        #
        # self.clear_background()
        # self.add_objs_to_background(eq)
        # self.render(
        #     VanishFrame(self.get_objs_frame(intro_eq))
        # )
        #
        # self.clear_background()
        #
        # grid = NumberPlane(
        #     -7, 7, -5, 5,
        #     mat=Material(stroke=DARK_BLUE)
        # )
        #
        # circle = Circle(mat=Material(stroke=ORANGE, stroke_width=8))
        # square = Rectangle(mat=Material(stroke=RED_D, stroke_width=8))
        # line = Line(
        #     start=VEC3_LEFT * 10, end=VEC3_RIGHT * 10,
        #     mat=Material(stroke=PURPLE_A, stroke_width=8)
        # )
        #
        # self.render(
        #     MorphShape(eq, grid),
        # )
        #
        # self.add_objs_to_background(grid)
        #
        # self.clear_background()
        #
        # self.render(
        #     MorphShape(grid, circle, speed=0.005),
        #     MorphShape(circle, square),
        #     MorphShape(square, line)
        # )
        # self.add_objs_to_background(line)
        #
        # self.pause(0.5)


if __name__ == "__main__":
    StartScene()
