import streamlit as st
import google.generativeai as genai

if "GEMINI_KEY" not in st.secrets:
    st.error("API-avain puuttuu.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])

# Käytetään työkalua listana, joka sisältää vain nimen
model = genai.GenerativeModel(
    model_name='models/gemini-3.5-flash',
    tools=[genai.protos.Tool(google_search_retrieval=genai.protos.GoogleSearchRetrieval())]
)

if "messages" not in st.session_state: st.session_state.messages = []

st.title("🤖 Digi-Apuri 2026")

if user_input := st.chat_input("Kirjoita viestisi..."):
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        # Käytetään generointia
        response = model.generate_content(user_input)
        vastaus = response.text
    except Exception as e:
        vastaus = f"Virhe: {str(e)}"

    with st.chat_message("assistant"):
        st.write(vastaus)
    st.session_state.messages.append({"role": "assistant", "content": vastaus})
    st.rerun()
