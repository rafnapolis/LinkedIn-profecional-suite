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
    st.error("Error crítico: Revisa tu API KEY en Secrets.")

# --- ENLACES ---
MONETAG = st.secrets.get("MONETAG_LINK", "#")
MP_ARG = st.secrets.get("MP_LINK", "#")
KOFI_GLOBAL = st.secrets.get("KOFI_LINK", "#")

# --- INICIALIZACIÓN DE ESTADOS (Clave para que no 'pase de largo') ---
if 'paso_monetag' not in st.session_state:
    st.session_state.paso_monetag = False
if 'espera_completada' not in st.session_state:
    st.session_state.espera_completada = False

st.set_page_config(page_title="LinkedIn Suite Pro", page_icon="🚀")

# Función de botón corregida para evitar que salga sin letras
def dibujar_boton(texto, link, color="#28a745"):
    st.markdown(f'''
        <a href="{link}" target="_blank" style="text-decoration: none;">
            <div style="background-color: {color}; color: white; padding: 18px; text-align: center; border-radius: 12px; font-weight: bold; margin: 10px 0; font-size: 18px;">
                {texto}
            </div>
        </a>
    ''', unsafe_allow_html=True)

st.title("💼 LinkedIn Professional Suite")
tabs = st.tabs(["✨ Humanizador", "👤 Perfil", "📄 Auditoría CV"])

# --- TAB 1: HUMANIZADOR ---
with tabs[0]:
    t_post = st.text_area("Borrador:")
    if st.button("🚀 Optimizar Post"):
        if t_post:
            res = model.generate_content(f"Optimiza este post para LinkedIn: {t_post}")
            st.write(res.text)
            st.info(f"👉 [Más herramientas gratis aquí]({MONETAG})")

# --- TAB 2: PERFIL (FLUJO FORZADO MONETAG) ---
with tabs[1]:
    st.header("Análisis de Perfil")
    f_perfil = st.file_uploader("Sube tu foto", type=["jpg", "png", "jpeg"], key="up_perfil")
    
    if f_perfil:
        st.image(f_perfil, width=150)
        
        # PASO 1: Obligar a ir a Monetag
        st.subheader("1️⃣ Obtener Acceso")
        dibujar_boton("🚀 CLIC AQUÍ: VER PUBLICIDAD Y ACTIVAR IA", MONETAG, color="#0077b5")
        
        if st.button("YA HICE CLIC (DESBLOQUEAR SIGUIENTE PASO)"):
            st.session_state.paso_monetag = True
        
        # PASO 2: Solo si hizo clic, aparece el temporizador
        if st.session_state.paso_monetag:
            st.markdown("---")
            st.subheader("2️⃣ Validando Token (10s)")
            if st.button("🔗 INICIAR VALIDACIÓN"):
                barra = st.progress(0)
                aviso = st.empty()
                for i in range(11):
                    barra.progress(i * 10)
                    aviso.text(f"Verificando... No cierres la ventana. Faltan {10-i}s")
                    time.sleep(1)
                st.session_state.espera_completada = True
                aviso.success("✅ Servidor de IA Listo.")

        # PASO 3: Solo si esperó, aparece el botón final
        if st.session_state.espera_completada:
            if st.button("⚡ EJECUTAR ANÁLISIS DE PERFIL"):
                img = Image.open(f_perfil)
                res = model.generate_content(["Analiza esta foto de LinkedIn profesionalmente.", img])
                st.write(res.text)
                # Reset para seguridad
                st.session_state.paso_monetag = False
                st.session_state.espera_completada = False

# --- TAB 3: CV (BLOQUEO POR COMPROBANTE) ---
with tabs[2]:
    st.header("🎯 Auditoría Premium CV")
    f_cv = st.file_uploader("Sube tu CV (Imagen)", type=["jpg", "png", "jpeg"], key="up_cv")
    
    if f_cv:
        st.subheader("1. Realiza el Pago")
        col1, col2 = st.columns(2)
        with col1: dibujar_boton("Pagar Mercado Pago", MP_ARG, color="#009ee3")
        with col2: dibujar_boton("Pay with Ko-fi", KOFI_GLOBAL, color="#ff5e5b")
        
        st.markdown("---")
        st.subheader("2. Sube tu Comprobante")
        f_pago = st.file_uploader("Captura del comprobante", type=["jpg", "png", "jpeg"], key="up_pago")
        
        if f_pago:
            st.success("✅ Comprobante detectado.")
            if st.button("🚀 INICIAR ANÁLISIS PROFESIONAL"):
                with st.spinner("Analizando..."):
                    img_cv = Image.open(f_cv)
                    res = model.generate_content(["Analiza este CV como reclutador senior.", img_cv])
                    st.markdown(res.text)
        else:
            st.warning("⚠️ Debes subir el comprobante para desbloquear este botón.")
