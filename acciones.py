import os
import easygui
from tqdm import tqdm
from pymkv import MKVFile
from mutagen.mp4 import MP4
from natsort import natsorted
from funciones import obtener_paths, limpiar_info, obtener_tracks_info


def subir():
    carpetas = list(filter(lambda x: os.path.isdir(x), os.listdir()))
    for carpeta in tqdm(carpetas):
        archivos = os.listdir(carpeta)
        progreso = tqdm(archivos)
        progreso.set_description(carpeta)
        for archivo in progreso:
            try:
                os.rename(os.path.join(carpeta, archivo), archivo)
            except FileExistsError as error:
                print(f"El archivo {archivo} ya existía y no será movido")
        try:
            os.rmdir(carpeta)
        except Exception as error:
            print(type(error))


def limpiar_nombres():
    ext = input("Extensión: ")
    progreso = tqdm(list(filter(lambda x: os.path.isfile(x) and os.path.splitext(x)[1] == ext,
                    os.listdir())))
    for path in progreso:
        progreso.set_description(path)
        nombre, ext = os.path.splitext(path)
        nuevo_nombre = limpiar_info(nombre, "[]")
        os.rename(path, nuevo_nombre + ext)


def renombrar_con_id():
    base = input("Nombre base (#=ID): ")
    i = int(input("ID inicial: "))
    progreso = tqdm(natsorted(obtener_paths()))
    for path in progreso:
        progreso.set_description(path)
        nombre, ext = os.path.splitext(path)
        nuevo_nombre = base.replace("#", f"{i:02d}")
        os.rename(path, nuevo_nombre + ext)
        i += 1


def reemplazar_en_nombre():
    reemplazar = input("Frase a reemplazar: ")
    reemplazo = input("Reemplazo: ")
    progreso = tqdm(obtener_paths())
    for path in progreso:
        progreso.set_description(path)
        nuevo_nombre = path.replace(reemplazar, reemplazo)
        os.rename(path, nuevo_nombre)


def distribuir():
    # TO DO: check len, check existe carpetas
    etiquetas = input("Etiquetas separados por \",\": ").split(",")
    categorias = input("categorias respectivas separadas por \",\": ").split(",")
    destinos = dict()
    for par in zip(etiquetas, categorias):
        etiqueta, carpeta = par
        destinos[etiqueta] = carpeta
    progeso = tqdm(list(filter(lambda x: os.path.isfile(x), os.listdir())))
    for path in progeso:
        progeso.set_description(path)
        for etiqueta in etiquetas:
            if etiqueta in path:
                try:
                    os.rename(path, os.path.join(destinos[etiqueta], path))
                except FileNotFoundError:
                    os.mkdir(destinos[etiqueta])
                    os.rename(path, os.path.join(destinos[etiqueta], path))
                break


def redistribuir():
    etiquetas = input("Etiquetas separados por \",\": ").split(",")
    categorias = input("categorias respectivas separadas por \",\": ").split(",")
    destinos = dict()
    for par in zip(etiquetas, categorias):
        etiqueta, carpeta = par
        destinos[etiqueta] = carpeta
    carpetas = list(filter(lambda x: os.path.isdir(x), os.listdir()))
    progreso = tqdm(carpetas)
    for carpeta in progreso:
        progreso.set_description(carpeta)
        paths = list(filter(lambda x: os.path.isfile(os.path.join(carpeta, x)),
                            os.listdir(carpetas)))
        for path in paths:
            for etiqueta in etiquetas:
                if etiqueta in path:
                    try:
                        os.rename(path, os.path.join(destinos[etiqueta], path))
                    except FileNotFoundError:
                        os.mkdir(destinos[etiqueta])
                        os.rename(path, os.path.join(destinos[etiqueta], path))
                    break
        try:
            os.rmdir(carpeta)
        except Exception as error:
            print(f"La carpeta {carpeta} todavía contiene archivos")


def editar_metadata():
    archivos = list(filter(lambda x: os.path.isfile(x), os.listdir()))
    for id_ in range(len(archivos[:-1])):  # A: A range of all the fields except the script
        archivo = MP4(archivos[id_])          # A: Capture the file to edit
        archivo['©nam'] = ""  # U: Take the file name and makeit the tittle
        archivo['©ART'] = ""  # U: Edit the Autor
        archivo['©alb'] = ""  # U: Edit the Album
        archivo.pprint()
        archivo.save()


def cambiar_idioma():
    paths = list(filter(lambda x: os.path.isfile(x) and os.path.splitext(x)[1] == ".mkv",
                        os.listdir()))
    if paths:
        tabla_tracks, subs_multiples = obtener_tracks_info(paths[0])
        print(tabla_tracks)
        idioma_audio = input("Idioma de audio: ")
        idioma_subs = input("Idioma de subtítulos: ")
        if subs_multiples:
            subs_id = int(input("ID subtítulos: "))
        output_dir = easygui.diropenbox(msg="Selecciona la carpeta output")
        progreso = tqdm(paths)
        for path in progreso:
            progreso.set_description(path)
            mkv = MKVFile(file_path=path)
            tracks = mkv.get_track()
            audios = list(filter(lambda x: x.track_type == "audio",
                          tracks))
            subs = list(filter(lambda x: x.track_type == "subtitles",
                        tracks))
            if idioma_audio in map(lambda x: x.language, audios):
                for audio in audios:
                    audio.default_track = (audio.language == idioma_audio)
            if idioma_subs in map(lambda x: x.language, subs):
                for sub in subs:
                    if subs_multiples:
                        enabled = (sub.track_id == subs_id)
                    else:
                        enabled = (sub.language == idioma_subs)
                    sub.forced_track = enabled
                    sub.default_track = enabled
            mkv.mux(os.path.join(output_dir, path), silent=True)


if __name__ == "__main__":
    pass
