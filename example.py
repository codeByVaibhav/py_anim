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
        self.camera.pos = vector(0, 0, 8)

        text = TexText('Hello World', mat=Material(
            stroke=DARK_BLUE, stroke_width=4))
        sphere = Cuboid(1, 1, 1)

        self.render(
            ShowCreation(text),
            MorphShape(text, sphere),
            RotateFrame(
                VEC3_X_AXIS + VEC3_Z_AXIS, 360,
                self.get_objs_frame(sphere),
                speed=0.008
            ),
        )

        self.add_objs_to_background(sphere)

        self.pause(0.3)


if __name__ == "__main__":
    s = StartScene()
