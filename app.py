import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
import urllib.parse

# --- CONFIGURACIÓN DE IA ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = "gemini-1.5-flash" if "models/gemini-1.5-flash" in modelos else modelos[0].replace("models/", "")
    model = genai.GenerativeModel(target_model)
except:
    st.error("Error de configuración de IA. Revisa tus Secrets.")

# --- ENLACES ---
MONETAG = st.secrets.get("MONETAG_LINK", "#")
MP_ARG = st.secrets.get("MP_LINK", "#")
KOFI_GLOBAL = st.secrets.get("KOFI_LINK", "#")
URL_APP = "TU_URL_DE_STREAMLIT_AQUI" # Reemplaza con tu link real

# --- ESTADOS DE SESIÓN ---
if 'clic_monetag' not in st.session_state: st.session_state.clic_monetag = False
if 'perfil_valido' not in st.session_state: st.session_state.perfil_valido = False
if 'pago_cv_verificado' not in st.session_state: st.session_state.pago_cv_verificado = False

st.set_page_config(page_title="LinkedIn Suite Pro", page_icon="🚀")

def dibujar_boton(texto, link, color="#28a745"):
    st.markdown(f'''<a href="{link}" target="_blank" style="text-decoration:none;"><div style="background-color:{color};color:white;padding:18px;text-align:center;border-radius:12px;font-weight:bold;margin:10px 0;font-size:18px;box-shadow:0px 4px 10px rgba(0,0,0,0.1);">{texto}</div></a>''', unsafe_allow_html=True)

st.title("💼 LinkedIn Professional Suite")
tabs = st.tabs(["✨ Humanizador", "👤 Perfil (Gratis)", "📄 Auditoría CV (Premium)"])

# --- TAB 1: HUMANIZADOR ---
with tabs[0]:
    t_post = st.text_area("Borrador de Post:")
    if st.button("🚀 Optimizar Post"):
        if t_post:
            res = model.generate_content(f"Optimiza este post para LinkedIn: {t_post}")
            st.write(res.text)
            st.info(f"👉 [Más herramientas gratis aquí]({MONETAG})")

# --- TAB 2: PERFIL (CON FUNCIÓN COMPARTIR) ---
with tabs[1]:
    st.header("Análisis de Perfil")
    f_p = st.file_uploader("Sube tu foto", type=["jpg", "png", "jpeg"], key="p_up")
    if f_p:
        st.image(f_p, width=150)
        dibujar_boton("🚀 CLIC AQUÍ: ACTIVAR IA (MONETAG)", MONETAG, color="#0077b5")
        
        if st.button("YA HICE CLIC (DESBLOQUEAR SIGUIENTE PASO)"):
            st.session_state.clic_monetag = True
        
        if st.session_state.clic_monetag:
            if st.button("🔗 INICIAR VALIDACIÓN DE 10 SEG"):
                barra = st.progress(0)
                for i in range(11):
                    barra.progress(i * 10)
                    time.sleep(1)
                st.session_state.perfil_valido = True
                st.success("✅ Acceso Validado.")

        if st.session_state.perfil_valido:
            if st.button("⚡ EJECUTAR ANÁLISIS"):
                with st.spinner("IA Analizando..."):
                    img = Image.open(f_p)
                    # Forzamos a la IA a dar una puntuación numérica clara
                    prompt = "Analiza esta foto de LinkedIn. 1. Dame una puntuación del 1 al 10 en una sola línea que diga 'PUNTUACIÓN: X/10'. 2. Da 3 consejos breves."
                    res = model.generate_content([prompt, img])
                    st.session_state['resultado_ia'] = res.text
                    st.write(res.text)

            # BOTÓN PARA COMPARTIR EN LINKEDIN
            if 'resultado_ia' in st.session_state:
                st.markdown("---")
                st.subheader("📢 ¡Comparte tu resultado!")
                
                # Extraemos la puntuación para el mensaje social
                msg = f"🚀 Acabo de auditar mi perfil de LinkedIn con IA y obtuve un gran resultado. ¡Prueba tu puntuación gratis aquí! {URL_APP}"
                msg_encoded = urllib.parse.quote(msg)
                share_url = f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(URL_APP)}&text={msg_encoded}"
                
                st.code(msg, language="text") # Para que lo copien fácil
                dibujar_boton("📲 COMPARTIR EN MI LINKEDIN", share_url, color="#0077b5")

# --- TAB 3: CV (CAJERO VIRTUAL IA) ---
with tabs[2]:
    st.header("🎯 Auditoría Premium CV")
    f_cv = st.file_uploader("Sube tu CV (Imagen)", type=["jpg", "png", "jpeg"], key="cv_up")
    if f_cv:
        st.subheader("2. Realiza el Pago")
        c1, c2 = st.columns(2)
        with c1: dibujar_boton("Mercado Pago (ARG)", MP_ARG, color="#009ee3")
        with c2: dibujar_boton("Ko-fi (Global)", KOFI_GLOBAL, color="#ff5e5b")
        
        st.subheader("3. Validación de Comprobante")
        f_pago = st.file_uploader("Sube captura del pago", type=["jpg", "png", "jpeg"], key="p_ia")
        if f_pago:
            if st.button("🔍 VERIFICAR PAGO CON IA"):
                with st.spinner("Verificando..."):
                    v_res = model.generate_content(["Responde VALIDO si es un comprobante de pago real, sino FALSO.", Image.open(f_pago)])
                    if "VALIDO" in v_res.text.upper():
                        st.session_state.pago_cv_verificado = True
                        st.success("✅ Pago confirmado.")
                    else: st.error("❌ Comprobante no válido.")

            if st.session_state.pago_cv_verificado:
                if st.button("🚀 INICIAR AUDITORÍA"):
                    res = model.generate_content(["Analiza este CV para ATS.", Image.open(f_cv)])
                    st.markdown(res.text)
                    st.balloons()
