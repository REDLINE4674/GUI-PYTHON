# Administrador PostgreSQL

Aplicación de escritorio desarrollada en Python con Tkinter para conectarse a una base de datos PostgreSQL, consultar tablas, visualizar registros e insertar nuevas tuplas sin escribir SQL manualmente.

## Descripción

Este proyecto permite:

- Iniciar sesión con las credenciales guardadas en la tabla `usuarios`.
- Asignar acceso según el rol del usuario.
- Conectarse a una base de datos local o remota.
- Listar las tablas públicas disponibles.
- Consultar los registros de una tabla seleccionada bajo demanda.
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

La aplicación abrirá una ventana de inicio de sesión. Al validar el usuario en la tabla `usuarios`, obtiene su nombre y rol, y luego muestra el menú permitido para ese perfil.

## Uso

1. Ingresa tu nombre de usuario y contraseña.
2. Selecciona una tabla del menú lateral.
3. Pulsa **Consultar registros** para cargar los datos y ver el total encontrado. La tabla no aparece hasta solicitar la consulta.
4. Si tienes rol de administrador, pulsa **Insertar registro** para agregar una fila.
5. Pulsa **Regresar al menú principal** para volver a la pantalla de inicio.

### Perfiles

La tabla `usuarios` debe tener las columnas `nombre`, `contrasena` y `rol`.

- `rol = 1`: administrador. Puede consultar todas las tablas públicas disponibles y tiene habilitada la inserción de registros.
- `rol = 2`: usuario normal. Solo puede consultar la tabla `pacientes` (o `paciente`, si así se llama en la base de datos); no tiene habilitada la inserción.

La aplicación actualmente no ofrece operaciones para editar o eliminar registros.

## Notas importantes

- La aplicación está enfocada a tablas dentro del esquema `public`.
- Los datos se muestran en una tabla visual de Tkinter.
- La lógica de inserción evita columnas generadas o de identidad, según la consulta SQL utilizada.
- La base de datos debe estar disponible antes de ejecutar la aplicación.
- La configuración de conexión a PostgreSQL se encuentra en `administrador/conexion.py`.

## Posibles mejoras futuras

- Agregar edición y eliminación de registros.
- Soporte para consultas SQL personalizadas.
- Mejor manejo de errores y validaciones de entrada.
- Exportación de datos a CSV o Excel.
- Autenticación más robusta y configuración desde archivo `.env`.

## Licencia

Este proyecto no incluye una licencia específica en este momento. Si deseas, puedes definir una licencia según el uso que le quieras dar.
