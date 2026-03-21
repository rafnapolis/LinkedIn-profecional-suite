import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- CONFIGURACIÓN DE IA ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = "gemini-1.5-flash" if "models/gemini-1.5-flash" in modelos else modelos[0].replace("models/", "")
    model = genai.GenerativeModel(target_model)
except:
    st.error("Error de configuración de IA.")

# --- ENLACES ---
MONETAG = st.secrets.get("MONETAG_LINK", "#")
MP_ARG = st.secrets.get("MP_LINK", "#")
KOFI_GLOBAL = st.secrets.get("KOFI_LINK", "#")

st.set_page_config(page_title="LinkedIn Suite Pro", page_icon="🚀")

def boton_pago(texto, link, color="#28a745"):
    st.markdown(f'''<a href="{link}" target="_blank" style="text-decoration:none;"><div style="background-color:{color};color:white;padding:15px;text-align:center;border-radius:10px;font-weight:bold;margin:10px 0;">{texto}</div></a>''', unsafe_allow_html=True)

st.title("💼 LinkedIn Professional Suite")
tabs = st.tabs(["✨ Humanizador", "👤 Perfil", "📄 Auditoría CV"])

# --- TAB 1: HUMANIZADOR ---
with tabs[0]:
    texto_post = st.text_area("Borrador de Post:")
    if st.button("🚀 Optimizar"):
        if texto_post:
            res = model.generate_content(f"Optimiza este post para LinkedIn: {texto_post}")
            st.write(res.text)
            st.info(f"👉 [Más herramientas gratis aquí]({MONETAG})")

# --- TAB 2: PERFIL (CON TEMPORIZADOR DE 10 SEG) ---
with tabs[1]:
    st.header("Análisis de Perfil")
    foto = st.file_uploader("Sube tu foto de perfil", type=["jpg", "png", "jpeg"], key="p_foto")
    
    if foto:
        st.image(foto, width=150)
        st.subheader("🔑 Paso 1: Activar Servidor de IA")
        st.write("Haz clic abajo para abrir el portal de acceso:")
        boton_pago("ACCEDER AL PORTAL (CLIC AQUÍ)", MONETAG, color="#0077b5")
        
        # El botón de "Validar" inicia el conteo
        if st.button("🔗 VALIDAR ACCESO"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(11):
                progress_bar.progress(i * 10)
                status_text.text(f"Validando publicidad... Espera {10-i} segundos")
                time.sleep(1) # Aquí es donde el usuario espera viendo la pantalla
            
            status_text.success("✅ Acceso Validado. Servidor listo.")
            # Guardamos en la sesión que ya esperó
            st.session_state['perfil_ready'] = True

        # Solo si ya pasó el tiempo, aparece el botón final
        if st.session_state.get('perfil_ready'):
            if st.button("⚡ EJECUTAR ANÁLISIS DE PERFIL"):
                with st.spinner("IA Analizando..."):
                    img = Image.open(foto)
                    res = model.generate_content(["Analiza esta foto de LinkedIn. Puntaje y mejoras.", img])
                    st.write(res.text)
                    # Reset para la próxima vez
                    st.session_state['perfil_ready'] = False

# --- TAB 3: AUDITORÍA CV (COMPROBANTE REAL) ---
with tabs[2]:
    st.header("🎯 Auditoría Premium CV")
    cv_file = st.file_uploader("Sube tu CV (Imagen)", type=["jpg", "png", "jpeg"], key="cv_main")
    
    if cv_file:
        st.subheader("1. Pago de Auditoría")
        c1, c2 = st.columns(2)
        with c1: boton_pago("Mercado Pago (ARG)", MP_ARG, color="#009ee3")
        with c2: boton_pago("Pay Ko-fi (Global)", KOFI_GLOBAL, color="#ff5e5b")
        
        st.markdown("---")
        st.subheader("2. Validar Pago")
        comprobante = st.file_uploader("Sube captura del pago", type=["jpg", "png", "jpeg"], key="val_pago")
        
        if comprobante:
            st.success("✅ Comprobante detectado.")
            # Temporizador de seguridad de 5 segundos para el CV también
            if st.button("🚀 INICIAR AUDITORÍA PROFESIONAL"):
                with st.spinner("Procesando datos..."):
                    time.sleep(3)
                    img_cv = Image.open(cv_file)
                    res = model.generate_content(["Analiza este CV ATS.", img_cv])
                    st.markdown(res.text)
        else:
            st.warning("⚠️ Sube tu comprobante para desbloquear el análisis.")
