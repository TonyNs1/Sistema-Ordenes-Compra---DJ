import os
import json
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment
import xlwings as xw

def exportar_usando_machote(df: pd.DataFrame, nombre_archivo: str, carpeta_destino: str, ruta_machote: str) -> str:
    try:
        # Ruta final
        ruta_salida = os.path.join(carpeta_destino, nombre_archivo)

        # Cargar machote
        wb = load_workbook(ruta_machote)
        ws = wb.active

        # Encabezado desde la fila 2
        fila = 2

        for _, row in df.iterrows():
            # Código como texto sin ".0"
            codigo_str = str(row["Código"]).replace(".0", "") if isinstance(row["Código"], (int, float)) else str(row["Código"])
            ws.cell(row=fila, column=1, value=codigo_str)

            # Números con 2 decimales
            ws.cell(row=fila, column=2, value=round(float(row["Cantidad comprada"]), 2))
            ws.cell(row=fila, column=3, value=round(float(row["Costo unitario de la compra"]), 2))
            ws.cell(row=fila, column=4, value=round(float(row["Descuento"]), 2))

            fila += 1

        # Ajustar alineación de todas las celdas
        for row in ws.iter_rows(min_row=2, max_row=fila - 1, min_col=1, max_col=4):
            for cell in row:
                cell.alignment = Alignment(horizontal="center", vertical="center")

        # Guardar archivo en disco
        wb.save(ruta_salida)
        wb.close()

        # ✅ Autoajuste con Excel real (Windows + Excel instalado)
        ajustar_excel_con_excel(ruta_salida)

        return ruta_salida

    except Exception as e:
        raise RuntimeError(f"❌ Error al exportar usando la plantilla. Detalles: {e}")


def ajustar_excel_con_excel(ruta: str):
    """Abre y guarda el archivo con Excel real para corregir estructura interna."""
    try:
        app = xw.App(visible=False)
        libro = app.books.open(ruta)
        libro.save()
        libro.close()
        app.quit()
    except Exception as e:
        print(f"⚠️ Error al ajustar con Excel: {e}")


def cargar_historial_ordenes(ruta_historial: str) -> list:
    if not os.path.exists(ruta_historial):
        return []
    with open(ruta_historial, "r", encoding="utf-8") as f:
        return json.load(f)


def exportar_orden_excel(df: pd.DataFrame, ruta: str) -> None:
    df.to_excel(ruta, index=False)

