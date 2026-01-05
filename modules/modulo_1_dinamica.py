import streamlit as st
import streamlit.components.v1 as components
import pandas as pd # <--- IMPORTANTE: Necesario para generar el Excel/CSV
import base64
import time

# --- CONFIGURACIÓN DE LAS UNIDADES ---
UNIDADES = {
    "1. Observemos el fenómeno": 1,
    "2. Expliquemos lo observado": 3, 
    "3. Entendiendo el fenómeno": 6, 
    "4. Hora de explorar": 9,
    "5. Pon a prueba tu conocimiento": 10,
    "6. Encuesta de satisfacción": 11
}

# --- URLs SIMULADORES ---
URL_MATERIA = "https://phet.colorado.edu/sims/html/states-of-matter/latest/states-of-matter_es.html"
URL_GASES = "https://phet.colorado.edu/sims/html/gas-properties/latest/gas-properties_es.html"
URL_PRESION = "https://phet.colorado.edu/sims/html/under-pressure/latest/under-pressure_es.html"

# --- FUNCIÓN IMÁGENES ---
def get_img_as_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

# --- POP-UPS ---
@st.dialog("Detalle del Proceso")
def mostrar_popup(fase_id):
    if fase_id == 1:
        st.subheader("1. Ascenso Tropical")
        st.markdown("El aire cálido y húmedo en el ecuador es calentado por el sol, subiendo rápidamente hasta la tropopausa.")
        try: st.image("assets/images/fase1_ascenso.png")
        except: st.warning("Falta imagen")
        if st.button("Siguiente Fase ➡️"):
            st.session_state.popup_activo = 2
            st.rerun()
    elif fase_id == 2:
        st.subheader("2. Transporte hacia los Polos")
        st.markdown("El aire se mueve horizontalmente hacia los polos, llevando ozono y vapor de agua.")
        try: st.image("assets/images/fase2_transporte.png")
        except: st.warning("Falta imagen")
        col_back, col_next = st.columns(2)
        with col_back:
            if st.button("⬅️ Fase Anterior"):
                st.session_state.popup_activo = 1
                st.rerun()
        with col_next:
            if st.button("Siguiente Fase ➡️"):
                st.session_state.popup_activo = 3
                st.rerun()
    elif fase_id == 3:
        st.subheader("3. Descenso en Latitudes Medias")
        st.markdown("Al enfriarse en latitudes altas, el aire desciende nuevamente.")
        try: st.image("assets/images/fase3_descenso.png")
        except: st.warning("Falta imagen")
        if st.button("🔄 Volver al inicio"):
            st.session_state.popup_activo = None
            st.rerun()

def render():
    # --- ESTADO INICIAL ---
    if 'paso_modulo1' not in st.session_state:
        st.session_state.paso_modulo1 = 1
    if 'popup_activo' not in st.session_state:
        st.session_state.popup_activo = None
    if 'view_simulador' not in st.session_state:
        st.session_state.view_simulador = 'menu'
    
    # Inicializar variable para guardar respuestas del QUIZ en memoria
    if 'resultados_quiz' not in st.session_state:
        st.session_state.resultados_quiz = None

    # Seguridad: Mostrar botones siempre, excepto dentro de simulador
    if st.session_state.paso_modulo1 != 9:
        st.session_state.view_simulador = 'menu'

    if st.session_state.popup_activo is not None:
        mostrar_popup(st.session_state.popup_activo)

    def ir_a_unidad():
        if st.session_state.selector_unidad in UNIDADES:
            st.session_state.paso_modulo1 = UNIDADES[st.session_state.selector_unidad]
            st.session_state.view_simulador = 'menu'

    def siguiente():
        st.session_state.paso_modulo1 += 1
        st.session_state.view_simulador = 'menu'
    
    def anterior():
        st.session_state.paso_modulo1 -= 1
        st.session_state.view_simulador = 'menu'

    # --- SIDEBAR ---
    st.sidebar.markdown("---")
    st.sidebar.header("📍 Estructura del Módulo")
    unidad_actual = "1. Observemos el fenómeno"
    for nombre, paso_inicio in UNIDADES.items():
        if st.session_state.paso_modulo1 >= paso_inicio:
            unidad_actual = nombre

    st.sidebar.radio(
        "Ir directamente a:",
        options=list(UNIDADES.keys()),
        index=list(UNIDADES.keys()).index(unidad_actual),
        key="selector_unidad",
        on_change=ir_a_unidad
    )

    # --- CONTENIDO ---

    if st.session_state.paso_modulo1 == 1:
        st.title("MÓDULO 1: \"EL GRAN RÍO DEL CIELO\"")
        st.markdown("### El aire que respiramos no está quieto.")
        st.write("Desde los trópicos hasta los polos, la atmósfera fluye como un inmenso río que transporta energía, vapor de agua y trazadores invisibles. En este módulo conocerás cómo se mueve ese fluido y descubrirás el papel de la circulación Brewer–Dobson, un proceso clave que impulsa el ascenso del aire en los trópicos y su descenso en latitudes medias." \
        " A través de visualizaciones globales y experimentos interactivos, observarás cómo el aire cálido asciende, cómo el frío desciende y cómo este movimiento constante mantiene en equilibrio la atmósfera." \
        " Prepárate para mirar al cielo como un océano en movimiento, donde cada corriente cuenta una historia del clima.")
        st.info("👇 Presiona **Siguiente** para continuar.")

    elif st.session_state.paso_modulo1 == 2:
        img_base64 = get_img_as_base64("assets/images/AnimacionBD.gif")
        if img_base64:
             st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("data:image/gif;base64,{img_base64}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            .texto-overlay {{
                background-color: rgba(0, 0, 0, 0.7);
                color: white;
                padding: 30px;
                border-radius: 10px;
                text-align: center;
                margin-top: 20px;
                backdrop-filter: blur(5px);
            }}
            </style>
            """, unsafe_allow_html=True)
        
        st.markdown("<h1 style='text-align: center; color: white; text-shadow: 2px 2px 4px #000;'>EL GRAN RÍO DEL CIELO</h1>", unsafe_allow_html=True)
        st.markdown("""
        <div class="texto-overlay">
            <h3>¿Sabías qué la atmosfera está compuesta de fluidos de tipo gaseoso como el vapor de agua y cambia constantemente?</h3>
        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.paso_modulo1 == 3:
        st.header("2. Expliquemos lo observado")
        col_txt, col_img = st.columns(2)
        with col_txt:
            st.markdown("### La Circulación Global")
            st.write("Explicación general del fenómeno Brewer-Dobson...")
        with col_img:
            try: st.image("assets/images/esquema_bd.png")
            except: st.write("Falta img")

    elif st.session_state.paso_modulo1 == 4:
        st.header("2. Expliquemos lo observado")
        st.subheader("Las 3 Fases del Motor Atmosférico")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔥 Ascenso Tropical", use_container_width=True):
                st.session_state.popup_activo = 1
                st.rerun()
        with col2:
            if st.button("✈️ Transporte Hacia Polos", use_container_width=True):
                st.session_state.popup_activo = 2
                st.rerun()
        with col3:
            if st.button("❄️ Descenso Polar", use_container_width=True):
                st.session_state.popup_activo = 3
                st.rerun()

    elif st.session_state.paso_modulo1 == 5:
        st.header("2. Expliquemos lo observado")
        st.subheader("Conclusiones Clave")
        st.info("**1. El Motor Térmico**\n\nEl sol calienta el ecuador más que los polos...")
        st.warning("**2. La Cinta Transportadora**\n\nEste flujo distribuye gases de efecto invernadero...")
        st.success("**3. Escala de Tiempo**\n\nNo es un viento rápido; es una circulación lenta...")

    elif st.session_state.paso_modulo1 == 6:
        st.header("3. Entendiendo el fenómeno")
        st.subheader("Concepto 1: El Fluido")
        st.markdown("Un fluido es cualquier sustancia que no tiene una forma fija...")
        try: st.image("assets/images/concepto_fluido.gif", use_container_width=True)
        except: st.warning("Falta gif fluido")

    elif st.session_state.paso_modulo1 == 7:
        st.header("3. Entendiendo el fenómeno")
        st.subheader("Concepto 2: El Flujo")
        st.markdown("Es el movimiento del fluido...")
        try: st.image("assets/images/concepto_flujo.gif", use_container_width=True)
        except: st.warning("Falta gif flujo")

    elif st.session_state.paso_modulo1 == 8:
        st.header("3. Entendiendo el fenómeno")
        st.subheader("Concepto 3: La Circulación")
        st.markdown("Cuando el flujo se organiza en un patrón cerrado...")
        try: st.image("assets/images/concepto_circulacion.gif", use_container_width=True)
        except: st.warning("Falta gif circulacion")

    elif st.session_state.paso_modulo1 == 9:
        st.header("4. Hora de explorar")
        if st.session_state.view_simulador == 'menu':
            st.markdown("Selecciona un simulador para comenzar:")
            col_sim1, col_sim2, col_sim3 = st.columns(3)
            with col_sim1:
                st.image("https://phet.colorado.edu/sims/html/states-of-matter/latest/states-of-matter-600.png")
                if st.button("🧊 Estados de la Materia", use_container_width=True):
                    st.session_state.view_simulador = 'materia'; st.rerun()
            with col_sim2:
                st.image("https://phet.colorado.edu/sims/html/gas-properties/latest/gas-properties-600.png")
                if st.button("🎈 Propiedades de los Gases", use_container_width=True):
                    st.session_state.view_simulador = 'gases'; st.rerun()
            with col_sim3:
                st.image("https://phet.colorado.edu/sims/html/under-pressure/latest/under-pressure-600.png")
                if st.button("🌊 Bajo Presión", use_container_width=True):
                    st.session_state.view_simulador = 'presion'; st.rerun()
        elif st.session_state.view_simulador == 'materia':
            components.iframe(URL_MATERIA, height=600)
            if st.button("⬅️ Volver al menú"): st.session_state.view_simulador = 'menu'; st.rerun()
        elif st.session_state.view_simulador == 'gases':
            components.iframe(URL_GASES, height=600)
            if st.button("⬅️ Volver al menú"): st.session_state.view_simulador = 'menu'; st.rerun()
        elif st.session_state.view_simulador == 'presion':
            components.iframe(URL_PRESION, height=600)
            if st.button("⬅️ Volver al menú"): st.session_state.view_simulador = 'menu'; st.rerun()

    # === PASO 10: QUIZ INTERACTIVO (CON GUARDADO EN MEMORIA) ===
    elif st.session_state.paso_modulo1 == 10:
        st.header("5. Pon a prueba tu conocimiento")
        st.markdown("Selecciona la respuesta correcta para cada pregunta.")
        st.write("---")
        with st.form("quiz_form"):
            r1 = st.radio("1. ¿Cuál es la mejor definición de un fluido?", ["Sustancia siempre líquida", "Sustancia sin forma fija que se deforma", "Gas que cambia color"], index=None)
            st.write("")
            r2 = st.radio("2. La Circulación Brewer-Dobson es fundamental porque...", ["Genera huracanes", "Transporta químicos y vapor hacia los polos", "Enfría la superficie"], index=None)
            st.write("")
            r3 = st.radio("3. El 'Tape Recorder' atmosférico nos muestra evidencia de:", ["Ascenso lento en trópicos", "Velocidad del viento", "Temperatura del océano"], index=None)
            st.write("")
            r4 = st.radio("4. En el simulador, al calentar un gas en volumen fijo, la presión...", ["Disminuye", "Se mantiene", "Aumenta"], index=None)
            st.write("")
            submitted = st.form_submit_button("Enviar Respuestas")
            
            if submitted:
                puntaje = 0
                if r1 == "Sustancia sin forma fija que se deforma": puntaje += 1; st.success("1. Correcto")
                else: st.error("1. Incorrecto")
                
                if r2 == "Transporta químicos y vapor hacia los polos": puntaje += 1; st.success("2. Correcto")
                else: st.error("2. Incorrecto")

                if r3 == "Ascenso lento en trópicos": puntaje += 1; st.success("3. Correcto")
                else: st.error("3. Incorrecto")

                if r4 == "Aumenta": puntaje += 1; st.success("4. Correcto")
                else: st.error("4. Incorrecto")

                # --- GUARDADO EN SESSION_STATE ---
                # Guardamos las respuestas en la memoria del navegador para usarlas al final
                st.session_state.resultados_quiz = {
                    "Puntaje_Quiz": puntaje,
                    "Resp_1": r1,
                    "Resp_2": r2,
                    "Resp_3": r3,
                    "Resp_4": r4
                }

                if puntaje == 4: st.balloons(); st.markdown("### 🎉 ¡Perfecto! (4/4)")
                else: st.markdown(f"### Tu puntaje: {puntaje}/4")
                
                st.info("Tus resultados han sido guardados temporalmente. Continúa a la encuesta para finalizar.")
# === PASO 11: ENCUESTA Y REPORTE FINAL (CORREGIDO) ===
    elif st.session_state.paso_modulo1 == 11:
        st.header("6. Encuesta de satisfacción")
        st.markdown("""
        ¡Has llegado al final del Módulo 1! 
        Por favor, responde estas breves preguntas para generar tu **Certificado de Finalización** (Reporte).
        """)
        
        # 1. EL FORMULARIO (Solo para recoger datos)
        with st.form("encuesta_form"):
            col_eval1, col_eval2 = st.columns(2)
            
            with col_eval1:
                st.markdown("**Claridad del contenido**")
                val_claridad = st.slider("¿Qué tan fácil fue entender los conceptos?", 1, 5, 5, key="val_claridad")
                
            with col_eval2:
                st.markdown("**Recursos Visuales**")
                val_visual = st.slider("¿Te ayudaron las animaciones y simuladores?", 1, 5, 5, key="val_visual")
                
            st.markdown("**Comentarios Adicionales**")
            comentarios = st.text_area("¿Qué te gustaría ver en los próximos módulos?", placeholder="Escribe aquí tu opinión...")
            
            # Identificación
            usuario = st.text_input("Nombre o Código de Estudiante (Obligatorio para el reporte)")

            st.write("")
            # El botón de envío solo cambia el estado, NO descarga nada aún
            btn_enviar_encuesta = st.form_submit_button("Generar Reporte Completo 💾", type="primary")

        # 2. LÓGICA FUERA DEL FORMULARIO (Se ejecuta al presionar el botón)
        if btn_enviar_encuesta:
            if not usuario:
                st.error("⚠️ Por favor ingresa tu nombre dentro del formulario para generar el reporte.")
            else:
                # A. Recuperar datos del Quiz
                datos_quiz = st.session_state.resultados_quiz
                if datos_quiz is None:
                    datos_quiz = {"Puntaje_Quiz": "No presentado", "Resp_1": "N/A", "Resp_2": "N/A", "Resp_3": "N/A", "Resp_4": "N/A"}

                # B. Consolidar TODO
                datos_finales = {
                    "Estudiante": [usuario],
                    "Fecha": [pd.Timestamp.now()],
                    "Eval_Claridad": [val_claridad],
                    "Eval_Visual": [val_visual],
                    "Comentarios": [comentarios],
                    "Quiz_Puntaje": [datos_quiz["Puntaje_Quiz"]],
                    "Quiz_R1": [datos_quiz["Resp_1"]],
                    "Quiz_R2": [datos_quiz["Resp_2"]],
                    "Quiz_R3": [datos_quiz["Resp_3"]],
                    "Quiz_R4": [datos_quiz["Resp_4"]],
                }
                
                # C. Generar CSV
                df_resultados = pd.DataFrame(datos_finales)
                csv = df_resultados.to_csv(index=False).encode('utf-8')

                # D. Mostrar Éxito
                st.success("¡Gracias! Módulo completado exitosamente.")
                st.balloons()
                
                st.markdown("### 📥 Tu Reporte de Estudiante")
                st.write("Descarga este archivo. Contiene tu nota del examen y tu constancia de participación.")
                
                # E. BOTÓN DE DESCARGA (Ahora sí está fuera del form y funcionará)
                st.download_button(
                    label="Descargar Reporte (.csv)",
                    data=csv,
                    file_name=f"Reporte_MOVEA_Mod1_{usuario}.csv",
                    mime="text/csv",
                )

    # --- FOOTER ---
    st.write("")
    st.divider()
    col_prev, col_vacia, col_next = st.columns([1, 4, 1])
    
    with col_prev:
        mostrar_atras = False
        if st.session_state.paso_modulo1 > 1: mostrar_atras = True
        if st.session_state.paso_modulo1 == 9 and st.session_state.view_simulador != 'menu': mostrar_atras = False
        if mostrar_atras: st.button("⬅️ Atrás", on_click=anterior, key="btn_atras")
    
    with col_next:
        if st.session_state.paso_modulo1 == 5:
             st.button("🧠 Entender la teoría ➡️", on_click=siguiente, type="primary", use_container_width=True)
        else:
            mostrar_siguiente = False
            if st.session_state.paso_modulo1 < 11: mostrar_siguiente = True
            if st.session_state.paso_modulo1 == 9 and st.session_state.view_simulador != 'menu': mostrar_siguiente = False
            if mostrar_siguiente: st.button("Siguiente ➡️", on_click=siguiente, key="btn_siguiente")