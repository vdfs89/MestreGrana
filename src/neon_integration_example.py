"""
Exemplos de integração do cliente Neon em Streamlit.
Para usar no seu app, copie os padrões abaixo.
"""

import streamlit as st
from config import get_neon_database
import pandas as pd


def example_fetch_users():
    """Exemplo: buscar usuários do banco."""
    client = get_neon_database()
    
    # Usando fetch_all() com retry automático
    users = client.fetch_all("SELECT id, name, email FROM users LIMIT 10")
    
    if users:
        df = pd.DataFrame(users, columns=["ID", "Name", "Email"])
        st.dataframe(df)
    else:
        st.info("Nenhum usuário encontrado")


def example_fetch_with_params():
    """Exemplo: query com parâmetros (SQL injection safe)."""
    client = get_neon_database()
    user_id = st.number_input("ID do usuário", value=1)
    
    # Usando context manager com parâmetros
    with client.query(
        "SELECT id, name, email FROM users WHERE id = %s",
        (user_id,)
    ) as cursor:
        user = cursor.fetchone()
        
        if user:
            st.success(f"✅ Usuário: {user}")
        else:
            st.warning(f"Usuário {user_id} não encontrado")


def example_insert_transaction():
    """Exemplo: inserir transação com validação."""
    client = get_neon_database()
    
    with st.form("nova_transacao"):
        user_id = st.number_input("ID do usuário")
        amount = st.number_input("Valor", min_value=0.01, step=0.01)
        description = st.text_input("Descrição")
        
        if st.form_submit_button("Registrar"):
            success = client.execute(
                """
                INSERT INTO transactions (user_id, amount, description, transaction_date)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                """,
                (user_id, amount, description)
            )
            
            if success:
                st.success("✅ Transação registrada")
            else:
                st.error("❌ Erro ao registrar transação")


def example_fetch_dataframe():
    """Exemplo: retornar dados como pandas DataFrame."""
    client = get_neon_database()
    
    # Retorna DataFrame diretamente
    df = client.fetch_dataframe(
        "SELECT user_id, SUM(amount) as total FROM transactions GROUP BY user_id"
    )
    
    if df is not None and not df.empty:
        st.bar_chart(df.set_index("user_id"))
    else:
        st.info("Sem dados para exibir")


def example_health_dashboard():
    """Exemplo: exibir status de saúde do banco em sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.subheader("Status do Banco")
    
    client = get_neon_database()
    health = client.health_check()
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        status = "🟢" if health["connected"] else "🔴"
        st.metric("Conexão", status)
    
    with col2:
        st.metric("Versão", health["version"][:30] if health["version"] else "N/A")
    
    if health.get("error"):
        st.sidebar.error(f"Erro: {health['error']}")


def example_error_handling():
    """Exemplo: tratamento robusto de erros."""
    client = get_neon_database()
    
    try:
        # Retry automático (máx 3 tentativas com backoff)
        result = client.fetch_one("SELECT COUNT(*) FROM transactions")
        st.success(f"Total de transações: {result[0]}")
        
    except Exception as e:
        st.error(f"❌ Erro ao consultar banco: {e}")
        st.info("💡 O cliente Neon já tentou reconectar automaticamente")


# Exemplos de query pattern
EXAMPLE_QUERIES = {
    "Usuários ativos": """
        SELECT id, name, email, created_at
        FROM users
        WHERE created_at > NOW() - INTERVAL '30 days'
        ORDER BY created_at DESC
    """,
    "Transações por categoria": """
        SELECT c.name, COUNT(*) as count, SUM(t.amount) as total
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        GROUP BY c.name
        ORDER BY total DESC
    """,
    "Débitos vencidos": """
        SELECT user_id, SUM(amount) as total_due, MAX(due_date) as latest_due
        FROM debts
        WHERE due_date < CURRENT_DATE AND status = 'open'
        GROUP BY user_id
        ORDER BY total_due DESC
    """,
}


def example_dynamic_query():
    """Exemplo: query dinâmica baseada em seleção."""
    client = get_neon_database()
    
    selected_query = st.selectbox("Selecione uma query", list(EXAMPLE_QUERIES.keys()))
    
    if st.button("Executar"):
        query = EXAMPLE_QUERIES[selected_query]
        df = client.fetch_dataframe(query)
        
        if df is not None and not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Sem resultados")


if __name__ == "__main__":
    st.title("Exemplos - Integração Neon com Streamlit")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Buscar",
        "Inserir",
        "Dashboard",
        "Queries"
    ])
    
    with tab1:
        st.subheader("Fetch com Parâmetros")
        example_fetch_with_params()
    
    with tab2:
        st.subheader("Inserir Transação")
        example_insert_transaction()
    
    with tab3:
        st.subheader("Status do Banco")
        example_health_dashboard()
    
    with tab4:
        st.subheader("Queries Dinâmicas")
        example_dynamic_query()
