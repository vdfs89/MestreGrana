"""Streamlit session state management."""

try:
    import streamlit as st
except Exception:
    from _stubs import st


def init_session_state():
    """Initialize session state with default values."""
    defaults = {
        "messages": [],
        "current_page": "💬 Assistente",
        "user_name": None,
        "theme": "dark",
        "language": "pt-br",
        "dados_carregados": False,
        "perfil": None,
        "produtos": None,
        "transacoes": None,
        "historico": None,
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_state(key, default=None):
    """Get value from session state."""
    if hasattr(st, "session_state"):
        return st.session_state.get(key, default)
    return default


def set_state(key, value):
    """Set value in session state."""
    if hasattr(st, "session_state"):
        st.session_state[key] = value


def add_message(role, content, metadata=None):
    """Add message to chat history.
    
    Args:
        role: 'user' or 'assistant'
        content: str - Message content
        metadata: dict - Additional metadata
    """
    message = {
        "role": role,
        "content": content,
    }
    if metadata:
        message.update(metadata)
    
    messages = get_state("messages", [])
    messages.append(message)
    set_state("messages", messages)


def get_messages():
    """Get all messages from chat history."""
    return get_state("messages", [])


def clear_messages():
    """Clear chat history."""
    set_state("messages", [])


def set_page(page_name):
    """Set current page."""
    set_state("current_page", page_name)


def get_page():
    """Get current page."""
    return get_state("current_page", "💬 Assistente")
