import psycopg2
from psycopg2 import sql


# Datos de conexión
HOST = "localhost"
DATABASE = "NucleoDeDiagnostico"
PORT = "5433"
USUARIO = "admin"
PASSWORD = "1234"

# Conectar a PostgreSQL
def conectar():

    conexion = psycopg2.connect(
        host=HOST,
        database=DATABASE,
        user=USUARIO,
        password=PASSWORD,
        port=PORT
    )

    return conexion


# Obtener las tablas de la base de datos
def obtener_tablas(conexion):

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """)

    tablas = cursor.fetchall()

    cursor.close()

    return tablas


# Consultar los registros de una tabla
def consultar_registros(conexion, nombre_tabla):

    cursor = conexion.cursor()

    consulta = sql.SQL("SELECT * FROM {}").format(
        sql.Identifier(nombre_tabla)
    )

    cursor.execute(consulta)

    columnas = [columna[0] for columna in cursor.description]

    registros = cursor.fetchall()

    cursor.close()

    return columnas, registros


# Obtener las columnas que se pueden insertar
def obtener_columnas(conexion, nombre_tabla):

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

    return columnas

def consulta_usuarios(conexion, nombre, contrasena):
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            SELECT nombre, rol
            FROM usuarios
            WHERE nombre = %s AND contrasena = %s
        """, (nombre, contrasena))
        return cursor.fetchone()
    finally:
        cursor.close()

# Insertar un registro
def insertar_registro(conexion, nombre_tabla, nombres, valores):

    cursor = conexion.cursor()

    if nombres:

        consulta = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(

            sql.Identifier(nombre_tabla),

            sql.SQL(", ").join(
                map(sql.Identifier, nombres)
            ),

            sql.SQL(", ").join(
                sql.Placeholder() for valor in valores
            )
        )

        cursor.execute(consulta, valores)

    else:

        consulta = sql.SQL("INSERT INTO {} DEFAULT VALUES").format(
            sql.Identifier(nombre_tabla)
        )

        cursor.execute(consulta)

    conexion.commit()

    cursor.close()
