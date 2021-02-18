from lib.scene_obj.scene_obj import *
from lib.svg.parser import *


class Svg(SceneObj):
    def __init__(self, svg_file, **kwargs):
        super().__init__(**kwargs)
        parsed_svg = Parser(svg_file)
        self.paths = parsed_svg.paths
        self.width = parsed_svg.width
        self.height = parsed_svg.height

    def apply_transform(self, point):
        return (self.rot.rotate(point) + self.pos) * self.scale

    def get_mat_and_paths(self):
        return [
            path_obj.apply_func(self.apply_transform) for path_obj in self.paths
        ]
