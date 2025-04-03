import streamlit as st
import pandas as pd
import plotly.express as px
from funciones_ganamos import carga_ganamos  # Importa la función desde el archivo local

# Configuración de la página
st.set_page_config(page_title="Análisis de Datos - Ganamos", layout="wide")

# Título de la aplicación
st.title("📊 Análisis de Datos - Ganamos")

# Carga de datos
@st.cache_data
def cargar_datos():
    df = carga_ganamos()
    return df

df = cargar_datos()

# Verificación de carga de datos
if df is None or df.empty:
    st.error("No se pudieron cargar los datos. Verifica la fuente de datos.")
    st.stop()

# Sidebar para filtros
st.sidebar.header("Filtros")

# Selección de columna para análisis
columnas_numericas = df.select_dtypes(include=['number']).columns.tolist()
columna_seleccionada = st.sidebar.selectbox("Selecciona una métrica:", columnas_numericas)

# Filtro por fecha si hay una columna de fecha en el dataset
if 'fecha' in df.columns:
    df['fecha'] = pd.to_datetime(df['fecha'])
    fecha_min = df['fecha'].min()
    fecha_max = df['fecha'].max()
    rango_fechas = st.sidebar.date_input("Rango de Fechas", [fecha_min, fecha_max], fecha_min, fecha_max)
    df = df[(df['fecha'] >= pd.Timestamp(rango_fechas[0])) & (df['fecha'] <= pd.Timestamp(rango_fechas[1]))]

# Visualización de datos
st.subheader("📈 Visualización de Datos")

# Gráfico de dispersión
fig_scatter = px.scatter(df, x=df.index, y=columna_seleccionada, title=f"Dispersión de {columna_seleccionada}")
st.plotly_chart(fig_scatter, use_container_width=True)

# Histograma
fig_hist = px.histogram(df, x=columna_seleccionada, title=f"Distribución de {columna_seleccionada}", nbins=30)
st.plotly_chart(fig_hist, use_container_width=True)

# Tabla de datos
st.subheader("📋 Vista de Datos")
st.dataframe(df)

# Exportar datos
st.download_button(
    label="📥 Descargar CSV",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="datos_ganamos.csv",
    mime="text/csv"
)
