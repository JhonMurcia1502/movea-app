import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import base64
import os
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURACIÓN DE LAS UNIDADES ---
# Actualizado a 11 pasos totales para incluir el concepto de Fraccionamiento
UNIDADES = {
    "1. Observemos el fenómeno": 1,  # Pasos 1-3
    "2. Expliquemos lo observado": 4, # Pasos 4-7 (Se añade Fraccionamiento)
    "3. Entendiendo el fenómeno": 8, 
    "4. Hora de explorar": 9, 
    "5. Pon a prueba tu conocimiento y Encuesta": 10
}

# --- FUNCIÓN IMÁGENES ---
def get_img_as_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

# --- FUNCIÓN PARA CARGAR EL SIMULADOR HTML PERSONALIZADO ---
def cargar_simulador_html():
    ruta_html = "assets/html/Simulador destilacion.html"
    
    if os.path.exists(ruta_html):
        with open(ruta_html, 'r', encoding='utf-8') as f:
            html_content = f.read()
        components.html(html_content, height=800, scrolling=True)
    else:
        st.error(f"⚠️ No se encontró el archivo del simulador en: {ruta_html}")
        st.info("Por favor sube tu archivo HTML a la carpeta 'assets/html/' con el nombre 'simulador_isotopos.html'")

# --- POP-UPS / DIÁLOGOS ---
@st.dialog("H2O vs HDO")
def mostrar_moleculas():
    st.subheader("La diferencia está en el núcleo")
    try: 
        st.image("assets/images/M3_H2O-HDO.png", use_container_width=True)
    except: 
        st.info("💡 [Sube 'mod3_detalle_nucleo.png' a assets/images/]")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### H₂O (Ligera)")
        st.write("Hidrógeno común. Masa: **18 g/mol**.")
    with col2:
        st.markdown("### HDO (Semi-pesada)")
        st.write("Un Hidrógeno es reemplazado por **Deuterio**. Masa: **19 g/mol**.")

def render():
    # --- ESTADO INICIAL ---
    if 'paso_modulo3' not in st.session_state:
        st.session_state.paso_modulo3 = 1
    if 'resultados_quiz_m3' not in st.session_state:
        st.session_state.resultados_quiz_m3 = None

    def ir_a_unidad():
        if st.session_state.selector_unidad_m3 in UNIDADES:
            st.session_state.paso_modulo3 = UNIDADES[st.session_state.selector_unidad_m3]

    def siguiente():
        st.session_state.paso_modulo3 += 1
    
    def anterior():
        st.session_state.paso_modulo3 -= 1

    # --- SIDEBAR ---
    st.sidebar.markdown("---")
    st.sidebar.header("📍 Estructura Módulo 3")
    unidad_actual = "1. Observemos el fenómeno"
    for nombre, paso_inicio in UNIDADES.items():
        if st.session_state.paso_modulo3 >= paso_inicio:
            unidad_actual = nombre

    st.sidebar.radio(
        "Ir directamente a:",
        options=list(UNIDADES.keys()),
        index=list(UNIDADES.keys()).index(unidad_actual),
        key="selector_unidad_m3",
        on_change=ir_a_unidad
    )

    # --- CONTENIDO ---

    # PASO 1: INTRODUCCIÓN
    if st.session_state.paso_modulo3 == 1:
        st.title("MÓDULO 3: LA HUELLA ISOTÓPICA")
        st.subheader("Dinámica de Trazadores Atmosféricos Y PROCESOS DE FRACCIONAMIENTO")
        st.markdown("""
        En los módulos anteriores, observamos cómo el calor mueve masas gigantescas de aire a escala planetaria. Ahora, cambiaremos nuestra
        escala de observación: pasaremos de los kilómetros a los ángstroms.
        
        Dejaremos de ver la atmosfera solo como un fluido en movimiento para entenderla como un laboratorio de destilación. Utilizaremos la 
        composición química del agua como una 'caja negra' que registra la historia térmica de las nubes.
        """)

    # PASO 2: ANIMACIÓN DE TRANSICIÓN
    elif st.session_state.paso_modulo3 == 2:
        img_base64 = get_img_as_base64("assets/images/animacion_movea.gif")
        if img_base64:
             st.markdown(f"<style>.stApp {{background-image: url('data:image/gif;base64,{img_base64}'); background-size: cover; background-attachment: fixed;}}</style>", unsafe_allow_html=True)
        st.markdown("<br><br><h1 style='text-align: center; color: white; text-shadow: 3px 3px 5px #000;'>MÓDULO 3: LA HUELLA ISOTÓPICA - DINÁMICA DE TRAZADORES ATMOSFÉRICOS Y PROCESOS DE FRACCIONAMIENTO</h1>", unsafe_allow_html=True)
        st.markdown("<div style='background-color: rgba(0, 0, 0, 0.6); padding: 25px; border-radius: 15px; color: white; text-align: center;'><h3>En este módulo, dejaremos de ver el aire solo como un gas que se mueve, y empezaremos a analizar su composición química., la atmósfera actúa como un laboratorio de destilación. Cada proceso de condensación deja una firma química única.</h3></div>", unsafe_allow_html=True)

    # PASO 3: ISOTOPÓLOGOS
    elif st.session_state.paso_modulo3 == 3:
        st.header("1. Observemos el fenómeno")
        st.subheader("No toda el agua es igual 💧")
        st.markdown("Existen variaciones moleculares llamadas **Isotopólogos**. El más relevante para rastrear masas de aire es el **HDO**.")
        try: st.image("assets/images/Isotopos.png", caption="H2O vs HDO", use_container_width=True)
        except: st.warning("Falta imagen: mod3_moleculas.png")
        if st.button("🔍 Ver detalles moleculares"): mostrar_moleculas()

    # PASO 4: CARRERA DE CONDENSACIÓN
    elif st.session_state.paso_modulo3 == 4:
        st.header("2. Expliquemos lo observado")
        st.subheader("La pregunta clave")
        col_txt, col_img = st.columns(2)
        with col_txt:
            st.markdown("""
            Si lanzamos ambas moleculas (H₂O y HDO) DENTRO DE UNA NUBE CONVECTIVA QUE ASCIENDE RAPIDAMENTE...
                         
            ¿Cuál de las dos crees que "caerá" primero en forma de lluvia y porqué?
            """)
        with col_img:
            try: st.image("assets/images/mod3_nube_lluvia.png", caption="Preferencia de condensación")
            except: st.warning("Falta imagen: mod3_nube_lluvia.png")

    # PASO 5: FRACCIONAMIENTO ISOTÓPICO (NUEVO)
    elif st.session_state.paso_modulo3 == 5:
        st.header("2. Expliquemos lo observado")
        st.subheader("No es solo peso, es Energía")
        st.markdown("""
        Aunque el HDO es más pesado, la razón física real de su comportamiento es la Presión de Vapor de Saturación.
        """)
        col_f, col_icon = st.columns([2, 1])
        with col_f:
            st.info("""
                    $e_{sat}(HDO) < e_{sat}(H_2O)$
            """)
            st.markdown("El enlace de Hidrógeno-Deuterio es ligeramente más fuerte. Esto significa que el HDO prefiere estar en estado líquido. Requiere menos energía para condensarse y más energía para evaporarse.")
        with col_icon:
            st.image("assets/images/nube hdo.png", width=300)

    # PASO 6: MODELO RAYLEIGH (DESPLAZADO)
    elif st.session_state.paso_modulo3 == 6:
        st.header("2. Expliquemos lo observado")
        st.subheader("¿Cómo ocurre dicho proceso?")
        st.markdown("""
            Para modelar este proceso en la atmósfera, usamos el Modelo de Destilación de Rayleigh.
                    
            Pero primero debemos distinguir entre dos procesos de formación de nubes:
                    
        """)
        tab1, tab2 = st.tabs(["1. Sistema Cerrado (Equilibrio)", "2. Sistema Abierto (Rayleigh)"])
        with tab1: st.info("La lluvia se forma pero se queda dentro de la nubre, manteniendo contacto con el vapor.")
        with tab2: st.error("La lluvia se forma y cae inmediatamente.")
        try: st.image("assets/images/Rayleigh.png", width=520)
        except: st.warning("Falta imagen: mod3_rayleigh_esquema.png")

        st.markdown("""
                    En el modelo Rayleigh, la parcela de aire pierde masa constantemente. Como el HDO se va con la lluvia, el vapor que queda se vuelve cada vez más "pobre" o "ligero". Es un proceso de empobrecimiento irreversible.
                    """)

    # PASO 7: MATEMÁTICA (DESPLAZADO)
    elif st.session_state.paso_modulo3 == 7:
        st.header("2. Expliquemos lo observado")
        st.subheader("La Matemática del Agotamiento")
        colin, colgr = st.columns(2)
        
        with colin:
            st.markdown("La ecuación que predice el agotamiento del isotópologo es la siguiente:")
            st.latex(r"R = R_0 \cdot f^{(\alpha - 1)}")
            st.markdown("""
                    Donde:
                    - R: Relación isotópica final (HDO/H₂O).
                    - R₀: Relación inicial (en el océano).
                    - f: Fracción de vapor restante (disminuye con la altura).
                    - α: Factor de fraccionamiento (depende de la temperatura).
                    
                    La relación isotópica ($R$) depende de la fracción de vapor restante ($f$). A mayor altura, menos vapor queda y más 'agotada' está la huella química.""")
        with colgr:
            try: st.image("assets/images/Grafica.png", width=300)
            except: st.warning("Falta imagen")

    # PASO 8: DATOS REALES (DESPLAZADO)
    elif st.session_state.paso_modulo3 == 8:
        st.header("3. Entendiendo el fenómeno")
        st.subheader("Observando la Realidad (Datos ACE-FTS)")
        st.markdown("Estas gráficas nos permiten observar la concentración de agua, agua deuterada y el agotamiento de agua deuterada en la atmosfera tropical.")
        try: st.image("assets/images/Perfil Vertical Fraccionamiento.png", use_container_width=True)
        except: st.warning("Falta imagen")
        st.success("Si observamos detalladamente podemos ver como el agotamiento ocurre hasta la altura de 16km aproximadamente, tal cual predice el modelo de Raileygh. No obstante despues se muestra un incremento, el motivo detras de esto lo veremos en el ultimo modulo.")

    # PASO 9: SIMULADOR
    elif st.session_state.paso_modulo3 == 9:
        st.header("4. Hora de explorar")
        st.markdown("Ahora que conocemos la teória es momento de verla en acción, utiliza el siguiente simulador para observar como ocurre el agotamiento de HDO en una parcela de aire a medida que asciende.")
        cargar_simulador_html()

# PASO 10: QUIZ Y ENCUESTA UNIFICADOS
    elif st.session_state.paso_modulo3 == 10:
        st.header("5. Pon a prueba tu conocimiento y Encuesta Final")
        st.markdown("Es momento de consolidar tu aprendizaje sobre fraccionamiento isotópico.")
        
        estudiante = st.text_input("Ingresa tu Nombre o Código de Estudiante:")
        
        with st.form("evaluacion_m3"):
            st.subheader("A. Quiz de Huella Isotópica")
            q1 = st.radio("1. ¿Qué es el fraccionamiento isotópico?", ["La ruptura de moléculas", "El reparto desigual de isótopos en un cambio de fase"], index=None)
            q2 = st.radio("2. Si alpha es mayor a 1, el HDO...", ["Prefiere ser vapor", "Prefiere ser líquido"], index=None)
            q3 = st.radio("3. ¿Cuál modelo describe mejor la atmósfera real donde la lluvia cae?", ["Equilibrio", "Rayleigh"], index=None)
            
            st.divider()
            st.subheader("B. Encuesta de Satisfacción")
            valoracion = st.slider("Valora tu aprendizaje en este módulo (1 = Bajo, 5 = Alto)", 1, 5, 5)
            comentarios = st.text_area("¿Algún comentario o duda sobre la destilación de Rayleigh?")
            
            enviado = st.form_submit_button("Enviar Resultados y Finalizar", type="primary")
            
            if enviado:
                if not estudiante:
                    st.warning("⚠️ Necesitamos tu nombre para guardar el progreso.")
                elif q1 is None or q2 is None or q3 is None:
                    st.warning("⚠️ No olvides responder todas las preguntas.")
                else:
                    with st.spinner("Enviando datos al servidor de MOVEA..."):
                        try:
                            pts = 0
                            if q1 == "El reparto desigual de isótopos en un cambio de fase": pts += 1
                            if q2 == "Prefiere ser líquido": pts += 1
                            if q3 == "Rayleigh": pts += 1
                            
                            url_hoja = "https://docs.google.com/spreadsheets/d/1DVRJmYBDmAaJkLrxgCOedtglRfzSHyOcs0VfLNh_OFA/edit"
                            conn = st.connection("gsheets", type=GSheetsConnection)
                            df_existente = conn.read(spreadsheet=url_hoja)
                            
                            nuevo_registro = pd.DataFrame([{
                                "Fecha": pd.Timestamp.now(tz="America/Bogota").strftime("%Y-%m-%d %H:%M:%S"),
                                "Estudiante": estudiante,
                                "Modulo": "3-Isotopos",
                                "Puntaje": f"{pts}/3",
                                "Q1_Respuesta": q1,
                                "Q2_Respuesta": q2,
                                "Q3_Respuesta": q3,
                                "Valoracion": valoracion,
                                "Comentarios": comentarios
                            }])
                            
                            df_actualizado = pd.concat([df_existente, nuevo_registro], ignore_index=True)
                            conn.update(spreadsheet=url_hoja, data=df_actualizado)
                            
                            st.success(f"¡Datos registrados, {estudiante}! Gran trabajo analizando isótopos.")
                            if pts == 3: st.balloons()
                        except Exception as e:
                            st.error(f"Error de red: {e}")

    # FOOTER
    st.divider()
    col_prev, col_next = st.columns([1, 1])
    with col_prev:
        if st.session_state.paso_modulo3 > 1: st.button("⬅️ Atrás", on_click=anterior, key="btn_atras_m3")
    with col_next:
        # Ajustado a 10 pasos máximos
        if st.session_state.paso_modulo3 < 10: st.button("Siguiente ➡️", on_click=siguiente, key="btn_sig_m3")