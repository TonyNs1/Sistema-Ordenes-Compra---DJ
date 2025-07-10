
import pandas as pd
import unicodedata

def load_data(uploaded_file):
    df = pd.read_excel(uploaded_file, header=1)
    df.columns = df.columns.str.strip()

    def normalize(col):
        return (
            unicodedata.normalize('NFKD', col)
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
    return df.rename(columns=renamed_cols).copy()
