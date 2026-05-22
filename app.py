import streamlit as st
import google.generativeai as genai

# 1. Asetetaan sivu
st.set_page_config(page_title="Mallien lista", page_icon="🤖")
st.title("🤖 Mallien listaus")

# 2. Varmistetaan että API-avain löytyy
if "GEMINI_KEY" not in st.secrets:
    st.error("Virhe: GEMINI_KEY puuttuu Streamlit Secretsistä.")
    st.stop()

# 3. Konfiguroidaan Gemini
try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    
    # 4. Haetaan lista
    st.write("Haetaan malleja palvelimelta...")
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # 5. Näytetään lista
    st.success(f"Löytyi {len(models)} mallia:")
    st.write(models)
    
    st.info("Kopioi yllä olevasta listasta se nimi, jota haluat käyttää, ja kerro se minulle!")

except Exception as e:
    st.error(f"Tapahtui virhe yhteydessä: {str(e)}")
