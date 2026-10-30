import tkinter as tk
import psycopg

conexion = psycopg.connect(
    host="localhost",
    port=5433,
    dbname="gui",
    user="admin",
    password="1234"
)

print("Conexión exitosa")

conexion.close()

ventana = tk.Tk()

ventana.title("Mi aplicación")

ventana.mainloop()

