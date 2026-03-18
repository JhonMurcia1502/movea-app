import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import base64

# --- CONFIGURACIÓN DE LAS UNIDADES ---
# Ajustamos los índices porque agregamos una pantalla más (Total: 12 pasos)
UNIDADES = {
    "1. Observemos el fenómeno": 1,
    "2. Expliquemos lo observado": 3,
    "3. Entendiendo el fenómeno": 7, # Se mueve al 7
    "4. Hora de explorar": 10,       # Se mueve al 10
    "5. Pon a prueba tu conocimiento": 11,
    "6. Encuesta de satisfacción": 12
}

# --- URL SIMULADOR ---
URL_ENERGIA = "https://phet.colorado.edu/sims/html/energy-forms-and-changes/latest/energy-forms-and-changes_es.html"

# --- FUNCIÓN IMÁGENES ---
def get_img_as_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

# --- POP-UPS (Unidad 2) ---
@st.dialog("Concepto: Densidad")
def mostrar_densidad():
    st.subheader("¿Por qué sube el aire?")
    st.markdown("""
    **La clave es la DENSIDAD.**
    
    Imagina una caja llena de pelotas (moléculas).
    * **Aire Frío:** Las pelotas están quietas y apretadas. Pesan más.
    * **Aire Caliente:** Las pelotas se mueven rápido y se separan. Ocupan más espacio pero pesan menos.
    
    Al ser más ligero, el aire caliente flota sobre el frío.
    """)

@st.dialog("Mecanismo de Transferencia")
def mostrar_mecanismo(tipo):
    if tipo == "radiacion":
        st.subheader("1. Radiación ☀️")
        st.markdown("Es energía que viaja por el espacio. El Sol emite ondas electromagnéticas hasta la Tierra.")
        try: st.image("assets/images/mod2_radiacion.png")
        except: st.warning("Falta img")
        if st.button("Siguiente: Conducción ➡️"): st.session_state.popup_mecanismo = "conduccion"; st.rerun()

    elif tipo == "conduccion":
        st.subheader("2. Conducción 🔥")
        st.markdown("Es calor por contacto directo. El suelo caliente pasa energía al aire que lo toca.")
        try: st.image("assets/images/mod2_conduccion.png")
        except: st.warning("Falta img")
        col_prev, col_next = st.columns(2)
        with col_prev:
            if st.button("⬅️ Anterior"): st.session_state.popup_mecanismo = "radiacion"; st.rerun()
        with col_next:
            if st.button("Siguiente: Convección ➡️"): st.session_state.popup_mecanismo = "conveccion"; st.rerun()

    elif tipo == "conveccion":
        st.subheader("3. Convección 🌬️")
        st.markdown("Es calor en movimiento. El aire caliente sube transportando energía.")
        try: st.image("assets/images/mod2_conveccion.png")
        except: st.warning("Falta img")
        col_prev, col_next = st.columns(2)
        with col_prev:
            if st.button("⬅️ Anterior"): st.session_state.popup_mecanismo = "conduccion"; st.rerun()
        with col_next:
            if st.button("🔄 Cerrar y Continuar"): st.session_state.popup_mecanismo = None; st.rerun()

def render():
    # --- ESTADO INICIAL ---
    if 'paso_modulo2' not in st.session_state:
        st.session_state.paso_modulo2 = 1
    if 'resultados_quiz_m2' not in st.session_state:
        st.session_state.resultados_quiz_m2 = None
    if 'popup_mecanismo' not in st.session_state:
        st.session_state.popup_mecanismo = None
    if 'vista_monzon' not in st.session_state:
        st.session_state.vista_monzon = 'intro'

    # Seguridad: Si no estamos en el paso del Monzón (9), resetear vista
    if st.session_state.paso_modulo2 != 9:
        st.session_state.vista_monzon = 'intro'

    # Activar Popups
    if st.session_state.popup_mecanismo is not None:
        mostrar_mecanismo(st.session_state.popup_mecanismo)

    def ir_a_unidad():
        if st.session_state.selector_unidad_m2 in UNIDADES:
            st.session_state.paso_modulo2 = UNIDADES[st.session_state.selector_unidad_m2]
            st.session_state.vista_monzon = 'intro'

    def siguiente():
        st.session_state.paso_modulo2 += 1
        st.session_state.vista_monzon = 'intro'
    
    def anterior():
        st.session_state.paso_modulo2 -= 1
        st.session_state.vista_monzon = 'intro'

    # --- SIDEBAR ---
    st.sidebar.markdown("---")
    st.sidebar.header("📍 Estructura Módulo 2")
    unidad_actual = "1. Observemos el fenómeno"
    for nombre, paso_inicio in UNIDADES.items():
        if st.session_state.paso_modulo2 >= paso_inicio:
            unidad_actual = nombre

    st.sidebar.radio(
        "Ir directamente a:",
        options=list(UNIDADES.keys()),
        index=list(UNIDADES.keys()).index(unidad_actual),
        key="selector_unidad_m2",
        on_change=ir_a_unidad
    )

    # ==========================================
    # DESARROLLO DEL CONTENIDO
    # ==========================================

    # --- UNIDAD 1: OBSERVA ---
    if st.session_state.paso_modulo2 == 1:
        st.title("MÓDULO 2: EL AIRE QUE SE ELEVA")
        st.subheader("Transferencia de Calor y Convección")
        st.markdown("""
        ### Detrás de cada corriente de aire hay un motor silencioso: el calor.
        En este módulo aprenderás cómo la energía solar calienta la superficie de la Tierra, 
        generando movimientos verticales que dan origen a la **convección**. Este fenómeno no solo transporta calor,
        sino tambien vapor de agua e isótopos hacia las capas superiores de la atmósfera.
                    
        A partir de simulaciones, imagenes satelitales y la observación de los monzones
        -grandes sistemas de circulación impulsados por el calor- comprenderás como el aire
        se eleva, cómo se enfria y cómo este ciclo alimenta la dinámica global de la atmósfera.
        El calor no solo se siente, también se mueve. Descubre cómo da vida al aire que asciende.
        """)
        st.info("👇 Presiona **Siguiente** para comenzar.")

    elif st.session_state.paso_modulo2 == 2:
        img_base64 = get_img_as_base64("assets/images/mod2_intro.gif")
        if img_base64:
             st.markdown(f"""<style>.stApp {{background-image: url("data:image/gif;base64,{img_base64}"); background-size: cover; background-attachment: fixed;}}</style>""", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: white; text-shadow: 2px 2px 4px #000;'>AIRE CÁLIDO ASCIENDE ⬆️<br>AIRE FRÍO DESCIENDE ⬇️</h1>", unsafe_allow_html=True)
        st.markdown("""
            El calor impulsa los grandes movimientos del aire.
            Descubramos cómo la energía solar genera el ascenso del vapor de agua que alimenta la atmósfera.
            """)

    # --- UNIDAD 2: EXPLIQUEMOS (PANTALLA RESTAURADA: EL SOL) ---
    elif st.session_state.paso_modulo2 == 3:
        st.header("2. Expliquemos lo observado")
        st.subheader("Todo comienza con el Sol ☀️")
        
        col_txt, col_img = st.columns([1, 1])
        with col_txt:
            st.markdown("""
            La superficie de la Tierra absorbe la radiación solar y se calienta. 
            Este calor se transfiere al aire que está en contacto directo con ella.
            
            **La Cadena de Eventos:**
            1. El suelo se calienta.
            2. Transfiere calor al aire (Conducción).
            3. El aire se expande y sube (Convección).

            Este movimiento vertical de ascenso de aire caliente es el motor de la convección
            """)
            if st.button("🔍 ¿Por qué sube? (Click aquí)"):
                mostrar_densidad()

        with col_img:
            try: st.image("assets/images/mod2_sol_tierra.png", caption="Calentamiento Superficial", use_container_width=True)
            except: st.warning("Falta imagen: mod2_sol_tierra.png")

    # --- UNIDAD 2: EXPLIQUEMOS (3 BOTONES) ---
    elif st.session_state.paso_modulo2 == 4:
        st.header("2. Expliquemos lo observado")
        st.subheader("¿Cómo viaja el calor?")
        st.markdown("""
        La transferencia de calor es el proceso físico mediante el cual la energía térmica se transporta de un
        sistema de mayor temperatura a uno de menor temperatura.
        
        En la atmósfera, este balande energético se mantiene por tres mecanismos:
        
         **Haz clic sobre cada uno para ver un ejemplo**
                    """)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("https://cdn-icons-png.flaticon.com/512/169/169367.png", width=80)
            if st.button("1. Conducción", use_container_width=True): st.session_state.popup_mecanismo = "conduccion"; st.rerun()
        with col2:
            st.image("https://cdn-icons-png.flaticon.com/512/1541/1541486.png", width=80)
            if st.button("2. Radiación", use_container_width=True): st.session_state.popup_mecanismo = "radiacion"; st.rerun()
        with col3:
            st.image("https://cdn-icons-png.flaticon.com/512/950/950986.png", width=80)
            if st.button("3. Convección", use_container_width=True): st.session_state.popup_mecanismo = "conveccion"; st.rerun()

    # --- UNIDAD 2: EXPLIQUEMOS (ANALOGÍA OLLA) ---
    elif st.session_state.paso_modulo2 == 5:
        st.header("2. Expliquemos lo observado")
        st.subheader("La Analogía de la Olla")
        st.markdown("La convección es el movimiento del fluido, tal como ocurre en tu cocina al hervir agua.")
        col_olla, col_atm = st.columns(2)
        with col_olla:
            try: st.image("assets/images/mod2_olla.png", caption="Olla hirviendo", use_container_width=True)
            except: st.warning("Falta mod2_olla.png")
        with col_atm:
            st.info("**En la atmósfera:**\nEl suelo caliente actúa como la estufa, haciendo que el aire suba y cree celdas de circulación.")

    # --- UNIDAD 2: EXPLIQUEMOS (PUENTE/CLAVE) ---
    elif st.session_state.paso_modulo2 == 6:
        st.header("2. Expliquemos lo observado")
        st.subheader("De los tres, ¿Cúal es el que mueve el aire?")
        st.markdown("""
            Los tres procesos ocurren al mismo tiempo, pero tienen roles diferentes para el movimiento del aire:

            1. **La Conducción**: Es importante, pero solo camienta la finísima capa de aire que esta
            en contacto directo con el suelo.

            2. **La Radiación**: Calienta la superficie y algunas partes de la atmosfera, pero es la 
            convección el único mecanismo que físicamente transporta ese aire caliente y húmedo desde 
            la superficie hacia lo alto de la atmósfera.
            """)
        st.subheader("Por lo tanto, para entender cómo asciende el vapor de agua...")
        st.subheader("... la **CONVECCIÓN** es el proceso clave que debemos estudiar.")

    # ==========================================================
    # --- UNIDAD 3: ENTENDIENDO EL FENÓMENO ---
    # ==========================================================

    # PANTALLA 1: DEFINICIÓN DE CONVECCIÓN
    elif st.session_state.paso_modulo2 == 7:
        st.header("3. Entendiendo el fenómeno")
        st.subheader("La Convección Atmosférica")
        col_def, col_img = st.columns(2)
        with col_def:
            st.markdown("""
            **Definición:**
            Es el mecanismo de transporte de calor dominante en la troposfera.
            
            Ocurre cuando el aire caliente y menos denso asciende, se enfria en las alturas,
            y el aire mas frío y denso desciende para tomar su lugar. Este ciclo constante,
            conodido como celda convectiva, transporta verticalmente calor, humedad y energia.
            """)
        with col_img:
            try: st.image("assets/images/mod2_def_conveccion.png", caption="Esquema de Convección", use_container_width=True)
            except: st.info("[Imagen: Esquema general]")

    # PANTALLA 2: DEFINICIÓN DE CONVECCIÓN PROFUNDA
    elif st.session_state.paso_modulo2 == 8:
        st.header("3. Entendiendo el fenómeno")
        st.subheader("Convección Profunda")
        col_def, col_img = st.columns(2)
        with col_def:
            st.markdown("""
            **Definición:**
            Es un tipo de convección muy intensa y potente.

            En los tropicos, la energía solar es tan intensa que las corrientes ascendentes pueden "perforar"
            toda la troposfera hasta alcanzar  la tropopausa. (La tapa de la atmosfera ~17km).
            """)
        with col_img:
                try: 
                        st.video(
                        "assets/images/mod2_video_profunda.mp4", 
                        autoplay=True, 
                        loop=True, 
                        muted=True
                    )
                except Exception as e: 
                    st.info("💡 [Sube tu video 'mod2_video_profunda.mp4' a la carpeta assets/images/]")

    # PANTALLA 3: EL MONZÓN (HUB DE NAVEGACIÓN)
    elif st.session_state.paso_modulo2 == 9:
        st.header("3. Entendiendo el fenómeno")
        
        # --- VISTA PRINCIPAL ---
        if st.session_state.vista_monzon == 'intro':
            st.subheader("El Monzón")
    
            st.markdown("""
            **Definición:**
            Un monzón es el ejemplo más espectacular de convección
            estacional a gran escala. No es solo lluvia; es un
            'interruptor' en la circualción atmosférica.
                        
            Durante el verano, la tierra se calienta mucho más rapido
            que el océano. Este diferencial extremo de temperatura 
            crea una zona de baja presión sobre el continente, que
            literalmente 'aspira' el aire increiblemente húmedo del
            ocpeano. Este aire asciende masivamente, se enfría y genera 
            lluias torrenciales

            """)
            st.info("Explora los ejemplos:")

            st.divider()
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                st.markdown("##### Caso A: Norteamérica")
                if st.button("🌎 Ver Monzón de Norteamérica", use_container_width=True):
                    st.session_state.vista_monzon = 'nam'; st.rerun()
            with col_btn2:
                st.markdown("##### Caso B: Asia / Otro")
                if st.button("🌏 Ver Monzón Asiático", use_container_width=True):
                    st.session_state.vista_monzon = 'asia'; st.rerun()

        # --- SUB-PANTALLAS ---
        elif st.session_state.vista_monzon == 'nam':
            st.subheader("El Monzón de Norteamérica (NAM)")
            st.markdown("El calor del desierto impulsa una convección profunda que transporta humedad desde el Golfo de California.")
            try: st.image("assets/images/mod2_monzon_nam.png", caption="Mapa del NAM", use_container_width=True)
            except: st.warning("Falta imagen")
            if st.button("⬅️ Volver a definiciones"): st.session_state.vista_monzon = 'intro'; st.rerun()

        elif st.session_state.vista_monzon == 'asia':
            st.subheader("El Monzón Asiático")
            st.markdown("El sistema monzónico más grande del mundo. Genera lluvias torrenciales en la India y el Sudeste Asiático.")
            try: st.image("assets/images/mod2_monzon_asia.png", caption="Mapa Asia", use_container_width=True)
            except: st.warning("Falta imagen")
            if st.button("⬅️ Volver a definiciones"): st.session_state.vista_monzon = 'intro'; st.rerun()

    # --- UNIDAD 4: HORA DE EXPLORAR ---
    elif st.session_state.paso_modulo2 == 10:
        st.header("4. Hora de explorar")
        st.markdown("### Laboratorio: Formas y Cambios de Energía")
        st.markdown("**Tu Misión:** Activa 'Símbolos de Energía' y calienta el agua para ver la convección.")
        components.iframe(URL_ENERGIA, height=650)

    # --- UNIDAD 5: QUIZ ---
    elif st.session_state.paso_modulo2 == 11:
        st.header("5. Pon a prueba tu conocimiento")
        with st.form("quiz_m2_form"):
            p1 = st.radio("1. Mecanismo que mueve calor por contacto:", ["Radiación", "Conducción", "Convección"], index=None)
            st.write("")
            p2 = st.radio("2. ¿Qué caracteriza a la convección profunda?", ["Solo ocurre en el suelo", "Llega hasta la tropopausa", "Es horizontal"], index=None)
            st.write("")
            p3 = st.radio("3. El Monzón se produce por...", ["Diferencia térmica Tierra-Mar", "Fases Lunares", "Mareas"], index=None)
            
            submitted = st.form_submit_button("Enviar Respuestas")
            if submitted:
                puntaje = 0
                if p1 == "Conducción": puntaje +=1
                if p2 == "Llega hasta la tropopausa": puntaje +=1
                if p3 == "Diferencia térmica Tierra-Mar": puntaje +=1
                
                st.session_state.resultados_quiz_m2 = {"Puntaje": puntaje}
                if puntaje == 3: st.balloons(); st.success("¡Perfecto! (3/3)")
                else: st.warning(f"Tu puntaje: {puntaje}/3")

    # --- UNIDAD 6: ENCUESTA ---
    elif st.session_state.paso_modulo2 == 12:
        st.header("6. Encuesta de satisfacción")
        
        # 1. Formulario
        with st.form("encuesta_m2"):
            usuario = st.text_input("Nombre / Código")
            claridad = st.slider("Claridad", 1, 5, 5)
            comentarios = st.text_area("Comentarios")
            btn_enviar = st.form_submit_button("Generar Reporte 💾", type="primary")
        
        # 2. Lógica post-envío (Botón descarga fuera del form)
        if btn_enviar:
            if not usuario:
                st.error("Ingresa tu nombre.")
            else:
                quiz_data = st.session_state.resultados_quiz_m2
                nota = quiz_data["Puntaje"] if quiz_data else "N/A"
                datos = {"Estudiante": [usuario], "Módulo": ["2"], "Nota": [nota], "Claridad": [claridad], "Comentarios": [comentarios], "Fecha": [pd.Timestamp.now()]}
                df = pd.DataFrame(datos)
                csv = df.to_csv(index=False).encode('utf-8')
                st.success("¡Gracias!"); st.balloons()
                st.download_button("Descargar Reporte", csv, f"Reporte_Mod2_{usuario}.csv", "text/csv")

    # --- FOOTER ---
    st.write("")
    st.divider()
    col_prev, col_vacia, col_next = st.columns([1, 4, 1])
    
    with col_prev:
        mostrar_atras = True
        if st.session_state.paso_modulo2 == 9 and st.session_state.vista_monzon != 'intro':
            mostrar_atras = False
        
        if st.session_state.paso_modulo2 > 1 and mostrar_atras:
            st.button("⬅️ Atrás", on_click=anterior, key="atras_m2")
            
    with col_next:
        mostrar_siguiente = True
        if st.session_state.paso_modulo2 == 9 and st.session_state.vista_monzon != 'intro':
            mostrar_siguiente = False
            
        if st.session_state.paso_modulo2 < 12 and mostrar_siguiente:
            st.button("Siguiente ➡️", on_click=siguiente, key="sig_m2")