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
    ▸ Si no se sube, intenta restaurar sesión anterior desde disco.
    """
    uploaded = st.file_uploader("📤 Cargar archivo Excel", type="xlsx")

    if uploaded:
        nuevo_hash = _file_hash(uploaded.getvalue())
        hash_anterior = st.session_state.get("hash_archivo")

        # 🆕 ARCHIVO NUEVO
        if nuevo_hash != hash_anterior:
            for k in list(st.session_state.keys()):
                del st.session_state[k]

            if os.path.exists(TMP_STATE):
                os.remove(TMP_STATE)

            with open(temp_file, "wb") as f:
                f.write(uploaded.getbuffer())
            st.session_state.hash_archivo = nuevo_hash

            df = load_data(temp_file)
            st.session_state.orig_df = df.copy()
            st.session_state.df = df.copy()

            st.success("✅ Archivo Excel cargado correctamente (nuevo)")
            return True

        # 📁 ARCHIVO IGUAL AL ANTERIOR
        else:
            if "df" not in st.session_state:
                with open(temp_file, "wb") as f:
                    f.write(uploaded.getbuffer())

                df = load_data(temp_file)
                st.session_state.orig_df = df.copy()
                st.session_state.df = df.copy()
                st.info("ℹ️ Archivo igual al anterior, se restauraron los datos")
            else:
                st.info("ℹ️ Estás trabajando con el mismo archivo cargado previamente")
            return True

    # 🧠 SESIÓN GUARDADA EN DISCO
    elif inicializar_sesion(temp_file):
        st.info("ℹ️ Se restauró la sesión anterior desde disco")
        return True

    # 🚫 NADA CARGADO
    st.warning("⚠️ Necesitas subir un archivo Excel para comenzar")
    return False


