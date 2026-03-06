## 🙏 Créditos & Licenças

**Desenvolvimento:**
- Projeto criado por vdfs89 para bootcamp Santander DIO.
- Inspiração: MestreGrana, GPT, Groq, Gemini, OpenAI, MongoDB Atlas, Streamlit.

**Licença:**
- MIT License. Livre para uso, modificação e distribuição, desde que mantidos os créditos.

**Agradecimentos:**
- Comunidade DIO, mentores, revisores e todos que contribuíram com feedback.
## ❓ FAQ & Troubleshooting

**1. Não conecta ao MongoDB Atlas:**
	- Verifique se o IP está liberado no painel Atlas.
	- Confirme usuário/senha e string de conexão no `.env`.
	- Teste conexão via CLI: `mongosh <string de conexão>`.
	- Ping no cluster: `ping cluster0-shard-00-00.3ahjc49.mongodb.net`.
	- Use `tls=true` na string de conexão.

**2. Streamlit Cloud não conecta ao Atlas:**
	- Certifique-se de liberar o IP 0.0.0.0/0 no Atlas para acesso público (apenas para testes, nunca em produção).
	- Adicione as variáveis de ambiente no painel de secrets do Streamlit Cloud.
	- Verifique se o cluster está ativo e não em modo pause.
	- Consulte os logs do Streamlit Cloud para detalhes do erro.
	- Teste a conexão localmente antes de subir para a nuvem.

**2. Erro de dependências:**
	- Execute `pip install -r requirements.txt`.
	- Ative o ambiente virtual corretamente.

**3. Streamlit não inicia:**
	- Verifique se está no diretório correto.
	- Ative o ambiente virtual.
	- Execute `streamlit run src/streamlit.py`.

**4. Voz não funciona:**
	- Verifique se o microfone está conectado e liberado no navegador.
	- Teste com outro navegador.

**5. Segurança:**
	- Nunca suba `.env` ou credenciais para o GitHub.
	- Confira se `.env` está no `.gitignore`.

**6. Dúvidas sobre API keys:**
	- As chaves Groq, Gemini e OpenAI são opcionais, mas recomendadas para melhor experiência.
## 📝 Instruções Rápidas

1. Clone o repositório:
	```bash
	git clone https://github.com/vdfs89/InvestimentoDIO.git
	cd InvestimentoDIO
	```
2. Crie e ative o ambiente virtual:
	```bash
	python -m venv .venv
	# Windows:
	.venv\Scripts\activate
	# Linux/Mac:
	source .venv/bin/activate
	```
3. Instale as dependências:
	```bash
	pip install -r requirements.txt
	```
4. Configure o arquivo `.env` com sua string do MongoDB Atlas e chaves de API (Groq, Gemini, OpenAI):
	```env
	MONGODB_ATLAS_URI=mongodb+srv://<usuario>:<senha>@<cluster>.mongodb.net/
	GROQ_API_KEY=...
	GEMINI_API_KEY=...
	OPENAI_API_KEY=...
	```
5. Execute o app:
	```bash
	streamlit run src/streamlit.py
	```

## 💡 Exemplos de Uso

- Faça login com qualquer usuário/senha para testar o fluxo.
- Pergunte sobre produtos financeiros, simule investimentos, peça recomendações personalizadas.
- Use o chat de voz para interagir com a IA (Groq Orpheus TTS).
- Exporte o histórico de conversas em CSV.
- Visualize gráficos dinâmicos e métricas de performance.
data/         # Dados mockados do cliente (João Silva)
docs/         # Documentação completa (caso de uso, base, prompts, métricas, pitch)
src/          # Código principal (app.py, agente.py, config.py)
examples/     # (Opcional) Exemplos de uso
assets/       # (Opcional) Imagens e diagramas


# 💸 MestreGrana: Inteligência que forja sua liberdade financeira

Agente de IA Generativa que ensina conceitos de finanças pessoais de forma simples e personalizada, usando os próprios dados do cliente como exemplos práticos. MestreGrana é seu mentor digital para conquistar autonomia e segurança financeira.

---


## 💡 O Que é o MestreGrana?
O MestreGrana é um educador financeiro que ensina, não recomenda. Ele explica conceitos como reserva de emergência, tipos de investimentos e análise de gastos usando uma abordagem didática e exemplos concretos baseados no perfil do cliente.


### O que o MestreGrana faz:

✅ Explica conceitos financeiros de forma simples
✅ Usa dados do cliente como exemplos práticos
✅ Responde dúvidas sobre produtos financeiros
✅ Analisa padrões de gastos de forma educativa


### O que o MestreGrana NÃO faz:

❌ Não recomenda investimentos específicos
❌ Não acessa dados bancários sensíveis
❌ Não substitui um profissional certificado

---

## 🏗️ Arquitetura


## 🏗️ Arquitetura e Fluxo de Dados

**Stack:**

- Interface: Streamlit
- LLM: Groq, Gemini, OpenAI (failover multi-LLM)
- Banco de dados: MongoDB Atlas (cloud, gratuito)
- Dados: JSON/CSV mockados (apenas para testes)

**Fluxo RAG:**
O MestreGrana utiliza Retrieval-Augmented Generation (RAG) para alimentar a IA com contexto real do usuário, usando buscas semânticas e filtros de contexto via Atlas. Isso garante respostas personalizadas e condizentes com o perfil do investidor.
---

## ☁️ MongoDB Atlas

O projeto utiliza MongoDB Atlas como banco de dados principal, hospedado na nuvem (DBaaS). Os dados de produtos financeiros são lidos diretamente do cluster Atlas, permitindo integração com IA, buscas semânticas e escalabilidade.

**Segurança:** Nunca exponha credenciais reais em arquivos públicos ou README! Adicione `.env` e `secrets.toml` ao seu `.gitignore` para garantir segurança das credenciais.

**Reforço:** Nunca suba arquivos `.env` ou `secrets.toml` no repositório. Eles devem conter apenas dados sensíveis e ficar fora do controle de versão. Compartilhe credenciais apenas por canais seguros.

### Como configurar o MongoDB Atlas:
1. Crie uma conta gratuita em https://www.mongodb.com/atlas/database
2. Crie um cluster (M0 Free Tier)
3. Crie um usuário de banco e configure o IP de acesso
4. Copie a string de conexão (exemplo):
	`mongodb+srv://<usuario>:<senha>@<cluster>.mongodb.net/`
5. Adicione a string ao arquivo `.env`:
	`MONGODB_ATLAS_URI=mongodb+srv://<usuario>:<senha>@<cluster>.mongodb.net/`
6. O app já está pronto para ler os dados do Atlas!
## 🌐 Visão de Futuro
O MestreGrana foi projetado para ser agnóstico a bancos de dados, permitindo a futura implementação de camadas de grafos para análise de vínculos financeiros complexos (Neo4j).

Na evolução do projeto, está prevista a integração com bancos de dados orientados a grafos (ex: Neo4j), permitindo análises avançadas de relacionamentos entre produtos, clientes e transações. Isso abrirá espaço para recomendações personalizadas, detecção de fraudes e visualização de redes financeiras.

---
## 🚀 Pitch de Negócios
O MestreGrana é uma solução de IA para educação financeira, pensada para escalar em ambientes corporativos, bootcamps e consultorias. Com arquitetura robusta, integração cloud e foco em personalização, ele prepara o usuário para decisões financeiras seguras e autônomas, elevando o padrão de atendimento digital.

---

---


## 📁 Estrutura do Projeto

Este repositório reúne múltiplos módulos do bootcamp Bradesco - GenAI & Dados, cada um com seu foco e exemplos práticos:

```plaintext
.
├── assets/       # Identidade visual e diagramas de arquitetura
├── data/         # Bases mockadas para o contexto do RAG
├── docs/         # Documentação técnica e estratégica (Prompts, Métricas)
├── examples/     # Scripts de apoio e estudos do bootcamp
├── src/          # Core do sistema (Streamlit e Agente)
├── tests/        # Validações de lógica e integração
└── requirements.txt
```
---

## 🚀 Exemplos de Uso

### Executando o app

```bash
streamlit run src/streamlit.py
```

### Exemplos de perguntas para o assistente:

- "Como funciona a reserva de emergência?"
- "Quais produtos de renda fixa são recomendados para meu perfil?"
- "Me mostre meus gastos por categoria este mês."
- "O que é CDI?"
- "Simule um aporte mensal de R$ 500 para meta de viagem."

### Recursos interativos:
- Chat de voz (pergunte e ouça a resposta)
- Gráficos dinâmicos de gastos
- Exportação do histórico de conversas
- Feedback do usuário
- Integração com MongoDB Atlas para dados reais

---
│   └── readme.md
│
├── assets/       # Imagens e diagramas (opcional)
│
└── README.md     # Documentação principal do projeto
```

Cada pasta contém arquivos autoexplicativos para facilitar o estudo e navegação entre os módulos do bootcamp.

---

## 🚀 Como Executar

1. Instalar dependências
```bash
pip install -r src/requirements.txt
```

2. Rodar o MestreGrana
```bash
streamlit run src/streamlit.py
```

---

## 📱 Experiência Mobile
O app é responsivo e otimizado para uso em smartphones e tablets.

## 💬 Histórico de Conversas
Todas as interações ficam salvas e podem ser exportadas em CSV para acompanhamento.

## 📊 Gráficos Dinâmicos
Visualize o resumo financeiro do mês em gráficos interativos.

## ⭐ Feedback do Usuário
Envie sugestões, elogios ou críticas diretamente pelo app.

## 🚀 Como usar
1. Instale as dependências: `pip install -r src/requirements.txt`
2. Execute o app: `streamlit run src/streamlit.py`
3. Preencha o formulário, use o chat de voz e explore os recursos!

---


## 🎯 Exemplo de Uso

Pergunta: "O que é CDI?"
MestreGrana: "CDI é uma taxa de referência usada pelos bancos. Quando um investimento rende '100% do CDI', significa que ele acompanha essa taxa. Hoje o CDI está próximo da Selic. Quer que eu explique a diferença entre os dois?"

Pergunta: "Onde estou gastando mais?"
MestreGrana: "Olhando suas transações de outubro, sua maior despesa é moradia (R$ 1.380), seguida de alimentação (R$ 570). Juntas, representam quase 80% dos seus gastos. Isso é bem comum! Quer que eu explique algumas estratégias de organização?"

---

## 📊 Métricas de Avaliação

| Métrica        | Objetivo                                              | Método de Verificação                       |
|--------------- |------------------------------------------------------|---------------------------------------------|
| Assertividade  | O agente responde o que foi perguntado?              | Testes unitários com perguntas padrão.      |
| Segurança      | Evita inventar informações (anti-alucinação)?        | Grounding check contra a base-conhecimento. |
| Coerência      | A resposta é adequada ao perfil do cliente?          | Validação de persona via few-shot.          |

---

## 🎬 Diferenciais

- Personalização: Usa os dados do próprio cliente nos exemplos
- 100% Local: Roda com Groq, Gemini, OpenAI, sem enviar dados para APIs externas
- Educativo: Foco em ensinar, não em vender produtos
- Seguro: Estratégias de anti-alucinação documentadas

---

## 📋 Regras do Assistente Financeiro

O mentor segue as seguintes diretrizes, inspiradas no modelo do professor:

- Responde apenas perguntas sobre o mundo financeiro (finanças pessoais, investimentos, metas e produtos financeiros);
- Não recomenda investimentos específicos, apenas explica conceitos e funcionamento;
- Não responde perguntas fora do tema finanças. Caso ocorra, lembra seu papel de educador financeiro;
- Usa exemplos personalizados com base nos dados fornecidos;
- Linguagem simples, como se explicasse para um amigo;
- Admite quando não sabe algo: "Não tenho essa informação, mas posso explicar...";
- Sempre pergunta se o cliente entendeu;
- Responde de forma sucinta e direta, com no máximo 3 parágrafos;
- As respostas são permitidas apenas em português ou inglês.

---

## 📝 Documentação Completa

Toda a documentação técnica, estratégias de prompt e casos de teste estão disponíveis na pasta docs/.

---

## ✨ Sobre

Desenvolvido por Vitor Silva para o bootcamp Bradesco DIO, aplicando técnicas de Engenharia de Software, IA Generativa e Ciência da Computação.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vitor-silva-7418111a2)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/vdfs89)

*Projeto desenvolvido como parte dos requisitos para conclusão do bootcamp na plataforma DIO.*

O MestreGrana é pensado para ser extensível e preparado para o futuro da análise financeira. A arquitetura modular permite integrar novas fontes de dados, IA, e camadas de grafos, tornando o assistente apto para cenários corporativos, consultorias e bootcamps.
