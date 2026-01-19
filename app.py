import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Merchant Advisor Hub", layout="wide")

# --- 1. CARGA DE DATOS (SSOT) ---
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

# --- 2. LOGIN Y NAVEGACIÓN ---
st.sidebar.header("👤 Sesión de Asesor")
nombre_asesor = st.sidebar.text_input("Nombre y Apellido:", placeholder="Ej: Ana García")

if not nombre_asesor:
    st.sidebar.warning("⚠️ Ingresa tu nombre para acceder.")
    st.title("🚀 Bienvenido al Merchant Advisor Hub")
    st.info("Por favor, identifícate en el panel lateral para visualizar tu cartera.")
    st.stop()

st.sidebar.divider()
seccion = st.sidebar.radio("Ir a:", ["🏠 Home", "📝 Gestión Individual"])

# Cargar datos globales
df = load_ssot_data()

# --- 3. SECCIÓN: HOME (DASHBOARD) ---
if seccion == "🏠 Home":
    st.title(f"📊 Dashboard de Cartera")
    st.markdown(f"Bienvenido/a, **{nombre_asesor}**. Aquí tienes el resumen de tu cartera asignada.")
    
    # KPIs Rápidos
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Merchants", len(df))
    c2.metric("Ventas Totales", f"${df['Ventas_Mes'].sum():,}")
    
    riesgo_count = len(df[df['Estado'] == "🔴 En Riesgo"])
    c3.metric("En Riesgo", riesgo_count, delta=riesgo_count, delta_color="inverse")
    
    avg_perf = df['Variacion'].mean()
    c4.metric("Perf. Promedio", f"{avg_perf:.1f}%")

    st.divider()

    # Gráficos Interactivos
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Distribución de Ventas")
        fig_ventas = px.bar(df, x='Nombre', y='Ventas_Mes', color='Estado', 
                           color_discrete_map={"🟢 Estable": "#28a745", "🔴 En Riesgo": "#dc3545", "🟡 Potencial": "#ffc107"})
        st.plotly_chart(fig_ventas, use_container_width=True)

    with col_chart2:
        st.subheader("Salud de la Cartera")
        fig_pie = px.pie(df, names='Estado', hole=0.4, 
                         color='Estado', color_discrete_map={"🟢 Estable": "#28a745", "🔴 En Riesgo": "#dc3545", "🟡 Potencial": "#ffc107"})
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("📑 Tabla General de Merchants")
    st.dataframe(df[['Nombre', 'CUIT', 'Ventas_Mes', 'Estado']], use_container_width=True, hide_index=True)

# --- 4. SECCIÓN: GESTIÓN INDIVIDUAL ---
elif seccion == "📝 Gestión Individual":
    st.title("📋 Gestión Detallada")
    
    # Buscador de Merchant
    df['Display_Name'] = df['Nombre'] + " | CUIT: " + df['CUIT'].astype(str)
    merchant_label = st.selectbox("Selecciona para gestionar:", options=df['Display_Name'].values)
    
    row = df[df['Display_Name'] == merchant_label].iloc[0]
    
    # Cabecera Merchant
    st.subheader(f"Merchant: {row['Nombre']}")
    st.info(f"Asesor a cargo: {nombre_asesor} | CUIT: {row['CUIT']} | Nro: {row['NroComercio']}")

    # Formulario
    with st.form("registro_contacto", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            fecha = st.date_input("Fecha", datetime.now())
            tipo = st.selectbox("Canal", ["Llamada", "Email", "WhatsApp", "Visita"])
        with col_b:
            compromiso = st.text_input("Compromiso / Next Step")
            prioridad = st.select_slider("Urgencia", options=["Baja", "Media", "Alta"])
        
        resumen = st.text_area("Notas e Insights de la conversación")
        submit = st.form_submit_button("Guardar Gestión")
        
        if submit:
            st.success(f"✅ Gestión para {row['Nombre']} registrada exitosamente.")

    # Alerta de IA
    if row['Variacion'] < 0:
        st.warning(f"⚠️ Alerta: El comercio {row['Nombre']} bajó sus ventas. Se recomienda contacto inmediato.")
