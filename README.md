# Administrador PostgreSQL

Aplicación de escritorio desarrollada en Python con Tkinter para conectarse a una base de datos PostgreSQL, consultar tablas, visualizar registros e insertar nuevas tuplas sin escribir SQL manualmente.

## Descripción

Este proyecto permite:

- Iniciar sesión con usuario y contraseña de PostgreSQL.
- Conectarse a una base de datos local o remota.
- Listar las tablas públicas disponibles.
- Consultar todos los registros de una tabla seleccionada.
- Mostrar los datos en una interfaz gráfica.
- Insertar nuevas filas en tablas seleccionadas mediante formularios generados automáticamente.

La lógica de conexión a la base de datos se encuentra en `administrador/conexion.py` y la interfaz gráfica principal se controla desde `administrador/main.py`.

## Tecnologías

- Python 3.x
- Tkinter (GUI)
- PostgreSQL
- psycopg2

## Estructura del proyecto

```text
GUI-PYTHON/
├── administrador/
│   ├── __pycache__/
│   ├── conexion.py
│   ├── consultas.py
│   ├── insertar.py
│   ├── login.py
│   ├── main.py
│   └── menu.py
├── .venv312/
├── .git/
└── README.md
```

## Requisitos

Antes de ejecutar la aplicación asegúrate de tener instalado:

- Python 3.10 o superior
- PostgreSQL
- pip
- Un usuario con acceso a la base de datos configurada

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/REDLINE4674/GUI-PYTHON.git
cd GUI-PYTHON
```

2. Crea y activa un entorno virtual (opcional pero recomendado):

```bash
python -m venv .venv
```

En Windows:

```bash
.venv\Scripts\activate
```

3. Instala la dependencia principal:

```bash
pip install psycopg2
```

> Si tu entorno lo requiere, también puedes usar `psycopg2-binary` en lugar de `psycopg2`.

## Configuración de conexión

El archivo `administrador/conexion.py` contiene la configuración por defecto de PostgreSQL:

```python
HOST = "localhost"
DATABASE = "NucleoDeDiagnostico"
PORT = "5433"
```

Debes ajustar estos valores si tu instancia de PostgreSQL usa otra IP, nombre de base de datos o puerto.

Ejemplo:

```python
HOST = "localhost"
DATABASE = "mi_base"
PORT = "5432"
```

## Ejecución

Desde la raíz del proyecto:

```bash
python administrador/main.py
```

La aplicación abrirá una ventana de inicio de sesión. Ingresando usuario y contraseña válidos, se conectará a PostgreSQL y mostrará el menú principal.

## Uso

1. Ingresa usuario y contraseña.
2. Selecciona una tabla desde el menú lateral.
3. Revisa los registros en la vista principal.
4. Haz clic en "Insertar tupla" para agregar un nuevo registro.

## Notas importantes

- La aplicación está enfocada a tablas dentro del esquema `public`.
- Los datos se muestran en una tabla visual de Tkinter.
- La lógica de inserción evita columnas generadas o de identidad, según la consulta SQL utilizada.
- La base de datos debe estar disponible antes de ejecutar la aplicación.

## Posibles mejoras futuras

- Agregar edición y eliminación de registros.
- Soporte para consultas SQL personalizadas.
- Mejor manejo de errores y validaciones de entrada.
- Exportación de datos a CSV o Excel.
- Autenticación más robusta y configuración desde archivo `.env`.

## Licencia

Este proyecto no incluye una licencia específica en este momento. Si deseas, puedes definir una licencia según el uso que le quieras dar.
