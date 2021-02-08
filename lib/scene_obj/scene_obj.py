from copy import deepcopy

from lib.material.material import *
from lib.math.quaternion import *


class SceneObj(object):
    def __init__(
            self,
            pos=VEC3_ZERO,
            rot=QUAT_IDEN,
            scale=VEC3_NSCALE,
            mat=DEFAUT_MAT
    ):
        self.pos = pos
        self.rot = rot
        self.scale = scale
        self.mat = mat

    def copy(self):
        return deepcopy(self)

    def get_mat_and_paths(self):
        pass
