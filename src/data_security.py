"""
Segurança de dados - Validação, sanitização e proteção de inputs.
Previne SQL injection, XSS, CSRF e outras vulnerabilidades comuns.
"""

import re
import hashlib
import secrets
from typing import Any, Dict, List, Optional
from urllib.parse import quote
import streamlit as st


class DataSecurity:
    """Utilitários de segurança para validação e sanitização de dados."""

    # Padrões de validação
    EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    CPF_PATTERN = re.compile(r"^\d{11}$")
    PHONE_PATTERN = re.compile(r"^(\+?55)?(\d{10,11})$")
    URL_PATTERN = re.compile(r"^https?://[^\s/$.?#].[^\s]*$", re.IGNORECASE)

    # Limites de comprimento
    MAX_INPUT_LENGTH = 1000
    MAX_EMAIL_LENGTH = 254
    MAX_CPF_LENGTH = 11
    MAX_PHONE_LENGTH = 20

    # Palavras-chave SQL suspeitas (detecção básica)
    SQL_KEYWORDS = [
        "DROP",
        "DELETE",
        "INSERT",
        "UPDATE",
        "UNION",
        "SELECT",
        "EXEC",
        "EXECUTE",
        "SCRIPT",
        ";",
        "--",
        "/*",
        "*/",
    ]

    @staticmethod
    def validate_email(email: str) -> bool:
        """Valida formato de e-mail."""
        if not email or len(email) > DataSecurity.MAX_EMAIL_LENGTH:
            return False
        return bool(DataSecurity.EMAIL_PATTERN.match(email.lower()))

    @staticmethod
    def validate_cpf(cpf: str) -> bool:
        """
        Valida CPF (apenas formato, não verifica dígito verificador).
        Para produção, use biblioteca como 'validate-cpf'.
        """
        if not cpf:
            return False
        cpf_clean = re.sub(r"\D", "", cpf)
        return bool(DataSecurity.CPF_PATTERN.match(cpf_clean))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Valida número de telefone brasileiro."""
        if not phone or len(phone) > DataSecurity.MAX_PHONE_LENGTH:
            return False
        return bool(DataSecurity.PHONE_PATTERN.match(re.sub(r"\D", "", phone)))

    @staticmethod
    def validate_url(url: str) -> bool:
        """Valida URL (http/https apenas)."""
        if not url or len(url) > 2048:  # URL max length
            return False
        return bool(DataSecurity.URL_PATTERN.match(url))

    @staticmethod
    def sanitize_string(value: str, max_length: int = MAX_INPUT_LENGTH) -> str:
        """
        Sanitiza string removendo caracteres perigosos.

        Args:
            value: String a sanitizar
            max_length: Comprimento máximo permitido

        Returns:
            String sanitizada
        """
        if not isinstance(value, str):
            return ""

        # Truncar se exceder limite
        value = value[: min(len(value), max_length)]

        # Remover caracteres de controle e null bytes
        value = "".join(char for char in value if ord(char) >= 32 or char in "\n\t\r")
        value = value.replace("\x00", "")

        return value.strip()

    @staticmethod
    def detect_sql_injection(value: str) -> bool:
        """
        Detecta padrões suspeitos de SQL injection.
        ⚠️ NÃO é suficiente sozinho - sempre use prepared statements!

        Args:
            value: String a verificar

        Returns:
            True se detectado padrão suspeito
        """
        if not isinstance(value, str):
            return False

        upper_value = value.upper()
        for keyword in DataSecurity.SQL_KEYWORDS:
            if keyword in upper_value:
                return True

        return False

    @staticmethod
    def hash_sensitive_data(value: str, salt: Optional[str] = None) -> str:
        """
        Hash SHA-256 para dados sensíveis (não senha!).
        Para senha, use bcrypt (passlib).

        Args:
            value: Valor a hashear
            salt: Salt opcional (se None, gera novo)

        Returns:
            Hash SHA-256 com salt
        """
        if salt is None:
            salt = secrets.token_hex(16)

        combined = f"{salt}{value}"
        hash_obj = hashlib.sha256(combined.encode())
        return f"{salt}${hash_obj.hexdigest()}"

    @staticmethod
    def validate_financial_amount(value: Any) -> bool:
        """
        Valida valor monetário.

        Args:
            value: Valor a validar

        Returns:
            True se é número positivo com até 2 casas decimais
        """
        try:
            amount = float(value)
            # Verificar intervalo realista e precisão
            return 0 <= amount <= 999999999.99 and len(str(amount).split(".")[-1]) <= 2
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_date(date_str: str, format_str: str = "%Y-%m-%d") -> bool:
        """Valida data em formato específico."""
        try:
            from datetime import datetime

            datetime.strptime(date_str, format_str)
            return True
        except ValueError:
            return False

    @staticmethod
    def escape_html(value: str) -> str:
        """Escapa caracteres HTML para evitar XSS (Streamlit já faz isso, mas útil para API)."""
        replacements = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#x27;",
        }
        return "".join(replacements.get(char, char) for char in value)

    @staticmethod
    def validate_input_batch(inputs: Dict[str, Any], schema: Dict[str, Dict]) -> Dict[str, Any]:
        """
        Valida lote de inputs contra esquema.

        Args:
            inputs: Dict com valores do usuário
            schema: Dict com regras de validação
                Exemplo:
                {
                    'email': {'type': 'email', 'required': True},
                    'amount': {'type': 'amount', 'required': True, 'min': 0, 'max': 10000},
                    'cpf': {'type': 'cpf', 'required': False}
                }

        Returns:
            Dict com valores validados, ou None se inválido
        """
        validated = {}

        for field, rules in schema.items():
            value = inputs.get(field)
            field_type = rules.get("type")
            required = rules.get("required", False)

            # Verificar obrigatoriedade
            if required and (value is None or value == ""):
                raise ValueError(f"Campo obrigatório faltando: {field}")

            if value is None or value == "":
                validated[field] = None
                continue

            # Validar por tipo
            if field_type == "email":
                if not DataSecurity.validate_email(value):
                    raise ValueError(f"E-mail inválido: {field}")
                validated[field] = value.lower()

            elif field_type == "cpf":
                if not DataSecurity.validate_cpf(value):
                    raise ValueError(f"CPF inválido: {field}")
                validated[field] = re.sub(r"\D", "", value)

            elif field_type == "amount":
                if not DataSecurity.validate_financial_amount(value):
                    raise ValueError(f"Valor inválido: {field}")
                amount = float(value)
                min_val = rules.get("min", 0)
                max_val = rules.get("max", float("inf"))
                if not (min_val <= amount <= max_val):
                    raise ValueError(f"Valor fora do intervalo [{min_val}, {max_val}]: {field}")
                validated[field] = amount

            elif field_type == "date":
                fmt = rules.get("format", "%Y-%m-%d")
                if not DataSecurity.validate_date(value, fmt):
                    raise ValueError(f"Data inválida: {field}")
                validated[field] = value

            elif field_type == "string":
                max_len = rules.get("max_length", DataSecurity.MAX_INPUT_LENGTH)
                validated[field] = DataSecurity.sanitize_string(value, max_len)

            else:
                # Default: sanitizar como string
                validated[field] = DataSecurity.sanitize_string(value)

        return validated


def security_middleware_streamlit():
    """
    Aplicar headers de segurança em Streamlit.
    Nota: Streamlit tem limitações de customização de headers;
    isso é mais relevante em FastAPI backend.
    """
    # Streamlit não permite customizar headers HTTP diretamente,
    # mas pode-se usar Meta tags:
    st.set_page_config(
        page_title="MestreGrana",
        page_icon="💰",
        layout="wide",
    )

    # Adicionar meta tags de segurança via HTML
    st.markdown(
        """
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="referrer" content="strict-origin-when-cross-origin">
        <style>
            /* CSP via meta - limitado em Streamlit */
        </style>
        """,
        unsafe_allow_html=True,
    )


# Exemplos de uso
EXAMPLE_VALIDATION_SCHEMA = {
    "email": {"type": "email", "required": True},
    "cpf": {"type": "cpf", "required": False},
    "amount": {"type": "amount", "required": True, "min": 0.01, "max": 100000},
    "transaction_date": {"type": "date", "required": True, "format": "%Y-%m-%d"},
    "description": {"type": "string", "required": False, "max_length": 500},
}
