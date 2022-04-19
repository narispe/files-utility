from pymkv import MKVFile
from easygui import fileopenbox, diropenbox
from beautifultable import BeautifulTable
import os
from functions import get_paths, handle_input, check_input
from natsort import natsorted


def get_mkv_info(path=None):
    if path is None:
        file_path = fileopenbox()
    else:
        if os.path.isfile(path):
            file_path = path
        elif os.path.isdir(path):
            files_paths = get_paths(path, ext=".mkv")
            if files_paths is None:
                return None
            file_path = natsorted(files_paths)[0]
    mkv = MKVFile(file_path)
    table = BeautifulTable()
    table.column_headers = ["ID", "Tipo", "Idioma", "Nombre",
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


def choose_mkv_modify(dir_path=None):
    mkv_info = get_mkv_info(dir_path)
    if mkv_info is None:
        print("No existen mkv en la carpeta")
        return None
    else:
        audio_choose = None
        subs_choose = None
        print(mkv_info["table"])
        op_tracks = handle_input("[0] Cancelar\n"
                                 "[1] Cambiar audio y subtítulos\n"
                                 "[2] Cambiar solo audio\n"
                                 "[3] Cambiar solo subtítulos\n"
                                 "[4] Omitir\n"
                                 ": ",
                                 4, 0)
        if op_tracks == 0:  # Omitir
            return None
        elif op_tracks == 1:  # Audio y Subs
            audio_choose = track_choose("Selecciona el audio: ",
                                        "audio", mkv_info)
            subs_choose = track_choose("Selecciona los subtítulos: ",
                                       "subtitles", mkv_info)
        elif op_tracks == 2:  # Audio
            audio_choose = track_choose("Selecciona el audio: ",
                                        "audio", mkv_info)
        elif op_tracks == 3:  # Subs
            subs_choose = track_choose("Selecciona los subtítulos: ",
                                       "subtitles", mkv_info)
        elif op_tracks == 4:  # Omitir
            pass

        op_titles = handle_input("[0] Cancelar\n"
                                 "[1] Conservar títulos\n"
                                 "[2] Borrar títulos\n"
                                 "[3] Añadir títulos\n"
                                 ": ",
                                 3, 0)
        titles_list = None
        if op_titles == 0:
            return None
        elif op_titles == 1:  # Conservar
            delete_title = False
        elif op_titles == 2:  # Borrar
            delete_title = True
        elif op_titles == 3:  # Añadir
            delete_title = False
            op_in = handle_input("[1] Archivo .txt de títulos por episodio\n"
                                 "[2] Ingreso manual\n"
                                 ": ",
                                 2)
            if op_in == 1:  # Archivo
                txt_file_path = fileopenbox("Selecciona el archivo .txt",
                                            default="*.txt")
                with open(txt_file_path, "r", encoding="utf-8") as txt_file:
                    lines = txt_file.readlines()
                titles_names = list()
                for line in lines:
                    line = line.strip()
                    if not line.startswith("«") or not line.endswith("»"):
                        line = line.replace("«", "").replace("»", "")
                        line = "«" + line + "»"
                    titles_names.append(line)
                start_index = check_input("Índice inicial: ", is_int=True)
                titles_list = [f"{i + start_index:02d} - {titles_names[i]}"
                               for i in range(len(titles_names))]
            elif op_in == 2:  # Manual
                titles_list = check_input("Ingresa los títulos separados por \",\": ",
                                          length=len(get_paths(dir_path, ext=".mkv")))

        op_output = handle_input("[0] Cancelar\n"
                                 "[1] Salida por defecto\n"
                                 "[2] Seleccionar salida\n"
                                 ": ",
                                 2, 0)
        if op_output == 0:
            return None
        elif op_output == 1:  # Defecto
            output_dir = os.path.join(dir_path, "Output")
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
        elif op_output == 2:  # Elegir
            output_dir = diropenbox("Seleciona carpeta para la salida")

        return {"audio": audio_choose,
                "subs": subs_choose,
                "delete_title": delete_title,
                "titles": titles_list,
                "output_dir": output_dir}
