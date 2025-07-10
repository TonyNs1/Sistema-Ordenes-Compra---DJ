import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode


def mostrar_aggrid(
    df,
    editable: bool = False,
    seleccionar_filas: bool = True,
    columnas_bloqueadas: list | None = None,
    height: int = 450,
    key: str = "aggrid",
) -> dict:
    """Renderiza un DataFrame en AgGrid.

    • Si `editable=True`, usa MODEL_CHANGED para capturar celdas editadas.
    • Las columnas numéricas se muestran con 2 decimales.
    • Incluye checkbox de encabezado para seleccionar/desmarcar todo.
    • Alterna color de filas (estilo zebra) con JS sin errores.
    """
    df = df.copy().reset_index(drop=True)

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(resizable=True, wrapText=True, autoHeight=True)

    columnas_num = {
        "Cantidad a comprar",
        "Cantidad comprada",
        "Costo unitario de la compra",
        "Descuento",
    }

    for col in df.columns:
        editable_col = editable and (columnas_bloqueadas is None or col not in columnas_bloqueadas)
        flex_val = 2 if col.lower().startswith(("nombre", "último")) else 1

        if col in columnas_num:
            gb.configure_column(
                col,
                type=["numericColumn", "customNumericFormat"],
                valueFormatter=JsCode(
                    """
                    function(params) {
                        let val = parseFloat(params.value);
                        return isNaN(val) ? '0.00' : val.toFixed(2);
                    }
                    """
                ),
                editable=editable_col,
                flex=flex_val,
                minWidth=120,
            )
        else:
            gb.configure_column(col, editable=editable_col, flex=flex_val, minWidth=100)

    if seleccionar_filas:
        gb.configure_selection(
            selection_mode="multiple",
            use_checkbox=True,
            header_checkbox=True,
            header_checkbox_filtered_only=False
        )

    # Alternar color de filas estilo zebra (sin romper JS)
    gb.configure_grid_options(
        domLayout="normal",
        suppressRowClickSelection=True,
        enableCellTextSelection=True,
        headerHeight=30,
        rowHeight=34,
        rowClassRules={
            "fila-alterna": JsCode("function(params) { return params.node.rowIndex % 2 === 0; }")
        },
        suppressKeyboardEvent=JsCode(
            """
            function(params) {
                const ENTER = 13, TAB = 9;
                if (params.event.keyCode === ENTER || params.event.keyCode === TAB) {
                    params.api.stopEditing();
                }
                return false;
            }
            """
        ),
    )

    update_mode = (
        GridUpdateMode.MODEL_CHANGED if editable else GridUpdateMode.SELECTION_CHANGED
    )

    grid_response = AgGrid(
        df,
        gridOptions=gb.build(),
        update_mode=update_mode,
        data_return_mode="AS_INPUT",
        allow_unsafe_jscode=True,
        use_container_width=True,
        height=height,
        theme="streamlit",
        key=key,
    )

    return grid_response


