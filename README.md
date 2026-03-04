data/         # Dados mockados do cliente (João Silva)
docs/         # Documentação completa (caso de uso, base, prompts, métricas, pitch)
src/          # Código principal (app.py, agente.py, config.py)
examples/     # (Opcional) Exemplos de uso
assets/       # (Opcional) Imagens e diagramas


# 💸 MestreGrana: Inteligência que forja sua liberdade financeira

Agente de IA Generativa que ensina conceitos de finanças pessoais de forma simples e personalizada, usando os próprios dados do cliente como exemplos práticos. MestreGrana é seu mentor digital para conquistar autonomia e segurança financeira.

---

## 💡 O Que é o Edu?
O Edu é um educador financeiro que ensina, não recomenda. Ele explica conceitos como reserva de emergência, tipos de investimentos e análise de gastos usando uma abordagem didática e exemplos concretos baseados no perfil do cliente.

### O que o Edu faz:

✅ Explica conceitos financeiros de forma simples
✅ Usa dados do cliente como exemplos práticos
✅ Responde dúvidas sobre produtos financeiros
✅ Analisa padrões de gastos de forma educativa

### O que o Edu NÃO faz:

❌ Não recomenda investimentos específicos
❌ Não acessa dados bancários sensíveis
❌ Não substitui um profissional certificado

---

## 🏗️ Arquitetura

**Stack:**

- Interface: Streamlit
- LLM: Groq, Gemini, OpenAI (failover multi-LLM)
- Dados: JSON/CSV mockados

---


## 📁 Estrutura do Projeto

Este repositório reúne múltiplos módulos do bootcamp Bradesco - GenAI & Dados, cada um com seu foco e exemplos práticos:

```
├── data/         # Dados mockados do cliente (Finanças)
│   ├── perfil_investidor.json
│   ├── transacoes.csv
│   ├── historico_atendimento.csv
│   └── produtos_financeiros.json
│
├── docs/         # Documentação completa (caso de uso, base, prompts, métricas, pitch)
│   ├── 01-documentacao-agente.md
│   ├── 02-base-conhecimento.md
│   ├── 03-prompts.md
│   ├── 04-metricas.md
│   └── 05-pitch.md
│
├── src/          # Código principal do assistente financeiro
│   ├── streamlit.py
│   ├── config.py
│   └── requirements.txt
│
├── examples/     # Exemplos de scripts Python para estudo
│   ├── analise_acao.py
│   ├── primeiro_programa.py
│   └── Salario.py
│
├── utilities/    # Scripts utilitários para manipulação de dados
│   └── nome_maiusculo.py
│
├── tests/        # Testes automatizados
│   └── test_calculadora_exportacao.py
│
├── E-CARDS/      # Módulo SQL do bootcamp (projeto de banco de dados)
│   ├── assets/
│   ├── db_scripts/
│   ├── prompts/
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
2. Rodar o Edu
```bash
streamlit run src/app.py
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
Edu: "CDI é uma taxa de referência usada pelos bancos. Quando um investimento rende '100% do CDI', significa que ele acompanha essa taxa. Hoje o CDI está próximo da Selic. Quer que eu explique a diferença entre os dois?"

Pergunta: "Onde estou gastando mais?"
Edu: "Olhando suas transações de outubro, sua maior despesa é moradia (R$ 1.380), seguida de alimentação (R$ 570). Juntas, representam quase 80% dos seus gastos. Isso é bem comum! Quer que eu explique algumas estratégias de organização?"

---

## 📊 Métricas de Avaliação

| Métrica        | Objetivo                                              |
|--------------- |------------------------------------------------------|
| Assertividade  | O agente responde o que foi perguntado?              |
| Segurança      | Evita inventar informações (anti-alucinação)?        |
| Coerência      | A resposta é adequada ao perfil do cliente?          |

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
