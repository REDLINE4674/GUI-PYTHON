import tkinter as tk
from tkinter import messagebox
from conexion import conectar


def mostrar_login(ventana, al_conectar):

    # Tamaño exclusivo para la vista de inicio de sesión
    ventana.geometry("400x350")
    ventana.resizable(False, False)

    login = tk.Frame(ventana)
    login.pack(expand=True, fill="both", padx=30, pady=20)

    tk.Label(
        login,
        text="Administrador PostgreSQL",
        font=("Arial", 16, "bold")
    ).pack(pady=(10, 5))

    tk.Label(
        login,
        text="Inicia sesión para continuar",
        fg="#555555"
    ).pack(pady=(0, 15))

    tk.Label(login, text="Usuario", font=("Arial", 10, "bold")).pack(anchor="w")
    caja_usuario = tk.Entry(login, width=32)
    caja_usuario.pack(pady=(3, 10), fill="x")
    caja_usuario.focus()

    tk.Label(login, text="Contraseña", font=("Arial", 10, "bold")).pack(anchor="w")
    caja_password = tk.Entry(login, show="*", width=32)
    caja_password.pack(pady=(3, 15), fill="x")

    def iniciar_sesion(event=None):

        usuario = caja_usuario.get().strip()
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

            # Habilitar redimensionamiento antes de pasar al menú
            ventana.resizable(True, True)
            login.destroy()

            al_conectar(conexion, usuario)

        except Exception as error:
            messagebox.showerror(
                "Error de conexión",
                "No se pudo conectar con PostgreSQL.\n\n"
                "Verifica tu usuario y contraseña.\n\n"
                "Detalle: " + str(error)
            )

    # Permitir iniciar sesión presionando Enter
    caja_password.bind("<Return>", iniciar_sesion)

    tk.Button(
        login,
        text="Iniciar sesión",
        command=iniciar_sesion,
        width=20,
        bg="#1f6aa5",
        fg="white",
        font=("Arial", 10, "bold")
    ).pack(pady=10)