import tkinter as tk
from tkinter import ttk, messagebox
from conexion import obtener_tablas
from consultas import mostrar_datos
from insertar import abrir_ventana_insertar


def mostrar_menu(ventana, conexion, usuario):

    # Tamaños independientes para el menú y para la vista de cada sección
    TAMANO_MENU = "460x450"
    TAMANO_SECCION = "950x550"

    # Aplicar tamaño exclusivo de la ventana del menú
    ventana.geometry(TAMANO_MENU)

    # Encabezado fijo de la aplicación
    encabezado = tk.Frame(ventana)
    encabezado.pack(fill="x", padx=15, pady=(10, 5))

    tk.Label(
        encabezado,
        text="Administrador PostgreSQL",
        font=("Arial", 16, "bold")
    ).pack()

    tk.Label(
        encabezado,
        text="Usuario conectado: " + usuario,
        fg="#555555"
    ).pack()

    # Contenedor principal donde alternan el menú y la sección activa
    contenedor_principal = tk.Frame(ventana)
    contenedor_principal.pack(fill="both", expand=True, padx=15, pady=10)

    # VISTA 1: MENÚ DE SECCIONES
    frame_menu = tk.Frame(contenedor_principal, relief="groove", borderwidth=1)
    frame_menu.pack(fill="both", expand=True)

    tk.Label(
        frame_menu,
        text="SECCIONES DISPONIBLES",
        font=("Arial", 13, "bold")
    ).pack(pady=(18, 5))

    frame_botones_menu = tk.Frame(frame_menu)
    frame_botones_menu.pack(pady=10)

    # VISTA 2: PANEL DE LA SECCIÓN SELECCIONADA (oculta al inicio)
    frame_seccion = tk.Frame(contenedor_principal, relief="groove", borderwidth=1)

    # Barra superior con botón de regreso y título de la sección
    barra_superior = tk.Frame(frame_seccion)
    barra_superior.pack(fill="x", padx=15, pady=12)

    def regresar_al_menu():
        seccion_actual["nombre"] = None
        frame_resultados.pack_forget()
        frame_seccion.pack_forget()
        ventana.geometry(TAMANO_MENU)
        frame_menu.pack(fill="both", expand=True)

    tk.Button(
        barra_superior,
        text="← Regresar al menú",
        command=regresar_al_menu,
        bg="#555555",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=10
    ).pack(side="left")

    titulo_seccion = tk.Label(
        barra_superior,
        text="",
        font=("Arial", 15, "bold")
    )
    titulo_seccion.pack(side="left", padx=20)

    # Botones de acción dentro de la sección
    frame_acciones = tk.Frame(frame_seccion)
    frame_acciones.pack(pady=10)

    # Contenedor de resultados (oculto hasta presionar "Consultas generales")
    frame_resultados = tk.Frame(frame_seccion)

    etiqueta_total = tk.Label(
        frame_resultados,
        text="Total de registros encontrados: 0",
        font=("Arial", 11, "bold"),
        anchor="w"
    )
    etiqueta_total.pack(fill="x", padx=15, pady=(5, 5))

    frame_tabla = tk.Frame(frame_resultados)
    frame_tabla.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical")
    scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal")

    tabla_visual = ttk.Treeview(
        frame_tabla,
        show="headings",
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    scroll_y.config(command=tabla_visual.yview)
    scroll_x.config(command=tabla_visual.xview)

    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")
    tabla_visual.pack(side="left", fill="both", expand=True)

    # Estado de la sección seleccionada
    seccion_actual = {"nombre": None}

    def ejecutar_consulta_general():
        nombre = seccion_actual["nombre"]
        if nombre is None:
            return

        frame_resultados.pack(fill="both", expand=True)
        mostrar_datos(
            conexion,
            tabla_visual,
            etiqueta_total,
            nombre
        )

    def abrir_insercion():
        nombre = seccion_actual["nombre"]
        if nombre is None:
            return

        abrir_ventana_insertar(
            ventana,
            conexion,
            nombre,
            ejecutar_consulta_general
        )

    tk.Button(
        frame_acciones,
        text="Consultas generales",
        command=ejecutar_consulta_general,
        width=22,
        bg="#1f6aa5",
        fg="white",
        font=("Arial", 10, "bold")
    ).pack(side="left", padx=10)

    tk.Button(
        frame_acciones,
        text="Insertar nuevo registro",
        command=abrir_insercion,
        width=22,
        bg="#2e7d32",
        fg="white",
        font=("Arial", 10, "bold")
    ).pack(side="left", padx=10)

    # Cambiar del menú hacia la sección elegida
    def seleccionar_seccion(nombre):
        seccion_actual["nombre"] = nombre
        titulo_seccion.config(text=f"Sección: {nombre.capitalize()}")

        # Reiniciar vista previa de la tabla
        tabla_visual.delete(*tabla_visual.get_children())
        tabla_visual["columns"] = ()
        etiqueta_total.config(text="Total de registros encontrados: 0")
        frame_resultados.pack_forget()

        # Ocultar menú, ampliar ventana y mostrar la sección
        frame_menu.pack_forget()
        ventana.geometry(TAMANO_SECCION)
        frame_seccion.pack(fill="both", expand=True)

    # Cargar dinámicamente las tablas de PostgreSQL como botones en el menú
    try:
        tablas = obtener_tablas(conexion)

        if not tablas:
            tk.Label(
                frame_botones_menu,
                text="No hay tablas disponibles en la base de datos.",
                fg="#777777"
            ).pack(pady=10)

        for fila in tablas:
            nombre = fila[0]
            tk.Button(
                frame_botones_menu,
                text=nombre.capitalize(),
                width=26,
                height=2,
                font=("Arial", 11),
                command=lambda n=nombre: seleccionar_seccion(n)
            ).pack(pady=6)

    except Exception as error:
        messagebox.showerror(
            "Error",
            "No se pudieron obtener las secciones.\n\n" + str(error)
        )