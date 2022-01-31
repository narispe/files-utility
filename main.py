
from funciones import seleccionar_dir, manejar_entrada
from acciones import (subir, limpiar_nombres, renombrar_con_id, reemplazar_en_nombre,
                      distribuir, redistribuir, editar_metadata, cambiar_idioma)


def main():
    dic_acciones = {1: subir,
                    2: limpiar_nombres,
                    3: renombrar_con_id,
                    4: reemplazar_en_nombre,
                    5: distribuir,
                    6: redistribuir,
                    7: editar_metadata,
                    8: cambiar_idioma}
    seleccionar_dir()
    id_accion = manejar_entrada("[1] Subir\n"
                                "[2] Limpiar nombres\n"
                                "[3] Renombrar con ID\n"
                                "[4] Reemplazar en nombre\n"
                                "[5] Editar Metadata\n"
                                "[6] Distribuir\n"
                                "[7] Redistribuir\n"
                                "[8] Cambiar idioma\n"
                                ": ",
                                8)
    dic_acciones[id_accion]()


if __name__ == "__main__":
    main()
