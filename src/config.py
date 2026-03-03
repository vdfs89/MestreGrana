import streamlit as st

def get_keys():
    try:
        return {
            "GROQ": st.secrets["GROQ_API_KEY"],
            "GEMINI": st.secrets["GEMINI_API_KEY"],
            "OPENAI": st.secrets["OPENAI_API_KEY"]
        }
    except Exception:
        st.error("Erro: Chaves de API não configuradas no st.secrets.")
        st.stop()
