
from easygui import diropenbox, filesavebox
import os
import webbrowser
from functions import handle_input, check_input, get_paths
from mkv import choose_mkv_modify
from actions import (raise_files, clear_files_names, enumerate_files,
                     rename_files, distribute, re_distribute,
                     edite_mkv, edite_mp4, edite_pdf,
                     search_files)


def main():
    dir_path = diropenbox()
    while dir_path is not None:
        title = os.path.basename(dir_path).center(30, "_")
        id_action = handle_input(f"{title}\n"
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
            raise_files(dir_path)

        elif id_action == 2:  # Limpiar nombres
            ext = check_input("Extensión: ", form=".*")  # TODO
            if get_paths(dir_path, ext=ext) is None:
                print(f"No existen archivo de extension {ext}")
                continue
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
            labels = input("Etiquetas separados por \",\": ").split(",")
            categories = input("Categorías respectivas separadas por \",\": ").split(",")
            distribute(dir_path, labels, categories)

        elif id_action == 6:  # Redistribuir
            labels = input("Etiquetas separados por \",\": ").split(",")
            categories = input("Categorías respectivas separadas por \",\": ").split(",")
            re_distribute(dir_path, labels, categories)

        elif id_action == 7:  # Editar MKV
            choose = choose_mkv_modify(dir_path)
            if choose is not None:
                edite_mkv(dir_path, choose["output_dir"],
                          choose["audio"], choose["subs"],
                          choose["delete_title"], choose["titles"])

        elif id_action == 8:  # Editar MP4
            edite_mp4()

        elif id_action == 9:  # Editar PDF
            id_option = handle_input("[0] Cancelar\n"
                                     "[1] Comprimir\n"
                                     "[2] Comprimir recursivo\n"
                                     ": ",
                                     2)
            # output_dir = diropenbox()
            output_dir = None
            if id_option == 1:
                edite_pdf(dir_path, output_dir, "compress", rewrite=True)
            elif id_option == 2:
                edite_pdf(dir_path, output_dir, "recursive_compress", rewrite=True)

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
