import streamlit as st
import os
from views.vista_principal import vista_principal

# Configurar app
st.set_page_config(page_title="📦 Depósito Jiménez", layout="wide")
RUTA_ORDENES = os.path.expanduser("~/Desktop/Ordenes de Compra")

# Menú lateral con pestañas
opciones = ["📦 Inventario", "📜 Historial de Órdenes"]
seleccion = st.sidebar.radio("Ir a:", opciones)

# Manejador principal con control de errores
try:
    if seleccion == "📦 Inventario":
        vista_principal(RUTA_ORDENES)
    elif seleccion == "📜 Historial de Órdenes":
        vista_historial(RUTA_ORDENES)
except Exception as e:
    st.error("❌ Ocurrió un error inesperado al ejecutar la aplicación.")
    st.exception(e)
