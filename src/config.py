try:
    import streamlit as st
except Exception:
    from _stubs import st
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


def get_required_env(key: str):
    """Retorna variável de ambiente obrigatória ou levanta KeyError se ausente."""
    try:
        # Prioriza st.secrets quando disponível (Streamlit Cloud)
        value = None
        try:
            value = st.secrets.get(key)
        except Exception:
            value = None

        if value:
            return value

        # Fallback para variáveis de ambiente locais
        if key in os.environ:
            return os.environ[key]

        # Não encontrada
        raise KeyError(f"Required environment variable '{key}' is missing")
    except KeyError:
        raise
    except Exception:
        raise KeyError(f"Required environment variable '{key}' is missing")


def get_optional_env(key: str, default=None):
    """Retorna variável de ambiente opcional, ou `default` se ausente."""
    try:
        try:
            value = st.secrets.get(key)
        except Exception:
            value = None

        if value is not None:
            return value
        return os.environ.get(key, default)
    except Exception:
        return os.environ.get(key, default)


def validate_env_variable(key: str):
    """Valida presença de variável de ambiente. Retorna True ou valor quando presente."""
    try:
        val = get_optional_env(key)
        if val is None or val == "":
            raise KeyError(f"Environment variable '{key}' is missing or empty")
        return val
    except KeyError:
        raise
    except Exception:
        return None
