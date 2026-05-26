"""
Relatórios Contábeis - DRE, Fluxo de Caixa, Análise de Variância.
Gera relatórios financeiros profissionais.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional
from config import get_neon_database


class FinancialReports:
    """Gerador de relatórios contábeis e análises financeiras."""

    @staticmethod
    def get_income_statement(year: int, month: Optional[int] = None) -> Dict:
        """
        Demonstração de Resultado do Exercício (DRE).
        
        Args:
            year: Ano fiscal
            month: Mês (1-12) ou None para ano completo
        
        Returns:
            Dict com dados de receita/despesa
        """
        client = get_neon_database()

        date_filter = f"EXTRACT(YEAR FROM transaction_date) = {year}"
        if month:
            date_filter += f" AND EXTRACT(MONTH FROM transaction_date) = {month}"

        query = f"""
            SELECT 
                c.name as category,
                SUM(CASE WHEN t.amount > 0 THEN t.amount ELSE 0 END) as revenue,
                SUM(CASE WHEN t.amount < 0 THEN ABS(t.amount) ELSE 0 END) as expense
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE {date_filter}
            GROUP BY c.name
            ORDER BY revenue DESC
        """

        df = client.fetch_dataframe(query) or pd.DataFrame()

        total_revenue = df["revenue"].sum() if not df.empty else 0
        total_expense = df["expense"].sum() if not df.empty else 0

        return {
            "period": f"{month}/{year}" if month else f"{year}",
            "data": df,
            "total_revenue": total_revenue,
            "total_expense": total_expense,
            "gross_profit": total_revenue - total_expense,
        }

    @staticmethod
    def get_cashflow(year: int) -> pd.DataFrame:
        """Fluxo de caixa mensal."""
        client = get_neon_database()

        query = """
            SELECT 
                DATE_TRUNC('month', transaction_date)::date as month,
                SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as inflow,
                SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END) as outflow
            FROM transactions
            WHERE EXTRACT(YEAR FROM transaction_date) = %s
            GROUP BY DATE_TRUNC('month', transaction_date)
            ORDER BY month
        """

        return client.fetch_dataframe(query, (year,)) or pd.DataFrame()

    @staticmethod
    def get_variance_analysis(
        year: int,
        budget_vs_actual: bool = True,
    ) -> pd.DataFrame:
        """
        Análise de Variância (Budget vs Actual ou YoY).
        
        Args:
            year: Ano para análise
            budget_vs_actual: Se True, compara com budget; se False, compara YoY
        
        Returns:
            DataFrame com variâncias
        """
        client = get_neon_database()

        if budget_vs_actual:
            # Budget vs Actual
            query = """
                SELECT 
                    c.name as category,
                    b.budget_limit as budget,
                    SUM(ABS(t.amount)) as actual,
                    (SUM(ABS(t.amount)) - b.budget_limit) as variance,
                    ROUND(
                        ((SUM(ABS(t.amount)) - b.budget_limit) / b.budget_limit * 100),
                        2
                    ) as variance_pct
                FROM transactions t
                JOIN categories c ON t.category_id = c.id
                LEFT JOIN budgets b ON b.category_id = c.id
                WHERE EXTRACT(YEAR FROM t.transaction_date) = %s
                GROUP BY c.name, b.budget_limit
            """
        else:
            # Year-over-Year
            query = """
                SELECT 
                    c.name as category,
                    SUM(CASE WHEN EXTRACT(YEAR FROM t.transaction_date) = %s THEN ABS(t.amount) ELSE 0 END) as current_year,
                    SUM(CASE WHEN EXTRACT(YEAR FROM t.transaction_date) = %s - 1 THEN ABS(t.amount) ELSE 0 END) as previous_year,
                    (SUM(CASE WHEN EXTRACT(YEAR FROM t.transaction_date) = %s THEN ABS(t.amount) ELSE 0 END) - 
                     SUM(CASE WHEN EXTRACT(YEAR FROM t.transaction_date) = %s - 1 THEN ABS(t.amount) ELSE 0 END)) as variance
                FROM transactions t
                JOIN categories c ON t.category_id = c.id
                WHERE EXTRACT(YEAR FROM t.transaction_date) IN (%s, %s - 1)
                GROUP BY c.name
            """
            return (
                client.fetch_dataframe(query, (year, year, year, year, year, year))
                or pd.DataFrame()
            )

        return client.fetch_dataframe(query, (year,)) or pd.DataFrame()

    @staticmethod
    def render_income_statement(year: int, month: Optional[int] = None):
        """Renderiza DRE em Streamlit."""
        st.subheader("📊 Demonstração de Resultado (DRE)")

        report = FinancialReports.get_income_statement(year, month)

        period = report["period"]
        st.markdown(f"**Período**: {period}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "💰 Receita Total",
                f"R$ {report['total_revenue']:,.2f}",
            )

        with col2:
            st.metric(
                "💸 Despesa Total",
                f"R$ {report['total_expense']:,.2f}",
            )

        with col3:
            profit = report["gross_profit"]
            color = "green" if profit >= 0 else "red"
            st.metric(
                "📈 Lucro Líquido",
                f"R$ {profit:,.2f}",
                delta=f"{(profit / report['total_revenue'] * 100):.1f}%" if report["total_revenue"] > 0 else "N/A",
            )

        # Tabela detalhada
        if not report["data"].empty:
            st.dataframe(report["data"], use_container_width=True)

            # Gráfico
            fig_data = report["data"][["category", "revenue", "expense"]].set_index(
                "category"
            )
            st.bar_chart(fig_data)
        else:
            st.info("Nenhum dado disponível para este período")

    @staticmethod
    def render_cashflow(year: int):
        """Renderiza fluxo de caixa."""
        st.subheader("💵 Fluxo de Caixa Mensal")

        df = FinancialReports.get_cashflow(year)

        if not df.empty:
            df["net_flow"] = df["inflow"] - df["outflow"]

            st.dataframe(df, use_container_width=True)

            # Visualizações
            col1, col2 = st.columns(2)

            with col1:
                st.line_chart(df.set_index("month")[["inflow", "outflow"]])

            with col2:
                st.area_chart(df.set_index("month")["net_flow"])

            # Resumo
            st.metric(
                "Fluxo Líquido Anual",
                f"R$ {df['net_flow'].sum():,.2f}",
            )
        else:
            st.info("Nenhum dado de fluxo disponível")

    @staticmethod
    def render_variance_analysis(year: int):
        """Renderiza análise de variância."""
        st.subheader("📉 Análise de Variância")

        tab1, tab2 = st.tabs(["Budget vs Actual", "Year-over-Year"])

        with tab1:
            df_bva = FinancialReports.get_variance_analysis(year, budget_vs_actual=True)

            if not df_bva.empty:
                # Colorir variâncias negativas (boas) em verde
                st.dataframe(
                    df_bva.style.highlight_max(
                        subset=["variance_pct"],
                        color="lightcoral",
                    ),
                    use_container_width=True,
                )
            else:
                st.info("Nenhum budget configurado para comparação")

        with tab2:
            df_yoy = FinancialReports.get_variance_analysis(year, budget_vs_actual=False)

            if not df_yoy.empty:
                st.dataframe(df_yoy, use_container_width=True)

                # Gráfico de comparação
                chart_data = df_yoy[["category", "current_year", "previous_year"]].set_index(
                    "category"
                )
                st.bar_chart(chart_data)
            else:
                st.info("Nenhum dado anterior para comparação YoY")


def render_reports_page():
    """Página completa de relatórios."""
    st.title("📋 Relatórios Contábeis")

    st.markdown("""
    Gere relatórios financeiros profissionais para seu negócio:
    - 📊 Demonstração de Resultado (DRE)
    - 💵 Fluxo de Caixa
    - 📉 Análise de Variância (Budget vs Actual / YoY)
    """)

    # Seletor de período
    col1, col2, col3 = st.columns(3)

    with col1:
        year = st.number_input("Ano", min_value=2020, max_value=2030, value=2026)

    with col2:
        month_selection = st.radio("Período", ["Anual", "Mensal"])

    with col3:
        month = None
        if month_selection == "Mensal":
            month = st.number_input("Mês", min_value=1, max_value=12, value=5)

    st.markdown("---")

    # Tabs de relatórios
    tab1, tab2, tab3 = st.tabs([
        "DRE",
        "Fluxo de Caixa",
        "Variância",
    ])

    with tab1:
        FinancialReports.render_income_statement(year, month)

    with tab2:
        FinancialReports.render_cashflow(year)

    with tab3:
        FinancialReports.render_variance_analysis(year)

    st.markdown("---")

    with st.expander("📥 Exportar Relatório"):
        format_type = st.radio("Formato", ["CSV", "Excel"])

        if st.button("Gerar Download"):
            st.info(f"💡 Download em formato {format_type} será implementado em breve")

    with st.expander("📚 Glossário Contábil"):
        st.markdown("""
        **DRE (Demonstração de Resultado)**: Mostra receitas, despesas e lucro/prejuízo em um período.
        
        **Fluxo de Caixa**: Entrada e saída de dinheiro mês a mês.
        
        **Variância**: Diferença entre valor orçado e real (ou ano anterior e ano atual).
        """)
