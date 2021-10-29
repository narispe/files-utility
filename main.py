import os
from mutagen.mp4 import MP4
from natsort import natsorted


def entrada(mensaje, n_max):
    op = input(mensaje)
    while not op.isdecimal or int(op) > n_max:
        op = input(mensaje)
    return int(op)


def seleccionar_filtro():
    op = entrada("[1] Archivo\n[2] Carpeta\n: ", 2)
    return os.path.isfile if op == 1 else os.path.isdir


def reemplazar_en_nombre():
    reemplazar = input("Frase a reemplazar: ")
    reemplazo = input("Reemplazo: ")
    filtro = seleccionar_filtro()
    paths = list(filter(lambda x: filtro(x), os.listdir()))
    for path in paths:
        nuevo_nombre = path.replace(reemplazar, reemplazo)
        os.rename(path, nuevo_nombre)


def renombrar_con_id():
    base = input("Base con # = id:\n")
    filtro = seleccionar_filtro()
    if filtro == os.path.isfile:
        ext = input("Extensión: ")
    paths = list(filter(lambda x: filtro(x) and os.path.splitext(x)[1] == ext,
                        os.listdir()))
    i = 1
    for path in natsorted(paths):
        nombre, ext = os.path.splitext(path)
        nuevo_nombre = base.replace("#", f"{i:02d}")
        os.rename(path, nuevo_nombre + ext)
        i += 1


def editar_Media_Data():
    archivos = list(filter(lambda x: os.path.isfile(x), os.listdir()))
    for id_ in range(len(archivos[:-1])):  # A: A range of all the fields except the script
        archivo = MP4(archivos[id_])          # A: Capture the file to edit
        archivo['©nam'] = ""  # U: Take the file name and makeit the tittle
        archivo['©ART'] = ""  # U: Edit the Autor
        archivo['©alb'] = ""  # U: Edit the Album
        archivo.pprint()
        archivo.save()


def distribuir():
    identificadores = input("Identificador separados por \",\": ").split(",")
    etiquetas = input("Etiquetas separados por \",\": ").split(",")
    diccionario = dict()
    for par in zip(identificadores, etiquetas):
        id_, label = par
        diccionario[id_] = label
    archivos = list(filter(lambda x: os.path.isfile(x), os.listdir()))
    for archivo in archivos:
        identificador = list(filter(lambda x: x in archivo, diccionario.keys()))
        if not identificador:
            pass
        else:
            destino = diccionario[identificador[0]]
            if not os.path.isdir(destino):
                os.mkdir(destino)
            os.rename(archivo, os.path.join(destino, archivo))


def redistribuir():
    identificadores = input("Identificador separados por \",\": ").split(",")
    etiquetas = input("Etiquetas separados por \",\": ").split(",")
    diccionario = dict()
    for par in zip(identificadores, etiquetas):
        id_, label = par
        diccionario[id_] = label
    carpetas = list(filter(lambda x: os.path.isdir(x), os.listdir()))
    for carpeta in carpetas:
        archivos = list(filter(lambda x: os.path.isfile(os.path.join(carpeta, x)),
                               os.listdir(carpeta)))
        for archivo in archivos:
            identificador = list(filter(lambda x: x in archivo, diccionario.keys()))
            if not identificador:
                pass
            else:
                destino = diccionario[identificador[0]]
                if not os.path.isdir(destino):
                    os.mkdir(destino)
                os.rename(archivo, os.path.join(destino, archivo))
        os.rmdir(carpeta)


def subir():
    carpetas = list(filter(lambda x: os.path.isdir(x), os.listdir()))
    for carpeta in carpetas:
        archivos = os.listdir(carpeta)
        for archivo in archivos:
            os.rename(os.path.join(carpeta, archivo), archivo)
        os.rmdir(carpeta)


dic_funciones = {1: reemplazar_en_nombre,
                 2: renombrar_con_id,
                 3: editar_Media_Data,
                 4: distribuir,
                 5: redistribuir,
                 6: subir}


if __name__ == "__main__":

    op = entrada("[1] Reemplazar\n"
                 "[2] Renombrar\n"
                 "[3] Editar metadata\n"
                 "[4] Distribuir\n"
                 "[5] Redistribuir\n"
                 "[6] Subir\n"
                 ": ",
                 6)
    dic_funciones[int(op)]()
