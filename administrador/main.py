import tkinter as tk
from login import mostrar_login
from menu import mostrar_menu

# Crear ventana principal
ventana = tk.Tk()

ventana.title("Nucleo de Diagnostico")
ventana.geometry("900x500")


# Abrir el menú después de iniciar sesión
def iniciar_aplicacion(conexion, usuario, rol):

    mostrar_menu(
        ventana,
        conexion,
        usuario,
        rol,
        cerrar_sesion
    )


# Cerrar la aplicación
def cerrar_aplicacion():

    if conexion_actual:

        conexion_actual.close()

    ventana.destroy()


# Variable para guardar la conexión
conexion_actual = None


def cerrar_sesion():

    global conexion_actual

    if conexion_actual:
        conexion_actual.close()
        conexion_actual = None

    for widget in ventana.winfo_children():
        widget.destroy()

    mostrar_login(
        ventana,
        conexion_exitosa
    )


# Recibir conexión desde el login
def conexion_exitosa(conexion, usuario, rol):

    global conexion_actual

    conexion_actual = conexion

    iniciar_aplicacion(
        conexion,
        usuario,
        rol
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
