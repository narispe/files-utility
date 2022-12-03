
from easygui import diropenbox, filesavebox
import os
from functions import handle_input, check_input, get_paths
from mkv import choose_mkv_modify
from actions import (raise_files, clear_files_names, enumerate_files,
                     rename_files, distribute, re_distribute,
                     edite_mkv, edite_mp4, edite_pdf,
                     search_files)


def main():
    print("Seleccionando carpeta...")
    dir_path = diropenbox()
    while dir_path is not None:
        title = os.path.basename(dir_path).center(30, "_")
        id_action = handle_input(f"\n{title}\n"
                                 "[0] Cambiar carpeta\n"
                                 "[1] Subir\n"
                                 "[2] Limpiar nombres\n"
                                 "[3] Enumerar\n"
                                 "[4] Reemplazar en nombre\n"
                                 "[5] Distribuir\n"
                                 "[6] Redistribuir\n"
                                 "[7] Editar MKV\n"
                                 "[8] Editar MP4\n"
                                 "[9] Editar PDF\n"
                                 "[10] Buscar archivos\n"
                                 "[11] Salir\n"
                                 ": ",
                                 11)

        if id_action == 0:  # Cambiar carpeta
            new_dir_path = diropenbox()
            dir_path = new_dir_path if new_dir_path is not None else dir_path

        elif id_action == 1:  # Subir
            id_remove = handle_input("[0] Cancelar\n"
                                     "[1] Eliminar duplicados\n"
                                     "[2] No mover duplicados\n"
                                     ": ", 2)
            if id_remove == 0:
                continue
            remove_duplicates = True if id_remove == 1 else False
            raise_files(dir_path, remove_duplicates)

        elif id_action == 2:  # Limpiar nombres
            ext = check_input("Extensión: ", form=".*")  # TODO
            clear_files_names(dir_path, ext)

        elif id_action == 3:  # Enumerate
            template, extension = check_input("Plantilla con extensión"
                                              " (# = índice): ",
                                              content="#", is_file=True)
            initial_id = check_input("Índice inicial: ", is_int=True)
            enumerate_files(dir_path, template, initial_id, extension)

        elif id_action == 4:  # Reemplazar en nombre
            searched = input("Frase a reemplazar: ")
            replaced = input("Reemplazo: ")
            rename_files(dir_path, searched, replaced)

        elif id_action == 5:  # Distribuir
            # TODO: check len
            id_label = handle_input("[0] Cancelar\n[1] Usar plantilla de fotos\n[2] Manual\n:",
                                    2)
            if id_label == 0:
                continue
            elif id_label == 1:
                labels = [f"{year}{month:02d}" for year in range(2006, 2023) for month in range(1, 13)]
                categories = [f"{year}-{month:02d}" for year in range(2006, 2023) for month in range(1, 13)]
            elif id_label == 2:
                labels = input("Etiquetas separados por \",\": ").split(",")
                categories = input("Categorías respectivas separadas por \",\": ").split(",")
            distribute(dir_path, labels, categories)

        elif id_action == 6:  # Redistribuir
            labels = input("Etiquetas separados por \",\": ").split(",")
            categories = input("Categorías respectivas separadas por \",\": ")
            re_distribute(dir_path, labels, categories.split(","))

        elif id_action == 7:  # Editar MKV
            edite_mkv(dir_path)

        elif id_action == 8:  # Editar MP4
            edite_mp4()

        elif id_action == 9:  # Editar PDF
            edite_pdf(dir_path)

        elif id_action == 10:  # Buscar archivos
            ext = check_input("Extensión: ", form=".*")
            output_file = filesavebox(default=dir_path + "/")
            if not output_file.endswith(".txt"):
                output_file = output_file + ".txt"
            search_files(dir_path, ext, output_file)

        elif id_action == 11:  # Salir
            break


if __name__ == "__main__":
    main()
