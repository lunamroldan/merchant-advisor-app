import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# CONFIGURACIÓN
st.set_page_config(page_title="Merchant Advisor Hub", layout="wide")

# --- 1. PERSISTENCIA (Para Trazabilidad) ---
# Inicializamos el historial en la sesión para que no se borre al navegar entre pestañas
if 'historial_db' not in st.session_state:
    st.session_state.historial_db = pd.DataFrame(
        columns=["Fecha", "Asesor", "Merchant", "Canal", "Resumen", "Compromiso", "Prioridad"]
    )

# --- 2. CARGA DE DATOS MAESTROS ---
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

# --- 3. SIDEBAR (LOGIN Y NAVEGACIÓN) ---
st.sidebar.header("👤 Sesión de Asesor")
nombre_asesor = st.sidebar.text_input("Nombre del Asesor/a:", placeholder="Ej: Ana García")

if not nombre_asesor:
    st.sidebar.warning("⚠️ Ingresa tu nombre para continuar.")
    st.title("🚀 Merchant Advisor Hub")
    st.info("Por favor, identifícate en el panel lateral para acceder a tu cartera.")
    st.stop()

st.sidebar.divider()
menu = st.sidebar.radio("Navegación", ["🏠 Home / Dashboard", "📝 Gestión Individual"])
df_maestro = load_data()

# --- 4. VISTA: HOME / DASHBOARD ---
if menu == "🏠 Home / Dashboard":
    st.title(f"📊 Panel General: {nombre_asesor}")
    
    # KPIs Rápidos
    c1, c2, c3 = st.columns(3)
    c1.metric("Merchants a cargo", len(df_maestro))
    c2.metric("Ventas Totales", f"${df_maestro['Ventas_Mes'].sum():,}")
    c3.metric("Gestiones Realizadas", len(st.session_state.historial_db))

    st.divider()
    
    col_a, col_b = st.columns(2)
    with col_a:
        fig1 = px.bar(df_maestro, x='Nombre', y='Ventas_Mes', color='Estado', title="Ventas por Comercio")
        st.plotly_chart(fig1, use_container_width=True)
    with col_b:
        fig2 = px.pie(df_maestro, names='Estado', hole=0.4, title="Salud de mi Cartera")
        st.plotly_chart(fig2, use_container_width=True)

# --- 5. VISTA: GESTIÓN INDIVIDUAL + HISTORIAL ---
else:
    st.title("📋 Gestión y Trazabilidad")
    
    # Selector de Merchant
    df_maestro['Selector'] = df_maestro['Nombre'] + " | CUIT: " + df_maestro['CUIT'].astype(str)
    seleccion = st.selectbox("Selecciona un Merchant para gestionar:", df_maestro['Selector'])
    
    row = df_maestro[df_maestro['Selector'] == seleccion].iloc[0]
    
    st.markdown(f"### Merchant: **{row['Nombre']}**")
    st.caption(f"CUIT: {row['CUIT']} | Nro Comercio: {row['NroComercio']} | Asesor: {nombre_asesor}")

    # Layout de dos columnas para Registro e Historial
    col_registro, col_historial = st.columns([1, 1])

    with col_registro:
        st.subheader("📝 Registrar Contacto")
        with st.form("form_gestion", clear_on_submit=True):
            f_col, c_col = st.columns(2)
            fecha_g = f_col.date_input("Fecha", datetime.now())
            canal_g = f_col.selectbox("Canal", ["WhatsApp", "Llamada", "Email", "Visita"])
            compromiso_g = c_col.text_input("Próximo paso")
            prioridad_g = c_col.select_slider("Urgencia", options=["Baja", "Media", "Alta"])
            
            resumen_g = st.text_area("Resumen de la conversación")
            
            if st.form_submit_button("Guardar Gestión"):
                # Crear nuevo registro
                nuevo_log = pd.DataFrame([{
                    "Fecha": fecha_g.strftime("%Y-%m-%d"),
                    "Asesor": nombre_asesor,
                    "Merchant": row['Nombre'],
                    "Canal": canal_g,
                    "Resumen": resumen_g,
                    "Compromiso": compromiso_g,
                    "Prioridad": prioridad_g
                }])
                
                # Actualizar el historial en la sesión
                st.session_state.historial_db = pd.concat([st.session_state.historial_db, nuevo_log], ignore_index=True)
                st.success("✅ Registro guardado en el historial.")
                st.rerun()

    with col_historial:
        st.subheader("📚 Historial de Seguimiento")
        
        # Filtrar historial para el merchant seleccionado
        hist_filtrado = st.session_state.historial_db[
            st.session_state.historial_db['Merchant'] == row['Nombre']
        ].sort_index(ascending=False) # Ver el más reciente primero

        if not hist_filtrado.empty:
            for _, h_row in hist_filtrado.iterrows():
                with st.expander(f"{h_row['Fecha']} - {h_row['Canal']} ({h_row['Prioridad']})"):
                    st.write(f"**Resumen:** {h_row['Resumen']}")
                    st.info(f"**Siguiente paso:** {h_row['Compromiso']}")
                    st.caption(f"Registrado por: {h_row['Asesor']}")
        else:
            st.info("No hay registros previos para este CUIT.")
