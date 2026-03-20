import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# --- CONFIGURACIÓN DE IA DINÁMICA ---
# Esto evita el error 404 al buscar el modelo disponible en tu cuenta
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Buscamos modelos que soporten generación de contenido
    modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # Prioridad de selección
    if "models/gemini-1.5-flash" in modelos:
        target_model = "gemini-1.5-flash"
    elif "models/gemini-1.5-pro" in modelos:
        target_model = "gemini-1.5-pro"
    else:
        target_model = modelos[0].replace("models/", "")
        
    model = genai.GenerativeModel(target_model)
except Exception as e:
    st.error("Error de configuración inicial. Revisa las Secrets en Streamlit.")

# --- ENLACES DE MONETIZACIÓN ---
MONETAG = st.secrets.get("MONETAG_LINK", "#")
MP_ARG = st.secrets.get("MP_LINK", "#")
KOFI_GLOBAL = st.secrets.get("KOFI_LINK", "#")

# --- INTERFAZ ---
st.set_page_config(page_title="LinkedIn Suite Pro", page_icon="🚀")

# Estilo para botones de pago
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

# --- TAB 1: HUMANIZADOR ---
with tabs[0]:
    st.header("Humanizador de Posts")
    texto_post = st.text_area("Pega tu borrador:", placeholder="Ej: Hoy instalé un servidor...")
    
    if st.button("🚀 Optimizar Post"):
        if texto_post:
            with st.spinner("La IA está escribiendo..."):
                prompt = f"Eres experto en LinkedIn. Convierte esto en un post humano con 3 ganchos y una pregunta final: {texto_post}"
                response = model.generate_content(prompt)
                st.markdown("### ✅ Tu Post Optimizado:")
                st.write(response.text)
                st.info(f"👉 [¿Quieres más tips virales? Haz clic aquí]({MONETAG})")
        else:
            st.warning("Escribe algo primero.")

# --- TAB 2: AUDITOR DE PERFIL (Monetizado con Monetag) ---
with tabs[1]:
    st.header("Auditoría de Perfil")
    st.write("Analiza tu foto de perfil con IA para mejorar tu marca personal.")
    
    foto = st.file_uploader("Sube tu foto de perfil", type=["jpg", "png", "jpeg"])
    
    if foto:
        st.image(foto, width=150)
        st.markdown(f"### 🛡️ Validación Requerida")
        st.write("Para ver tu puntaje de perfil (0-10) y consejos de IA, activa tu sesión:")
        
        boton_pago("🔑 1. GENERAR TOKEN (GRATIS)", MONETAG, color="#0077b5")
        
        if st.button("⚡ 2. VER RESULTADOS DE AUDITORÍA"):
            with st.spinner("Analizando imagen..."):
                img = Image.open(foto)
                res = model.generate_content(["Analiza esta foto de LinkedIn. Da un puntaje del 1 al 10, evalúa la iluminación, el fondo y la expresión profesional.", img])
                st.success("Análisis de Perfil Completado")
                st.markdown(res.text)

# --- TAB 3: AUDITOR DE CV (Monetización Directa) ---
with tabs[2]:
    st.header("Auditoría de CV (ATS Friendly)")
    st.write("Analizamos tu CV para que pase los filtros de las grandes empresas.")
    
    cv_file = st.file_uploader("Sube tu CV en formato Imagen (Próximamente PDF)", type=["jpg", "png", "jpeg"])
    
    if cv_file:
        st.markdown("### 💳 Activa tu Auditoría Premium")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Argentina**")
            boton_pago("Pagar con Mercado Pago", MP_ARG, color="#009ee3")
            
        with col2:
            st.write("**Resto del Mundo**")
            boton_pago("Pay with Ko-fi (USD)", KOFI_GLOBAL, color="#ff5e5b")
            
        if st.button("🚀 INICIAR ANÁLISIS DE CV"):
            with st.spinner("Escaneando debilidades en el CV..."):
                img_cv = Image.open(cv_file)
                res = model.generate_content(["Actúa como un reclutador experto. Analiza este CV, busca palabras clave faltantes y errores que los filtros ATS rechazarían.", img_cv])
                st.markdown("### 📊 Informe de Auditoría:")
                st.markdown(res.text)
