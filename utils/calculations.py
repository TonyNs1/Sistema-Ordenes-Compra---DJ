import pandas as pd

def compute_suggestions(df, dias_min, dias_max, margen_extra):
    df = df.copy()
    df['Promedio mensual'] = pd.to_numeric(df.get('Promedio mensual', 0), errors='coerce').fillna(0)
    df['Existencias'] = pd.to_numeric(df.get('Existencias', 0), errors='coerce').fillna(0)

    df['Mínimo sugerido'] = (df['Promedio mensual'] / 30) * dias_min
    df['Máximo sugerido'] = (df['Promedio mensual'] / 30) * dias_max * (1 + (margen_extra / 100))
    df['Cantidad a comprar'] = df['Máximo sugerido'] - df['Existencias']
    import math
    df['Cantidad a comprar'] = df['Cantidad a comprar'].apply(lambda x: max(0, math.floor(x)))


    def clasificar_alerta(row):
        ex = row['Existencias']
        mini = row['Mínimo sugerido']
        maxi = row['Máximo sugerido']
        if ex <= 0:
            return '🔴'
        elif ex < mini:
            return '🟡'
        elif mini <= ex <= maxi:
            return '🟢'
        elif ex <= maxi * 1.2:
            return '🟠'
        else:
            return '🔵'

    df['Alerta'] = df.apply(clasificar_alerta, axis=1)
    return df