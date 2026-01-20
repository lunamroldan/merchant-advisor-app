import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="GESTION ESTRATEGICA DE CARTERA", layout="wide")

# --- 1. PERSISTENCIA DE DATOS (ARCHIVO LOCAL CSV) ---
DB_FILE = "database_gestiones.csv"

def cargar_historial():
    """Carga el historial desde el CSV o crea uno vacío si no existe."""
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    else:
        return pd.DataFrame(
            columns=["Fecha", "Asesor", "Merchant", "CUIT", "Canal", "Resumen", "Compromiso", "Prioridad"]
        )

def guardar_registro(nuevo_log):
    """Añade un nuevo registro al archivo CSV."""
    df_actual = cargar_historial()
    df_actual = pd.concat([df_actual, nuevo_log], ignore_index=True)
    df_actual.to_csv(DB_FILE, index=False)
    return df_actual

# Cargamos los datos persistentes al iniciar la app
historial_db = cargar_historial()

# --- 2. CARGA DE DATOS MAESTROS (SSOT) ---
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
st.sidebar.header("👤 KAM")
nombre_asesor = st.sidebar.text_input("Nombre del Asesor/a:", placeholder="Ej: Ana García")

if not nombre_asesor:
    st.sidebar.warning("⚠️ Ingresa tu nombre para continuar.")
    st.title("🚀 GESTION ESTRATEGICA DE CARTERA")
    st.info("Por favor, identifícate en el panel lateral para acceder.")
    st.stop()

st.sidebar.divider()
menu = st.sidebar.radio("Navegación", ["🏠 Home / Dashboard", "📝 Gestión Individual"])
df_maestro = load_data()

# --- 4. VISTA: HOME / DASHBOARD ---
if menu == "🏠 Home / Dashboard":
    st.title(f"📊 Dashboard de Cartera")
    st.markdown(f"Bienvenido/a **{nombre_asesor}**. Resumen de performance y gestiones históricas.")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Merchants a cargo", len(df_maestro))
    c2.metric("TPV Total", f"${df_maestro['Ventas_Mes'].sum():,}")
    c3.metric("Total Gestiones Históricas", len(historial_db))

    st.divider()
    
    col_a, col_b = st.columns(2)
    with col_a:
        fig1 = px.bar(df_maestro, x='Nombre', y='Ventas_Mes', color='Estado', title="Ventas por Comercio")
        st.plotly_chart(fig1, use_container_width=True)
    with col_b:
        fig2 = px.pie(df_maestro, names='Estado', hole=0.4, title="Salud de Cartera")
        st.plotly_chart(fig2, use_container_width=True)

# --- 5. VISTA: GESTIÓN INDIVIDUAL + HISTORIAL ---
else:
    st.title("📋 Gestión y Trazabilidad")
    
    df_maestro['Selector'] = df_maestro['Nombre'] + " | CUIT: " + df_maestro['CUIT'].astype(str)
    seleccion = st.selectbox("Selecciona un Merchant:", df_maestro['Selector'])
    row = df_maestro[df_maestro['Selector'] == seleccion].iloc[0]
    
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
                # GUARDADO FÍSICO
                historial_db = guardar_registro(nuevo_log)
                st.success("✅ Gestión guardada permanentemente en la base de datos.")
                st.rerun()

    with col_hist:
        st.subheader("📚 Historial Reciente")
        # Filtramos del historial cargado del archivo
        hist_f = historial_db[historial_db['Merchant'] == row['Nombre']].sort_index(ascending=False)
        
        if not hist_f.empty:
            for _, h in hist_f.head(5).iterrows():
                with st.expander(f"{h['Fecha']} - {h['Canal']}"):
                    st.write(f"**Notas:** {h['Resumen']}")
                    st.caption(f"Compromiso: {h['Compromiso']} | KAM: {h['Asesor']}")
        else:
            st.info("Sin registros previos en la base de datos.")

    # --- SECCIÓN DE TABLA RESUMEN Y DESCARGA ---
    st.divider()
    st.subheader("📊 Tabla de Seguimiento Histórico")
    
    if not historial
