import concurrent.futures
from lib.scene.scene import *
from lib.math.vector import *
from lib.material.color import *
from lib.geometry.shapes import *
from lib.animation.animation import *
from lib.tex.equation import *
from lib.tex.text import *
import mpmath


def complex_func(vec, inp=2):
    comp = complex(vec.x(), vec.y())**inp
    return vector(comp.real, comp.imag, 0)


class StartScene(Scene):
    def __init__(self, width=1920, height=1080, fps=60):
        super().__init__(width=width, height=height, fps=fps)

    def begin(self):
        self.camera.pos = vector(0, 0, 4)

        # text = TexText('Hello World', mat=Material(
        #     stroke=DARK_BLUE, stroke_width=4))
        cube = Cuboid(1, 1, 1, mat=Material(
            stroke=DARK_BLUE, stroke_width=8))
        circle = Circle(mat=Material(stroke=ORANGE, stroke_width=8))
        square = Rectangle(mat=Material(stroke=RED_D, stroke_width=8))
        line = Line(start=VEC3_LEFT*10, end=VEC3_RIGHT*10,
                    mat=Material(stroke=PURPLE_A, stroke_width=8))

        self.render(
            ShowCreation(cube),
            RotateFrame(
                VEC3_X_AXIS + VEC3_Z_AXIS, 360,
                self.get_objs_frame(cube),
                speed=0.05
            ),
        )

        self.add_objs_to_background(cube)

        self.pause(0.2)
        self.background_frame = []

        self.render(
            MorphShape(cube, circle),
            MorphShape(circle, square),
            MorphShape(square, line)
        )


if __name__ == "__main__":
    s = StartScene()
