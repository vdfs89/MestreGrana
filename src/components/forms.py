"""Form components with validation."""

try:
    import streamlit as st
except Exception:
    from _stubs import st

import re
from data_security import DataSecurity


def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """Validate phone format (Brazil)."""
    pattern = r'^\(\d{2}\)\s?9?\d{4}-\d{4}$'
    return re.match(pattern, phone) is not None


def validate_cpf(cpf):
    """Validate CPF format."""
    return DataSecurity().is_valid_cpf(cpf)


def render_email_input(label="Email", key="email"):
    """Render email input with validation.
    
    Args:
        label: str - Input label
        key: str - Unique key
    
    Returns:
        str - Email value or None if invalid
    """
    email = st.text_input(label, key=key)
    
    if email and not validate_email(email):
        st.error("❌ Email inválido")
        return None
    
    return email


def render_phone_input(label="Telefone", key="phone"):
    """Render phone input with validation.
    
    Args:
        label: str - Input label
        key: str - Unique key
    
    Returns:
        str - Phone value or None if invalid
    """
    phone = st.text_input(label, placeholder="(11) 99999-9999", key=key)
    
    if phone and not validate_phone(phone):
        st.error("❌ Telefone inválido. Formato: (11) 99999-9999")
        return None
    
    return phone


def render_cpf_input(label="CPF", key="cpf"):
    """Render CPF input with validation.
    
    Args:
        label: str - Input label
        key: str - Unique key
    
    Returns:
        str - CPF value or None if invalid
    """
    cpf = st.text_input(label, placeholder="123.456.789-10", key=key)
    
    if cpf and not validate_cpf(cpf):
        st.error("❌ CPF inválido")
        return None
    
    return cpf


def render_currency_input(label="Valor", key="currency"):
    """Render currency input.
    
    Args:
        label: str - Input label
        key: str - Unique key
    
    Returns:
        float - Parsed value or None
    """
    try:
        value = st.number_input(label, key=key, min_value=0.0, format="%.2f")
        return value
    except Exception as e:
        st.error(f"❌ Erro ao processar valor: {e}")
        return None


def render_date_input(label="Data", key="date"):
    """Render date input.
    
    Args:
        label: str - Input label
        key: str - Unique key
    
    Returns:
        datetime - Date value
    """
    date = st.date_input(label, key=key)
    return date


def render_contact_form():
    """Render contact form with validation.
    
    Returns:
        dict - Form data or None if invalid
    """
    st.subheader("📝 Formulário de Contato")
    
    with st.form("contact_form"):
        name = st.text_input("Nome")
        email = render_email_input("Email", key="contact_email")
        phone = render_phone_input("Telefone", key="contact_phone")
        message = st.text_area("Mensagem")
        
        submitted = st.form_submit_button("Enviar")
        
        if submitted:
            if not name or not email or not phone or not message:
                st.error("❌ Todos os campos são obrigatórios")
                return None
            
            return {
                "name": name,
                "email": email,
                "phone": phone,
                "message": message,
            }
    
    return None


def render_profile_form(initial_data=None):
    """Render user profile form.
    
    Args:
        initial_data: dict - Initial form data
    
    Returns:
        dict - Form data or None if invalid
    """
    st.subheader("👤 Perfil do Usuário")
    
    initial_data = initial_data or {}
    
    with st.form("profile_form"):
        name = st.text_input("Nome", value=initial_data.get("name", ""))
        email = render_email_input("Email", key="profile_email")
        cpf = render_cpf_input("CPF", key="profile_cpf")
        phone = render_phone_input("Telefone", key="profile_phone")
        birth_date = render_date_input("Data de Nascimento", key="profile_birth")
        
        col1, col2 = st.columns(2)
        with col1:
            risk_profile = st.selectbox(
                "Perfil de Risco",
                ["Conservador", "Moderado", "Agressivo"],
            )
        with col2:
            investment_experience = st.selectbox(
                "Experiência em Investimentos",
                ["Nenhuma", "Pouca", "Moderada", "Muita"],
            )
        
        submitted = st.form_submit_button("Salvar Perfil")
        
        if submitted:
            if not name or not email or not cpf or not phone:
                st.error("❌ Todos os campos obrigatórios devem ser preenchidos")
                return None
            
            return {
                "name": name,
                "email": email,
                "cpf": cpf,
                "phone": phone,
                "birth_date": birth_date,
                "risk_profile": risk_profile,
                "investment_experience": investment_experience,
            }
    
    return None
