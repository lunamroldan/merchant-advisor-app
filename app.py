import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Merchant Advisor Hub", layout="wide")

# SIMULACIÓN DE SSOT (Aquí conectarías tu base de datos real)
def load_ssot_data():
    data = {
        "MerchantID": [101, 102, 103],
        "Nombre": ["Tienda Alpha", "Bazar Beta", "Moda Gamma"],
        "Ventas_Mes": [15000, 8000, 12000],
        "Estado": ["🟢 Estable", "🔴 En Riesgo", "🟡 Potencial"]
    }
    return pd.DataFrame(data)

# INTERFAZ
st.title("🚀 Merchant Advisor Hub")
st.sidebar.header("Filtros de Cartera")

df = load_ssot_data()
merchant_selec = st.sidebar.selectbox("Seleccionar Merchant", df["Nombre"])

# DASHBOARD DEL MERCHANT SELECCIONADO
row = df[df["Nombre"] == merchant_selec].iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("Ventas Actuales", f"${row['Ventas_Mes']}")
col2.metric("Salud del Cliente", row['Estado'])
col3.button("Ver Historial Completo")

st.divider()

# SECCIÓN DE REGISTRO (EL CUADERNO)
st.subheader(f"📝 Cuaderno de Registro: {merchant_selec}")

with st.form("registro_contacto"):
    fecha = st.date_input("Fecha del contacto", datetime.now())
    tipo = st.selectbox("Canal", ["Llamada", "Email", "WhatsApp", "Reunión Presencial"])
    resumen = st.text_area("Resumen de la conversación e Insights")
    compromiso = st.text_input("Próximo paso / Compromiso")
    
    submit = st.form_submit_button("Guardar Gestión")
    
    if submit:
        # AQUÍ SE ENVIARÍA EL DATO A TU BASE DE DATOS SEGURA
        st.success(f"Gestión guardada exitosamente para {merchant_selec}")

# SUGERENCIA DE AI (SIMULADA)
st.info(f"💡 **Sugerencia de AI para {merchant_selec}:** Basado en la caída de ventas del 5%, se recomienda ofrecer la nueva funcionalidad de cuotas sin interés.")
