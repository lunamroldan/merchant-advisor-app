import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Merchant Advisor Hub", layout="wide")

# --- 1. CARGA DE DATOS SSOT ---
def load_ssot_data():
    # Datos con tipos específicos: CUIT y NroComercio como INT
    data = {
        "CUIT": [30712345678, 20987654321, 33444555667],
        "NroComercio": [123456789, 987654321, 456123789],
        "Nombre": ["Tienda Alpha", "Bazar Beta", "Moda Gamma"],
        "Ventas_Mes": [15000, 8000, 12000],
        "Estado": ["🟢 Estable", "🔴 En Riesgo", "🟡 Potencial"]
    }
    return pd.DataFrame(data)

# --- 2. PANEL LATERAL (SIDEBAR) ---
st.sidebar.header("👤 Identificación")
nombre_asesor = st.sidebar.text_input("Nombre del Asesor/a:", placeholder="Ej: Juan Pérez")

st.sidebar.divider()

st.sidebar.header("🔍 Selección de Merchant")
df = load_ssot_data()

# Creamos la etiqueta de visualización combinando los datos
df['Display_Name'] = (
    df['Nombre'] + 
    " | CUIT: " + df['CUIT'].astype(str) + 
    " | Nro: " + df['NroComercio'].astype(str)
)

merchant_selec_label = st.sidebar.selectbox(
    "Selecciona un Merchant para gestionar:",
    options=df['Display_Name'].values
)

# Extraer la fila de datos correspondiente a la selección
row = df[df['Display_Name'] == merchant_selec_label].iloc[0]

# --- 3. INTERFAZ PRINCIPAL ---
st.title("🚀 Merchant Advisor Hub")

# Validación de nombre de asesor
if not nombre_asesor:
    st.warning("👈 Por favor, ingresa tu nombre en el panel lateral para habilitar la gestión.")
    st.stop()

# CABECERA (Aquí estaba el error de la llave)
st.markdown(f"### Gestionando: **{row['Nombre']}**")
st.caption(f"CUIT: {row['CUIT']} | Nro Comercio: {row['NroComercio']} | **Asesor/a a cargo: {nombre_asesor}**")

# MÉTRICAS
c1, c2, c3 = st.columns(3)
c1.metric("Ventas Actuales", f"${row['Ventas_Mes']:,}")
c2.metric("Estado de Salud", row['Estado'])
c3.metric("CUIT ID", row['CUIT'])

st.divider()

# --- 4. FORMULARIO DE REGISTRO ---
st.subheader("📝 Cuaderno de Registro")

with st.form("registro_contacto", clear_on_submit=True):
    col_a, col_b = st.columns(2)
    
    with col_a:
        fecha = st.date_input("Fecha de contacto", datetime.now())
        tipo = st.selectbox("Canal", ["Llamada", "Email", "WhatsApp", "Visita"])
    
    with col_b:
        compromiso = st.text_input("Compromiso / Próximo paso")
        prioridad = st.select_slider("Prioridad de la acción", options=["Baja", "Media", "Alta"])
    
    resumen = st.text_area("Insights y Resumen de la conversación")
    
    submit = st.form_submit_button("Guardar Gestión")
    
    if submit:
        # Estructura de datos lista para escalar a base de datos
        nueva_gestion = {
            "Fecha": fecha.strftime("%Y-%m-%d"),
            "Asesor": nombre_asesor,
            "Merchant": row['Nombre'],
            "CUIT": int(row['CUIT']),
            "NroComercio": int(row['NroComercio']),
            "Canal": tipo,
            "Resumen": resumen,
            "Compromiso": compromiso,
            "Prioridad": prioridad
        }
        
        st.success(f"✅ Gestión guardada exitosamente por {nombre_asesor}")
        # Muestra lo que se guardaría (útil para debug)
        with st.expander("Ver datos registrados"):
            st.write(nueva_gestion)

# --- 5. SUGERENCIA DE AI ---
st.info(f"💡 **Tip para {nombre_asesor}:** El merchant {row['Nombre']} prefiere contacto vía {tipo} según tendencias históricas.")
