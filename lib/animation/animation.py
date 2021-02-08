from lib.material.material import *
from lib.math.interpolation import *
from lib.math.path import *
from lib.math.quaternion import *


class Animation(object):
    def __init__(self):
        pass

    def progress(self):
        pass


class MorphShape(Animation):
    def __init__(
        self,
        startObj,
        endObj,
        no_of_points=200,
        speed=0.0625
    ):
        super().__init__()
        self.speed = speed
        self.no_of_points = no_of_points

        self.startObj = startObj.copy()
        self.endObj = endObj.copy()

    def progress(self):
        per = -self.speed
        final_frames = []

        smat, spaths = self.startObj.get_mat_and_paths()
        emat, epaths = self.endObj.get_mat_and_paths()

        spaths, epaths = get_equal_len_paths(spaths, epaths)

        spaths = [path_linspace(p) for p in spaths]
        epaths = [path_linspace(p) for p in epaths]

        while per <= 1:
            per += self.speed
            nper = smooth(per)
            frame = []

            for spath, epath in zip(spaths, epaths):
                mpath = [lerp(s, e, nper) for s, e, in zip(spath, epath)]
                mmat = smat.lerp(emat, nper)
                frame.append((mmat, mpath))

            final_frames.append(frame)
        return final_frames


class ShowCreation(Animation):
    def __init__(
            self,
            obj,
            speed=0.0625
    ):
        super().__init__()
        self.speed = speed
        self.obj = obj.copy()

    def progress(self):
        per = -self.speed
        final_frames = []

        mat, paths = self.obj.get_mat_and_paths()

        final_mat = mat.copy()
        mat.fill_opacity = 0

        alpha = (len(paths) - 1) / 50
        while per - alpha <= 1:
            per += self.speed

            frame = [(mat, lerp_path(path, smooth(per - (i / 50))))
                     for i, path in enumerate(paths)]

            final_frames.append(frame)

        if final_mat.fill_opacity != 0:
            per = -self.speed
            while per <= 1:
                per += self.speed * 2
                nper = smooth(per)

                frame = [(mat.lerp(final_mat, nper), path) for path in paths]

                final_frames.append(frame)

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
