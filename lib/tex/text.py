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

    def get_mat_and_paths(self):
        return (
            self.mat,
            [
                [(self.rot.rotate(p) + self.pos) * self.scale for p in path] for path in self.paths
            ]
        )
