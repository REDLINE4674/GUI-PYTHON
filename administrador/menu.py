
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from PIL import Image, ImageTk

from conexion import obtener_tablas
from consultas import mostrar_datos
from insertar import abrir_ventana_insertar


def mostrar_menu(ventana, conexion, usuario, rol, al_cerrar_sesion):

    ventana.title("Nucleo De Diagnostico")
    ventana.configure(bg="#F0F2F5")

    es_administrador = str(rol) == "1"
    es_usuario_normal = str(rol) == "2"
    perfil = "Administrador" if es_administrador else "Usuario normal" if es_usuario_normal else "Rol no definido"

    def es_tabla_pacientes(nombre_tabla):
        nombre_normalizado = str(nombre_tabla).strip().lower()
        return nombre_normalizado in ("paciente", "pacientes")

    barra_superior = tk.Frame(ventana, bg="#1F4E79")
    barra_superior.pack(fill="x", padx=12, pady=(12, 0))

    tk.Label(
        barra_superior,
        text=f"Bienvenido  {usuario}",
        font=("Arial", 12, "bold"),
        bg="#1F4E79",
        fg="white"
    ).pack(side="left", padx=15, pady=10)

    tk.Button(
        barra_superior,
        text="Cerrar sesión",
        command=al_cerrar_sesion,
        bg="white",
        fg="#1F4E79",
        relief="flat",
        font=("Arial", 10, "bold"),
        cursor="hand2"
    ).pack(side="right", padx=10, pady=5)

    # CONTENEDOR PRINCIPAL

    contenido = tk.Frame(ventana, bg="#F0F2F5")
    contenido.pack(fill="both", expand=True)

    # MENU LATERAL

    menu = tk.Frame(
        contenido,
        bg="white",
        width=210,
        relief="solid",
        borderwidth=1
    )

    menu.pack(
        side="left",
        fill="y",
        padx=(12, 6),
        pady=12
    )

    menu.pack_propagate(False)

    # Encabezado del menú lateral
    tk.Label(
        menu,
        text="CONSULTAS GENERALES",
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#1F4E79"
    ).pack(pady=20)

    # Separador
    ttk.Separator(
        menu,
        orient="horizontal"
    ).pack(fill="x", padx=12, pady=5)

    # Contenedor de botones de tablas
    contenedor_botones = tk.Frame(
        menu,
        bg="white"
    )

    contenedor_botones.pack(
        fill="both",
        expand=True,
        padx=8,
        pady=10
    )

    # PANEL DE CONTENIDO

    panel = tk.Frame(
        contenido,
        bg="white",
        relief="solid",
        borderwidth=1
    )

    panel.pack(
        side="right",
        fill="both",
        expand=True,
        padx=(6, 12),
        pady=12
    )

    # Variable para recordar la tabla seleccionada
    tabla_seleccionada = {"nombre": None}

    def limpiar_panel():

        for widget in panel.winfo_children():
            widget.destroy()

    # MENU PRINCIPAL

    def mostrar_inicio():

        boton_regresar.pack_forget()
        tabla_seleccionada["nombre"] = None

        limpiar_panel()

        inicio = tk.Frame(
            panel,
            bg="white"
        )

        inicio.pack(
            fill="both",
            expand=True
        )

        # Imagen
        try:

            ruta_imagen = Path(__file__).resolve().parent / "imagenes" / "nd.png"
            imagen = Image.open(ruta_imagen)
            imagen = imagen.resize((160, 160))

            logo = ImageTk.PhotoImage(imagen)

            etiqueta_imagen = tk.Label(
                inicio,
                image=logo,
                bg="white"
            )

            etiqueta_imagen.image = logo
            etiqueta_imagen.pack(pady=(50, 15))

        except Exception:

            tk.Label(
                inicio,
                text="NÚCLEO",
                font=("Arial", 30, "bold"),
                fg="#1F4E79",
                bg="white"
            ).pack(pady=(70, 15))

        # Usuario conectado
        tk.Label(
            inicio,
            text=f"Usuario: {usuario}",
            font=("Arial", 21, "bold"),
            bg="white",
            fg="#333333"
        ).pack(pady=10)

        tk.Label(
            inicio,
            text=f"Perfil: {perfil}",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#1F4E79"
        ).pack(pady=(0, 10))

        # Mensaje de bienvenida
        tk.Label(
            inicio,
            text="Bienvenido al sistema de administración de datos.",
            font=("Arial", 11),
            bg="white",
            fg="#666666"
        ).pack(pady=15)

        tk.Label(
            inicio,
            text="Selecciona una tabla del menú lateral para comenzar.",
            font=("Arial", 10),
            bg="white",
            fg="#888888"
        ).pack(pady=5)

    boton_regresar = tk.Button(
        barra_superior,
        text="Regresar al menú",
        command=mostrar_inicio,
        bg="#E8EEF5",
        fg="#1F4E79",
        relief="flat",
        font=("Arial", 10),
        cursor="hand2"
    )

    # VISTA DE TABLAS

    def seleccionar_tabla(nombre):

        if es_usuario_normal and not es_tabla_pacientes(nombre):
            messagebox.showwarning(
                "Acceso restringido",
                "Tu perfil solo puede consultar la tabla de pacientes.",
                parent=ventana
            )
            return

        if not boton_regresar.winfo_manager():
            boton_regresar.pack(side="right", padx=(0, 10), pady=5)

        tabla_seleccionada["nombre"] = nombre

        limpiar_panel()

        # Encabezado de la tabla
        encabezado_tabla = tk.Frame(
            panel,
            bg="white"
        )

        encabezado_tabla.pack(
            fill="x",
            padx=20,
            pady=15
        )

        titulo_tabla = tk.Label(
            encabezado_tabla,
            text=f"Tabla: {nombre.capitalize()}",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#1F4E79"
        )

        titulo_tabla.pack(side="left")

        contador_registros = tk.Label(
            encabezado_tabla,
            text="Registros encontrados: 0",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#666666"
        )
        contador_registros.pack(side="right")

        vista_registros = {"tabla": None}

        # ACTUALIZAR REGISTROS

        def actualizar(mostrar_si_oculto=True):

            nombre_actual = tabla_seleccionada["nombre"]

            if nombre_actual is not None:
                if vista_registros["tabla"] is None:
                    if not mostrar_si_oculto:
                        return 0

                    contenedor_tabla = tk.Frame(
                        panel,
                        bg="white"
                    )

                    contenedor_tabla.pack(
                        fill="both",
                        expand=True,
                        padx=20,
                        pady=10
                    )

                    tabla_visual = ttk.Treeview(
                        contenedor_tabla,
                        show="headings"
                    )
                    scroll_vertical = ttk.Scrollbar(
                        contenedor_tabla,
                        orient="vertical",
                        command=tabla_visual.yview
                    )
                    scroll_horizontal = ttk.Scrollbar(
                        contenedor_tabla,
                        orient="horizontal",
                        command=tabla_visual.xview
                    )

                    tabla_visual.configure(
                        yscrollcommand=scroll_vertical.set,
                        xscrollcommand=scroll_horizontal.set
                    )
                    tabla_visual.grid(row=0, column=0, sticky="nsew")
                    scroll_vertical.grid(row=0, column=1, sticky="ns")
                    scroll_horizontal.grid(row=1, column=0, sticky="ew")
                    contenedor_tabla.grid_rowconfigure(0, weight=1)
                    contenedor_tabla.grid_columnconfigure(0, weight=1)
                    vista_registros["tabla"] = tabla_visual

                cantidad = mostrar_datos(
                    conexion,
                    vista_registros["tabla"],
                    titulo_tabla,
                    nombre_actual
                )
                contador_registros.config(
                    text=f"Registros encontrados: {cantidad}"
                )
                return cantidad
            return 0

        # BOTONES INFERIORES

        botones = tk.Frame(
            panel,
            bg="white"
        )

        botones.pack(
            fill="x",
            padx=20,
            pady=15
        )

        tk.Button(
            botones,
            text="Consultar registros",
            command=actualizar,
            width=20,
            bg="#5A8FC4",
            fg="white",
            relief="flat",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side="left", padx=5)

        # Insertar registro
        if es_administrador or (
            es_usuario_normal and es_tabla_pacientes(nombre)
        ):
            tk.Button(
                botones,
                text="Insertar registro",
                command=lambda: abrir_ventana_insertar(
                    ventana,
                    conexion,
                    nombre,
                    lambda: actualizar(mostrar_si_oculto=False)
                ),
                width=20,
                bg="#1F4E79",
                fg="white",
                relief="flat",
                font=("Arial", 10, "bold"),
                cursor="hand2"
            ).pack(side="right")

    # CARGAR TABLAS

    try:

        tablas = obtener_tablas(conexion)

        if not tablas:

            tk.Label(
                contenedor_botones,
                text="No hay tablas disponibles",
                bg="white",
                fg="gray",
                font=("Arial", 9)
            ).pack(pady=10)

        for fila in tablas:

            nombre = fila[0]

            if es_usuario_normal and not es_tabla_pacientes(nombre):
                continue

            tk.Button(
                contenedor_botones,
                text=nombre.capitalize(),
                command=lambda n=nombre: seleccionar_tabla(n),
                width=21,
                height=2,
                bg="#E8EEF5",
                fg="#333333",
                activebackground="#D0DFEF",
                relief="flat",
                font=("Arial", 10),
                cursor="hand2"
            ).pack(pady=5, padx=5)

    except Exception as error:

        messagebox.showerror(
            "Error",
            "No se pudieron obtener las tablas.\n\n" + str(error)
        )

    mostrar_inicio()
