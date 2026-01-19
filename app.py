import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Merchant Advisor Hub", layout="wide")

# --- 1. CARGA DE DATOS SSOT (Enriquecida) ---
def load_ssot_data():
    data = {
        "CUIT": [30712345678, 20987654321, 33444555667],
        "NroComercio": [123456789, 987654321, 456123789],
        "Nombre": ["Tienda Alpha", "Bazar Beta", "Moda Gamma"],
        "Ventas_Mes": [15000, 8000, 12000],
        "Estado": ["🟢 Estable", "🔴 En Riesgo", "🟡 Potencial"]
    }
    return pd.DataFrame(data)

# --- 2. LÓGICA DE SELECCIÓN EN SIDEBAR ---
df = load_ssot_data()

st.sidebar.header("🔍 Buscador de Cartera")

# Creamos una columna auxiliar para el selector que combine los datos técnicos
df['Display_Name'] = (
    df['Nombre'] + 
    " | CUIT: " + df['CUIT'].astype(str) + 
    " | Nro: " + df['NroComercio'].astype(str)
)

# Selector en el Sidebar
seleccion = st.sidebar.selectbox(
    "Selecciona un Merchant para gestionar:",
    options=df['Display_Name'].values,
    index=0
)

# Extraer los datos del merchant seleccionado
row = df[df['Display_Name'] == seleccion].iloc[0]

# --- 3. INTERFAZ PRINCIPAL ---
st.title("🚀 Merchant Advisor Hub")

# Cabecera con Info Técnica del Merchant Seleccionado
st.markdown(f"### Gestionando: **{row['Nombre']}**")
st.caption(f"CUIT: {row['CUIT']} | Número de Comercio: {row['NroComercio']}")

# DASHBOARD DE MÉTRICAS
col1, col2, col3 = st.columns(3)
col1.metric("Ventas Actuales", f"${row['Ventas_Mes']:,}")
col2.metric("Estado de Salud", row['Estado'])
col3.metric("CUIT", row['CUIT'])

st.divider()

# --- 4. SECCIÓN DE REGISTRO ---
st.subheader(f"📝 Cuaderno de Registro: {row['Nombre']}")

with st.form("registro_contacto", clear_on_submit=True):
    c1, c2 = st.columns(2)
    with c1:
        fecha = st.date_input("Fecha del contacto", datetime.now())
        tipo = st.selectbox("Canal", ["Llamada", "Email", "WhatsApp", "Reunión Presencial"])
    with c2:
        compromiso = st.text_input("Próximo paso / Compromiso")
        prioridad = st.select_slider("Prioridad", options=["Baja", "Media", "Alta"])
    
    resumen = st.text_area("Resumen de la conversación e Insights")
    
    submit = st.form_submit_button("Guardar Gestión")
    
    if submit:
        # Aquí la lógica de guardado usaría row['CUIT'] como llave primaria
        st.success(f"Gestión vinculada al CUIT {row['CUIT']} guardada exitosamente.")

# SUGERENCIA DE AI
st.info(f"💡 **Sugerencia de AI para {row['Nombre']}:** El merchant con CUIT {row['CUIT']} tiene un perfil apto para financiamiento de capital de trabajo.")
