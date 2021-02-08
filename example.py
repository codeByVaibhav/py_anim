from lib.animation.animation import *
from lib.geometry.shapes import *
from lib.scene.scene import *
from lib.tex.text import *


# import mpmath


def complex_func(vec, inp=2):
    comp = complex(vec.x(), vec.y()) ** inp
    return vector(comp.real, comp.imag, 0)


class StartScene(Scene):
    def __init__(self, width=1920, height=1080, fps=60):
        super().__init__(width=width, height=height, fps=fps)

    def begin(self):
        self.camera.pos = vector(0, 0, 4)

        # text = TexEquation(
        #     r'Integral $\int_{a}^{b} x^2 \,dx$ inside text',
        #     mat=Material(stroke=DARK_BLUE, stroke_width=2, fill_opacity=1.0, fill=DARK_BLUE),
        # )
        # cube = Cuboid(1, 1, 1, mat=Material(
        #     stroke=DARK_BLUE, stroke_width=8))

        grid = NumberPlane(
            -7, 7, -5, 5,
            mat=Material(stroke=DARK_BLUE)
        )

        circle = Circle(mat=Material(stroke=ORANGE, stroke_width=8))
        square = Rectangle(mat=Material(stroke=RED_D, stroke_width=8))
        line = Line(
            start=VEC3_LEFT * 10, end=VEC3_RIGHT * 10,
            mat=Material(stroke=PURPLE_A, stroke_width=8)
        )

        self.render(
            ShowCreation(grid),
            RotateFrame(
                VEC3_Y_AXIS, 360,
                self.get_objs_frame(grid),
                speed=0.01
            ),
        )

        self.add_objs_to_background(grid)

        self.pause(0.2)
        self.clear_background()

        self.render(
            MorphShape(grid, circle, speed=0.005),
            MorphShape(circle, square),
            MorphShape(square, line)
        )
        self.add_objs_to_background(line)

        self.pause(0.5)


if __name__ == "__main__":
    StartScene()
