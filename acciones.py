import os
import easygui
from tqdm import tqdm
from pymkv import MKVFile
from mutagen.mp4 import MP4
from natsort import natsorted
from funciones import obtener_paths, limpiar_info


def subir():
    carpetas = list(filter(lambda x: os.path.isdir(x), os.listdir()))
    for carpeta in tqdm(carpetas):
        archivos = os.listdir(carpeta)
        for archivo in tqdm(archivos):
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
    paths = list(filter(lambda x: os.path.isfile(x) and os.path.splitext(x)[1] == ext,
                        os.listdir()))
    for path in tqdm(natsorted(paths)):
        nombre, ext = os.path.splitext(path)
        nuevo_nombre = limpiar_info(nombre, "[]")
        os.rename(path, nuevo_nombre + ext)


def renombrar_con_id():
    base = input("Nombre base (#=ID): ")
    i = int(input("ID inicial: "))
    paths = obtener_paths()
    for path in tqdm(natsorted(paths)):
        nombre, ext = os.path.splitext(path)
        nuevo_nombre = base.replace("#", f"{i:02d}")
        os.rename(path, nuevo_nombre + ext)
        i += 1


def reemplazar_en_nombre():
    reemplazar = input("Frase a reemplazar: ")
    reemplazo = input("Reemplazo: ")
    paths = obtener_paths()
    for path in tqdm(paths):
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
    archivos = list(filter(lambda x: os.path.isfile(x), os.listdir()))
    for archivo in tqdm(archivos):
        for etiqueta in etiquetas:
            if etiqueta in archivo:
                try:
                    os.rename(archivo, os.path.join(destinos[etiqueta], archivo))
                except FileNotFoundError:
                    os.mkdir(destinos[etiqueta])
                    os.rename(archivo, os.path.join(destinos[etiqueta], archivo))
                break


def redistribuir():
    etiquetas = input("Etiquetas separados por \",\": ").split(",")
    categorias = input("categorias respectivas separadas por \",\": ").split(",")
    destinos = dict()
    for par in zip(etiquetas, categorias):
        etiqueta, carpeta = par
        destinos[etiqueta] = carpeta
    carpetas = list(filter(lambda x: os.path.isdir(x), os.listdir()))
    for carpeta in tqdm(carpetas):
        archivos = list(filter(lambda x: os.path.isfile(os.path.join(carpeta, x)),
                               os.listdir(carpetas)))
        for archivo in tqdm(archivos):
            for etiqueta in etiquetas:
                if etiqueta in archivo:
                    try:
                        os.rename(archivo, os.path.join(destinos[etiqueta], archivo))
                    except FileNotFoundError:
                        os.mkdir(destinos[etiqueta])
                        os.rename(archivo, os.path.join(destinos[etiqueta], archivo))
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
        idioma_audio = input("Idioma de audio: ")
        idioma_subs = input("Idioma de subtítulos: ")
        etiqueta_subs = input("Etiqueta subs (\"\" omitir): ")
        print("Selecciona la carpeta de salida")
        output_dir = easygui.diropenbox()
        i = 1
        print("INICIO")
        for path in tqdm(paths):
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
                    if etiqueta_subs:
                        enabled = (sub.language == idioma_subs and etiqueta_subs in sub.track_name)
                    else:
                        enabled = (sub.language == idioma_subs)
                    sub.forced_track = enabled
                    sub.default_track = enabled
            mkv.mux(os.path.join(output_dir, path), silent=True)
            print(f"{os.path.join(output_dir, path)} LISTO")
            i += 1


if __name__ == "__main__":
    pass
