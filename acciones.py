import os
from natsort import natsorted
from funciones import manejar_entrada, obtener_paths, limpiar_info


def subir():
    carpetas = list(filter(lambda x: os.path.isdir(x), os.listdir()))
    for carpeta in carpetas:
        archivos = os.listdir(carpeta)
        for archivo in archivos:
            os.rename(os.path.join(carpeta, archivo), archivo)
        os.rmdir(carpeta)


def limpiar_nombres():
    ext = input("Extensión: ")
    paths = list(filter(lambda x: os.path.isfile(x) and os.path.splitext(x)[1] == ext,
                        os.listdir()))
    for path in natsorted(paths):
        nombre, ext = os.path.splitext(path)
        nuevo_nombre = limpiar_info(nombre, "[]")
        os.rename(path, nuevo_nombre + ext)


def renombrar_con_id():
    base = input("Nombre base (#=ID): ")
    i = int(input("ID inicial: "))
    paths = obtener_paths()
    for path in natsorted(paths):
        nombre, ext = os.path.splitext(path)
        nuevo_nombre = base.replace("#", f"{i:02d}")
        os.rename(path, nuevo_nombre + ext)
        i += 1


def reemplazar_en_nombre():
    reemplazar = input("Frase a reemplazar: ")
    reemplazo = input("Reemplazo: ")
    paths = obtener_paths()
    for path in paths:
        nuevo_nombre = path.replace(reemplazar, reemplazo)
        os.rename(path, nuevo_nombre)


# def editar_metadata():
#     archivos = list(filter(lambda x: os.path.isfile(x), os.listdir()))
#     for id_ in range(len(archivos[:-1])):  # A: A range of all the fields except the script
#         archivo = MP4(archivos[id_])          # A: Capture the file to edit
#         archivo['©nam'] = ""  # U: Take the file name and makeit the tittle
#         archivo['©ART'] = ""  # U: Edit the Autor
#         archivo['©alb'] = ""  # U: Edit the Album
#         archivo.pprint()
#         archivo.save()


# def distribuir():
#     identificadores = input("Identificador separados por \",\": ").split(",")
#     etiquetas = input("Etiquetas separados por \",\": ").split(",")
#     diccionario = dict()
#     for par in zip(identificadores, etiquetas):
#         id_, label = par
#         diccionario[id_] = label
#     archivos = list(filter(lambda x: os.path.isfile(x), os.listdir()))
#     for archivo in archivos:
#         identificador = list(filter(lambda x: x in archivo, diccionario.keys()))
#         if not identificador:
#             pass
#         else:
#             destino = diccionario[identificador[0]]
#             if not os.path.isdir(destino):
#                 os.mkdir(destino)
#             os.rename(archivo, os.path.join(destino, archivo))


# def redistribuir():
#     identificadores = input("Identificador separados por \",\": ").split(",")
#     etiquetas = input("Etiquetas separados por \",\": ").split(",")
#     diccionario = dict()
#     for par in zip(identificadores, etiquetas):
#         id_, label = par
#         diccionario[id_] = label
#     carpetas = list(filter(lambda x: os.path.isdir(x), os.listdir()))
#     for carpeta in carpetas:
#         archivos = list(filter(lambda x: os.path.isfile(os.path.join(carpeta, x)),
#                                os.listdir(carpeta)))
#         for archivo in archivos:
#             identificador = list(filter(lambda x: x in archivo, diccionario.keys()))
#             if not identificador:
#                 pass
#             else:
#                 destino = diccionario[identificador[0]]
#                 if not os.path.isdir(destino):
#                     os.mkdir(destino)
#                 os.rename(archivo, os.path.join(destino, archivo))
#         os.rmdir(carpeta)
