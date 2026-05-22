import streamlit as st
import google.generativeai as genai
import datetime

# API-avaimen haku
if "GEMINI_KEY" not in st.secrets:
    st.error("API-avainta (GEMINI_KEY) ei löydetty Streamlitin asetuksista.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])

# Päivämäärä kontekstiksi
tanaan = datetime.date.today().strftime("%d.%m.%Y")

# Järjestelmäohjeet
ohjeet_normaali = (
    f"Olet PC-Keisarin Digi-Apuri, ystävällinen tekoälyavustaja ikäihmisille. Tänään on {tanaan}. "
    "Vastaa selkeästi ja rauhallisesti. JOS kysymys vaatii tietoa, jota et tiedä tai joka on "
    "tapahtunut koulutuksesi jälkeen, KÄYTÄ Google-hakua vastaamiseen. "
    "Jos huomaat, että käyttäjä vitsailee, aloita vastauksesi: 'Pelleilet kanssani, vastataanpa sitte Pohjanmaan murteella!'"
)

ohjeet_pohjanmaa = (
    f"Olet PC-Keisarin Digi-Apuri (pohojalainen huumorimoodi). Tänään on {tanaan}. "
    "Puhu PELKKÄÄ LEVEÄÄ ETELÄ-POHJANMAAN MURRETTA. Vastaa topakasti. "
    "JOS kysymys vaatii ajankohtaista tietoa, KÄYTÄ Google-hakua. "
    "Älä käytä d-kirjainta. Käytä murresanoja: moon, soot, son, kropsu, komia, pöyröö."
)

if "vitsimoodi" not in st.session_state: st.session_state.vitsimoodi = False
if "messages" not in st.session_state: st.session_state.messages = []

st.title("🤖 Digi-Apuri")

# Näytetään vanhat viestit
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Moodin hallinta
if st.session_state.vitsimoodi:
    st.warning("⚠️ Digi-Apuri on lukittu Pohojanmaan murteelle.")
    col1, col2 = st.columns(2)
    if col1.button("K (Palaa asialinjalle)"):
        st.session_state.vitsimoodi = False
        st.rerun()
    if col2.button("E (Jatka murteella!)"):
        st.rerun()

# Käyttäjän syöte
if user_input := st.chat_input("Kirjoita viestisi..."):
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    nykyiset_ohjeet = ohjeet_pohjanmaa if st.session_state.vitsimoodi else ohjeet_normaali
    
    # Generointi hakutoiminnon kanssa
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash', 
        system_instruction=nykyiset_ohjeet,
        tools=[{"google_search_retrieval": {}}]
    )
        
    try:
        response = model.generate_content(user_input)
        vastaus = response.text
        if "Pohjanmaan murteella" in vastaus: st.session_state.vitsimoodi = True
    except Exception as e:
        vastaus = "Hups, nyt joku lanka katkes. Kokeile uurestaan!"

    with st.chat_message("assistant"):
        st.write(vastaus)
    st.session_state.messages.append({"role": "assistant", "content": vastaus})
    st.rerun()
