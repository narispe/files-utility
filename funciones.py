import os
from mutagen.mp4 import MP4


def entrada(mensaje, n_max):
    op = input(mensaje)
    while not op.isdecimal or int(op) > n_max:
        op = input(mensaje)
    return int(op)


def seleccionar_filtro():
    op = entrada("[1] Archivo\n[2] Carpeta\n: ", 2)
    filtro = os.path.isfile if op == 1 else os.path.isdir
    return filtro


def reemplazar_en_nombre():
    reemplazar = input("Frase a reemplazar: ")
    reemplazo = input("Reemplazo: ")
    filtro = seleccionar_filtro()
    paths = list(filter(lambda x: filtro(x), os.listdir()))
    for path in paths:
        nuevo_nombre = path.replace(reemplazar, reemplazo)
        os.rename(path, nuevo_nombre)


def renombrar_con_id():
    base = input("base")
    filtro = seleccionar_filtro()
    paths = list(filter(lambda x: filtro(x), os.listdir()))
    i = 1
    for path in sorted(paths):
        nombre, ext = os.path.splitext(path)
        nuevo_nombre = f"{base} " + f"{i:02d}"
        os.rename(path, nuevo_nombre+ext)
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


def redistribuir():
    etiquetas = input("Etiquetas separadas por \",\":\n").split(",")
    print(etiquetas)
    carpetas = list(filter(lambda x: os.path.isdir(x), os.listdir()))
    print(carpetas)
    for carpeta in carpetas:
        print(os.listdir(carpeta))
        archivos = list(filter(lambda x: os.path.isfile(os.path.join(carpeta, x)),
                               os.listdir(carpeta)))
        print(archivos)
        for archivo in archivos:
            destinos = list(filter(lambda x: x in archivo, etiquetas))
            print(destinos)
            if not destinos:
                pass
            else:
                destino = destinos[0]
                if not os.path.isdir(destino):
                    os.mkdir(destino)
                os.rename(os.path.join(carpeta, archivo), os.path.join(destino, archivo))
        os.rmdir(carpeta)


def subir():
    carpetas = list(filter(lambda x: os.path.isdir(x), os.listdir()))
    for carpeta in carpetas:
        archivos = os.listdir(carpeta)
        for archivo in archivos:
            os.rename(os.path.join(carpeta, archivo), archivo)
        os.rmdir(carpeta)


if __name__ == "__main__":
    pass
