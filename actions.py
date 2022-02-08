from tqdm import tqdm
from pymkv import MKVFile
from natsort import natsorted
from mutagen.mp4 import MP4
import os
from functions import get_paths, clear_name


def raise_files(base_path):
    dirs = get_paths(base_path, get_dirs=True)
    for dir_path in tqdm(dirs):
        files_paths = get_paths(dir_path)
        pgb = tqdm(files_paths)
        pgb.set_description(os.path.basename(dir_path))
        for file_path in pgb:
            try:
                os.rename(file_path, os.path.join(base_path, file_path))
            except FileExistsError as error:
                print(f"El archivo {os.path.basename(file_path)} ya existía y no será movido")
        try:
            os.rmdir(dir_path)
        except Exception as error:
            print(type(error))


def clear_files_names(base_path, extension):
    files_paths = get_paths(base_path, ext=extension)
    pgb = tqdm(files_paths)
    pgb.set_description(os.path.basename(base_path))
    for file_path in pgb:
        new_file_name = clear_name(os.path.basename(file_path))
        new_file_path = os.path.join(base_path, new_file_name + extension)
        os.rename(file_path, new_file_path)


def enumerate_files(base_path, name_template, current_id, extension):
    files_paths = get_paths(base_path, ext=extension)
    pgb = tqdm(natsorted(files_paths))
    pgb.set_description(os.path.basename(base_path))
    for file_path in pgb:
        new_basename = name_template.replace("#", f"{current_id:02d}") + extension
        os.rename(file_path, os.path.join(base_path, new_basename))
        current_id += 1


def rename_files(base_path, searched_sentence, replaced_sentence):
    files_paths = get_paths(base_path)
    pgb = tqdm(files_paths)
    pgb.set_description(os.path.basename(base_path))
    for file_path in pgb:
        new_basename = os.path.basename(file_path).replace(searched_sentence,
                                                           replaced_sentence)
        os.rename(file_path, os.path.join(base_path, new_basename))


def distribute(base_path, labels, categories):
    destiny_dirs = {label: category for (label, category) in zip(labels, categories)}
    files_paths = get_paths(base_path)
    for file_path in tqdm(files_paths):
        for label in labels:
            if label in os.path.basename(file_path):
                new_file_path = os.path.join(base_path, destiny_dirs[label],
                                             os.path.basename(file_path))
                try:
                    os.rename(file_path, new_file_path)
                except FileNotFoundError:
                    os.mkdir(destiny_dirs[label])
                    os.rename(file_path, new_file_path)
                break


def re_distribute(base_path, labels, categories):
    destiny_dirs = {label: category for (label, category) in zip(labels, categories)}
    dirs_paths = get_paths(base_path, get_dirs=True)
    pgb = tqdm(dirs_paths)
    for dir_path in pgb:
        pgb.set_description(os.path.basename(dir_path))
        files_paths = get_paths(dir_path)
        for file_path in tqdm(files_paths):
            for label in labels:
                if label in os.path.basename(file_path):
                    new_file_path = os.path.join(base_path, destiny_dirs[label],
                                                 os.path.basename(file_path))
                    try:
                        os.rename(file_path, new_file_path)
                    except FileNotFoundError:
                        os.mkdir(destiny_dirs[label])
                        os.rename(file_path, new_file_path)
                    break


def edite_mkv(base_path, output_path, audio_choose, subs_choose, delete_title=False, titles=None):
    files_paths = get_paths(base_path, ext=".mkv")
    pgb = tqdm(natsorted(files_paths))
    errors = list()
    for file_path in pgb:
        pgb.set_description(os.path.basename(file_path))
        mkv = MKVFile(file_path)
        tracks = mkv.get_track()
        audio_tracks = list(filter(lambda x: x.track_type == "audio",
                                   tracks))
        subs_tracks = list(filter(lambda x: x.track_type == "subtitles",
                                  tracks))

        if delete_title:
            mkv.title = ""
        elif titles is not None:
            mkv.title = titles[files_paths.index(file_path)]

        if len(audio_tracks) > 1 and audio_choose is not None:
            for audio in audio_tracks:
                enabled = (audio.track_id == audio_choose if type(audio_choose) is int
                           else audio.language == audio_choose)
                audio.default_track = enabled
                audio.forced_track = False

        if len(subs_tracks) > 1 and subs_choose is not None:
            for subs in subs_tracks:
                enabled = (subs.track_id == subs_choose if type(subs_choose) is int
                           else subs.language == subs_choose)
                subs.default_track = enabled
                # sub.forced_track = enabled

        try:
            mkv.mux(os.path.join(output_path, os.path.basename(file_path)),
                    silent=True)
        except Exception as error:
            errors.append(os.path.basename(file_path))

    if len(errors) == 0:
        print("Se procesaron correctamente todos los archivos")
    else:
        print("Los siguientes archivos tuvieron errores al procesarse")
        print("\n".join(errors))


def edite_mp4(base_path):
    files_paths = get_paths(base_path, ext=".mp4")
    pgb = tqdm(natsorted(files_paths))
    pgb.set_description(os.path.basename(base_path))
    for file_path in pgb:
        mp4 = MP4(file_path)


if __name__ == "__main__":
    x = "xcx"
    x.center(1, )
