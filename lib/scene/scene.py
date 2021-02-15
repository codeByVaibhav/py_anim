import copy

from cairosvg import svg2png
from tqdm import tqdm

from lib.file.constants import *
from lib.material.material import *
from lib.math.quaternion import *

import shlex
import subprocess as sp
from io import BytesIO
from touch import touch

svg = f'''\
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 WIDTH HEIGHT">
<rect width="100%" height="100%" fill="black" />
<!--  <path d="M960 0L960 1080" stroke="red"/>  -->
<!--  <path d="M0 540L1920 540" stroke="red"/>  -->

'''


class Camera(object):
    def __init__(self, width=1920, height=1080, pos=vector(0, 0, 8), rot=QUAT_IDEN, scale=vector(1, 1, 1)):
        self.pos = pos
        self.rot = rot
        self.scale = scale
        self.center_coordinate = vector(width / 2, height / 2)
        self.aspect_ratio = height / width
        self.fov = np.pi / 2
        self.fov_rad = 1.0 / math.tan(self.fov / 2)
        self.near = 0.0001
        self.far = 100000

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
            projected_path.append(out_p)
        return projected_path


class Scene(object):
    def __init__(
            self,
            width=1920,
            height=1080,
            quality='5M',
            fps=24,
            **kwargs
    ):
        self.unit_time = 1 / fps
        self.fps = fps

        self.camera = Camera(width=width, height=height)

        self.width = width
        self.height = height
        self.quality = quality

        self.svg_header = svg.replace('WIDTH', str(width))
        self.svg_header = self.svg_header.replace('HEIGHT', str(height))
        self.svg_end = '\n</svg>'
        self.frames = []
        self.svg_frames = []
        self.background_frame = []

        self.begin()
        self.end()

    def begin(self):
        '''
        This function starts the scene.
        Should be implemented by child object.
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

    def pause(self, time, frame=None):
        '''
        if frame is None than background is rendered at pause time
        '''
        if frame is None:
            while time > 0:
                time -= self.unit_time
                self.frames.append(self.background_frame)
        else:
            while time > 0:
                time -= self.unit_time
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
            mat, paths = obj.get_mat_and_paths()
            self.background_frame += [(mat, path) for path in paths]
        self.background_frame = self.get_sorted_frame(self.background_frame)

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

    def get_svg_path(self, path, mat=DEFAUT_MAT):
        d = 'M' + "".join(f'L{i[0]} {i[1]}' for i in path)[1:]
        return f'<path d="{d}" {mat}/>'

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
            f'{VIDEO_DIR}\\out.mp4',  # output file
        ])
        ffmpeg_cmd = sp.Popen(command, stdin=sp.PIPE)

        for i, frame in enumerate(tqdm(self.frames)):
            svg_paths = [
                self.get_svg_path(
                    self.camera.get_projected_path(path),
                    mat=mat
                ) for mat, path in frame
            ]
            svg_frame = self.svg_header + '\n'.join(svg_paths) + self.svg_end
            svg2png(bytestring=svg_frame, write_to=ffmpeg_cmd.stdin)
            # write_svg(VIDEO_DIR + f"\\{i + 1}.svg", svg_frame)

        ffmpeg_cmd.stdin.close()
        ffmpeg_cmd.wait()
        os.system(f'{VIDEO_DIR}\\out.mp4')


def write_svg(file, frame):
    with open(file, 'w') as opened_file:
        opened_file.write(frame)
