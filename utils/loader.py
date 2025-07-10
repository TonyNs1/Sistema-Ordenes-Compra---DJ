import os
import hashlib
import streamlit as st
from utils.data_loader import load_data
from utils.session_manager import inicializar_sesion

TMP_STATE = os.path.join(os.path.dirname(__file__), "orden_tmp.json")

def _file_hash(fileobj: bytes) -> str:
    """Devuelve el hash MD5 de un archivo cargado para comparar si cambió."""
    return hashlib.md5(fileobj).hexdigest()

def cargar_archivo_excel(temp_file: str) -> bool:
    """
    ▸ Carga un archivo Excel solo si es diferente al ya cargado.
    ▸ Si es el mismo, mantiene filtros, columnas y orden en curso.
    ▸ Si no se sube, intenta restaurar sesión anterior desde disco (solo si no hay sesión activa).
    """
    uploaded = st.file_uploader("📤 Cargar archivo Excel", type="xlsx")

    # Usuario sube archivo
    if uploaded:
        nuevo_hash = _file_hash(uploaded.getvalue())
        hash_anterior = st.session_state.get("hash_archivo")

        if nuevo_hash != hash_anterior:
            # Reiniciamos todo si es archivo nuevo
            st.session_state.clear()

            # Borrar archivo anterior
            if os.path.exists(TMP_STATE):
                os.remove(TMP_STATE)

            # Guardar archivo
            with open(temp_file, "wb") as f:
                f.write(uploaded.getbuffer())

            st.session_state.hash_archivo = nuevo_hash
            st.session_state.archivo_nuevo = True

            # Cargar datos
            df = load_data(temp_file)
            st.session_state.orig_df = df.copy()
            st.session_state.df = df.copy()

            st.success("✅ Archivo nuevo cargado correctamente.")
            return True

        else:
            # Mismo archivo
            if "df" not in st.session_state:
                with open(temp_file, "wb") as f:
                    f.write(uploaded.getbuffer())
                df = load_data(temp_file)
                st.session_state.orig_df = df.copy()
                st.session_state.df = df.copy()

            st.session_state.archivo_nuevo = False
            st.info("ℹ️ Estás trabajando con el mismo archivo ya cargado.")
            return True

    # Restaurar sesión anterior si no hay nada en memoria
    if "df" not in st.session_state and inicializar_sesion(temp_file):
        st.session_state.archivo_nuevo = False
        st.info("ℹ️ Se restauró la sesión anterior desde disco.")
        return True

    st.warning("⚠️ Necesitas subir un archivo Excel para comenzar.")
    return False


