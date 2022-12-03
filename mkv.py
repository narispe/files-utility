import subprocess
import os
from os import path
from natsort import natsorted
from beautifultable import BeautifulTable
from easygui import diropenbox
from pymkv import MKVFile
from functions import handle_input, load_titles_file


def get_mkv_info(files_paths, index=0):
    file_path = natsorted(files_paths)[index]
    mkv = MKVFile(file_path)
    table = BeautifulTable()
    table.columns.header = ["ID", "Tipo", "Idioma", "Nombre",
                            "Defecto", "Forzado"]
    audio_ids, audio_idioms, multip_audio_idioms = list(), list(), dict()
    subs_ids, subs_idioms, multip_subs_idioms = list(), list(), dict()
    tracks = mkv.get_track()
    for track in tracks:
        table.rows.append([track.track_id, track.track_type,
                           track.language, track.track_name,
                           track.default_track, track.forced_track])
        if track.track_type == "audio":
            audio_ids.append(track.track_id)
            if track.language not in audio_idioms:
                audio_idioms.append(track.language)
                multip_audio_idioms[track.language] = False
            else:
                multip_audio_idioms[track.language] = True
        if track.track_type == "subtitles":
            subs_ids.append(track.track_id)
            if track.language not in subs_idioms:
                subs_idioms.append(track.language)
                multip_subs_idioms[track.language] = False
            else:
                multip_subs_idioms[track.language] = True
    return {"table": table,
            "has_title": mkv.title is not None,
            "audio_ids": audio_ids,
            "audio_idioms": audio_idioms,
            "multip_audio_idioms": multip_audio_idioms,
            "subs_ids": subs_ids,
            "subs_idioms": subs_idioms,
            "multip_subs_idioms": multip_subs_idioms,
            "count": len(mkv.get_track())}


def track_choose(message, track_type, mkv_info):
    if track_type == "audio":
        ids = mkv_info["audio_ids"]
        idioms = mkv_info["audio_idioms"]
        multip_idioms = mkv_info["multip_audio_idioms"]
    elif track_type == "subtitles":
        ids = mkv_info["subs_ids"]
        idioms = mkv_info["subs_idioms"]
        multip_idioms = mkv_info["multip_subs_idioms"]
    choose = input(message)
    try:
        if choose.isdecimal():
            if int(choose) > max(ids):
                raise ValueError("El ID ingresado es mayor al máximo")
            if int(choose) < min(ids):
                raise ValueError("El ID ingresado es menor al mínimo")
        else:
            if choose not in idioms:
                raise ValueError("Ninguna pista presenta el idioma ingresado")
            if multip_idioms[choose]:
                raise ValueError("Existen varias pistas del idioma ingresado")
    except ValueError as error:
        print(error)
        return track_choose(message, track_type, mkv_info)
    else:
        if choose.isdecimal():
            return int(choose)
        return choose


def choose_mkv_modify(files_paths, dir_path):
    mkv_info = get_mkv_info(files_paths)
    print(mkv_info["table"])
    op_tracks = handle_input("[0] Cancelar\n"
                             "[1] Cambiar audio y subtítulos\n"
                             "[2] Cambiar solo audio\n"
                             "[3] Cambiar solo subtítulos\n"
                             "[4] Omitir\n"
                             ": ", 4, 0)
    audio_choose, subs_choose = None, None
    if op_tracks == 0:  # Omitir
        return None
    if op_tracks == 1 or op_tracks == 2:
        audio_choose = track_choose("Selecciona el audio: ",
                                    "audio", mkv_info)
    if op_tracks == 1 or op_tracks == 3:
        subs_choose = track_choose("Selecciona los subtítulos: ",
                                   "subtitles", mkv_info)

    op_titles = handle_input("[0] Cancelar\n"
                             "[1] Conservar títulos\n"
                             "[2] Borrar títulos\n"
                             "[3] Añadir títulos\n"
                             ": ", 3, 0)
    titles_list, delete_title = None, False
    if op_titles == 0:
        return None
    elif op_titles == 2:  # Borrar
        delete_title = True
    elif op_titles == 3:  # Añadir
        titles_list = load_titles_file(dir_path)

    output_dir = None
    if audio_choose is not None or subs_choose is not None:
        op_output = handle_input("[0] Cancelar\n"
                                 "[1] Sobreescribir\n"
                                 "[2] Salida por defecto\n"
                                 "[3] Seleccionar salida\n"
                                 ": ", 3)
        if op_output == 0:
            return None
        elif op_output == 2:  # Defecto
            output_dir = path.join(dir_path, "Output")
            if not path.exists(output_dir):
                os.mkdir(output_dir)
        elif op_output == 3:  # Elegir
            output_dir = diropenbox(msg="Seleciona carpeta para la salida",
                                    default=dir_path + "/")
    return {"audio": audio_choose,
            "subs": subs_choose,
            "delete_title": delete_title,
            "titles": titles_list,
            "output_dir": output_dir}


def process_mkv(file_path, audio_choose, subs_choose, title, output_dir):
    if title is not None and audio_choose is None and subs_choose is None:
        subprocess.run(["mkvpropedit", file_path, "-e",
                        "info", "-s", f"title={title}"],
                       capture_output=True)
    else:
        mkv = MKVFile(file_path)
        if title is not None:
            mkv.title = title
        tracks = mkv.get_track()
        audio_tracks = list(filter(lambda x: x.track_type == "audio",
                                   tracks))
        subs_tracks = list(filter(lambda x: x.track_type == "subtitles",
                                  tracks))
        if audio_choose is not None:
            for audio in audio_tracks:
                enabled = (audio.track_id == audio_choose
                           if type(audio_choose) is int
                           else audio.language == audio_choose)
                audio.default_track = enabled
                audio.forced_track = False
        if subs_choose is not None:
            for subs in subs_tracks:
                enabled = (subs.track_id == subs_choose
                           if type(subs_choose) is int
                           else subs.language == subs_choose)
                subs.default_track = enabled
                subs.forced_track = subs.forced_track
        mkv.mux(path.join(output_dir, path.basename(file_path)),
                silent=True)
