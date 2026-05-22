import streamlit as st
import google.generativeai as genai
import datetime

if "GEMINI_KEY" not in st.secrets:
    st.error("API-avain puuttuu.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])

# Käytetään gemini-3.5-flash -mallia
model = genai.GenerativeModel('models/gemini-3.5-flash')

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
        # VUODEN 2026 KORJAUS:
        # Käytetään 'google_search_retrieval' -toimintoa suoraan mallin 
        # config-asetuksissa, eikä erillisessä tools-listassa.
        response = model.generate_content(
            user_input,
            tools=[genai.types.Tool(google_search_retrieval=genai.types.GoogleSearchRetrieval())]
        )
        vastaus = response.text
    except Exception as e:
        # Jos haku epäonnistuu, tehdään puhdas generointi ilman työkalua
        vastaus = model.generate_content(user_input).text

    with st.chat_message("assistant"):
        st.write(vastaus)
    st.session_state.messages.append({"role": "assistant", "content": vastaus})
    st.rerun()
