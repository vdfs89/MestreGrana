# Integração Neon - Guia Técnico

## 📋 Visão Geral

O MestreGrana agora usa um **cliente Neon robusto** com:

✅ **Connection Pooling** - Reutilização eficiente de conexões (2-10 conexões por padrão)  
✅ **Health Check** - Validação automática de conexão  
✅ **Retry Logic** - Reconexão automática com backoff exponencial (até 3 tentativas)  
✅ **Context Manager** - Gerenciamento seguro de transações  
✅ **Logging Detalhado** - Rastreamento de erros e performance  

## 🚀 Quick Start

### 1. Validar Conexão Neon

```bash
# Execute o script de validação
python src/validate_neon.py
```

Output esperado:
```
============================================================
🔍 VALIDAÇÃO NEON DATABASE
============================================================

1️⃣  Verificando variáveis de ambiente...
✅ DATABASE_URL encontrado: postgresql@***:***

2️⃣  Inicializando cliente Neon...
✅ Cliente inicializado

3️⃣  Executando health check...
   Connected: True
   Version: PostgreSQL 15.x...
   Active Connections: 2

4️⃣  Testando pool de conexões...
   Query 1: ✅ (1,)
   ...

✅ VALIDAÇÃO CONCLUÍDA COM SUCESSO
```

### 2. Usar no Streamlit

```python
from config import get_neon_database

# Obter cliente (Streamlit faz cache automático)
client = get_neon_database()

# Query simples
users = client.fetch_all("SELECT * FROM users LIMIT 10")

# Query com parâmetros (SQL injection safe)
user = client.fetch_one(
    "SELECT * FROM users WHERE id = %s",
    (123,)
)

# Retornar como DataFrame
df = client.fetch_dataframe(
    "SELECT * FROM transactions WHERE user_id = %s",
    (123,)
)

# Inserir/Atualizar (sem retornar dados)
success = client.execute(
    "INSERT INTO transactions (user_id, amount) VALUES (%s, %s)",
    (123, 99.99)
)
```

## 🏗️ Arquitetura

### `src/neon_client.py` - Cliente Principal

| Método | Descrição | Exemplo |
|--------|-----------|---------|
| `connect()` | Cria pool de conexões | `client.connect()` |
| `health_check()` | Valida saúde do banco | `status = client.health_check()` |
| `validate_connection()` | Query rápida de validação | `if client.validate_connection():` |
| `query()` | Context manager para queries | `with client.query(sql) as cur:` |
| `fetch_one(sql, params)` | Retorna 1 linha | `user = client.fetch_one(...)` |
| `fetch_all(sql, params)` | Retorna todas as linhas | `users = client.fetch_all(...)` |
| `fetch_dataframe(sql, params)` | Retorna pandas DataFrame | `df = client.fetch_dataframe(...)` |
| `execute(sql, params)` | INSERT/UPDATE/DELETE | `client.execute(...)` |
| `close()` | Fecha pool | `client.close()` |

### `src/config.py` - Centralização de Configurações

- `get_keys()` - Obtém chaves de API (st.secrets ou .env)
- `get_neon_database()` - Cliente Neon cached pelo Streamlit
- `check_neon_health()` - Status para exibição em sidebar

### `src/validate_neon.py` - Validação e Testes

Script standalone que testa:
1. Variáveis de ambiente
2. Inicialização do cliente
3. Health check
4. Pool de conexões
5. Estrutura de tabelas
6. Transações

## 🔧 Configuração

### Variáveis de Ambiente Necessárias

```bash
# .env (desenvolvimento local)
DATABASE_URL=postgresql://user:password@ep-xxxx.neondb.com/dbname

# Streamlit Cloud: adicione em Settings → Secrets
GROQ_API_KEY=...
GEMINI_API_KEY=...
OPENAI_API_KEY=...
MONGODB_ATLAS_URI=...
```

### Pool de Conexões (Customização)

```python
from neon_client import NeonClient

# Padrão: 2-10 conexões, 3 retries, 1s delay
client = NeonClient()

# Customizado para alta concorrência
client = NeonClient(
    min_connections=5,
    max_connections=20,
    max_retries=5,
    retry_delay=0.5
)
```

## ⚡ Performance e Boas Práticas

### ✅ Faça

```python
# 1. Usar context manager para limpeza automática
with client.query("SELECT * FROM users") as cursor:
    users = cursor.fetchall()

# 2. Usar parâmetros para evitar SQL injection
client.fetch_one(
    "SELECT * FROM users WHERE email = %s",
    (email,)  # ← seguro!
)

# 3. Usar fetch_dataframe para análises
df = client.fetch_dataframe("SELECT * FROM transactions")
df.groupby("category").sum()

# 4. Aplicar filtros no SQL (não em Python)
# ❌ LENTO: carregar 100k linhas
users = client.fetch_all("SELECT * FROM users")
filtered = [u for u in users if u[2] > 100]

# ✅ RÁPIDO: filtrar no banco
users = client.fetch_all("SELECT * FROM users WHERE balance > %s", (100,))
```

### ❌ Não Faça

```python
# ❌ SQL concatenação (injection risk)
query = f"SELECT * FROM users WHERE id = {user_id}"

# ❌ Múltiplas conexões
conn1 = connect()
conn2 = connect()  # desperdício de pool

# ❌ Carregar tudo e filtrar em Python
all_data = client.fetch_all("SELECT * FROM huge_table")
filtered = [row for row in all_data if row[5] == "value"]
```

## 🔍 Debug e Logs

### Ativar Logging Detalhado

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("neon_client")

# Agora verá logs como:
# ✅ Pool Neon inicializado: 2-10 conexões
# ⚠️ Retry 1/3 em 1.0s: connection timeout
```

### Health Check em Tempo Real

```python
client = get_neon_database()
health = client.health_check()

print(f"Conectado: {health['connected']}")
print(f"Versão: {health['version']}")
print(f"Conexões ativas: {health.get('active_connections', 'N/A')}")
print(f"Erro: {health.get('error', 'Nenhum')}")
```

## 🛡️ Tratamento de Erros

O cliente retira automaticamente em caso de:
- **Timeout de conexão** (10s por padrão)
- **Desconexão inesperada** (reconnect automático)
- **Query timeout** (Neon define 30s)

```python
try:
    result = client.fetch_one("SELECT * FROM users WHERE id = %s", (999,))
except Exception as e:
    st.error(f"Erro após 3 retries: {e}")
```

## 📊 Monitoramento em Produção

### Sidebar Health Dashboard

```python
from config import check_neon_health

st.sidebar.metric("Neon Status", check_neon_health())
```

### Alertas Recomendados (Neon Console)

- Conexões ativas > 15
- Query time > 5 segundos
- Storage > 80% quota

## 🚨 Troubleshooting

| Problema | Solução |
|----------|---------|
| `DATABASE_URL not found` | Configure em `.env` ou `st.secrets` |
| `connection timeout` | Valide DATABASE_URL, firewall, Network |
| `pool exhausted` | Aumente `max_connections` ou reduza taxa de requisições |
| `too many connections` | Reduza `min_connections` ou aumente timeout |
| `query timeout` | Use `LIMIT` e índices, contacte Neon support |

## 📚 Referências

- [Neon Docs](https://neon.tech/docs)
- [psycopg2 Pool](https://www.psycopg.org/psycopg2/docs/pool.html)
- [PostgreSQL Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)

---

**Mantido em**: `docs/04-neon-integration.md`  
**Último atualizado**: maio 2026
