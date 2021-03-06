import os
import time

# ffmpeg -r 60 -i .\\pngFrames\\%02d.png -c:v libx264 -vf fps=0.01 -threads 16 -pix_fmt yuv420p out.mp4

TEXT_TO_REPLACE = "YourText"

START_TIME = time.strftime(f"%Y-%m-%d-%H-%M-%S")

# region LaTeX
TEX_USE_CTEX = False

TEX_DIR = ".\\latex\\"
TEX_TEMP_FILE = ".\\templates\\texTemp.tex"
CTEX_TEMP_FILE = ".\\templates\\ctexTemp.tex"

TEX_DIR = os.path.abspath(TEX_DIR)
TEX_TEMP_FILE = os.path.abspath(TEX_TEMP_FILE)
CTEX_TEMP_FILE = os.path.abspath(CTEX_TEMP_FILE)

f = open(TEX_TEMP_FILE, "r")
TEX_TEMP_TXT = f.read()
f.close()

f = open(CTEX_TEMP_FILE, "r")
CTEX_TEMP_TXT = f.read()
f.close()
# endregion

# region SVG
SVG_TEMP_FILE = ".\\templates\\svgTemp.svg"
SVG_TEMP_FILE = os.path.abspath(SVG_TEMP_FILE)

f = open(SVG_TEMP_FILE, "r")
SVG_TEMP_TXT = f.read()
f.close()
# endregion


# region Video
FRAMES_DIR = ".\\frames\\" + START_TIME
VIDEO_DIR = ".\\out\\" + START_TIME

FRAMES_DIR = os.path.abspath(FRAMES_DIR)
VIDEO_DIR = os.path.abspath(VIDEO_DIR)

os.mkdir(FRAMES_DIR)
os.mkdir(VIDEO_DIR)

# endregion
