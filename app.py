import streamlit as st
import google.generativeai as genai

# Varmistetaan, että API-avain on tallessa
if "GEMINI_KEY" not in st.secrets:
    st.error("API-avainta (GEMINI_KEY) ei löydetty järjestelmästä. Määritä se Streamlitin asetuksissa.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])

# Alustetaan muuttujat, joilla pidetään kirjaa vitsimoodista
if "vitsimoodi" not in st.session_state:
    st.session_state.vitsimoodi = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# TÄRKEÄÄ: Ohjeistetaan tekoäly tunnistamaan pelleily ja toimimaan sen mukaan
ohjeet = (
    "Olet PC-Keisarin Digi-Apuri, ystävällinen tekoälyavustaja ikäihmisille. "
    "MUKAUTETTU SÄÄNTÖ: Jos huomaat, että käyttäjä pelleilee, vitsailee tyhmiä, "
    "kyselee täysin asiaankuulumattomia (kuten 'onko kuu juustoa') tai yrittää muuten vain "
    "testata sinua hölmöillä kysymyksillä, sinun TÄYTYY aloittaa vastauksesi lauseella: "
    "'Pelleilet kanssani, annampa takaisin!' ja vastata sen jälkeen vitsillä, ironisesti tai hassusti takaisin. "
    "Pysy kuitenkin kohteliaana."
)

model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=ohjeet)

st.title("🤖 Digi-Apuri")

# Näytetään vanhat viestit
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Jos ollaan aktiivisessa vitsimoodissa, tarjotaan napit paluuseen
if st.session_state.vitsimoodi:
    st.warning("Digi-Apuri on vitsimoodissa. Palataanko oikeasti asiaan?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("K (Kyllä, palaa asiaan)"):
            st.session_state.vitsimoodi = False
            st.session_state.messages.append({"role": "assistant", "content": "Selvä pyyhi! Palataanpa takaisin asialinjalle. Miten voin auttaa digiasioissa?"})
            st.rerun()
    with col2:
        if st.button("E (Ei, jatketaan vitsillä)"):
            st.write("Jatketaan siis pelleilyä! 😉")

# Otetaan käyttäjän teksti vastaan
if user_input := st.chat_input("Kirjoita viestisi tähän..."):
    # Näytetään käyttäjän viesti
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Tarkistetaan jos käyttäjä vastasi suoraan tekstinä K/E vitsimoodissa
    if st.session_state.vitsimoodi and user_input.strip().upper() in ["K", "KYLLÄ"]:
        st.session_state.vitsimoodi = False
        vastaus = "Selvä pyyhi! Palataanpa takaisin asialinjalle. Miten voin auttaa digiasioissa?"
    else:
        # Haetaan vastaus tekoälyltä
        try:
            response = model.generate_content(user_input)
            vastaus = response.text
            
            # Jos tekoäly päätti herjata pelleilystä, kytketään vitsimoodi päälle muistiin
            if "Pelleilet kanssani" in vastaus:
                st.session_state.vitsimoodi = True
                # Lisätään loppuun vaatimus paluusta
                vastaus += "\n\n*Oikeasti, palataanko asiaan? (K/E)*"
                
        except Exception as e:
            vastaus = "Hups, yhteys katkesi. Yritetäänpä uudelleen!"

    # Näytetään tekoälyn vastaus
    with st.chat_message("assistant"):
        st.write(vastaus)
    st.session_state.messages.append({"role": "assistant", "content": vastaus})
    st.rerun()
