from lib.math.interpolation import lerp


def get_equal_len_paths(spaths, epaths):
    if len(spaths) < len(epaths):
        last_index = len(spaths) - 1
        s_i = 0
        while len(spaths) != len(epaths):
            spaths.append(spaths[s_i])
            if s_i == last_index:
                s_i = -1
            s_i += 1
    elif len(spaths) > len(epaths):
        last_index = len(epaths) - 1
        s_i = 0
        while len(epaths) != len(spaths):
            epaths.append(epaths[s_i])
            if s_i == last_index:
                s_i = -1
            s_i += 1
    return spaths, epaths


def path_linspace(path, no_of_points=200):
    if len(path) == no_of_points:
        return path
    return [lerp_path(path, 1 / no_of_points * n)[-1] for n in range(no_of_points + 1)]


def lerp_path(path, per):
    if per <= 0:
        return [path[0]]
    if per >= 1:
        return path

    per *= len(path) - 1

    last_point = int(per)
    new_per = per - last_point
    new_path = path[:last_point + 1]

    new_path.append(
        lerp(path[last_point], path[last_point + 1], new_per)
    )
    return new_path
