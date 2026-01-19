import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Merchant Advisor Hub", layout="wide")

# --- 1. DATOS DE CARTERA (Simulando la base asignada al asesor) ---
def load_ssot_data():
    data = {
        "CUIT": [30712345678, 20987654321, 33444555667, 30555666778],
        "NroComercio": [123456789, 987654321, 456123789, 789456123],
        "Nombre": ["Tienda Alpha", "Bazar Beta", "Moda Gamma", "Tech Solutions"],
        "Ventas_Mes": [15000, 8000, 12000, 45000],
        "Ventas_Prev": [14000, 9500, 12500, 40000],
        "Estado": ["🟢 Estable", "🔴 En Riesgo", "🟡 Potencial", "🟢 Estable"]
    }
    df = pd.DataFrame(data)
    # Cálculo de performance
    df['Variacion'] = ((df['Ventas_Mes'] - df['Ventas_Prev']) / df['Ventas_Prev']) * 100
    return df

# --- 2. PANEL LATERAL (LOGIN Y NAVEGACIÓN) ---
st.sidebar.header("👤 Sesión de Asesor")
nombre_asesor = st.sidebar.text_input("Nombre y Apellido:", placeholder="Ej: Ana García")

if not nombre_asesor:
    st.sidebar.warning("⚠️ Ingresa tu nombre para acceder.")
    st.title("🚀 Bienvenido al Merchant Advisor Hub")
    st.info("Por favor, identifícate en el panel lateral para visualizar tu cartera.")
    st.stop()

st.sidebar.divider()
# Navegación
seccion = st.sidebar.radio("Ir a:", ["🏠 Home / Dashboard", "📝 Gestión Individual"])

# Carga de datos
df = load_ssot_data()

# --- 3. SECCIÓN: HOME / DASHBOARD ---
if seccion == "🏠 Home / Dashboard":
    st.title(f"📊 Dashboard de Cartera: {nombre_asesor}")
    
    # KPIs Globales de la cartera
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Merchants a cargo", len(df))
    c2.metric("Ventas Totales", f"${df['Ventas_Mes'].sum():,}")
    
    # Salud promedio
    riesgo_count = len(df[df['Estado'] == "🔴 En Riesgo"])
    c3.metric("Comercios en Riesgo",
