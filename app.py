import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# --- CONFIGURACIÓN DE IA DINÁMICA ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    if "models/gemini-1.5-flash" in modelos:
        target_model = "gemini-1.5-flash"
    elif "models/gemini-1.5-pro" in modelos:
        target_model = "gemini-1.5-pro"
    else:
        target_model = modelos[0].replace("models/", "")
        
    model = genai.GenerativeModel(target_model)
except Exception as e:
    st.error("Error de configuración de IA. Revisa las Secrets.")

# --- ENLACES DE MONETIZACIÓN ---
MONETAG = st.secrets.get("MONETAG_LINK", "#")
MP_ARG = st.secrets.get("MP_LINK", "#")
KOFI_GLOBAL = st.secrets.get("KOFI_LINK", "#")

# --- INTERFAZ ---
st.set_page_config(page_title="LinkedIn Suite Pro", page_icon="🚀")

def boton_pago(texto, link, color="#28a745"):
    st.markdown(f'''
        <a href="{link}" target="_blank" style="text-decoration: none;">
            <div style="background-color: {color}; color: white; padding: 15px; text-align: center; border-radius: 10px; font-weight: bold; margin: 10px 0;">
                {texto}
            </div>
        </a>
    ''', unsafe_allow_html=True)

st.title("💼 LinkedIn Professional Suite")
tabs = st.tabs(["✨ Humanizador", "👤 Auditor de Perfil", "📄 Auditor de CV"])

# --- TAB 1: HUMANIZADOR (Monetización DirectLink) ---
with tabs[0]:
    st.header("Humanizador de Posts")
    texto_post = st.text_area("Pega tu borrador:")
    if st.button("🚀 Optimizar Post"):
        if texto_post:
            with st.spinner("Optimizando..."):
                res = model.generate_content(f"Optimiza este post para LinkedIn con ganchos virales: {texto_post}")
                st.markdown(res.text)
                st.info(f"👉 [Descarga más plantillas virales aquí]({MONETAG})")

# --- TAB 2: AUDITOR DE PERFIL (Protección por Clic) ---
with tabs[1]:
    st.header("Auditoría de Perfil")
    foto = st.file_uploader("Sube tu foto de perfil", type=["jpg", "png", "jpeg"], key="perfil")
    if foto:
        st.image(foto, width=150)
        st.markdown("### 🔑 Acceso")
        st.write("Haz clic abajo para generar tu código de acceso gratuito:")
        boton_pago("GENERAR CLAVE DE ACCESO", MONETAG, color="#0077b5")
        
        acceso_confirmado = st.checkbox("He generado mi clave de acceso")
        
        if st.button("⚡ ANALIZAR PERFIL"):
            if acceso_confirmado:
                with st.spinner("Analizando..."):
                    img = Image.open(foto)
                    res = model.generate_content(["Analiza esta foto de perfil profesional. Da puntaje del 1 al 10 y consejos.", img])
                    st.markdown(res.text)
            else:
                st.error("Por favor, genera tu clave en el botón azul primero.")

# --- TAB 3: AUDITOR DE CV (Protección por Comprobante) ---
with tabs[2]:
    st.header("Auditoría de CV Premium")
    cv_file = st.file_uploader("Sube tu CV (Imagen)", type=["jpg", "png", "jpeg"], key="cv")
    
    if cv_file:
        st.markdown("### 💳 Paso 1: Pago de Auditoría")
        c1, c2 = st.columns(2)
        with c1: boton_pago("Pagar Mercado Pago (ARG)", MP_ARG, color="#009ee3")
        with c2: boton_pago("Pay Ko-fi (Global)", KOFI_GLOBAL, color="#ff5e5b")
        
        st.markdown("---")
        st.markdown("### 🔐 Paso 2: Validación de Pago")
        comprobante = st.text_input("Ingresa el número de operación o ID de transacción:")
        confirmacion_pago = st.checkbox("Confirmo que he realizado el pago correctamente")

        if st.button("🚀 INICIAR AUDITORÍA PROFESIONAL"):
            if confirmacion_pago and len(comprobante) > 4:
                with st.spinner("Análisis ATS en curso..."):
                    img_cv = Image.open(cv_file)
                    res = model.generate_content(["Analiza este CV como reclutador experto. Busca errores ATS y palabras clave.", img_cv])
                    st.success(f"Análisis para transacción {comprobante}:")
                    st.markdown(res.text)
            else:
                st.error("Debes ingresar un ID de transacción válido y confirmar el pago para continuar.")
    
