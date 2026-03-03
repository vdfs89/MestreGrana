import streamlit as st
from config import get_keys
from agente import FinanceForge
from gtts import gTTS
import base64

st.set_page_config(page_title="FinanceForge", page_icon="💸")
keys = get_keys()
ff = FinanceForge(keys)

def tocar_audio(texto):
    texto_limpo = texto.replace("**", "").replace("#", "")
    tts = gTTS(text=texto_limpo, lang='pt')
    tts.save("audio.mp3")
    with open("audio.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

st.title("💸 FinanceForge")
st.info("Agente Financeiro Proativo com Failover Ativo.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if prompt := st.chat_input("Como estão minhas metas hoje?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.spinner("Consultando sua base de dados..."):
        resposta, provedor = ff.responder(st.session_state.messages)
    with st.chat_message("assistant"):
        st.markdown(f"**[{provedor}]** {resposta}")
        st.session_state.messages.append({"role": "assistant", "content": resposta})
        tocar_audio(resposta)
