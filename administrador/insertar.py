
import tkinter as tk
from tkinter import ttk, messagebox

from conexion import obtener_columnas, insertar_registro


def abrir_ventana_insertar(ventana, conexion, nombre_tabla, actualizar):

    estilo = None
    tema_anterior = None

    try:

        columnas = obtener_columnas(conexion, nombre_tabla)

        # CONFIGURACION DE LA VENTANA

        nueva = tk.Toplevel(ventana)

        nueva.title("Nuevo registro")
        nueva.geometry("450x600")
        nueva.resizable(False, False)

        nueva.configure(bg="#F0F2F5")

        nueva.transient(ventana)
        nueva.grab_set()

        # Estilos
        estilo = ttk.Style(nueva)
        tema_anterior = estilo.theme_use()
        estilo.theme_use("clam")

        estilo.configure(
            "Formulario.TCombobox",
            padding=(0, 0),
            font=("Arial", 10),
            fieldbackground="white",
            foreground="#333333",
            background="white",
            bordercolor="#333333",
            lightcolor="#333333",
            darkcolor="#333333",
            borderwidth=1,
            relief="solid"
        )
        estilo.map(
            "Formulario.TCombobox",
            fieldbackground=[("readonly", "white")],
            foreground=[("readonly", "#333333")]
        )

        def cerrar():
            nueva.destroy()
            estilo.theme_use(tema_anterior)

        nueva.protocol("WM_DELETE_WINDOW", cerrar)

        # ENCABEZADO

        encabezado = tk.Frame(
            nueva,
            bg="#1F4E79",
            height=85
        )

        encabezado.pack(fill="x")
        encabezado.pack_propagate(False)

        tk.Label(
            encabezado,
            text="Nuevo registro",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#1F4E79"
        ).pack(anchor="w", padx=20, pady=(15, 2))

        tk.Label(
            encabezado,
            text=f"Tabla: {nombre_tabla.capitalize()}",
            font=("Arial", 10),
            fg="#DCE8F5",
            bg="#1F4E79"
        ).pack(anchor="w", padx=20)

        # CONTENEDOR DEL FORMULARIO

        contenedor = tk.Frame(
            nueva,
            bg="#F0F2F5"
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=12
        )

        # Canvas para permitir desplazamiento
        canvas = tk.Canvas(
            contenedor,
            bg="white",
            highlightthickness=0
        )

        scroll = ttk.Scrollbar(
            contenedor,
            orient="vertical",
            command=canvas.yview
        )

        formulario = tk.Frame(
            canvas,
            bg="white"
        )

        ventana_formulario = canvas.create_window(
            (0, 0),
            window=formulario,
            anchor="nw"
        )

        canvas.configure(
            yscrollcommand=scroll.set
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll.pack(
            side="right",
            fill="y"
        )

        # Ajustar el tamaño del formulario
        def ajustar_formulario(event):

            canvas.configure(
                scrollregion=canvas.bbox("all")
            )

        def ajustar_ancho(event):

            canvas.itemconfigure(
                ventana_formulario,
                width=event.width
            )

        formulario.bind(
            "<Configure>",
            ajustar_formulario
        )

        canvas.bind(
            "<Configure>",
            ajustar_ancho
        )

        def desplazar_formulario(event):
            canvas.yview_scroll(int(-event.delta / 120), "units")

        nueva.bind("<MouseWheel>", desplazar_formulario)

        # CAMPOS DEL FORMULARIO

        entradas = []

        for i, columna in enumerate(columnas):

            nombre_columna = columna[0]
            nombre_normalizado = nombre_columna.lower()

            # Contenedor individual
            campo = tk.Frame(
                formulario,
                bg="white"
            )

            campo.pack(
                fill="x",
                padx=20,
                pady=9
            )
            campo.grid_columnconfigure(0, minsize=150)
            campo.grid_columnconfigure(1, weight=1)
            campo.grid_rowconfigure(0, minsize=30)

            # Etiqueta
            tk.Label(
                campo,
                text=nombre_columna.replace("_", " ").capitalize(),
                font=("Arial", 10, "bold"),
                bg="white",
                fg="#333333",
                anchor="w",
                wraplength=130
            ).grid(row=0, column=0, sticky="w", padx=(0, 12))

            if nombre_normalizado == "sexo":

                entrada = ttk.Combobox(
                    campo,
                    values=["F", "M"],
                    state="readonly",
                    font=("Arial", 10),
                    style="Formulario.TCombobox"
                )

                entrada.set("")

            elif nombre_normalizado == "turno":

                entrada = ttk.Combobox(
                    campo,
                    values=["M", "V"],
                    state="readonly",
                    font=("Arial", 10),
                    style="Formulario.TCombobox"
                )

                entrada.set("")

            else:

                entrada = tk.Entry(
                    campo,
                    font=("Arial", 10),
                    relief="solid",
                    borderwidth=1
                )

            entrada.grid(
                row=0,
                column=1,
                sticky="nsew",
                ipady=5
            )

            entradas.append(entrada)

        def cancelar():

            cerrar()

        #Guardar

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
                    "El registro se insertó correctamente.",
                    parent=nueva
                )

                cerrar()

                # Actualizar la tabla visual
                actualizar()

            except Exception as error:

                conexion.rollback()

                messagebox.showerror(
                    "Error al insertar",
                    str(error),
                    parent=nueva
                )

        #Botones

        botones = tk.Frame(
            nueva,
            bg="#F0F2F5"
        )

        botones.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

        # Botón cancelar
        tk.Button(
            botones,
            text="Cancelar",
            command=cancelar,
            width=15,
            bg="#E0E4E8",
            fg="#333333",
            relief="flat",
            font=("Arial", 10),
            cursor="hand2"
        ).pack(side="left")

        # Botón guardar
        tk.Button(
            botones,
            text="Guardar registro",
            command=guardar,
            width=18,
            bg="#1F4E79",
            fg="white",
            activebackground="#163A5A",
            activeforeground="white",
            relief="flat",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side="right")

    except Exception as error:

        if estilo is not None and tema_anterior is not None:
            estilo.theme_use(tema_anterior)

        messagebox.showerror(
            "Error",
            "No se pudo abrir el formulario.\n\n" + str(error)
        )
