import tkinter as tk
from tkinter import messagebox
from conexion import obtener_columnas, insertar_registro


def abrir_ventana_insertar(ventana, conexion, nombre_tabla, actualizar):

    try:

        columnas = obtener_columnas(conexion, nombre_tabla)

        nueva = tk.Toplevel(ventana)

        nueva.title("Insertar tupla")
        nueva.geometry("350x550")
        nueva.resizable(False, False)

        tk.Label(
            nueva,
            text="Insertar en " + nombre_tabla,
            font=("Arial", 14, "bold")
        ).pack(pady=15)

        entradas = []

        # Crear los campos automáticamente
        for columna in columnas:

            nombre_columna = columna[0]

            tk.Label(
                nueva,
                text=nombre_columna
            ).pack(pady=3)

            entrada = tk.Entry(nueva, width=35)

            entrada.pack(pady=3)

            entradas.append(entrada)

        # Guardar los datos
        def guardar():

            nombres = []
            valores = []

            for i in range(len(columnas)):

                valor = entradas[i].get()

                if valor != "":

                    nombres.append(columnas[i][0])
                    valores.append(valor)

            try:

                insertar_registro(
                    conexion,
                    nombre_tabla,
                    nombres,
                    valores
                )

                messagebox.showinfo(
                    "Registro insertado",
                    "La tupla se insertó correctamente."
                )

                nueva.destroy()

                # Actualizar la tabla visual
                actualizar()

            except Exception as error:

                conexion.rollback()

                messagebox.showerror(
                    "Error al insertar",
                    str(error)
                )

        tk.Button(
            nueva,
            text="Guardar",
            command=guardar,
            width=18
        ).pack(pady=20)

    except Exception as error:

        messagebox.showerror(
            "Error",
            "No se pudo abrir el formulario.\n\n" + str(error)
        )
