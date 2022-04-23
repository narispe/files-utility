from easygui import fileopenbox, diropenbox
import os
from os import path


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
        print("Se han ingresado más elementos"
              if len(input_.split(separator)) > length
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


def get_paths(dir_path=None, recursive=False, get_dirs=False, ext=None):
    if dir_path is None:
        dir_path = diropenbox(msg="Selecciona la carpeta input")
    if not recursive:
        paths = get_local_paths(dir_path, get_dirs, ext)
    else:
        paths = get_recursive_paths(dir_path, get_dirs, ext)
    if paths == []:
        if ext is not None:
            print(f"No se encontraron archivos de extensión {ext}")
        elif get_dirs:
            print("No se encontraron directorios")
        return None
    return paths


def get_local_paths(dir_path, get_dirs, ext):
    if not get_dirs:
        if ext is None:
            paths = filter(lambda path: path.isfile(path.join(dir_path, path)),
                           os.listdir(dir_path))
        else:
            paths = filter(lambda path: path.isfile(path.join(dir_path, path))
                           and path.splitext(path)[1] == ext,
                           os.listdir(dir_path))
    else:
        paths = filter(lambda path: path.isdir(path.join(dir_path, path)),
                       os.listdir(dir_path))
    return [path.join(dir_path, path) for path in paths]


def get_recursive_paths(dir_path, get_dirs, ext):
    paths = list()
    for root, dirs, files in os.walk(dir_path):
        if not get_dirs:
            if ext is not None:
                files = filter(lambda file: path.splitext(file)[1] == ext,
                               files)
            paths.extend([path.join(root, file) for file in files])
        else:
            paths.extend([path.join(root, dir_) for dir_ in dirs])
    return paths


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


def load_titles_file(dir_path):
    txt_file_path = fileopenbox("Selecciona el archivo .txt",
                                default=dir_path + "/*.txt")
    with open(txt_file_path, "r", encoding="utf-8") as txt_file:
        lines = txt_file.readlines()
    titles_names = list()
    for line in lines:
        line = line.strip()
        if not line.startswith("«") or not line.endswith("»"):
            line = line.replace("«", "").replace("»", "")
            line = "«" + line + "»"
        titles_names.append(line)
    op_id = handle_input("[1] Incluir índice\n"
                         "[2] Sin índice\n"
                         ": ", 2)
    if op_id == 1:
        start_index = check_input("Índice inicial: ", is_int=True)
        titles_list = [f"{i + start_index:02d}: {titles_names[i]}"
                       for i in range(len(titles_names))]
    elif op_id == 2:
        titles_list = titles_names
    return titles_list


if __name__ == "__main__":
    print(get_paths())
