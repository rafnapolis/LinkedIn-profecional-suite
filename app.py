import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
import urllib.parse

# --- CONFIGURACIÓN DE IA ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    modelos_visibles = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    modelo_final = "models/gemini-1.5-flash" if "models/gemini-1.5-flash" in modelos_visibles else modelos_visibles[0]
    model = genai.GenerativeModel(modelo_final.replace("models/", ""))
except Exception as e:
    st.error("Error de configuración de IA.")

# --- ENLACES ---
URL_APP = "https://linkedin-profecional-suite-hybj2gli8cjvqbhtkwazq2.streamlit.app/"
MONETAG = st.secrets.get("MONETAG_LINK", "#")
MP_ARG = st.secrets.get("MP_LINK", "#")
KOFI_GLOBAL = st.secrets.get("KOFI_LINK", "#")

if 'pago_cv_verificado' not in st.session_state: st.session_state.pago_cv_verificado = False

st.set_page_config(page_title="LinkedIn Suite Pro", page_icon="💼")

def dibujar_boton(texto, link, color="#0077b5"):
    st.markdown(f'''<a href="{link}" target="_blank" style="text-decoration:none;"><div style="background-color:{color};color:white !important;padding:15px;text-align:center;border-radius:10px;font-weight:bold;margin:10px 0;font-size:16px;">{texto}</div></a>''', unsafe_allow_html=True)

st.title("Suite Profesional de LinkedIn 💼")
tabs = st.tabs(["✨ Humanizador", "👤 Perfil (Gratis)", "📄 Auditoría CV (Premium)"])

# --- TAB 1: HUMANIZADOR ---
with tabs[0]:
    t_post = st.text_area("Borrador del Post:", key="h_input")
    if t_post:
        if 'clic_monetag_h' not in st.session_state: st.session_state.clic_monetag_h = False
        if 'h_valido' not in st.session_state: st.session_state.h_valido = False

        if not st.session_state.clic_monetag_h:
            dibujar_boton("🚀 ACTIVAR IA (MONETAG)", MONETAG)
            if st.button("YA HICE CLIC", key="btn_h"):
                st.session_state.clic_monetag_h = True
                st.rerun()
        elif not st.session_state.h_valido:
            barra_h = st.progress(0)
            for i in range(1, 11):
                time.sleep(1); barra_h.progress(i * 10)
            st.session_state.h_valido = True
            st.rerun()
        else:
            if st.button("🚀 OPTIMIZAR"):
                res = model.generate_content(f"Humaniza este post de LinkedIn: {t_post}")
                st.write(res.text)

# --- TAB 2: PERFIL ---
with tabs[1]:
    f_p = st.file_uploader("Sube tu foto", type=["jpg", "png", "jpeg"], key="p_up")
    if f_p:
        if 'clic_p' not in st.session_state: st.session_state.clic_p = False
        if not st.session_state.clic_p:
            dibujar_boton("🚀 ACTIVAR ANÁLISIS (MONETAG)", MONETAG)
            if st.button("VALIDAR CLIC", key="btn_p"):
                st.session_state.clic_p = True
                st.rerun()
        else:
            if st.button("⚡ ANALIZAR"):
                res = model.generate_content(["Analiza esta foto de LinkedIn. Tips y Score.", Image.open(f_p)])
                st.write(res.text)

# --- TAB 3: AUDITORÍA CV (ERROR CORREGIDO AQUÍ) ---
with tabs[2]:
    st.header("🎯 Auditoría de CV (ATS)")
    f_cv = st.file_uploader("Sube tu CV (Imagen)", type=["jpg", "png", "jpeg"], key="cv_up")
    
    if f_cv:
        if st.button("🚀 DIAGNÓSTICO GRATUITO"):
            with st.spinner("Analizando..."):
                # CORRECCIÓN: Comillas simples triples cerradas correctamente
                prompt_cv = '''Analiza este CV. Formato:
                PARTE_GRATIS: Puntuación ATS (0-10) y 2 errores graves.
                PARTE_PREMIUM: Análisis detallado por sección y consejos pro.'''
                
                res = model.generate_content([prompt_cv, Image.open(f_cv)])
                partes = res.text.split("PARTE_PREMIUM:")
                st.session_state['cv_free'] = partes[0].replace("PARTE_GRATIS:", "")
                st.session_state['cv_premium'] = partes[1] if len(partes) > 1 else "Error al generar premium."

        if 'cv_free' in st.session_state:
            st.info(f"📊 Diagnóstico: {st.session_state['cv_free']}")
            
            if not st.session_state.pago_cv_verificado:
                col1, col2 = st.columns(2)
                with col1: dibujar_boton("Pagar $5.000 (ARG)", MP_ARG, "#009ee3")
                with col2: dibujar_boton("Pagar $5 USD (Global)", KOFI_GLOBAL, "#ff5e5b")
                
                f_pago = st.file_uploader("Sube captura del pago", type=["jpg", "png", "jpeg"])
                if f_pago and st.button("🔍 VALIDAR PAGO"):
                    v = model.generate_content(["¿Es un ticket de pago? Responde VALIDO o FALSO.", Image.open(f_pago)])
                    if "VALIDO" in v.text.upper():
                        st.session_state.pago_cv_verificado = True
                        st.rerun()
            else:
                st.success("🏆 Auditoría Completa")
                st.write(st.session_state['cv_premium'])
                st.download_button("📥 DESCARGAR (TXT)", st.session_state['cv_premium'], file_name="Auditoria.txt")
