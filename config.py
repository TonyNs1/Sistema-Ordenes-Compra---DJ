# config.py

import os
import tempfile
from pathlib import Path

# ──────────────────────────────────────────────────────────────
# RUTAS TEMPORALES
# ──────────────────────────────────────────────────────────────
TEMP_FILE = os.path.join(tempfile.gettempdir(), "ultimo_archivo.xlsx")

# ──────────────────────────────────────────────────────────────
# RUTAS PERSISTENTES
# ──────────────────────────────────────────────────────────────
RUTA_BASE = Path(__file__).resolve().parent

# Historial persistente de órdenes
RUTA_HISTORIAL = RUTA_BASE / "data" / "historial_ordenes.json"

# Carpeta fija para exportar órdenes (escritorio)
CARPETA_EXPORTACIONES = Path.home() / "Desktop" / "Ordenes de Compra"

# Plantilla oficial para el ERP
ARCHIVO_MACHOTE = RUTA_BASE / "Compra_OC_carga_masiva.xlsx"

# ──────────────────────────────────────────────────────────────
# COLUMNAS DE TABLAS
# ──────────────────────────────────────────────────────────────
VISIBLE_COLUMNS = [
    "Eliminar", "Alerta", "Código", "Nombre",
    "Promedio mensual", "Existencias", "Cantidad a comprar",
    "Último costo", "Fecha última compra", "Último proveedor"
]

# Columnas requeridas por el machote ERP
COLUMNAS_MACHOTE = [
    "Código",
    "Cantidad comprada",
    "Costo unitario de la compra",
    "Descuento"
]


