# views/vista_historial.py

import streamlit as st
import os
from utils.exporter import cargar_historial_ordenes, exportar_usando_machote

def vista_historial(ruta_historial):
    st.header("📜 Historial de Órdenes de Compra")
    machote_path = os.path.join(os.path.dirname(__file__), "..", "Compra_OC_carga_masiva.xlsx")


    historial = cargar_historial_ordenes(ruta_historial)

    if not historial:
        st.info("No hay órdenes cerradas registradas aún.")
        return

    for orden in historial:
        with st.expander(f"📦 {orden['nombre_archivo']}"):
            st.dataframe(orden["df"], use_container_width=True)

            col1, col2 = st.columns([3, 1])

            with col1:
                if st.button(f"📥 Descargar con plantilla", key=f"desc_{orden['nombre_archivo']}"):
                    ruta_exportada = exportar_usando_machote(
                        df=orden["df"],
                        nombre_archivo=orden["nombre_archivo"],
                        ruta_salida=ruta_historial,
                        machote_path=machote_path
                    )

                    if ruta_exportada and os.path.exists(ruta_exportada):
                        with open(ruta_exportada, "rb") as f:
                            st.download_button(
                                label="⬇️ Descargar Excel final",
                                data=f,
                                file_name=orden["nombre_archivo"],
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key=f"dl_{orden['nombre_archivo']}"
                            )
                    else:
                        st.error("❌ No se pudo generar el archivo con la plantilla.")

            with col2:
                if st.button(f"🗑️ Eliminar orden", key=f"del_{orden['nombre_archivo']}"):
                    try:
                        os.remove(orden["ruta"])
                        st.success(f"Orden {orden['nombre_archivo']} eliminada.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ No se pudo eliminar: {e}")


