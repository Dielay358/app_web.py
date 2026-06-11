import streamlit as st
import numpy as np
from scipy.stats import poisson
from google import genai
import os

# Configuración de la página
st.set_page_config(page_title="ZERORISK TOWER", page_icon="🏗️", layout="centered")

# --- ESTILOS Y LOGO ---
st.image("logo_unica.png", width=150)
st.title("🏗️ ZERORISK TOWER")
st.subheader("Sistema Inteligente de Control Estructural")

# --- BARRA LATERAL (ENTRADA DE DATOS) ---
st.sidebar.header("🎮 Parámetros de Operación")

radio = st.sidebar.slider("Radio del Carro (m)", 2.0, 45.0, 20.0)
cap_max = 8000 if radio <= 16.5 else 8000 * (16.5 / radio)
st.sidebar.info(f"📌 Capacidad máx para {radio}m: {cap_max:.1f}kg")

carga = st.sidebar.number_input("Masa de la Carga (kg)", 0.0, 8000.0, 1000.0)
viento = st.sidebar.slider("Velocidad del Viento (km/h)", 0, 100, 0)
mantenimiento = st.sidebar.slider("Nivel de Mantenimiento", 1, 10, 10)
contrapeso = st.sidebar.number_input("Masa del Contrapeso (kg)", 5000.0, 30000.0, 15000.0)

# --- LÓGICA DE INGENIERÍA ---
mv = (carga * radio) + (2500 * 22.5) + (0.005 * viento**2 * 15 * 50)
me = contrapeso * 12
fs = me / mv
pf = (1 - poisson.pmf(0, (12 - mantenimiento) / 12)) * 100
up = (carga / cap_max) * 100

# --- DASHBOARD DE MÉTRICAS ---
col1, col2, col3 = st.columns(3)

with col1:
    color = "normal" if fs > 1.3 else "inverse"
    st.metric("Factor Seguridad", f"{fs:.2f}", delta_color=color)
with col2:
    st.metric("Riesgo Mecánico", f"{pf:.1f}%")
with col3:
    st.metric("Uso Capacidad", f"{up:.1f}%")

# --- BOTÓN DE IA ---
if st.button("🧠 GENERAR DIAGNÓSTICO IA"):
    # Aquí puedes usar tu API Key (configurada como secreto en Streamlit)
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    prompt = f"Analiza para ZERORISK TOWER: FS {fs:.2f}, Capacidad {up:.1f}%, Viento {viento}km/h. Da diagnóstico y plan de acción."
    
    with st.spinner('El Ingeniero Senior está analizando...'):
        response = client.models.generate_content(model='gemini-flash-latest', contents=prompt)
        st.success("Análisis Completado")
        st.markdown(response.text)

st.divider()
st.caption("© 2026 - Proyecto Integrador de Ingeniería UNICA")