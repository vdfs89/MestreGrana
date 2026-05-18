import streamlit as st
import os
from dotenv import load_dotenv

# Carrega variáveis do .env (em desenvolvimento local)
load_dotenv()


def get_keys():
    """Retorna chaves de API (st.secrets em produção, ENV em dev)."""
    try:
        return {
            "GROQ": st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY"),
            "GEMINI": st.secrets.get("GEMINI_API_KEY")
            or os.environ.get("GEMINI_API_KEY"),
            "OPENAI": st.secrets.get("OPENAI_API_KEY")
            or os.environ.get("OPENAI_API_KEY"),
        }
    except Exception:
        st.error("Erro: Chaves de API não configuradas em st.secrets ou .env")
        st.stop()


@st.cache_resource
def get_neon_database():
    """
    Retorna cliente Neon com pooling e health check.
    Cached em Streamlit para reutilização entre sessions.
    """
    from neon_client import get_neon_client

    try:
        client = get_neon_client()
        if not client.validate_connection():
            st.error("❌ Falha ao conectar ao Neon Database")
            st.stop()
        return client
    except Exception as e:
        st.error(f"❌ Erro ao inicializar Neon: {e}")
        st.stop()


def check_neon_health():
    """Retorna status health check do Neon para exibição em sidebar."""
    try:
        client = get_neon_database()
        health = client.health_check()
        
        if health["connected"]:
            status = f"🟢 Online - {health['version'][:50]}..."
        else:
            status = f"🔴 Offline - {health.get('error', 'Erro desconhecido')}"
        
        return status
    except Exception as e:
        return f"🟠 Erro - {str(e)[:30]}"
