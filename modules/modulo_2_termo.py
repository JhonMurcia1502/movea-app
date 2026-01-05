import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import base64

# --- CONFIGURACIÓN DE LAS UNIDADES ---
UNIDADES = {
    "1. Observemos el fenómeno": 1,
    "2. Expliquemos lo observado": 3,
    "3. Entendiendo el fenómeno": 6,
    "4. Hora de explorar": 8,
    "5. Pon a prueba tu conocimiento": 9,
    "6. Encuesta de satisfacción": 10
}

# --- URL SIMULADOR (PhET: Formas y Cambios de Energía) ---
URL_ENERGIA = "https://phet.colorado.edu/sims/html/energy-forms-and-changes/latest/energy-forms-and-changes_es.html"

# --- FUNCIÓN IMÁGENES ---
def get_img_as_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

def render():
    # --- ESTADO INICIAL ---
    if 'paso_modulo2' not in st.session_state:
        st.session_state.paso_modulo2 = 1
    if 'resultados_quiz_m2' not in st.session_state:
        st.session_state.resultados_quiz_m2 = None

    # Función de navegación lateral
    def ir_a_unidad():
        if st.session_state.selector_unidad_m2 in UNIDADES:
            st.session_state.paso_modulo2 = UNIDADES[st.session_state.selector_unidad_m2]

    def siguiente():
        st.session_state.paso_modulo2 += 1
    
    def anterior():
        st.session_state.paso_modulo2 -= 1

    # --- SIDEBAR (Barra Lateral) ---
    st.sidebar.markdown("---")
    st.sidebar.header("📍 Estructura Módulo 2")
    
    # Determinar unidad actual
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
    # DESARROLLO DEL CONTENIDO (Basado en PDF)
    # ==========================================

    # --- UNIDAD 1: OBSERVA (INTRO) ---
    if st.session_state.paso_modulo2 == 1:
        st.title("MÓDULO 2: EL AIRE QUE SE ELEVA")
        st.subheader("Transferencia de Calor y Convección")
        
        st.markdown("""
        ### Detrás de cada corriente de aire hay un motor silencioso: el calor.
        
        En este módulo aprenderás cómo la energía solar calienta la superficie de la Tierra, 
        generando movimientos verticales que dan origen a la **convección**.
        
        Descubre cómo el calor no solo se siente, sino que **mueve el mundo**.
        """)
        st.info("👇 Presiona **Siguiente** para comenzar el viaje.")

    # --- UNIDAD 1: OBSERVA (ANIMACIÓN GLOBAL) ---
    elif st.session_state.paso_modulo2 == 2:
        # Fondo animado o Imagen de Convección Global
        img_base64 = get_img_as_base64("assets/images/mod2_intro.gif")
        if img_base64:
             st.markdown(f"""<style>.stApp {{background-image: url("data:image/gif;base64,{img_base64}"); background-size: cover; background-attachment: fixed;}}</style>""", unsafe_allow_html=True)
        
        st.markdown("<h1 style='text-align: center; color: white; text-shadow: 2px 2px 4px #000;'>AIRE CÁLIDO ASCIENDE<br>AIRE FRÍO DESCIENDE</h1>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background-color: rgba(0,0,0,0.6); padding: 20px; border-radius: 10px; color: white; text-align: center; margin-top: 50px;'>
            <h3>Todo comienza con el Sol ☀️</h3>
            <p>La superficie absorbe radiación, se calienta y transfiere esa energía al aire.<br>
            Al calentarse, el aire se expande, se vuelve más ligero y... ¡Despega!</p>
        </div>
        """, unsafe_allow_html=True)

    # --- UNIDAD 2: EXPLIQUEMOS (ANALOGÍA OLLA) ---
    elif st.session_state.paso_modulo2 == 3:
        st.header("2. Expliquemos lo observado")
        st.subheader("La Física de la Convección")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Imagina una olla con agua hirviendo.** 🔥
            
            1. El fuego calienta el agua del fondo.
            2. El agua caliente se expande (baja su densidad) y sube a la superficie.
            3. Al llegar arriba, se enfría, se vuelve pesada y vuelve a bajar.
            
            **¡Esto mismo ocurre en la atmósfera!** Pero en lugar de una hornilla, tenemos la Tierra caliente.
            """)
        with col2:
            try: st.image("assets/images/mod2_olla.png", caption="Corrientes de convección", use_container_width=True)
            except: st.warning("Falta imagen: mod2_olla.png")

    # --- UNIDAD 2: EXPLIQUEMOS (DETALLE DENSIDAD) ---
    elif st.session_state.paso_modulo2 == 4:
        st.header("2. Expliquemos lo observado")
        st.subheader("¿Por qué flota el aire caliente?")
        
        st.info("""
        💡 **Concepto Clave: Densidad**
        
        Cuando el aire se calienta, sus moléculas se mueven más rápido y se separan.
        Ocupan más espacio con la misma cantidad de masa.
        
        **Mayor Temperatura ➡️ Menor Densidad ➡️ Flotabilidad (Ascenso)**
        """)
        
        st.write("Es el mismo principio que hace volar a los globos aerostáticos.")

    # --- UNIDAD 2: EXPLIQUEMOS (MONZÓN INTRO) ---
    elif st.session_state.paso_modulo2 == 5:
        st.header("2. Expliquemos lo observado")
        st.subheader("El Monzón de Norteamérica (NAM)")
        
        st.markdown("""
        En verano, el desierto de México y el suroeste de EE.UU. se calientan muchísimo más que el océano.
        
        Esto crea una gigantesca "burbuja" de aire caliente que sube con fuerza, actuando como una aspiradora 
        que atrae aire húmedo del mar.
        """)
        try: st.image("assets/images/mod2_monzon_mapa.png", caption="Sistema del Monzón de Norteamérica", use_container_width=True)
        except: st.warning("Falta imagen: mod2_monzon_mapa.png")

    # --- UNIDAD 3: ENTENDIENDO (DATOS SATELITALES) ---
    elif st.session_state.paso_modulo2 == 6:
        st.header("3. Entendiendo el fenómeno")
        st.subheader("Evidencia Satelital: La Chimenea de Humedad")
        
        st.markdown("""
        ¿Cómo sabemos que esto ocurre? Los satélites **ACE-FTS y MLS** nos permiten ver el vapor de agua (H₂O).
        
        Observa el siguiente gráfico real. Muestra cómo una columna de humedad inyecta agua desde la superficie 
        hasta lo más alto de la atmósfera durante el monzón.
        """)
        
        # Aquí iría tu gráfico de Matplotlib/Plotly con datos reales
        try: st.image("assets/images/mod2_perfil_h2o.png", caption="Perfil vertical de H2O (Datos Reales)", use_container_width=True)
        except: st.warning("Falta imagen: mod2_perfil_h2o.png")

    # --- UNIDAD 3: ENTENDIENDO (CONCLUSIÓN SATELITAL) ---
    elif st.session_state.paso_modulo2 == 7:
        st.header("3. Entendiendo el fenómeno")
        st.success("""
        **Lo que nos dicen los datos:**
        
        Esa "mancha" roja que sube en el gráfico anterior confirma la teoría: 
        la convección profunda es capaz de hidratar la estratosfera, superando la barrera del frío.
        """)
        st.write("Ahora es tu turno de experimentar con el calor.")

    # --- UNIDAD 4: HORA DE EXPLORAR (SIMULADOR) ---
    elif st.session_state.paso_modulo2 == 8:
        st.header("4. Hora de explorar")
        st.markdown("### Laboratorio: Formas y Cambios de Energía")
        
        st.info("""
        **Instrucciones:**
        1. Dentro del simulador, ve a la pestaña **"Sistemas"** (la segunda opción).
        2. Arrastra el símbolo de **Energía** (la 'E') para activarlo.
        3. Coloca un calentador debajo del recipiente con agua.
        4. **Observa:** ¿Ves los bloques de energía roja ('calor') subiendo? Eso es convección.
        """)
        
        components.iframe(URL_ENERGIA, height=600)

    # --- UNIDAD 5: QUIZ ---
    elif st.session_state.paso_modulo2 == 9:
        st.header("5. Pon a prueba tu conocimiento")
        st.markdown("Demuestra que eres un experto en termodinámica atmosférica.")
        st.write("---")
        
        with st.form("quiz_m2_form"):
            p1 = st.radio("1. ¿Cuál es el motor principal que impulsa el ascenso del aire?", 
                          ["La gravedad", "El calor (energía solar)", "La rotación de la tierra"], index=None)
            st.write("")
            p2 = st.radio("2. ¿Qué le pasa a la densidad del aire cuando se calienta?", 
                          ["Aumenta (se hace más pesado)", "Disminuye (se hace más ligero)", "Se queda igual"], index=None)
            st.write("")
            p3 = st.radio("3. El Monzón de Norteamérica es un ejemplo de...", 
                          ["Convección a gran escala impulsada por el calentamiento del continente", "Enfriamiento del océano", "Vientos polares"], index=None)
            st.write("")
            
            submitted = st.form_submit_button("Enviar Respuestas")
            
            if submitted:
                puntaje = 0
                if p1 == "El calor (energía solar)": puntaje +=1; st.success("1. ¡Correcto! El sol es la fuente de energía.")
                else: st.error("1. Incorrecto. Recuerda que el calor hace expandir el gas.")
                
                if p2 == "Disminuye (se hace más ligero)": puntaje +=1; st.success("2. ¡Correcto! Por eso asciende.")
                else: st.error("2. Incorrecto. El calor separa las moléculas, bajando la densidad.")
                
                if p3 == "Convección a gran escala impulsada por el calentamiento del continente": puntaje +=1; st.success("3. ¡Correcto! Es una gigantesca chimenea térmica.")
                else: st.error("3. Incorrecto.")
                
                # Guardar en sesión
                st.session_state.resultados_quiz_m2 = {"Puntaje": puntaje}
                
                if puntaje == 3: st.balloons(); st.markdown("### 🎉 ¡Excelente! (3/3)")
                else: st.markdown(f"### Tu puntaje: {puntaje}/3")

    # --- UNIDAD 6: ENCUESTA ---
    elif st.session_state.paso_modulo2 == 10:
        st.header("6. Encuesta de satisfacción")
        st.write("Ayúdanos a mejorar el Módulo 2.")
        
        with st.form("encuesta_m2"):
            usuario = st.text_input("Nombre / Código")
            claridad = st.slider("Claridad de la explicación de Convección", 1, 5, 5)
            simulador = st.slider("Utilidad del Simulador de Energía", 1, 5, 5)
            comentarios = st.text_area("Comentarios")
            
            btn_enviar = st.form_submit_button("Finalizar Módulo 2 💾", type="primary")
        
        if btn_enviar:
            if not usuario:
                st.error("Por favor ingresa tu nombre.")
            else:
                # Recuperar nota quiz
                quiz_data = st.session_state.resultados_quiz_m2
                nota = quiz_data["Puntaje"] if quiz_data else 0
                
                # Crear DataFrame
                datos = {
                    "Estudiante": [usuario],
                    "Módulo": ["2 - Termodinámica"],
                    "Nota Quiz": [nota],
                    "Eval Claridad": [claridad],
                    "Eval Simulador": [simulador],
                    "Comentarios": [comentarios],
                    "Fecha": [pd.Timestamp.now()]
                }
                df = pd.DataFrame(datos)
                csv = df.to_csv(index=False).encode('utf-8')
                
                st.success("¡Datos guardados!")
                st.balloons()
                st.download_button("Descargar Reporte Módulo 2", csv, f"Reporte_Mod2_{usuario}.csv", "text/csv")

    # --- FOOTER NAVEGACIÓN ---
    st.write("")
    st.divider()
    col_prev, col_vacia, col_next = st.columns([1, 4, 1])
    
    with col_prev:
        if st.session_state.paso_modulo2 > 1:
            st.button("⬅️ Atrás", on_click=anterior)
    
    with col_next:
        if st.session_state.paso_modulo2 < 10:
            st.button("Siguiente ➡️", on_click=siguiente)