from tkinter import messagebox
from conexion import consultar_registros


def mostrar_datos(conexion, tabla_visual, etiqueta_total, nombre_tabla):

    try:
        columnas, registros = consultar_registros(
            conexion,
            nombre_tabla
        )

        # Limpiar registros previos
        tabla_visual.delete(*tabla_visual.get_children())

        # Configurar encabezados dinámicamente
        tabla_visual["columns"] = columnas

        for columna in columnas:
            tabla_visual.heading(columna, text=columna)
            tabla_visual.column(columna, width=130, anchor="center")

        # Insertar filas
        for registro in registros:
            tabla_visual.insert("", "end", values=registro)

        # Mostrar total de registros encontrados
        etiqueta_total.config(
            text=f"Total de registros encontrados: {len(registros)}"
        )

    except Exception as error:
        messagebox.showerror(
            "Error",
            "No se pudieron consultar los registros.\n\n" + str(error)
        )