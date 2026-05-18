# MestreGrana

**MEDE. PLANEJA. MULTIPLICA.** 📊

MestreGrana é um assistente financeiro em Streamlit que combina chat com IA, dashboard interativo, relatórios financeiros, simulador de produtos e auditoria completa para apoiar educação financeira e organização do histórico do usuário.

## O que este projeto entrega

- 💬 **Chat Financeiro** com resposta por múltiplos modelos (Groq, Gemini, OpenAI)
- 🎙️ **Chat de Voz** com captura de áudio e resposta sintetizada (gTTS)
- 📊 **Dashboard** com visão de saldo, transações, perfil de investidor e produtos
- 📈 **Relatórios Financeiros** (DRE, Fluxo de Caixa, Análise de Variância)
- 💼 **Simulador de Produtos** com 15+ produtos financeiros e cenários customizados
- 📋 **Auditoria Completa** com rastreamento de alterações e ações do usuário
- 🎨 **Branding Profissional** com identidade visual MestreGrana
- 🔐 **Segurança Avançada** (LGPD, validação de inputs, sanitização, prepared statements)
- 💾 **Integração Neon** com connection pooling, health checks e retry automático
- 📁 **Fallback Local** com CSV/JSON quando banco não estiver disponível

## Como funciona

1. O usuário acessa o app Streamlit com interface profissional (MestreGrana branding)
2. Chat multimodelo: Groq (Llama 3), Gemini, OpenAI - com fallback automático
3. Dados integrados: Neon PostgreSQL + MongoDB Atlas + fallback local (CSV/JSON)
4. Módulos especializados: Dashboard, Relatórios, Simulador, Auditoria
5. Validação & Segurança: Input sanitization, LGPD compliance, audit trail
6. Exportação: Histórico em CSV, relatórios em PDF (via financial_reports)

## Stack principal

- **Backend**: Python 3.10+
- **Frontend**: Streamlit (layout responsivo, custom CSS)
- **Databases**: PostgreSQL (Neon) + MongoDB Atlas (opcional) + local files
- **LLM**: Groq (free), Google Gemini (free), OpenAI (paid)
- **Audio**: speech_recognition (input) + gTTS (output)
- **Branding**: Custom CSS com cores #00CB63 (verde) + #042540 (azul)

## Estrutura do repositório

```txt
.
├── .github/
│   └── workflows/
│       └── ci.yml                    # GitHub Actions (lint, tests)
├── data/
│   ├── historico_atendimento.csv
│   ├── perfil_investidor.json
│   ├── produtos_financeiros.json
│   └── transacoes.csv
├── docs/
│   ├── 00-resumo-dados.md
│   ├── 01-documentacao-agente.md
│   ├── 02-base-conhecimento.md
│   ├── 03-prompts.md
│   ├── 04-metricas.md
│   ├── 05-pitch.md
│   ├── 06-divulgacao-linkedin.md
│   └── 07-branding-guidelines.md    # New: brand identity
├── scripts/
│   └── neon_schema.sql
├── src/
│   ├── audit_logs.py                # New: audit trail
│   ├── branding.py                  # New: custom theme & UI
│   ├── config.py
│   ├── cookies_consent.py           # New: LGPD
│   ├── data_security.py             # New: input validation
│   ├── financial_reports.py         # New: DRE, cashflow, variance
│   ├── neon_client.py
│   ├── products_simulator.py        # New: product catalog
│   ├── requirements.txt
│   ├── streamlit.py
│   └── teste_mongodb.py
├── tests/
│   ├── test_branding.py             # New
│   ├── test_config.py               # New
│   ├── test_data_security.py        # New
│   └── test_neon_client.py          # New
├── .env.example                     # New: config template
├── .gitignore
├── Dockerfile                       # New: containerization
├── packages.txt
├── README.md
├── SETUP.md                         # New: setup guide
├── setup_db.py
└── validate_all.py                  # New: validation script
```

## Início Rápido (3 passos)

### 1. Copiar template de configuração
```bash
cp .env.example .env
```

### 2. Preencher credenciais em `.env`
```env
GROQ_API_KEY=gsk_...              # Free: https://console.groq.com
GEMINI_API_KEY=AIza...             # Free: https://aistudio.google.com
OPENAI_API_KEY=sk-...              # Paid: https://platform.openai.com
DATABASE_URL=postgresql://...      # Neon: https://neon.tech
MONGODB_ATLAS_URI=mongodb+srv://... # Optional: https://mongodb.com
```

### 3. Validar e rodar
```bash
python validate_all.py              # Test all connections
streamlit run src/streamlit.py      # Start the app
```

**Guia detalhado**: Veja [SETUP.md](SETUP.md) para instruções passo-a-passo de cada serviço.

## Pré-requisitos

- Python 3.10+
- pip ou conda
- Credenciais de: Groq (free), Gemini (free), OpenAI (free/paid), Neon (free), MongoDB (optional)

## Banco de dados

O schema está em [scripts/neon_schema.sql](scripts/neon_schema.sql) e pode ser aplicado com:

```bash
python setup_db.py
```

**Neon PostgreSQL** integrado com:
- ✅ Connection pooling (eficiente com 2-10 conexões)
- ✅ Health check automático
- ✅ Retry com backoff exponencial (até 3 tentativas)
- ✅ TLS encryption em transmissão
- ✅ Logging detalhado e tratamento robusto de erros

**Validação**: Para testar todas as conexões (Neon, MongoDB, LLMs), execute:

```bash
python validate_all.py
```

Você verá status de cada serviço: 🟢 OK, ❌ Erro, ⚪ Não configurado.

O app tenta usar Neon primeiro. Se indisponível, tenta MongoDB Atlas. Se ambos falharem, usa fallback local (CSV/JSON).

## Testes

O projeto tem testes unitários em [tests/](tests/) e pode ser executado assim:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/

# Run with coverage report
pytest tests/ --cov=src --cov-report=html
```

**GitHub Actions** roda testes automaticamente em cada push (veja [.github/workflows/ci.yml](.github/workflows/ci.yml)).

## Deploy

### Streamlit Cloud
1. Configure [packages.txt](packages.txt) com `libpq-dev`
2. Coloque variáveis em **Secrets** (Settings → Secrets)
3. Deploy apontando para `src/streamlit.py`

### Docker (Local ou VPS)
```bash
docker build -t mestregrana .
docker run -p 8501:8501 --env-file .env mestregrana
```

Acesse em `http://localhost:8501`

### Variáveis de Ambiente obrigatórias
- `GROQ_API_KEY` - LLM primary
- `GEMINI_API_KEY` - LLM fallback
- `OPENAI_API_KEY` - LLM fallback
- `DATABASE_URL` - Neon PostgreSQL

## Segurança & Conformidade

O MestreGrana implementa múltiplas camadas de proteção:

### 🔐 Segurança Técnica
- **Input Validation**: 8 tipos de validação (email, phone, CPF, etc.)
- **SQL Injection Safe**: Prepared statements em 100% das queries
- **XSS Protection**: Sanitização de inputs HTML/JavaScript
- **Password Hashing**: SHA-256 com salt automático
- **TLS Encryption**: Transmissão criptografada (Neon, MongoDB, APIs)

### 📋 Auditoria & Conformidade
- **Audit Trail**: Tabela `audit_log` com todas as alterações
- **User Activity**: Rastreamento de ações do usuário
- **LGPD Compliance**: Banner de consentimento, direito ao esquecimento
- **Tax Compliance**: Tabela `tax_compliance` para rastreamento tributário
- **Consent Management**: Tabela `user_consents` com histórico

### 📚 Documentação Técnica
Consulte para detalhes:
- [docs/07-branding-guidelines.md](docs/07-branding-guidelines.md) - Identidade visual
- [docs/06-data-security.md](docs/06-data-security.md) - Segurança detalhada
- [SETUP.md](SETUP.md) - Configuração de variáveis
- [docs/TERMO_DE_USO.md](docs/TERMO_DE_USO.md) - Termos legais & LGPD

### ⚠️ Avisos Importantes
- Não publique `.env` ou secrets no git
- Este é um assistente **educacional**, não substitui contador ou consultor tributário
- Validar casos tributários específicos com profissional
- Ler [TERMO_DE_USO.md](docs/TERMO_DE_USO.md) antes de usar com dados reais

## Créditos

Projeto desenvolvido no contexto do bootcamp Santander DIO / Bradesco DIO.
