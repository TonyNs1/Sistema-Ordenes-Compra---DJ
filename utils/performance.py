# utils/performance.py

import pandas as pd
import streamlit as st
from hashlib import md5

def _hash_dataframe(df: pd.DataFrame) -> str:
    """Devuelve un hash MD5 único para un DataFrame dado."""
    return md5(pd.util.hash_pandas_object(df, index=True).values).hexdigest()

def cachear_dataframe(nombre: str, df: pd.DataFrame):
    """
    Guarda una versión cacheada del DataFrame en session_state.
    Se usa para evitar cálculos repetidos.
    """
    hash_df = _hash_dataframe(df)
    st.session_state[f"{nombre}_df"] = df
    st.session_state[f"{nombre}_hash"] = hash_df

def obtener_cache_dataframe(nombre: str, df_actual: pd.DataFrame) -> pd.DataFrame | None:
    """
    Devuelve el DataFrame cacheado si no ha cambiado.
    Si el DataFrame actual tiene un hash diferente, retorna None.
    """
    hash_actual = _hash_dataframe(df_actual)
    hash_guardado = st.session_state.get(f"{nombre}_hash")
    if hash_actual == hash_guardado:
        return st.session_state.get(f"{nombre}_df")
    return None

def limpiar_cache(nombre: str):
    """Elimina el cache almacenado por nombre."""
    st.session_state.pop(f"{nombre}_df", None)
    st.session_state.pop(f"{nombre}_hash", None)
