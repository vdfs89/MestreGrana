"""LLM client utilities with retry and fallback strategy."""

try:
    import streamlit as st
except Exception:
    from _stubs import st

import os
from dotenv import load_dotenv
import time

load_dotenv()


def get_secret_or_env(key):
    """Get secret from Streamlit or environment."""
    try:
        return st.secrets[key]
    except Exception:
        return os.environ.get(key)


@st.cache_resource
def get_groq_client():
    """Initialize Groq client with lazy import."""
    try:
        from groq import Groq
        api_key = get_secret_or_env("GROQ_API_KEY")
        if not api_key:
            return None
        return Groq(api_key=api_key)
    except ImportError:
        return None


@st.cache_resource
def get_gemini_client():
    """Initialize Gemini client with lazy import."""
    try:
        import google.generativeai as genai
        api_key = get_secret_or_env("GEMINI_API_KEY")
        if not api_key:
            return None
        genai.configure(api_key=api_key)
        return genai
    except ImportError:
        return None


@st.cache_resource
def get_openai_client():
    """Initialize OpenAI client with lazy import."""
    try:
        from openai import OpenAI
        api_key = get_secret_or_env("OPENAI_API_KEY")
        if not api_key:
            return None
        return OpenAI(api_key=api_key)
    except ImportError:
        return None


def call_llm_with_retry(
    prompt,
    model="groq",
    max_retries=3,
    timeout=30,
    temperature=0.7
):
    """Call LLM with retry logic and fallback.

    Args:
        prompt: str - The prompt to send
        model: str - 'groq', 'gemini', or 'openai'
        max_retries: int - Number of retries (default 3)
        timeout: int - Timeout in seconds
        temperature: float - Temperature for generation

    Returns:
        str - Response text or None if failed
    """
    for attempt in range(max_retries):
        try:
            if model == "groq":
                client = get_groq_client()
                if not client:
                    continue
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=500,
                    timeout=timeout
                )
                return response.choices[0].message.content

            elif model == "gemini":
                client = get_gemini_client()
                if not client:
                    continue
                response = client.GenerativeModel("gemini-2.5-flash").generate_content(prompt)
                return response.text

            elif model == "openai":
                client = get_openai_client()
                if not client:
                    continue
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=500,
                    timeout=timeout
                )
                return response.choices[0].message.content

        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                st.warning(f"Tentativa {attempt + 1} falhou. Retrying em {wait_time}s...")
                time.sleep(wait_time)
            else:
                st.error(f"❌ Falha ao chamar {model}: {str(e)[:100]}")

    return None


def call_llm_with_fallback(prompt, models=None, temperature=0.7):
    """Call LLM with fallback chain.

    Args:
        prompt: str - The prompt
        models: list - Order of models to try (default: ['groq', 'gemini', 'openai'])
        temperature: float - Temperature

    Returns:
        str - Response from first successful model or None
    """
    if models is None:
        models = ["groq", "gemini", "openai"]

    for model in models:
        response = call_llm_with_retry(
            prompt,
            model=model,
            max_retries=1,
            temperature=temperature
        )
        if response:
            return response

    return None
