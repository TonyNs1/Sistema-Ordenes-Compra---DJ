import streamlit as st
import pandas as pd
from datetime import datetime
import os

from config              import TEMP_FILE
from utils.ui            import mostrar_parametros
from utils.loader        import cargar_archivo_excel
from utils.calculations  import compute_suggestions
from utils.filters       import apply_filters
from utils.descargas     import mostrar_botones_descarga
from utils.ordenes       import init_orden, add_items, close_order
from utils.exporter      import exportar_usando_machote
from utils.grid          import mostrar_aggrid


def vista_principal(ruta_ordenes) -> None:
    st.title("📦 Sistema de órdenes de compra – Depósito Jiménez")

    # 🎨 Estilo para filas alternas en AgGrid
    st.markdown(
        """
        <style>
        .ag-theme-streamlit .fila-alterna {
            background-color: #f4f4f4 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 1️⃣ Cargar archivo
    if not cargar_archivo_excel(TEMP_FILE):
        st.stop()

    df_stock = st.session_state.df
    init_orden()

    # 2️⃣ Parámetros y filtros
    days_min, days_max, margin = mostrar_parametros()
    df_calc = compute_suggestions(df_stock, days_min, days_max, margin)
    extra = st.session_state.get("extra_cols", [])
    df_disp = apply_filters(df_calc, extra)

    # 3️⃣ Tabla principal
    grid_main = mostrar_aggrid(df_disp, editable=False, seleccionar_filas=True, key="tabla_principal")
    st.session_state["seleccionados_actuales"] = grid_main.get("selected_rows", [])

    # 4️⃣ Agregar a orden
    if st.button("📥 Agregar seleccionados a orden"):
        seleccionados = st.session_state.get("seleccionados_actuales", [])
        if seleccionados:
            df_sel = pd.DataFrame(seleccionados)

            columnas_requeridas = ["Código", "Nombre", "Cantidad a comprar", "Último costo", "Descuento"]
            for col in columnas_requeridas:
                if col not in df_sel.columns:
                    df_sel[col] = 0
            add_items(df_sel[columnas_requeridas])

            st.session_state["seleccionados_actuales"] = []
            st.success(f"🟢 Se agregaron {len(df_sel)} producto(s).")
            st.rerun()
        else:
            st.warning("⚠️ No seleccionaste productos.")

    # 5️⃣ Orden en curso
    if st.session_state.orden_en_curso:
        with st.expander("🧾 Orden en curso", True):
            df_order = pd.DataFrame(st.session_state.orden_en_curso)

            grid_order = mostrar_aggrid(
                df_order,
                editable=True,
                seleccionar_filas=True,
                columnas_bloqueadas=["Código"],
                key="order_editor_grid"
            )

            # 💾 Guardar cambios
            if st.button("💾 Guardar cambios en la orden"):
                try:
                    df_guardado = pd.DataFrame(grid_order["data"]).copy()

                    columnas_esperadas = {
                        "Código": "Código",
                        "Nombre": "Nombre",
                        "Cantidad a comprar": "Cantidad comprada",
                        "Último costo": "Costo unitario de la compra",
                        "Descuento": "Descuento"
                    }
                    df_guardado.rename(columns=columnas_esperadas, inplace=True)

                    for col in columnas_esperadas.values():
                        if col not in df_guardado.columns:
                            df_guardado[col] = 0

                    for col in ["Cantidad comprada", "Costo unitario de la compra", "Descuento"]:
                        df_guardado[col] = pd.to_numeric(df_guardado[col], errors="coerce").fillna(0).round(2)

                    columnas_finales = list(columnas_esperadas.values())
                    st.session_state.orden_en_curso = df_guardado[columnas_finales].to_dict(orient="records")

                    st.success("✅ Cambios guardados correctamente.")
                except Exception as e:
                    st.error(f"❌ Error al guardar cambios: {e}")

            nombre_usr = st.text_input("📝 Nombre para esta orden", placeholder="Ej: Ferretería Los Ángeles")

            # ✅ Cerrar orden
            if st.button("✅ Cerrar orden"):
                try:
                    nombre  = nombre_usr.strip() or datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    fecha   = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    carpeta = os.path.join(os.path.expanduser("~"), "Desktop", "Ordenes de Compra")
                    machote = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Compra_OC_carga_masiva.xlsx"))
                    os.makedirs(carpeta, exist_ok=True)

                    df_final = pd.DataFrame(st.session_state.orden_en_curso)

                    df_export = df_final[["Código", "Cantidad comprada", "Costo unitario de la compra", "Descuento"]].copy()
                    for col in df_export.columns:
                        df_export[col] = pd.to_numeric(df_export[col], errors="coerce").fillna(0).round(2)

                    ruta_final = exportar_usando_machote(
                        df_export,
                        f"Orden_{nombre}_{fecha}.xlsx",
                        carpeta,
                        machote,
                    )

                    close_order(lambda *_, proveedor=None: ruta_final, nombre_orden=nombre)

                    # Desmarcar productos
                    if isinstance(st.session_state.df, pd.DataFrame):
                        st.session_state.df["Seleccionar"] = False
                        st.session_state.df = st.session_state.df.to_dict(orient="records")
                    elif isinstance(st.session_state.df, list):
                        for row in st.session_state.df:
                            if isinstance(row, dict) and "Seleccionar" in row:
                                row["Seleccionar"] = False

                    # 📥 Botón de descarga
                    if os.path.exists(ruta_final):
                        with open(ruta_final, "rb") as f:
                            st.download_button(
                                "📥 Descargar orden final",
                                f.read(),
                                file_name=os.path.basename(ruta_final),
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            )
                        st.session_state.update(ruta_ultima_orden=ruta_final, mostrar_descarga_final=True)

                except Exception as e:
                    st.error(f"❌ Error al cerrar la orden: {e}")

    # 6️⃣ Botones adicionales
    mostrar_botones_descarga(df_disp)

    if st.session_state.get("mostrar_descarga_final", False):
        st.success("✅ Orden cerrada correctamente.")
        if st.button("🔄 Comenzar nueva orden"):
            st.session_state.update(
                orden_en_curso=[],
                selected_codigos=set(),
                mostrar_descarga_final=False,
                ruta_ultima_orden=""
            )
            st.rerun()


