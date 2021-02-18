from lib.material.material import *
from lib.math.interpolation import *
from lib.math.path import *
from lib.math.quaternion import *


class Animation(object):
    def __init__(self):
        pass

    def progress(self):
        pass


class ShowCreation(Animation):
    def __init__(self, obj, speed=0.0625):
        super().__init__()
        self.speed = speed
        self.obj = obj.copy()

    def progress(self):
        per = -self.speed
        final_frames = []

        path_objects = self.obj.get_mat_and_paths()

        alpha = (len(path_objects) - 1) / 50
        while per - alpha <= 1:
            per += self.speed

            frame = []

            for i, path_obj in enumerate(path_objects):
                n_per = smooth(per - (i / 50))
                po = path_obj.lerp(n_per)
                po.mat.fill_opacity = 0
                frame.append(po)

            final_frames.append(frame)

        per = -self.speed
        while per <= 1:
            per += self.speed * 2
            n_per = smooth(per)

            frame = []

            for i, path_obj in enumerate(path_objects):
                path_obj = path_obj.copy()
                path_obj.mat.fill_opacity = lerp(0, path_obj.mat.fill_opacity, n_per)
                frame.append(path_obj)

            final_frames.append(frame)

        return final_frames


class MorphShape(Animation):
    def __init__(
        self,
        start_obj,
        end_obj,
        no_of_points=100,
        speed=0.0625
    ):
        super().__init__()
        self.speed = speed
        self.no_of_points = no_of_points

        self.start_obj = start_obj.copy()
        self.end_obj = end_obj.copy()

    def progress(self):
        per = -self.speed
        final_frames = []

        s_paths = self.start_obj.get_mat_and_paths()
        e_paths = self.end_obj.get_mat_and_paths()
        final_frame_paths = self.end_obj.get_mat_and_paths()

        # Make the paths of equal lengths
        if len(s_paths) < len(e_paths):
            s_paths = s_paths * (len(e_paths) // len(s_paths)) + s_paths[:len(e_paths) % len(s_paths)]
        elif len(e_paths) < len(s_paths):
            e_paths = e_paths * (len(s_paths) // len(e_paths)) + e_paths[:len(s_paths) % len(e_paths)]
        # Make each path of same size
        s_paths = [path.linspace(self.no_of_points) for path in s_paths]
        e_paths = [path.linspace(self.no_of_points) for path in e_paths]

        while per <= 1:
            per += self.speed
            n_per = smooth(per)
            frame = [s_path.lerp_to_path(e_path, n_per) for s_path, e_path in zip(s_paths, e_paths)]
            final_frames.append(frame)

        final_frames.append(final_frame_paths)
        return final_frames


class RotateFrame(Animation):
    def __init__(self, axis, angel, frame, speed=0.0625):
        super().__init__()
        self.axis = axis
        self.angel = angel
        self.frame = frame
        self.speed = speed

    def progress(self):
        per = -self.speed
        final_frames = []

        while per <= 1:
            per += self.speed
            nper = smooth(per)
            frame = []

            angel_of_rotation = lerp(0, self.angel, nper)
            rot = Quaternion(self.axis, angel_of_rotation)

            for mat, path in self.frame:
                path = [rot.rotate(p) for p in path]
                frame.append((mat, path))

            final_frames.append(frame)

        return final_frames


class ZoomFrame(Animation):
    def __init__(self, zoom_level, frame, speed=0.0625):
        super().__init__()
        self.zoom = zoom_level
        self.frame = frame
        self.speed = speed

    def progress(self):
        per = -self.speed
        final_frames = []

        while per <= 1:
            per += self.speed
            nper = smooth(per)
            frame = []

            scale = lerp(1, self.zoom, nper)

            for mat, path in self.frame:
                path = [p * scale for p in path]
                frame.append((mat, path))

            final_frames.append(frame)

        return final_frames


class Translate(Animation):
    def __init__(self, obj, target_pos, move_orignal_pos=True, speed=0.0625):
        super().__init__()
        self.obj = obj.copy()
        self.target_pos = target_pos
        self.speed = speed
        if move_orignal_pos:
            obj.pos = target_pos

    def progress(self):
        per = -self.speed

        final_frames = []
        start_pos = self.obj.pos
        while per <= 1:
            per += self.speed
            nper = smooth(per)

            self.obj.pos = lerp(start_pos, self.target_pos, nper)

            _, paths = self.obj.get_mat_and_paths()

            frame = [(self.obj.mat, path) for path in paths]

            final_frames.append(frame)
        return final_frames


INVISIBLE_MAT = Material(stroke=BLACK, fill_opacity=0, stroke_opacity=0)


class VanishFrame(Animation):
    def __init__(self, frame, speed=0.0625):
        super().__init__()
        self.frame = frame
        self.speed = speed

    def progress(self):
        per = -self.speed
        final_frames = []
        while per <= 1:
            per += self.speed
            nper = smooth(per)
            frame = []
            for mat, path in self.frame:
                nmat = mat.lerp(INVISIBLE_MAT, nper)
                frame.append((nmat, path))
            final_frames.append(frame)
        return final_frames


class ApplyFunction(Animation):
    def __init__(self, obj, func, start_input, end_input, speed=0.0625):
        super().__init__()
        self.obj = obj.copy()
        self.speed = speed
        self.func = func
        self.start_input = start_input
        self.end_input = end_input

    def progress(self):
        mat, paths = self.obj.get_mat_and_paths()
        final_frames = []
        per = -self.speed

        while per <= 1:
            nper = smooth(per)
            inp = lerp(self.start_input, self.end_input, nper)
            frame = []
            for path in paths:
                path = path_linspace(path)
                frame += [(mat, [self.func(p, inp=inp) for p in path])]
            final_frames.append(frame)
            per += self.speed

        return final_frames


class Scale(Animation):
    def __init__(self, obj, scale_size=2, speed=0.0625):
        super().__init__()
        self.obj = obj.copy()
        self.speed = speed
        self.scale_size = scale_size

    def progress(self):
        mat, paths = self.obj.get_mat_and_paths()
        per = 0
        frames = []
        while per <= 1:
            multi = lerp(1, self.scale_size, smooth(per))
            frames += [[(mat, [p * multi for p in path]) for path in paths]]
            per += self.speed
        return frames
