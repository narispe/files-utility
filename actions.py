import os
from os import path
from easygui import diropenbox
from tqdm import tqdm
from natsort import natsorted
from mutagen.mp4 import MP4
from functions import get_paths, clear_name, get_size_format
from mkv import choose_mkv_modify, process_mkv
from pdf import init_pdf_edit, compress_file, choose_pdf_modify


def raise_files(base_path, remove):
    dirs = get_paths(base_path, get_dirs=True)
    if dirs is None:
        return None
    for dir_path in tqdm(dirs):
        files_paths = get_paths(dir_path)
        if files_paths is not None:
            for file_path in files_paths:
                try:
                    os.rename(file_path, path.join(base_path,
                                                   path.basename(file_path)))
                except FileExistsError as error:
                    if remove:
                        os.remove(file_path)
        try:
            os.rmdir(dir_path)
        except OSError as error:
            pass


def clear_files_names(base_path, extension):
    files_paths = get_paths(base_path, ext=extension)
    if files_paths is None:
        return None
    for file_path in tqdm(files_paths):
        new_file_name = clear_name(path.splitext(path.basename(file_path))[0])
        new_file_path = path.join(base_path, new_file_name + extension)
        os.rename(file_path, new_file_path)


def enumerate_files(base_path, name_template, current_id, extension):
    files_paths = get_paths(base_path, ext=extension)
    if files_paths is None:
        return None
    for file_path in tqdm(natsorted(files_paths)):
        new_file_name = name_template.replace("#", f"{current_id:02d}")
        os.rename(file_path, path.join(base_path, new_file_name + extension))
        current_id += 1


def rename_files(base_path, searched_sentence, replaced_sentence):
    files_paths = get_paths(base_path)
    if files_paths is None:
        return None
    for file_path in tqdm(files_paths):
        file_name, extension = path.splitext(path.basename(file_path))
        new_file_name = path.basename(file_name).replace(searched_sentence,
                                                         replaced_sentence)
        os.rename(file_path, path.join(base_path, new_file_name + extension))


def distribute(base_path, labels, categories):
    files_paths = get_paths(base_path)
    if files_paths is None:
        return None
    destiny_dirs = {label: category for (label, category)
                    in zip(labels, categories)}
    for file_path in tqdm(files_paths):
        for label in labels:
            if label in path.basename(file_path) and not \
                    any(map(lambda x: x in path.basename(file_path),
                            filter(lambda x: x != label,
                                   labels))):
                new_file_path = path.join(base_path, destiny_dirs[label],
                                          path.basename(file_path))
                try:
                    os.rename(file_path, new_file_path)
                except FileNotFoundError:
                    os.mkdir(path.join(base_path, destiny_dirs[label]))
                    os.rename(file_path, new_file_path)
                break


def re_distribute(base_path, labels, categories):
    destiny_dirs = {label: category for (label, category)
                    in zip(labels, categories)}
    dirs_paths = get_paths(base_path, get_dirs=True)
    if dirs_paths is None:
        return None
    for dir_path in tqdm(dirs_paths):
        files_paths = get_paths(dir_path)
        for file_path in tqdm(files_paths):
            for label in labels:
                if label in path.basename(file_path):
                    new_file_path = path.join(base_path, destiny_dirs[label],
                                              path.basename(file_path))
                    try:
                        os.rename(file_path, new_file_path)
                    except FileNotFoundError:
                        os.mkdir(destiny_dirs[label])
                        os.rename(file_path, new_file_path)
                    break


def edite_mkv(base_path):
    files_paths = get_paths(base_path, ext=".mkv")
    if files_paths is None:
        return None
    choose = choose_mkv_modify(files_paths, base_path)
    if choose is None:
        return None
    errors = list()
    for file_path in tqdm(natsorted(files_paths)):
        if choose["titles"] is not None:
            title = choose["titles"][files_paths.index(file_path)]
        elif choose["delete_title"]:
            title = ""
        else:
            title = None
        try:
            process_mkv(file_path, choose["audio"], choose["subs"], title,
                        choose["output_dir"])
        except Exception as error:
            errors.append(path.splitext(path.basename(file_path))[0])
    if len(errors) == 0:
        print("Se procesaron correctamente todos los archivos")
    else:
        print("Los siguientes archivos tuvieron errores al procesarse")
        print("\n".join(errors))


def edite_mp4(base_path):
    files_paths = get_paths(base_path, ext=".mp4")
    if files_paths is None:
        return None
    for file_path in tqdm(natsorted(files_paths)):
        mp4 = MP4(file_path)


def edite_pdf(base_path):
    choose = choose_pdf_modify()
    if choose is None:
        return None
    if choose["action"] == "compress":
        files_paths = get_paths(base_path, ext=".pdf")
    elif choose["action"] == "recursive_compress":
        files_paths = get_paths(base_path, recursive=True, ext=".pdf")
    dir_initial_size = 0
    dir_compressed_size = 0
    init_pdf_edit()
    for file_path in tqdm(natsorted(files_paths)):
        file_name = path.basename(file_path)
        try:
            if choose["output_dir"] is None:
                output_file_path = file_path
            elif choose["action"] == "recursive_compress":
                common = path.commonpath([choose["output_dir"], file_path])
                file_path_rel = file_path.replace(common, "").strip("\\")
                output_file_path = os.path.join(choose["output_dir"],
                                                file_path_rel)
                if not path.exists(path.dirname(output_file_path)):
                    os.makedirs(path.dirname(output_file_path))
            elif choose["action"] == "compress":
                output_file_path = path.join(choose["output_dir"], file_name)
            initial_size, compressed_size = compress_file(file_path,
                                                          output_file_path)
        except TypeError:
            continue
        else:
            dir_initial_size += initial_size
            dir_compressed_size += compressed_size
    ratio = (dir_compressed_size - dir_initial_size) / dir_initial_size
    print(f"Tamaño inicial: {get_size_format(dir_initial_size)}")
    print(f"Tamaño final: {get_size_format(dir_compressed_size)}")
    print(f"Razón de reducción: {ratio:.2%}%")


def search_files(base_path, extension, output_file):
    files_paths = get_paths(base_path, recursive=True, ext=extension)
    if files_paths is None:
        return None
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(files_paths))


if __name__ == "__main__":
    pass
