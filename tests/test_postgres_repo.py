"""Tests for postgres_repo helpers with no DATABASE_URL configured."""
import os
import sys
from pathlib import Path
import importlib

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_postgres_repo_no_database_url(monkeypatch):
    # Ensure DATABASE_URL is not set for this test
    monkeypatch.delenv("DATABASE_URL", raising=False)

    # Import module after env change
    import repositories.postgres_repo as repo
    importlib.reload(repo)

    # get_pool should return None when DATABASE_URL not configured
    pool = repo.get_pool()
    assert pool is None

    # get_conn and get_transactions should return None
    assert repo.get_conn() is None
    assert repo.get_transactions() is None
