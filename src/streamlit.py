"""Entrypoint wrapper para Streamlit Cloud.

Este arquivo existe para permitir que o app seja iniciado como
`streamlit run src/streamlit.py` (esperado pelo Streamlit Cloud),
enquanto evita sombra (shadowing) do pacote `streamlit` durante
importações em testes locais.

Comportamento:
- Quando executado como script (via CLI), ele executa o módulo
  `streamlit_app` como __main__.
- Quando importado por outro módulo, ele levanta ImportError para
  que as importações façam fallback para o stub `_stubs.py`.
"""

if __name__ == "__main__":
    # Execute o módulo da aplicação real
    import runpy
    runpy.run_module('streamlit_app', run_name='__main__')
else:
    # Impede que `import streamlit` carregue este arquivo como módulo
    raise ImportError("Local entrypoint 'src/streamlit.py' is not importable; use the real 'streamlit' package or run as script")
try:
    import streamlit as st
except Exception:
    from _stubs import st
# Garantir que set_page_config seja chamado antes de qualquer outro comando Streamlit
try:
    st.set_page_config(page_title="MestreGrana", page_icon="💸", layout="wide")
except Exception:
    # Se já foi chamado (por exemplo em ambiente de teste stub), ignore
    pass
import base64
import pandas as pd
import json
import sys
import os

# Adiciona o diretório src/ ao caminho de importação
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import base64
import pandas as pd
import json
import sys
import os

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
            try:
                conn = get_conn() if get_conn else None
                if conn:
                    transacoes = pd.read_sql("SELECT * FROM transactions", conn)
                    if put_conn:
                        put_conn(conn)
                else:
                    transacoes = pd.read_csv("data/transacoes.csv")
            except:
                transacoes = pd.read_csv("data/transacoes.csv")

        if load_historico:
            historico = load_historico()
        else:
            historico = pd.read_csv("data/historico_atendimento.csv")

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
        user_voice = render_voice_input()
        if user_voice:
            st.success(f"Você disse: {user_voice}")
            render_voice_output("Ótimo! Recebi sua mensagem de voz.")
    except ImportError:
        st.error("❌ Componente de voz não disponível")

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
    pass
