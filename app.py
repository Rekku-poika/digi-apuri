import streamlit as st
import google.generativeai as genai

# Asetukset
if "GEMINI_KEY" not in st.secrets:
    st.error("API-avain puuttuu.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])

# Käytetään yksinkertaisinta mahdollista mallia ilman kokeellisia työkaluja
model = genai.GenerativeModel('models/gemini-2.0-flash')

st.title("🤖 Digi-Apuri 2026")

# Alustetaan keskusteluhistoria sessioon, jos se puuttuu
if "messages" not in st.session_state:
    st.session_state.messages = []

# Näytetään aiemmat viestit
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Käyttäjän syöte
if user_input := st.chat_input("Kysy jotain..."):
    # 1. Näytä käyttäjän viesti heti
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 2. Generoi vastaus
    with st.chat_message("assistant"):
        with st.spinner("Apuri miettii..."):
            try:
                response = model.generate_content(user_input)
                vastaus = response.text
                st.write(vastaus)
                st.session_state.messages.append({"role": "assistant", "content": vastaus})
            except Exception as e:
                st.error(f"Virhe: {str(e)}")
