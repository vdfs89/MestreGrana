"""
Gerenciamento de consentimento de cookies e dados (LGPD).
Implementa banner de consentimento, armazenamento e conformidade.
"""

import streamlit as st
import json
from datetime import datetime
from typing import Dict, Optional


class CookieConsent:
    """Gerenciador de consentimento de cookies e dados."""

    # Chave para session_state (Streamlit)
    SESSION_KEY = "cookie_consent"
    CONSENT_COOKIE_NAME = "mestregrana_consent"

    @staticmethod
    def get_consent_from_session() -> Optional[Dict]:
        """Retorna consentimento armazenado em session_state."""
        return st.session_state.get(CookieConsent.SESSION_KEY)

    @staticmethod
    def set_consent(
        analytics: bool = False,
        necessary: bool = True,
        preferences: bool = False,
        timestamp: Optional[str] = None,
    ):
        """
        Armazena consentimento em session_state.

        Args:
            analytics: Permitir Google Analytics, Groq/OpenAI logging
            necessary: Cookies técnicos (sessão, autenticação) - sempre True
            preferences: Preferências do usuário (dark mode, etc)
            timestamp: ISO timestamp (auto-preenchido se None)
        """
        consent = {
            "necessary": necessary,
            "analytics": analytics,
            "preferences": preferences,
            "timestamp": timestamp or datetime.now().isoformat(),
            "version": "1.0",  # Para rastreabilidade de versão de política
        }
        st.session_state[CookieConsent.SESSION_KEY] = consent
        return consent

    @staticmethod
    def save_consent_to_db(user_id: str, client) -> bool:
        """
        Salva consentimento no banco para auditoria LGPD.

        Args:
            user_id: ID do usuário
            client: NeonClient

        Returns:
            True se sucesso
        """
        consent = CookieConsent.get_consent_from_session()
        if not consent:
            return False

        try:
            consent_json = json.dumps(consent)
            success = client.execute(
                """
                INSERT INTO user_consents (user_id, consent_type, consent_data, consented_at, ip_address)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (user_id, consent_type) DO UPDATE
                SET consent_data = EXCLUDED.consent_data, consented_at = EXCLUDED.consented_at
                """,
                (user_id, "cookies_analytics", consent_json, consent["timestamp"], "tracked"),
            )
            return success
        except Exception as e:
            st.warning(f"⚠️ Erro ao salvar consentimento: {e}")
            return False

    @staticmethod
    def render_consent_banner():
        """
        Renderiza banner de consentimento (LGPD-compliant).
        Chamado no topo de cada página.
        """
        existing_consent = CookieConsent.get_consent_from_session()

        # Se usuário já consentiu, não mostrar novamente
        if existing_consent:
            return

        st.markdown("---")
        st.warning("🍪 **Consentimento de Cookies e Dados**")

        col1, col2, col3 = st.columns(3)

        with col1:
            analytics = st.checkbox(
                "📊 Analytics (opcional)",
                value=False,
                help="Permitir coleta de uso anônimo (Google Analytics, Groq, OpenAI)",
            )

        with col2:
            preferences = st.checkbox(
                "⚙️ Preferências (opcional)",
                value=False,
                help="Lembrar configurações do usuário",
            )

        with col3:
            necessary = st.checkbox(
                "✅ Necessários (obrigatório)",
                value=True,
                disabled=True,
                help="Sessão, autenticação, funcionalidades básicas",
            )

        st.info(
            "🔐 Leia nossa [Política de Cookies e Privacidade →](docs/TERMO_DE_USO.md) "
            "para detalhes sobre como seus dados são tratados."
        )

        col_accept, col_reject = st.columns(2)

        with col_accept:
            if st.button("✅ Aceitar Selecionados", use_container_width=True):
                CookieConsent.set_consent(
                    analytics=analytics,
                    necessary=necessary,
                    preferences=preferences,
                )
                st.rerun()

        with col_reject:
            if st.button("❌ Apenas Necessários", use_container_width=True):
                CookieConsent.set_consent(
                    analytics=False,
                    necessary=True,
                    preferences=False,
                )
                st.rerun()

        st.markdown("---")

    @staticmethod
    def can_track_analytics() -> bool:
        """Retorna True se usuário consentiu com analytics."""
        consent = CookieConsent.get_consent_from_session()
        return consent is not None and consent.get("analytics", False)

    @staticmethod
    def can_store_preferences() -> bool:
        """Retorna True se usuário consentiu com preferências."""
        consent = CookieConsent.get_consent_from_session()
        return consent is not None and consent.get("preferences", False)

    @staticmethod
    def get_consent_status() -> str:
        """Retorna string com status de consentimento para exibição."""
        consent = CookieConsent.get_consent_from_session()
        if not consent:
            return "⚪ Não consentido"

        parts = []
        if consent.get("necessary"):
            parts.append("Necessários")
        if consent.get("analytics"):
            parts.append("Analytics")
        if consent.get("preferences"):
            parts.append("Preferências")

        return "🟢 " + ", ".join(parts)


# Exemplo de uso integrado em streamlit.py:
"""
import streamlit as st
from cookies_consent import CookieConsent

st.set_page_config(page_title="MestreGrana", layout="wide")

# Renderizar banner de consentimento (chamado ANTES de enviar dados)
CookieConsent.render_consent_banner()

# Depois disso, o resto da app...

# Se quiser enviar dados para analytics:
if CookieConsent.can_track_analytics():
    # enviar para Groq/Google/OpenAI
    pass

# Salvar consentimento ao fazer login:
if user_logged_in and CookieConsent.get_consent_from_session():
    CookieConsent.save_consent_to_db(user_id, neon_client)

# Exibir status em sidebar:
st.sidebar.metric("Consentimento", CookieConsent.get_consent_status())
"""
