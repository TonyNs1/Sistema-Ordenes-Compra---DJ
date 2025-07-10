def apply_filters(df, extra):
    """
    Aplica el orden de columnas y agrega columnas extra seleccionadas (sin filtros).
    """
    df_filtered = df.copy()

    columnas_orden = [
        'Alerta', 'Código', 'Nombre', 'Promedio mensual', 'Existencias',
        'Cantidad a comprar', 'Último costo', 'Fecha última compra', 'Último proveedor'
    ]
    columnas_extra = [c for c in extra if c in df_filtered.columns]
    columnas_mostrar = columnas_orden + columnas_extra

    return df_filtered[columnas_mostrar]

