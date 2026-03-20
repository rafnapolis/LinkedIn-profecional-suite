import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# 1. CONFIGURACIÓN DE IA Y ENLACES
genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
model = genai.GenerativeModel("gemini-1.5-flash")
MONETAG_LINK = os.environ.get('MONETAG_LINK')
MP_LINK = "https://link.mercadopago.com.ar/ministerioicd" # Para Argentina
KOFI_LINK = "https://ko-fi.com/ministerioicd" # Para el resto del mundo

st.set_page_config(page_title="Professional AI Suite", page_icon="📈", layout="centered")

# --- INTERFAZ DE NAVEGACIÓN ---
menu = ["✨ Humanizar Post", "👤 Optimizar Perfil", "📄 Auditar CV"]
choice = st.sidebar.selectbox("¿Qué quieres hacer hoy?", menu)

# --- OPCIÓN 1: HUMANIZADOR (Monetización Indirecta) ---
if choice == "✨ Humanizar Post":
    st.title("🤖 LinkedIn Humanizer")
    texto = st.text_area("Pega tu idea aquí:")
    if st.button("Optimizar Post"):
        if texto:
            with st.spinner("Procesando..."):
                res = model.generate_content(f"Optimiza este post para LinkedIn con ganchos virales: {texto}")
                st.markdown(res.text)
                st.info(f"👉 [Obtén más tips aquí]({MONETAG_LINK})")

# --- OPCIÓN 2: OPTIMIZAR PERFIL (Monetización Monetag) ---
elif choice == "👤 Optimizar Perfil":
    st.title("📸 Auditoría de Foto y Perfil")
    st.write("Sube tu foto de perfil para un análisis de impacto visual.")
    
    img_file = st.file_uploader("Sube tu foto (JPG/PNG)", type=["jpg", "png", "jpeg"])
    
    if img_file:
        st.image(img_file, width=150)
        st.markdown(f"### 🛡️ Paso de Seguridad\nPara recibir el puntaje ATS y análisis de imagen, genera tu clave de acceso:")
        
        # Botón Monetag
        st.markdown(f'''<a href="{MONETAG_LINK}" target="_blank" style="text-decoration:none;">
            <div style="background-color:#0077b5;color:white;padding:12px;text-align:center;border-radius:8px;">
                🔑 GENERAR CLAVE DE ACCESO IA
            </div></a>''', unsafe_allow_html=True)
        
        if st.button("⚡ VER MI PUNTAJE"):
            img = Image.open(img_file)
            res = model.generate_content(["Analiza esta foto de perfil para LinkedIn. Da un puntaje del 1 al 10 y 3 consejos de mejora profesional.", img])
            st.success("Análisis completado:")
            st.write(res.text)

# --- OPCIÓN 3: AUDITAR CV (Monetización Directa) ---
elif choice == "📄 Auditar CV":
    st.title("🎯 CV Auditor Pro")
    st.write("Analizamos tu CV para que supere los filtros de las grandes empresas.")
    
    cv_file = st.file_uploader("Sube tu CV (Imagen o PDF)", type=["jpg", "png", "pdf"])
    
    if cv_file:
        # Lógica de Pago por Ubicación
        st.markdown("### 💳 Activa tu Auditoría Premium")
        ubicacion = st.radio("¿Dónde te encuentras?", ["Argentina", "Resto del Mundo"])
        
        link_pago = MP_LINK if ubicacion == "Argentina" else KOFI_LINK
        texto_pago = "Pagar con Mercado Pago (ARS)" if ubicacion == "Argentina" else "Pay with Ko-fi (USD)"
        
        st.markdown(f'''<a href="{link_pago}" target="_blank" style="text-decoration:none;">
            <div style="background-color:#28a745;color:white;padding:12px;text-align:center;border-radius:8px;">
                💰 {texto_pago}
            </div></a>''', unsafe_allow_html=True)
        
        st.warning("Una vez realizado el pago, presiona el botón para procesar el documento.")
        
        if st.button("🚀 INICIAR AUDITORÍA"):
            # Aquí Gemini analiza el contenido del CV
            res = model.generate_content("Analiza este CV. Detecta fallas para software ATS y dime cómo hacerlo más atractivo para recruiters.")
            st.markdown(res.text)
