"""
Auditoria e Logs - Visualização e análise de alterações de dados.
Integra com a tabela audit_log para conformidade e troubleshooting.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List
from config import get_neon_database


class AuditLog:
    """Gerenciador de auditoria e logs."""

    @staticmethod
    def get_recent_changes(
        limit: int = 50,
        table_filter: Optional[str] = None,
        days: int = 30,
    ) -> pd.DataFrame:
        """
        Retorna alterações recentes registradas.

        Args:
            limit: Número máximo de registros
            table_filter: Filtrar por tabela específica
            days: Últimos N dias

        Returns:
            DataFrame com audit_log
        """
        client = get_neon_database()

        where_clause = f"WHERE changed_at > NOW() - INTERVAL '{days} days'"
        if table_filter:
            where_clause += f" AND table_name = '{table_filter}'"

        query = f"""
            SELECT 
                id,
                table_name,
                operation,
                changed_by,
                changed_at,
                old_values,
                new_values,
                ip_address
            FROM audit_log
            {where_clause}
            ORDER BY changed_at DESC
            LIMIT {limit}
        """

        return client.fetch_dataframe(query) or pd.DataFrame()

    @staticmethod
    def get_user_activity(user_id: str, days: int = 30) -> pd.DataFrame:
        """Retorna atividade de um usuário específico."""
        client = get_neon_database()

        query = """
            SELECT 
                changed_at,
                table_name,
                operation,
                record_id
            FROM audit_log
            WHERE changed_by = %s AND changed_at > NOW() - INTERVAL %s
            ORDER BY changed_at DESC
        """

        return (
            client.fetch_dataframe(query, (user_id, f"{days} days"))
            or pd.DataFrame()
        )

    @staticmethod
    def get_table_statistics(days: int = 30) -> pd.DataFrame:
        """Retorna estatísticas por tabela."""
        client = get_neon_database()

        query = """
            SELECT 
                table_name,
                operation,
                COUNT(*) as count,
                COUNT(DISTINCT changed_by) as unique_users
            FROM audit_log
            WHERE changed_at > NOW() - INTERVAL %s
            GROUP BY table_name, operation
            ORDER BY count DESC
        """

        return (
            client.fetch_dataframe(query, (f"{days} days",))
            or pd.DataFrame()
        )

    @staticmethod
    def get_deleted_records(table_name: str, days: int = 30) -> pd.DataFrame:
        """Retorna registros deletados (para recuperação)."""
        client = get_neon_database()

        query = """
            SELECT 
                record_id,
                changed_at,
                changed_by,
                old_values,
                ip_address
            FROM audit_log
            WHERE table_name = %s AND operation = 'DELETE' AND changed_at > NOW() - INTERVAL %s
            ORDER BY changed_at DESC
        """

        return (
            client.fetch_dataframe(query, (table_name, f"{days} days"))
            or pd.DataFrame()
        )

    @staticmethod
    def render_audit_dashboard():
        """Renderiza dashboard de auditoria completo."""
        st.subheader("📋 Dashboard de Auditoria")

        tab1, tab2, tab3, tab4 = st.tabs([
            "Alterações Recentes",
            "Por Tabela",
            "Atividade de Usuário",
            "Registros Deletados"
        ])

        # TAB 1: Alterações Recentes
        with tab1:
            col1, col2, col3 = st.columns(3)

            with col1:
                limit = st.slider("Mostrar últimos N registros", 10, 500, 50)

            with col2:
                days = st.slider("Últimos N dias", 1, 365, 30)

            with col3:
                table_filter = st.selectbox(
                    "Filtrar por tabela",
                    ["Todos", "users", "transactions", "tax_compliance", "audit_log"],
                )

            table_val = None if table_filter == "Todos" else table_filter

            df = AuditLog.get_recent_changes(limit, table_val, days)

            if not df.empty:
                # Formatação
                df["changed_at"] = pd.to_datetime(df["changed_at"]).dt.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                df = df[
                    [
                        "changed_at",
                        "table_name",
                        "operation",
                        "changed_by",
                        "ip_address",
                    ]
                ]

                st.dataframe(df, use_container_width=True)

                # Estatísticas
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total de Alterações", len(df))
                with col2:
                    inserts = len(df[df["operation"] == "INSERT"])
                    st.metric("INSERTs", inserts)
                with col3:
                    deletes = len(df[df["operation"] == "DELETE"])
                    st.metric("DELETEs", deletes)
            else:
                st.info("Nenhum registro encontrado")

        # TAB 2: Estatísticas por Tabela
        with tab2:
            days = st.slider("Últimos N dias (tab 2)", 1, 365, 30, key="days_tab2")

            df_stats = AuditLog.get_table_statistics(days)

            if not df_stats.empty:
                st.dataframe(df_stats, use_container_width=True)

                # Gráfico
                fig_data = df_stats.groupby("table_name")["count"].sum().sort_values()
                st.bar_chart(fig_data)
            else:
                st.info("Nenhum dado disponível")

        # TAB 3: Atividade de Usuário
        with tab3:
            user_id = st.text_input("ID do usuário")
            days = st.slider("Últimos N dias (tab 3)", 1, 365, 30, key="days_tab3")

            if user_id:
                df_user = AuditLog.get_user_activity(user_id, days)

                if not df_user.empty:
                    st.dataframe(df_user, use_container_width=True)
                    st.metric("Total de Ações", len(df_user))
                else:
                    st.warning(f"Nenhuma atividade encontrada para {user_id}")
            else:
                st.info("Digite um ID de usuário para ver atividade")

        # TAB 4: Registros Deletados (Recuperação)
        with tab4:
            table_name = st.selectbox(
                "Selecionar tabela",
                ["transactions", "users", "tax_compliance"],
                key="del_table",
            )
            days = st.slider("Últimos N dias (tab 4)", 1, 365, 30, key="days_tab4")

            df_deleted = AuditLog.get_deleted_records(table_name, days)

            if not df_deleted.empty:
                st.warning(f"⚠️ {len(df_deleted)} registros deletados encontrados")
                st.dataframe(df_deleted, use_container_width=True)

                if st.button(
                    "🔄 Recuperar Registro Selecionado",
                    key="recover_btn",
                ):
                    st.info("💡 Contacte administrador para recuperação manual")
            else:
                st.info("Nenhum registro deletado recentemente")


def render_audit_page():
    """Página completa de auditoria."""
    st.title("🔍 Auditoria e Logs")

    st.markdown("""
    **Visualize todas as alterações no banco de dados:**
    - ✅ Quem alterou
    - ✅ Quando alterou
    - ✅ De onde (IP)
    - ✅ O que mudou (valores antigos/novos)
    """)

    AuditLog.render_audit_dashboard()

    st.markdown("---")

    with st.expander("📚 Como Usar Auditoria"):
        st.markdown("""
        ### Caso de Uso 1: Audit Compliance
        Use a aba "Alterações Recentes" para gerar relatórios de conformidade mensal.
        
        ### Caso de Uso 2: Investigação de Anomalias
        Filtre por usuário na aba "Atividade de Usuário" para investigar comportamentos suspeitos.
        
        ### Caso de Uso 3: Recuperação de Dados
        A aba "Registros Deletados" permite recuperar dados deletados accidentalmente.
        
        ### Caso de Uso 4: Análise de Performance
        "Por Tabela" mostra quais operações são mais frequentes (útil para otimização).
        """)
