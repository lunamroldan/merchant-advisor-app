import streamlit as st
import pandas as pd
from datetime import datetime
import os

# CONFIGURACIÓN Y ESTILO
st.set_page_config(page_title="Merchant Management System", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS TEMPORAL (Simulando la SSOT) ---
DB_FILE = "gestion_merchants.csv"

def inicializar_db():
    if not os.path.exists(DB_FILE):
        df = pd.DataFrame(columns=["Fecha", "Merchant", "Asesora", "Tipo", "Resumen", "Compromiso", "Prioridad"])
        df.to_csv(DB_FILE, index=False)

def guardar_gestion(datos):
    df = pd.read_csv(DB_FILE)
    nuevo_registro = pd.DataFrame([datos])
    df = pd.concat([df, nuevo_registro], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

inicializar_db()

# --- DATOS DE CARTERA (SSOT) ---
merchants_data = {
    "Nombre": ["Tienda Sol", "Eco Market", "Tech Gadgets", "Boutique Luna"],
    "Segmento": ["TOP", "Medium", "TOP", "Low"],
    "Ventas_Var": ["+15%", "-10%", "Estable", "-5%"],
    "Salud": ["🟢", "🔴", "🟡", "🟡"]
}
df_merchants = pd.DataFrame(merchants_data)

# --- INTERFAZ ---
st.title("💼 Panel de Asesoras: Gestión de Cartera")

# Sidebar para selección
st.sidebar.header("Mi Cartera")
merchant_selec = st.sidebar.selectbox("Selecciona un Merchant para gestionar:", df_merchants["Nombre"])
asesora_nombre = st.sidebar.text_input("Nombre de la Asesora", "Usuario")

# Vista de métricas rápidas (Data-Driven)
m_info = df_merchants[df_merchants["Nombre"] == merchant_selec].iloc[0]
c1, c2, c3 = st.columns(3)
with c1: st.metric("Segmento", m_info["Segmento"])
with c2: st.metric("Var. Ventas (30d)", m_info["Ventas_Var"])
with c3: st.metric("Estado de Salud", m_info["Salud"])

st.divider()

# --- CUADERNO DE REGISTRO ---
col_form, col_hist = st.columns([1, 1])

with col_form:
    st.subheader("📝 Registrar Nuevo Contacto")
    with st.form("form_gestion", clear_on_submit=True):
        tipo = st.selectbox("Canal de contacto", ["Llamada", "WhatsApp", "Email", "Visita"])
        prioridad = st.select_slider("Prioridad de la acción", options=["Baja", "Media", "Alta"])
        resumen = st.text_area("¿De qué hablaron? (Insights)")
        compromiso = st.text_input("Compromiso / Siguiente paso")
        
        btn_guardar = st.form_submit_button("Guardar en Historial")
        
        if btn_guardar:
            nueva_data = {
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Merchant": merchant_selec,
                "Asesora": asesora_nombre,
                "Tipo": tipo,
                "Resumen": resumen,
                "Compromiso": compromiso,
                "Prioridad": prioridad
            }
            guardar_gestion(nueva_data)
            st.success("Registro guardado correctamente.")

with col_hist:
    st.subheader("📚 Historial de Seguimiento")
    historial = pd.read_csv(DB_FILE)
    hist_merchant = historial[historial["Merchant"] == merchant_selec].sort_values(by="Fecha", ascending=False)
    
    if not hist_merchant.empty:
        for i, row in hist_merchant.iterrows():
            with st.expander(f"{row['Fecha']} - {row['Tipo']}"):
                st.write(f"**Resumen:** {row['Resumen']}")
                st.write(f"**Próximo paso:** {row['Compromiso']}")
                st.caption(f"Registrado por: {row['Asesora']} | Prioridad: {row['Prioridad']}")
    else:
        st.info("No hay registros previos para este merchant.")

# --- ANALÍTICA AGREGADA ---
st.divider()
if st.checkbox("Ver desempeño general de la cartera"):
    st.dataframe(historial)
