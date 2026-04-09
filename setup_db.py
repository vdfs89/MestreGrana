import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


def carregar_schema() -> str:
    schema_path = Path(__file__).parent / "scripts" / "neon_schema.sql"
    if not schema_path.exists():
        raise FileNotFoundError(f"Arquivo de schema nao encontrado: {schema_path}")
    return schema_path.read_text(encoding="utf-8")


def criar_tabelas() -> None:
    load_dotenv()
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL nao encontrada no ambiente/.env")

    queries = carregar_schema()

    conn = psycopg2.connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.execute(queries)
        conn.commit()
        print("Tabelas criadas/atualizadas com sucesso no NeonDB!")
    except Exception as e:
        conn.rollback()
        print(f"Erro ao criar tabelas: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    criar_tabelas()
