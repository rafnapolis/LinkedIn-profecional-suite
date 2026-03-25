import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
import urllib.parse

# --- CONFIGURACIÓN DE IA BLINDADA ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    modelos_visibles = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    modelo_final = "models/gemini-1.5-flash" if "models/gemini-1.5-flash" in modelos_visibles else modelos_visibles[0]
    model = genai.GenerativeModel(modelo_final.replace("models/", ""))
except Exception as e:
    st.error("Error de conexión. Revisa tu API KEY.")

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
                res = model.generate_content(["Analiza esta foto de LinkedIn. Puntuación: X/10.", Image.open(f_p)])
                st.session_state['res_perfil'] = res.text
            if 'res_perfil' in st.session_state:
                st.write(st.session_state['res_perfil'])
                url_share = f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(URL_APP)}"
                dibujar_boton("📲 COMPARTIR EN LINKEDIN", url_share, color="#0077b5")

# --- TAB 3: CV (CON BOTÓN DE DESCARGA) ---
with tabs[2]:
    st.header("🎯 Auditoría Premium CV")
    f_cv = st.file_uploader("1. Sube tu CV (Imagen)", type=["jpg", "png", "jpeg"], key="cv_up")
    if f_cv:
        st.subheader("2. Realiza el Pago")
        c1, c2 = st.columns(2)
        with c1: dibujar_boton("Mercado Pago (ARG)", MP_ARG, color="#009ee3")
        with c2: dibujar_boton("Ko-fi (Global)", KOFI_GLOBAL, color="#ff5e5b")
        f_pago = st.file_uploader("3. Sube captura del pago", type=["jpg", "png", "jpeg"])
        
        if f_pago and st.button("🔍 VERIFICAR PAGO"):
            with st.spinner("Verificando..."):
                v_res = model.generate_content(["Responde VALIDO si es un ticket de pago, sino FALSO.", Image.open(f_pago)])
                if "VALIDO" in v_res.text.upper():
                    st.session_state.pago_cv_verificado = True
                    st.success("✅ Pago confirmado.")
                else: st.error("❌ Ticket no válido.")

        if st.session_state.pago_cv_verificado:
            if st.button("🚀 INICIAR AUDITORÍA"):
                with st.spinner("Analizando CV..."):
                    res = model.generate_content(["Analiza este CV para filtros ATS. Sé muy detallado.", Image.open(f_cv)])
                    st.session_state['res_cv'] = res.text
            
            if 'res_cv' in st.session_state:
                st.markdown("### 📋 Tu Informe de Auditoría:")
                st.markdown(st.session_state['res_cv'])
                
                # --- BOTÓN DE DESCARGA ---
                st.download_button(
                    label="📥 DESCARGAR AUDITORÍA (TXT)",
                    data=st.session_state['res_cv'],
                    file_name="Auditoria_LinkedIn_Suite.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                st.balloons()
