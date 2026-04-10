<p align="center">
	<img src="img/unnamed.jpg" alt="Banner MestreGrana" width="100%" />
</p>

# MestreGrana

Mentor financeiro com IA para apoio em educacao financeira e orientacao de IRPF no Brasil, com respostas auditadas por um juiz multimodelo.

## Visao Geral

O app combina tres modelos para aumentar qualidade e seguranca:
- Groq (Llama 3) gera uma resposta candidata
- Google Gemini gera outra resposta candidata
- OpenAI (gpt-4o-mini) atua como juiz e escolhe a melhor resposta (ou bloqueia respostas inseguras)

A aplicacao roda em Streamlit e usa:
- Neon PostgreSQL (principal, para transacoes e schema fiscal)
- MongoDB Atlas (opcional, para produtos e historico legado)
- fallback local com arquivos em data/

## Principais Recursos

- Chat financeiro com foco em IRPF
- Auditoria multimodelo com bloqueio de resposta insegura
- Radar de deducoes (saude e educacao) no contexto do agente
- Chat de voz e resposta em audio
- Dashboard com metricas e visualizacoes
- Exportacao de historico em CSV

## Arquitetura (Resumo)

1. Usuario pergunta no chat.
2. Groq e Gemini geram respostas candidatas.
3. GPT-4o-mini avalia as candidatas com base no contexto financeiro e nas regras tributarias.
4. O app mostra a resposta vencedora (ou bloqueio de seguranca).

## Requisitos

- Python 3.10+
- Dependencias em src/requirements.txt
- Para deploy Streamlit Cloud, arquivo packages.txt com libpq-dev

## Configuracao de Ambiente

Crie um arquivo .env local (nunca commitar):

```env
# IA
GROQ_API_KEY=...
GEMINI_API_KEY=...
OPENAI_API_KEY=...
GROQ_TTS_API_KEY=...

# Banco principal (Neon)
DATABASE_URL=postgresql://usuario:senha@host/neondb?sslmode=require

# Opcional (Atlas)
MONGODB_ATLAS_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/
```

No Streamlit Cloud, configure as mesmas chaves em Secrets (TOML).

## Instalacao e Execucao Local

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

pip install -r src/requirements.txt
streamlit run src/streamlit.py
```

## Banco de Dados Neon

O schema esta em scripts/neon_schema.sql e pode ser aplicado com:

```bash
python setup_db.py
```

Tabelas principais:
- users
- categories (com is_tax_deductible)
- transactions
- budgets
- debts
- ai_insights

## Deploy no Streamlit Cloud

1. Garanta que packages.txt existe na raiz com:

```txt
libpq-dev
```

2. Use psycopg2-binary sem pin estrito em src/requirements.txt.
3. Configure Secrets no painel do app.
4. Faça redeploy.

## Troubleshooting

### Falha de conexao no Neon

- Verifique DATABASE_URL
- Confirme usuario/senha no Neon
- Confirme sslmode=require
- Rode python setup_db.py para testar conexao real

### Falha de build no Streamlit Cloud (pg_config/libpq)

- Verifique se packages.txt contem libpq-dev
- Verifique se src/requirements.txt contem psycopg2-binary

### Atlas offline

- O app continua funcional com fallback local para produtos/historico
- Verifique MONGODB_ATLAS_URI e whitelist de IP no Atlas

### Audio nao funciona

- Verifique permissao de microfone no navegador
- Teste outro navegador

## Seguranca

- Nunca publique .env, secrets.toml ou credenciais
- Rotacione chaves se houver exposicao
- .gitignore ja bloqueia arquivos sensiveis e audios temporarios

## Estrutura do Projeto

```txt
.
├── data/
├── docs/
├── examples/
├── scripts/
│   └── neon_schema.sql
├── src/
│   ├── streamlit.py
│   ├── requirements.txt
│   └── teste_mongodb.py
├── tests/
├── setup_db.py
├── packages.txt
└── README.md
```

## Aviso Legal

O MestreGrana e um assistente de IA para apoio educacional e organizacao financeira. Casos tributarios especificos devem ser validados com contador.

## Creditos

Desenvolvido por vdfs89 no contexto de bootcamp Santander DIO / Bradesco DIO.
