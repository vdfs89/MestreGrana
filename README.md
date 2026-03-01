# 💰 Finanças do Zero: Mentor de Liberdade com IA Resiliente

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-f55036?style=for-the-badge)

Este repositório contém o projeto final desenvolvido para o bootcamp da **DIO (Digital Innovation One)**. O projeto evoluiu de uma simples curadoria de dados para uma aplicação de **IA de Alta Disponibilidade**, focada em democratizar a educação financeira.

## 🚀 Sobre o Projeto

O **Finanças do Zero** é um mentor digital que utiliza a técnica de **RAG (Retrieval-Augmented Generation)** para guiar o usuário desde a organização do orçamento básico até os primeiros passos em investimentos, garantindo respostas seguras e baseadas em dados curados.

## 🛠️ Engenharia de Software e Diferenciais Técnicos

Diferente de implementações convencionais, este projeto foi desenvolvido com foco em **resiliência e segurança**, aplicando conceitos fundamentais da Ciência da Computação:

* **Arquitetura de Failover (Contingência):** O sistema implementa uma hierarquia de modelos de linguagem (LLMs). Caso o provedor principal (**Groq/Llama 3.3**) apresente instabilidade ou limite de quota, o sistema alterna automaticamente para o **Google Gemini 1.5 Flash**, e em última instância para o **OpenAI GPT-4o-mini**.
* **Gestão Segura de Credenciais:** Utilização de `st.secrets` para o gerenciamento de chaves de API, seguindo as melhores práticas de segurança e evitando a exposição de dados sensíveis no controle de versão.
* **Pipeline de Voz Integrado:** Conversão de texto para fala (TTS) via **gTTS**, proporcionando uma experiência de usuário mais fluida e acessível.

## 🧠 Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **Interface:** Streamlit
* **IA e Modelos:** * Llama 3.3 (via Groq) - *Alta performance e baixa latência*
    * Gemini 1.5 Flash (Google AI) - *Resiliência e contexto amplo*
    * GPT-4o-mini (OpenAI) - *Estabilidade de fallback*
* **Contexto:** Google NotebookLM (Curadoria de RAG)

## ⚙️ Instalação e Execução

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/vdfs89/financas-do-zero.git](https://github.com/vdfs89/financas-do-zero.git)
    cd financas-do-zero
    ```

2.  **Configure as chaves de API:**
    Crie uma pasta `.streamlit` e um arquivo `secrets.toml` dentro dela:
    ```toml
    GROQ_API_KEY = "sua_chave_aqui"
    GEMINI_API_KEY = "sua_chave_aqui"
    OPENAI_API_KEY = "sua_chave_aqui"
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Inicie a aplicação:**
    ```bash
    streamlit run app.py
    ```

## 👤 Desenvolvedor

**Vitor Silva** *Estudante de Ciência da Computação | Desenvolvedor Full-Stack & IA Enthusiast*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vitor-silva-7418111a2)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/vdfs89)

---
*Projeto desenvolvido como parte dos requisitos para conclusão do bootcamp na plataforma DIO.*
