import os
from os import path
from PDFNetPython3.PDFNetPython import PDFDoc, Optimizer, SDFDoc, PDFNet
from functions import handle_input
from easygui import diropenbox


def init_pdf_edit():
    demo_key = "demo:1650333343252:7bd26c220300000000859ea86b8e40bd390b8a93782acda0e7be174451"
    PDFNet.Initialize(demo_key)


def choose_pdf_modify(dir_path):
    op_action = handle_input("[0] Cancelar\n"
                             "[1] Comprimir\n"
                             "[2] Comprimir recursivo\n"
                             ": ", 2)
    if op_action == 0:
        return None
    elif op_action == 1:
        action = "compress"
    elif op_action == 2:
        action = "recursive_compress"
    op_output = handle_input("[0] Cancelar\n"
                             "[1] Sobreescribir\n"
                             "[2] Salida por defecto\n"
                             "[3] Seleccionar salida\n"
                             ": ", 3)
    if op_output == 0:
        return None
    elif op_output == 1:
        output_dir = None
    elif op_output == 2:
        output_dir = path.join(dir_path, "Output")
        if not path.exists(output_dir):
            os.mkdir(output_dir)
    elif op_output == 3:
        output_dir = diropenbox(default=dir_path)
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
        print(f"\nError al comprimir [{input_file}]")
        try:
            doc.Close()
        except Exception as error:
            print("***:", type(error))
        return False
    compressed_size = os.path.getsize(output_file)
    return (initial_size, compressed_size)


if __name__ == "__main__":
    pass
