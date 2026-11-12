# Lab 9 — Módulo de Exportación MVC

Proyecto MVC para consultar y registrar productos en PostgreSQL y exportar el inventario a CSV, TXT, JSON y PDF.

## Requisitos
- Python 3.10 o superior
- PostgreSQL
- DBeaver (opcional, para ejecutar el SQL)

## Instalación en PowerShell
Abre PowerShell dentro de la carpeta `Lab_9`:

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Si PowerShell bloquea la activación, puedes ejecutar directamente:
```powershell
.venv\\Scripts\\python.exe -m pip install -r requirements.txt
```

## Configuración de PostgreSQL
1. Copia `.env.example` y nombra la copia `.env`.
2. Edita `.env` y coloca la contraseña real de tu usuario PostgreSQL.
3. En DBeaver, conéctate a la misma base de datos indicada por `DB_NAME`.
4. Ejecuta `Model/database_squema.sql`.
5. El script trabaja con `login_system.products` y `login_system.users`. No crea una segunda tabla `public.products` ni elimina registros.

La tabla de productos se consulta con estos campos reales:
- `id_producto`
- `nombre`
- `precio`
- `cantidad`
- `descripcion`

El Modelo presenta al resto de la aplicación las claves `id`, `nombre`, `precio`, `stock` y `descripcion`.

Usuario inicial de laboratorio: `admin` / `admin123`, únicamente si el INSERT lo crea. Si la tabla ya tiene un usuario admin, `ON CONFLICT` no cambia su contraseña.

## Ejecución
```powershell
python main.py
```
En la pestaña **Inventario de Productos**, selecciona CSV, TXT, JSON o PDF y pulsa **Exportar Reporte**.

## Pruebas
```powershell
python -m unittest discover -s tests -v
```
Las pruebas del módulo de exportación no requieren conexión a PostgreSQL.

## Arquitectura
- `exporters.py`: clase abstracta `Exporter` y las clases `CSVExporter`, `TXTExporter`, `JSONExporter` y `PDFExporter`. Aquí viven los imports y la lógica de archivos.
- `Model/products_model.py`: consultas a `login_system.products`.
- `Controller/products_controller.py`: obtiene los datos y llama de forma polimórfica a `exporter.export(datos, ruta)`.
- `Views/home_view.py`: selector de formato y botón de exportación. No importa `csv`, `json` ni `fpdf`.

No se incluye el archivo `.env` en el ZIP ni en Git. Nunca compartas la contraseña de PostgreSQL.
