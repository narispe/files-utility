import os
from PDFNetPython3.PDFNetPython import PDFDoc, Optimizer, SDFDoc, PDFNet
import easygui


def init_pdf_edit():
    PDFNet.Initialize()


def compress_file(input_file, output_file):
    if not output_file:
        output_file = input_file
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
        except:
            pass
        return False
    compressed_size = os.path.getsize(output_file)
    return (initial_size, compressed_size)


if __name__ == "__main__":
    pass
