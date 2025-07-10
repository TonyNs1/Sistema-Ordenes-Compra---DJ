# utils/ui.py

import streamlit as st

# ─────────────────────────────────────────
def mostrar_parametros():
    days_min = st.sidebar.slider("📉 Días mínimo", 1, 60, 35, key="days_min")
    days_max = st.sidebar.slider("📈 Días máximo", 1, 90, 35, key="days_max")
    margin   = st.sidebar.number_input("🧮 Margen extra (%)", 0, 100, 0, key="margin")
    return days_min, days_max, margin
