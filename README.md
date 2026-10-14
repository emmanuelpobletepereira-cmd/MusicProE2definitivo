# Music Pro — Bodega e inventario

Aplicación Django con inventario público, fichas de productos y administración de la bodega. Utiliza SQLite y Faker para generar datos de prueba.

## Instalación en Windows

Abre CMD dentro de la carpeta que contiene `manage.py`. Necesitas Python instalado. Ejecuta cada comando por separado:

```bat
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py createsuperuser
.venv\Scripts\python.exe manage.py runserver
```

Si ya tienes `.venv`, omite el primer comando. Si ya creaste un superusuario, omite `createsuperuser`.

Abre http://127.0.0.1:8000/ para consultar el inventario. El administrador está en http://127.0.0.1:8000/admin/. Mantén la terminal abierta. Para detener el servidor, presiona Ctrl+C.

Para iniciar nuevamente, basta con:

```bat
.venv\Scripts\python.exe manage.py runserver
```

El entorno y la base local no se suben a GitHub. Cada equipo debe instalar las dependencias y aplicar las migraciones.

## Base de datos y migraciones

La conexión está en `musicpro_backend/settings.py`. El motor es SQLite y el archivo habitual es `db.sqlite3`, junto a `manage.py`.

```bat
.venv\Scripts\python.exe manage.py verificar_bd
.venv\Scripts\python.exe manage.py showmigrations bodega
.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

`verificar_bd` identifica la conexión, las tablas y los registros. Las migraciones de la aplicación están en `Core/migrations/`; su etiqueta de Django es `bodega`.

Cuando cambies un modelo en `Core/models.py`, genera y aplica una nueva migración:

```bat
.venv\Scripts\python.exe manage.py makemigrations bodega
.venv\Scripts\python.exe manage.py migrate
```

Conserva todo el historial. El diagrama se entrega aparte y debe actualizarse si cambian los modelos.
