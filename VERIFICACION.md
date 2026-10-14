# Verificación — 14 de octubre de 2026

Esta revisión se realizó sobre la copia actual del proyecto. Sustituye el informe anterior, que citaba archivos ausentes y resultados de otra copia.

## Limpieza realizada

- Retirados `README_GITHUB.md` (publicación y 15 commits, fuera de la pauta proporcionada) y `readme` (duplicado).
- Retirado `musicpro_backend/.gitignore`: repetía reglas ya presentes en el `.gitignore` principal.
- Simplificadas las guías; retiradas las referencias a otras evaluaciones, pantallas públicas inexistentes, documentos ausentes y diagramas adicionales.
- Conservados modelos, validaciones, configuración de Admin, comandos y las cinco migraciones de negocio: corresponden a los requisitos o sostienen su funcionamiento.
- Conservadas las pruebas existentes de CRUD, filtros, modelos y Faker como apoyo a la verificación.
- Un único diagrama PNG se entrega fuera de la carpeta del proyecto. Se contrastaron sus 53 columnas y 11 claves foráneas con las diez tablas reales.

## Comprobaciones ejecutadas

Se utilizó Python 3.12.14 en un entorno de comprobación separado, con las versiones de `requirements.txt`: Django 6.1.1 y Faker 40.40.0.

- `check`: sin problemas.
- `makemigrations --check --dry-run`: sin cambios pendientes.
- `test Core --noinput`: 40 pruebas aprobadas.
- La base local estaba sin tablas. Se aplicaron las migraciones existentes: 20 tablas, incluidas las diez del negocio, y cero migraciones pendientes.
- Conexión SQLite verificada mediante `SELECT 1`; claves foráneas sin infracciones.
- Se instaló Faker 40.40.0, que faltaba en `.venv`.

El intérprete de `.venv` apunta a Python 3.15 y su ejecución quedó bloqueada por permisos de acceso en esta sesión. Las pruebas se realizaron con el intérprete separado indicado arriba; no se comprobó el arranque mediante `servidor.bat`. El entorno existente contiene Django 6.1.2; para reproducir exactamente las comprobaciones, instala las versiones de `requirements.txt` en un entorno funcional.

## Cargas comprobadas en una base separada

No se añadieron los datos masivos a `db.sqlite3`. Se usó una base de ensayo fuera del proyecto, con lote de 1.000 y semilla 42. Cada ejecución fue aditiva y se verificó su diferencia de conteo.

| Productos solicitados | Antes | Después | Segundos |
| ---: | ---: | ---: | ---: |
| 100 | 0 | 100 | 3.35 |
| 1000 | 100 | 1100 | 0.81 |
| 100000 | 1100 | 101100 | 82.34 |
| 1000000 | 101100 | 1101100 | 740.32 |

También se ejecutó una muestra de 20 productos con `--completo` y lote de 7, para verificar datos relacionados. El comando comprobó compras, ventas, detalles y movimientos; `PRAGMA foreign_key_check` no encontró infracciones.

La base local quedó con la estructura preparada, sin datos ficticios ni superusuario. Para utilizar Admin, crea tu cuenta con `python manage.py createsuperuser`. Las cuatro cargas deben repetirse con el docente como solicita la pauta; estas comprobaciones no sustituyen esa demostración.


## Actualización: página pública de bodega

Se añadió la portada en `/` y la ficha `/productos/<id>/`, conectadas a los modelos existentes. `Ver el sitio` apunta a la portada. El administrador continúa disponible en `/admin/`.

Se ejecutaron `check`, `makemigrations --check --dry-run` y `test Core --noinput` con el entorno `.venv` de esta copia y Django 6.1.1: sin problemas de configuración, sin migraciones nuevas y **46 pruebas aprobadas**. Las seis pruebas nuevas comprueban resumen, búsqueda/filtros, parámetros inválidos, paginación, ficha pública, rechazo de escrituras, escape de texto y estado vacío. Se actualizó la prueba antigua que exigía tener únicamente rutas de Admin.

La página incluye reglas adaptables a móvil; la inspección visual en navegador quedó pendiente porque no se autorizó a Codex a acceder al servidor local. No se modificaron modelos ni registros existentes.

## Mejoras del inventario y nueva comprobación

Se conservó el arranque directo con `manage.py runserver` y se retiró el lanzador por lotes según los cambios locales del estudiante. El README incluye instalación desde una copia nueva, conexión SQLite, migraciones, recorrido del CRUD, cargas de Faker y soluciones a errores habituales.

La consulta pública permite buscar también por ubicación y ordenar por menor stock. El orden alfabético usa `Lower` para evitar separar mayúsculas y minúsculas según el comportamiento de SQLite. Los enlaces de paginación conservan solamente los filtros válidos, y las fichas permiten volver a la consulta y página anteriores. Los destinos externos o ajenos al inventario se descartan al construir el enlace de regreso.

Los números de página negativos, no numéricos o excesivamente largos se normalizan a la primera página. Se añadieron descripciones para la tabla y los filtros, identificación de la página actual, controles táctiles más amplios y una explicación del umbral de reposición. Los finales de línea de los archivos de texto se definen en `.gitattributes`.

Comprobación ejecutada con Django 6.1.1:

- `manage.py check`: sin problemas.
- `manage.py makemigrations --check --dry-run`: sin cambios pendientes.
- `manage.py test Core --noinput`: **52 pruebas aprobadas**.
- Revisión de Git: sin errores de espacios; no se incluyen bases SQLite, archivos `.env` ni el entorno virtual.

Las seis pruebas de regresión nuevas cubren parámetros de búsqueda, búsqueda por ubicación, orden alfabético, menor stock, regreso desde la ficha y números de página inválidos. Las pruebas anteriores de CRUD, integridad y Faker continúan pasando. No se modificó la estructura de los modelos ni se cargaron datos nuevos en la base habitual durante esta revisión. La inspección visual sigue pendiente, como se indicó en la comprobación anterior.
