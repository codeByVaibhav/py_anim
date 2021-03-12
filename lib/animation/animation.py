from lib.material.material import *
from lib.math.interpolation import *
from lib.math.path import *
from lib.math.quaternion import *


class Animation(object):
    def __init__(self):
        pass

    def progress(self):
        pass


class ShowShape(Animation):
    def __init__(self, shape, speed=0.0625):
        super().__init__()
        self.speed = speed
        self.shape = shape.copy()

    def progress(self):
        per = -self.speed
        final_frames = []
        paths = self.shape.get_mat_and_paths()
        path_objects = []
        for path in paths:
            path_objects += path.get_subpaths()

        alpha = (len(path_objects) - 1) / 50
        while per - alpha <= 1:
            per += self.speed
            frame = []
            for i, path_obj in enumerate(path_objects):
                po = path_obj.lerp(smooth(per - (i / 50)))
                po.mat.fill_opacity = 0
                frame.append(po)

            final_frames.append(frame)

        per = -self.speed
        while per <= 1:
            per += self.speed
            frame = []
            for i, path_obj in enumerate(paths):
                path_obj = path_obj.copy()
                path_obj.mat.fill_opacity = lerp(0, path_obj.mat.fill_opacity, smooth(per))
                frame.append(path_obj)

            final_frames.append(frame)

        return final_frames


class MorphShape(Animation):
    def __init__(
            self,
            start_shape,
            end_shape,
            no_of_points=100,
            speed=0.0625
    ):
        super().__init__()
        self.speed = speed
        self.no_of_points = no_of_points

        self.start_shape = start_shape.copy()
        self.end_shape = end_shape.copy()

    def progress(self):
        per = -self.speed
        final_frames = []

        paths_s = self.start_shape.get_mat_and_paths()
        paths_e = self.end_shape.get_mat_and_paths()
        final_frame_paths = self.end_shape.get_mat_and_paths()

        s_paths = []
        for path in paths_s:
            s_paths += path.get_subpaths()

        e_paths = []
        for path in paths_e:
            e_paths += path.get_subpaths()

        # Make the paths of equal lengths
        s_paths = s_paths * (len(e_paths) // len(s_paths)) + s_paths[:len(e_paths) % len(s_paths)]
        e_paths = e_paths * (len(s_paths) // len(e_paths)) + e_paths[:len(s_paths) % len(e_paths)]
        # Make each path of same size
        s_paths = [path.linspace(self.no_of_points) for path in s_paths]
        e_paths = [path.linspace(self.no_of_points) for path in e_paths]

        while per <= 1:
            per += self.speed
            frame = [s_path.lerp_to_path(e_path, smooth(per)) for s_path, e_path in zip(s_paths, e_paths)]
            final_frames.append(frame)

        final_frames.append(final_frame_paths)
        return final_frames


class RotateShape(Animation):
    def __init__(self, axis, angel, shape, speed=0.0625):
        super().__init__()
        self.axis = axis
        self.angel = angel
        self.shape = shape
        self.speed = speed

    def progress(self):
        per = -self.speed
        final_frames = []

        paths = self.shape.get_mat_and_paths()

        while per <= 1:
            per += self.speed
            angel_of_rotation = lerp(0, self.angel, smooth(per))
            rot = Quaternion(self.axis, angel_of_rotation)
            frame = [path.apply_func(rot.rotate) for path in paths]
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
