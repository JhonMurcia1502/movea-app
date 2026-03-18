import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import base64
import os

# --- CONFIGURACIÓN DE LAS UNIDADES ---
UNIDADES = {
    "1. Observemos el fenómeno": 1,
    "2. Expliquemos lo observado": 3,
    "3. Entendiendo el fenómeno": 6, 
    "4. Hora de explorar": 7, 
    "5. Pon a prueba tu conocimiento": 8,
    "6. Encuesta de satisfacción": 9
}

# --- FUNCIÓN IMÁGENES ---
def get_img_as_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

# --- FUNCIÓN PARA CARGAR TU HTML PERSONALIZADO ---
def cargar_simulador_html():
    ruta_html = "assets/html/simulador_isotopos.html"
    
    if os.path.exists(ruta_html):
        with open(ruta_html, 'r', encoding='utf-8') as f:
            html_content = f.read()
        # Renderizamos el HTML con altura suficiente y scroll
        components.html(html_content, height=800, scrolling=True)
    else:
        st.error(f"⚠️ No se encontró el archivo del simulador en: {ruta_html}")
        st.info("Por favor sube tu archivo HTML a la carpeta 'assets/html/' con el nombre 'simulador_isotopos.html'")

# --- POP-UPS / DIÁLOGOS ---
# --- POP-UPS / DIÁLOGOS ---
@st.dialog("H2O vs HDO")
def mostrar_moleculas():
    st.subheader("La diferencia está en el núcleo")
    
    # --- AQUÍ HABILITAMOS LA IMAGEN ---
    try: 
        # Asegúrate de subir esta imagen a tu carpeta assets/images/
        st.image("assets/images/mod3_detalle_nucleo.png", use_container_width=True)
    except: 
        st.info("💡 [Espacio para imagen: Sube 'mod3_detalle_nucleo.png' a assets/images/]")
        
    st.divider() # Una línea sutil para separar la imagen del texto
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### H₂O (Ligera)")
        st.write("Hidrógeno común. Masa: **18 g/mol**.")
        st.write("Es la más abundante.")
    with col2:
        st.markdown("### HDO (Semi-pesada)")
        st.write("Un Hidrógeno es reemplazado por **Deuterio** (tiene un neutrón extra).")
        st.write("Masa: **19 g/mol**.")

def render():
    # --- ESTADO INICIAL ---
    if 'paso_modulo3' not in st.session_state:
        st.session_state.paso_modulo3 = 1
    if 'resultados_quiz_m3' not in st.session_state:
        st.session_state.resultados_quiz_m3 = None

    # Navegación
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

    # ==========================================
    # DESARROLLO DEL CONTENIDO
    # ==========================================

    # --- UNIDAD 1: OBSERVA (INTRODUCCIÓN) ---
    if st.session_state.paso_modulo3 == 1:
        st.title("MÓDULO 3: LA HUELLA ISOTÓPICA")
        st.subheader("Dinámica de Trazadores Atmosféricos")
        
        st.markdown("""
        **Cambiamos de escala:** Dejaremos de ver la atmósfera solo como un fluido gigante para verla como un **laboratorio químico**.
        
        Pasaremos de los kilómetros a los ángstroms para entender cómo la composición del agua cambia mientras viaja por las nubes.
        Utilizaremos los isótopos como "espías" que nos cuentan la historia térmica del aire.
        """)
        st.info("👇 Presiona **Siguiente** para entrar al laboratorio.")

    # --- UNIDAD 1: OBSERVA (LOS ISOTOPÓLOGOS) ---
    elif st.session_state.paso_modulo3 == 2:
        st.header("1. Observemos el fenómeno")
        st.subheader("No toda el agua es igual 💧")
        
        st.markdown("""
        El agua común ($H_2O$) tiene una "hermana gemela" un poco más pesada llamada **HDO**.
        La diferencia es mínima pero fundamental: un neutrón extra.
        """)
        
        try: st.image("assets/images/mod3_moleculas.png", caption="Comparación molecular", use_container_width=True)
        except: st.warning("Falta imagen: mod3_moleculas.png")
        
        if st.button("🔍 Ver detalles moleculares"):
            mostrar_moleculas()

    # --- UNIDAD 2: EXPLIQUEMOS (LA PREGUNTA CLAVE) ---
    elif st.session_state.paso_modulo3 == 3:
        st.header("2. Expliquemos lo observado")
        st.subheader("La carrera de la condensación")
        
        col_txt, col_img = st.columns([1,1])
        with col_txt:
            st.markdown("""
            Si lanzamos vapor de $H_2O$ y HDO dentro de una nube que sube... **¿Cuál cae primero como lluvia?**
            
            La respuesta es el **HDO** (el pesado).
            
            **¿Por qué?** No solo por gravedad, sino por la **Presión de Vapor de Saturación**.
            El enlace del HDO es más fuerte, por lo que "prefiere" ser líquido. Requiere menos energía para condensarse que el agua normal.
            """)
        with col_img:
            try: st.image("assets/images/mod3_nube_lluvia.png", caption="El HDO cae preferencialmente", use_container_width=True)
            except: st.warning("Falta imagen: mod3_nube_lluvia.png")

    # --- UNIDAD 2: EXPLIQUEMOS (MODELO RAYLEIGH) ---
    elif st.session_state.paso_modulo3 == 4:
        st.header("2. Expliquemos lo observado")
        st.subheader("El Modelo de Destilación de Rayleigh")
        
        st.markdown("Para entender esto matemáticamente, comparamos dos sistemas:")
        
        tab1, tab2 = st.tabs(["1. Sistema Cerrado (Equilibrio)", "2. Sistema Abierto (Rayleigh)"])
        
        with tab1:
            st.info("""
            **La lluvia se queda con la nube.**
            El líquido formado viaja junto con el vapor. Mantienen contacto y se intercambian moléculas.
            *Resultado:* El vapor NO se empobrece tanto de HDO.
            """)
            
        with tab2:
            st.error("""
            **La lluvia abandona el sistema.**
            Apenas se forma la gota, cae y se va. 
            *Resultado:* La nube pierde masa constantemente. El vapor que queda se vuelve "pobre" en HDO muy rápido.
            **¡Así funciona la atmósfera real!**
            """)
        
        try: st.image("assets/images/mod3_rayleigh_esquema.png", caption="Comparación de sistemas", use_container_width=True)
        except: st.warning("Falta imagen: mod3_rayleigh_esquema.png")

    # --- UNIDAD 2: EXPLIQUEMOS (ECUACIÓN Y GRÁFICA) ---
    elif st.session_state.paso_modulo3 == 5:
        st.header("2. Expliquemos lo observado")
        st.subheader("La Matemática del Agotamiento")
        
        st.latex(r"R = R_0 \cdot f^{(\alpha - 1)}")
        
        st.markdown("""
        Esta ecuación predice cuánto HDO queda ($R$) basándose en cuánto vapor original queda ($f$).
        
        A medida que subimos (aumenta la altura), $f$ disminuye, y el HDO desaparece drásticamente.
        """)
        try: st.image("assets/images/mod3_grafica_ideal.png", caption="Perfil Ideal de Agotamiento Isotópico", use_container_width=True)
        except: st.warning("Falta imagen: mod3_grafica_ideal.png")

    # --- UNIDAD 3: ENTENDIENDO (DATOS REALES) ---
    elif st.session_state.paso_modulo3 == 6:
        st.header("3. Entendiendo el fenómeno")
        st.subheader("Observando la Realidad (Datos ACE-FTS)")
        
        st.markdown("""
        Estas gráficas muestran datos reales de la atmósfera tropical. 
        Mira la gráfica de la derecha ($\delta D$).
        """)
        
        try: st.image("assets/images/mod3_perfiles_ace.png", caption="Perfiles Verticales Reales (H2O, HDO y Delta-D)", use_container_width=True)
        except: st.warning("Falta imagen: mod3_perfiles_ace.png")
        
        st.success("""
        **Conclusión:**
        La curva roja se mueve a la izquierda (se agota) hasta los 16 km, tal como predice Rayleigh.
        
        ⚠️ **¡Ojo!** Arriba de 16 km, la curva se devuelve a la derecha (se enriquece). ¿Por qué? 
        Eso es un misterio que resolveremos en el próximo módulo.
        """)

    # --- UNIDAD 4: HORA DE EXPLORAR (HTML PERSONALIZADO) ---
    elif st.session_state.paso_modulo3 == 7:
        st.header("4. Hora de explorar")
        st.markdown("### Simulador de Fraccionamiento Isotópico")
        st.markdown("""
        Experimenta con una parcela de aire. Observa cómo cambia la proporción de moléculas azules ($H_2O$) 
        y rojas (HDO) a medida que la nube asciende y llueve.
        """)
        
        # --- AQUÍ CARGAMOS TU ARCHIVO HTML ---
        cargar_simulador_html()

    # --- UNIDAD 5: QUIZ ---
    elif st.session_state.paso_modulo3 == 8:
        st.header("5. Pon a prueba tu conocimiento")
        with st.form("quiz_m3"):
            st.write("Selecciona la respuesta correcta:")
            
            q1 = st.radio("1. ¿Qué diferencia principal tiene el HDO respecto al agua común?", 
                          ["Tiene dos oxígenos", "Tiene un neutrón extra (Deuterio)", "Es un gas noble"], index=None)
            
            q2 = st.radio("2. En el Modelo de Rayleigh (Sistema Abierto), ¿qué pasa con la lluvia?", 
                          ["Se queda en la nube", "Se evapora inmediatamente", "Es removida del sistema al instante"], index=None)
            
            q3 = st.radio("3. ¿Qué le pasa al vapor de agua remanente cuando la nube sube?", 
                          ["Se enriquece de HDO", "Se empobrece (pierde) HDO", "Mantiene su composición igual"], index=None)
            
            submitted = st.form_submit_button("Enviar Respuestas")
            if submitted:
                pts = 0
                if q1 == "Tiene un neutrón extra (Deuterio)": pts += 1
                if q2 == "Es removida del sistema al instante": pts += 1
                if q3 == "Se empobrece (pierde) HDO": pts += 1
                
                st.session_state.resultados_quiz_m3 = {"Puntaje": pts}
                if pts == 3: st.balloons(); st.success("¡Excelente! (3/3)")
                else: st.warning(f"Puntaje: {pts}/3")

    # --- UNIDAD 6: ENCUESTA ---
    elif st.session_state.paso_modulo3 == 9:
        st.header("6. Encuesta de satisfacción")
        with st.form("encuesta_m3"):
            user = st.text_input("Nombre / Código")
            rating = st.slider("Calificación Módulo 3", 1, 5, 5)
            comments = st.text_area("Comentarios sobre el tema de Isótopos")
            send = st.form_submit_button("Generar Reporte 💾", type="primary")
        
        if send:
            if not user: st.error("Falta nombre")
            else:
                q_data = st.session_state.resultados_quiz_m3
                nota = q_data["Puntaje"] if q_data else 0
                df = pd.DataFrame({
                    "Estudiante": [user], "Módulo": ["3-Isótopos"], "Nota": [nota], 
                    "Valoración": [rating], "Comentarios": [comments], "Fecha": [pd.Timestamp.now()]
                })
                csv = df.to_csv(index=False).encode('utf-8')
                st.success("¡Datos guardados!")
                st.balloons()
                st.download_button("Descargar Reporte", csv, f"Reporte_Mod3_{user}.csv", "text/csv")

    # --- FOOTER ---
    st.write("")
    st.divider()
    col_prev, col_vacia, col_next = st.columns([1, 4, 1])
    with col_prev:
        if st.session_state.paso_modulo3 > 1: st.button("⬅️ Atrás", on_click=anterior)
    with col_next:
        if st.session_state.paso_modulo3 < 9: st.button("Siguiente ➡️", on_click=siguiente)