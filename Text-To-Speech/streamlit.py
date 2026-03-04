import streamlit as st
import base64
import pandas as pd
import json
import sys
import os
from groq import Groq
import google.generativeai as genai
from openai import OpenAI
from gtts import gTTS

st.set_page_config(page_title="FinanceForge", page_icon="💸")

try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
    OPENAI_KEY = st.secrets["OPENAI_API_KEY"]
except KeyError as e:
    st.error(f"Erro: Chave {e} não encontrada no st.secrets. Verifique as configurações.")
    st.stop()


# --- Inicialização dos Clientes ---
client_groq = Groq(api_key=GROQ_KEY)
genai.configure(api_key=GEMINI_KEY)
client_openai = OpenAI(api_key=OPENAI_KEY)


# --- Modularização: Função de leitura dos dados ---
def ler_dados_financeiros():
    try:
        perfil = json.load(open("data/perfil_investidor.json", "r", encoding='utf-8'))
        produtos = json.load(open("data/produtos_financeiros.json", "r", encoding='utf-8'))
        transacoes = pd.read_csv("data/transacoes.csv")
        historico = pd.read_csv("data/historico_atendimento.csv")
        return perfil, produtos, transacoes, historico
    except Exception as e:
        st.error(f"Erro ao ler dados financeiros: {e}")
        return None, None, None, None

# --- Função para montar contexto RAG ---
def montar_contexto_rag():
    perfil, produtos, transacoes, historico = ler_dados_financeiros()
    if perfil is None:
        return "Contexto indisponível."
    saldo = transacoes[transacoes['tipo']=='entrada']['valor'].sum() - transacoes[transacoes['tipo']=='saida']['valor'].sum()
    if historico is not None and 'resumo' in historico.columns and not historico['resumo'].empty:
        historico_resumo = historico['resumo'].iloc[-1]
    else:
        historico_resumo = "Nenhum resumo disponível."
    contexto = f"""
    CLIENTE: {perfil['nome']}, {perfil['idade']} anos, {perfil['profissao']}.
    PERFIL: {perfil['perfil_investidor']}. OBJETIVO: {perfil['objetivo_principal']}.
    SALDO ATUAL: R$ {saldo:.2f}.
    METAS: {[m['meta'] for m in perfil['metas']]}
    HISTÓRICO: {historico_resumo}
    PRODUTOS: {[p['nome'] for p in produtos]}
    """
    return contexto


# --- Modularização: Função de failover ---
def failover_llm(messages):
    try:
        response = client_groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )
        return response.choices[0].message.content, "Groq (Llama)"
    except Exception as e:
        st.warning(f"Groq offline: {e}. Alternando para Gemini...")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"{messages[0]['content']}\n\nUsuário: {messages[-1]['content']}"
        response = model.generate_content(prompt)
        return response.text, "Google Gemini"
    except Exception as e:
        st.warning(f"Gemini offline: {e}. Alternando para OpenAI...")
    try:
        response = client_openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return response.choices[0].message.content, "OpenAI"
    except Exception:
        return "Desculpe, não consegui conectar a nenhum modelo de IA.", "Erro"

def get_ai_response(messages):
    return failover_llm(messages)

def play_audio(text):
    st.markdown("**Transcrição do áudio:**")
    st.write(text)
    voz_lenta = st.session_state.get("voz_lenta", False)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Voz lenta", key="voz_lenta_btn"):
            st.session_state["voz_lenta"] = True
    with col2:
        if st.button("Voz normal", key="voz_normal_btn"):
            st.session_state["voz_lenta"] = False
    try:
        tts = gTTS(text=text, lang='pt', slow=voz_lenta)
        tts.save("voice.mp3")
        with open("voice.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except Exception:
        st.error("Erro ao gerar áudio.")

# --- Interface ---

st.title("💸 FinanceForge: Mentor Financeiro Proativo")

# --- Resumo mensal automático ao abrir o app ---
try:
    transacoes = pd.read_csv("data/transacoes.csv")
    entradas = transacoes[transacoes['tipo'] == 'entrada']['valor'].sum()
    saidas = transacoes[transacoes['tipo'] == 'saida']['valor'].sum()
    saldo = entradas - saidas
    st.info(f"Resumo do mês:")
    st.write(f"Receita: R$ {entradas:.2f}")
    st.write(f"Despesas: R$ {saidas:.2f}")
    st.write(f"Saldo: R$ {saldo:.2f}")
except Exception:
    st.warning("Não foi possível calcular o resumo mensal.")


# --- Atualização dinâmica do contexto RAG ---
def atualizar_contexto_system():
    contexto_rag = montar_contexto_rag()
    return {
        "role": "system",
        "content": (
            "Você é o FinanceForge, um agente financeiro inteligente e proativo. "
            "Baseie suas respostas EXCLUSIVAMENTE nos dados fornecidos abaixo. "
            "Nunca invente informações financeiras. Se não souber algo, admita e peça atualização dos dados. "
            "Seja consultivo, educativo e empático. Responda sempre em português.\n\n"
            f"--- CONTEXTO DO CLIENTE ---\n{contexto_rag}\n---------------------------"
        )
    }

if "messages" not in st.session_state:
    st.session_state.messages = [atualizar_contexto_system()]


# --- Exibir histórico com log do provedor ---
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            # Exibe o provedor se for resposta do agente
            if msg["role"] == "assistant":
                # Busca o provedor na mensagem anterior (se disponível)
                if i > 0:
                    prev = st.session_state.messages[i-1]
                    if isinstance(prev, dict) and "provider" in prev:
                        st.caption(f"Provedor: {prev['provider']}")

if prompt := st.chat_input("Pergunte sobre metas, investimentos, gastos..."):
    # Atualiza o contexto RAG antes de cada pergunta
    st.session_state.messages[0] = atualizar_contexto_system()
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # --- Validação de perguntas fora do escopo e idioma ---
    prompt_lower = prompt.lower()
    escopo_financeiro = ["gasto", "despesa", "transacao", "extrato", "meta", "investimento", "recomendacao", "produto", "saldo", "renda", "reserva", "cdb", "tesouro", "lci", "lca", "fundo"]
    # Verifica se está em português ou inglês
    import langdetect
    try:
        idioma = langdetect.detect(prompt)
    except Exception:
        idioma = "unknown"
    idioma_valido = idioma in ["pt", "en"]
    if not idioma_valido:
        st.warning("O agente só responde perguntas em português ou inglês.")
    elif not any(p in prompt_lower for p in escopo_financeiro):
        st.warning("Pergunta fora do escopo financeiro! O agente só responde sobre finanças pessoais, investimentos, metas e produtos financeiros.")
    else:
        with st.spinner("Consultando mentor financeiro..."):
            resposta, provider = get_ai_response(st.session_state.messages)
        with st.chat_message("assistant"):
            st.markdown(f"**[{provider}]** {resposta}")
            st.session_state.messages.append({"role": "assistant", "content": resposta})
            play_audio(resposta)

        # Sugestões proativas após cada resposta
        st.divider()
        st.markdown("**Sugestões para você continuar:**")
        st.button("Simular aporte mensal para meta de reserva", key="sugestao_aporte")
        st.button("Ver resumo do mês atual", key="sugestao_resumo")
        st.button("Consultar produtos recomendados para meu perfil", key="sugestao_produtos")

    # --- Formatação visual para perguntas sobre gastos, metas ou recomendações ---
    if any(p in prompt_lower for p in ["gasto", "despesa", "transacao", "extrato"]):
        try:
            df = pd.read_csv("data/transacoes.csv")
            st.subheader("Tabela de Gastos Recentes")
            st.dataframe(df)
        except Exception:
            st.warning("Não foi possível exibir a tabela de gastos.")
    if "meta" in prompt_lower:
        try:
            with open("data/perfil_investidor.json", "r", encoding='utf-8') as f:
                perfil = json.load(f)
            metas = pd.DataFrame(perfil["metas"])
            st.subheader("Metas Financeiras")
            st.dataframe(metas)
        except Exception:
            st.warning("Não foi possível exibir a tabela de metas.")
    if any(p in prompt_lower for p in ["investimento", "recomendacao", "produto"]):
        try:
            with open("data/produtos_financeiros.json", "r", encoding='utf-8') as f:
                produtos = json.load(f)
            produtos_df = pd.DataFrame(produtos)
            st.subheader("Catálogo de Produtos Financeiros")
            st.dataframe(produtos_df)
        except Exception:
            st.warning("Não foi possível exibir a tabela de produtos.")