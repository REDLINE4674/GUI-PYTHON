import tkinter as tk
from tkinter import ttk, messagebox
from conexion import obtener_tablas
from consultas import mostrar_datos
from insertar import abrir_ventana_insertar


def mostrar_menu(ventana, conexion, usuario):

    # Encabezado
    tk.Label(
        ventana,
        text="Administrador PostgreSQL",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    tk.Label(
        ventana,
        text="Usuario conectado: " + usuario
    ).pack()

    # Contenedor principal
    contenido = tk.Frame(ventana)

    contenido.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    # Menú lateral
    menu = tk.Frame(
        contenido,
        width=160,
        relief="groove",
        borderwidth=1
    )

    menu.pack(
        side="left",
        fill="y",
        padx=5
    )

    menu.pack_propagate(False)

    tk.Label(
        menu,
        text="TABLAS",
        font=("Arial", 12, "bold")
    ).pack(pady=10)

    # Panel de consultas
    panel = tk.Frame(contenido)

    panel.pack(
        side="right",
        fill="both",
        expand=True
    )

    titulo_tabla = tk.Label(
        panel,
        text="Selecciona una tabla",
        font=("Arial", 16, "bold")
    )

    titulo_tabla.pack(pady=10)

    # Tabla visual
    tabla_visual = ttk.Treeview(
        panel,
        show="headings"
    )

    tabla_visual.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    # Variable para recordar la tabla seleccionada
    tabla_seleccionada = {"nombre": None}

    # Consultar la tabla seleccionada
    def seleccionar_tabla(nombre):

        tabla_seleccionada["nombre"] = nombre

        mostrar_datos(
            conexion,
            tabla_visual,
            titulo_tabla,
            nombre
        )

    # Actualizar la tabla actual
    def actualizar():

        nombre = tabla_seleccionada["nombre"]

        if nombre is not None:

            mostrar_datos(
                conexion,
                tabla_visual,
                titulo_tabla,
                nombre
            )

    # Abrir formulario de inserción
    def insertar_tupla():

        nombre = tabla_seleccionada["nombre"]

        if nombre is None:

            messagebox.showwarning(
                "Selecciona una tabla",
                "Primero selecciona una tabla."
            )

            return

        abrir_ventana_insertar(
            ventana,
            conexion,
            nombre,
            actualizar
        )

    tk.Button(
        panel,
        text="Insertar tupla",
        command=insertar_tupla
    ).pack(pady=5)

    # Obtener las tablas de PostgreSQL
    try:

        tablas = obtener_tablas(conexion)

        for fila in tablas:

            nombre = fila[0]

            tk.Button(
                menu,
                text=nombre.capitalize(),
                width=18,
                command=lambda nombre=nombre: seleccionar_tabla(nombre)
            ).pack(pady=5)

    except Exception as error:

        messagebox.showerror(
            "Error",
            "No se pudieron obtener las tablas.\n\n" + str(error)
        )
