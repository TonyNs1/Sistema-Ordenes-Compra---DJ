# utils/ordenes.py
import os
import json
import pandas as pd
import streamlit as st

# ----------------------------------------------------------------------
# 1. Inicializador simple y seguro
# ----------------------------------------------------------------------
def init_orden() -> None:
    """Asegura las estructuras en session_state para manejar la orden."""
    st.session_state.setdefault("orden_en_curso", [])
    st.session_state.setdefault("selected_codigos", set())
    st.session_state.setdefault("nombre_orden", "")
    st.session_state.setdefault("ruta_ultima_orden", None)
    st.session_state.setdefault("mostrar_descarga_final", False)

# ----------------------------------------------------------------------
# 2. Agregar productos únicos
# ----------------------------------------------------------------------
def add_items(df_nuevos: pd.DataFrame) -> None:
    """
    Agrega filas al pedido, evitando duplicados por 'Código'.
    df_nuevos debe tener al menos: Código, Nombre, Cantidad a comprar, Último costo, Descuento
    """
    if df_nuevos.empty:
        st.warning("⚠️ No hay filas válidas para agregar.")
        return

    columnas = ["Código", "Nombre", "Cantidad a comprar", "Último costo", "Descuento"]
    for col in columnas:
        if col not in df_nuevos.columns:
            df_nuevos[col] = 0

    df_nuevos["Código"] = df_nuevos["Código"].astype(str)

    codigos_existentes = st.session_state["selected_codigos"]
    df_filtrado = df_nuevos[~df_nuevos["Código"].isin(codigos_existentes)]

    if df_filtrado.empty:
        st.info("ℹ️ Los productos seleccionados ya están en la orden.")
        return

    # Asegurar campo Descuento numérico
    df_filtrado["Descuento"] = pd.to_numeric(df_filtrado["Descuento"], errors="coerce").fillna(0)

    st.session_state["orden_en_curso"].extend(df_filtrado.to_dict(orient="records"))
    st.session_state["selected_codigos"].update(df_filtrado["Código"].tolist())

# ----------------------------------------------------------------------
# 3. Remover productos por índices
# ----------------------------------------------------------------------
def remove_items(idx_list) -> None:
    """Quita productos de la orden y actualiza el set de códigos."""
    for idx in sorted(idx_list, reverse=True):
        codigo = st.session_state["orden_en_curso"][idx]["Código"]
        st.session_state["orden_en_curso"].pop(idx)
        st.session_state["selected_codigos"].discard(str(codigo))

# ----------------------------------------------------------------------
# 4. Cerrar la orden
# ----------------------------------------------------------------------
def close_order(export_fn, nombre_orden="General"):
    """
    Llama a export_fn(DataFrame) -> ruta, reinicia el estado y devuelve la ruta.
    export_fn debe aceptar (df, proveedor=nombre_orden) o similar (se usa *args / **kwargs).
    """
    orden = st.session_state.get("orden_en_curso", [])
    if not orden:
        st.warning("⚠️ La orden está vacía.")
        return None

    df_export = pd.DataFrame(orden)
    if df_export.empty:
        st.warning("⚠️ No hay datos válidos para exportar.")
        return None

    try:
        ruta_exportada = export_fn(df_export, proveedor=nombre_orden)
    except TypeError:
        # Si export_fn no acepta proveedor
        ruta_exportada = export_fn(df_export)

    # Reset de estado
    st.session_state["orden_en_curso"] = []
    st.session_state["selected_codigos"] = set()
    st.session_state["ruta_ultima_orden"] = ruta_exportada
    st.session_state["mostrar_descarga_final"] = True

    return ruta_exportada
