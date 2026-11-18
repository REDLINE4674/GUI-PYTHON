import tkinter as tk
from login import mostrar_login
from menu import mostrar_menu

# Crear ventana principal
ventana = tk.Tk()

ventana.title("Administrador PostgreSQL")
ventana.geometry("900x500")

# Abrir el menú después de iniciar sesión
def iniciar_aplicacion(conexion, usuario):

    mostrar_menu(
        ventana,
        conexion,
        usuario
    )

# Cerrar la aplicación
def cerrar_aplicacion():

    if conexion_actual:

        conexion_actual.close()

    ventana.destroy()

# Variable para guardar la conexión
conexion_actual = None

# Recibir conexión desde el login
def conexion_exitosa(conexion, usuario):

    global conexion_actual

    conexion_actual = conexion

    iniciar_aplicacion(
        conexion,
        usuario
    )

# Configurar cierre de ventana
ventana.protocol(
    "WM_DELETE_WINDOW",
    cerrar_aplicacion
)

# Mostrar pantalla de inicio de sesión
mostrar_login(
    ventana,
    conexion_exitosa
)

# Ejecutar aplicación
ventana.mainloop()
