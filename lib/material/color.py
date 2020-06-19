import numpy as np


def col_hex_to_rgb(hex_col):
    hex_col = hex_col.lstrip("#")
    r_g_b = [int(hex_col[i:i + 2], 16) for i in (0, 2, 4)]
    return np.array(r_g_b)


def col_get_col(r, g, b):
    return np.array(r, g, b)


def col_to_str(col):
    return str(col)[1:-1]


DARK_BLUE = col_hex_to_rgb("#236B8E")
DARK_BROWN = col_hex_to_rgb("#8B4513")
LIGHT_BROWN = col_hex_to_rgb("#CD853F")
BLUE_E = col_hex_to_rgb("#1C758A")
BLUE_D = col_hex_to_rgb("#29ABCA")
BLUE_C = col_hex_to_rgb("#58C4DD")
BLUE_B = col_hex_to_rgb("#9CDCEB")
BLUE_A = col_hex_to_rgb("#C7E9F1")
TEAL_E = col_hex_to_rgb("#49A88F")
TEAL_D = col_hex_to_rgb("#55C1A7")
TEAL_C = col_hex_to_rgb("#5CD0B3")
TEAL_B = col_hex_to_rgb("#76DDC0")
TEAL_A = col_hex_to_rgb("#ACEAD7")
GREEN_E = col_hex_to_rgb("#699C52")
GREEN_D = col_hex_to_rgb("#77B05D")
GREEN_C = col_hex_to_rgb("#83C167")
GREEN_B = col_hex_to_rgb("#A6CF8C")
GREEN_A = col_hex_to_rgb("#C9E2AE")
YELLOW_E = col_hex_to_rgb("#E8C11C")
YELLOW_D = col_hex_to_rgb("#F4D345")
YELLOW_C = col_hex_to_rgb("#FFFF00")
YELLOW_B = col_hex_to_rgb("#FFEA94")
YELLOW_A = col_hex_to_rgb("#FFF1B6")
GOLD_E = col_hex_to_rgb("#C78D46")
GOLD_D = col_hex_to_rgb("#E1A158")
GOLD_C = col_hex_to_rgb("#F0AC5F")
GOLD_B = col_hex_to_rgb("#F9B775")
GOLD_A = col_hex_to_rgb("#F7C797")
RED_E = col_hex_to_rgb("#CF5044")
RED_D = col_hex_to_rgb("#E65A4C")
RED_C = col_hex_to_rgb("#FC6255")
RED_B = col_hex_to_rgb("#FF8080")
RED_A = col_hex_to_rgb("#F7A1A3")
MAROON_E = col_hex_to_rgb("#94424F")
MAROON_D = col_hex_to_rgb("#A24D61")
MAROON_C = col_hex_to_rgb("#C55F73")
MAROON_B = col_hex_to_rgb("#EC92AB")
MAROON_A = col_hex_to_rgb("#ECABC1")
PURPLE_E = col_hex_to_rgb("#644172")
PURPLE_D = col_hex_to_rgb("#715582")
PURPLE_C = col_hex_to_rgb("#9A72AC")
PURPLE_B = col_hex_to_rgb("#B189C6")
PURPLE_A = col_hex_to_rgb("#CAA3E8")
WHITE = col_hex_to_rgb("#FFFFFF")
BLACK = col_hex_to_rgb("#000000")
LIGHT_GRAY = col_hex_to_rgb("#BBBBBB")
LIGHT_GREY = col_hex_to_rgb("#BBBBBB")
GRAY = col_hex_to_rgb("#888888")
GREY = col_hex_to_rgb("#888888")
DARK_GREY = col_hex_to_rgb("#444444")
DARK_GRAY = col_hex_to_rgb("#444444")
DARKER_GREY = col_hex_to_rgb("#222222")
DARKER_GRAY = col_hex_to_rgb("#222222")
GREY_BROWN = col_hex_to_rgb("#736357")
PINK = col_hex_to_rgb("#D147BD")
LIGHT_PINK = col_hex_to_rgb("#DC75CD")
GREEN_SCREEN = col_hex_to_rgb("#00FF00")
ORANGE = col_hex_to_rgb("#FF862F")

ALL_col_hex_to_rgbS = [
    DARK_BLUE,
    DARK_BROWN,
    LIGHT_BROWN,
    BLUE_E,
    BLUE_D,
    BLUE_C,
    BLUE_B,
    BLUE_A,
    TEAL_E,
    TEAL_D,
    TEAL_C,
    TEAL_B,
    TEAL_A,
    GREEN_E,
    GREEN_D,
    GREEN_C,
    GREEN_B,
    GREEN_A,
    YELLOW_E,
    YELLOW_D,
    YELLOW_C,
    YELLOW_B,
    YELLOW_A,
    GOLD_E,
    GOLD_D,
    GOLD_C,
    GOLD_B,
    GOLD_A,
    RED_E,
    RED_D,
    RED_C,
    RED_B,
    RED_A,
    MAROON_E,
    MAROON_D,
    MAROON_C,
    MAROON_B,
    MAROON_A,
    PURPLE_E,
    PURPLE_D,
    PURPLE_C,
    PURPLE_B,
    PURPLE_A,
    WHITE,
    LIGHT_GRAY,
    LIGHT_GREY,
    GRAY,
    GREY,
    DARK_GREY,
    DARK_GRAY,
    DARKER_GREY,
    DARKER_GRAY,
    GREY_BROWN,
    PINK,
    LIGHT_PINK,
    GREEN_SCREEN,
    ORANGE,
    BLACK
]
