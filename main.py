
from easygui import diropenbox
import os
import webbrowser
from functions import handle_input, check_input, get_paths
from mkv import choose_mkv_modify
from actions import (raise_files, clear_files_names, enumerate_files, rename_files,
                     distribute, re_distribute, edite_mkv, edite_mp4)


def main():
    dir_path = diropenbox()
    while dir_path is not None:
        title = os.path.basename(dir_path).center(30, "_")
        id_accion = handle_input(f"{title}\n"
                                 "[0] Cambiar carpeta\n"
                                 "[1] Subir\n"
                                 "[2] Limpiar nombres\n"
                                 "[3] Enumerar\n"
                                 "[4] Reemplazar en nombre\n"
                                 "[5] Distribuir\n"
                                 "[6] Redistribuir\n"
                                 "[7] Editar MKV\n"
                                 "[8] Editar MP4\n"
                                 "[9] Descargar\n"
                                 "[10] Salir\n"
                                 ": ",
                                 10)

        if id_accion == 0:  # Cambiar carpeta
            new_dir_path = diropenbox()
            dir_path = new_dir_path if new_dir_path is not None else dir_path

        elif id_accion == 1:  # Subir
            raise_files(dir_path)

        elif id_accion == 2:  # Limpiar nombres
            ext = check_input("Extensión: ", form=".*")  # TODO
            if get_paths(dir_path, ext=ext) is None:
                print(f"No existen archivo de extension {ext}")
                continue
            clear_files_names(dir_path, ext)

        elif id_accion == 3:  # Enumerate
            template = check_input("Plantilla (#=ID): ", content="#")
            initial_id = check_input("ID inicial: ", is_int=True)
            extension = check_input("Extensión: ", form=".*")  # TODO
            enumerate_files(dir_path, template, initial_id, extension)

        elif id_accion == 4:  # Reemplazar en nombre
            searched = input("Frase a reemplazar: ")
            replaced = input("Reemplazo: ")
            rename_files(dir_path, searched, replaced)

        elif id_accion == 5:  # Distribuir
            # TODO: check len
            labels = input("Etiquetas separados por \",\": ").split(",")
            categories = input("Categorías respectivas separadas por \",\": ").split(",")
            distribute(dir_path, labels, categories)

        elif id_accion == 6:  # Redistribuir
            labels = input("Etiquetas separados por \",\": ").split(",")
            categories = input("Categorías respectivas separadas por \",\": ").split(",")
            re_distribute(dir_path, labels, categories)

        elif id_accion == 7:  # Editar MKV
            choose = choose_mkv_modify(dir_path)
            if choose is not None and choose["output_dir"] is not None:
                edite_mkv(dir_path, choose["output_dir"],
                          choose["audio"], choose["subs"],
                          choose["delete_title"], choose["titles"])

        elif id_accion == 8:  # Editar MP4
            edite_mp4()

        elif id_accion == 9:
            urls = list()
            url = input("Ingresa una url ([0] Terminar): ")
            while url != "0":
                if url != "":
                    urls.append(url)
                url = input("Ingresa una url ([0] Terminar): ")
            for url in urls:
                webbrowser.open_new(url)

        elif id_accion == 10:  # Salir
            break


if __name__ == "__main__":
    main()
