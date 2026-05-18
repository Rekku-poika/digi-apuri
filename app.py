import streamlit as st
import google.generativeai as genai

# Varmistetaan, että API-avain on tallessa
if "GEMINI_KEY" not in st.secrets:
    st.error("API-avainta (GEMINI_KEY) ei löydetty järjestelmästä. Määritä se Streamlitin asetuksissa.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])

# Alustetaan muuttujat, joilla pidetään kirjaa murremoodista
if "vitsimoodi" not in st.session_state:
    st.session_state.vitsimoodi = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# Järjestelmäohjeet normaalitilaan
ohjeet_normaali = (
    "Olet PC-Keisarin Digi-Apuri, ystävällinen tekoälyavustaja ikäihmisille. "
    "Vastaat selkeästi ja rauhallisesti. JOS huomaat, että käyttäjä leikittelee, "
    "pelleilee, vitsailee tyhmiä tai kysyy jotain aivan hölmöä, sinun TÄYTYY aloittaa vastauksesi lauseella: "
    "'Pelleilet kanssani, vastataanpa sitte Pohjanmaan murteella!' "
    "ja muuttua heti pohojalaiseksi."
)

# Laajennettu Etelä-Pohjanmaan murresanakirja tekoälylle 
ohjeet_pohjanmaa = (
    "Olet PC-Keisarin Digi-Apuri, mutta olet nyt huumorimoodissa ja puhut "
    "PELKKÄÄÄ LAJIA JA LEVEÄÄ ETELÄ-POHJANMAAN MURRETTA. Vastaa topakasti, "
    "itsepäisesti ja pohojalaisella uholla ja huumorilla käyttäjän kysymyksiin. "
    "Älä käytä d-kirjainta (esim. 'pohjanmaa', 'pöyrä', 'meiren'). [cite: 38] "
    "Korvaa ts-yhdistelmä kaksois-veellä tai ärrällä (esim. 'kattoa').\n\n"
    
    "Käytä ehdottomasti näitä pronomineja ja verbejä:\n"
    "- moon = minä olen, soot = sinä olet, son = hän on [cite: 164, 165, 166]\n"
    "- moomma = me olemme, tootta = te olette, non = he ovat [cite: 167, 168, 169]\n"
    "- notta = jotta / että [cite: 85]\n\n"
    
    "Käytä vastauksissasi tilaisuuden tullen tätä virallista sanastoa:\n"
    "- trahteerata = tarjoilla, kattaa pöytä, olla vieraanvarainen [cite: 155]\n"
    "- firaata / tormoottaa = puuhastella / kiiruhtaa, mennä lujaa [cite: 154]\n"
    "- kränä / änkköö = riita, ongelma, väittely [cite: 137]\n"
    "- umpelooset = perunat [cite: 24, 156]\n"
    "- kropsu = pannukakku [cite: 122]\n"
    "- ankkastukki / pöökiä = pullapitko, pulla [cite: 12, 40, 63]\n"
    "- komia = komea, hieno [cite: 100]\n"
    "- tanttu = leninki, hame, mekko [cite: 6, 127]\n"
    "- rääppöö = puolustuskyvytön, pieni ihminen [cite: 143]\n"
    "- päässilimäänen = täysin holtittomasti käyttäytyvä [cite: 139]\n"
    "- pöyröö / pöhölö = hölmö, tyhmä [cite: 114, 119]\n"
    "- toimittaa / kehua = puhua, jutella, kertoa [cite: 56, 128]\n"
    "- kihveli = rikkalapio [cite: 8, 162]\n"
    "- peräruoka = jälkiruoka [cite: 140]\n\n"
    
    "Esimerkki asenteesta: 'Mitäs sä ny siinä trossaat? Jos se sun pränkkä tietokonees on oikunten, "
    "niin ei tartte hotalehtaa ja prääsätä! Moon tekoäly lakeurelta, eikä mun kanssa änkätä!' [cite: 116, 137]"
)

st.title("🤖 Digi-Apuri")

# Näytetään vanhat viestit
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Jos ollaan aktiivisessa pohojalaismoodissa, näytetään varoitus ja paluunapit
if st.session_state.vitsimoodi:
    st.warning("⚠️ Digi-Apuri on lukittu Pohojanmaan murteelle.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("K (Kyllä, palaa asialinjalle)"):
            st.session_state.vitsimoodi = False
            vastaus_paluu = "No soot siinä oikeas, palataanpa asialinjalle ja puhutaan suomea. Miten mä voin auttaa sua digiasioos?"
            st.session_state.messages.append({"role": "assistant", "content": vastaus_paluu})
            st.rerun()
    with col2:
        if st.button("E (Ei, annetaan palaa vaan!)"):
            st.session_state.messages.append({"role": "assistant", "content": "No sitte firaatahan viäläkin lisää! Anna tulla kysymyksiä, moon valmiina!"})
            st.rerun()

# Otetaan käyttäjän teksti vastaan
if user_input := st.chat_input("Kirjoita viestisi tähän..."):
    # Näytetään käyttäjän viesti
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Tarkistetaan jos käyttäjä kirjoitti suoraan tekstikenttään "K"
    if st.session_state.vitsimoodi and user_input.strip().upper() in ["K", "KYLLÄ"]:
        st.session_state.vitsimoodi = False
        vastaus = "No soot siinä oikeas, palataanpa asialinjalle ja puhutaan suomea. Miten mä voin auttaa sua digiasioos?"
    else:
        # Valitaan ohjeet sen mukaan, onko moodi päällä vai ei
        nykyiset_ohjeet = ohjeet_pohjanmaa if st.session_state.vitsimoodi else ohjeet_normaali
        model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=nykyiset_ohjeet)
        
        try:
            response = model.generate_content(user_input)
            vastaus = response.text
            
            # Jos lause laukaisee murteen, lukitaan se päälle
            if "Pohjanmaan murteella" in vastaus:
                st.session_state.vitsimoodi = True
            
            # Jos ollaan murretilassa, lisätään loppuun aina K/E muistutus tekstinä
            if st.session_state.vitsimoodi:
                vastaus += "\n\n*Oikeasti, palataanko asiaan? (K/E)*"
                
        except Exception as e:
            vastaus = "Hupsista keikkaa, joku lanka katkes matkalla. Koitetaanpa uurestaan!"

    # Näytetään tekoälyn vastaus
    with st.chat_message("assistant"):
        st.write(vastaus)
    st.session_state.messages.append({"role": "assistant", "content": vastaus})
    st.rerun()
