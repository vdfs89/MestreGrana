# 📚 Exemplos de Uso - MestreGrana

Este documento descreve os exemplos de uso práticos integrados ao projeto MestreGrana, ensinando desenvolvedores a interagir com os bancos de dados e com os modelos de Inteligência Artificial usando fallback automático.

---

## 🤖 1. Consulta ao Mentor de IA com Dados Locais

O arquivo [exemplo_llm_e_dados.py](file:///f:/DIO/Santander/InvestimentoDIO/examples/exemplo_llm_e_dados.py) demonstra como inicializar a cadeia de inteligência artificial do MestreGrana localmente, injetar dados reais mockados e obter uma resposta personalizada fundamentada e segura.

### Como Executar

No terminal, execute o script utilizando o Python do ambiente virtual:

```bash
# Windows
.venv\Scripts\python.exe -Xutf8 examples/exemplo_llm_e_dados.py
```

*Nota: O parâmetro `-Xutf8` força o Python a utilizar codificação UTF-8 no console do Windows, evitando falhas de encode com emojis.*

### Funcionamento Interno

1. **Carregamento de Dados**: Utiliza as funções do serviço modular `data_service` para buscar `data/perfil_investidor.json` e `data/transacoes.csv`.
2. **Construção de Contexto**: Consolida as informações de perfil (nome, metas, saldo) e transações recentes do usuário em uma string de contexto estruturada (System Prompt).
3. **Cadeia de Modelos com Fallback**: Aciona o resolvedor central `call_llm_with_fallback`, que tenta consultar na seguinte ordem de failover:
   * **Groq** (`llama-3.3-70b-versatile`)
   * **Gemini** (`gemini-2.5-flash`)
   * **OpenAI** (`gpt-4o-mini`)
4. **Resultado**: Imprime o conselho financeiro personalizado gerado pela IA.

---

## 🗄️ 2. Integração de Banco de Dados com Neon (PostgreSQL)

O arquivo [neon_integration_example.py](file:///f:/DIO/Santander/InvestimentoDIO/src/neon_integration_example.py) contém uma página modelo interativa em Streamlit demonstrando o uso correto de conexões de pooling com o Neon Database.

### Padrões de Integração Recomendados

#### A. Buscando dados usando pooling seguro e conversão para DataFrame:
```python
from config import get_neon_database
import pandas as pd

client = get_neon_database()
df = client.fetch_dataframe("SELECT * FROM transactions LIMIT 10")
```

#### B. Execução segura contra SQL Injection (Prepared Statements):
```python
client = get_neon_database()

# Parâmetros passados em tupla de forma sanitizada pelo psycopg2
with client.query(
    "SELECT name FROM users WHERE id = %s",
    (user_id,)
) as cursor:
    row = cursor.fetchone()
```

#### C. Inserções transacionais com rollback automático em caso de erro:
```python
client = get_neon_database()

# Executa query transacional e retorna True em caso de sucesso
success = client.execute(
    "INSERT INTO transactions (user_id, amount, description) VALUES (%s, %s, %s)",
    (user_id, amount, description)
)
```

---

## 🎤 3. Chat de Voz & gTTS

O módulo de voz do MestreGrana (`src/components/voice.py` e `src/streamlit.py`) permite capturar a fala do usuário e sintetizar respostas.

### Como Funciona a Integração
1. **Entrada**: `render_voice_input()` ativa o microfone via `pyaudio` e usa a API do Google Cloud (`SpeechRecognition`) para traduzir a fala do usuário para texto.
2. **Processamento**: O texto resultante é integrado com o contexto financeiro local e enviado à cadeia de IA.
3. **Saída**: A resposta gerada é repassada para `render_voice_output()`, que utiliza a biblioteca `gTTS` (Google Text-to-Speech) para sintetizar e renderizar um componente de áudio nativo reproduzível no Streamlit.

---

## 🧪 Validação Geral de Conexões

Caso queira checar se as variáveis de ambiente das chaves e conexões do seu arquivo `.env` estão ativas, basta executar a ferramenta de validação completa do projeto:

```bash
# Windows
python -Xutf8 validate_all.py
```
