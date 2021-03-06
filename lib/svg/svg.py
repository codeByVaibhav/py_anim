from lib.tex.tex_to_svg import tex_to_svg_file
from lib.scene_obj.scene_obj import *
from lib.svg.parser import *

class Svg(SceneObj):
    def __init__(self, svg_file, **kwargs):
        super().__init__(**kwargs)
        parsed_svg = Parser(svg_file)
        self.paths = parsed_svg.paths
        self.top_left = parsed_svg.top_left
        self.bottom_right = parsed_svg.bottom_right
        self.width = self.bottom_right.x() - self.top_left.x()
        self.height = self.bottom_right.y() - self.top_left.y()
        self.mid = self.top_left.lerp(self.bottom_right, 0.5)

    def get_mat_and_paths(self):
        pos = self.pos - self.mid
        return (
            self.mat,
            [
                [ (self.rot.rotate(p) + pos) * self.scale for p in path ] for path in self.paths
            ]
        )

