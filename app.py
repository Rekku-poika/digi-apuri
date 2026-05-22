import streamlit as st
import google.generativeai as genai
import datetime

# Varmistetaan API-avain
if "GEMINI_KEY" not in st.secrets:
    st.error("API-avainta (GEMINI_KEY) ei löydetty.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])

tanaan = datetime.date.today().strftime("%d.%m.%Y")

# Järjestelmäohjeet
ohjeet_normaali = (
    f"Olet PC-Keisarin Digi-Apuri, ystävällinen digiohjaaja ikäihmisille. Tänään on {tanaan}. "
    "Vastaa selkeästi. JOS kysymys vaatii ajankohtaista tietoa, käytä hakua."
)

ohjeet_pohjanmaa = (
    f"Olet PC-Keisarin Digi-Apuri (pohojalainen murre). Tänään on {tanaan}. "
    "Käytä leveää murretta ja hakua tarvittaessa."
)

if "vitsimoodi" not in st.session_state: st.session_state.vitsimoodi = False
if "messages" not in st.session_state: st.session_state.messages = []

st.title("🤖 Digi-Apuri")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_input := st.chat_input("Kirjoita viestisi..."):
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    nykyiset_ohjeet = ohjeet_pohjanmaa if st.session_state.vitsimoodi else ohjeet_normaali
    
    # MALLIN ALUSTUS - KÄYTETÄÄN VARMAA TAPAA
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=nykyiset_ohjeet
    )
    
    try:
        # Haetaan vastaus (ilman tools-määrittelyä, joka aiheuttaa virheitä)
        # Gemini 1.5 Flashissa on sisäänrakennettu kyky päättää hakutarpeesta
        response = model.generate_content(
            user_input,
            tools=[{"google_search_retrieval": {}}]
        )
        vastaus = response.text
        if "Pohjanmaan murteella" in vastaus: st.session_state.vitsimoodi = True
    except Exception as e:
        # Jos haku ei toimi, kokeillaan ilman sitä
        try:
            response = model.generate_content(user_input)
            vastaus = response.text
        except:
            vastaus = "Olipa kinkkinen kysymys! Kokeile uudestaan."

    with st.chat_message("assistant"):
        st.write(vastaus)
    st.session_state.messages.append({"role": "assistant", "content": vastaus})
    st.rerun()
