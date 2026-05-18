<p align="center">
	<img src="img/unnamed.jpg" alt="Banner MestreGrana" width="100%" />
</p>

# MestreGrana

MestreGrana é um assistente financeiro em Streamlit que combina chat com IA, áudio, dashboard e dados mockados para apoiar educação financeira e organização do histórico do usuário.

## O que este projeto entrega

- Chat financeiro com resposta gerada por múltiplos modelos e validação por juiz.
- Chat de voz com captura do microfone e resposta em áudio.
- Dashboard com visão de saldo, transações e catálogo de produtos.
- Exportação de histórico em CSV.
- Login rápido com persistência opcional em MongoDB Atlas.
- Fallback local com arquivos em data/ quando o banco não estiver disponível.

## Como funciona

1. O usuário conversa com o assistente no Streamlit.
2. O app consulta os dados de perfil, transações e histórico.
3. As respostas passam por um fluxo multimodelo com Groq, Gemini e OpenAI.
4. O resultado é exibido com áudio, histórico e contexto de apoio.

## Stack principal

- Python 3.10+
- Streamlit
- PostgreSQL no Neon
- MongoDB Atlas como suporte opcional
- Groq, Google Gemini e OpenAI

## Estrutura do repositório

```txt
.
├── data/
├── docs/
├── examples/
├── img/
├── scripts/
│   └── neon_schema.sql
├── src/
│   ├── config.py
│   ├── requirements.txt
│   ├── streamlit.py
│   └── teste_mongodb.py
├── tests/
├── setup_db.py
├── packages.txt
└── README.md
```

## Pré-requisitos

- Python 3.10 ou superior.
- Dependências listadas em [src/requirements.txt](src/requirements.txt).
- Arquivo [packages.txt](packages.txt) na raiz com `libpq-dev` para o deploy no Streamlit Cloud.

## Configuração de ambiente

Crie um arquivo `.env` local com as chaves necessárias:

```env
GROQ_API_KEY=...
GEMINI_API_KEY=...
OPENAI_API_KEY=...
GROQ_TTS_API_KEY=...

DATABASE_URL=postgresql://usuario:senha@host/neondb?sslmode=require
MONGODB_ATLAS_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/
```

O app também pode usar `st.secrets` no Streamlit Cloud. Se alguma chave obrigatória estiver ausente, a aplicação encerra com mensagem clara.

## Executar localmente

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r src/requirements.txt
streamlit run src/streamlit.py
```

## Banco de dados

O schema principal está em [scripts/neon_schema.sql](scripts/neon_schema.sql) e pode ser aplicado com:

```bash
python setup_db.py
```

O app tenta usar o Neon primeiro. Se o banco ou o Atlas não estiverem disponíveis, ele usa os arquivos locais em data/ como fallback.

## Testes

O projeto tem testes em [tests/](tests/) e pode ser executado assim:

```powershell
$env:PYTHONPATH='.'
python -m pytest tests/
```

O uso de `python -m pytest` evita problemas de importação que podem acontecer em alguns ambientes quando o `PYTHONPATH` não inclui a raiz do projeto.

## Deploy no Streamlit Cloud

1. Garanta que [packages.txt](packages.txt) contenha `libpq-dev`.
2. Configure as variáveis em Secrets do Streamlit Cloud.
3. Faça o deploy apontando para [src/streamlit.py](src/streamlit.py).

## Dados de exemplo

Os dados mockados usados pelo app estão em:

- [data/perfil_investidor.json](data/perfil_investidor.json)
- [data/produtos_financeiros.json](data/produtos_financeiros.json)
- [data/transacoes.csv](data/transacoes.csv)
- [data/historico_atendimento.csv](data/historico_atendimento.csv)

## Observações importantes

- Não publique `.env`, secrets ou credenciais.
- Casos tributários específicos devem ser validados com contador.
- O projeto foi pensado para demonstração, estudo e apoio educacional.
- **Leia [TERMO_DE_USO.md](docs/TERMO_DE_USO.md)** antes de usar em dados reais — contém avisos legais, LGPD e limitações.

## Conformidade e Segurança

O MestreGrana implementa:
- Rastreamento de conformidade tributária (tabela `tax_compliance`)
- Auditoria completa de alterações (`audit_log`)
- Suporte a documentação anexada (`supporting_documents`)
- Criptografia TLS em transmissão
- Verificação de credenciais em variáveis de ambiente
- Bloqueio de senhas no `.gitignore`

**Importante**: Este é um assistente educacional, não substitui contador ou consultor tributário.

## Créditos

Projeto desenvolvido no contexto do bootcamp Santander DIO / Bradesco DIO.
