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
    st.error("Error de configuración de IA. Revisa tus Secrets.")

# --- ENLACES ---
MONETAG = st.secrets.get("MONETAG_LINK", "#")
MP_ARG = st.secrets.get("MP_LINK", "#")
KOFI_GLOBAL = st.secrets.get("KOFI_LINK", "#")

# --- ESTADOS DE SESIÓN (Para evitar saltos) ---
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
            res = model.generate_content(f"Optimiza este post para LinkedIn con ganchos: {t_post}")
            st.write(res.text)
            st.info(f"👉 [Más herramientas gratis aquí]({MONETAG})")

# --- TAB 2: PERFIL (MONETIZACIÓN POR TIEMPO) ---
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
            if st.button("⚡ EJECUTAR ANÁLISIS DE PERFIL"):
                img = Image.open(f_p)
                res = model.generate_content(["Analiza esta foto de LinkedIn profesionalmente.", img])
                st.write(res.text)
                st.session_state.clic_monetag = False
                st.session_state.perfil_valido = False

# --- TAB 3: CV (VALIDACIÓN DE COMPROBANTE CON IA) ---
with tabs[2]:
    st.header("🎯 Auditoría Premium CV")
    f_cv = st.file_uploader("1. Sube tu CV (Imagen)", type=["jpg", "png", "jpeg"], key="cv_up")
    
    if f_cv:
        st.subheader("2. Realiza el Pago")
        c1, c2 = st.columns(2)
        with c1: dibujar_boton("Mercado Pago (ARG)", MP_ARG, color="#009ee3")
        with c2: dibujar_boton("Ko-fi (Global)", KOFI_GLOBAL, color="#ff5e5b")
        
        st.markdown("---")
        st.subheader("3. Validación de Comprobante")
        f_pago = st.file_uploader("Sube la captura de tu pago", type=["jpg", "png", "jpeg"], key="pago_ia")
        
        if f_pago:
            if st.button("🔍 VERIFICAR PAGO CON IA"):
                with st.spinner("Nuestra IA está verificando el ticket..."):
                    img_ticket = Image.open(f_pago)
                    v_prompt = "Responde solo VALIDO si esta imagen es un comprobante de pago de banco, Mercado Pago o Ko-fi. Si es otra cosa, responde FALSO."
                    v_res = model.generate_content([v_prompt, img_ticket])
                    
                    if "VALIDO" in v_res.text.upper():
                        st.session_state.pago_cv_verificado = True
                        st.success("✅ ¡Pago confirmado! Botón de Auditoría desbloqueado.")
                    else:
                        st.error("❌ Imagen no válida. Sube un comprobante de pago real.")

            if st.session_state.pago_cv_verificado:
                if st.button("🚀 INICIAR AUDITORÍA PROFESIONAL"):
                    with st.spinner("Analizando CV..."):
                        img_cv = Image.open(f_cv)
                        res = model.generate_content(["Analiza este CV para filtros ATS.", img_cv])
                        st.markdown(res.text)
                        st.balloons()
                        st.session_state.pago_cv_verificado = False
