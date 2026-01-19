import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# CONFIGURACIÓN DE ESTILO
st.set_page_config(page_title="GEC - Gestión Estratégica de Cartera", layout="wide")
st.markdown("<style>.stMetric { background-color: #ffffff; border-radius: 10px; border: 1px solid #e0e0e0; padding: 10px; }</style>", unsafe_allow_html=True)

# --- BASE DE DATOS (Mantenemos CSV para esta etapa) ---
DB_FILE = "gec_gestion.csv"
if not os.path.exists(DB_FILE):
    df = pd.DataFrame(columns=["Fecha_Gestion", "Merchant", "Tipo_Accion", "Resumen", "Proximo_Contacto", "Estado_GEC", "Prioridad", "TPV_Potencial"])
    df.to_csv(DB_FILE, index=False)

# --- LÓGICA DE DATOS (Simulando TPV y Cupones) ---
merchants_master = pd.DataFrame({
    "Nombre": ["Tienda Sol", "Eco Market", "Tech Gadgets", "Boutique Luna"],
    "TPV_Mensual": [500000, 120000, 800000, 45000],
    "Ticket_Promedio": [15000, 5000, 25000, 3200],
    "Zeta": ["Construcción", "Maduro", "Construcción", "En Riesgo"]
})

# --- FUNCIONES DE APOYO ---
def calcular_etiqueta(tpv, ticket):
    if tpv > 500000: return "💎 Alto Valor"
    if ticket < 5000: return "📈 Potencial Upselling"
    return "⚖️ Estándar"

# --- INTERFAZ: DASHBOARD DE TAREAS (FUTURO) ---
st.title("🚀 GEC: Gestión Estratégica de Cartera")

# Cargar historial
historial = pd.read_csv(DB_FILE)
historial['Proximo_Contacto'] = pd.to_datetime(historial['Proximo_Contacto'])

# CAJA DE TAREAS (Dashboard)
hoy = datetime.now().date()
tareas_hoy = historial[historial['Proximo_Contacto'].dt.date <= hoy]

st.subheader("📌 Caja de Tareas (Para hoy)")
if not tareas_hoy.empty:
    cols = st.columns(len(tareas_hoy.head(4)))
    for i, (_, tarea) in enumerate(tareas_hoy.head(4).iterrows()):
        cols[i].warning(f"**{tarea['Merchant']}**\n\n{tarea['Tipo_Accion']}")
else:
    st.success("✅ ¡No tienes tareas pendientes para hoy!")

st.divider()

# --- GESTIÓN INDIVIDUAL ---
col_izq, col_der = st.columns([1, 2])

with col_izq:
    st.subheader("🎯 Acción Estratégica")
    m_selec = st.selectbox("Seleccionar Merchant:", merchants_master["Nombre"])
    m_data = merchants_master[merchants_master["Nombre"] == m_selec].iloc[0]
    
    # ETIQUETAS AUTOMÁTICAS
    etiqueta = calcular_etiqueta(m_data["TPV_Mensual"], m_data["Ticket_Promedio"])
    st.info(f"**Análisis de Potencialidad:** {etiqueta}")
    
    with st.form("registro_gec", clear_on_submit=True):
        accion = st.selectbox("¿Qué acción realizaste?", ["Fidelización", "Recuperación", "Upselling (Cuotas)", "Soporte"])
        resumen = st.text_area("Notas del contacto")
        prox_cita = st.date_input("Próximo contacto (Planificación)", datetime.now() + timedelta(days=7))
        estado_gec = st.select_slider("Estado en la GEC", options=["Zeta", "Construcción", "Maduro"])
        
        if st.form_submit_button("Guardar y Planificar"):
            nueva_fila = {
                "Fecha_Gestion": datetime.now().strftime("%Y-%m-%d"),
                "Merchant": m_selec,
                "Tipo_Accion": accion,
                "Resumen": resumen,
                "Proximo_Contacto": prox_cita,
                "Estado_GEC": estado_gec,
                "TPV_Potencial": m_data["TPV_Mensual"]
            }
            pd.DataFrame([nueva_fila]).to_csv(DB_FILE, mode='a', header=False, index=False)
            st.rerun()

with col_der:
    st.subheader("📚 Historial y Estrategia Pasada")
    m_hist = historial[historial["Merchant"] == m_selec].sort_values("Fecha_Gestion", ascending=False)
    
    if not m_hist.empty:
        for _, r in m_hist.iterrows():
            with st.expander(f"{r['Fecha_Gestion']} - {r['Tipo_Accion']}"):
                st.write(f"**Resumen:** {r['Resumen']}")
                st.caption(f"Próxima acción planificada para: {r['Proximo_Contacto'].date()}")
    else:
        st.info("Sin registros previos.")

# --- SECCIÓN "QUÉ MAS PUEDO HACER" (BAJA PRIORIDAD) ---
with st.expander("🔍 Ver Cartera No Prioritaria"):
    st.write("Aquí aparecen los merchants que ya están maduros o no requieren acción inmediata.")
    st.dataframe(merchants_master[merchants_master["Zeta"] == "Maduro"])
