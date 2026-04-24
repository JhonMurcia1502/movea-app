import streamlit as st
import streamlit.components.v1 as components
import pandas as pd # <--- IMPORTANTE: Necesario para generar el Excel/CSV
import base64
import time
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURACIÓN DE LAS UNIDADES ---
UNIDADES = {
    "1. Observemos el fenómeno": 1,
    "2. Expliquemos lo observado": 3, 
    "3. Entendiendo el fenómeno": 6, 
    "4. Hora de explorar": 9,
    "5. Pon a prueba tu conocimiento y Encuesta": 10
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
@st.dialog("Tape Recorder")
def mostrar_popup(fase_id):
    if fase_id == 1:
        st.subheader("Zona tropical")
        st.markdown("En el trópico, bajo el dominio de la célula de Hadley, observamos la señal canónica del tape recorder. Las bandas diagonales ascendentes muestran cómo el aire, al elevarse, transporta la firma estacional del vapor de agua hacia la estratosfera. Este patrón es la evidencia directa del lento ascenso que define la rama ascendente de la circulación Brewer-Dobson.")
        try: st.image("assets/images/Tape Recorder Tropical.png")
        except: st.warning("Falta imagen")
        if st.button("Siguiente ➡️"):
            st.session_state.popup_activo = 2
            st.rerun()
    elif fase_id == 2:
        st.subheader("Latitudes medias")
        st.markdown("En las latitudes medias, la señal de ascenso desaparece. La dinámica aquí está dominada por la célula de Ferrel, que se caracteriza por un movimiento de aire superficial hacia los polos y un descenso de aire estratosférico. El gráfico muestra un fuerte ciclo estacional, pero sin la propagación vertical vista en el trópico, indicando una ausencia de ascenso neto a gran escala hacia la estratosfera.")
        try: st.image("assets/images/Tape Recorder Medias.png")
        except: st.warning("Falta imagen")
        col_back, col_next = st.columns(2)
        with col_back:
            if st.button("⬅️ Anterior"):
                st.session_state.popup_activo = 1
                st.rerun()
        with col_next:
            if st.button("Siguiente ➡️"):
                st.session_state.popup_activo = 3
                st.rerun()
    elif fase_id == 3:
        st.subheader("Zona polar")
        st.markdown("En las regiones polares, el aire es extremadamente seco, una característica del dominio de la célula Polar. Este es el punto de descenso principal de la circulación Brewer-Dobson. El aire que ha viajado por la estratosfera pierde su humedad y desciende de nuevo a la troposfera, por lo que no se observa ninguna señal de ascenso, sino un fuerte ciclo anual influenciado por el vórtice polar.")
        try: st.image("assets/images/Tape Recorder Polar.png")
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
            st.markdown("### Un océano de aire organizado: La Circulación Global")
            st.write("Aunque el movimiento del aire puede parecer caótico, a gran escala se organiza en gigantescos patrones de circulación que distribuyen el calor desde el ecuador hacia los polos. Estas son las tres célular principales en cada hemisferio:")
            st.info("**1. Célula de Hadley (0° a 30°)**\n\nEl motor del trópico. El aire caliente y húmedo asciende en el ecuador, se enfria, y luego desciende en las zonas subtropicales.")
            st.warning("**2. Célula de Ferrel (30° a 60°)**\n\nLa célula de las latitudes medias. No es impulsada directamente por la temperatura, si no que actúa como un engranaje entre las otras dos célular, con un movimiento promedio de aire superficial hacia los polos.")
            st.success("**3. Célula Polar (60° a 90°)**\n\nEn los polos, el aire frío y denso desciende y se desplaza hacia latitudes más bajas.")

        with col_img:
            try: st.image("assets/images/celulas-hadley-2.jpg")
            except: st.write("Falta img")

    elif st.session_state.paso_modulo1 == 4:
        st.header("2. Expliquemos lo observado")
        st.subheader("Evidencia del transporte atmosférico: La señal del Tape Recorder")
        st.write("El 'tape recorder' atmosférico es un término análogo utilizado para describir la 'grabación' de las variaciones estacionales de un trazador químico (como el vapor de agua) en las masas de aire que ascienden lentamente en la estratosfera tropical. A medida que el aire sube, transporta consigo la firma de la concentración del trazador presente en la tropopausa, creando un patrón vertical que, al ser visualizado en el tiempo se semeja a las bandas de una cinta magnética. Este fenómeno constituye una de las evidencias más directas del lento ascenso de la céñula de Hadley hacia la estratosfera.")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Zona Tropical", use_container_width=True):
                st.session_state.popup_activo = 1
                st.rerun()
        with col2:
            if st.button("Latitudes Medias", use_container_width=True):
                st.session_state.popup_activo = 2
                st.rerun()
        with col3:
            if st.button("Zona Polar", use_container_width=True):
                st.session_state.popup_activo = 3
                st.rerun()

    elif st.session_state.paso_modulo1 == 5:
        st.header("2. Expliquemos lo observado")
        st.subheader("¿Notaste los patrones?")
        st.write("Como viste, la señal de ascenso clara del 'Tape Recorder' solo aparece en la zona tropical. En las latitudes medias y polares, el patrón es muy diferente. ¿Por qué ocurre esto?")
        st.success("La respuesta está en los principios fundamentales que gobiernan la atmósfera. Para entenderlo, necesitamos definir dos ideas clave: Fluido y Flujo.")

    elif st.session_state.paso_modulo1 == 6:
        st.header("3. Entendiendo el fenómeno")
        st.subheader("El Fluido")
        col_fluido, col_imgfluido = st.columns(2)
        with col_fluido:
            st.markdown("En física, un fluido es una sustancia que se deforma continuamente bajo la aplicación de una tensión cortante, sin importar cuán pequeña sea. En términos más simples, es una sustancia cuyas partículas no tienen una posición fija y pueden moverse con libertad."
                    "\n\nEl aire que compone nuestra atmósfera, una mezcla de gases como nitrógeno, oxígeno y vapor de agua, es un ejemplo clásico de un fluido compresible.")
        with col_imgfluido:
            try: st.video(
                    "assets/images/H2O GLOBAL.mp4",
                    autoplay=True,
                    loop=True,
                    muted=True
            )
            except: st.warning("Falta gif fluido")

    elif st.session_state.paso_modulo1 == 7:
        st.header("3. Entendiendo el fenómeno")
        st.subheader("El Flujo")
        col_flujo, col_flujoimg = st.columns(2)
        with col_flujo:
            st.markdown("El flujo es el movimiento macroscópico y colectivo de un fluido. Es el resultado de diferencias de presión y temperatura que impulsan a las partículas del fluido en una dirección general. En la atmósfera, este movimiento se manifiesta como el viento."
                        "\n\nEl flujo puede ser:"
                        "\n1. Laminar: Suave y ordenado, con capas de fluido que se deslizan unas sobre otras."
                        "\n2. Turbulento: Caótico e irregular, con remolinos y vórtices.")
        with col_flujoimg:
            try: st.video(
                    "assets/images/H2O GLOBAL.mp4",
                    autoplay=True,
                    loop=True,
                    muted=True
            )
            except: st.warning("Falta gif flujo")

    elif st.session_state.paso_modulo1 == 8:
        st.header("3. Entendiendo el fenómeno")
        st.subheader("La Circulación BD")
        col_circ, col_circimg = st.columns(2)
        with col_circ:
            st.markdown("La Circulación de Brewer-Dobson es un modelo que describe el flujo promedio y a gran escala del fluido atmosférico en la estratosfera. No es un viento que se pueda medir en un solo lugar, sino un lento movimiento residual a escala planetaria."
                        "\n\nEste flujo es el principal mecanismo de transporte de masa y energía entre la estratosfera tropical y la polar, siendo responsable de la distribución global de trazadores clave como el ozono y el vapor de agua.")
        with col_circimg:
            try: st.image("assets/images/AnimacionBD.gif", use_container_width=True)
            except: st.warning("Falta gif circulacion")

    elif st.session_state.paso_modulo1 == 9:
        st.header("4. Hora de explorar")
        if st.session_state.view_simulador == 'menu':
            st.markdown("El movimiento del aire, su temperatura y presión están conectados. Para complementar la teoría, experimenta tú mismo con estos conceptos en los simuladores interactivos de PhET Colorado." \
            "\nSelecciona un simulador para comenzar:")
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
            st.info("Observa cómo se comportan las partículas al cambiar la temperatura. ¿Qué le pasa al 'aire' cuando se calienta?")
            components.iframe(URL_MATERIA, height=600)
            if st.button("⬅️ Volver al menú"): st.session_state.view_simulador = 'menu'; st.rerun()
        elif st.session_state.view_simulador == 'gases':
            st.info("Explora la relación entre la presión y la temperatura en un gas como el aire.")
            components.iframe(URL_GASES, height=600)
            if st.button("⬅️ Volver al menú"): st.session_state.view_simulador = 'menu'; st.rerun()
        elif st.session_state.view_simulador == 'presion':
            st.info("Descubre cómo cambia la presión con la altitud en un fluido.")
            components.iframe(URL_PRESION, height=600)
            if st.button("⬅️ Volver al menú"): st.session_state.view_simulador = 'menu'; st.rerun()

    # === PASO 10: QUIZ Y ENCUESTA UNIFICADOS ===
    elif st.session_state.paso_modulo1 == 10:
        st.header("5. Pon a prueba tu conocimiento y Encuesta Final")
        st.markdown("Selecciona la respuesta correcta para cada pregunta y evalúa este módulo.")
        
        estudiante = st.text_input("Ingresa tu Nombre o Código de Estudiante:")
        
        with st.form("evaluacion_m1"):
            st.subheader("A. Quiz de Dinámica de Fluidos")
            r1 = st.radio("1. ¿Cuál es la mejor definición de un fluido?", ["Sustancia siempre líquida", "Sustancia sin forma fija que se deforma", "Gas que cambia color"], index=None)
            r2 = st.radio("2. La Circulación Brewer-Dobson es fundamental porque...", ["Genera huracanes", "Transporta químicos y vapor hacia los polos", "Enfría la superficie"], index=None)
            r3 = st.radio("3. El 'Tape Recorder' atmosférico nos muestra evidencia de:", ["Ascenso lento en trópicos", "Velocidad del viento", "Temperatura del océano"], index=None)
            r4 = st.radio("4. En el simulador, al calentar un gas en volumen fijo, la presión...", ["Disminuye", "Se mantiene", "Aumenta"], index=None)
            
            st.divider()
            st.subheader("B. Encuesta de Satisfacción")
            valoracion = st.slider("¿Qué tan fácil fue entender los conceptos y simuladores? (1 = Difícil, 5 = Muy fácil)", 1, 5, 5)
            comentarios = st.text_area("¿Qué te gustaría ver en los próximos módulos o qué mejorarías?")
            
            enviado = st.form_submit_button("Enviar Resultados y Finalizar", type="primary")
            
            if enviado:
                if not estudiante:
                    st.warning("⚠️ Por favor ingresa tu nombre antes de enviar.")
                elif r1 is None or r2 is None or r3 is None or r4 is None:
                    st.warning("⚠️ Por favor responde todas las preguntas del quiz.")
                else:
                    with st.spinner("Sincronizando con la base de datos..."):
                        try:
                            pts = 0
                            if r1 == "Sustancia sin forma fija que se deforma": pts += 1
                            if r2 == "Transporta químicos y vapor hacia los polos": pts += 1
                            if r3 == "Ascenso lento en trópicos": pts += 1
                            if r4 == "Aumenta": pts += 1
                            
                            url_hoja = "https://docs.google.com/spreadsheets/d/1DVRJmYBDmAaJkLrxgCOedtglRfzSHyOcs0VfLNh_OFA/edit"
                            conn = st.connection("gsheets", type=GSheetsConnection)
                            df_existente = conn.read(spreadsheet=url_hoja)
                            
                            nuevo_registro = pd.DataFrame([{
                                "Fecha": pd.Timestamp.now(tz="America/Bogota").strftime("%Y-%m-%d %H:%M:%S"),
                                "Estudiante": estudiante,
                                "Modulo": "1-Dinamica",
                                "Puntaje": f"{pts}/4",
                                "Q1_Respuesta": r1,
                                "Q2_Respuesta": r2,
                                "Q3_Respuesta": r3,
                                "Q4_Respuesta": r4,
                                "Valoracion": valoracion,
                                "Comentarios": comentarios
                            }])
                            
                            df_actualizado = pd.concat([df_existente, nuevo_registro], ignore_index=True)
                            conn.update(spreadsheet=url_hoja, data=df_actualizado)
                            
                            st.success(f"¡Gracias {estudiante}! Módulo completado exitosamente.")
                            if pts == 4: st.balloons()
                        except Exception as e:
                            st.error(f"Error de conexión: {e}")

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
            # Ajustado a 10 pasos máximos
            if st.session_state.paso_modulo1 < 10: mostrar_siguiente = True
            if st.session_state.paso_modulo1 == 9 and st.session_state.view_simulador != 'menu': mostrar_siguiente = False
            if mostrar_siguiente: st.button("Siguiente ➡️", on_click=siguiente, key="btn_siguiente")