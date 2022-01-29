import os
import easygui
from mutagen.mp4 import MP4


def seleccionar_dir():
    os.chdir(easygui.diropenbox())


def manejar_entrada(mensaje, n_max):
    op = input(mensaje)
    while not op.isdecimal() or int(op) > n_max:
        op = input(mensaje)
    return int(op)


def obtener_paths():
    op = manejar_entrada("[1] Archivo\n[2] Carpeta\n: ", 2)
    if op == 1:
        ext = input("Ingresa la extensión: ")
        return list(filter(lambda x: os.path.isfile(x) and os.path.splitext(x)[1] == ext,
                           os.listdir()))
    else:
        return list(filter(lambda x: os.path.isdir(x),
                           os.listdir()))


def limpiar_info(entrada, caracteres_entorno=str):
    caracter_inicial, caracter_final = caracteres_entorno
    resultado = ""
    eliminando = False
    i = 0
    for i in range(len(entrada)):
        caracter = entrada[i]
        if caracter == caracter_inicial:
            eliminando = True
        if not eliminando:
            resultado += caracter
        if caracter == " " and entrada[i-1] == caracter_final:
            eliminando = False
    return resultado.strip()
