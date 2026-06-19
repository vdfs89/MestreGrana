"""Entrypoint da aplicação Streamlit.

Observação importante:
este arquivo chama-se `streamlit.py`, o que pode sombrear o pacote
externo `streamlit` durante resolução de import no Python.
"""

if __name__ != "__main__":
    # Impede que `import streamlit` carregue este arquivo como módulo.
    raise ImportError("Local entrypoint 'src/streamlit.py' is not importable; use the real 'streamlit' package or run as script")

import os
import sys

# Evita shadowing deste arquivo (`src/streamlit.py`) ao importar o pacote real.
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_ORIGINAL_SYS_PATH = list(sys.path)
sys.path = [p for p in sys.path if os.path.abspath(p or os.curdir) != _THIS_DIR]
try:
    import streamlit as st
except Exception:
    from _stubs import st
finally:
    sys.path = _ORIGINAL_SYS_PATH
# Garantir que set_page_config seja chamado antes de qualquer outro comando Streamlit
try:
    st.set_page_config(page_title="MestreGrana", page_icon="💸", layout="wide")
except Exception:
    # Se já foi chamado (por exemplo em ambiente de teste stub), ignore
    pass
import base64
import pandas as pd
import json

# Adiciona o diretório src/ ao caminho de importação
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
from datetime import datetime
from dotenv import load_dotenv

# Importa módulo de branding (crítico para UI)
try:
    from branding import apply_custom_theme, render_header, render_footer, COLORS
except ImportError as e:
    print(f"Aviso: Módulo de branding não disponível: {e}")
    def apply_custom_theme(): pass
    def render_header(): pass
    def render_footer(): pass
    COLORS = {}

# Importa novos módulos de funcionalidades
try:
    from audit_logs import render_audit_page
    from financial_reports import render_reports_page
    from products_simulator import render_catalog_page
    from cookies_consent import CookieConsent
    from data_security import DataSecurity
except ImportError as e:
    print(f"Aviso: Alguns módulos não estão disponíveis: {e}")
    render_audit_page = render_reports_page = render_catalog_page = None
    CookieConsent = DataSecurity = None

# Importa módulo de charts (Plotly-based)
try:
    from components.charts import plot_saldo_evolution, plot_gastos_categoria, plot_receitas_vs_despesas
except ImportError as e:
    print(f"Aviso: Módulo de charts não disponível: {e}")
    plot_saldo_evolution = plot_gastos_categoria = plot_receitas_vs_despesas = None

# Importa serviços e repositórios
try:
    from services.data_service import load_perfil, load_produtos, load_transacoes, load_historico
except ImportError as e:
    print(f"Aviso: Serviços de dados não disponíveis: {e}")
    load_perfil = load_produtos = load_transacoes = load_historico = None

try:
    from repositories.postgres_repo import get_pool, get_conn, put_conn
except ImportError as e:
    print(f"Aviso: Repositório Postgres não disponível: {e}")
    get_pool = get_conn = put_conn = None

try:
    from repositories.mongo_repo import get_mongo_client, get_mongo_db, find_documents
except ImportError as e:
    print(f"Aviso: Repositório MongoDB não disponível: {e}")
    get_mongo_client = get_mongo_db = find_documents = None

try:
    from core.llm_client import get_groq_client, get_gemini_client, get_openai_client, call_llm_with_fallback
except ImportError as e:
    print(f"Aviso: LLM clients não disponíveis: {e}")
    get_groq_client = get_gemini_client = get_openai_client = call_llm_with_fallback = None

try:
    from components.tables import render_transactions_table, render_products_table, render_metrics_grid
except ImportError as e:
    print(f"Aviso: Componentes de tabelas não disponíveis: {e}")
    render_transactions_table = render_products_table = render_metrics_grid = None

try:
    from components.forms import render_profile_form, render_contact_form
    from components.modals import show_alert, show_confirm_dialog, show_progress, show_tabs
    from components.cards import render_kpi_section, render_stat_card, render_info_card
except ImportError as e:
    print(f"Aviso: Componentes de UI não disponíveis: {e}")
    render_profile_form = render_contact_form = None
    show_alert = show_confirm_dialog = show_progress = show_tabs = None
    render_kpi_section = render_stat_card = render_info_card = None

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


@st.cache_data(ttl=300)
def get_postgres_version():
    try:
        conn = get_conn() if get_conn else None
        if conn is None:
            return None
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            row = cur.fetchone()
        if conn and put_conn:
            put_conn(conn)
        return row[0] if row else None
    except Exception:
        return None


atlas_status = "⚪ Não configurado"
atlas_enabled = False
neon_status = "⚪ Não configurado"
mongo_client = None
mongo_db = None
produtos_collection = None

# Try to initialize MongoDB via mongo_repo
try:
    if get_mongo_client:
        mongo_client = get_mongo_client()
        if mongo_client:
            mongo_db = get_mongo_db()
            atlas_enabled = True
            atlas_status = "🟢 Online"
        else:
            atlas_status = "🔴 Offline"
    elif not get_secret_or_env("MONGODB_ATLAS_URI"):
        atlas_status = "⚪ Não configurado"
except Exception:
    atlas_status = "🔴 Offline"

DATABASE_URL = get_secret_or_env("DATABASE_URL")
if DATABASE_URL:
    try:
        _ = get_postgres_version()
        neon_status = "🟢 Online"
    except Exception:
        neon_status = "🔴 Offline"
elif not DATABASE_URL:
    neon_status = "⚪ Não configurado"

# Aplicar tema customizado
apply_custom_theme()

st.sidebar.markdown(f"**Status Atlas:** {atlas_status}")
st.sidebar.markdown(f"**Status Neon:** {neon_status}")
st.sidebar.markdown("**Status LLM:** 🟢 Online")

GROQ_KEY = get_secret_or_env("GROQ_API_KEY")
GEMINI_KEY = get_secret_or_env("GEMINI_API_KEY")
OPENAI_KEY = get_secret_or_env("OPENAI_API_KEY")

if not GROQ_KEY or not GEMINI_KEY or not OPENAI_KEY:
    st.error("Erro: Uma ou mais chaves de API não foram encontradas em st.secrets ou no ambiente (.env). Verifique as configurações.")
    st.stop()

# Lazy initialization — clientes são carregados sob demanda via core.llm_client
# client_groq = get_groq_client()
# genai.API_KEY = GEMINI_KEY  # Deprecated — use get_gemini_client() instead
# client_openai = get_openai_client()


# --- Modularização: Função de leitura dos dados ---
def ler_dados_financeiros():
    try:
        # Use services when available, fallback to direct load
        if load_perfil:
            perfil = load_perfil()
        else:
            with open("data/perfil_investidor.json", "r", encoding='utf-8') as f:
                perfil = json.load(f)

        if atlas_enabled and find_documents:
            # Busca produtos do MongoDB Atlas via repository
            produtos = find_documents("produtos")
        elif load_produtos:
            produtos = load_produtos()
        else:
            with open("data/produtos_financeiros.json", "r", encoding="utf-8") as f:
                produtos = json.load(f)

        if load_transacoes:
            transacoes = load_transacoes()
        else:
            transacoes = None
        # Se load_transacoes retornou DataFrame vazio, tente Postgres via repository
        try:
            import pandas as _pd
            if transacoes is None or (isinstance(transacoes, _pd.DataFrame) and transacoes.empty):
                # Tenta obter via repositório Postgres
                if 'get_transactions' in globals() and callable(globals().get('get_transactions')):
                    transacoes = get_transactions()
                elif get_conn:
                    # fallback simples usando conexão direta
                    conn = get_conn()
                    if conn:
                        transacoes = _pd.read_sql("SELECT * FROM transactions", conn)
                        if put_conn:
                            put_conn(conn)
        except Exception:
            # Mantém transacoes possivelmente None
            pass

        if load_historico:
            historico = load_historico()
        else:
            historico = None

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

    # Exibe KPIs usando cards reutilizáveis quando disponíveis
    try:
        kpi_data = [
            {"title": "Saldo Atual", "value": f"R$ {saldo_total:,.2f}", "delta": None,},
            {"title": "Total Investido", "value": f"R$ {total_investido:,.2f}", "delta": None,},
            {"title": "Produtos", "value": total_produtos, "delta": None,},
            {"title": "Transações", "value": total_transacoes, "delta": None,},
        ]
        if render_kpi_section:
            render_kpi_section(kpi_data)
        else:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Saldo Atual", f"R$ {saldo_total:,.2f}")
            col2.metric("Total Investido (Metas)", f"R$ {total_investido:,.2f}")
            col3.metric("Produtos Financeiros", total_produtos)
            col4.metric("Transações", total_transacoes)
    except Exception:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Saldo Atual", f"R$ {saldo_total:,.2f}")
        col2.metric("Total Investido (Metas)", f"R$ {total_investido:,.2f}")
        col3.metric("Produtos Financeiros", total_produtos)
        col4.metric("Transações", total_transacoes)

    st.markdown("---")

    # Gráfico de evolução do saldo (Plotly)
    if historico is not None and not historico.empty and "data" in historico.columns and "saldo" in historico.columns:
        st.subheader("Evolução do Saldo")
        if plot_saldo_evolution:
            fig = plot_saldo_evolution(historico)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Módulo de gráficos não disponível")

    # Gráfico de distribuição de gastos (Plotly)
    if transacoes is not None and not transacoes.empty and "categoria" in transacoes.columns and "valor" in transacoes.columns:
        st.subheader("Gastos por Categoria")
        if plot_gastos_categoria:
            fig = plot_gastos_categoria(transacoes)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Módulo de gráficos não disponível")

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
    # Botão para editar perfil usando o formulário modular
    try:
        if render_profile_form:
            if st.button("✏️ Editar Perfil"):
                profile_data = render_profile_form(initial_data=perfil)
                if profile_data:
                    # Aqui poderíamos persistir via repositório; por enquanto notificamos o usuário
                    if show_alert:
                        show_alert("Perfil salvo com sucesso!", "success")
                    else:
                        st.success("Perfil salvo com sucesso!")
    except Exception:
        pass
# --- Exibição do menu de navegação na barra lateral ---
with st.sidebar:
    st.header("📱 Navegação")
    pagina = st.radio(
        "Escolha a página:",
        [
            "💬 Assistente",
            "📊 Dashboard",
            "🎤 Voz",
            "📋 Auditoria",
            "📈 Relatórios",
            "💼 Produtos & Simulador",
        ]
    )
    st.markdown("---")
    st.markdown("### ⚙️ Conformidade")
    # Renderiza banner de consentimento LGPD
    if CookieConsent:
        CookieConsent.render_consent_banner()

# --- Renderização do Header com Branding ---
render_header()

# --- Renderização de páginas ---
if pagina == "📊 Dashboard":
    mostrar_dashboard()

elif pagina == "🎤 Voz":
    try:
        from components.voice import render_voice_input, render_voice_output
        st.title("🎤 Chat com Voz")
        
        perfil, produtos, transacoes, historico = ler_dados_financeiros()
        user_name = perfil.get("nome", "Usuário") if perfil else "Usuário"
        user_profile = perfil.get("perfil_investidor", "não definido") if perfil else "não definido"
        
        st.markdown(f"""
        Olá, **{user_name}**! Use o botão abaixo para falar com o **MestreGrana**.
        O assistente irá ouvir sua voz, responder com base no seu perfil (**{user_profile}**) e sintetizar a resposta em áudio.
        """)
        
        user_voice = render_voice_input()
        if user_voice:
            st.info(f"🎤 **Transcrição:** {user_voice}")
            
            # Gera contexto com dados reais
            transacoes_str = transacoes.to_string() if transacoes is not None else "Nenhuma transação registrada."
            
            system_prompt = f"""Você é o MestreGrana, um mentor financeiro experiente e resiliente.
Seu objetivo é responder a perguntas de voz do usuário de forma falada, ou seja, de maneira curta, direta e natural.
Aqui estão as informações reais sobre o usuário:
Nome: {user_name}
Perfil de Investidor: {user_profile}
Renda Mensal: R$ {perfil.get('renda_mensal', 0):,.2f}
Objetivo Principal: {perfil.get('objetivo_principal', 'Não informado')}
Patrimônio Total: R$ {perfil.get('patrimonio_total', 0):,.2f}
Reserva de Emergência Atual: R$ {perfil.get('reserva_emergencia_atual', 0):,.2f}
Metas: {perfil.get('metas', [])}

Últimas transações reais do usuário:
{transacoes_str}

Instruções para resposta:
1. Responda de forma extremamente curta (1 a 3 frases no máximo), direta e natural, adequada para ser ouvida por voz.
2. Fundamente suas respostas nos dados reais fornecidos. Se a resposta requerer dados não disponíveis, diga claramente que não possui essa informação.
3. Não alucine sobre o saldo ou transações do usuário.
4. Mantenha as respostas focadas em educação e orientação financeira."""

            chat_context = system_prompt + f"\n\nPergunta do Usuário por voz: {user_voice}\nResposta curta do MestreGrana:"
            
            with st.spinner("Pensando..."):
                response = call_llm_with_fallback(chat_context)
                
            if response:
                st.success(f"🤖 **MestreGrana:** {response}")
                # Renderiza o botão para reproduzir a resposta
                render_voice_output(response)
                
                # Registra ação na auditoria
                try:
                    from audit_logs import log_action
                    log_action(
                        user_id=user_name,
                        action="chat_voz",
                        details=f"Pergunta por voz: {user_voice[:100]}"
                    )
                except Exception:
                    pass
            else:
                st.error("Desculpe, ocorreu um erro ao gerar a resposta com os modelos disponíveis.")
    except ImportError as e:
        st.error(f"❌ Componente de voz não disponível: {e}")

elif pagina == "📋 Auditoria":
    if render_audit_page:
        render_audit_page()
    else:
        st.error("❌ Módulo de Auditoria não disponível")

elif pagina == "📈 Relatórios":
    if render_reports_page:
        render_reports_page()
    else:
        st.error("❌ Módulo de Relatórios não disponível")

elif pagina == "💼 Produtos & Simulador":
    if render_catalog_page:
        render_catalog_page()
    else:
        st.error("❌ Módulo de Produtos & Simulador não disponível")

elif True:
    # Assistente (fallback/default)
    st.subheader("💬 Converse com o MestreGrana")

    perfil, produtos, transacoes, historico = ler_dados_financeiros()
    user_name = perfil.get("nome", "Usuário") if perfil else "Usuário"
    user_profile = perfil.get("perfil_investidor", "não definido") if perfil else "não definido"

    st.markdown(f"""
    Olá, **{user_name}**! Eu sou o **MestreGrana**, seu consultor financeiro inteligente.
    Com base no seu perfil **{user_profile}** e no seu objetivo principal (**{perfil.get('objetivo_principal', 'não definido')}**), posso lhe ajudar a:
    - 🎯 **Medir**: Acompanhar seus gastos e receitas.
    - 📊 **Planejar**: Simular cenários de investimentos.
    - 📈 **Multiplicar**: Identificar oportunidades para seu perfil.
    """)

    # Sugestões rápidas
    st.markdown("💡 **Perguntas frequentes:**")
    cols = st.columns(3)
    sugestao_1 = "Como posso completar minha reserva de emergência?"
    sugestao_2 = "Faça uma análise rápida do meu perfil de gastos deste mês."
    sugestao_3 = "Quais são as melhores sugestões de investimentos para o meu perfil?"

    prompt = None
    if cols[0].button("🎯 Reserva de Emergência", use_container_width=True):
        prompt = sugestao_1
    elif cols[1].button("📊 Analisar meus Gastos", use_container_width=True):
        prompt = sugestao_2
    elif cols[2].button("📈 Onde Investir?", use_container_width=True):
        prompt = sugestao_3

    # Inicializa o histórico de mensagens se estiver vazio
    if "messages" not in st.session_state or not st.session_state.messages:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": f"Olá {user_name}! Sou o MestreGrana, seu aliado financeiro. Como posso lhe ajudar hoje?"
            }
        ]

    # Renderiza mensagens anteriores
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Captura novo input de texto
    user_input = st.chat_input("Digite sua dúvida financeira...")
    if user_input:
        prompt = user_input

    if prompt:
        # Se for uma pergunta nova, adiciona e exibe
        if not st.session_state.messages or st.session_state.messages[-1]["content"] != prompt:
            # Exibe e grava
            with st.chat_message("user"):
                st.markdown(prompt)
            try:
                from core.state import add_message
                add_message("user", prompt)
            except Exception:
                st.session_state.messages.append({"role": "user", "content": prompt})

            # Gera contexto com dados reais
            transacoes_str = transacoes.to_string() if transacoes is not None else "Nenhuma transação registrada."

            system_prompt = f"""Você é o MestreGrana, um mentor financeiro experiente e resiliente.
Seu objetivo é orientar o usuário com base nos seus dados reais e evitar alucinações.
Aqui estão as informações reais sobre o usuário:
Nome: {user_name}
Idade: {perfil.get('idade', 'Não informado')}
Profissão: {perfil.get('profissao', 'Não informado')}
Renda Mensal: R$ {perfil.get('renda_mensal', 0):,.2f}
Perfil de Investidor: {user_profile}
Objetivo Principal: {perfil.get('objetivo_principal', 'Não informado')}
Patrimônio Total: R$ {perfil.get('patrimonio_total', 0):,.2f}
Reserva de Emergência Atual: R$ {perfil.get('reserva_emergencia_atual', 0):,.2f}
Metas: {perfil.get('metas', [])}

Últimas transações reais do usuário:
{transacoes_str}

Instruções para resposta:
1. Responda de forma extremamente clara, estruturada e amigável, em português (Brasil).
2. Fundamente suas respostas nos dados reais fornecidos. Se a resposta requerer dados não disponíveis, diga claramente que não possui essa informação.
3. Não invente ou alucine sobre o saldo ou transações do usuário.
4. Ao dar conselhos sobre investimentos, adeque-se sempre ao perfil de investidor do usuário ({user_profile}).
5. Mantenha as respostas focadas em educação e orientação financeira. Se o usuário fugir do assunto, guie-o de volta com simpatia."""

            # Cria contexto com histórico
            chat_context = system_prompt + "\n\nHistórico da conversa:\n"
            for msg in st.session_state.messages[-6:]:
                role_name = "Usuário" if msg["role"] == "user" else "Assistente"
                chat_context += f"{role_name}: {msg['content']}\n"
            chat_context += "Assistente:"

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner("Pensando..."):
                    response = call_llm_with_fallback(chat_context)
                if response:
                    message_placeholder.markdown(response)
                    try:
                        from core.state import add_message
                        add_message("assistant", response)
                    except Exception:
                        st.session_state.messages.append({"role": "assistant", "content": response})

                    # Registra ação na auditoria
                    try:
                        from audit_logs import log_action
                        log_action(
                            user_id=user_name,
                            action="chat_assistente",
                            details=f"Prompt: {prompt[:100]}"
                        )
                    except Exception:
                        pass
                else:
                    st.error("Desculpe, os serviços de IA estão offline ou ocupados no momento. Tente novamente.")
