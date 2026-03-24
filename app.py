import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
import urllib.parse

# --- CONFIGURACIÓN DE IA BLINDADA ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Buscamos modelos disponibles para evitar el error 404
    modelos_visibles = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # Prioridad: 1.5-flash, si no, el primero que funcione
    modelo_final = "models/gemini-1.5-flash" if "models/gemini-1.5-flash" in modelos_visibles else modelos_visibles[0]
    model = genai.GenerativeModel(modelo_final.replace("models/", ""))
except Exception as e:
    st.error("Error crítico de conexión. Revisa tu API KEY en Secrets.")

# --- ENLACES ---
URL_APP = "https://linkedin-profecional-suite-hybj2gli8cjvqbhtkwazq2.streamlit.app/"
MONETAG = st.secrets.get("MONETAG_LINK", "#")
MP_ARG = st.secrets.get("MP_LINK", "#")
KOFI_GLOBAL = st.secrets.get("KOFI_LINK", "#")

# --- ESTADOS ---
if 'clic_monetag' not in st.session_state: st.session_state.clic_monetag = False
if 'perfil_valido' not in st.session_state: st.session_state.perfil_valido = False
if 'pago_cv_verificado' not in st.session_state: st.session_state.pago_cv_verificado = False

st.set_page_config(page_title="LinkedIn Suite Pro", page_icon="🚀")

def dibujar_boton(texto, link, color="#28a745"):
    st.markdown(f'''<a href="{link}" target="_blank" style="text-decoration:none;"><div style="background-color:{color};color:white !important;padding:18px;text-align:center;border-radius:12px;font-weight:800;margin:10px 0;font-size:18px;text-shadow:1px 1px 2px rgba(0,0,0,0.5);border:1px solid rgba(255,255,255,0.2);">{texto}</div></a>''', unsafe_allow_html=True)

st.title("💼 LinkedIn Professional Suite")
tabs = st.tabs(["✨ Humanizador", "👤 Perfil (Gratis)", "📄 Auditoría CV (Premium)"])

# --- TAB 1: HUMANIZADOR ---
with tabs[0]:
    t_post = st.text_area("Borrador del Post:")
    if st.button("🚀 OPTIMIZAR"):
        if t_post:
            res = model.generate_content(f"Mejora este post para LinkedIn: {t_post}")
            st.write(res.text)

# --- TAB 2: PERFIL (FLUJO SEGURO) ---
with tabs[1]:
    st.header("👤 Análisis de Perfil")
    f_p = st.file_uploader("Sube tu foto", type=["jpg", "png", "jpeg"], key="p_up")
    
    if f_p:
        st.image(f_p, width=150)
        
        if not st.session_state.clic_monetag:
            st.info("🎯 Haz clic para activar la IA.")
            dibujar_boton("🚀 CLIC AQUÍ: ACTIVAR IA (MONETAG)", MONETAG, color="#0077b5")
            if st.button("YA HICE CLIC"):
                st.session_state.clic_monetag = True
                st.rerun()

        elif st.session_state.clic_monetag and not st.session_state.perfil_valido:
            barra = st.progress(0)
            for i in range(11):
                barra.progress(i * 10)
                time.sleep(1)
            st.session_state.perfil_valido = True
            st.rerun()

        elif st.session_state.perfil_valido:
            if st.button("⚡ EJECUTAR ANÁLISIS"):
                img = Image.open(f_p)
                res = model.generate_content(["Analiza esta foto de LinkedIn. Puntuación: X/10.", img])
                st.session_state['res_perfil'] = res.text
            
            if 'res_perfil' in st.session_state:
                st.write(st.session_state['res_perfil'])
                msg = f"🚀 ¡Mi perfil fue auditado por IA! Prueba el tuyo gratis: {URL_APP}"
                url_share = f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(URL_APP)}"
                st.code(msg)
                dibujar_boton("📲 COMPARTIR EN LINKEDIN", url_share, color="#0077b5")

# --- TAB 3: CV (CAJERO VIRTUAL) ---
with tabs[2]:
    st.header("🎯 Auditoría Premium CV")
    f_cv = st.file_uploader("Sube tu CV (Imagen)", type=["jpg", "png", "jpeg"], key="cv_up")
    if f_cv:
        dibujar_boton("Mercado Pago (ARG)", MP_ARG, color="#009ee3")
        f_pago = st.file_uploader("Sube captura del pago", type=["jpg", "png", "jpeg"])
        if f_pago and st.button("🔍 VERIFICAR PAGO"):
            v_res = model.generate_content(["Responde VALIDO si es un ticket de pago, sino FALSO.", Image.open(f_pago)])
            if "VALIDO" in v_res.text.upper():
                st.session_state.pago_cv_verificado = True
                st.success("✅ Pago confirmado.")
            else: st.error("❌ Ticket no válido.")

        if st.session_state.pago_cv_verificado:
            if st.button("🚀 INICIAR AUDITORÍA"):
                res = model.generate_content(["Analiza este CV para ATS.", Image.open(f_cv)])
                st.markdown(res.text)
