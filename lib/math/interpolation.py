import numpy as np

from lib.math.functions import sigmoid


def smooth(t, inflection=10.0):
    error = sigmoid(-inflection / 2)
    return np.clip(
        (sigmoid(inflection * (t - 0.5)) - error) / (1 - 2 * error),
        0, 1,
    )


def lerp(s, e, per):
    if per <= 0:
        return s
    elif per >= 1:
        return e
    return s + per * (e - s)
