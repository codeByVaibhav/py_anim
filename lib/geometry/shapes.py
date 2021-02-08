from copy import deepcopy
from itertools import count

from lib.math.constants import *
from lib.math.interpolation import lerp
from lib.math.path import path_linspace
from lib.math.vector import *
from lib.scene_obj.scene_obj import *


class Line(SceneObj):
    def __init__(self, start=VEC3_ZERO, end=VEC3_X_AXIS, **kwargs):
        super().__init__(**kwargs)
        self.start = start
        self.end = end

    def get_mat_and_paths(self):
        start = (self.rot.rotate(self.start) + self.pos) * self.scale
        end = (self.rot.rotate(self.end) + self.pos) * self.scale
        return (
            self.mat,
            [
                [start, end]
            ]
        )


class Rectangle(SceneObj):
    def __init__(self, width=1, height=1, **kwargs):
        super().__init__(**kwargs)

        self.lup = VEC3_LEFT * width + VEC3_UP * height
        self.rup = VEC3_RIGHT * width + VEC3_UP * height
        self.rdown = VEC3_RIGHT * width + VEC3_DOWN * height
        self.ldown = VEC3_LEFT * width + VEC3_DOWN * height
        self.width = width
        self.height = height

    def get_mat_and_paths(self):
        lup = (self.rot.rotate(self.lup) + self.pos) * self.scale
        rup = (self.rot.rotate(self.rup) + self.pos) * self.scale
        rdown = (self.rot.rotate(self.rdown) + self.pos) * self.scale
        ldown = (self.rot.rotate(self.ldown) + self.pos) * self.scale
        return (
            self.mat,
            [
                [rdown, rup, lup, ldown, rdown]
            ]
        )


class Circle(SceneObj):
    def __init__(self, start=0, end=TAU, radius=1, step=0.06981317007977318, **kwargs):
        super().__init__(**kwargs)
        self.start = start
        self.end = end
        self.radius = radius
        self.step = step
        self.path = []
        self.generate_path()

    def generate_path(self):
        self.path = []
        theta = count(self.start, step=self.step)
        for a in theta:
            self.path.append(vector(self.radius * math.cos(a), self.radius * math.sin(a), 0))
            if a >= self.end:
                break

    def get_mat_and_paths(self):
        return (
            self.mat,
            [
                [(self.rot.rotate(p) + self.pos) * self.scale for p in self.path]
            ]
        )


# x -> breadth, y -> height, z -> depth
class Cuboid(SceneObj):
    def __init__(self, breadth, height, depth, **kwargs):
        super().__init__(**kwargs)
        # Front face
        self.frd = (VEC3_X_AXIS * breadth) - (VEC3_Y_AXIS * height) + (VEC3_Z_AXIS * depth)
        self.fru = (VEC3_X_AXIS * breadth) + (VEC3_Y_AXIS * height) + (VEC3_Z_AXIS * depth)
        self.flu = (VEC3_X_AXIS * -breadth) + (VEC3_Y_AXIS * height) + (VEC3_Z_AXIS * depth)
        self.fld = (VEC3_X_AXIS * -breadth) - (VEC3_Y_AXIS * height) + (VEC3_Z_AXIS * depth)
        # Back face
        self.brd = (VEC3_X_AXIS * breadth) - (VEC3_Y_AXIS * height) - (VEC3_Z_AXIS * depth)
        self.bru = (VEC3_X_AXIS * breadth) + (VEC3_Y_AXIS * height) - (VEC3_Z_AXIS * depth)
        self.blu = (VEC3_X_AXIS * -breadth) + (VEC3_Y_AXIS * height) - (VEC3_Z_AXIS * depth)
        self.bld = (VEC3_X_AXIS * -breadth) - (VEC3_Y_AXIS * height) - (VEC3_Z_AXIS * depth)
        self.paths = []
        self.generate_paths()

    def generate_paths(self):
        self.paths = []
        front_face = [self.frd, self.fru, self.flu, self.fld, self.frd]
        left_face = [self.fld, self.flu, self.blu, self.bld, self.fld]
        right_face = [self.brd, self.bru, self.fru, self.frd, self.brd]
        up_face = [self.fru, self.bru, self.blu, self.flu, self.fru]
        down_face = [self.brd, self.frd, self.fld, self.bld, self.brd]
        back_face = [self.brd, self.bru, self.blu, self.bld, self.brd]
        self.paths.append(front_face)
        self.paths.append(left_face)
        self.paths.append(right_face)
        self.paths.append(up_face)
        self.paths.append(down_face)
        self.paths.append(back_face)

    def get_mat_and_paths(self):
        return (
            self.mat,
            [
                [(self.rot.rotate(p) + self.pos) * self.scale for p in path] for path in self.paths
            ]
        )


class LinearFunction(SceneObj):
    def __init__(self, start, end, func, step=np.pi / 90, **kwargs):
        super().__init__(**kwargs)
        self.start = start
        self.end = end
        self.step = step
        self.func = func
        self.path = []
        self.generate_path()

    def generate_path(self):
        self.path = []
        x_points = count(self.start, step=self.step)
        for p in x_points:
            self.path.append(vector(p, self.func(p), 0))
            if p >= self.end:
                break

    def get_mat_and_paths(self):
        return (
            self.mat,
            [
                [(self.rot.rotate(p) + self.pos) * self.scale for p in self.path]
            ]
        )


class NumberPlane(SceneObj):
    def __init__(self, sx, ex, sy, ey, **kwargs):
        super().__init__(**kwargs)
        self.sx, self.ex, self.sy, self.ey = sx, ex, sy, ey
        self.paths = []
        self.generate_paths()

    def generate_paths(self):
        self.paths = []

        for w in range(self.sx, self.ex + 1):
            ldown = vector(w, self.sy, 0)
            lup = vector(w, self.ey, 0)
            self.paths.append([lup, ldown])

        for h in range(self.sy, self.ey + 1):
            ldown = vector(self.sx, h, 0)
            rdown = vector(self.ex, h, 0)
            self.paths.append([ldown, rdown])

    def split_paths(self, num_splits):
        new_paths = []
        for path in self.paths:
            new_paths.append(path_linspace(path, num_splits))
        self.paths = new_paths

    def get_mat_and_paths(self):
        return (
            self.mat,
            [
                [(self.rot.rotate(p) + self.pos) * self.scale for p in path] for path in self.paths
            ]
        )


class SplitedNumberPlane(SceneObj):
    def __init__(self, sx, ex, sy, ey, **kwargs):
        super().__init__(**kwargs)
        self.sx, self.ex, self.sy, self.ey = sx, ex, sy, ey
        self.paths = []
        self.generate_paths()

    def generate_paths(self):
        self.paths = []
        # w is all the y axis
        for w in range(self.sx, 0):
            ldown = vector(w, self.sy, 0)
            mid = vector(w, -0.001, 0)
            self.paths.append([ldown, mid])

        for w in range(0, self.ex + 1):
            rdown = vector(w, self.sy, 0)
            mid = vector(w, -0.001, 0)
            self.paths.append([rdown, mid])

        for w in range(self.sx, 0):
            lup = vector(w, self.ey, 0)
            mid = vector(w, 0.001, 0)
            self.paths.append([lup, mid])

        for w in range(0, self.ex + 1):
            rup = vector(w, self.ey, 0)
            mid = vector(w, 0.001, 0)
            self.paths.append([rup, mid])

        # h is all the x axis
        for h in range(self.sy, 0):
            ldown = vector(self.sx, h, 0)
            mid = vector(-0.001, h, 0)
            self.paths.append([ldown, mid])

        for h in range(0, self.ey + 1):
            rup = vector(self.ex, h, 0)
            mid = vector(0.001, h, 0)
            self.paths.append([rup, mid])

        for h in range(self.sy, 0):
            rdown = vector(self.ex, h, 0)
            mid = vector(0.001, h, 0)
            self.paths.append([rdown, mid])

        for h in range(0, self.ey + 1):
            lup = vector(self.sx, h, 0)
            mid = vector(-0.001, h, 0)
            self.paths.append([lup, mid])

    def get_mat_and_paths(self):
        return (
            self.mat,
            [
                [(self.rot.rotate(p) + self.pos) * self.scale for p in path] for path in self.paths
            ]
        )


plus_90_around_z_axis_rot = Quaternion(VEC3_Z_AXIS, 90)
arrow_head_size = 0.4


class Arrow(SceneObj):
    def __init__(self, start=VEC3_ZERO, end=VEC3_X_AXIS, **kwargs):
        super().__init__(**kwargs)

        self.line_s = start
        self.line_e = end + vec_direction_norm(end, start) * arrow_head_size
        self.tri_p1 = vec_norm(plus_90_around_z_axis_rot.rotate(end)) * arrow_head_size * 0.5 + self.line_e
        self.tri_p2 = end
        self.tri_p3 = vec_direction(self.tri_p1, self.line_e) + self.line_e

    def get_mat_and_paths(self):
        line_s = (self.rot.rotate(self.line_s) + self.pos) * self.scale
        line_e = (self.rot.rotate(self.line_e) + self.pos) * self.scale
        tri_p1 = (self.rot.rotate(self.tri_p1) + self.pos) * self.scale
        tri_p2 = (self.rot.rotate(self.tri_p2) + self.pos) * self.scale
        tri_p3 = (self.rot.rotate(self.tri_p3) + self.pos) * self.scale
        return (
            self.mat,
            [
                [line_s, line_e, tri_p1, tri_p2, tri_p3, line_e]
            ]
        )


class CubicalSphere(SceneObj):
    def __init__(self, radius, subdivision=32, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.subdivision = subdivision
        self.paths = []
        self.generate_paths()

    def generate_paths(self):
        self.paths = []
        # Make all the verticies
        bru = vec_norm(vector(1, 1, 1)) * self.radius
        fld = vec_direction(bru, VEC3_ZERO)

        blu = deepcopy(bru)
        blu[0] *= -1
        frd = vec_direction(blu, VEC3_ZERO)

        bld = deepcopy(blu)
        bld[1] *= -1

        brd = deepcopy(bru)
        brd[1] *= -1

        flu = deepcopy(fld)
        flu[1] *= -1

        fru = deepcopy(frd)
        fru[1] *= -1

        # front edges
        fu = path_linspace([flu, fru], no_of_points=self.subdivision)
        fd = path_linspace([fld, frd], no_of_points=self.subdivision)
        fl = path_linspace([fld, flu], no_of_points=self.subdivision)
        fr = path_linspace([frd, fru], no_of_points=self.subdivision)
        # back edges
        bu = path_linspace([blu, bru], no_of_points=self.subdivision)
        bd = path_linspace([bld, brd], no_of_points=self.subdivision)
        bl = path_linspace([bld, blu], no_of_points=self.subdivision)
        br = path_linspace([brd, bru], no_of_points=self.subdivision)

        del_per = 1 / self.subdivision
        per = 0
        while per <= 1:
            mus = [lerp(s, e, per) for s, e in zip(fu, bu)]
            mds = [lerp(s, e, per) for s, e in zip(fd, bd)]
            mls = [lerp(s, e, per) for s, e in zip(fl, bl)]
            mrs = [lerp(s, e, per) for s, e in zip(fr, br)]
            mfs = [lerp(s, e, per) for s, e in zip(fl, fr)]
            mbs = [lerp(s, e, per) for s, e in zip(bl, br)]

            mue = [lerp(s, e, per + del_per) for s, e in zip(fu, bu)]
            mde = [lerp(s, e, per + del_per) for s, e in zip(fd, bd)]
            mle = [lerp(s, e, per + del_per) for s, e in zip(fl, bl)]
            mre = [lerp(s, e, per + del_per) for s, e in zip(fr, br)]
            mfe = [lerp(s, e, per + del_per) for s, e in zip(fl, fr)]
            mbe = [lerp(s, e, per + del_per) for s, e in zip(bl, br)]
            # up side
            for i, (s, e) in enumerate(list(zip(mus, mue))[:-1]):
                self.paths += [[s, mus[i + 1], mue[i + 1], e, s]]
            # down side
            for i, (s, e) in enumerate(list(zip(mds, mde))[:-1]):
                self.paths += [[s, mds[i + 1], mde[i + 1], e, s]]
            # left side
            for i, (s, e) in enumerate(list(zip(mls, mle))[:-1]):
                self.paths += [[s, mls[i + 1], mle[i + 1], e, s]]
            # right side
            for i, (s, e) in enumerate(list(zip(mrs, mre))[:-1]):
                self.paths += [[s, mrs[i + 1], mre[i + 1], e, s]]
            # front side
            for i, (s, e) in enumerate(list(zip(mfs, mfe))[:-1]):
                self.paths += [[s, mfs[i + 1], mfe[i + 1], e, s]]
            # back side
            for i, (s, e) in enumerate(list(zip(mbs, mbe))[:-1]):
                self.paths += [[s, mbs[i + 1], mbe[i + 1], e, s]]

            per += del_per

        self.paths = [[vec_norm(p) * self.radius for p in path] for path in self.paths]

    def get_mat_and_paths(self):
        return (
            self.mat,
            [
                [(self.rot.rotate(p) + self.pos) * self.scale for p in path] for path in self.paths
            ]
        )


class Sphere(SceneObj):
    def __init__(self, radius, subdivision=32, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.subdivision = subdivision
        self.paths = []
        self.generate_paths()

    def generate_paths(self):
        self.paths = []
        circle = []
        start_angle = np.pi / 2
        del_per = 1 / self.subdivision
        per = 0
        while per <= 1:
            theta = lerp(-start_angle, start_angle, per)
            x = self.radius * math.cos(theta)
            y = self.radius * math.sin(theta)
            circle.append(vector(x, y, 0))
            per += del_per

        rot = Quaternion(VEC3_Y_AXIS, lerp(0, TAU, del_per), angel_in_radians=True)

        per = del_per
        while per <= 1:
            new_circle = [rot.rotate(p) for p in circle]
            for i, (s, e) in enumerate(list(zip(circle, new_circle))[:-1]):
                s2 = circle[i + 1]
                e2 = new_circle[i + 1]
                self.paths += [[e, e2, s2, s, e]]
            circle = new_circle
            per += del_per

    def get_mat_and_paths(self):
        return (
            self.mat,
            [
                [(self.rot.rotate(p) + self.pos) * self.scale for p in path] for path in self.paths
            ]
        )


class Cylinder(SceneObj):
    def __init__(self, radius, height, subdivision=32, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.height = height
        self.subdivision = subdivision
        self.paths = []
        self.generate_paths()

    def generate_paths(self):
        self.paths = []
        circle = []
        del_per = 1 / self.subdivision
        per = 0
        while per <= 1:
            theta = lerp(0, TAU, per)
            x = self.radius * math.cos(theta)
            z = self.radius * math.sin(theta)
            circle.append(vector(x, 0, z))
            per += del_per

        half_height = self.height / 2
        start_pos = vector(0, -half_height, 0)
        end_pos = vector(0, half_height, 0)
        all_y_pos = np.linspace(start_pos, end_pos, self.subdivision)

        for i, y_pos in enumerate(all_y_pos[:-1]):
            e_y_pos = all_y_pos[i + 1]
            s_circle = [p + y_pos for p in circle]
            e_circle = [p + e_y_pos for p in circle]
            for i, (s, e) in enumerate(list(zip(s_circle, e_circle))[:-1]):
                s2 = s_circle[i + 1]
                e2 = e_circle[i + 1]

                self.paths += [[s, s2, e2, e, s]]

    def get_mat_and_paths(self):
        return (
            self.mat,
            [
                [(self.rot.rotate(p) + self.pos) * self.scale for p in path] for path in self.paths
            ]
        )
