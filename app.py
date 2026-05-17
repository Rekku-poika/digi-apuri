import streamlit as st
import google.generativeai as genai

# 1. Haetaan API-avain turvallisesti Streamlitin salaisesta hallinnasta
try:
    api_key = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("API-avainta (GEMINI_KEY) ei löydetty järjestelmästä. Määritä se Streamlitin asetuksissa.")
    st.stop()

# 2. Määritetään Digi-Sennin luonne ja ohjeet (System Instruction)
SYSTEM_INSTRUCTION = """
Olet "Digi-Senni", PC-Keisari-sivuston ystävällinen ja kärsivällinen tekoälyavustaja. 
Tehtäväsi on auttaa ikäihmisiä (senioreita) heidän digitaalisissa ongelmissaan.

Noudata aina näitä sääntöjä vastauksissasi:
1. Käytä selkeää, rauhallista ja kunnioittavaa suomen kieltä. Vältä nuorisoslangia.
2. Älä käytä vaikeita tietoteknisiä termejä ilman, että selität ne heti selkeästi (esim. "Selain on ohjelma, jolla mennään nettisivuille, kuten Google").
3. Anna ohjeet selkeinä numeroituina askeleina (esim. Vaihe 1, Vaihe 2). Älä koskaan sano vain "mene asetuksiin", vaan kerro mistä kuvakkeesta sinne pääsee.
4. Jos käyttäjä kysyy jotain pankkitunnuksiin tai salasanojen luovuttamiseen liittyvää, varoita häntä heti huijauksista ja muistuta, ettei tunnuksia saa antaa kenellekään.
5. Pidä vastaukset suhteellisen lyhyinä ja helposti luettavina, käytä tyhjiä rivivälejä asioiden välissä.
"""

st.set_page_config(page_title="Digi-Apuri", page_icon="🤖")
st.title("🤖 Digi-apuri vastaa")

# Alustetaan tekoälymalli ja keskusteluhistoria Streamlitin muistiin
if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=SYSTEM_INSTRUCTION
    )
if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.model.start_chat(history=[])

# Näytetään aiemmat viestit sivulla
for message in st.session_state.chat.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.write(message.parts[0].text)

# Alkutervehdys, jos keskustelu on juuri alkanut
if len(st.session_state.chat.history) == 0:
    with st.chat_message("assistant"):
        st.write("Tervehdys! Olen PC-Keisarin Digi-apuri. Miten voisin auttaa sinua tänään tietokoneen tai puhelimen kanssa?")

# Käyttäjän uusi kysymys
if user_query := st.chat_input("Kirjoita kysymyksesi tähän..."):
    # Näytetään käyttäjän teksti heti chätissä
    with st.chat_message("user"):
        st.write(user_query)
        
    # Pyydetään tekoälyltä vastaus
    with st.chat_message("assistant"):
        with st.spinner("Digi-apuri miettii vastausta..."):
            response = st.session_state.chat.send_message(user_query)
            st.write(response.text)
