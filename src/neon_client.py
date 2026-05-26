"""
Neon Database Client com connection pooling, health check e retry logic.
Centraliza toda integração com Neon (PostgreSQL) para MestreGrana.
"""

import os
import logging
import time
from typing import Optional, Generator, Dict, Any
from contextlib import contextmanager
from psycopg2 import pool, sql, OperationalError, DatabaseError
from psycopg2.extensions import connection as psycopg2_connection
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class NeonClient:
    """
    Cliente para Neon Database com pooling, validação e retry logic.
    
    Features:
    - Connection pooling (reutilização de conexões)
    - Health check automático
    - Retry com backoff exponencial
    - Context manager para queries seguras
    - Logging detalhado
    """

    def __init__(
        self,
        database_url: Optional[str] = None,
        min_connections: int = 2,
        max_connections: int = 10,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """
        Inicializa cliente Neon.
        
        Args:
            database_url: Connection string (DATABASE_URL). Se None, busca em ENV.
            min_connections: Mínimo de conexões no pool
            max_connections: Máximo de conexões no pool
            max_retries: Máximo de tentativas de reconexão
            retry_delay: Delay inicial (segundos) para retry com backoff
        """
        self.database_url = database_url or os.environ.get("DATABASE_URL")
        if not self.database_url:
            raise ValueError(
                "DATABASE_URL não configurado. "
                "Configure em .env ou passe como argumento."
            )

        self.min_connections = min_connections
        self.max_connections = max_connections
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._pool: Optional[pool.SimpleConnectionPool] = None
        self._initialized = False

    def connect(self) -> bool:
        """
        Cria pool de conexões.
        
        Returns:
            True se sucesso, False caso contrário.
        """
        if self._initialized:
            return True

        try:
            self._pool = pool.SimpleConnectionPool(
                self.min_connections,
                self.max_connections,
                self.database_url,
                # Timeout de 10 segundos para conexão
                connect_timeout=10,
                # Reutilizar conexão após desconexão
                keepalives=1,
                keepalives_idle=30,
                keepalives_interval=10,
                keepalives_count=5,
            )
            self._initialized = True
            logger.info(
                f"✅ Pool Neon inicializado: {self.min_connections}-{self.max_connections} conexões"
            )
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao criar pool Neon: {e}")
            self._initialized = False
            return False

    def validate_connection(self) -> bool:
        """
        Valida conexão com Neon executando query simples.
        
        Returns:
            True se conexão válida, False caso contrário.
        """
        if not self._initialized and not self.connect():
            return False

        try:
            with self.query("SELECT 1") as cursor:
                cursor.fetchone()
            logger.debug("✅ Validação Neon: OK")
            return True
        except Exception as e:
            logger.warning(f"⚠️ Validação Neon falhou: {e}")
            return False

    def health_check(self) -> Dict[str, Any]:
        """
        Executa health check detalhado da conexão Neon.
        
        Returns:
            Dicionário com status e informações da conexão.
        """
        status = {
            "connected": False,
            "pool_initialized": self._initialized,
            "version": None,
            "error": None,
        }

        if not self._initialized and not self.connect():
            status["error"] = "Não conseguiu criar pool de conexões"
            return status

        try:
            with self.query("SELECT version()") as cursor:
                version = cursor.fetchone()
                status["version"] = version[0] if version else "Desconhecido"

            with self.query(
                "SELECT COUNT(*) FROM pg_stat_activity WHERE state = 'active'"
            ) as cursor:
                active_connections = cursor.fetchone()[0]
                status["active_connections"] = active_connections

            status["connected"] = True
            logger.info("✅ Health check Neon: PASS")
        except Exception as e:
            status["error"] = str(e)
            logger.error(f"❌ Health check falhou: {e}")

        return status

    @contextmanager
    def query(self, sql_query: str, params: tuple = None, max_retries: int = None):
        """
        Context manager seguro para executar queries com retry automático.
        
        Usage:
            with client.query("SELECT * FROM users WHERE id = %s", (123,)) as cursor:
                row = cursor.fetchone()
        
        Args:
            sql_query: Query SQL (com %s para parâmetros)
            params: Tupla de parâmetros para a query
            max_retries: Override do max_retries padrão
        
        Yields:
            psycopg2 cursor
        """
        if not self._initialized and not self.connect():
            raise RuntimeError("Não conseguiu conectar ao Neon")

        max_retries = max_retries or self.max_retries
        attempt = 0
        last_error = None

        while attempt <= max_retries:
            conn = None
            try:
                conn = self._pool.getconn()
                conn.autocommit = False  # Explícito: usar transações

                with conn.cursor() as cursor:
                    cursor.execute(sql_query, params or ())
                    yield cursor
                    conn.commit()
                    return

            except (OperationalError, DatabaseError) as e:
                # Erro de conexão/banco: tenta reconectar
                if conn:
                    try:
                        conn.rollback()
                    except:
                        pass
                last_error = e
                attempt += 1

                if attempt <= max_retries:
                    delay = self.retry_delay * (2 ** (attempt - 1))  # Backoff exponencial
                    logger.warning(
                        f"⚠️ Retry {attempt}/{max_retries} em {delay:.1f}s: {e}"
                    )
                    time.sleep(delay)
                else:
                    logger.error(f"❌ Query falhou após {max_retries} tentativas: {e}")
                    raise

            except Exception as e:
                # Erro inesperado: não tenta retry
                logger.error(f"❌ Erro inesperado na query: {e}")
                if conn:
                    try:
                        conn.rollback()
                    except:
                        pass
                raise

            finally:
                if conn:
                    try:
                        self._pool.putconn(conn)
                    except:
                        pass

        raise last_error or RuntimeError("Erro desconhecido na query")

    def fetch_one(self, sql_query: str, params: tuple = None) -> Optional[tuple]:
        """Executa query e retorna 1 linha."""
        try:
            with self.query(sql_query, params) as cursor:
                return cursor.fetchone()
        except Exception as e:
            logger.error(f"fetch_one falhou: {e}")
            return None

    def fetch_all(self, sql_query: str, params: tuple = None) -> list:
        """Executa query e retorna todas as linhas."""
        try:
            with self.query(sql_query, params) as cursor:
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"fetch_all falhou: {e}")
            return []

    def fetch_dataframe(self, sql_query: str, params: tuple = None):
        """Executa query e retorna pandas DataFrame."""
        try:
            import pandas as pd

            with self.query(sql_query, params) as cursor:
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                return pd.DataFrame(rows, columns=columns)
        except ImportError:
            logger.error("pandas não instalado para fetch_dataframe")
            return None
        except Exception as e:
            logger.error(f"fetch_dataframe falhou: {e}")
            return None

    def execute(self, sql_query: str, params: tuple = None) -> bool:
        """Executa query sem retornar dados (INSERT/UPDATE/DELETE)."""
        try:
            with self.query(sql_query, params) as cursor:
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"execute falhou: {e}")
            return False

    def close(self):
        """Fecha pool de conexões."""
        if self._pool:
            self._pool.closeall()
            self._pool = None
            self._initialized = False
            logger.info("✅ Pool Neon fechado")

    def __enter__(self):
        """Context manager support."""
        if not self.connect():
            raise RuntimeError("Não conseguiu conectar ao Neon")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager support."""
        self.close()


# Cliente global singleton para Streamlit cache
_neon_client: Optional[NeonClient] = None


def get_neon_client(database_url: Optional[str] = None) -> NeonClient:
    """
    Retorna cliente Neon singleton (reutiliza pool entre chamadas).
    
    Args:
        database_url: DATABASE_URL (opcional, usa ENV se não passar)
    
    Returns:
        NeonClient conectado
    """
    global _neon_client

    if _neon_client is None:
        _neon_client = NeonClient(database_url)
        _neon_client.connect()

    return _neon_client
