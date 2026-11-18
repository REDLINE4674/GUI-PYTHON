import tkinter as tk
from tkinter import ttk, messagebox
from conexion import obtener_columnas, insertar_registro


def abrir_ventana_insertar(ventana, conexion, nombre_tabla, actualizar):

    try:
        columnas = obtener_columnas(conexion, nombre_tabla)

        nueva = tk.Toplevel(ventana)
        nueva.title(f"Insertar registro - {nombre_tabla.capitalize()}")
        nueva.geometry("460x440")
        nueva.resizable(False, False)
        nueva.grab_set()

        tk.Label(
            nueva,
            text=f"Nuevo registro en {nombre_tabla.capitalize()}",
            font=("Arial", 13, "bold")
        ).pack(pady=12)

        # Contenedor con barra de desplazamiento vertical
        contenedor = tk.Frame(nueva)
        contenedor.pack(fill="both", expand=True, padx=20)

        canvas = tk.Canvas(contenedor, highlightthickness=0)
        scrollbar = ttk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
        frame_campos = tk.Frame(canvas)

        frame_campos.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=frame_campos, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        entradas = []

        # Colocar etiqueta a la izquierda (column=0) e input a la derecha (column=1)
        for fila_idx, columna in enumerate(columnas):
            nombre_columna = columna[0]

            tk.Label(
                frame_campos,
                text=f"{nombre_columna}:",
                font=("Arial", 10, "bold"),
                anchor="w"
            ).grid(row=fila_idx, column=0, sticky="w", padx=(5, 15), pady=8)

            entrada = tk.Entry(frame_campos, width=32)
            entrada.grid(row=fila_idx, column=1, sticky="e", padx=(0, 10), pady=8)

            entradas.append(entrada)

        # Guardar registro en PostgreSQL
        def guardar():
            nombres = []
            valores = []

            for i in range(len(columnas)):
                valor = entradas[i].get().strip()
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
                    "El registro se insertó correctamente."
                )

                nueva.destroy()
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
            width=20,
            bg="#2e7d32",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(pady=15)

    except Exception as error:
        messagebox.showerror(
            "Error",
            "No se pudo abrir el formulario.\n\n" + str(error)
        )