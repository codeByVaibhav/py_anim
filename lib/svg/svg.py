from lib.scene_obj.scene_obj import *
from lib.svg.parser import *


class Svg(SceneObj):
    def __init__(self, svg_file, **kwargs):
        super().__init__(**kwargs)
        parsed_svg = Parser(svg_file)
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