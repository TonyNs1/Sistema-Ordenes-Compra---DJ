def apply_filters(df, extra):
    """
    Reordena las columnas para mostrar primero las importantes.
    Agrega columnas extra seleccionadas por el usuario (sin aplicar filtros de valores).

    Args:
        df (pd.DataFrame): DataFrame original.
        extra (list): Lista de columnas adicionales seleccionadas.

    Returns:
        pd.DataFrame: DataFrame con columnas reorganizadas y extra agregadas si existen.
    """
    df_filtered = df.copy()

    columnas_base = [
        'Alerta', 'Código', 'Nombre', 'Promedio mensual',
        'Existencias', 'Cantidad a comprar', 'Último costo',
        'Fecha última compra', 'Último proveedor'
    ]

    # Mantener solo columnas existentes
    columnas_orden = [c for c in columnas_base if c in df_filtered.columns]
    columnas_extra = [c for c in extra if c in df_filtered.columns and c not in columnas_orden]

    columnas_finales = columnas_orden + columnas_extra

    # Solo devuelve columnas válidas
    return df_filtered[columnas_finales]
