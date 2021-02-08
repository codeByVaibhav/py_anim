import re
from xml.dom import minidom
from lib.geometry.curves import *
from lib.math.vector import *


class Parser(object):
    def __init__(self, svg_file):
        self.svg_file = svg_file
        self.defs = {}
        self.paths = []
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

    def get_normal_path(self, path_string):
        path_string = path_string.replace('-', ',-')
        path_string = path_string.replace(',', ' ')
        path_string = path_string.replace('M ', 'M')
        path_string = path_string.replace('L ', 'L')
        path_string = path_string.replace('H ', 'H')
        path_string = path_string.replace('V ', 'V')
        path_string = path_string.replace('C ', 'C')
        path_string = path_string.replace('S ', 'S')
        path_string = path_string.replace('Q ', 'Q')
        path_string = path_string.replace('T ', 'T')
        path_string = path_string.replace('A ', 'A')
        path_string = path_string.replace('Z ', 'Z')
        path_string = path_string.replace('m ', 'm')
        path_string = path_string.replace('l ', 'l')
        path_string = path_string.replace('h ', 'h')
        path_string = path_string.replace('v ', 'v')
        path_string = path_string.replace('c ', 'c')
        path_string = path_string.replace('s ', 's')
        path_string = path_string.replace('q ', 'q')
        path_string = path_string.replace('t ', 't')
        path_string = path_string.replace('a ', 'a')
        path_string = path_string.replace('z ', 'z')
        return path_string

    def str_to_float(self, *points):
        return (float(point) for point in points)

    def get_absolute_paths(self, all_path):
        new_all_path = all_path[:]
        for i, path in enumerate(all_path):
            for j, (cmd, points) in enumerate(path):
                if cmd == 'l':
                    pcmd, ppoints = new_all_path[i][j - 1]
                    x, y = self.str_to_float(*ppoints.split(' ')[-2:])
                    lx, ly = self.str_to_float(*points.split(' '))
                    new_all_path[i][j] = ('L', f'{lx + x} {ly + y}')
                elif cmd == 'c':
                    pcmd, ppoints = new_all_path[i][j - 1]
                    x, y = self.str_to_float(*ppoints.split(' ')[-2:])
                    c1x, c1y, c2x, c2y, ex, ey = self.str_to_float(*points.split(' '))
                    new_all_path[i][j] = ('C', f'{c1x + x} {c1y + y} {c2x + x} {c2y + y} {ex + x} {ey + y}')
                elif cmd == 'q':
                    pcmd, ppoints = new_all_path[i][j - 1]
                    x, y = self.str_to_float(*ppoints.split(' ')[-2:])
                    cx, cy, ex, ey = self.str_to_float(*points.split(' '))
                    new_all_path[i][j] = ('Q', f'{cx + x} {cy + y} {ex + x} {ey + y}')
                elif cmd == 'a':
                    pcmd, ppoints = new_all_path[i][j - 1]
                    x, y = self.str_to_float(*ppoints.split(' ')[-2:])
                    rx, ry, angle_x_axis, large_arc_flag, sweep_flag, ex, ey = self.str_to_float(*points.split(' '))
                    new_all_path[i][j] = (
                    'A', f'{rx + x} {ry + y} {angle_x_axis} {large_arc_flag} {sweep_flag} {ex + x} {ey + y}')

        return new_all_path

    def get_dpath_commands_and_points(self, path_string):
        pattern = '["MLHVCSQTAZmlhvcsqtaz"]'
        path_string = self.get_normal_path(path_string)
        all_path = []
        Ms = list(zip(
            re.findall('[M]', path_string),
            re.split('[M]', path_string)[1:]
        ))
        for _, path in Ms:
            all_path.append(list(zip(
                re.findall(pattern, 'M' + path),
                re.split(pattern, 'M' + path)[1:]
            )))
        all_path = self.get_absolute_paths(all_path)
        return all_path

    def get_last_vec(self, path, i):
        cmd, points = path[i - 1]
        if cmd == 'H':
            sx = points
            index = 2
            while cmd == 'H':
                cmd, points = path[i - index]
                index += 1
            sy = points.split(' ')[-1]
        elif cmd == 'V':
            sy = points
            index = 2
            while cmd == 'V':
                cmd, points = path[i - index]
                index += 1
            if cmd == 'H':
                sx = points
            else:
                sx = points.split(' ')[-2]
        else:
            sx, sy = points.split(' ')[-2:]
        return vector(sx, sy)

    def get_line(self, path_points, i):
        if i == 0:
            cmd, points = path_points[0]
            x, y = points.split(' ')
            return [vector(x, y)]

        cmd, e_points = path_points[i]

        s_vec = self.get_last_vec(path_points, i)

        if cmd == 'L':
            ex, ey = e_points.split(' ')[-2:]
            return [vector(ex, ey)]
        elif cmd == 'H':
            return [vector(e_points, s_vec.y())]
        elif cmd == 'V':
            return [vector(s_vec.x(), e_points)]
        elif cmd == 'C':
            c1x, c1y, c2x, c2y, ex, ey = e_points.split(' ')
            return cubic_path(s_vec, vector(c1x, c1y), vector(c2x, c2y), vector(ex, ey))
        elif cmd == 'S':
            # Not Implemented
            return []
        elif cmd == 'Q':
            mx, my, ex, ey = e_points.split(' ')
            return quadratic_path(s_vec, vector(mx, my), vector(ex, ey))
        elif cmd == 'T':
            # Not Implemented
            return []
        elif cmd == 'A':
            rx, ry, angle_x_axis, large_arc_flag, sweep_flag, ex, ey = e_points.split(' ')
            return arc_path(s_vec, vector(ex, ey), float(rx), float(ry), float(angle_x_axis), int(large_arc_flag),
                            int(sweep_flag))
        elif cmd in ['Z', 'z']:
            cmd, path = path_points[0]
            x, y = path.split(' ')[-2:]
            return [vector(x, y)]

    def get_path_from_d_path(self, d_path):
        paths = self.get_dpath_commands_and_points(d_path)
        new_paths = []
        for path in paths:
            line = []
            path_size = len(path)
            for i in range(path_size):
                line += self.get_line(path, i)
            new_paths.append(line)
        return new_paths

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

    def get_defs_from_svg(self, element):
        if not isinstance(element, minidom.Element):
            return
        elif element.tagName in ['defs', 'svg', 'symbol']:
            [self.get_defs_from_svg(child) for child in element.childNodes]
        elif element.getAttribute('id'):
            if element.tagName == 'path':
                self.defs[element.getAttribute('id')] = self.get_path_from_d_path(element.getAttribute('d'))

    def add_rect(self, rect_element):
        x = float(rect_element.getAttribute('x')) * 0.1
        y = float(rect_element.getAttribute('y')) * -0.1
        width = float(rect_element.getAttribute('width')) * 0.1
        height = float(rect_element.getAttribute('height')) * 0.1

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
        paths = self.defs[path_link]
        new_paths = []
        for path in paths:
            new_path = []
            for p in path:
                res_vec = vector(p.x() + vec.x(), p.y() + vec.y(), 0) * 0.1
                res_vec.xyz[1] *= -1
                dis_from_origin = res_vec.distance(VEC3_ZERO)
                if dis_from_origin < self.sdt:
                    self.sdt = dis_from_origin
                    self.top_left = res_vec
                if dis_from_origin > self.sdb:
                    self.sdb = dis_from_origin
                    self.bottom_right = res_vec
                new_path.append(res_vec)
            new_paths.append(new_path)
        self.paths += new_paths

    def add_path(self, path_element):
        paths = self.get_path_from_d_path(path_element.getAttribute('d'))
        new_paths = []
        for path in paths:
            new_path = []
            for p in path:
                res_vec = vector(p.x() + vec.x(), (p.y() + vec.y()) * -1, 0) * 0.1

                new_path.append(res_vec)
            new_paths.append(new_path)
        self.paths += new_paths
