# Segurança de Dados - Guia Completo

## 🔐 Visão Geral

O MestreGrana implementa múltiplas camadas de segurança para proteger dados financeiros:

✅ **Validação de entrada** - Previne SQL injection, XSS  
✅ **Sanitização** - Remove caracteres perigosos  
✅ **Criptografia em trânsito** - TLS/HTTPS obrigatório  
✅ **Proteção de secrets** - Variáveis de ambiente seguras  
✅ **Auditoria** - Log de todas as alterações  
✅ **Conformidade LGPD** - Consentimento e retenção  

---

## 🚀 Quick Start - Validar Inputs

### 1. Validação Individual

```python
from data_security import DataSecurity

# E-mail
if DataSecurity.validate_email(user_email):
    st.success("✅ E-mail válido")
else:
    st.error("❌ E-mail inválido")

# CPF
if DataSecurity.validate_cpf(user_cpf):
    st.success("✅ CPF válido")
else:
    st.error("❌ CPF inválido")

# Valor monetário
if DataSecurity.validate_financial_amount(amount):
    st.success("✅ Valor válido")
else:
    st.error("❌ Valor inválido")
```

### 2. Validação em Lote (Recomendado)

```python
from data_security import DataSecurity, EXAMPLE_VALIDATION_SCHEMA

# Form do usuário
email = st.text_input("E-mail")
cpf = st.text_input("CPF")
amount = st.number_input("Valor")

if st.button("Enviar"):
    try:
        # Validar tudo de uma vez
        validated = DataSecurity.validate_input_batch(
            {
                "email": email,
                "cpf": cpf,
                "amount": amount,
            },
            EXAMPLE_VALIDATION_SCHEMA,
        )
        
        # Dados validados e sanitizados
        st.success(f"✅ Dados válidos: {validated}")
        
        # Inserir no banco
        neon_client.execute(
            "INSERT INTO users (email, cpf, amount) VALUES (%s, %s, %s)",
            (validated["email"], validated["cpf"], validated["amount"]),
        )
        
    except ValueError as e:
        st.error(f"❌ Erro de validação: {e}")
```

### 3. Sanitização de Strings

```python
from data_security import DataSecurity

# Remover caracteres perigosos
user_input = st.text_input("Descrição")
safe_input = DataSecurity.sanitize_string(user_input, max_length=500)

# Verificar SQL injection
if DataSecurity.detect_sql_injection(user_input):
    st.error("❌ Entrada suspeita de SQL injection!")
else:
    # Seguro para usar em prepared statement
    neon_client.execute(
        "INSERT INTO transactions (description) VALUES (%s)",
        (safe_input,),  # Parametrizado = SEGURO
    )
```

---

## 🏗️ Arquitetura de Segurança

### Camada 1: Validação de Entrada
```
User Input
    ↓
[validate_email / validate_cpf / validate_financial_amount]
    ↓
Invalid? → Error + Stop
    ↓
Valid
```

### Camada 2: Sanitização
```
Valid Input
    ↓
[sanitize_string / escape_html / remove_sql_keywords]
    ↓
Cleaned Input
```

### Camada 3: Prepared Statements (CRITICAL)
```
Cleaned Input
    ↓
client.execute("INSERT INTO ... VALUES (%s, %s)", (param1, param2))
                                                ↑
                                        Parametrizado = SQL injection BLOCKED
```

### Camada 4: Criptografia em Trânsito
```
Data
    ↓
[TLS/HTTPS Encryption]
    ↓
PostgreSQL (Neon) via SSL
    ↓
[TLS/HTTPS Decryption]
    ↓
Application
```

### Camada 5: Auditoria
```
INSERT/UPDATE/DELETE
    ↓
[Trigger in Database]
    ↓
audit_log table (old_values, new_values, user_id, timestamp, ip)
```

---

## 🛡️ Validações Implementadas

| Tipo | Método | O que faz | Exemplo |
|------|--------|----------|---------|
| **E-mail** | `validate_email()` | RFC 5322 básico | `user@example.com` |
| **CPF** | `validate_cpf()` | 11 dígitos | `123.456.789-00` |
| **Telefone** | `validate_phone()` | Brasil (10-11 dígitos) | `(11) 99999-9999` |
| **URL** | `validate_url()` | HTTP/HTTPS only | `https://example.com` |
| **Valor Monetário** | `validate_financial_amount()` | 0 a 999M, 2 casas decimais | `1234.56` |
| **Data** | `validate_date()` | Formato específico | `2026-05-17` |
| **String** | `sanitize_string()` | Remove caracteres perigosos | Qualquer texto |
| **SQL Injection** | `detect_sql_injection()` | Detecta keywords suspeitas | `DROP TABLE; --` |

---

## 📚 Boas Práticas

### ✅ FAÇA

```python
# 1. Sempre usar prepared statements (psycopg2 com %s)
client.execute(
    "SELECT * FROM users WHERE email = %s",
    (email,)  # ← Separado do SQL = SEGURO
)

# 2. Validar e sanitizar entrada
email = DataSecurity.sanitize_string(user_input)
if not DataSecurity.validate_email(email):
    raise ValueError("E-mail inválido")

# 3. Usar HTTPS/TLS (Neon já usa SSL por padrão)
DATABASE_URL = "postgresql://...?sslmode=require"

# 4. Armazenar secrets em variáveis de ambiente
DATABASE_URL = os.environ.get("DATABASE_URL")
# Nunca: DATABASE_URL = "postgresql://user:password@host/db"

# 5. Limitar permissões no banco
# Usuário app: SELECT, INSERT, UPDATE (sem DROP, ALTER)
# Usuário admin: Todas as permissões

# 6. Registrar alterações em auditoria
# Trigger no banco insere em audit_log automaticamente

# 7. Respeitar LGPD (consentimento, retenção, direitos)
CookieConsent.render_consent_banner()
```

### ❌ NÃO FAÇA

```python
# ❌ SQL concatenação (SQL INJECTION!)
query = f"SELECT * FROM users WHERE email = '{email}'"
# Se email = "'; DROP TABLE users; --"
# Resultado: SELECT * FROM users WHERE email = ''; DROP TABLE users; --'

# ❌ Hardcoded credentials
DATABASE_URL = "postgresql://admin:password123@host/db"
OPENAI_API_KEY = "sk-1234567890abcdef"

# ❌ Confiar em dados do cliente sem validar
user_role = st.selectbox("Seu role", ["admin", "user"])  # Usuário pode escolher "admin"!

# ❌ Logar dados sensíveis
logger.info(f"User email: {email}, Password: {password}")  # NÃO!

# ❌ Desabilitar HTTPS
DATABASE_URL = "postgresql://...?sslmode=disable"  # NÃO!

# ❌ Armazenar senhas em texto plano
# Usar bcrypt/scrypt (passlib):
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed = pwd_context.hash(password)
```

---

## 🔑 Secrets Management

### Desenvolvimento Local (.env)

```bash
# .env (NUNCA commit no Git!)
DATABASE_URL=postgresql://user:pass@localhost/neondb
GROQ_API_KEY=gsk_...
GEMINI_API_KEY=AIzaSy...
OPENAI_API_KEY=sk_...
MONGODB_ATLAS_URI=mongodb+srv://...
```

**Proteger:**
```bash
# Adicionar ao .gitignore
echo ".env" >> .gitignore

# Permissões restritas (Linux/Mac)
chmod 600 .env
```

### Produção (Streamlit Cloud / Neon)

```python
# streamlit.py
def get_secret_or_env(key):
    try:
        return st.secrets[key]  # Streamlit Cloud
    except:
        return os.environ.get(key)  # Fallback: variável de ambiente

DATABASE_URL = get_secret_or_env("DATABASE_URL")
```

**Configurar em Streamlit Cloud:**
1. Deploy → Settings → Secrets
2. Adicionar cada chave:
   ```
   DATABASE_URL = "postgresql://..."
   GROQ_API_KEY = "gsk_..."
   ```

---

## 🚨 Checklist de Segurança

### Antes de Deploy

- [ ] Todas as queries usam prepared statements (`%s`)
- [ ] `.env` nunca foi commitado (check: `git log --all --full-history -- .env`)
- [ ] Secrets em st.secrets ou variáveis de ambiente (nunca hardcoded)
- [ ] Validação de entrada em todos os forms
- [ ] HTTPS/TLS habilitado (Neon/Streamlit já fazem)
- [ ] Logs não contêm senhas ou tokens
- [ ] Rate limiting em APIs (se aplicável)
- [ ] CORS bem configurado (se API separada)
- [ ] Consentimento de cookies (LGPD) implementado
- [ ] Política de privacidade ([TERMO_DE_USO.md](TERMO_DE_USO.md)) visível

### Em Produção

- [ ] Monitorar audit_log para atividades suspeitas
- [ ] Revisar permissões de banco de dados regularmente
- [ ] Fazer backup criptografado diariamente
- [ ] Revogar chaves API comprometidas imediatamente
- [ ] Manter dependências atualizadas (`pip list --outdated`)
- [ ] Testar cenários de falha e recuperação

---

## 📊 Exemplo Completo: Form Seguro

```python
import streamlit as st
from data_security import DataSecurity, EXAMPLE_VALIDATION_SCHEMA
from config import get_neon_database

st.title("Registrar Transação")

with st.form("transaction_form"):
    email = st.text_input("E-mail")
    cpf = st.text_input("CPF")
    amount = st.number_input("Valor", min_value=0.01)
    description = st.text_area("Descrição")
    transaction_date = st.date_input("Data")
    
    submitted = st.form_submit_button("Salvar")

if submitted:
    try:
        # 1. Validar tudo
        validated = DataSecurity.validate_input_batch(
            {
                "email": email,
                "cpf": cpf,
                "amount": amount,
                "description": description,
                "transaction_date": str(transaction_date),
            },
            EXAMPLE_VALIDATION_SCHEMA,
        )
        
        # 2. Conectar banco
        client = get_neon_database()
        
        # 3. Inserir com prepared statement (SEGURO)
        success = client.execute(
            """
            INSERT INTO transactions 
            (email, cpf, amount, description, transaction_date)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                validated["email"],
                validated["cpf"],
                validated["amount"],
                validated["description"],
                validated["transaction_date"],
            ),
        )
        
        if success:
            st.success("✅ Transação salva com segurança!")
        else:
            st.error("❌ Erro ao salvar")
            
    except ValueError as e:
        st.error(f"❌ {e}")
    except Exception as e:
        st.error(f"❌ Erro inesperado: {e}")
```

---

## 🔍 Detectar Vulnerabilidades

### Ferramenta: Bandit (Python)

```bash
# Instalar
pip install bandit

# Escanear código
bandit -r src/

# Relatório HTML
bandit -r src/ -f html -o security_report.html
```

### Ferramenta: pip-audit (Dependências)

```bash
# Instalar
pip install pip-audit

# Verificar vulnerabilidades conhecidas
pip-audit

# Exemplo output:
# Found 1 vulnerability in requests [2.25.0]
# Vulnerability: CVE-2021-3XXX
# Fix: pip install --upgrade requests
```

### Ferramenta: OWASP ZAP (Se tiver API)

```bash
# Teste automatizado de segurança web
docker run -t owasp/zap2docker-stable zap-baseline.py -t http://localhost:8501
```

---

## 📚 Referências

- [OWASP Top 10 2023](https://owasp.org/www-project-top-ten/)
- [CWE-89: SQL Injection](https://cwe.mitre.org/data/definitions/89.html)
- [CWE-79: Cross-site Scripting (XSS)](https://cwe.mitre.org/data/definitions/79.html)
- [LGPD - Lei Geral de Proteção de Dados](http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
- [psycopg2 Documentation](https://www.psycopg.org/)

---

**Arquivo**: `src/data_security.py`  
**Documentação**: `docs/06-data-security.md`  
**Integrar no**: `src/streamlit.py`
