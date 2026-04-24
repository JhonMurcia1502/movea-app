import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Importación de los módulos de MOVEA
from modules import modulo_1_dinamica
from modules import modulo_2_termo
from modules import modulo_3_isotopos
from modules import modulo_4_trazador

# Configuración global de la página
st.set_page_config(page_title="MOVEA - Física Atmosférica", layout="wide")


# --- SIDEBAR GLOBAL ---
st.sidebar.image("assets/images/globe.png", width=100)
st.sidebar.title("Navegación General")

# Menú Principal
opcion_global = st.sidebar.radio(
    "Selecciona un Módulo:", 
    ["🏠 Inicio", 
     "🌊 Módulo 1: El Gran Río", 
     "🔥 Módulo 2: Aire que se Eleva", 
     "⚗️ Módulo 3: La Huella Isotópica",
     "🕵️‍♂️ Módulo 4: El Veredicto del Trazador"
     ] # <--- NUEVA OPCIÓN
)

# --- ENRUTAMIENTO ---
if opcion_global == "🏠 Inicio":
    st.title("☁️ Proyecto MOVEA")
    st.markdown("""
    ### Bienvenid@ a MOVEA
    **Módulos Virtuales de Enseñanza y Aprendizaje en Física Atmosférica**
    
    La atmósfera está en constante movimiento. En su interior circula no solo aire, sino también energía, vapor de agua y pequeñas huellas moleculares que cuentan la historia del clima de la Tierra. 
    
    Este MOVEA te invita a recorrer ese viaje invisible: desde el movimiento de los grandes flujos atmosféricos, hasta el ascenso del vapor de agua y los procesos que transforman su composición isotópica. 
    
    A través de visualizaciones, simulaciones y datos satelitales reales, podrás explorar cómo el calor impulsa los movimientos del aire, cómo el vapor se eleva y cómo los isótopos del agua nos ayudan a rastrear el transporte de masas de aire en la atmósfera tropical. Explora, observa y comprende la física que conecta el calor, el agua y el movimiento del cielo. 
    
    **Selecciona un módulo en el menú de la izquierda para comenzar.**
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("🌊 **Módulo 1:** Dinámica de Fluidos y Circulación Global.")
    with col2:
        st.warning("🔥 **Módulo 2:** Termodinámica y Convección (El aire que sube).")
    with col3:
        st.success("⚗️ **Módulo 3:** Dinámica de Trazadores Atmosfericos y Fraccionamiento Isotopico (La Huella Isotópica).")
    with col4:
        st.info("🕵️‍♂️ **Módulo 4:** Dinámica de la Tropopausa (El veredicto del Trazador).")

    st.markdown("""
     El conocimiento sobre la atmósfera no solo está en los laboratorios o los satélites: también puede descubrirse en tu pantalla. MOVEA es una plataforma virtual interactiva diseñada para que aprendas física desde la observación, la experimentación y la exploración digital, comprendiendo los procesos que gobiernan el movimiento del aire, el agua y la energía en nuestro planeta. 

    Aquí encontrarás módulos temáticos independientes que te invitan a observar fenómenos, explicar lo que ocurre, entender los principios que los rigen y poner a prueba tus ideas. Cada módulo combina recursos visuales, simulaciones interactivas, videos, ejercicios y evaluaciones con retroalimentación inmediata, para que avances a tu ritmo, desde cualquier lugar y sin necesidad de registro. 

    MOVEA nace en el marco del proyecto de investigación “Aproximación física del comportamiento delisotopólogo HDO como trazador de masas deaire en la atmósfera tropical”, como un espacio abierto que une la física, la educación y la tecnología. Nuestro propósito es democratizar el acceso al conocimiento científico, ofreciendo un entorno intuitivo, accesible y gratuito para estudiantes, docentes y curiosos del mundo natural           

    **Explora, experimenta y comprende:**
    - Observa los fenómenos atmosféricos.
    - Interactúa con simulaciones PhET
    - Analiza, mide, gráfica y reflexiona
    - Evalua tu comprensión y comparte tus descubrimientos

    Porque aprender física es también una forma de mirar el mundo con nuevos ojos.

    **Guia de uso del sitio**

    La barra lateral te permite acceder a los cuatro módulos del curso.
            
    Cada módulo está estructurado en seis momentos:
    
    1. Observemos el fenómeno
    2. Expliquemos lo observado
    3. Entendiendo el fenómeno
    4. Hora de explorar
    5. Pon a prueba tu conocimiento
    6. Encuesta de satisfacción.
    
    Puedes recorrer los modulos en cualquier orden.
                
    **Intencionalidad pedagógica**
    
    MOVEA busca que el aprendizaje de la física atmosférica sea una experiencia activa, significativa y accesible, fomentando la curiosidad científica y el pensamiento analítico. Aquí, tú eres quien observa, predice, mide, analiza y explica. 

    **Autores y Colaboradores**
    
    **Jhon Eduar Murcia Cruz** - Licenciado en física, Universidad Distrital Francisco José de Caldas.
    
    **Karen Patricia Gaitan de los Rios** - PhD ...., Universidad Autonoma de Mexico. Licenciada en física, Universidad Distrital Francisco José de Caldas.
                
    """)


elif opcion_global == "🌊 Módulo 1: El Gran Río":
    modulo_1_dinamica.render()

elif opcion_global == "🔥 Módulo 2: Aire que se Eleva":
    modulo_2_termo.render() # <--- LLAMADA AL NUEVO MÓDULO

elif opcion_global == "⚗️ Módulo 3: La Huella Isotópica":
    modulo_3_isotopos.render()

elif opcion_global == "🕵️‍♂️ Módulo 4: El Veredicto del Trazador":
    modulo_4_trazador.render()