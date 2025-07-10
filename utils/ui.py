# utils/ui.py

import streamlit as st

def mostrar_parametros():
    """
    Muestra y devuelve los parámetros configurables del cálculo de sugerencias:
    - Días mínimo
    - Días máximo
    - Margen adicional

    Los guarda en session_state para evitar recálculos innecesarios.
    """
    if "parametros" not in st.session_state:
        st.session_state.parametros = {
            "days_min": 35,
            "days_max": 35,
            "margin": 0
        }

    with st.sidebar:
        st.markdown("## ⚙️ Parámetros de cálculo")

        days_min = st.slider(
            "📉 Días mínimo",
            1, 60, st.session_state.parametros["days_min"],
            key="days_min"
        )
        days_max = st.slider(
            "📈 Días máximo",
            1, 90, st.session_state.parametros["days_max"],
            key="days_max"
        )
        margin = st.number_input(
            "🧮 Margen extra (%)",
            0, 100, st.session_state.parametros["margin"],
            key="margin"
        )

    st.session_state.parametros.update({
        "days_min": days_min,
        "days_max": days_max,
        "margin": margin
    })

    return days_min, days_max, margin
