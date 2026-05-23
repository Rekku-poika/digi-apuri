import streamlit as st
from openai import OpenAI

# 1. Konfigurointi
client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"], 
    base_url="https://api.groq.com/openai/v1"
)

# 2. Alustetaan muuttujat
if "vitsimoodi" not in st.session_state: st.session_state.vitsimoodi = False
if "messages" not in st.session_state: st.session_state.messages = []

# 3. Järjestelmäohjeet (Alkuperäinen murresanakirja ja ohjeistus)
ohjeet_normaali = (
    "Olet PC-Keisarin Digi-Apuri, ystävällinen tekoälyavustaja ikäihmisille. "
    "Vastaat selkeästi ja rauhallisesti. JOS huomaat, että käyttäjä leikittelee, "
    "pelleilee, vitsailee tyhmiä tai kysyy jotain aivan hölmöä, sinun TÄYTYY aloittaa vastauksesi lauseella: "
    "'Pelleilet kanssani, vastataanpa sitte Pohjanmaan murteella!' ja muuttua heti pohojalaiseksi."
)

ohjeet_pohjanmaa = (
    "Olet PC-Keisarin Digi-Apuri, mutta olet nyt huumorimoodissa ja puhut "
    "PELKKÄÄÄ LAJIA JA LEVEÄÄ ETELÄ-POHJANMAAN MURRETTA. Vastaa topakasti, "
    "itsepäisesti ja pohojalaisella uholla ja huumorilla käyttäjän kysymyksiin. "
    "Älä käytä d-kirjainta. Korvaa ts-yhdistelmä kaksois-veellä tai ärrällä. "
    "Käytä sanoja: moon, soot, son, moomma, tootta, non, notta. "
    "Sanasto: trahteerata, firaata, kränä, umpelooset, kropsu, ankkastukki, komia, tanttu, rääppöö, päässilimäänen, pöyröö, toimittaa, kihveli, peräruoka."
)

st.title("🤖 Digi-Apuri")

# Näytetään vanhat viestit
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Moodin hallinta
if st.session_state.vitsimoodi:
    st.warning("⚠️ Digi-Apuri on lukittu Pohojanmaan murteelle.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("K (Kyllä, palaa asialinjalle)"):
            st.session_state.vitsimoodi = False
            st.session_state.messages.append({"role": "assistant", "content": "No soot siinä oikeas, palataanpa asialinjalle ja puhutaan suomea. Miten mä voin auttaa sua digiasioos?"})
            st.rerun()
    with col2:
        if st.button("E (Ei, annetaan palaa vaan!)"):
            st.session_state.messages.append({"role": "assistant", "content": "No sitte firaatahan viäläkin lisää! Anna tulla kysymyksiä, moon valmiina!"})
            st.rerun()

# Käyttäjän syöte
if user_input := st.chat_input("Kirjoita viestisi tähän..."):
    with st.chat_message("user"): st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    if st.session_state.vitsimoodi and user_input.strip().upper() in ["K", "KYLLÄ"]:
        st.session_state.vitsimoodi = False
        vastaus = "No soot siinä oikeas, palataanpa asialinjalle ja puhutaan suomea. Miten mä voin auttaa sua digiasioos?"
    else:
        nykyiset_ohjeet = ohjeet_pohjanmaa if st.session_state.vitsimoodi else ohjeet_normaali
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": nykyiset_ohjeet}] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )
            vastaus = completion.choices[0].message.content
            
            if "Pelleilet kanssani" in vastaus or "Pohjanmaan murteella" in vastaus:
                st.session_state.vitsimoodi = True
            
            if st.session_state.vitsimoodi:
                vastaus += "\n\n*Oikeasti, palataanko asiaan? (K/E)*"
        except Exception as e:
            vastaus = "Hupsista keikkaa, joku lanka katkes matkalla. Koitetaanpa uurestaan!"

    with st.chat_message("assistant"): st.write(vastaus)
    st.session_state.messages.append({"role": "assistant", "content": vastaus})
    st.rerun()
