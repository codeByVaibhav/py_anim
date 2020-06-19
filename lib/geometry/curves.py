import numpy as np
from lib.math.vector import *
from lib.math.interpolation import lerp

def quadratic_path(s, m, e):
        path = []
        per = 0
        while per <= 1:
            t1    = lerp(s, m, per)
            t2    = lerp(m, e, per)
            point = lerp(t1, t2, per)
            path.append(point)
            per += 0.0625
        return path

def cubic_path(s, c1, c2, e):
        path = []
        per = 0
        while per <= 1:
            p1 = lerp(s, c1, per)
            p2 = lerp(c1, c2, per)
            p3 = lerp(c2, e, per)
            t1 = lerp(p1, p2, per)
            t2 = lerp(p2, p3, per)
            point = lerp(t1, t2, per)
            path.append(point)
            per += 0.0625
        return path

def ange_bt_vec(vec1, vec2):
    cos = vec1.dot(vec2) / ( vec_mag(vec1) * vec_mag(vec2.mag()) )
    cos = np.clip(cos, -1, 1)
    return math.acos( cos ) * (180/np.pi)

def arc_path(s, e, rx, ry, angel_from_x_axis, large_arc_flag, sweep_flag):
    x1 = s[0]
    y1 = s[1]
    x2 = e[0]
    y2 = e[1]
    if rx == 0 or ry == 0:
        return [vector(x1, y1), vector(x2, y2)]
    
    rx = rx if rx >= 0 else -rx
    ry = ry if ry >= 0 else -ry
    
    angel_from_x_axis *= (np.pi / 180)
    
    r_mat = np.array([
        [math.cos(angel_from_x_axis), math.sin(angel_from_x_axis)],
        [-math.sin(angel_from_x_axis), math.cos(angel_from_x_axis)]
    ])
    rx_ry = np.array([ (x1-x2)/2, (y1-y2)/2 ])
    # Compute (x1′, y1′)
    x_1, y_1 = r_mat.dot(rx_ry)
    alpha = (x_1**2 / rx**2) + (y_1**2 / ry**2)
    if alpha > 1:
        rx *= math.sqrt(alpha)
        ry *= math.sqrt(alpha)
    # Compute (cx′, cy′)
    cx_1_cy_1_sign = -1 if large_arc_flag == sweep_flag else 1
    z1 = ( rx**2 * ry**2 - rx**2 * y_1**2 - ry**2 * x_1**2 ) / ( rx**2*y_1**2 + ry**2*x_1**2 )
    z1 = np.clip(z1, 0, math.inf)
    cx_1, cy_1 = cx_1_cy_1_sign * ( math.sqrt( z1 ) * np.array([ rx*y_1/ry, -(ry*x_1/rx) ]) )

    c_1_mat = np.array([cx_1, cy_1])
    r_mat[0][1] *= -1
    r_mat[1][0] *= -1
    # Compute (cx, cy) from (cx′, cy′)
    cx, cy = r_mat.dot(c_1_mat) + np.array([ (x1+x2)/2, (y1+y2)/2 ])

    # Calculate θ1 θ2 Δθ
    x_axis = VEC2_X_AXIS
    start_vec = vector( (x_1 - cx_1 ) / rx,  (y_1 - cy_1 ) / ry )
    end_vec   = vector( (-x_1 - cx_1) / rx,  (-y_1 - cy_1) / ry )

    theta_1 = ange_bt_vec(VEC2_X_AXIS, start_vec)
    del_theta = ange_bt_vec(start_vec, end_vec) % 360

    if sweep_flag == 0 and del_theta > 0:
        del_theta -= 360
    elif sweep_flag == 1 and del_theta < 0:
        del_theta += 360

    theta_1 *= (np.pi / 180)
    del_theta *= (np.pi / 180)
    theta_2 = theta_1 + del_theta

    path = []
    per = 0
    while per <= 1:
        a = lerp(theta_1, theta_2, per)
        x, y = r_mat.dot(np.array([ rx * math.cos(a), ry * math.sin(a) ])) + np.array([ cx, cy ])
        path.append( vector( x, y ) )
        per += 0.0625
    return path
