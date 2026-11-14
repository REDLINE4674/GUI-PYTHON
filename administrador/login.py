import tkinter as tk
from tkinter import messagebox
from conexion import conectar


def mostrar_login(ventana, al_conectar):

    login = tk.Frame(ventana)

    login.pack(expand=True)

    tk.Label(
        login,
        text="Administrador PostgreSQL",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    tk.Label(login, text="Usuario").pack()

    caja_usuario = tk.Entry(login)
    caja_usuario.pack(pady=5)

    tk.Label(login, text="Contraseña").pack()

    caja_password = tk.Entry(login, show="*")
    caja_password.pack(pady=5)

    def iniciar_sesion():

        usuario = caja_usuario.get()
        password = caja_password.get()

        if usuario == "" or password == "":
            messagebox.showwarning(
                "Campos vacíos",
                "Ingresa tu usuario y contraseña."
            )
            return

        try:

            conexion = conectar(usuario, password)

            messagebox.showinfo(
                "Conexión exitosa",
                "Bienvenido " + usuario
            )

            login.destroy()

            al_conectar(conexion, usuario)

        except Exception as error:

            messagebox.showerror(
                "Error de conexión",
                "No se pudo conectar con PostgreSQL.\n\n"
                "Verifica tu usuario y contraseña.\n\n"
                "Detalle: " + str(error)
            )

    tk.Button(
        login,
        text="Iniciar sesión",
        command=iniciar_sesion,
        width=18
    ).pack(pady=15)
