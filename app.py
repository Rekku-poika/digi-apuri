import streamlit as st
import google.generativeai as genai
import datetime

# Varmistetaan API-avain
if "GEMINI_KEY" not in st.secrets:
    st.error("API-avainta ei löydetty.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])

# Päivämäärä
tanaan = datetime.date.today().strftime("%d.%m.%Y")

# Järjestelmäohjeet
ohjeet_normaali = (
    f"Olet PC-Keisarin Digi-Apuri, ystävällinen digiohjaaja ikäihmisille. Tänään on {tanaan}. "
    "Vastaa selkeästi ja rauhallisesti. JOS kysymys vaatii ajankohtaista tietoa, KÄYTÄ Google-hakua. "
)

ohjeet_pohjanmaa = (
    f"Olet PC-Keisarin Digi-Apuri (pohojalainen huumorimoodi). Tänään on {tanaan}. "
    "Puhu leveää etelä-pohjanmaan murretta. Käytä Google-hakua ajankohtaisiin asioihin."
)

if "vitsimoodi" not in st.session_state: st.session_state.vitsimoodi = False
if "messages" not in st.session_state: st.session_state.messages = []

st.title("🤖 Digi-Apuri")

# Viestihistoria
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Käyttäjän syöte
if user_input := st.chat_input("Kirjoita viestisi..."):
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    nykyiset_ohjeet = ohjeet_pohjanmaa if st.session_state.vitsimoodi else ohjeet_normaali
    
    # KÄYTETÄÄN TÄTÄ MALLIA, SE ON VARMIN VAIHTOEHTO HAKUTOIMINNOLLA
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        system_instruction=nykyiset_ohjeet,
        tools=[{"google_search_retrieval": {}}]
    )
    
    try:
        response = model.generate_content(user_input)
        vastaus = response.text
        if "Pohjanmaan murteella" in vastaus: st.session_state.vitsimoodi = True
    except Exception as e:
        vastaus = f"Virhe: {str(e)}" # TÄMÄ NÄYTTÄÄ NYT VIRHEEN PUNAISENA

    with st.chat_message("assistant"):
        st.write(vastaus)
    st.session_state.messages.append({"role": "assistant", "content": vastaus})
    st.rerun()
