from tkinter import messagebox
from conexion import consultar_registros


def mostrar_datos(conexion, tabla_visual, titulo, nombre_tabla):

    try:

        columnas, registros = consultar_registros(
            conexion,
            nombre_tabla
        )

        # Actualizar título
        titulo.config(text=nombre_tabla.capitalize())

        # Limpiar tabla visual
        tabla_visual.delete(*tabla_visual.get_children())

        # Configurar columnas
        tabla_visual["columns"] = columnas

        for columna in columnas:

            tabla_visual.heading(
                columna,
                text=columna
            )

            tabla_visual.column(
                columna,
                width=120
            )

        # Mostrar registros
        for registro in registros:

            tabla_visual.insert(
                "",
                "end",
                values=registro
            )
        return len(registros)

    except Exception as error:

        messagebox.showerror(
            "Error",
            "No se pudieron consultar los registros.\n\n" + str(error)
        )
        return 0
