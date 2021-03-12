import copy

from cairosvg import svg2png
from tqdm import tqdm
import subprocess as sp

from lib.file.constants import *
from lib.material.material import *
from lib.math.quaternion import *


class Camera(object):
    def __init__(self, width=1920, height=1080, pos=vector(0, 0, 4), rot=QUAT_IDEN, scale=vector(1, 1, 1)):
        self.pos = pos
        self.rot = rot
        self.scale = scale
        self.center_coordinate = vector(width / 2, height / 2)
        self.aspect_ratio = height / width
        self.fov = np.pi / 2
        self.fov_rad = 1.0 / math.tan(self.fov / 2)
        self.near = 0.001
        self.far = 1000000

        self.proj_mat = np.array([
            [self.aspect_ratio / self.fov_rad, 0, 0, 0],
            [0, self.fov_rad, 0, 0],
            [0, 0, self.far / (self.far - self.near), 1],
            [0, 0, (-self.far * self.near) / (self.far - self.near), 0]
        ],
            dtype=np.float64
        )

    def copy(self):
        return copy.deepcopy(self)

    def get_projected_path(self, path):
        projected_path = []
        for p in path:
            p = (self.rot.rotate(p) + self.pos) * self.scale
            proj_p = np.array([p[0], p[1], p[2], 1]).dot(self.proj_mat)
            proj_p /= proj_p[-1]
            out_p = vector(proj_p[0], -proj_p[1]) + vector(1, 1)
            out_p *= self.center_coordinate
            projected_path.append(vector(*out_p, 0))
        return projected_path

    def get_projected_point(self, p):
        p = (self.rot.rotate(p) + self.pos) * self.scale
        proj_p = np.array([p[0], p[1], p[2], 1]).dot(self.proj_mat)
        proj_p /= proj_p[-1]
        out_p = vector(proj_p[0], -proj_p[1]) + vector(1, 1)
        out_p *= self.center_coordinate
        return vector(*out_p, 0)


class Scene(object):
    def __init__(
            self,
            width=1920,
            height=1080,
            quality='5M',
            fps=60,
            cam_pos=vector(0, 0, 4),
            **kwargs
    ):
        self.unit_time = 1 / fps
        self.fps = fps
        self.camera = Camera(width=width, height=height, pos=cam_pos)
        self.width = width
        self.height = height
        self.quality = quality
        self.output_file = os.path.join(VIDEO_DIR, 'out.mp4')
        self.frames = []
        self.svg_frames = []
        self.background_frame = []
        self.begin()
        self.end()

    def begin(self):
        '''
        This function starts the scene.
        Should be implemented by child class.
        '''
        pass

    def clear_background(self):
        self.background_frame = []

    def render(self, *animations, merged=False, merged_stay_equal=False, get_frames_without_background=False,
               sort_frames=False):
        all_frames = []
        for animation in animations:
            frames = animation.progress()
            if merged:
                all_frames += [[*frames]]
            else:
                all_frames += [*frames]
        if merged:
            all_frames = self.merge_frames(
                *all_frames,
                stay_equal=merged_stay_equal
            )

        if get_frames_without_background:
            if sort_frames:
                d_frames = all_frames[:]
            else:
                d_frames = self.get_sorted_frames(all_frames[:])

        all_frames = self.insert_background_to_frames(*all_frames)

        all_frames = self.get_sorted_frames(
            all_frames) if sort_frames else all_frames

        self.frames += all_frames

        if get_frames_without_background:
            return d_frames

        return all_frames

    def merge_frames(self, *frames, stay_equal=False):
        '''
        Takes different frames and mergs them and returns
        the merged frames
        '''
        # last_frame_no = 0
        last_frame_no = 0
        for f in frames:
            if last_frame_no < len(f):
                last_frame_no = len(f)

        # merged_frame = [
        #     [frame[i] if i < len(frame) else frame[-1] for frame in frames]
        #     for i in
        #     [i for i in range(last_frame_no)]
        # ]
        merged_frame = []
        for i in range(last_frame_no):
            frame = [frame[i] if i < len(frame) else frame[-1] for frame in frames]
            for f in frames:
                if i < len(f):
                    frame += f[i]
                elif stay_equal:
                    frame += f[-1]
            merged_frame.append(frame)

        return merged_frame

    def pause(self, pause_time, frame=None):
        '''
        if frame is None than background is rendered at pause time
        '''
        if frame is None:
            while pause_time > 0:
                pause_time -= self.unit_time
                self.frames.append(self.background_frame)
        else:
            while pause_time > 0:
                pause_time -= self.unit_time
                self.frames += self.get_sorted_frame(
                    self.insert_background_to_frames(frame)
                )

    def insert_background_to_frames(self, *frames):
        if len(self.background_frame) > 0:
            return [self.background_frame + frame for frame in frames]
        return frames

    def add_frames_to_background(self, *frames):
        for frame in frames:
            self.background_frame += frame
        self.background_frame = self.get_sorted_frame(self.background_frame)

    def add_objs_to_background(self, *objs):
        for obj in objs:
            self.background_frame += obj.get_mat_and_paths()
        # self.background_frame = self.get_sorted_frame(self.background_frame)

    def get_objs_frame(self, *objs):
        frame = []
        for obj in objs:
            mat, paths = obj.get_mat_and_paths()
            frame += [(mat, path) for path in paths]
        return frame

    def get_sorted_path(self, path):
        return sorted(path, key=lambda vec: vec[2])

    def get_sorted_frame(self, frame):
        # return sorted(frame, key=lambda mat_path: self.get_sorted_path(mat_path[-1])[-1][2], reverse=True)
        return sorted(frame, key=self.sorter_f, reverse=True)

    def sorter_f(self, mat_path):
        if mat_path[-1]:
            return self.get_sorted_path(mat_path[-1])[-1][2]
        return 0

    def get_sorted_frames(self, frames):
        return [self.get_sorted_frame(frame) for frame in frames]

    def end(self):
        print('Processing all Frames.')

        command = " ".join([
            'ffmpeg',
            '-y',  # overwrite output file if it exists
            '-vsync', '0',
            '-hwaccel', 'cuda',
            '-hwaccel_output_format', 'cuda',
            '-f', 'image2pipe',
            '-s', f'{self.width}x{self.height}',  # size of one frame
            '-i', '-',  # Input comes from a pipe
            '-an',  # expect no audio file
            '-loglevel', 'error',
            '-c:v', 'h264_nvenc',  # video codec
            '-vf', f'fps={self.fps}',  # video fps
            '-threads', '16',
            '-pix_fmt', 'yuv420p',
            '-b:v', f'{self.quality}',  # video quality
            f'{self.output_file}',  # output file
        ])

        ffmpeg_cmd = sp.Popen(command, stdin=sp.PIPE)

        for i, frame in enumerate(tqdm(self.frames)):
            svg_paths = '\n'.join([
                str(path_obj.apply_func(self.camera.get_projected_point))
                for path_obj in frame
            ])
            svg_frame = SVG_TEMP_TXT.replace(
                'WIDTH HEIGHT',
                f'{self.width} {self.height}'
            ).replace(TEXT_TO_REPLACE, svg_paths)
            svg2png(bytestring=svg_frame, write_to=ffmpeg_cmd.stdin)
            # write_svg(VIDEO_DIR + f"\\{i + 1}.svg", svg_frame)

        ffmpeg_cmd.stdin.close()
        ffmpeg_cmd.wait()
        os.system(self.output_file)


def write_svg(file, frame):
    with open(file, 'w') as opened_file:
        opened_file.write(frame)
