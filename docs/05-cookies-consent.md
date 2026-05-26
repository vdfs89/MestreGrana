# Consentimento de Cookies - Guia de Integração

## 📋 Visão Geral

O MestreGrana implementa **consentimento de cookies LGPD-compliant** com:

✅ **Banner de consentimento** na primeira acesso  
✅ **Armazenamento seguro** em session_state + banco de dados  
✅ **Auditoria** de consentimento com timestamp e IP  
✅ **Revogação** de consentimento a qualquer tempo  

## 🚀 Quick Start

### 1. Importar no Streamlit

```python
# src/streamlit.py
import streamlit as st
from cookies_consent import CookieConsent

st.set_page_config(page_title="MestreGrana", layout="wide")

# Renderizar banner (SEMPRE no topo!)
CookieConsent.render_consent_banner()

# Resto da app...
```

### 2. Verificar Consentimento Antes de Enviar Dados

```python
# Só enviar para analytics se usuário consentiu
if CookieConsent.can_track_analytics():
    # enviar evento para Google Analytics
    gtag.event("user_login", {"user_id": 123})

# Só armazenar preferências se consentido
if CookieConsent.can_store_preferences():
    st.session_state["dark_mode"] = True
```

### 3. Salvar Consentimento no Banco

```python
from config import get_neon_database

if user_logged_in:
    client = get_neon_database()
    success = CookieConsent.save_consent_to_db(user_id, client)
    if success:
        st.success("✅ Consentimento salvo com sucesso")
```

## 🏗️ Arquitetura

### `src/cookies_consent.py` - Gerenciador

| Método | Descrição |
|--------|-----------|
| `get_consent_from_session()` | Retorna consentimento armazenado em session_state |
| `set_consent(analytics, necessary, preferences)` | Armazena consentimento (com timestamp) |
| `save_consent_to_db(user_id, client)` | Persistem consentimento no banco (auditoria) |
| `render_consent_banner()` | Renderiza banner LGPD interativo |
| `can_track_analytics()` | True se usuário consentiu com analytics |
| `can_store_preferences()` | True se usuário consentiu com preferências |
| `get_consent_status()` | Retorna string com status para exibição |

### Tabela no Banco

```sql
CREATE TABLE user_consents (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(id),
    consent_type VARCHAR(50),      -- 'cookies_analytics', etc
    consent_data JSONB,             -- {'necessary': true, 'analytics': true, ...}
    consented_at TIMESTAMP,         -- ISO timestamp do consentimento
    revoked_at TIMESTAMP,           -- Quando foi revogado (NULL = ativo)
    ip_address VARCHAR(45),         -- Para auditoria
    user_agent VARCHAR(500)         -- Navegador/SO para rastreabilidade
);
```

## 📊 Exemplo Completo

### Integração no streamlit.py

```python
import streamlit as st
from cookies_consent import CookieConsent
from config import get_neon_database

st.set_page_config(page_title="MestreGrana", layout="wide")

# 1. SEMPRE renderizar banner no topo
CookieConsent.render_consent_banner()

# 2. Exibir status em sidebar
st.sidebar.markdown("---")
st.sidebar.metric("🍪 Consentimento", CookieConsent.get_consent_status())

# 3. App logic
st.title("MestreGrana - Assistente Financeiro")

# 4. Login
if st.session_state.get("user_id"):
    user_id = st.session_state["user_id"]
    
    # Salvar consentimento no banco para auditoria
    if CookieConsent.get_consent_from_session():
        client = get_neon_database()
        CookieConsent.save_consent_to_db(user_id, client)
    
    # Dashboard
    if CookieConsent.can_track_analytics():
        st.info("📊 Analytics ativado - seu uso está sendo acompanhado para melhorias")
    
    if CookieConsent.can_store_preferences():
        st.info("⚙️ Preferências ativadas - suas configurações serão lembradas")
```

## 🔍 Dados Coletados

### Se consentir com "Necessários" (obrigatório)
```json
{
    "necessary": true,
    "analytics": false,
    "preferences": false,
    "timestamp": "2026-05-17T10:30:00",
    "version": "1.0"
}
```

### Se consentir com tudo
```json
{
    "necessary": true,
    "analytics": true,
    "preferences": true,
    "timestamp": "2026-05-17T10:30:00",
    "version": "1.0"
}
```

Armazenado no banco:
```sql
INSERT INTO user_consents (user_id, consent_type, consent_data, consented_at, ip_address)
VALUES ('user123', 'cookies_analytics', '{"necessary": true, "analytics": true, "preferences": true, ...}', NOW(), '192.168.1.1')
```

## 🔄 Revogação de Consentimento

### No Streamlit

```python
if st.button("❌ Revogar Consentimento"):
    # Limpar session
    st.session_state[CookieConsent.SESSION_KEY] = None
    
    # Marcar como revogado no banco
    client = get_neon_database()
    client.execute(
        "UPDATE user_consents SET revoked_at = NOW() WHERE user_id = %s AND revoked_at IS NULL",
        (user_id,)
    )
    st.rerun()
```

### Usuário Manual

1. Abrir DevTools (F12)
2. Application → Cookies → Delete all
3. Acessar app novamente → banner reaparece

## 📜 Conformidade LGPD

O banner implementa:

✅ **Consentimento prévio**: Antes de enviar dados  
✅ **Granularidade**: Analytics e preferências são opcionais  
✅ **Rastreabilidade**: Timestamp, IP, user_agent no banco  
✅ **Revogação**: Fácil desativação de consentimento  
✅ **Documentação**: Link para [TERMO_DE_USO.md](TERMO_DE_USO.md)  

## 🛡️ Boas Práticas

### ✅ Faça

```python
# 1. Renderizar banner ANTES de qualquer coleta
CookieConsent.render_consent_banner()

# 2. Verificar consentimento antes de enviar dados
if CookieConsent.can_track_analytics():
    send_to_google_analytics()

# 3. Persistir consentimento no banco
CookieConsent.save_consent_to_db(user_id, client)

# 4. Respeitar revogação
# (app para de enviar dados se revogado)
```

### ❌ Não Faça

```python
# ❌ Enviar dados sem perguntar
send_to_google_analytics()  # NUNCA!

# ❌ Esconder consentimento
# (deve estar visível e fácil de revogar)

# ❌ Usar cookies para tracking sem consentimento
gtag.pageview()  # Precisa de can_track_analytics() == True
```

## 📚 Referências

- [Lei Geral de Proteção de Dados (LGPD)](http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
- [GDPR Cookies (similar à LGPD)](https://gdpr-info.eu/issues/cookies/)
- [Streamlit Session State](https://docs.streamlit.io/library/api-reference/session-state)

---

**Arquivo**: `src/cookies_consent.py`  
**Esquema**: `scripts/neon_schema.sql` (tabela `user_consents`)  
**Documentação**: `docs/TERMO_DE_USO.md` (Seção 2.5)
