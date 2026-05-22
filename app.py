import streamlit as st
import google.generativeai as genai

if "GEMINI_KEY" not in st.secrets:
    st.error("API-avain puuttuu.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])

# Käytetään mallia gemini-3.5-flash
# TÄRKEÄÄ: Poistetaan kaikki monimutkaiset tyyppimääritykset (types.Tool jne)
model = genai.GenerativeModel(
    model_name='models/gemini-3.5-flash',
    tools='google_search' # Tämä on uusin ja tuetuin tapa
)

if "messages" not in st.session_state: st.session_state.messages = []

st.title("🤖 Digi-Apuri 2026")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_input := st.chat_input("Kirjoita viestisi..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    try:
        # Käytetään suoraa generointia - malli osaa nyt käyttää 'google_search' 
        # työkalua, koska se on määritelty alustuksessa.
        response = model.generate_content(user_input)
        vastaus = response.text
    except Exception as e:
        vastaus = f"Tekninen virhe: {str(e)}"

    with st.chat_message("assistant"):
        st.write(vastaus)
    st.session_state.messages.append({"role": "assistant", "content": vastaus})
    st.rerun()
