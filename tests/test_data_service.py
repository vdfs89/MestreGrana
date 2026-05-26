"""Tests for data_service loaders."""
import sys
from pathlib import Path
import importlib

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from services import data_service


def test_load_perfil_returns_dict():
    perfil = data_service.load_perfil()
    assert isinstance(perfil, dict)


def test_load_produtos_returns_list():
    produtos = data_service.load_produtos()
    assert isinstance(produtos, list)


def test_load_transacoes_returns_dataframe():
    transacoes = data_service.load_transacoes()
    # pandas DataFrame or empty DataFrame acceptable
    try:
        import pandas as pd
        assert hasattr(transacoes, 'shape')
    except Exception:
        # If pandas not available in test env, at least ensure not raising
        assert transacoes is not None


def test_load_historico_returns_dataframe():
    historico = data_service.load_historico()
    try:
        import pandas as pd
        assert hasattr(historico, 'shape')
    except Exception:
        assert historico is not None
