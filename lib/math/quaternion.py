from lib.math.vector import *


# Hamilton product for quaternion multiplication
def H(a, b):
    return np.array([
        a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3],  # w
        a[0] * b[1] + a[1] * b[0] + a[2] * b[3] - a[3] * b[2],  # x
        a[0] * b[2] - a[1] * b[3] + a[2] * b[0] + a[3] * b[1],  # y
        a[0] * b[3] + a[1] * b[2] - a[2] * b[1] + a[3] * b[0],  # z
    ])


# Same as above function but using numpy.dot function
def H2(a, b):
    return a.dot([
        [b[0], b[1], b[2], b[3]],
        [-b[1], b[0], -b[3], b[2]],
        [-b[2], b[3], b[0], -b[1]],
        [-b[3], -b[2], b[1], b[0]],
    ])


class Quaternion(object):
    def __init__(
            self,
            axis_of_rotation,
            angel: float,
            angel_in_radians=False
    ):
        if not angel_in_radians:
            angel *= (np.pi / 180)

        self.axis = axis_of_rotation
        self.angel = angel
        w = math.cos(angel / 2)
        x = axis_of_rotation[0] * math.sin(angel / 2)
        y = axis_of_rotation[1] * math.sin(angel / 2)
        z = axis_of_rotation[2] * math.sin(angel / 2) if len(axis_of_rotation) > 2 else 0

        mag = math.sqrt(w ** 2 + x ** 2 + y ** 2 + z ** 2)

        w /= mag
        x /= mag
        y /= mag
        z /= mag

        self.wxyz = vector(w, x, y, z)

    def __mul__(self, o):
        r = Quaternion(VEC3_ZERO, 0)
        r.wxyz = H2(self.wxyz, o.wxyz)
        return r

    def __str__(self):
        return f'wxyz: {self.wxyz}'

    def rotate(self, vec):
        q_ = self.wxyz * -1
        q_[0] *= -1
        v = vector(0, *vec)
        r = H2(H2(self.wxyz, v), q_)

        return vector(*r[1:])


QUAT_IDEN = Quaternion(VEC3_ZERO, 0)
