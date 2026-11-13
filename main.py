
import tkinter as tk
from tkinter import messagebox
import psycopg2


def conectar_postgres(usuario, password):

    try:
        conexion = psycopg2.connect(
            host="localhost",
            port="5432",
            database="postgres",
            user=usuario,
            password=password
        )

        return conexion

    except psycopg2.Error as error:
        messagebox.showerror(
            "Error de conexión",
            f"No se pudo conectar:\n{error}"
        )
        return None


def iniciar_sesion():

    usuario = entrada_usuario.get()
    password = entrada_password.get()

    if not usuario or not password:
        messagebox.showwarning(
            "Campos vacíos",
            "Ingresa usuario y contraseña"
        )
        return

    conexion = conectar_postgres(usuario, password)

    if conexion:
        conexion.close()
        ventana_login.destroy()
        abrir_menu(usuario)


def abrir_menu(usuario):

    menu = tk.Tk()
    menu.title("Menú principal")
    menu.geometry("600x400")

    tk.Label(
        menu,
        text=f"Bienvenido: {usuario}",
        font=("Arial", 18, "bold")
    ).pack(pady=30)

    tk.Button(
        menu,
        text="Cerrar sesión",
        command=menu.destroy
    ).pack(pady=20)

    menu.mainloop()


# VENTANA LOGIN

ventana_login = tk.Tk()
ventana_login.title("Login PostgreSQL")
ventana_login.geometry("350x300")
ventana_login.resizable(False, False)

tk.Label(
    ventana_login,
    text="Inicio de sesión",
    font=("Arial", 18, "bold")
).pack(pady=20)

tk.Label(ventana_login, text="Usuario").pack()

entrada_usuario = tk.Entry(ventana_login)
entrada_usuario.pack(pady=5)

tk.Label(ventana_login, text="Contraseña").pack()

entrada_password = tk.Entry(
    ventana_login,
    show="*"
)
entrada_password.pack(pady=5)

tk.Button(
    ventana_login,
    text="Iniciar sesión",
    command=iniciar_sesion
).pack(pady=25)

ventana_login.mainloop()
