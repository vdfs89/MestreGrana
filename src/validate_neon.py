"""
Script de validação e teste da conexão Neon.
Execute com: python src/validate_neon.py
"""

import sys
import os
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent))

from neon_client import get_neon_client
from dotenv import load_dotenv

load_dotenv()


def validate_neon():
    """Executa suite completa de testes Neon."""
    print("\n" + "=" * 60)
    print("🔍 VALIDAÇÃO NEON DATABASE")
    print("=" * 60 + "\n")

    # 1. Validar variáveis de ambiente
    print("1️⃣  Verificando variáveis de ambiente...")
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL não configurado")
        return False

    # Mascarar URL por segurança
    masked_url = database_url.split("@")[0] + "@***:***" if "@" in database_url else "***"
    print(f"✅ DATABASE_URL encontrado: {masked_url}")

    # 2. Inicializar cliente
    print("\n2️⃣  Inicializando cliente Neon...")
    try:
        client = get_neon_client()
        print("✅ Cliente inicializado")
    except Exception as e:
        print(f"❌ Erro ao inicializar cliente: {e}")
        return False

    # 3. Health check
    print("\n3️⃣  Executando health check...")
    health = client.health_check()
    print(f"   Connected: {health['connected']}")
    print(f"   Version: {health['version']}")
    if health.get("active_connections"):
        print(f"   Active Connections: {health['active_connections']}")
    if health.get("error"):
        print(f"   Error: {health['error']}")

    if not health["connected"]:
        return False

    # 4. Testar pool de conexões
    print("\n4️⃣  Testando pool de conexões...")
    try:
        # Faz 5 queries sequenciais para testar reutilização
        for i in range(5):
            with client.query("SELECT %s as test_number", (i + 1,)) as cursor:
                result = cursor.fetchone()
                print(f"   Query {i + 1}: ✅ {result}")
        print("✅ Pool funcionando corretamente")
    except Exception as e:
        print(f"❌ Erro no pool: {e}")
        return False

    # 5. Testar estrutura de tabelas
    print("\n5️⃣  Verificando tabelas do schema...")
    try:
        tables = client.fetch_all(
            """
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY tablename
        """
        )
        if tables:
            print(f"✅ Encontradas {len(tables)} tabelas:")
            for (table,) in tables:
                print(f"   - {table}")
        else:
            print("⚠️  Nenhuma tabela encontrada (schema vazio)")
    except Exception as e:
        print(f"❌ Erro ao listar tabelas: {e}")
        return False

    # 6. Testar transação
    print("\n6️⃣  Testando transações...")
    try:
        # Cria tabela temporária para teste
        client.execute("DROP TABLE IF EXISTS test_transaction")
        client.execute(
            "CREATE TEMP TABLE test_transaction (id SERIAL PRIMARY KEY, value TEXT)"
        )
        client.execute(
            "INSERT INTO test_transaction (value) VALUES (%s)", ("teste",)
        )
        result = client.fetch_one("SELECT COUNT(*) FROM test_transaction")
        if result and result[0] > 0:
            print(f"✅ Transação funcionando (registros inseridos: {result[0]})")
        else:
            print("❌ Falha ao inserir dados")
            return False
    except Exception as e:
        print(f"❌ Erro em transação: {e}")
        return False

    print("\n" + "=" * 60)
    print("✅ VALIDAÇÃO CONCLUÍDA COM SUCESSO")
    print("=" * 60 + "\n")
    return True


if __name__ == "__main__":
    success = validate_neon()
    sys.exit(0 if success else 1)
