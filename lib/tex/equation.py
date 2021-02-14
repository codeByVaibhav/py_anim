from lib.math.interpolation import lerp
from lib.scene_obj.scene_obj import *
from lib.tex.svg_parser import *
from lib.tex.tex_to_svg import tex_to_svg_file
from lib.svg.svg import Parser


class TexEquation(SceneObj):
    def __init__(self, equation, **kwargs):
        super().__init__(**kwargs)
        equation = f'\\[ {equation} \\]'
        self.svg_file = tex_to_svg_file(equation)
        parsed_svg = Parser(self.svg_file)
        self.paths = parsed_svg.paths
        self.width = parsed_svg.width
        self.height = parsed_svg.height

    def get_mat_and_paths(self):
        return (
            self.mat,
            [
                [(self.rot.rotate(p) + self.pos) * self.scale for p in path] for path in self.paths
            ]
        )
