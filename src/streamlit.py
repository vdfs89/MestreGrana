
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
import speech_recognition as sr
import tempfile
import streamlit_webrtc as webrtc
import matplotlib.pyplot as plt
import numpy as np
import requests
from datetime import datetime
from dotenv import load_dotenv

try:
    import psycopg2
except Exception:
    psycopg2 = None

try:
    from pymongo import MongoClient
except Exception:
    MongoClient = None

# Carrega variaveis locais do .env (na nuvem, st.secrets prevalece)
load_dotenv()

# Busca as chaves primeiro em st.secrets, depois em variáveis de ambiente
def get_secret_or_env(key):
    try:
        return st.secrets[key]
    except Exception:
        return os.environ.get(key)


@st.cache_resource
def init_postgres_connection():
    db_url = get_secret_or_env("DATABASE_URL")
    if not db_url:
        return None
    if psycopg2 is None:
        raise RuntimeError("Dependencia psycopg2-binary nao instalada")
    return psycopg2.connect(db_url)


@st.cache_data(ttl=300)
def get_postgres_version():
    conn = init_postgres_connection()
    if conn is None:
        return None
    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        row = cur.fetchone()
    return row[0] if row else None


atlas_status = "⚪ Não configurado"
atlas_enabled = False
neon_status = "⚪ Não configurado"
mongo_client = None
mongo_db = None
produtos_collection = None
usuarios_collection = None
transacoes_collection = None
feedbacks_collection = None
historico_collection = None

MONGO_URI = get_secret_or_env("MONGODB_ATLAS_URI")
if MONGO_URI and MongoClient:
    try:
        mongo_client = MongoClient(MONGO_URI, tls=True, serverSelectionTimeoutMS=5000)
        mongo_db = mongo_client["InvestimentoDIO"]
        mongo_db.command("ping")
        produtos_collection = mongo_db["produtos"]
        usuarios_collection = mongo_db["usuarios"]
        transacoes_collection = mongo_db["transacoes"]
        feedbacks_collection = mongo_db["feedbacks"]
        historico_collection = mongo_db["historico"]
        atlas_enabled = True
        atlas_status = "🟢 Online"
    except Exception:
        atlas_status = "🔴 Offline"
elif MONGO_URI and not MongoClient:
    atlas_status = "🟠 pymongo ausente"

DATABASE_URL = get_secret_or_env("DATABASE_URL")
if DATABASE_URL:
    try:
        _ = get_postgres_version()
        neon_status = "🟢 Online"
    except Exception:
        neon_status = "🔴 Offline"
elif not DATABASE_URL:
    neon_status = "⚪ Não configurado"

st.set_page_config(page_title="MestreGrana", page_icon="💸")
st.sidebar.markdown(f"**Status Atlas:** {atlas_status}")
st.sidebar.markdown(f"**Status Neon:** {neon_status}")
st.sidebar.markdown("**Status LLM:** 🟢 Online")

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
@st.cache_data(ttl=600)
def carregar_perfil_investidor():
    with open("data/perfil_investidor.json", "r", encoding='utf-8') as f:
        return json.load(f)

@st.cache_data(ttl=600)
def carregar_produtos_financeiros():
    with open("data/produtos_financeiros.json", "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data(ttl=300)
def carregar_transacoes_csv():
    return pd.read_csv("data/transacoes.csv")

@st.cache_data(ttl=300)
def carregar_historico_atendimento():
    return pd.read_csv("data/historico_atendimento.csv")

def ler_dados_financeiros():
    try:
        perfil = carregar_perfil_investidor()
        if atlas_enabled and produtos_collection is not None:
            # Busca produtos diretamente do MongoDB Atlas
            produtos_cursor = produtos_collection.find()
            produtos = list(produtos_cursor)
            # Remove o campo '_id' do MongoDB para evitar problemas ao criar DataFrame
            for p in produtos:
                p.pop('_id', None)
        else:
            produtos = carregar_produtos_financeiros()
        conn_pg = init_postgres_connection()
        if conn_pg:
            transacoes = pd.read_sql("SELECT * FROM transactions", conn_pg)
        else:
            transacoes = carregar_transacoes_csv()
        historico = carregar_historico_atendimento()
        return perfil, produtos, transacoes, historico
    except Exception as e:
        st.error(f"Erro ao ler dados financeiros: {e}")
        return None, None, None, None

# --- DASHBOARD ANALÍTICO ---
def mostrar_dashboard():
    st.title("📊 Dashboard Financeiro Avançado")
    perfil, produtos, transacoes, historico = ler_dados_financeiros()
    if perfil is None:
        st.warning("Dados não disponíveis para o dashboard.")
        return

    # KPIs principais
    saldo_total = perfil.get("saldo", 0)
    total_investido = sum([m.get("valor", 0) for m in perfil.get("metas", [])])
    total_produtos = len(produtos) if produtos else 0
    total_transacoes = len(transacoes) if transacoes is not None else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Saldo Atual", f"R$ {saldo_total:,.2f}")
    col2.metric("Total Investido (Metas)", f"R$ {total_investido:,.2f}")
    col3.metric("Produtos Financeiros", total_produtos)
    col4.metric("Transações", total_transacoes)

    st.markdown("---")

    # Gráfico de evolução do saldo
    if historico is not None and "data" in historico.columns and "saldo" in historico.columns:
        st.subheader("Evolução do Saldo")
        fig, ax = plt.subplots()
        historico.plot(x="data", y="saldo", ax=ax, marker="o", color="#4F8A10")
        ax.set_ylabel("Saldo (R$)")
        ax.set_xlabel("Data")
        st.pyplot(fig)

    # Gráfico de distribuição de gastos
    if transacoes is not None and "categoria" in transacoes.columns and "valor" in transacoes.columns:
        st.subheader("Gastos por Categoria")
        gastos_categoria = transacoes[transacoes["tipo"]=="saida"].groupby("categoria")["valor"].sum().sort_values()
        fig2, ax2 = plt.subplots()
        gastos_categoria.plot(kind="barh", ax=ax2, color="#FFB347")
        ax2.set_xlabel("Valor (R$)")
        ax2.set_ylabel("Categoria")
        st.pyplot(fig2)

    # Filtro de produtos financeiros
    if produtos:
        st.subheader("Catálogo de Produtos Financeiros")
        filtro_tipo = st.selectbox("Filtrar por tipo", ["Todos"] + sorted(set([p.get("tipo", "") for p in produtos])))
        if filtro_tipo != "Todos":
            produtos_filtrados = [p for p in produtos if p.get("tipo", "") == filtro_tipo]
        else:
            produtos_filtrados = produtos
        st.dataframe(pd.DataFrame(produtos_filtrados))

    st.markdown("---")
    st.info("Dashboard alimentado em tempo real pelo MongoDB Atlas e dados locais. KPIs, gráficos e filtros para análise financeira completa.")
# --- Exibição do dashboard na barra lateral ---
with st.sidebar:
    st.header("Navegação")
    pagina = st.radio("Escolha a página:", ["Assistente", "Dashboard"])

if pagina == "Dashboard":
    mostrar_dashboard()

# --- Função para montar contexto RAG ---
def montar_contexto_rag():
    import requests

    # --- Login simples ---
    st.header("Login rápido")
    with st.form("login_form"):
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        submit = st.form_submit_button("Entrar")
        if submit and nome and email:
            try:
                ip = requests.get("https://api.ipify.org").text
                if atlas_enabled and usuarios_collection is not None and historico_collection is not None:
                    # Verifica duplicidade de email ou IP
                    usuario_existente = usuarios_collection.find_one({"$or": [{"email": email}, {"ip": ip}]})
                    if usuario_existente:
                        st.warning("Usuário já cadastrado com este email ou IP. Seu histórico será carregado.")
                    else:
                        usuarios_collection.insert_one(
                            {"nome": nome, "email": email, "ip": ip, "data": pd.Timestamp.now()}
                        )
                        st.success(f"Bem-vindo, {nome}! Seu acesso foi registrado.")

                    # Salva histórico de login
                    historico_collection.insert_one(
                        {"usuario": nome, "email": email, "acao": "login", "ip": ip, "data": pd.Timestamp.now()}
                    )

                    # Carrega histórico do usuário
                    historico_usuario = list(
                        historico_collection.find({"usuario": nome, "email": email}).sort("data", -1)
                    )
                    if historico_usuario:
                        st.info("Seu histórico de acessos:")
                        for h in historico_usuario:
                            st.write(f"{h['acao']} em {h['data']:%d/%m/%Y %H:%M} - IP: {h.get('ip','-')}")
                    else:
                        st.info("Nenhum histórico encontrado.")
                else:
                    # Fallback local sem persistência em banco
                    if "historico_login_local" not in st.session_state:
                        st.session_state["historico_login_local"] = []
                    st.session_state["historico_login_local"].append(
                        {"usuario": nome, "email": email, "acao": "login", "ip": ip, "data": datetime.now()}
                    )
                    st.success(f"Bem-vindo, {nome}! Login registrado localmente (Atlas indisponível).")
                    st.info("Histórico local da sessão:")
                    for h in reversed(st.session_state["historico_login_local"][-5:]):
                        st.write(f"{h['acao']} em {h['data']:%d/%m/%Y %H:%M} - IP: {h.get('ip','-')}")
            except Exception as e:
                st.error(f"Erro ao registrar login: {e}")
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


# --- 1. A Batalha de Modelos (Groq vs Gemini) ---
def gerar_respostas_candidatas(messages):
    """Pede respostas para Groq e Gemini."""
    respostas = {}

    try:
        resp_groq = client_groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        ).choices[0].message.content
        respostas["Groq (Llama 3)"] = resp_groq
    except Exception as e:
        print(f"Groq falhou: {e}")

    try:
        prompt_text = f"{messages[0]['content']}\n\nUsuário: {messages[-1]['content']}"
        model = genai.GenerativeModel('gemini-1.5-flash')
        resp_gemini = model.generate_content(prompt_text).text
        respostas["Google Gemini"] = resp_gemini
    except Exception as e:
        print(f"Gemini falhou: {e}")

    return respostas


# --- 2. O Juiz Implacável (OpenAI) ---
def auditor_juiz_multimodelo(pergunta, respostas_candidatas, contexto):
    """O GPT-4o-mini avalia as respostas candidatas e elege a campeã."""
    prompt_auditor = f"""
    Você é o Juiz Sênior da Receita Federal e Auditor Financeiro Chefe.
    Sua tarefa é avaliar pareceres de dois consultores IA e escolher o MAIS SEGURO e EXATO.

    DADOS DO CLIENTE E REGRAS TRIBUTÁRIAS: {contexto}
    PERGUNTA DO CLIENTE: {pergunta}

    RESPOSTAS DOS CONSULTORES:
    """

    for provedor, texto in respostas_candidatas.items():
        prompt_auditor += f"\n--- [{provedor}] ---\n{texto}\n"

    prompt_auditor += """
    Critérios de Avaliação:
    1. Zero alucinação (não inventar saldo ou transações).
    2. Precisão nas regras do Imposto de Renda (IRPF).
    3. Empatia e clareza.

    Responda APENAS com um JSON estrito neste formato:
    {
      "aprovado": true_ou_false,
      "provedor_vencedor": "Nome do provedor que deu a melhor resposta",
      "motivo": "Explicação curta do porquê ele venceu",
      "resposta_final": "A cópia exata da resposta vencedora (pode fazer pequenas correções tributárias se necessário)"
    }

    Se TODAS as respostas forem perigosas ou inventarem dados, marque "aprovado": false e explique o motivo.
    """

    try:
        response = client_openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt_auditor}],
            response_format={"type": "json_object"},
            temperature=0.0
        )
        veredito = json.loads(response.choices[0].message.content)
        return (
            veredito.get("aprovado", False),
            veredito.get("provedor_vencedor", ""),
            veredito.get("motivo", ""),
            veredito.get("resposta_final", "")
        )
    except Exception as e:
        return False, "", f"Erro no Tribunal da IA: {e}", ""


def executar_mesa_redonda(messages, pergunta, contexto_atual):
    respostas_candidatas = gerar_respostas_candidatas(messages)

    if not respostas_candidatas:
        return False, "Erro de Conexão", "Desculpe, meus servidores estão offline no momento.", "Sem respostas candidatas"

    aprovado, vencedor, motivo, melhor_resposta = auditor_juiz_multimodelo(
        pergunta, respostas_candidatas, contexto_atual
    )

    if aprovado:
        provider = f"🏆 {vencedor} (Auditado por OpenAI)"
        print(f"O Juiz escolheu {vencedor} porque: {motivo}")
        return True, provider, melhor_resposta, motivo

    resposta_bloqueada = (
        "⚠️ **Alerta de Segurança Fiscal:** Meus consultores geraram análises inconsistentes "
        "com as regras da Receita Federal para a sua pergunta. "
        "Para proteger sua declaração de IRPF, a resposta foi bloqueada."
    )
    provider = f"Sistema de Segurança 🛑 (Motivo: {motivo})"
    print(f"Bloqueio duplo! {motivo}")
    return False, provider, resposta_bloqueada, motivo

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

# --- Função para gerar áudio usando Orpheus TTS (Groq/Canopy Labs) ---
def gerar_audio_groq(texto, voice="autumn", style="excited", api_key=None):
    url = "https://api.canopylabs.com/orpheus/tts"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    # Voz autumn é uma das mais naturais; style expressive deixa mais fluente
    payload = {
        "text": texto,
        "voice": "autumn",  # Recomendada para voz humana
        "style": "expressive",  # Mais fluente e natural
        "language": "pt"  # Se disponível, usa português
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        with open("resposta_groq.mp3", "wb") as f:
            f.write(response.content)
        return "resposta_groq.mp3"
    else:
        st.error(f"Erro ao gerar áudio Groq: {response.text}")
        return None

# --- Interface ---

st.title("💸 MestreGrana: Mentor Financeiro Proativo")
# Inicializa o histórico de mensagens para evitar erro
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.subheader("Chat de Voz com IA")
st.info("Clique em 'Start' para ativar o microfone e fale sua pergunta. Quando terminar, clique em 'Stop'. Aguarde a transcrição e resposta.")

webrtc_ctx = webrtc.webrtc_streamer(
    key="voice-chat",
    mode=webrtc.WebRtcMode.SENDRECV,
    audio_receiver_size=256,
    media_stream_constraints={"audio": True, "video": False},
    async_processing=True,
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    },
)
transcricao = st.empty()
resposta_box = st.empty()
if webrtc_ctx.audio_receiver:
    st.info("🔴 Gravando...")
    import queue
    audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
    if audio_frames:
        st.info("Processando áudio...")
        audio = audio_frames[0].to_ndarray()
        import soundfile as sf
        import numpy as np
        tmp_audio_path = "temp_voice.wav"
        sf.write(tmp_audio_path, audio, 16000)
        recognizer = sr.Recognizer()
        with sr.AudioFile(tmp_audio_path) as source:
            audio_data = recognizer.record(source)
        try:
            texto = recognizer.recognize_google(audio_data, language="pt-BR")
            transcricao.success(f"Transcrição: {texto}")
        except Exception as e:
            transcricao.error(f"Não foi possível transcrever o áudio: {e}")
            texto = ""
        if texto:
            st.session_state.messages.append({"role": "user", "content": texto})
            contexto_atual = st.session_state.messages[0]["content"] if st.session_state.messages else ""
            aprovado, provedor, resposta, _ = executar_mesa_redonda(
                st.session_state.messages,
                texto,
                contexto_atual,
            )
            resposta_box.success(f"Resposta ({provedor}): {resposta}")
            # No bloco de resposta em áudio
            if aprovado:
                api_key_groq = get_secret_or_env("GROQ_TTS_API_KEY")
                audio_path = gerar_audio_groq(resposta, voice="autumn", style="excited", api_key=api_key_groq)
                if audio_path:
                    with open(audio_path, "rb") as f:
                        data = f.read()
                        b64 = base64.b64encode(data).decode()
                        st.markdown(f'<audio controls src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
                else:
                    st.warning("Erro ao gerar áudio da resposta.")

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
    perfil, produtos, transacoes, _ = ler_dados_financeiros()

    dedutiveis_keywords = {
        "medico", "consulta", "saude", "hospital", "clinica", "plano de saude",
        "faculdade", "graduacao", "pos", "mestrado", "doutorado", "educacao"
    }
    resumo_deducoes = "Nenhuma despesa potencialmente dedutível identificada no período."
    if transacoes is not None and "tipo" in transacoes.columns and "categoria" in transacoes.columns and "valor" in transacoes.columns:
        despesas = transacoes[transacoes["tipo"] == "saida"].copy()
        if not despesas.empty:
            despesas["categoria_norm"] = despesas["categoria"].astype(str).str.lower()
            mask = despesas["categoria_norm"].apply(lambda c: any(k in c for k in dedutiveis_keywords))
            dedutiveis = despesas[mask]
            if not dedutiveis.empty:
                total_dedutivel = dedutiveis["valor"].sum()
                categorias = sorted(set(dedutiveis["categoria"].astype(str).tolist()))
                resumo_deducoes = (
                    f"Total potencialmente dedutível: R$ {total_dedutivel:.2f}. "
                    f"Categorias encontradas: {categorias}."
                )

    return {
        "role": "system",
        "content": (
            "Você é o MestreGrana, um conselheiro financeiro inteligente e especialista em Imposto de Renda da Pessoa Física (IRPF) focado no Brasil. "
            "Seu objetivo é ajudar o usuário a organizar suas finanças diárias e facilitar a declaração anual de impostos. "
            "\n\n"
            "Tom de voz: amigável, direto, didático e encorajador. "
            "Explique termos financeiros e tributários complexos de forma simples. "
            "\n\n"
            "Funções principais:\n"
            "1) Análise de gastos e alertas de orçamento.\n"
            "2) Radar de deduções: identificar despesas potencialmente dedutíveis e lembrar de guardar comprovantes.\n"
            "3) Guia do IRPF: indicar a ficha correta da Receita para cada item.\n"
            "\n"
            "Regras tributárias que você domina:\n"
            "- Saúde é dedutível sem limite legal específico na declaração, desde que comprovada.\n"
            "- Educação dedutível com limite anual legal (ensino regular). Cursos livres não são dedutíveis.\n"
            "- Verbas rescisórias, FGTS e PDV são isentos, mas devem constar em Rendimentos Isentos e Não Tributáveis.\n"
            "\n"
            "Sempre baseie as respostas EXCLUSIVAMENTE nos dados fornecidos. "
            "Nunca invente informações financeiras. Se não souber, admita e peça atualização dos dados. "
            "Responda sempre em português.\n\n"
            f"--- CONTEXTO DO CLIENTE ---\n{contexto_rag}\n"
            f"--- RESUMO IRPF (PRÉ-ANÁLISE) ---\n{resumo_deducoes}\n"
            "---------------------------\n\n"
            "Aviso legal obrigatório: você é um assistente de IA e casos tributários específicos podem exigir orientação de contador."
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
    escopo_financeiro = [
        "gasto", "despesa", "transacao", "extrato", "meta", "investimento", "recomendacao", "produto", "saldo", "renda", "reserva", "cdb", "tesouro", "lci", "lca", "fundo",
        "levantar dinheiro", "poupar", "economizar", "guardar", "renda extra", "ganhar dinheiro", "CDI", "como investir", "dinheiro para investir", "educação financeira", "planejamento financeiro"
    ]
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
        # Novo filtro: aceita se qualquer palavra do escopo aparecer na pergunta
        palavras = prompt_lower.split()
        if not any(any(p in palavra for p in escopo_financeiro) for palavra in palavras):
            st.warning("Pergunta fora do escopo financeiro! O agente só responde sobre finanças pessoais, investimentos, metas e produtos financeiros.")
        else:
            with st.spinner("Consultando mentor financeiro..."):
                contexto_atual = st.session_state.messages[0]["content"] if st.session_state.messages else ""
                aprovado, provider, resposta, _ = executar_mesa_redonda(
                    st.session_state.messages,
                    prompt,
                    contexto_atual,
                )
            with st.chat_message("assistant"):
                st.markdown(f"**[{provider}]** {resposta}")
                st.session_state.messages.append({"role": "assistant", "content": resposta, "provider": provider})
                if aprovado:
                    play_audio(resposta)
            st.divider()
            st.markdown("**Sugestões para você continuar:**")
            if st.button("Simular aporte mensal para meta de reserva", key="sugestao_aporte"):
                resposta = "Para simular um aporte mensal, informe o valor desejado e o prazo da sua meta. O sistema irá calcular quanto você precisa investir por mês para atingir seu objetivo."
                st.markdown(f"**[Sugestão]** {resposta}")
                play_audio(resposta)
            if st.button("Ver resumo do mês atual", key="sugestao_resumo"):
                resposta = "Aqui está o resumo do seu mês: entradas, saídas, saldo final e principais categorias de gastos. Para detalhes, acesse a tabela de transações."
                st.markdown(f"**[Sugestão]** {resposta}")
                play_audio(resposta)
            if st.button("Consultar produtos recomendados para meu perfil", key="sugestao_produtos"):
                resposta = "Com base no seu perfil, os produtos recomendados são exibidos na tabela abaixo. Avalie as opções e compare rentabilidades, prazos e riscos."
                st.markdown(f"**[Sugestão]** {resposta}")
                play_audio(resposta)

    # --- Formatação visual para perguntas sobre gastos, metas ou recomendações ---
    if any(p in prompt_lower for p in ["gasto", "despesa", "transacao", "extrato"]):
        try:
            df = carregar_transacoes_csv()
            st.subheader("Tabela de Gastos Recentes")
            st.dataframe(df)
            # Gráfico de barras dos gastos por categoria
            if "categoria" in df.columns and "valor" in df.columns:
                gastos_categoria = df[df["tipo"]=="saida"].groupby("categoria")["valor"].sum().sort_values()
                st.subheader("Distribuição dos Gastos por Categoria")
                fig, ax = plt.subplots()
                gastos_categoria.plot(kind="barh", ax=ax, color="#FFB347")
                ax.set_xlabel("Valor (R$)")
                ax.set_ylabel("Categoria")
                ax.set_title("Gastos por Categoria")
                st.pyplot(fig)
        except Exception:
            st.warning("Não foi possível exibir a tabela de gastos.")
    if "meta" in prompt_lower:
        try:
            perfil = carregar_perfil_investidor()
            metas = pd.DataFrame(perfil["metas"])
            st.subheader("Metas Financeiras")
            st.dataframe(metas)
        except Exception:
            st.warning("Não foi possível exibir a tabela de metas.")
    if any(p in prompt_lower for p in ["investimento", "recomendacao", "produto"]):
        try:
            produtos = carregar_produtos_financeiros()
            produtos_df = pd.DataFrame(produtos)
            st.subheader("Catálogo de Produtos Financeiros")
            st.dataframe(produtos_df)
        except Exception:
            st.warning("Não foi possível exibir a tabela de produtos.")

    # Resposta padrão para perguntas sobre CDI
    if "cdi" in prompt_lower:
        resposta = (
            "CDI significa Certificado de Depósito Interbancário. São títulos emitidos por bancos para financiar suas operações diárias entre si, com duração de um dia útil. Para o investidor, o CDI é o principal benchmark de renda fixa, indicando o rendimento de produtos como CDBs, LCIs e LCAs, geralmente acompanhando de perto a taxa Selic.\n\n"
            "Pontos-chave sobre o CDI:\n"
            "- Finalidade: Os bancos usam o CDI para equilibrar o caixa no final do dia, garantindo que o saldo não fique negativo.\n"
            "- Rendimento: Um investimento de '100% do CDI' significa que ele rende exatamente a taxa CDI, que tende a superar a poupança.\n"
            "- Influência da Selic: O CDI caminha junto com a taxa Selic; se a Selic sobe, o CDI sobe, aumentando a rentabilidade da renda fixa.\n"
            "- Exemplos de Investimentos: CDBs, LCIs, LCAs e contas de pagamento (como Nubank, Banco Inter).\n\n"
            "O CDI é fundamental para entender o retorno de aplicações de baixo risco, servindo como uma base para comparar se um investimento está valendo a pena."
        )
        provider = "Resposta padrão"
        with st.chat_message("assistant"):
            st.markdown(f"**[{provider}]** {resposta}")
            st.session_state.messages.append({"role": "assistant", "content": resposta})
            play_audio(resposta)
        st.divider()
        st.markdown("**Sugestões para você continuar:**")
    else:
        with st.spinner("Consultando Llama e Gemini... passando pelo Juiz (GPT-4)..."):
            contexto_atual = st.session_state.messages[0]["content"] if st.session_state.messages else ""
            aprovado, provider, resposta, _ = executar_mesa_redonda(
                st.session_state.messages,
                prompt,
                contexto_atual,
            )
        with st.chat_message("assistant"):
            st.markdown(f"**[{provider}]** {resposta}")
            st.session_state.messages.append({"role": "assistant", "content": resposta, "provider": provider})
            if aprovado:
                play_audio(resposta)
        st.divider()
        st.markdown("**Sugestões para você continuar:**")
        st.button("Simular aporte mensal para meta de reserva", key="sugestao_aporte")
        st.button("Ver resumo do mês atual", key="sugestao_resumo")
        st.button("Consultar produtos recomendados para meu perfil", key="sugestao_produtos")


# --- Histórico de conversas ---
st.subheader("Histórico de Conversas")

# Filtra as mensagens em tempo real sem duplicar
chat_history = [msg for msg in st.session_state.messages if msg["role"] != "system"]

if chat_history:
    for i, msg in enumerate(chat_history):
        st.markdown(f"**{msg['role'].capitalize()}:** {msg['content']}")
    if st.button("Exportar histórico (CSV)"):
        import pandas as pd
        df_hist = pd.DataFrame(chat_history)
        st.download_button("Baixar histórico CSV", df_hist.to_csv(index=False), "historico_chat.csv", mime="text/csv")


# Feedback do usuário
st.subheader("Deixe seu feedback!")
feedback = st.text_area("O que achou do app? Sugestões, elogios ou críticas:")
if st.button("Enviar feedback"):
    if feedback:
        with open("feedbacks.txt", "a", encoding="utf-8") as f:
            f.write(feedback + "\n---\n")
        st.success("Obrigado pelo seu feedback! Sua opinião é fundamental para evoluirmos o MestreGrana.")
    else:
        st.warning("Digite algo antes de enviar.")

# Exibir feedbacks anteriores (opcional)
if st.button("Ver feedbacks recebidos"):
    try:
        with open("feedbacks.txt", "r", encoding="utf-8") as f:
            conteudo = f.read()
        st.text_area("Feedbacks recebidos:", value=conteudo, height=200)
    except Exception:
        st.info("Nenhum feedback recebido ainda.")