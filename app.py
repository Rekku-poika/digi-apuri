import streamlit as st
import google.generativeai as genai

if "GEMINI_KEY" not in st.secrets:
    st.error("API-avain puuttuu.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])

# TÄRKEÄÄ: Pakotetaan haku system_instruction-kohdassa
system_prompt = (
    "Olet Digi-Apuri. Sinulla on käytössäsi Google Search -työkalu. "
    "KUN käyttäjä kysyy ajankohtaisista asioista, ihmisistä, uutisista tai faktoista, "
    "JOITA et voi tietää varmuudella ilman internetiä, sinun ON käytettävä Google Searchia. "
    "Älä vastaa muistisi perusteella, jos kyseessä on muuttuva tieto."
)

model = genai.GenerativeModel(
    model_name='models/gemini-3.5-flash',
    system_instruction=system_prompt
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

    # Käytetään grounding-työkalua eksplisiittisesti
    try:
        response = model.generate_content(
            user_input,
            tools=[genai.types.Tool(google_search_retrieval=genai.types.GoogleSearchRetrieval())]
        )
        vastaus = response.text
    except Exception as e:
        vastaus = f"Hakutoiminto ei vastannut: {e}"

    with st.chat_message("assistant"):
        st.write(vastaus)
    st.session_state.messages.append({"role": "assistant", "content": vastaus})
    st.rerun()
