import streamlit as st
import google.generativeai as genai
import datetime

if "GEMINI_KEY" not in st.secrets:
    st.error("API-avain puuttuu.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])
tanaan = datetime.date.today().strftime("%d.%m.%Y")

# Käytetään mallia ilman tool-listauksia alustuksessa
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

if "messages" not in st.session_state: st.session_state.messages = []

st.title("🤖 Digi-Apuri")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_input := st.chat_input("Kirjoita viestisi..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    try:
        # TÄMÄ ON KORJAUS: Käytetään grounding-työkalua funktiona
        response = model.generate_content(
            user_input,
            tools=[genai.types.Tool(google_search_retrieval=genai.types.GoogleSearchRetrieval())]
        )
        vastaus = response.text
    except Exception as e:
        # Jos uusi tapa ei toimi, kokeillaan vähintään puhdasta generointia
        vastaus = "Tietoa haettaessa tapahtui virhe, mutta tässä on oma arvaukseni: " + model.generate_content(user_input).text

    with st.chat_message("assistant"):
        st.write(vastaus)
    st.session_state.messages.append({"role": "assistant", "content": vastaus})
    st.rerun()
