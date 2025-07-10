# Inventario App 📦

Aplicación para análisis de inventario, sugerencia de compras y gestión visual de stock con Streamlit.

## Funcionalidades principales:
- Carga y análisis de archivos Excel
- Cálculo de mínimos y máximos sugeridos por días configurables
- Alertas visuales (rojo, amarillo, verde, azul, naranja)
- Eliminación de filas con persistencia por código
- Botón 🧹 para reinicio total de sesión (borra archivos y estado)
- Exportación a CSV y Excel

## Estructura
```
inventario_app/
├── app.py
├── requirements.txt
├── README.md
└── utils/
    ├── calculations.py
    ├── data_loader.py
    ├── eliminador.py
    └── filters.py
```

## Cómo correr la app
1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar:
```bash
streamlit run app.py
```

3. Subir tu archivo Excel y comenzar el análisis.

---

Desarrollado por Tony 🔧