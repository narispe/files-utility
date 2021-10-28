import funciones as f


dic_funciones = {1: f.reemplazar_en_nombre,
                 2: f.renombrar_con_id,
                 3: f.editar_Media_Data,
                 4: f.distribuir,
                 5: f.redistribuir,
                 6: f.subir}


if __name__ == "__main__":

    op = f.entrada("[1] Reemplazar\n"
                   "[2] Renombrar\n"
                   "[3] Editar metadata\n"
                   "[4] Distribuir\n"
                   "[5] Redistribuir\n"
                   "[6] Subir\n"
                   ": ",
                   6)
    dic_funciones[int(op)]()
