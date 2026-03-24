import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
import urllib.parse

# --- CONFIGURACIÓN DE IA ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error("Error de configuración de IA. Revisa tus Secrets.")

# --- ENLACES Y URL REAL ---
# IMPORTANTE: Reemplaza con tu URL real si cambia
URL_APP = "https://linkedin-profecional-suite-hybj2gli8cjvqbhtkwazq2.streamlit.app/"
MONETAG = st.secrets.get("MONETAG_LINK", "#")
MP_ARG = st.secrets.get("MP_LINK", "#")
KOFI_GLOBAL = st.secrets.get("KOFI_LINK", "#")

# --- ESTADOS DE SESIÓN ---
if 'clic_monetag' not in st.session_state: st.session_state.clic_monetag = False
if 'perfil_valido' not in st.session_state: st.session_state.perfil_valido = False
if 'pago_cv_verificado' not in st.session_state: st.session_state.pago_cv_verificado = False

st.set_page_config(page_title="LinkedIn Suite Pro", page_icon="🚀", layout="centered")

# --- FUNCIÓN DE BOTÓN BLINDADO (PARA QUE NO SE BORREN LAS LETRAS) ---
def dibujar_boton(texto, link, color="#28a745"):
    st.markdown(f'''
        <a href="{link}" target="_blank" style="text-decoration: none;">
            <div style="
                background-color: {color}; 
                color: #FFFFFF !important; 
                padding: 18px; 
                text-align: center; 
                border-radius: 12px; 
                font-weight: 800; 
                margin: 10px 0; 
                font-size: 18px; 
                text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
                display: block;
                width: 100%;
                border: 1px solid rgba(255,255,255,0.2);
            ">
                {texto}
            </div>
        </a>
    ''', unsafe_allow_html=True)

st.title("💼 LinkedIn Professional Suite")
tabs = st.tabs(["✨ Humanizador", "👤 Perfil (Gratis)", "📄 Auditoría CV (Premium)"])

# --- TAB 1: HUMANIZADOR ---
with tabs[0]:
    st.header("Optimizar Post")
    t_post = st.text_area("Pega tu borrador aquí:", placeholder="Escribe algo...")
    if st.button("🚀 HUMANIZAR AHORA"):
        if t_post:
            with st.spinner("Transformando..."):
                res = model.generate_content(f"Reescribe este post para LinkedIn para que sea viral, humano y use ganchos: {t_post}")
                st.write(res.text)
                st.info(f"👉 [Descubre más herramientas aquí]({MONETAG})")

# --- TAB 2: AUDITORÍA DE PERFIL (VIRAL) ---
with tabs[1]:
    st.header("👤 Análisis de Imagen Profesional")
    f_p = st.file_uploader("Sube tu foto de perfil", type=["jpg", "png", "jpeg"], key="p_up")
    
    if f_p:
        st.image(f_p, width=150)
        
        if not st.session_state.clic_monetag:
            st.warning("🔑 Paso 1: Activa la IA gratuita haciendo clic abajo.")
            dibujar_boton("🚀 CLIC AQUÍ: ACTIVAR IA (MONETAG)", MONETAG, color="#0077b5")
            if st.button("YA HICE CLIC (INICIAR VALIDACIÓN)"):
                st.session_state.clic_monetag = True
                st.rerun()

        elif st.session_state.clic_monetag and not st.session_state.perfil_valido:
            st.info("⏳ Validando publicidad... Espera 10 segundos.")
            barra = st.progress(0)
            for i in range(11):
                barra.progress(i * 10)
                time.sleep(1)
            st.session_state.perfil_valido = True
            st.success("✅ ¡Acceso Validado!")
            st.rerun()

        elif st.session_state.perfil_valido:
            if st.button("⚡ OBTENER MI PUNTUACIÓN"):
                with st.spinner("Analizando tu perfil..."):
                    img = Image.open(f_p)
                    prompt = "Analiza esta foto para LinkedIn. 1. Dame una puntuación del 1 al 10: 'PUNTUACIÓN IA: X/10'. 2. Da 2 consejos breves."
                    res = model.generate_content([prompt, img])
                    st.session_state['res_perfil'] = res.text
            
            if 'res_perfil' in st.session_state:
                st.markdown(f"### 📊 Resultado:\n{st.session_state['res_perfil']}")
                
                # --- BOTÓN VIRAL ---
                msg = f"🚀 Mi perfil de LinkedIn obtuvo un gran puntaje con esta IA. ¡Prueba el tuyo gratis! {URL_APP}"
                url_share = f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(URL_APP)}"
                st.code(msg)
                dibujar_boton("📲 COMPARTIR PUNTAJE EN LINKEDIN", url_share, color="#0077b5")
                
                if st.button("🔄 Analizar otra foto"):
                    st.session_state.clic_monetag = False
                    st.session_state.perfil_valido = False
                    del st.session_state['res_perfil']
                    st.rerun()

# --- TAB 3: AUDITORÍA CV (CAJERO VIRTUAL) ---
with tabs[2]:
    st.header("🎯 Auditoría Premium CV")
    f_cv = st.file_uploader("1. Sube tu CV (Imagen)", type=["jpg", "png", "jpeg"], key="cv_up")
    
    if f_cv:
        st.subheader("2. Realiza el Pago")
        c1, c2 = st.columns(2)
        with c1: dibujar_boton("Mercado Pago (ARG)", MP_ARG, color="#009ee3")
        with c2: dibujar_boton("Ko-fi (Global)", KOFI_GLOBAL, color="#ff5e5b")
        
        st.markdown("---")
        st.subheader("3. Validación de Comprobante")
        f_pago = st.file_uploader("Sube captura del pago", type=["jpg", "png", "jpeg"], key="p_ia")
        
        if f_pago:
            if st.button("🔍 VERIFICAR PAGO CON IA"):
                with st.spinner("Nuestra IA está verificando el ticket..."):
                    img_ticket = Image.open(f_pago)
                    v_res = model.generate_content(["Responde solo VALIDO si esta imagen es un comprobante de pago real, sino responde FALSO.", img_ticket])
                    
                    if "VALIDO" in v_res.text.upper():
                        st.session_state.pago_cv_verificado = True
                        st.success("✅ ¡Pago confirmado!")
                    else:
                        st.error("❌ Imagen no válida. Sube un comprobante real.")

            if st.session_state.pago_cv_verificado:
                if st.button("🚀 INICIAR AUDITORÍA PROFESIONAL"):
                    with st.spinner("Analizando CV..."):
                        res = model.generate_content(["Analiza este CV profesionalmente para filtros ATS.", Image.open(f_cv)])
                        st.markdown(res.text)
                        st.balloons()
                        st.session_state.pago_cv_verificado = False
