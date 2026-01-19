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
    c3.metric("Comercios en Riesgo", riesgo_count, delta=riesgo_count, delta_color="inverse")
    
    avg_perf = df['Variacion'].mean()
    c4.metric("Performance Promedio", f"{avg_perf:.1f}%")

    st.divider()

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Ventas por Merchant")
        fig_ventas = px.bar(df, x='Nombre', y='Ventas_Mes', color='Estado', 
                           text_auto='.2s', color_discrete_map={"🟢 Estable": "#28a745", "🔴 En Riesgo": "#dc3545", "🟡 Potencial": "#ffc107"})
        st.plotly_chart(fig_ventas, use_container_width=True)

    with col_chart2:
        st.subheader("Estado de Salud de Cartera")
        fig_pie = px.pie(df, names='Estado', hole=0.4, 
                         color='Estado', color_discrete_map={"🟢 Estable": "#28a745", "🔴 En Riesgo": "#dc3545", "🟡 Potencial": "#ffc107"})
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("📑 Vista Rápida de Cartera")
    st.dataframe(df[['Nombre', 'CUIT', 'Ventas_Mes', 'Variacion', 'Estado']], use_container_width=True, hide_index=True)

# --- 4. SECCIÓN: GESTIÓN INDIVIDUAL ---
elif seccion == "📝 Gestión Individual":
    st.title("📋 Gestión de Merchant")
    
    # Selector de Merchant
    df['Display_Name'] = df['Nombre'] + " | CUIT: " + df['CUIT'].astype(str)
    merchant_label = st.selectbox("Selecciona un Merchant:", options=df['Display_Name'].values)
    
    row = df[df['Display_Name'] == merchant_label].iloc[0]
    
    # Info técnica
    st.markdown(f"### {row['Nombre']}")
    st.caption(f"CUIT: {row['CUIT']} | Nro Comercio: {row['NroComercio']}")

    # Formulario de registro (Idéntico al anterior)
    st.divider()
    with st.form("registro_contacto", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            fecha = st.date_input("Fecha", datetime.now())
            tipo = st.selectbox("Canal", ["Llamada", "Email", "WhatsApp", "Visita"])
        with col_b:
            compromiso = st.text_input("Próximo paso")
            prioridad = st.select_slider("Urgencia", options=["Baja", "Media", "Alta"])
        
        resumen = st.text_area("Notas e Insights")
        submit = st.form_submit_button("Guardar Gestión")
        
        if submit:
            st.success(f"Gestión para {row['Nombre']} guardada por {nombre_asesor}")

    # Sugerencia IA Proactiva
    if row['Variacion'] < 0:
        st.error(f"⚠️ **Alerta:** {row['Nombre']} bajó sus ventas un {abs(row['Variacion']):.1f}%. Necesita contacto urgente.")
