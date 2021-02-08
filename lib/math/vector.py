import math

import numpy as np


def vec_mag(vec):
    return math.sqrt(vec.dot(vec))


def vec_norm(vec):
    return vec / vec_mag(vec)


def vec_distance(vec1, vec2):
    return math.sqrt(((vec1 - vec2) ** 2).sum())


def vec_direction(start_vec, end_vec):
    return end_vec - start_vec


def vec_direction_norm(start_vec, end_vec):
    return vec_norm(vec_direction(start_vec, end_vec))


def vec_to_str(vec):
    return str(vec)[1:-1]


def vector(*values):
    return np.array(values, dtype=np.float64)


VEC2_X_AXIS = vector(1, 0)
VEC2_Y_AXIS = vector(0, 1)

VEC2_UP = vector(0, 1)
VEC2_DOWN = vector(0, -1)
VEC2_LEFT = vector(-1, 0)
VEC2_RIGHT = vector(1, 0)

VEC2_ZERO = vector(0, 0)

VEC2_NSCALE = vector(1, 1)

VEC3_X_AXIS = vector(1, 0, 0)
VEC3_Y_AXIS = vector(0, 1, 0)
VEC3_Z_AXIS = vector(0, 0, 1)

VEC3_UP = vector(0, 1, 0)
VEC3_DOWN = vector(0, -1, 0)
VEC3_LEFT = vector(-1, 0, 0)
VEC3_RIGHT = vector(1, 0, 0)
VEC3_IN = vector(0, 0, 1)
VEC3_OUT = vector(0, 0, -1)

VEC3_ZERO = vector(0, 0, 0)

VEC3_NSCALE = vector(1, 1, 1)
