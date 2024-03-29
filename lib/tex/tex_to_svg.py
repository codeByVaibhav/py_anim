import hashlib

from lib.file.constants import *


def tex_hash(expression, template_tex_file_body):
    id_str = str(expression + template_tex_file_body)
    hasher = hashlib.sha256()
    hasher.update(id_str.encode())
    # Truncating at 16 bytes for cleanliness
    return hasher.hexdigest()[:16]


def tex_to_svg_file(expression, template_tex_file_body=TEX_TEMP_FILE):
    tex_file = generate_tex_file(expression, template_tex_file_body)
    dvi_file = tex_to_dvi(tex_file)
    return dvi_to_svg(dvi_file)


def generate_tex_file(expression, template_tex_file_body):
    result = os.path.join(
        TEX_DIR,
        tex_hash(expression, template_tex_file_body)
    ) + ".tex"
    if not os.path.exists(result):
        # print("Writing \"%s\" to %s" % ("".join(expression), result))
        new_body = TEX_TEMP_TXT.replace(TEXT_TO_REPLACE, expression)
        with open(result, "w", encoding="utf-8") as outfile:
            outfile.write(new_body)
    return result


def tex_to_dvi(tex_file):
    result = tex_file.replace(".tex", ".dvi")
    if not os.path.exists(result):
        commands = [
            "latex",
            "-interaction=batchmode",
            "-halt-on-error",
            f'"{tex_file}"',
            f'-output-directory="{TEX_DIR}"',
            ">",
            os.devnull
        ]
        command = " ".join(commands)
        exit_code = os.system(command)
        if exit_code != 0:
            log_file = tex_file.replace(".tex", ".log")
            raise Exception(
                ("Latex error converting to dvi. " if not TEX_USE_CTEX
                 else "Xelatex error converting to xdv. ") +
                "See log output above or the log file: %s" % log_file)
    return result


def dvi_to_svg(dvi_file, regen_if_exists=False):
    """
    Converts a dvi, which potentially has multiple slides, into a
    directory full of enumerated pngs corresponding with these slides.
    Returns a list of PIL Image objects for these images sorted as they
    where in the dvi
    """
    result = dvi_file.replace(".dvi" if not TEX_USE_CTEX else ".xdv", ".svg")
    if not os.path.exists(result):
        commands = [
            "dvisvgm",
            f'"{dvi_file}"',
            "-n",
            "-v",
            "0",
            "-o",
            f'"{result}"',
            ">",
            os.devnull
        ]
        command = " ".join(commands)
        os.system(command)
    return result


if __name__ == "__main__":
    text = input("Enter your text: ")
    out = tex_to_svg_file(text, TEX_TEMP_FILE)
    print(out)
    os.system(out)
