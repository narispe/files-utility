import os
from os import path
from PDFNetPython3.PDFNetPython import PDFDoc, Optimizer, SDFDoc, PDFNet
from functions import handle_input
from easygui import diropenbox


def init_pdf_edit():
    PDFNet.Initialize()


def choose_pdf_modify(dir_path):
    op = handle_input("[0] Cancelar\n"
                      "[1] Comprimir\n"
                      "[2] Comprimir recursivo\n"
                      ": ", 2)
    if op == 0:
        return None
    elif op == 1:
        action = "compress"
    elif op == 2:
        action = "recursive_compress"
    op_output = handle_input("[0] Cancelar\n"
                             "[1] Sobreescribir\n"
                             "[2] Salida por defecto\n"
                             "[3] Seleccionar salida\n"
                             ": ", 3)
    if op_output == 0:
        return None
    elif op == 1:
        output_dir = None
    elif op == 2:
        output_dir = path.join(dir_path, "Output")
        if not path.exists(output_dir):
            os.mkdir(output_dir)
    elif op == 3:
        output_dir = diropenbox(default=dir_path+"/")
    return {"action": action, "output_dir": output_dir}


def compress_file(input_file, output_file):
    initial_size = os.path.getsize(input_file)
    try:
        doc = PDFDoc(input_file)
        doc.InitSecurityHandler()  # Optimize PDF with the default settings
        # Remove redundant information and compress data streams
        Optimizer.Optimize(doc)
        doc.Save(output_file, SDFDoc.e_linearized)
        doc.Close()
    except Exception as e:
        print("Error al comprimir=", e)
        try:
            doc.Close()
        except Exception as error:
            print("***", error)
        return False
    compressed_size = os.path.getsize(output_file)
    return (initial_size, compressed_size)


if __name__ == "__main__":
    pass
