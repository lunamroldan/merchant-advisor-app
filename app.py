import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Merchant Advisor Hub", layout="wide")

# --- 1. CARGA DE DATOS SSOT ---
def load_ssot_data():
    # Datos técnicos: CUIT (int), NroComercio (int), Nombre (str)
    data = {
        "CUIT": [30712345678, 20987654321, 33444555667],
        "NroComercio": [123456789, 987654321, 456123789],
        "Nombre": ["Tienda Alpha", "Bazar Beta", "Moda Gamma"],
        "Ventas_Mes": [15000, 8000, 12000],
        "Estado": ["🟢 Estable", "🔴 En Riesgo", "🟡 Potencial"]
    }
    return pd.DataFrame(data)

# --- 2. PANEL LATERAL (SIDEBAR) ---
st.sidebar.header("👤 Identificación del Asesor")
nombre_asesor = st.sidebar.text_input("Tu Nombre y Apellido:", placeholder="Ej: María Pérez")

st.sidebar.divider()

st.sidebar.header("🔍 Buscador de Cartera")
df = load_ssot_data()

# Formateo del nombre para el selector: Nombre | CUIT | Nro Comercio
df['Display_Name'] = (
    df['Nombre'] + 
    " | CUIT: " + df['CUIT'].astype(str) + 
    " | Nro: " + df['NroComercio'].astype(str)
)

merchant_selec_label = st.sidebar.selectbox(
    "Selecciona un Merchant para gestionar:",
    options=df['Display_Name'].values
)

# Extraer datos del merchant seleccionado
row = df[df['Display_Name'] == merchant_selec_label].iloc[0]

# --- 3. INTERFAZ PRINCIPAL ---
st.title("🚀 Merchant Advisor Hub")

# Validar si el asesor puso su nombre antes de permitir la gestión
if not nombre_asesor:
    st.warning("⚠️ Por favor, ingresa tu nombre en el panel lateral para comenzar a registrar.")
    st.stop()

# Info de cabecera
st.markdown(f"### Gestionando: **{
