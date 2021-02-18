import re
from copy import deepcopy
from xml.dom import minidom

from svgpathtools import parse_path

from lib.geometry.curves import *
from lib.material.material import *


class Path:
    def __init__(self, cmd_point: list, mat: Material = DEFAUT_MAT):
        self.cmd_point: list = cmd_point
        self.mat = mat

    def __iter__(self):
        return self.path_generator()

    def path_generator(self):
        for cmd, p in self.cmd_point:
            yield cmd, p

    def __len__(self):
        return len(self.cmd_point)

    def __getitem__(self, index):
        return self.cmd_point[index]

    def __setitem__(self, index, value):
        self.cmd_point[index] = value

    def append(self, cmd_point):
        self.cmd_point.append(cmd_point)

    def extend(self, cmd_points):
        self.cmd_point.extend(cmd_points)

    def get_cmd(self, index):
        return self.cmd_point[index][0]

    def copy(self):
        return deepcopy(self)

    def get_path_of_size(self, s: int):
        return Path(
            self.cmd_point + [self.cmd_point[-1]] * (s - len(self.cmd_point)),
            mat=self.mat.copy()
        )

    def linspace(self, no_of_points=100):
        if len(self) == no_of_points:
            return Path(self.cmd_point[:], mat=self.mat.copy())

        new_path = Path(
            [self.lerp(1 / no_of_points * n, get_last_cp=True) for n in range(no_of_points + 1)],
            mat=self.mat.copy()
        )

        if new_path.cmd_point[0][0] == 'M':
            return new_path
        else:
            new_path.cmd_point[0] = ('M', new_path.cmd_point[0][1])
            return new_path

    def lerp(self, per, get_last_cp=False):
        """
        Returns a new Path object which has path only unto percentage given to function.
        """
        if per <= 0:
            if get_last_cp:
                return self.cmd_point[0]
            return Path([self.cmd_point[0]], mat=self.mat.copy())
        elif per >= 1:
            if get_last_cp:
                return self.cmd_point[-1]
            return Path(self.cmd_point[:], mat=self.mat.copy())

        per *= len(self) - 1

        last_point = int(per)
        new_per = per - last_point
        last_p = ('L', lerp(self.cmd_point[last_point][1], self.cmd_point[last_point + 1][1], new_per))

        if get_last_cp:
            return last_p

        return Path([*self.cmd_point[:last_point + 1], last_p], mat=self.mat.copy())

    def apply_func(self, func):
        return Path([(cmd, func(p)) for cmd, p in self], mat=self.mat.copy())

    def lerp_to_path(self, path, percentage: float):
        assert len(path) == len(self)
        new_cmd_path = []
        for (cmd, p), (cmd2, p2) in zip(self, path):
            if cmd == 'M' or cmd2 == 'M':
                new_cmd_path += [('M', lerp(p, p2, percentage))]
            else:
                new_cmd_path += [('L', lerp(p, p2, percentage))]

        return Path(new_cmd_path, mat=self.mat.lerp(path.mat, percentage))

    def __repr__(self):
        return f'<path d="{self.d()}" {self.mat}/>'

    def d(self):
        return "".join(
            map(
                lambda p: p[0] + f'{p[1][0]} {p[1][1]}',
                self.cmd_point
            )
        )


def get_commands_and_points(path_str: str):
    path_str = parse_path(path_str).d()
    pattern = r'["MLHVCSQTAZ"]'
    points = re.split(pattern, path_str)[1:]
    commands = re.findall(pattern, path_str)
    return list(
        zip(
            commands,
            map(
                lambda ps: re.split(r'[", "]', ps[1:-1]),  # This function takes points str and returns list of points
                points
            )
        )
    )


def get_cmd_points(path_points, i):
    cmd, e_points = path_points[i]

    if cmd == 'M':
        return [('M', vector(*e_points, 0))]

    l_cmd, l_points = path_points[i - 1]
    s_vec = vector(*l_points[-2:])
    path = []

    if cmd == 'L':
        path = [vector(*e_points[-2:])]

    elif cmd == 'C':
        c1x, c1y, c2x, c2y, ex, ey = e_points
        path = cubic_path(s_vec, vector(c1x, c1y), vector(c2x, c2y), vector(ex, ey))
    elif cmd == 'S':
        c2x, c2y, ex, ey = e_points
        if l_cmd in ['S', 's', 'C', 'c']:
            # first control point is the reflection of the last curve's last control point
            last_end_p = vector(l_points[-2], l_points[-1])
            last_control_p = vector(l_points[-4], l_points[-3])
            path = cubic_path(
                s_vec,
                last_end_p + (last_end_p - last_control_p),
                vector(c2x, c2y),
                vector(ex, ey)
            )
        else:
            # else first control point coincides with starting point
            path = cubic_path(
                s_vec,
                s_vec,
                vector(c2x, c2y),
                vector(ex, ey)
            )
    elif cmd == 'Q':
        mx, my, ex, ey = e_points
        path = quadratic_path(s_vec, vector(mx, my), vector(ex, ey))
    elif cmd == 'T':
        # Not Implemented
        return []
    elif cmd == 'A':
        rx, ry, angle_x_axis, large_arc_flag, sweep_flag, ex, ey = e_points
        path = arc_path(
            s_vec,
            vector(ex, ey),
            float(rx),
            float(ry),
            float(angle_x_axis),
            int(large_arc_flag),
            int(sweep_flag)
        )

    return [('L', vector(*p, 0)) for p in path]


def get_path_obj_from_d_path(d_path):
    paths_and_commands = get_commands_and_points(d_path)
    path_obj = Path([])
    for i in range(len(paths_and_commands)):
        path_obj.extend(
            get_cmd_points(paths_and_commands, i)
        )
    return path_obj


class Parser(object):
    def __init__(self, svg_file):
        self.svg_file = svg_file
        self.defs = {}
        self.paths = []
        self.width = 0
        self.height = 0
        self.x_pix = 1
        self.y_pix = 1
        self.x_off = 0
        self.y_off = 0
        self.generate_paths()

    def generate_paths(self):
        """Only supports one svg element in an svg file"""
        svgDoc = minidom.parse(self.svg_file)

        svg = svgDoc.getElementsByTagName("svg")[0]

        width = svg.getAttribute("width")
        height = svg.getAttribute("height")

        try:
            width = float(width)
        except Exception as e:
            width = float(width[:-2])

        try:
            height = float(height)
        except Exception as e:
            height = float(height[:-2])

        self.width = width
        self.height = height

        if svg.getAttribute("viewBox"):
            sx, sy, user_width, user_height = list(map(float, svg.getAttribute("viewBox").split(" ")))
            self.x_pix = width / user_width
            self.y_pix = height / user_height
            self.x_off = -sx * self.x_pix
            self.y_off = -sy * self.y_pix

        self.get_defs_from_svg(svg)
        self.get_paths_from_svg(svg)

        svgDoc.unlink()

    def get_vec(self, p):
        return vector(
            p[0] * self.x_pix + self.x_off - (self.width / 2),
            -(p[1] * self.y_pix + self.y_off - (self.height / 2)),
            0
        )

    def get_paths_from_svg(self, element):
        if not isinstance(element, minidom.Element):
            return
        elif element.tagName in ['g', 'svg', 'symbol']:
            [self.get_paths_from_svg(child) for child in element.childNodes]
        elif element.tagName == 'use':
            self.add_use(element)
        elif element.tagName == 'rect':
            self.add_rect(element)
        elif element.tagName == 'path':
            self.add_path(element)
        elif element.tagName == 'circle':
            self.add_circle(element)

    def get_defs_from_svg(self, element):
        if not isinstance(element, minidom.Element):
            return
        elif element.tagName in ['defs', 'svg', 'symbol']:
            [self.get_defs_from_svg(child) for child in element.childNodes]
        elif element.getAttribute('id') and element.tagName == 'path':
            self.defs[element.getAttribute('id')] = get_path_obj_from_d_path(element.getAttribute('d'))

    def add_circle(self, circle_element):
        pass

    def add_rect(self, rect_element):
        x = float(rect_element.getAttribute('x'))
        y = float(rect_element.getAttribute('y'))
        width = float(rect_element.getAttribute('width'))
        height = float(rect_element.getAttribute('height'))

        l_up = self.get_vec(vector(x, y))
        r_down = self.get_vec(vector(x + width, y + height))
        r_up = self.get_vec(vector(x + width, y))
        l_down = self.get_vec(vector(x, y + height))

        path_obj = Path(
            [
                ('M', r_down), ('L', r_up), ('L', l_up), ('L', l_down), ('L', r_down)
            ]
        )

        self.paths.append(path_obj)

    def add_path(self, path_element):
        path_obj = get_path_obj_from_d_path(path_element.getAttribute('d'))

        self.paths.append(
            path_obj.apply_func(self.get_vec)
        )

    def add_use(self, use_element):
        x = float(use_element.getAttribute('x'))
        y = float(use_element.getAttribute('y'))
        path_link = use_element.getAttribute('xlink:href')[1:]
        path_obj = self.defs[path_link]

        self.paths.append(
            path_obj.apply_func(
                lambda point: self.get_vec(vector(point[0] + x, point[1] + y))
            )
        )
