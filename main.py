import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2


# VENTANA PRINCIPAL
ventana = tk.Tk()
ventana.title("Administrador PostgreSQL")
ventana.geometry("800x500")


# VARIABLES
conexion = None
usuario = "admin"
password = "1234"


# FUNCION PARA INICIAR SESION
def iniciar_sesion():

    global conexion, usuario, password

    usuario = caja_usuario.get()
    password = caja_password.get()

    try:

        conexion = psycopg2.connect(
            host="localhost",
            database="NucleoDeDiagnostico",
            user=usuario,
            password=password,
            port="5433"
        )

        messagebox.showinfo(
            "Conexion exitosa",
            "Bienvenido " + usuario
        )

        mostrar_menu()

    except:

        messagebox.showerror(
            "Error",
            "Usuario o contraseña incorrectos"
        )


# FUNCION PARA MOSTRAR MENU
def mostrar_menu():

    # OCULTAR LOGIN
    login.destroy()

    # TITULO
    tk.Label(
        ventana,
        text="Administrador PostgreSQL",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    tk.Label(
        ventana,
        text="Usuario conectado: " + usuario
    ).pack()

    # SELECCIONAR TABLA
    global lista_tablas

    lista_tablas = ttk.Combobox(
        ventana,
        state="readonly",
        width=30
    )
    lista_tablas.pack(pady=10)

    lista_tablas.bind(
        "<<ComboboxSelected>>",
        consultar_datos
    )

    # BOTON INSERTAR
    tk.Button(
        ventana,
        text="Insertar tupla",
        command=insertar_tupla
    ).pack(pady=5)

    # TABLA PARA MOSTRAR DATOS
    global tabla

    tabla = ttk.Treeview(ventana, show="headings")
    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    # CARGAR TABLAS
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_type = 'BASE TABLE'
    """)

    tablas = cursor.fetchall()

    lista_tablas["values"] = [fila[0] for fila in tablas]

    cursor.close()


# FUNCION PARA CONSULTAR DATOS
def consultar_datos(event=None):

    nombre_tabla = lista_tablas.get()

    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM " + nombre_tabla
    )

    columnas = [columna[0] for columna in cursor.description]

    registros = cursor.fetchall()

    tabla.delete(*tabla.get_children())

    tabla["columns"] = columnas

    for columna in columnas:

        tabla.heading(columna, text=columna)
        tabla.column(columna, width=120)

    for registro in registros:

        tabla.insert("", "end", values=registro)

    cursor.close()


# FUNCION PARA INSERTAR TUPLAS
def insertar_tupla():

    nombre_tabla = lista_tablas.get()

    if nombre_tabla == "":
        messagebox.showwarning(
            "Aviso",
            "Selecciona una tabla"
        )
        return

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name = %s
        AND is_generated = 'NEVER'
        AND is_identity = 'NO'
        ORDER BY ordinal_position
    """, (nombre_tabla,))

    columnas = cursor.fetchall()

    cursor.close()

    # NUEVA VENTANA
    nueva = tk.Toplevel(ventana)
    nueva.title("Insertar tupla")

    entradas = []

    for columna in columnas:

        tk.Label(
            nueva,
            text=columna[0]
        ).pack()

        entrada = tk.Entry(nueva)
        entrada.pack(pady=3)

        entradas.append(entrada)

    # GUARDAR DATOS
    def guardar():

        valores = []
        nombres = []

        for i in range(len(columnas)):

            valor = entradas[i].get()

            if valor != "":
                nombres.append(columnas[i][0])
                valores.append(valor)

        try:

            cursor = conexion.cursor()

            if len(nombres) > 0:

                campos = ", ".join(nombres)
                signos = ", ".join(["%s"] * len(valores))

                consulta = (
                    "INSERT INTO " + nombre_tabla +
                    " (" + campos + ") VALUES (" + signos + ")"
                )

                cursor.execute(consulta, valores)

            else:

                cursor.execute(
                    "INSERT INTO " + nombre_tabla +
                    " DEFAULT VALUES"
                )

            conexion.commit()

            cursor.close()

            messagebox.showinfo(
                "Correcto",
                "Tupla insertada correctamente"
            )

            nueva.destroy()
            consultar_datos()

        except Exception as error:

            conexion.rollback()

            messagebox.showerror(
                "Error",
                str(error)
            )

    tk.Button(
        nueva,
        text="Guardar",
        command=guardar
    ).pack(pady=15)


# FORMULARIO DE LOGIN
login = tk.Frame(ventana)
login.pack(expand=True)

tk.Label(
    login,
    text="INICIO DE SESION",
    font=("Arial", 18, "bold")
).pack(pady=15)

tk.Label(login, text="Usuario").pack()

caja_usuario = tk.Entry(login)
caja_usuario.pack(pady=5)

tk.Label(login, text="Contraseña").pack()

caja_password = tk.Entry(login, show="*")
caja_password.pack(pady=5)

tk.Button(
    login,
    text="Conectar",
    command=iniciar_sesion
).pack(pady=15)


# INICIAR PROGRAMA
ventana.mainloop()
