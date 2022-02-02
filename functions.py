import os
import easygui
from natsort import natsorted
from tqdm import tqdm
from pymkv import MKVFile
from beautifultable import BeautifulTable


def handle_input(message, max_option, min_option=0) -> int:
    op = input(message)
    while not op.isdecimal() or int(op) > max_option or int(op) < min_option:
        op = input(message)
    return int(op)


def get_paths(dir_path, get_dirs=False, ext=None):
    if dir_path is None:
        dir_path = easygui.diropenbox(msg="Selecciona la carpeta input")
    if not get_dirs:
        if ext is None:
            basenames = list(filter(lambda file: os.path.isfile(os.path.join(dir_path, file)),
                                    os.listdir(dir_path)))
            print(basenames)
        else:
            basenames = list(filter(lambda file: os.path.isfile(os.path.join(dir_path, file))
                                    and os.path.splitext(file)[1] == ext,
                                    os.listdir(dir_path)))
    else:
        basenames = list(filter(lambda x: os.path.isdir(x),
                                os.listdir(dir_path)))
    if not basenames:
        return None
    return [os.path.join(dir_path, basename) for basename in basenames]  # abs paths


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


def get_mkv_info(dir_path=None):
    if dir_path is None:
        file_path = easygui.fileopenbox()
    else:
        files_paths = get_paths(dir_path, ext=".mkv")
        if files_paths is None:
            return None
        file_path = natsorted(files_paths)[0]
    mkv = MKVFile(file_path)
    table = BeautifulTable()
    table.column_headers = ["ID", "Tipo", "Idioma", "Nombre", "Defecto", "Forzado"]
    audio_ids, audio_idioms, multip_idiom_audio = list(), list(), False
    subs_ids, subs_idioms, multip_idiom_subs = list(), list(), False
    for track in mkv.get_track():
        table.rows.append([track.track_id, track.track_type, track.language, track.track_name,
                           track.default_track, track.forced_track])
        if track.track_type == "audio":
            audio_ids.append(track.track_id)
            if track.language not in audio_idioms:
                audio_idioms.append(track.language)
            else:
                multip_idiom_audio = True
        if track.track_type == "subtitles":
            subs_ids.append(track.track_id)
            if track.language not in subs_idioms:
                subs_idioms.append(track.language)
            else:
                multip_idiom_subs = True
    info = {"table": table,
            "has_title": mkv.title is not None,
            "audio_ids": audio_ids,
            "audio_idioms": audio_idioms,
            "multip_idiom_audio": multip_idiom_audio,
            "subs_ids": subs_ids,
            "subs_idioms": subs_idioms,
            "multip_idiom_subs": multip_idiom_subs}
    return info


if __name__ == "__main__":
    pass
