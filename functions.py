from easygui import fileopenbox, diropenbox
import os


def handle_input(message, max_option, min_option=0) -> int:
    op = input(message)
    try:
        if not op.isdecimal():
            raise TypeError("Debes ingresar un número de las opciones disponibles")
        if int(op) > max_option:
            raise ValueError("El valor ingresado es mayor al máximo de las opciones disponibles")
        if int(op) < min_option:
            raise ValueError("El valor ingresado es menor al máximo de las opciones disponibles")
    except TypeError as error:
        print(error)
        return handle_input(message, max_option, min_option)
    except ValueError as error:
        print(error)
        return handle_input(message, max_option, min_option)
    else:
        return int(op)


def check_input(message, is_int=False, form=None, content=None,
                elem_list=None, length=None, separator=",", is_file=False):  # TO COMPLETE
    input_ = input(message)
    if length is not None:
        if len(input_.split(separator)) == length:
            return input_.split(separator)
        print("Se han ingresado más elementos" if len(input_.split(separator)) > length
              else "Se han ingresado menos elementos")
    if is_int:
        if input_.isdecimal():
            if elem_list is not None and int(input_) in elem_list:
                return int(input_)
            return int(input_)
        print("No se ha ingresado un dígito")
    if content is not None and not is_file:
        if content in input_:
            return input_
        print(f"No se ha incluido {content}")
    if elem_list is not None:
        if input_ in elem_list:
            return input_
        format_ = ", ".join(elem_list)
        print(f"Debes ingresar alguna de las siguientes opciones: {format_}")
    if form is not None:  # Check plantilla
        return input_
    if is_file:
        if input_.count(".") == 1:
            input_file, input_ext = input_.split(".")
            return (input_file, "." + input_ext)
    return check_input(message, is_int, form, content, elem_list, length, separator)


def get_paths(dir_path=None, get_dirs=False, ext=None):
    if dir_path is None:
        dir_path = diropenbox(msg="Selecciona la carpeta input")
    if not get_dirs:
        if ext is None:
            basenames = list(filter(lambda path: os.path.isfile(os.path.join(dir_path, path)),
                                    os.listdir(dir_path)))
        else:
            basenames = list(filter(lambda path: os.path.isfile(os.path.join(dir_path, path))
                                    and os.path.splitext(path)[1] == ext,
                                    os.listdir(dir_path)))
    else:
        basenames = list(filter(lambda path: os.path.isdir(os.path.join(dir_path, path)),
                                os.listdir(dir_path)))
    if not basenames:
        return None
    abs_paths = [os.path.join(dir_path, basename) for basename in basenames]
    return abs_paths  # abs paths


def clear_name(str_in, envir="[]"):
    envir_open, envir_close = envir
    str_out = ""
    deleting = False
    i = 0
    for i in range(len(str_in)):
        character = str_in[i]
        if character == envir_open:
            deleting = True
        if not deleting:
            str_out += character
        if character == " " and str_in[i-1] == envir_close:
            deleting = False
    return str_out.strip()


def handle_mp4():
    # Text values
    # mp4["@nam"] = ""  # track title
    # mp4["@alb"] = ""  # album
    # mp4["@ART"] = ""  # artist
    # mp4["aART"] = ""  # album artist
    # mp4["@wrt"] = ""  # composer
    # mp4["@day"] = ""  # year
    # mp4["@cmt"] = ""  # comment
    # mp4["desc"] = ""  # description (usually used in podcasts)
    # mp4["purd"] = ""  # purchase date
    # mp4["@grp"] = ""  # grouping
    # mp4["@gen"] = ""  # genre
    # mp4["@lyr"] = ""  # lyrics
    # mp4["purl"] = ""  # podcast URL
    # mp4["egid"] = ""  # podcast episode GUID
    # mp4["catg"] = ""  # podcast category
    # mp4["keyw"] = ""  # podcast keywords
    # mp4["@too"] = ""  # encoded by
    # mp4["cprt"] = ""  # copyright
    # mp4["soal"] = ""  # album sort order
    # mp4["soaa"] = ""  # album artist sort order
    # mp4["soar"] = ""  # artist sort order
    # mp4["sonm"] = ""  # title sort order
    # mp4["soco"] = ""  # composer sort order
    # mp4["sosn"] = ""  # show sort order
    # mp4["tvsh"] = ""  # show name
    # mp4["@wrk"] = ""  # work
    # mp4["@mvn"] = ""  # movement
    # # Boolean values
    # mp4["cpil"] = ""  # part of a compilation
    # mp4["pgap"] = ""  # part of a gapless album
    # mp4["pcst"] = ""  # podcast (iTunes reads this only on import)
    # # Tuples of ints:
    # mp4["trkn"] = ""  # track number, total tracks
    # mp4["disk"] = ""  # disc number, total discs
    # # Integer values:
    # mp4["tmpo"] = ""  # tempo/BPM
    # mp4["@mvc"] = ""  # Movement Count
    # mp4["@mvi"] = ""  # Movement Index
    # mp4["shwm"] = ""  # work/movement
    # mp4["stik"] = ""  # Media Kind
    # mp4["hdvd"] = ""  # HD Video
    # mp4["rtng"] = ""  # Content Rating
    # mp4["tves"] = ""  # TV Episode
    # mp4["tvsn"] = ""  # TV Season
    pass


def get_size_format(b, factor=1024, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


if __name__ == "__main__":
    print(get_paths())
