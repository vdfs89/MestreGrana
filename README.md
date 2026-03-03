# 💰 Finanças do Zero: Mentor de Liberdade com IA Resiliente

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-f55036?style=for-the-badge)

Este repositório contém o projeto final desenvolvido para o bootcamp da **DIO (Digital Innovation One)**. O projeto evoluiu de uma simples curadoria de dados para uma aplicação de **IA de Alta Disponibilidade**, focada em democratizar a educação financeira.

* **Pipeline de Voz Integrado:** Conversão de texto para fala (TTS) via **gTTS**, proporcionando uma experiência de usuário mais fluida e acessível.

# 💸 FinanceForge: Mentoria Financeira Inteligente

> **Status do Projeto:** 🚀 Deploy realizado com sucesso.
> **Link da Demo:** [engtutor.streamlit.app](https://engtutor.streamlit.app/)

---

## 🏗️ Arquitetura de Engenharia
Este projeto implementa um Agente Financeiro Resiliente utilizando uma estratégia de **Failover** entre Groq, Gemini e OpenAI, garantindo alta disponibilidade e respostas fundamentadas em **RAG (Retrieval-Augmented Generation)**.

---

## Estrutura Sugerida

```
src/
├── app.py              # Aplicação principal (Streamlit)
├── agente.py           # Lógica do agente (RAG + failover)
├── config.py           # Configurações (API keys)
└── requirements.txt    # Dependências
```

## Como Rodar

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar a aplicação
streamlit run src/app.py
```

---

## Documentação
Consulte a pasta `docs/` para detalhes sobre caso de uso, arquitetura, prompts, métricas e roteiro do pitch.
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vitor-silva-7418111a2)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/vdfs89)

---
*Projeto desenvolvido como parte dos requisitos para conclusão do bootcamp na plataforma DIO.*
