
import easygui
from functions import handle_input, get_mkv_info
from actions import (raise_files, clear_files_names, enumerate_files, rename_files,
                     distribute, re_distribute, edite_mkv, edite_mp4)


def main():
    base_dir = easygui.diropenbox()
    while True:
        id_accion = handle_input("[0] Cambiar carpeta\n"
                                 "[1] Subir\n"
                                 "[2] Limpiar nombres\n"
                                 "[3] Enumerar\n"
                                 "[4] Reemplazar en nombre\n"
                                 "[5] Distribuir\n"
                                 "[6] Redistribuir\n"
                                 "[7] Editar MKV\n"
                                 "[8] Editar MP4\n"
                                 ": ",
                                 8)

        if id_accion == 0:  # Cambiar carpeta
            base_dir = easygui.diropenbox()

        elif id_accion == 1:  # Subir
            raise_files(base_dir)

        elif id_accion == 2:  # Limpiar nombres
            ext = input("Extensión: ")
            clear_files_names(base_dir, ext)

        elif id_accion == 3:  # Enumerar
            template = input("Plantilla (# = ID): ")
            initial_id = int(input("ID inicial: "))
            extension = input("Extensión: ")
            enumerate_files(base_dir, template, initial_id, extension)

        elif id_accion == 4:  # Reemplazar en nombre
            searched = input("Frase a reemplazar: ")
            replaced = input("Reemplazo: ")
            rename_files(base_dir, searched, replaced)

        elif id_accion == 5:  # Distribuir
            # TODO: check len
            labels = input("Etiquetas separados por \",\": ").split(",")
            categories = input("Categorías respectivas separadas por \",\": ").split(",")
            distribute(base_dir, labels, categories)

        elif id_accion == 6:  # Redistribuir
            labels = input("Etiquetas separados por \",\": ").split(",")
            categories = input("Categorías respectivas separadas por \",\": ").split(",")
            re_distribute(base_dir, labels, categories)

        elif id_accion == 7:  # Editar MKV
            mkv_info = get_mkv_info(base_dir)
            if mkv_info is None:
                print("No existen mkv en la carpeta")
                continue
            print(mkv_info["table"])
            audio_id = handle_input("ID audio: ",
                                    max(mkv_info["audio_ids"]),
                                    min(mkv_info["audio_ids"]))
            subs_id = handle_input("ID subtítulos: ",
                                   max(mkv_info["subs_ids"]),
                                   min(mkv_info["subs_ids"]))
            if mkv_info["has_title"]:
                op_delete_title = handle_input("[1] Borrar títulos\n"
                                               "[2] Conservar títulos\n"
                                               ": ",
                                               2)
                delete_title = True if op_delete_title == 1 else False
            output_dir = easygui.diropenbox()
            edite_mkv(base_dir, output_dir, audio_id, subs_id, delete_title)

        elif id_accion == 8:  # Editar MP4
            edite_mp4()


if __name__ == "__main__":
    main()
