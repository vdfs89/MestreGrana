
# 💸 FinanceForge: Financial Mentor (DIO Challenge)


![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-f55036?style=for-the-badge)
![Gemini](https://img.shields.io/badge/Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)

> **Status do Projeto:** 🚀 Deploy realizado com sucesso
> **Demo:** [engtutor.streamlit.app](https://engtutor.streamlit.app/)

---

## 📂 Estrutura de Pastas

```
data/         # Dados mockados do cliente (João Silva)
docs/         # Documentação completa (caso de uso, base, prompts, métricas, pitch)
src/          # Código principal (app.py, agente.py, config.py)
examples/     # (Opcional) Exemplos de uso
assets/       # (Opcional) Imagens e diagramas
```

---

## 🏗️ Arquitetura e Diferenciais

- **Failover Multi-LLM:** Resiliência entre Groq, Gemini e OpenAI (sempre responde)
- **RAG Real:** Respostas baseadas nos arquivos CSV/JSON do cliente
- **Few-Shot Prompting:** Prompts com exemplos reais para evitar alucinação
- **Interface Streamlit:** Chat interativo, áudio em português, tabelas e sugestões proativas
- **Acessibilidade:** Voz lenta/normal, transcrição do áudio
- **Diagrama Mermaid:** Arquitetura visual no docs/01-documentacao-agente.md

---

## 🚀 Como Executar

```bash
# Instale as dependências
pip install -r src/requirements.txt

# Execute o app principal
streamlit run src/app.py
```

---

## 📑 Documentação

Consulte a pasta `docs/` para:
- 01-documentacao-agente.md: Caso de uso, persona, diagrama Mermaid
- 02-base-conhecimento.md: Dados mockados e integração RAG
- 03-prompts.md: System prompt, few-shot, edge cases
- 04-metricas.md: Avaliação, testes, métricas técnicas
- 05-pitch.md: Roteiro do vídeo de apresentação

---

## 🏆 Referência DIO

Este projeto segue o padrão oficial DIO, com melhorias de engenharia e UX. Todos os dados, prompts e diagramas estão alinhados ao roteiro do desafio Bradesco.

---

## ✨ Sobre

Desenvolvido por Vitor Silva para o bootcamp Bradesco DIO, aplicando técnicas de Engenharia de Software, IA Generativa e Ciência da Computação.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vitor-silva-7418111a2)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/vdfs89)

*Projeto desenvolvido como parte dos requisitos para conclusão do bootcamp na plataforma DIO.*
