import streamlit as st

def guardar_estado_df():
    """
    Guarda una copia del dataframe actual en session_state para mantener filtros,
    columnas visuales como 'Seleccionar' y '🛒 Orden', y vista actual tras recarga.
    """
    if "df" in st.session_state and isinstance(st.session_state.df, object):
        df_copy = st.session_state.df.copy(deep=True)
        st.session_state.df_guardado = df_copy


def restaurar_estado_df():
    """
    Restaura el dataframe si hay una copia guardada y no se ha cargado aún en esta sesión.
    Evita sobreescribir si ya hay 'df' activo.
    """
    if "df_guardado" in st.session_state and "df" not in st.session_state:
        st.session_state.df = st.session_state.df_guardado.copy(deep=True)

def injerta_columna_orden(df_calc):
    """
    Copia la columna '🛒 Orden' que ya existe en st.session_state.df
    hacia el dataframe recién calculado (df_calc). 
    Si no existía, la crea a partir de selected_codigos.
    """
    import streamlit as st
    if "df" in st.session_state and "🛒 Orden" in st.session_state.df.columns:
        # Mapeo Código → símbolo ✅
        mapa = dict(
            zip(
                st.session_state.df["Código"].astype(str),
                st.session_state.df["🛒 Orden"]
            )
        )
        df_calc["🛒 Orden"] = df_calc["Código"].astype(str).map(mapa).fillna("")
    else:
        sel = st.session_state.get("selected_codigos", set())
        df_calc["🛒 Orden"] = df_calc["Código"].astype(str).apply(
            lambda c: "✅" if c in sel else ""
        )
    return df_calc
