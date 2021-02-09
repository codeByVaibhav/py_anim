from lib.math.vector import *


# Hamilton product for quaternion multiplication
def H(a, b):
    return np.array([
        a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3],  # w
        a[0] * b[1] + a[1] * b[0] + a[2] * b[3] - a[3] * b[2],  # x
        a[0] * b[2] - a[1] * b[3] + a[2] * b[0] + a[3] * b[1],  # y
        a[0] * b[3] + a[1] * b[2] - a[2] * b[1] + a[3] * b[0],  # z
    ])


def H2(a, b):
    mat = np.array([
        # w       #x     #y     #z
        [b[0], b[1], b[2], b[3]],
        [-b[1], b[0], -b[3], b[2]],
        [-b[2], b[3], b[0], -b[1]],
        [-b[3], -b[2], b[1], b[0]],
    ])
    return a.dot(mat)


class Quaternion(object):
    def __init__(
            self,
            axis_of_rotaiton,
            angel: float,
            angel_in_radians=False
    ):
        if angel_in_radians == False:
            angel *= (np.pi / 180)

        self.axis = axis_of_rotaiton
        self.angel = angel
        w = math.cos(angel / 2)
        x = axis_of_rotaiton[0] * math.sin(angel / 2)
        y = axis_of_rotaiton[1] * math.sin(angel / 2)
        z = axis_of_rotaiton[2] * math.sin(angel / 2) if len(axis_of_rotaiton) > 2 else 0

        mag = math.sqrt(w ** 2 + x ** 2 + y ** 2 + z ** 2)

        w /= mag
        x /= mag
        y /= mag
        z /= mag

        self.wxyz = np.array([w, x, y, z], dtype=np.float64)

    def __mul__(self, o):
        r = Quaternion(VEC3_ZERO, 0)
        r.wxyz = H(self.wxyz, o.wxyz)
        return r

    def __str__(self):
        return f'wxyz: {self.wxyz}'

    def rotate(self, vec):
        q_ = self.wxyz * -1
        q_[0] *= -1
        # v = np.array([0, vec[0], vec[1], vec[2]], dtype=np.float64)
        v = vector(0, vec[0], vec[1], vec[2])
        r = H(H(self.wxyz, v), q_)

        return vector(r[1], r[2], r[3])


QUAT_IDEN = Quaternion(VEC3_ZERO, 0)
