import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIGURACIÓN DE IA DINÁMICA ---
# Detecta automáticamente el mejor modelo disponible para evitar errores 404
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = "gemini-1.5-flash" if "models/gemini-1.5-flash" in modelos else modelos[0].replace("models/", "")
    model = genai.GenerativeModel(target_model)
except Exception as e:
    st.error("Error de configuración de IA. Revisa las Secrets en Streamlit.")

# --- ENLACES DE MONETIZACIÓN ---
# Asegúrate de tener estos nombres exactos en tus Secrets de Streamlit
MONETAG = st.secrets.get("MONETAG_LINK", "#")
MP_ARG = st.secrets.get("MP_LINK", "#")
KOFI_GLOBAL = st.secrets.get("KOFI_LINK", "#")

# --- INTERFAZ ---
st.set_page_config(page_title="LinkedIn Professional Suite", page_icon="🚀", layout="centered")

def boton_pago(texto, link, color="#28a745"):
    st.markdown(f'''
        <a href="{link}" target="_blank" style="text-decoration: none;">
            <div style="background-color: {color}; color: white; padding: 15px; text-align: center; border-radius: 10px; font-weight: bold; margin: 10px 0; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
                {texto}
            </div>
        </a>
    ''', unsafe_allow_html=True)

st.title("💼 LinkedIn Professional Suite")
st.markdown("---")

tabs = st.tabs(["✨ Humanizador", "👤 Perfil", "📄 Auditoría CV"])

# --- TAB 1: HUMANIZADOR (Tráfico y Monetag) ---
with tabs[0]:
    st.header("Humanizador de Posts")
    st.write("Transforma ideas simples en posts virales para LinkedIn.")
    texto_post = st.text_area("Pega tu borrador aquí:", height=150)
    
    if st.button("🚀 Optimizar Post"):
        if texto_post:
            with st.spinner("La IA está trabajando..."):
                res = model.generate_content(f"Actúa como experto en LinkedIn. Optimiza este post con ganchos y estructura humana: {texto_post}")
                st.markdown("### ✅ Propuesta de Post:")
                st.write(res.text)
                st.info(f"👉 [¿Quieres más herramientas de crecimiento? Clic aquí]({MONETAG})")
        else:
            st.warning("Escribe algo antes de optimizar.")

# --- TAB 2: PERFIL (Validación por Clic) ---
with tabs[1]:
    st.header("Análisis de Foto de Perfil")
    st.write("Análisis visual de impacto para tu marca personal.")
    foto = st.file_uploader("Sube tu foto actual", type=["jpg", "png", "jpeg"], key="p_foto")
    
    if foto:
        st.image(foto, width=150)
        st.subheader("🔑 Obtener acceso")
        st.write("Haz clic abajo para generar tu clave gratuita de auditoría:")
        boton_pago("GENERAR CLAVE DE ACCESO", MONETAG, color="#0077b5")
        
        check_acceso = st.checkbox("Ya hice clic y generé mi clave")
        
        if st.button("⚡ VER MI PUNTAJE DE IA"):
            if check_acceso:
                with st.spinner("Analizando imagen..."):
                    img = Image.open(foto)
                    res = model.generate_content(["Evalúa esta foto de perfil. Da un puntaje del 1 al 10 y 3 consejos de vestimenta, fondo y expresión.", img])
                    st.success("Análisis completado:")
                    st.markdown(res.text)
            else:
                st.error("Por favor, genera tu clave primero usando el botón azul.")

# --- TAB 3: AUDITORÍA CV (PROTECCIÓN TOTAL POR COMPROBANTE) ---
with tabs[2]:
    st.header("🎯 Auditoría Premium de CV")
    st.write("Sube tu CV para un análisis estratégico de filtros ATS.")
    
    cv_file = st.file_uploader("1. Sube tu CV (Captura o Imagen)", type=["jpg", "png", "jpeg"], key="cv_main")
    
    if cv_file:
        st.markdown("---")
        st.subheader("2. Realiza el Pago")
        c1, c2 = st.columns(2)
        with c1: 
            st.write("**Argentina**")
            boton_pago("Mercado Pago (ARS)", MP_ARG, color="#009ee3")
        with c2: 
            st.write("**Global**")
            boton_pago("Pay with Ko-fi (USD)", KOFI_GLOBAL, color="#ff5e5b")
        
        st.markdown("---")
        st.subheader("3. Valida tu Auditoría")
        st.info("Sube una captura de tu comprobante de pago para desbloquear el análisis de IA.")
        
        # EL BOTÓN DE IA DEPENDE DE ESTE ARCHIVO
        comprobante = st.file_uploader("Sube la captura de tu Pago", type=["jpg", "png", "jpeg"], key="val_pago")
        
        if comprobante:
            st.success("✅ Comprobante recibido correctamente.")
            if st.button("🚀 INICIAR AUDITORÍA PROFESIONAL"):
                with st.spinner("Escaneando tu CV para filtros ATS..."):
                    img_cv = Image.open(cv_file)
                    prompt = "Eres un reclutador Tech senior. Analiza este CV. Detecta errores críticos de diseño, falta de palabras clave y dame 5 puntos de mejora para que pase los filtros ATS."
                    res = model.generate_content([prompt, img_cv])
                    st.markdown("### 📊 Informe de Auditoría Premium:")
                    st.markdown(res.text)
                    st.balloons()
        else:
            st.warning("⚠️ El botón de análisis aparecerá aquí después de subir tu comprobante de pago.")
