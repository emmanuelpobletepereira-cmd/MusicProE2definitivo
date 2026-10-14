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

## Administrar la bodega

En `/admin/`, inicia sesión con tu superusuario. Los modelos registrados son categorías, marcas, proveedores, clientes, productos, compras, detalles de compras, ventas, detalles de ventas y movimientos.

Para demostrar el CRUD de un producto:

1. Crea una categoría de prueba.
2. Añade un producto con código único, nombre, categoría, ubicación y existencias.
3. Búscalo por código y comprueba que está guardado.
4. Modifica su ubicación o cantidad y vuelve a consultarlo.
5. Elimínalo y verifica que desapareció. Elimina después la categoría de prueba.

Si el producto tiene detalles o movimientos asociados, Django protege su eliminación. Primero debes retirar esos registros dependientes.

El administrador incluye filtros, búsquedas y formularios personalizados. **El stock se edita manualmente**: crear, editar o eliminar un movimiento no recalcula automáticamente las existencias del producto. Compras y ventas muestran subtotales y totales calculados.

La página pública permite consultar el inventario sin iniciar sesión. La modificación de registros requiere acceso al administrador y permisos sobre los modelos.

## Datos ficticios y cargas

Para generar una muestra con Faker:

```bat
.venv\Scripts\python.exe manage.py cargar_datos --cantidad 100 --semilla 42
```

Para poblar también compras, ventas, detalles y movimientos, utiliza una muestra pequeña:

```bat
.venv\Scripts\python.exe manage.py cargar_datos --cantidad 20 --lote 7 --semilla 42 --completo
```

`--cantidad` cuenta productos nuevos; las categorías y los registros relacionados no están incluidos en esa cifra. Cada ejecución añade registros. Repetir la semilla no evita una carga adicional: los códigos son únicos por ejecución.

La pauta pide demostrar 100, 1.000, 100.000 y 1.000.000 datos con el docente. Cambia `--cantidad` a cada valor y verifica los conteos antes y después con `verificar_bd`. Puedes usar `--lote 1000` para limitar los objetos preparados en memoria.

Para ensayar en otra base desde CMD, elige un nombre nuevo:

```bat
set MUSICPRO_DB_PATH=ensayo-100.sqlite3
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py cargar_datos --cantidad 100 --semilla 42
.venv\Scripts\python.exe manage.py verificar_bd
set MUSICPRO_DB_PATH=
```

Repite con un archivo distinto para cada volumen. Quitar la variable vuelve a seleccionar `db.sqlite3`; no elimina la base de ensayo. Los tiempos medidos están en `VERIFICACION.md`.

## Comprobar el proyecto y resolver errores

```bat
.venv\Scripts\python.exe manage.py check
.venv\Scripts\python.exe manage.py test Core --noinput
```

Las pruebas utilizan una base temporal y no borran la base habitual.

| Mensaje o situación | Qué revisar |
| --- | --- |
| `No module named django` | Instala `requirements.txt` con el Python de `.venv`. |
| `no such table` | Ejecuta `manage.py migrate` en la base seleccionada. |
| El puerto 8000 está ocupado | Detén el servidor anterior o ejecuta `manage.py runserver 8001`. |
| El inventario aparece vacío | Crea productos en Admin o ejecuta una carga pequeña con Faker. |
| No puedes entrar en Admin | Crea el superusuario en la misma base con la que iniciaste el servidor. |
| El navegador muestra una versión anterior | Recarga con Ctrl+F5 y comprueba la carpeta desde la que ejecutaste el servidor. |

Cuando uses otro puerto, inclúyelo en la dirección del navegador, por ejemplo http://127.0.0.1:8001/.
