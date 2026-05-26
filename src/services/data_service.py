try:
    import streamlit as st
except Exception:
    from _stubs import st

import json
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


@st.cache_data(ttl=600)
def load_perfil():
    path = DATA_DIR / "perfil_investidor.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


@st.cache_data(ttl=600)
def load_produtos():
    path = DATA_DIR / "produtos_financeiros.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


@st.cache_data(ttl=300)
def load_transacoes():
    path = DATA_DIR / "transacoes.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data(ttl=300)
def load_historico():
    path = DATA_DIR / "historico_atendimento.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)
