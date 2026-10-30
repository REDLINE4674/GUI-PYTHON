import tkinter as tk
from tkinter import messagebox
import psycopg


# FUNCIÓN PARA INICIAR SESIÓN

def iniciar_sesion():

    # Obtener información de los Entry
    usuario = entrada_usuario.get()
    password = entrada_password.get()

    # Comprobar que no estén vacíos
    if usuario == "" or password == "":
        messagebox.showwarning(
            "Advertencia",
            "Debes ingresar usuario y contraseña"
        )
        return

    try:

        # CONECTAR CON POSTGRESQL
       
        conexion = psycopg.connect(
            host="localhost",
            port=5433,
            dbname="gui",
            user="admin",
            password="1234"
        )

        # Crear cursor
        cursor = conexion.cursor()

        # CONSULTAR USUARIO
       
        cursor.execute(
            """
            SELECT id, username
            FROM usuarios
            WHERE username = %s
            AND password = %s
            """,
            (usuario, password)
        )

        # Obtener resultado
        resultado = cursor.fetchone()

        # COMPROBAR RESULTADO

        if resultado:

            messagebox.showinfo(
                "Login",
                "Inicio de sesión correcto"
            )

        else:

            messagebox.showerror(
                "Login",
                "Usuario o contraseña incorrectos"
            )

        # Cerrar cursor
        cursor.close()

        # Cerrar conexión
        conexion.close()

    except Exception as error:

        messagebox.showerror(
            "Error",
            f"No se pudo conectar con PostgreSQL:\n\n{error}"
        )

# VENTANA

ventana = tk.Tk()

ventana.title("Inicio de sesión")
ventana.geometry("400x300")

# TÍTULO

titulo = tk.Label(
    ventana,
    text="INICIAR SESIÓN",
    font=("Arial", 18)
)

titulo.pack(pady=20)

# USUARIO

tk.Label(
    ventana,
    text="Usuario:"
).pack()

entrada_usuario = tk.Entry(
    ventana,
    width=30
)

entrada_usuario.pack()


# CONTRASEÑA

tk.Label(
    ventana,
    text="Contraseña:"
).pack()

entrada_password = tk.Entry(
    ventana,
    width=30,
    show="*"
)

entrada_password.pack()

# BOTÓN

boton = tk.Button(
    ventana,
    text="Iniciar sesión",
    command=iniciar_sesion
)

boton.pack(pady=20)


# INICIAR TKINTER

ventana.mainloop()