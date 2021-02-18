from lib.scene_obj.scene_obj import *
from lib.tex.tex_to_svg import tex_to_svg_file
from lib.svg.parser import Parser


class TexText(SceneObj):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.svg_file = tex_to_svg_file(text)
        parsed_svg = Parser(self.svg_file)
        self.paths = parsed_svg.paths
        self.width = parsed_svg.width
        self.height = parsed_svg.height

    def apply_transform(self, point):
        return (self.rot.rotate(point) + self.pos) * self.scale

    def get_mat_and_paths(self):
        return [
            path_obj.apply_func(self.apply_transform) for path_obj in self.paths
        ]
