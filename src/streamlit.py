import streamlit as st
import base64
import pandas as pd
import json
import sys
import os
from groq import Groq
import google.genai as genai
from openai import OpenAI
from gtts import gTTS

st.set_page_config(page_title="FinanceForge", page_icon="💸")


# Busca as chaves primeiro em st.secrets, depois em variáveis de ambiente
def get_secret_or_env(key):
    try:
        return st.secrets[key]
    except Exception:
        return os.environ.get(key)

GROQ_KEY = get_secret_or_env("GROQ_API_KEY")
GEMINI_KEY = get_secret_or_env("GEMINI_API_KEY")
OPENAI_KEY = get_secret_or_env("OPENAI_API_KEY")

if not GROQ_KEY or not GEMINI_KEY or not OPENAI_KEY:
    st.error("Erro: Uma ou mais chaves de API não foram encontradas em st.secrets ou no ambiente (.env). Verifique as configurações.")
    st.stop()


# --- Inicialização dos Clientes ---
client_groq = Groq(api_key=GROQ_KEY)
genai.API_KEY = GEMINI_KEY
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
if 'show_form' not in st.session_state:
    st.session_state['show_form'] = False

if st.button("Informar receita e despesas do mês"):
    st.session_state['show_form'] = True

if st.session_state['show_form']:
    with st.form("form_resumo_mes"):
        st.subheader("1. Resumo do Mês")
        mes_ano = st.text_input("Mês/Ano", value="03/2026")
        receita_esperada = st.number_input("Receita Total Esperada (R$)", min_value=0.0, format="%.2f")
        receita_realizada = st.number_input("Receita Total Realizada (R$)", min_value=0.0, format="%.2f")
        despesas = st.number_input("Despesas Totais (R$)", min_value=0.0, format="%.2f")
        saldo = receita_realizada - despesas

        st.subheader("2. Receitas (O que entra)")
        salario = st.number_input("Salário Líquido (R$)", min_value=0.0, format="%.2f")
        renda_extra = st.number_input("Renda Extra / Freela (R$)", min_value=0.0, format="%.2f")
        outros_receita = st.number_input("Outros (Dividendos/Restituição) (R$)", min_value=0.0, format="%.2f")
        total_receitas = salario + renda_extra + outros_receita

        st.subheader("3. Gastos Fixos - Necessidades (Meta: 50%)")
        aluguel = st.number_input("Aluguel/Financiamento (R$)", min_value=0.0, format="%.2f")
        condominio = st.number_input("Condomínio / IPTU (R$)", min_value=0.0, format="%.2f")
        energia = st.number_input("Energia / Água / Gás (R$)", min_value=0.0, format="%.2f")
        internet = st.number_input("Internet / Celular (R$)", min_value=0.0, format="%.2f")
        supermercado = st.number_input("Supermercado (Essencial) (R$)", min_value=0.0, format="%.2f")
        saude = st.number_input("Plano de Saúde / Medicamentos (R$)", min_value=0.0, format="%.2f")
        educacao = st.number_input("Educação / Escola (R$)", min_value=0.0, format="%.2f")
        total_fixos = aluguel + condominio + energia + internet + supermercado + saude + educacao

        st.subheader("4. Gastos Variáveis - Estilo de Vida (Meta: 30%)")
        streaming = st.number_input("Streaming (Netflix/Spotify) (R$)", min_value=0.0, format="%.2f")
        delivery = st.number_input("Delivery / Restaurantes (R$)", min_value=0.0, format="%.2f")
        transporte = st.number_input("Transporte (Apps/Combustível) (R$)", min_value=0.0, format="%.2f")
        hobbies = st.number_input("Compras / Hobbies (R$)", min_value=0.0, format="%.2f")
        estetica = st.number_input("Salão / Estética (R$)", min_value=0.0, format="%.2f")
        total_variaveis = streaming + delivery + transporte + hobbies + estetica

        st.subheader("5. Futuro - Dívidas e Investimentos (Meta: 20%)")
        dividas = st.number_input("Pagamento de Dívidas (R$)", min_value=0.0, format="%.2f")
        reserva = st.number_input("Reserva de Emergência (R$)", min_value=0.0, format="%.2f")
        investimentos = st.number_input("Aporte em Investimentos (R$)", min_value=0.0, format="%.2f")
        total_futuro = dividas + reserva + investimentos

        st.subheader("6. Controle de Cartão de Crédito")
        vencimento_cartao = st.text_input("Vencimento do Cartão")
        valor_fatura = st.number_input("Valor da Fatura (R$)", min_value=0.0, format="%.2f")

        submitted = st.form_submit_button("Calcular e baixar modelo")

    if submitted:
        st.info(f"Resumo do mês: {mes_ano}")
        st.write(f"Receita Esperada: R$ {receita_esperada:.2f}")
        st.write(f"Receita Realizada: R$ {receita_realizada:.2f}")
        st.write(f"Despesas Totais: R$ {despesas:.2f}")
        st.write(f"Saldo Final: R$ {saldo:.2f}")
        st.write(f"Total Receitas: R$ {total_receitas:.2f}")
        st.write(f"Total Gastos Fixos: R$ {total_fixos:.2f}")
        st.write(f"Total Gastos Variáveis: R$ {total_variaveis:.2f}")
        st.write(f"Total Futuro: R$ {total_futuro:.2f}")
        st.write(f"Valor Fatura Cartão: R$ {valor_fatura:.2f}")
        csv_modelo = gerar_modelo_csv_50_30_20(
            receita=receita_esperada,
            despesas=despesas,
            saldo=saldo,
            mes_ano=mes_ano
        )
        st.download_button(
            label="Baixar modelo preenchido (.csv)",
            data=csv_modelo,
            file_name="resumo_50-30-20.csv",
            mime="text/csv"
        )


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
                    "Você é o MestreGrana, um agente financeiro inteligente e proativo. "
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


def gerar_modelo_csv_50_30_20(receita=0.0, despesas=0.0, saldo=0.0, mes_ano=""): 
    import io
    modelo_csv = io.StringIO()
    modelo_csv.write(f"Resumo do Mês:,{mes_ano}\nReceita Total Esperada:,R$ {receita:.2f}\nReceita Total Realizada:,R$ {receita:.2f}\nSaldo Final (Receita - Gastos):,R$ {saldo:.2f}\n\n")
    modelo_csv.write("Receitas (O que entra)\nItem,Planejado (R$),Realizado (R$)\nSalário Líquido,,\nRenda Extra / Freela,,\nOutros (Dividendos/Restituição),,\nTotal Receitas,R$ 0,00,R$ 0,00\n\n")
    modelo_csv.write("Gastos Fixos - Necessidades (Meta: 50%)\nDescrição,Valor (R$),Vencimento,Status (PAGO?)\nAluguel/Financiamento,,,[]\nCondomínio / IPTU,,,[]\nEnergia / Água / Gás,,,[]\nInternet / Celular,,,[]\nSupermercado (Essencial),,,[]\nPlano de Saúde / Medicamentos,,,[]\nEducação / Escola,,,[]\n\n")
    modelo_csv.write("Gastos Variáveis - Estilo de Vida (Meta: 30%)\nDescrição,Valor (R$),Categoria\nStreaming (Netflix/Spotify),,Lazer\nDelivery / Restaurantes,,Lazer\nTransporte (Apps/Combustível),,Rotina\nCompras / Hobbies,,Desejo\nSalão / Estética,,Pessoal\n\n")
    modelo_csv.write("Futuro - Dívidas e Investimentos (Meta: 20%)\nDescrição,Valor (R$),Objetivo\nPagamento de Dívidas,,Quitação\nReserva de Emergência,,Segurança\nAporte em Investimentos,,Aposentadoria/Bens\n\n")
    modelo_csv.write("Controle de Cartão de Crédito\nVencimento:,\nValor da Fatura:,R$\n\n")
    modelo_csv.write("Próximos Passos Sugeridos:\nLevantamento: Olhe seu extrato bancário dos últimos 30 dias para preencher a coluna 'Realizado'.\nAjuste: Se a soma das 'Necessidades' passar de 50%, veja o que pode ser cortado no 'Estilo de Vida'.\nHábito: Reserve 10 minutos por semana para atualizar esses valores.\n")
    modelo_csv.seek(0)
    return modelo_csv.getvalue()