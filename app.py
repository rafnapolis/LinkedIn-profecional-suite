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

# Inicializar estados de sesión para el flujo móvil
if 'clic_monetag' not in st.session_state:
    st.session_state['clic_monetag'] = False
if 'perfil_ready' not in st.session_state:
    st.session_state['perfil_ready'] = False

st.set_page_config(page_title="LinkedIn Suite Pro", page_icon="🚀")

# Función mejorada para detectar el clic en Monetag
def link_monetag():
    st.session_state['clic_monetag'] = True

st.title("💼 LinkedIn Professional Suite")
tabs = st.tabs(["✨ Humanizador", "👤 Perfil", "📄 Auditoría CV"])

# --- TAB 2: PERFIL (FLUJO BLOQUEADO) ---
with tabs[1]:
    st.header("Análisis de Perfil")
    foto = st.file_uploader("Sube tu foto de perfil", type=["jpg", "png", "jpeg"], key="p_foto")
    
    if foto:
        st.image(foto, width=150)
        st.subheader("🔑 Paso 1: Activar Servidor")
        st.write("Para habilitar la IA, primero debes generar tu clave de acceso gratuita:")
        
        # EL BOTÓN DE MONETAG (Al hacer clic, cambia el estado)
        st.markdown(f'''<a href="{MONETAG}" target="_blank" style="text-decoration:none;">
            <div style="background-color:#0077b5;color:white;padding:15px;text-align:center;border-radius:10px;font-weight:bold;margin:10px 0;">
                🚀 CLIC AQUÍ: GENERAR CLAVE DE ACCESO
            </div></a>''', unsafe_allow_html=True)
        
        # Botón de confirmación manual para que Streamlit "sepa" que salieron a ver la publicidad
        if st.button("YA HICE CLIC EN EL BOTÓN AZUL ✅"):
            st.session_state['clic_monetag'] = True

        # PASO 2: Solo aparece si st.session_state['clic_monetag'] es True
        if st.session_state['clic_monetag']:
            st.markdown("---")
            st.subheader("⏳ Paso 2: Validando Publicidad")
            
            if st.button("🔗 INICIAR VALIDACIÓN DE 10 SEGUNDOS"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(11):
                    progress_bar.progress(i * 10)
                    status_text.text(f"Verificando token... Espera {10-i} segundos")
                    time.sleep(1)
                
                status_text.success("✅ Acceso Validado.")
                st.session_state['perfil_ready'] = True

        # PASO 3: Ejecución final
        if st.session_state.get('perfil_ready'):
            if st.button("⚡ EJECUTAR ANÁLISIS AHORA"):
                with st.spinner("IA Analizando..."):
                    img = Image.open(foto)
                    res = model.generate_content(["Analiza esta foto de LinkedIn profesionalmente.", img])
                    st.write(res.text)
                    # Reset para que tengan que volver a pagar/ver publicidad la próxima vez
                    st.session_state['clic_monetag'] = False
                    st.session_state['perfil_ready'] = False

# --- TAB 3: CV (SE MANTIENE EL COMPROBANTE) ---
with tabs[2]:
    st.header("🎯 Auditoría Premium CV")
    cv_file = st.file_uploader("Sube tu CV (Imagen)", type=["jpg", "png", "jpeg"], key="cv_main")
    if cv_file:
        st.markdown("### 1. Pago y 2. Comprobante")
        comprobante = st.file_uploader("Sube captura del pago", type=["jpg", "png", "jpeg"], key="val_pago")
        if comprobante:
            if st.button("🚀 INICIAR AUDITORÍA"):
                img_cv = Image.open(cv_file)
                res = model.generate_content(["Análisis ATS.", img_cv])
                st.markdown(res.text)
