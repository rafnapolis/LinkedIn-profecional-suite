import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
import urllib.parse

# --- CONFIGURACIÓN DE IA (GOOGLE GEMINI) ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    modelos_visibles = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    modelo_final = "models/gemini-1.5-flash" if "models/gemini-1.5-flash" in modelos_visibles else modelos_visibles[0]
    model = genai.GenerativeModel(modelo_final.replace("models/", ""))
except Exception as e:
    st.error("Error de configuración de IA. Verifica tu API KEY en Secrets.")

# --- ENLACES CONFIGURABLES ---
URL_APP = "https://linkedin-profecional-suite-hybj2gli8cjvqbhtkwazq2.streamlit.app/"
MONETAG = st.secrets.get("MONETAG_LINK", "#")
MP_ARG = st.secrets.get("MP_LINK", "#")
KOFI_GLOBAL = st.secrets.get("KOFI_LINK", "#")

# --- ESTADOS DE SESIÓN GLOBALES ---
if 'pago_cv_verificado' not in st.session_state: st.session_state.pago_cv_verificado = False

st.set_page_config(page_title="LinkedIn Suite Pro", page_icon="💼", layout="centered")

# --- FUNCIÓN PARA BOTONES ESTILIZADOS ---
def dibujar_boton(texto, link, color="#0077b5"):
    st.markdown(f'''
        <a href="{link}" target="_blank" style="text-decoration:none;">
            <div style="background-color:{color};color:white !important;padding:15px;text-align:center;border-radius:10px;font-weight:bold;margin:10px 0;font-size:16px;box-shadow: 0px 4px 6px rgba(0,0,0,0.1);">
                {texto}
            </div>
        </a>
    ''', unsafe_allow_html=True)

st.title("Suite Profesional de LinkedIn 💼")
st.markdown("---")

tabs = st.tabs(["✨ Humanizador", "👤 Perfil (Gratis)", "📄 Auditoría CV (Premium)"])

# --- TAB 1: HUMANIZADOR (CON MONETAG) ---
with tabs[0]:
    st.subheader("✨ Humanizador de Posts")
    t_post = st.text_area("Borrador del Post:", placeholder="Escribe aquí tu idea para LinkedIn...", key="h_input")
    
    if t_post:
        if 'clic_monetag_h' not in st.session_state: st.session_state.clic_monetag_h = False
        if 'h_valido' not in st.session_state: st.session_state.h_valido = False

        if not st.session_state.clic_monetag_h:
            st.info("Para activar el Humanizador, haz clic abajo (Apoya la herramienta gratuita).")
            dibujar_boton("🚀 CLIC AQUÍ: ACTIVAR IA (MONETAG)", MONETAG, color="#0077b5")
            if st.button("YA HICE CLIC (DESBLOQUEAR)", key="btn_h"):
                st.session_state.clic_monetag_h = True
                st.rerun()
        
        elif st.session_state.clic_monetag_h and not st.session_state.h_valido:
            with st.status("Validando acceso...", expanded=True) as s:
                barra_h = st.progress(0)
                for i in range(1, 11):
                    time.sleep(1)
                    barra_h.progress(i * 10)
                st.session_state.h_valido = True
                s.update(label="✅ IA Lista", state="complete")
                st.rerun()
        
        elif st.session_state.h_valido:
            if st.button("🚀 OPTIMIZAR AHORA", key="exec_h"):
                with st.spinner("Humanizando..."):
                    res = model.generate_content(f"Humaniza este post para LinkedIn, hazlo viral y auténtico: {t_post}")
                    st.session_state['res_h'] = res.text
            
            if 'res_h' in st.session_state:
                st.markdown("### ✨ Resultado:")
                st.write(st.session_state['res_h'])

# --- TAB 2: PERFIL (CON MONETAG) ---
with tabs[1]:
    st.header("👤 Análisis de Foto de Perfil")
    f_p = st.file_uploader("Sube tu foto", type=["jpg", "png", "jpeg"], key="p_up")
    
    if f_p:
        st.image(f_p, width=150)
        if 'clic_monetag_p' not in st.session_state: st.session_state.clic_monetag_p = False
        if 'p_valido' not in st.session_state: st.session_state.p_valido = False

        if not st.session_state.clic_monetag_p:
            dibujar_boton("🚀 CLIC AQUÍ: ACTIVAR ANÁLISIS (MONETAG)", MONETAG, color="#0077b5")
            if st.button("YA HICE CLIC", key="btn_p"):
                st.session_state.clic_monetag_p = True
                st.rerun()
        
        elif st.session_state.clic_monetag_p and not st.session_state.p_valido:
            barra_p = st.progress(0)
            for i in range(1, 11):
                time.sleep(1)
                barra_p.progress(i * 10)
            st.session_state.p_valido = True
            st.rerun()
        
        elif st.session_state.p_valido:
            if st.button("⚡ ANALIZAR FOTO", key="exec_p"):
                res = model.generate_content(["Analiza esta foto de LinkedIn. Puntuación X/10 y 3 tips.", Image.open(f_p)])
                st.session_state['res_p'] = res.text
            if 'res_p' in st.session_state:
                st.write(st.session_state['res_p'])

# --- TAB 3: AUDITORÍA CV (PREMIUM AGRESIVO) ---
with tabs[2]:
    st.header("🎯 Auditoría de CV (ATS)")
    st.write("Sube tu CV para un diagnóstico inmediato.")
    f_cv = st.file_uploader("Sube tu CV (Imagen)", type=["jpg", "png", "jpeg"], key="cv_up")
    
    if f_cv:
        if st.button("🚀 OBTENER DIAGNÓSTICO GRATUITO"):
            with st.spinner("Analizando..."):
                prompt_cv = """Analiza este CV. Formato:
                PARTE_GRATIS: Puntuación ATS
