import tkinter as tk
from tkinter import messagebox
import psycopg2

from conexion import conectar, consulta_usuarios

def mostrar_login(ventana, al_conectar):

    ventana.title("Inicio de sesión")
    ventana.geometry("900x500")
    ventana.resizable(False, False)
    ventana.configure(bg="#F0F2F5")

    login = tk.Frame(
        ventana,
        bg="white",
        relief="solid",
        borderwidth=1
    )

    login.place(
        relx=0.5,
        rely=0.5,
        anchor="center",
        width=360,
        height=400
    )

    encabezado = tk.Frame(
        login,
        bg="#1F4E79",
        height=100
    )

    encabezado.pack(fill="x")
    encabezado.pack_propagate(False)

    tk.Label(
        encabezado,
        text="NÚCLEO",
        font=("Arial", 22, "bold"),
        fg="white",
        bg="#1F4E79"
    ).pack(pady=(20, 3))

    tk.Label(
        encabezado,
        text="Sistema de administración de datos",
        font=("Arial", 9),
        fg="#DCE8F5",
        bg="#1F4E79"
    ).pack()

    formulario = tk.Frame(
        login,
        bg="white"
    )

    formulario.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=20
    )

    tk.Label(
        formulario,
        text="Inicio de sesión",
        font=("Arial", 16, "bold"),
        bg="white",
        fg="#333333"
    ).pack(pady=(0, 20))

    # Usuario
    tk.Label(
        formulario,
        text="Usuario",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#333333"
    ).pack(anchor="w")

    caja_usuario = tk.Entry(
        formulario,
        font=("Arial", 11),
        relief="solid",
        borderwidth=1
    )

    caja_usuario.pack(
        fill="x",
        pady=(5, 15),
        ipady=6
    )

    # Contraseña
    tk.Label(
        formulario,
        text="Contraseña",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#333333"
    ).pack(anchor="w")

    caja_password = tk.Entry(
        formulario,
        show="*",
        font=("Arial", 11),
        relief="solid",
        borderwidth=1
    )

    caja_password.pack(
        fill="x",
        pady=(5, 20),
        ipady=6
    )
    def iniciar_sesion():
        usuario = caja_usuario.get().strip()
        password = caja_password.get()

        if usuario == "" or password == "":
            messagebox.showwarning(
                "Campos vacíos",
                "Ingresa tu usuario y contraseña.",
                parent=ventana
            )
            return

        conexion = None
        try:
            conexion = conectar()
            usuario_valido = consulta_usuarios(conexion, usuario, password)
        except psycopg2.Error:
            if conexion is not None:
                conexion.close()
            messagebox.showerror(
                "Error de conexión",
                "No se pudo conectar con la base de datos.",
                parent=ventana
            )
            return

        if not usuario_valido:
            conexion.close()
            messagebox.showerror(
                "Error de inicio de sesión",
                "Usuario o contraseña incorrectos.",
                parent=ventana
            )
            return

        nombre_usuario, rol = usuario_valido
        perfil = "Administrador" if str(rol) == "1" else "Usuario normal" if str(rol) == "2" else "Rol no definido"
        messagebox.showinfo(
            "Inicio de sesión exitoso",
            f"Bienvenido, {nombre_usuario}!\nPerfil: {perfil}",
            parent=ventana
        )
        login.destroy()
        al_conectar(conexion, nombre_usuario, rol)

    def cancelar():

        caja_usuario.delete(0, tk.END)
        caja_password.delete(0, tk.END)
        caja_usuario.focus_set()

    botones = tk.Frame(
        formulario,
        bg="white"
    )

    botones.pack(fill="x")

    tk.Button(
        botones,
        text="Cancelar",
        command=cancelar,
        width=12,
        bg="#E0E4E8",
        fg="#333333",
        activebackground="#D0D5DA",
        relief="flat",
        font=("Arial", 10),
        cursor="hand2"
    ).pack(side="left", padx=(0, 5), ipady=5)

    tk.Button(
        botones,
        text="Iniciar sesión",
        command=iniciar_sesion,
        width=15,
        bg="#1F4E79",
        fg="white",
        activebackground="#163A5A",
        activeforeground="white",
        relief="flat",
        font=("Arial", 10, "bold"),
        cursor="hand2"
    ).pack(side="right", ipady=5)

    # Permitir iniciar sesión presionando Enter
    ventana.bind("<Return>", lambda event: iniciar_sesion())

    caja_usuario.focus_set()
