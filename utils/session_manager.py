import os
import pandas as pd
import streamlit as st
from config import TEMP_FILE
from utils.data_loader import load_data

def inicializar_sesion(temp_file):
    """
    Inicializa la sesión desde un archivo Excel previamente cargado.
    Restaura el dataframe original y columnas necesarias.
    """
    if not os.path.exists(temp_file):
        return False

    df_loaded = load_data(temp_file)

    st.session_state.orig_df = df_loaded.copy()
    st.session_state.df = df_loaded.copy()

    # 🔁 Agregar columna 'Seleccionar' si no existe
    if "Seleccionar" not in st.session_state.df.columns:
        st.session_state.df.insert(0, "Seleccionar", False)

    # 🛒 Restaurar marcas de orden desde 'selected_codigos'
    codigos_en_orden = st.session_state.get("selected_codigos", set())
    st.session_state.df["🛒 Orden"] = st.session_state.df["Código"].astype(str).apply(
        lambda c: "✅" if c in codigos_en_orden else ""
    )

    return True
