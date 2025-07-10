import pandas as pd
import unicodedata


def load_data(uploaded_file):
    try:
        # Leer archivo ignorando errores comunes
        df = pd.read_excel(uploaded_file, header=1, engine="openpyxl")
        df.columns = df.columns.str.strip()

        def normalize(col):
            return (
                unicodedata.normalize('NFKD', str(col))
                .encode('ascii', errors='ignore')
                .decode('ascii')
                .strip()
                .lower()
            )

        df.columns = [normalize(c) for c in df.columns]

        col_map = {
            'codigo': 'Código',
            'nombre': 'Nombre',
            'promedio mensual vendido': 'Promedio mensual',
            'promedio mensual': 'Promedio mensual',
            'existencias': 'Existencias',
            'costo ultima compra': 'Último costo',
            'ultimo costo unitario con descuento': 'Último costo',
            'ultimo proveedor': 'Último proveedor',
            'proveedor': 'Último proveedor',
            'categoria': 'Categoría',
            'categoría': 'Categoría',
            'ultima compra': 'Fecha última compra'
        }

        renamed_cols = {k: v for k, v in col_map.items() if k in df.columns}
        df = df.rename(columns=renamed_cols)

        # Normalizar valores vacíos o faltantes críticos
        if "Código" in df.columns:
            df = df[df["Código"].notna()]  # Filtrar filas sin código

        return df.reset_index(drop=True).copy()

    except Exception as e:
        raise RuntimeError(f"❌ Error al cargar el archivo Excel: {e}")
