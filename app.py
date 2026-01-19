import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# CONFIGURACIÓN
st.set_page_config(page_title="Merchant Advisor Hub", layout="wide")

# --- 1. DATOS ---
def load_data():
    data = {
        "CUIT": [30712345678, 20987654321, 33444555667],
        "NroComercio": [123456789, 987654321, 456123789],
        "Nombre": ["Tienda Alpha", "Bazar Beta", "Moda Gamma"],
        "Ventas_Mes": [15000, 8000, 12000],
        "Ventas_Prev": [14000, 9500, 12500],
        "Estado": ["🟢 Estable", "🔴 En Riesgo", "🟡 Potencial"]
    }
    df = pd.DataFrame(data)
    df['Variacion'] = ((df['Ventas_Mes'] - df['Ventas_Prev']) / df['Ventas_Prev']) * 100
    return df

# --- 2. SIDEBAR (LOGIN) ---
st.sidebar.header("👤 Sesión")
nombre_asesor = st.sidebar.text_input("Nombre del Asesor/a:")

if not nombre_asesor:
    st.sidebar.warning("Ingresa tu nombre para continuar.")
    st.title("🚀 Merchant Advisor Hub")
    st.info("Identifícate en el panel lateral.")
    st.stop()

menu = st.sidebar.radio("Navegación", ["🏠 Home", "📝 Gestión Individual"])
df = load_data()

# --- 3. VISTA HOME ---
if menu == "🏠 Home":
    st.title(f"📊 Dashboard de Cartera")
    st.write(f"Hola **{nombre_asesor}**, este es el estado de tus comercios.")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Merchants", len(df))
    c2.metric("Ventas Total", f"${df['Ventas_Mes'].sum():,}")
    c3.metric("Rendimiento", f"{df['Variacion'].mean():.1f}%")

    st.divider()
    
    col_a, col_b = st.columns(2)
    with col_a:
        fig1 = px.bar(df, x='Nombre', y='Ventas_Mes', color='Estado', title="Ventas por Comercio")
        st.plotly_chart(fig1, use_container_width=True)
    with col_b:
        fig2 = px.pie(df, names='Estado', hole=0.4, title="Salud de Cartera")
        st.plotly_chart(fig2, use_container_width=True)

# --- 4. VISTA GESTIÓN ---
else:
    st.title("📋 Registro de Gestión")
    df['Selector'] = df['Nombre'] + " | CUIT: " + df['CUIT'].astype(str)
    seleccion = st.selectbox("Selecciona un Merchant:", df['Selector'])
    
    row = df[df['Selector'] == seleccion].iloc[0]
    
    # Aquí es donde estaba el error de la llave (corregido)
    st.markdown(f"### Gestionando: **{row['Nombre']}**")
    st.caption(f"CUIT: {row['CUIT']} | Asesor: {nombre_asesor}")

    with st.form("form_gestion"):
        col1, col2 = st.columns(2)
        fecha = col1.date_input("Fecha", datetime.now())
        tipo = col1.selectbox("Canal", ["WhatsApp", "Llamada", "Visita"])
        compromiso = col2.text_input("Próximo paso")
        prioridad = col2.select_slider("Urgencia", options=["Baja", "Media", "Alta"])
        resumen = st.text_area("Resumen")
        
        if st.form_submit_button("Guardar"):
            st.success("✅ Registro guardado (Simulado)")
