import streamlit as st
# Importamos ambos módulos
from modules import modulo_1_dinamica
from modules import modulo_2_termo  # <--- NUEVO IMPORT

st.set_page_config(page_title="MOVEA - Física Atmosférica", layout="wide")

# --- SIDEBAR GLOBAL ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1162/1162951.png", width=100)
st.sidebar.title("Navegación General")

# Menú Principal
opcion_global = st.sidebar.radio(
    "Selecciona un Módulo:", 
    ["🏠 Inicio", "🌊 Módulo 1: El Gran Río", "🔥 Módulo 2: Aire que se Eleva"] # <--- NUEVA OPCIÓN
)

# --- ENRUTAMIENTO ---
if opcion_global == "🏠 Inicio":
    st.title("☁️ Proyecto MOVEA")
    st.markdown("""
    ### Bienvenid@ a MOVEA
    **Módulos Virtuales de Enseñanza y Aprendizaje en Física Atmosférica**
    
    Esta plataforma te permitirá explorar la dinámica de nuestra atmósfera utilizando:
    * 🛰️ Datos satelitales reales (ACE-FTS y MLS)
    * 🧪 Simuladores interactivos
    * 🧠 Retos conceptuales
    
    **Selecciona un módulo en el menú de la izquierda para comenzar.**
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("🌊 **Módulo 1:** Dinámica de Fluidos y Circulación Global.")
    with col2:
        st.warning("🔥 **Módulo 2:** Termodinámica y Convección (El aire que sube).")

elif opcion_global == "🌊 Módulo 1: El Gran Río":
    modulo_1_dinamica.render()

elif opcion_global == "🔥 Módulo 2: Aire que se Eleva":
    modulo_2_termo.render() # <--- LLAMADA AL NUEVO MÓDULO