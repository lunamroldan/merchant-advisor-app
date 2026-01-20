import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="GESTION ESTRATEGICA DE CARTERA", layout="wide")

# --- 1. PERSISTENCIA DE DATOS (ARCHIVO CSV) ---
DB_FILE = "base_datos_kam.csv"

def cargar_datos_persistentes():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    else:
        return pd.DataFrame(columns=["Fecha", "KAM", "Merchant", "CUIT", "Canal", "Resumen", "Compromiso", "Prioridad"])

def guardar_en_disco(nuevo_registro):
    df_actual = cargar_datos_persistentes()
    df_actual = pd.concat([df_actual, nuevo_registro], ignore_index=True)
    df_actual.to_csv(DB_FILE, index=False)
    return df_actual

# Carga inicial de la base histórica
historial_completo = cargar_datos_persistentes()

# --- 2. DATOS MAESTROS DE CARTERA ---
def get_cartera():
    data = {
        "CUIT": [30712345678, 20987654321, 33444555667],
        "NroComercio": [123456789, 987654321, 456123789],
        "Nombre": ["Tienda Alpha", "Bazar Beta", "Moda Gamma"],
        "Ventas_Mes": [15000, 8000, 12000],
        "Ventas_Prev": [14000, 9500, 12500],
        "Estado": ["🟢 MAM", "🔴 INACTIVO", "🟡 CHURN"]
    }
    df = pd.DataFrame(data)
    df['Variacion'] = ((df['Ventas_Mes'] - df['Ventas_Prev']) / df['Ventas_Prev']) * 100
    return df

# --- 3. INTERFAZ Y NAVEGACIÓN ---
st.sidebar.header("👤 Panel KAM")
nombre_kam = st.sidebar.text_input("Ingresa tu Nombre:", placeholder="Ej: Ana García")

if not nombre_kam:
    st.sidebar.warning("⚠️ Identifícate para operar.")
    st.title("🚀 GESTION ESTRATEGICA DE CARTERA")
    st.info("Por favor, ingresa tu nombre en el panel lateral.")
    st.stop()

st.sidebar.divider()
menu = st.sidebar.radio("Navegación:", ["🏠 Dashboard Home", "📝 Gestión de Comercio"])
df_cartera = get_cartera()

# --- 4. VISTA: DASHBOARD HOME ---
if menu == "🏠 Dashboard Home":
    st.title("📊 Resumen Estratégico de Cartera")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Merchants", len(df_cartera))
    m2.metric("TPV Total", f"${df_cartera['Ventas_Mes'].sum():,}")
    m3.metric("Gestiones Totales", len(historial_completo))

    st.divider()
    c_izq, c_der = st.columns(2)
    with c_izq:
        fig_bar = px.bar(df_cartera, x='Nombre', y='Ventas_Mes', color='Estado', title="TPV por Comercio")
        st.plotly_chart(fig_bar, use_container_width=True)
    with c_der:
        fig_pie = px.pie(df_cartera, names='Estado', hole=0.4, title="Estado de Salud")
        st.plotly_chart(fig_pie, use_container_width=True)

# --- 5. VISTA: GESTIÓN E HISTORIAL ---
else:
    st.title("📝 Gestión Individual y Trazabilidad")
    
    df_cartera['Selector'] = df_cartera['Nombre'] + " | CUIT: " + df_cartera['CUIT'].astype(str)
    merchant_label = st.selectbox("Selecciona un comercio:", df_cartera['Selector'])
    item = df_car
