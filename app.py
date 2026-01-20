import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="GESTION ESTRATEGICA DE CARTERA", layout="wide")

# --- 1. PERSISTENCIA DE DATOS (Trazabilidad) ---
if 'historial_db' not in st.session_state:
    st.session_state.historial_db = pd.DataFrame(
        columns=["Fecha", "Asesor", "Merchant", "CUIT", "Canal", "Resumen", "Compromiso", "Prioridad"]
    )

# --- 2. CARGA DE DATOS MAESTROS ---
def load_data():
    data = {
        "CUIT": [30712345678, 20987654321, 33444555667],
        "NroComercio": [123456789, 987654321, 456123789],
        "Nombre": ["Tienda Alpha", "Bazar Beta", "Moda Gamma"],
        "Ventas_Mes": [15000, 8000, 12000],
        "Ventas_Prev": [14000, 9500, 12500],
        "Estado": ["🟢 MAM ", "🔴 INACTIVO ", "🟡 CHURN "]
    }
    df = pd.DataFrame(data)
    df['Variacion'] = ((df['Ventas_Mes'] - df['Ventas_Prev']) / df['Ventas_Prev']) * 100
    return df

# --- 3. SIDEBAR (SESIÓN Y NAVEGACIÓN) ---
st.sidebar.header("👤 KAM ")
nombre_asesor = st.sidebar.text_input("Nombre del Asesor/a:", placeholder="Ej: Ana García")

if not nombre_asesor:
    st.sidebar.warning("⚠️ Ingresa tu nombre para continuar.")
    st.title("🚀GESTION ESTRATEGICA DE CARTERA ")
    st.info("Por favor, identifícate en el panel lateral para acceder.")
    st.stop()

st.sidebar.divider()
menu = st.sidebar.radio("Navegación", ["🏠 Home / Dashboard", "📝 Gestión Individual"])
df_maestro = load_data()

# --- 4. VISTA: HOME / DASHBOARD ---
if menu == "🏠 Home / Dashboard":
    st.title(f"📊 Dashboard de Cartera")
    st.markdown(f"Bienvenido/a **{nombre_asesor}**. Resumen de performance y gestiones.")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Merchants a cargo", len(df_maestro))
    c2.metric("TPV", f"${df_maestro['Ventas_Mes'].sum():,}")
    c3.metric("Total Gestiones", len(st.session_state.historial_db))

    st.divider()
    
    col_a, col_b = st.columns(2)
    with col_a:
        fig1 = px.bar(df_maestro, x='Nombre', y='Ventas_Mes', color='Estado', title="Ventas por Comercio")
        st.plotly_chart(fig1, use_container_width=True)
    with col_b:
        fig2 = px.pie(df_maestro, names='Estado', hole=0.4, title="Salud de Cartera")
        st.plotly_chart(fig2, use_container_width=True)

# --- 5. VISTA: GESTIÓN INDIVIDUAL + HISTORIAL + DESCARGA ---
else:
    st.title("📋 Gestión y Trazabilidad")
    
    # Selector de Merchant
    df_maestro['Selector'] = df_maestro['Nombre'] + " | CUIT: " + df_maestro['CUIT'].astype(str)
    seleccion = st.selectbox("Selecciona un Merchant:", df_maestro['Selector'])
    
    row = df_maestro[df_maestro['Selector'] == seleccion].iloc[0]
    
    # Registro de Contacto
    col_reg, col_hist = st.columns([1, 1])

    with col_reg:
        st.subheader("📝 Registrar Gestión")
        with st.form("form_gestion", clear_on_submit=True):
            f_col, c_col = st.columns(2)
            fecha_g = f_col.date_input("Fecha", datetime.now())
            canal_g = f_col.selectbox("Canal", ["WhatsApp", "Llamada", "Visita", "Email"])
            compromiso_g = c_col.text_input("Próximo paso")
            prioridad_g = c_col.select_slider("Urgencia", options=["Baja", "Media", "Alta"])
            resumen_g = st.text_area("Resumen de la conversación")
            
            if st.form_submit_button("Guardar Registro"):
                nuevo_log = pd.DataFrame([{
                    "Fecha": fecha_g.strftime("%Y-%m-%d"),
                    "Asesor": nombre_asesor,
                    "Merchant": row['Nombre'],
                    "CUIT": row['CUIT'],
                    "Canal": canal_g,
                    "Resumen": resumen_g,
                    "Compromiso": compromiso_g,
                    "Prioridad": prioridad_g
                }])
                st.session_state.historial_db = pd.concat([st.session_state.historial_db, nuevo_log], ignore_index=True)
                st.success("✅ Gestión guardada.")
                st.rerun()

    with col_hist:
        st.subheader("📚 Historial Reciente")
        hist_f = st.session_state.historial_db[st.session_state.historial_db['Merchant'] == row['Nombre']].sort_index(ascending=False)
        
        if not hist_f.empty:
            for _, h in hist_f.head(3).iterrows():
                with st.expander(f"{h['Fecha']} - {h['Canal']}"):
                    st.write(f"**Notas:** {h['Resumen']}")
                    st.caption(f"Compromiso: {h['Compromiso']}")
        else:
            st.info("Sin registros previos.")

    # --- SECCIÓN DE TABLA RESUMEN Y DESCARGA (NUEVA) ---
    st.divider()
    st.subheader("📊 Tabla de Seguimiento General")
    
    if not st.session_state.historial_db.empty:
        # Mostramos la tabla completa de la sesión
        st.dataframe(st.session_state.historial_db, use_container_width=True, hide_index=True)
        
        # Lógica de descarga
        csv = st.session_state.historial_db.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📥 Descargar Reporte de Gestiones (CSV)",
            data=csv,
            file_name=f"gestiones_{nombre_asesor}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )
    else:
        st.warning("Aún no hay datos en la tabla resumen para descargar.")
