import streamlit as st
import pandas as pd
import base64
import streamlit.components.v1 as components
import os

# --- CONFIGURACIÓN DE LAS UNIDADES ---
UNIDADES = {
    "1. Observemos el fenómeno": 1, 
    "2. Expliquemos lo observado": 3, 
    "3. Entendiendo el fenómeno": 5, 
    "4. Hora de explorar": 6, 
    "5. Pon a prueba tu conocimiento": 7,
    "6. Encuesta de satisfacción": 8
}

def get_img_as_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

def render():
    if 'paso_modulo4' not in st.session_state:
        st.session_state.paso_modulo4 = 1
    if 'resultados_quiz_m4' not in st.session_state:
        st.session_state.resultados_quiz_m4 = None

    def ir_a_unidad():
        if st.session_state.selector_unidad_m4 in UNIDADES:
            st.session_state.paso_modulo4 = UNIDADES[st.session_state.selector_unidad_m4]

    def siguiente():
        st.session_state.paso_modulo4 += 1
    
    def anterior():
        st.session_state.paso_modulo4 -= 1

    # ---- Función HTML ---

    def cargar_simulador_trazador():
        ruta_html = "assets/html/simulador_trazador.html"
        if os.path.exists(ruta_html):
            with open(ruta_html, 'r', encoding='utf-8') as f:
                html_content = f.read()
        # El alto de 800px es ideal para que quepan los controles y la gráfica
            components.html(html_content, height=800, scrolling=True)
        else:
            st.error("No se encontró el archivo del simulador.")

    # --- SIDEBAR ---
    st.sidebar.markdown("---")
    st.sidebar.header("📍 Estructura Módulo 4")
    unidad_actual = "1. Observemos el fenómeno"
    for nombre, paso_inicio in UNIDADES.items():
        if st.session_state.paso_modulo4 >= paso_inicio:
            unidad_actual = nombre

    st.sidebar.radio(
        "Ir directamente a:",
        options=list(UNIDADES.keys()),
        index=list(UNIDADES.keys()).index(unidad_actual),
        key="selector_unidad_m4",
        on_change=ir_a_unidad
    )

    # ==========================================
    # DESARROLLO DEL CONTENIDO
    # ==========================================

    # --- UNIDAD 1: INTRODUCCIÓN ---
    if st.session_state.paso_modulo4 == 1:
        st.title("MÓDULO 4: EL VEREDICTO DEL TRAZADOR")
        st.subheader("Más allá de la Tropopausa")
        st.markdown("""
        Hemos llegado a la pieza final del rompecabezas. 
        
        En los módulos anteriores vimos cómo el aire sube lentamente en los trópicos y cómo las tormentas violentas elevan el calor. También aprendimos que la lluvia empobrece el vapor de isótopos pesados (HDO).
        
        Pero quedó un misterio sin resolver en los datos satelitales. Es hora de descubrir cómo el agua sólida (hielo) cambia las reglas del juego y nos permite rastrear el origen del aire estratosférico.
        """)
        st.info("👇 Presiona **Siguiente** para investigar la anomalía.")

    # --- UNIDAD 1: LA ANOMALÍA ---
    elif st.session_state.paso_modulo4 == 2:
        st.header("1. Observemos el fenómeno")
        st.subheader("El misterio de los 16 kilómetros")
        col_txt, col_img = st.columns(2)
        with col_txt:
            st.markdown("""
            Recuerda la gráfica de datos satelitales ACE-FTS del módulo anterior.
            
            El Modelo de Destilación de Rayleigh nos dijo que, a medida que subimos, el HDO debería desaparecer casi por completo. Esto se cumple a la perfección... **hasta los 16 km** (la tropopausa).
            
            Sin embargo, por encima de esta altura, ¡la concentración de HDO vuelve a aumentar!
            **¿Cómo puede enriquecerse el aire si ya no le queda vapor pesado?**
            """)
        with col_img:
            try: st.image("assets/images/mod4_anomalia.png", caption="Anomalía de enriquecimiento isotópico >16km")
            except: st.warning("Falta imagen: mod4_anomalia.png")

    # --- UNIDAD 2: EL HIELO ---
    elif st.session_state.paso_modulo4 == 3:
        st.header("2. Expliquemos lo observado")
        st.subheader("Congelando la trampa de Rayleigh")
        st.markdown("La respuesta está en la **Convección Profunda** (la que vimos en el Módulo 2 con los Monzones).")
        
        col_txt, col_img = st.columns([1.5, 1])
        with col_txt:
            st.info("""
            **1. Ascenso Violento y Congelación Rápida:**
            En las tormentas tropicales más intensas, el aire sube tan rápido que el agua líquida no tiene tiempo de caer como lluvia. En su lugar, **se congela de golpe** formando cristales de hielo.
            
            Al congelarse, el proceso de fraccionamiento se detiene. El hielo "atrapa" una gran cantidad de HDO en su interior.
            
            **2. Perforando la Tropopausa (Overshooting):**
            La tormenta tiene tanta energía que rompe el límite de la tropopausa, inyectando esos cristales de hielo cargados de HDO directamente en la estratosfera seca.
            """)
        with col_img:
            try: st.image("assets/images/mod4_hielo_overshoot.png", caption="Inyección de hielo convectivo")
            except: st.warning("Falta imagen: mod4_hielo_overshoot.png")

    # --- UNIDAD 2: LA SUBLIMACIÓN ---
    elif st.session_state.paso_modulo4 == 4:
        st.header("2. Expliquemos lo observado")
        st.subheader("El retorno al estado gaseoso")
        col_txt, col_img = st.columns(2)
        with col_txt:
            st.markdown("""
            Una vez que los cristales de hielo de la tormenta son inyectados en la baja estratosfera, se encuentran en un ambiente extremadamente frío y seco.
            
            Aquí ocurre la **Sublimación**: los cristales de hielo pasan directamente de estado sólido a vapor.
            
            Al sublimarse, todo el HDO que estaba atrapado en el hielo se libera al ambiente. **¡Por esto la gráfica se mueve hacia la derecha y se enriquece!**
            """)
        with col_img:
            try: st.image("assets/images/mod4_sublimacion.png", caption="Sublimación en la baja estratosfera")
            except: st.warning("Falta imagen: mod4_sublimacion.png")

    # --- UNIDAD 3: EL TRAZADOR ---
    elif st.session_state.paso_modulo4 == 5:
        st.header("3. Entendiendo el fenómeno")
        st.subheader("El HDO como el Espía Definitivo 🕵️‍♂️")
        st.markdown("Gracias a este descubrimiento, la composición isotópica se convierte en nuestra mejor herramienta para rastrear cómo el vapor de agua llega a la estratosfera.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.success("""
            ### 🐢 Masa de Aire "Lenta"
            * **Origen:** Ascenso lento tropical (Circulación Brewer-Dobson).
            * **Proceso:** Destilación de Rayleigh perfecta.
            * **Huella Isotópica:** Vapor **MUY AGOTADO** (poco HDO).
            """)
        with col2:
            st.error("""
            ### 🚀 Masa de Aire "Rápida"
            * **Origen:** Convección Profunda (Tormentas/Monzones).
            * **Proceso:** Congelación rápida, inyección de hielo y sublimación.
            * **Huella Isotópica:** Vapor **ENRIQUECIDO** (mucho HDO).
            """)
        
        try: st.image("assets/images/mod4_resumen_trazador.png", use_container_width=True)
        except: st.empty()

    # --- UNIDAD 4: INTERACTIVO ---
    elif st.session_state.paso_modulo4 == 6:
        st.header("4. Hora de explorar")
        st.markdown("### El Laboratorio de Trazadores")
        st.markdown("Imagina que eres un físico atmosférico analizando masas de aire. Ajusta las condiciones de la atmósfera y observa la huella isotópica resultante en la baja estratosfera.")
        
        cargar_simulador_trazador()

        
    # --- UNIDAD 5: QUIZ ---
    elif st.session_state.paso_modulo4 == 7:
        st.header("5. Pon a prueba tu conocimiento")
        with st.form("quiz_m4"):
            q1 = st.radio("1. ¿Qué proceso físico 'detiene' el fraccionamiento de Rayleigh en las tormentas fuertes?", ["La ebullición", "La congelación rápida del agua en hielo", "La conducción de calor"], index=None)
            q2 = st.radio("2. ¿Cómo libera el hielo inyectado su HDO en la estratosfera?", ["Se derrite y llueve", "A través de la sublimación (de hielo a vapor)", "A través de la radiación"], index=None)
            q3 = st.radio("3. Si detectamos vapor de agua con mucho HDO (enriquecido) en la estratosfera, sabemos que el aire subió...", ["Muy lentamente", "A través de convección profunda rápida"], index=None)
            if st.form_submit_button("Enviar Respuestas"):
                pts = 0
                if q1 == "La congelación rápida del agua en hielo": pts += 1
                if q2 == "A través de la sublimación (de hielo a vapor)": pts += 1
                if q3 == "A través de convección profunda rápida": pts += 1
                st.session_state.resultados_quiz_m4 = {"Puntaje": pts}
                if pts == 3: st.balloons(); st.success("¡Excelente! Has dominado la dinámica isotópica.")
                else: st.warning(f"Puntaje: {pts}/3")

    # --- UNIDAD 6: ENCUESTA FINAL ---
    elif st.session_state.paso_modulo4 == 8:
        st.header("6. Encuesta de satisfacción")
        st.success("¡Felicidades! Has completado todos los módulos de MOVEA.")
        with st.form("encuesta_m4"):
            user = st.text_input("Nombre / Código")
            rating = st.slider("Valoración Global del Aplicativo MOVEA", 1, 5, 5)
            comments = st.text_area("Comentarios Finales y Sugerencias")
            if st.form_submit_button("Generar Certificado Final 💾"):
                if not user: st.error("Ingresa tu nombre para el certificado final.")
                else:
                    df = pd.DataFrame({"Estudiante": [user], "Módulo": ["4-Final"], "Valoración": [rating], "Comentarios": [comments]})
                    st.download_button("Descargar Certificado", df.to_csv(index=False).encode('utf-8'), f"Certificado_MOVEA_{user}.csv")

    # --- FOOTER ---
    st.divider()
    col_prev, col_next = st.columns([1, 1])
    with col_prev:
        if st.session_state.paso_modulo4 > 1: st.button("⬅️ Atrás", on_click=anterior, key="btn_atras_m4")
    with col_next:
        if st.session_state.paso_modulo4 < 8: st.button("Siguiente ➡️", on_click=siguiente, key="btn_sig_m4")