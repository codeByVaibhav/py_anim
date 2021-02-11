import re
from xml.dom import minidom

from lib.geometry.curves import *
from lib.math.vector import *


class SvgParser(object):
    def __init__(self, svg_file):
        self.svg_file = svg_file
        self.defs = {}
        self.paths = []
        self.scale = 0.05
        self.sdt = math.inf
        self.sdb = -math.inf
        self.top_left = VEC3_ZERO
        self.bottom_right = VEC3_ZERO
        self.generate_defs()
        self.generate_path()

    def generate_path(self):
        doc = minidom.parse(self.svg_file)
        for svg in doc.getElementsByTagName("svg"):
            self.get_paths_from_svg(svg)
        doc.unlink()

    def generate_defs(self):
        doc = minidom.parse(self.svg_file)
        for svg in doc.getElementsByTagName("svg"):
            self.get_defs_from_svg(svg)
        doc.unlink()

    def get_points_from_str(self, points_str: str):
        return list(filter(lambda x: x, points_str.replace('-', ' -').split(' ')))

    def get_commands_and_points(self, path_str: str):
        pattern = r'["MLHVCSQTAZ"]'
        paths_str = path_str.split('M')[1:]
        paths = []
        for path_s in paths_str:
            path_s = 'M' + path_s
            commands = re.findall(pattern, path_s)
            points = map(self.get_points_from_str, re.split(pattern, path_s)[1:])
            paths.append(list(zip(commands, points)))
        return paths

    def get_last_vec(self, path, i):
        cmd, points = path[i - 1]
        index = 2

        if cmd == 'H':
            scmd = 'H'
            sx = points[0]
            while scmd == 'H':
                scmd, points = path[i - index]
                index += 1
            sy = points[-1]
            return cmd + scmd, [sx, sy]

        elif cmd == 'V':
            scmd = 'V'
            sy = points[0]
            while scmd == 'V':
                scmd, points = path[i - index]
                index += 1
            sx = points[0] if scmd == 'H' else points[-2]
            return cmd + scmd, [sx, sy]

        return cmd, points

    def get_line(self, path_points, i):
        cmd, e_points = path_points[i]

        if i == 0:
            return [vector(*e_points)]
        elif cmd == 'Z':
            return [vector(*path_points[0][1])]

        lcmd, l_points = self.get_last_vec(path_points, i)
        s_vec = vector(l_points[-2], l_points[-1])

        if cmd == 'L':
            ex, ey = e_points[-2:]
            return [vector(ex, ey)]
        elif cmd == 'H':
            return [vector(*e_points, s_vec[1])]
        elif cmd == 'V':
            return [vector(s_vec[0], *e_points)]
        elif cmd == 'C':
            c1x, c1y, c2x, c2y, ex, ey = e_points
            return cubic_path(s_vec, vector(c1x, c1y), vector(c2x, c2y), vector(ex, ey))
        elif cmd == 'S':
            c2x, c2y, ex, ey = e_points
            if lcmd in ['S', 's', 'C', 'c']:
                # first control point is the reflection of the last curve's last control point
                last_end_p = vector(l_points[-2], l_points[-1])
                last_control_p = vector(l_points[-4], l_points[-3])
                return cubic_path(
                    s_vec,
                    last_end_p + (last_end_p - last_control_p),
                    vector(c2x, c2y),
                    vector(ex, ey)
                )
            else:
                # else first control point coincides with starting point
                return cubic_path(
                    s_vec,
                    s_vec,
                    vector(c2x, c2y),
                    vector(ex, ey)
                )
        elif cmd == 'Q':
            mx, my, ex, ey = e_points
            return quadratic_path(s_vec, vector(mx, my), vector(ex, ey))
        elif cmd == 'T':
            # Not Implemented
            return []
        elif cmd == 'A':
            rx, ry, angle_x_axis, large_arc_flag, sweep_flag, ex, ey = e_points
            return arc_path(
                s_vec,
                vector(ex, ey),
                float(rx),
                float(ry),
                float(angle_x_axis),
                int(large_arc_flag),
                int(sweep_flag)
            )

    def get_path_from_d_path(self, d_path):
        paths = self.get_commands_and_points(d_path)
        result_path = []
        for path in paths:
            for i in range(len(path)):
                result_path += self.get_line(path, i)
        return result_path

    def get_paths_from_svg(self, element):
        if not isinstance(element, minidom.Element):
            return
        elif element.tagName in ['g', 'svg', 'symbol']:
            [self.get_paths_from_svg(child) for child in element.childNodes]
        elif element.tagName == 'use':
            self.add_use(element)
        elif element.tagName == 'rect':
            self.add_rect(element)

    def get_defs_from_svg(self, element):
        if not isinstance(element, minidom.Element):
            return
        elif element.tagName in ['defs', 'svg', 'symbol']:
            [self.get_defs_from_svg(child) for child in element.childNodes]
        elif element.getAttribute('id'):
            if element.tagName == 'path':
                self.defs[element.getAttribute('id')] = self.get_path_from_d_path(element.getAttribute('d'))

    def add_rect(self, rect_element):
        x = float(rect_element.getAttribute('x')) * self.scale
        y = float(rect_element.getAttribute('y')) * - self.scale
        width = float(rect_element.getAttribute('width')) * self.scale
        height = float(rect_element.getAttribute('height')) * self.scale

        lup = vector(x, y, 0)
        rdown = vector(x + width, y + height, 0)
        rup = vector(x + width, y, 0)
        ldown = vector(x, y + height, 0)

        self.paths.append([rdown, rup, lup, ldown, rdown])

    def add_use(self, use_element):
        x = use_element.getAttribute('x')
        y = use_element.getAttribute('y')
        vec = vector(x, y)
        path_link = use_element.getAttribute('xlink:href')[1:]
        new_path = []
        for p in self.defs[path_link]:
            res_vec = vector(p[0] + vec[0], -1 * (p[1] + vec[1]), 0) * self.scale
            dis_from_origin = vec_distance(res_vec, VEC3_ZERO)
            if dis_from_origin < self.sdt:
                self.sdt = dis_from_origin
                self.top_left = res_vec
            if dis_from_origin > self.sdb:
                self.sdb = dis_from_origin
                self.bottom_right = res_vec
            new_path.append(res_vec)

        self.paths.append(new_path)
