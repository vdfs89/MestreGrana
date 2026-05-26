"""
Catálogo de Produtos e Simulador de Cenários.
Amplia catálogo de produtos financeiros e oferece simulações "what-if".
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from config import get_neon_database


class ProductCatalog:
    """Gerenciador do catálogo de produtos financeiros."""

    # Produtos padrão expandidos
    PRODUCTS = {
        "Investimentos": [
            {
                "name": "Tesouro Direto - Prefixado",
                "risk": "Baixo",
                "return_pa": "12.5%",
                "min_investment": 100,
                "description": "Tesouro do Governo Federal com retorno prefixado",
            },
            {
                "name": "Tesouro Direto - IPCA+",
                "risk": "Baixo",
                "return_pa": "IPCA + 6.5%",
                "min_investment": 100,
                "description": "Proteção contra inflação + ganho real",
            },
            {
                "name": "Fundo de Renda Fixa",
                "risk": "Médio",
                "return_pa": "11-13%",
                "min_investment": 500,
                "description": "Aplicação em títulos de renda fixa",
            },
            {
                "name": "Fundo de Ações",
                "risk": "Alto",
                "return_pa": "15-20%",
                "min_investment": 1000,
                "description": "Diversificação em ações da bolsa",
            },
            {
                "name": "ETF - Índice S&P 500",
                "risk": "Alto",
                "return_pa": "18-22%",
                "min_investment": 100,
                "description": "Exposição ao mercado americano",
            },
            {
                "name": "CDB - Certificado de Depósito Bancário",
                "risk": "Baixo-Médio",
                "return_pa": "10-12%",
                "min_investment": 250,
                "description": "Renda fixa com garantia FGC até R$ 250k",
            },
        ],
        "Crédito": [
            {
                "name": "Empréstimo Pessoal",
                "rate_pa": "20-40%",
                "min_amount": 500,
                "max_amount": 50000,
                "description": "Crédito rápido sem garantia",
            },
            {
                "name": "Empréstimo Consignado",
                "rate_pa": "2-8%",
                "min_amount": 1000,
                "max_amount": 100000,
                "description": "Desconto direto em folha (mais barato)",
            },
            {
                "name": "Cartão de Crédito",
                "rate_pa": "15-20%",
                "min_amount": 100,
                "max_amount": 50000,
                "description": "Limite rotativo com taxa de juros",
            },
            {
                "name": "Financiamento de Veículo",
                "rate_pa": "8-15%",
                "min_amount": 10000,
                "max_amount": 500000,
                "description": "Com garantia (alienação fiduciária)",
            },
            {
                "name": "Financiamento Imobiliário",
                "rate_pa": "6-10%",
                "min_amount": 100000,
                "max_amount": 2000000,
                "description": "Imóvel como garantia",
            },
        ],
        "Seguros": [
            {
                "name": "Seguro de Vida",
                "cost_pm": "50-500",
                "coverage": "Até R$ 1M",
                "description": "Proteção para família em caso de morte",
            },
            {
                "name": "Seguro de Saúde",
                "cost_pm": "200-2000",
                "coverage": "Médicos e hospitais",
                "description": "Cobertura médica abrangente",
            },
            {
                "name": "Seguro de Auto",
                "cost_pm": "100-1000",
                "coverage": "Danos/Roubos/Terceiros",
                "description": "Proteção para seu veículo",
            },
        ],
        "Previdência": [
            {
                "name": "PGBL - Plano Gerador de Benefício Livre",
                "risk": "Médio",
                "return_pa": "8-12%",
                "tax_benefit": "30%",
                "description": "Aposentadoria privada com dedução fiscal",
            },
            {
                "name": "VGBL - Vida Gerador de Benefício Livre",
                "risk": "Médio",
                "return_pa": "8-12%",
                "tax_benefit": "0%",
                "description": "Aposentadoria privada sem dedução",
            },
        ],
    }

    @staticmethod
    def render_catalog():
        """Renderiza catálogo interativo de produtos."""
        st.subheader("💼 Catálogo de Produtos Financeiros")

        # Categoria
        category = st.selectbox(
            "Selecione uma categoria",
            list(ProductCatalog.PRODUCTS.keys()),
        )

        products = ProductCatalog.PRODUCTS[category]

        # Exibir produtos
        for i, product in enumerate(products):
            with st.expander(f"📌 {product['name']}", expanded=(i == 0)):
                cols = st.columns(2)

                with cols[0]:
                    for key, value in product.items():
                        if key != "name":
                            st.write(f"**{key}**: {value}")

                with cols[1]:
                    if st.button(
                        "📊 Simular Aplicação",
                        key=f"sim_{category}_{i}",
                    ):
                        st.session_state["selected_product"] = product["name"]
                        st.session_state["selected_category"] = category
                        st.rerun()

        st.info(
            "💡 Clique em 'Simular Aplicação' para fazer projeções financeiras sobre este produto"
        )


class ScenarioSimulator:
    """Simulador de cenários "what-if" para planejamento financeiro."""

    @staticmethod
    def simulate_investment(
        initial_amount: float,
        monthly_contribution: float,
        annual_return: float,
        years: int,
    ) -> pd.DataFrame:
        """Simula crescimento de investimento."""
        months = years * 12
        monthly_return = annual_return / 12 / 100

        balance = initial_amount
        data = []

        for month in range(1, months + 1):
            balance = balance * (1 + monthly_return) + monthly_contribution
            year = (month - 1) // 12 + 1

            data.append(
                {
                    "Month": month,
                    "Year": year,
                    "Balance": balance,
                    "Total_Contributed": initial_amount
                    + (monthly_contribution * month),
                    "Gains": balance
                    - (initial_amount + monthly_contribution * month),
                }
            )

        return pd.DataFrame(data)

    @staticmethod
    def simulate_loan(
        principal: float,
        annual_rate: float,
        months: int,
    ) -> pd.DataFrame:
        """Simula amortização de empréstimo."""
        monthly_rate = annual_rate / 12 / 100
        monthly_payment = principal * (
            monthly_rate * (1 + monthly_rate) ** months
        ) / ((1 + monthly_rate) ** months - 1)

        balance = principal
        data = []

        for month in range(1, months + 1):
            interest = balance * monthly_rate
            principal_payment = monthly_payment - interest
            balance -= principal_payment

            data.append(
                {
                    "Month": month,
                    "Payment": monthly_payment,
                    "Principal": principal_payment,
                    "Interest": interest,
                    "Balance": max(0, balance),
                }
            )

        return pd.DataFrame(data)

    @staticmethod
    def render_simulator():
        """Renderiza simulador interativo."""
        st.subheader("🎯 Simulador de Cenários")

        sim_type = st.radio(
            "Tipo de Simulação",
            ["💰 Investimento", "💳 Empréstimo", "📊 Análise Comparativa"],
        )

        if sim_type == "💰 Investimento":
            ScenarioSimulator._render_investment_simulator()

        elif sim_type == "💳 Empréstimo":
            ScenarioSimulator._render_loan_simulator()

        else:
            ScenarioSimulator._render_comparative_analysis()

    @staticmethod
    def _render_investment_simulator():
        """Simulador de investimentos."""
        col1, col2 = st.columns(2)

        with col1:
            initial = st.number_input(
                "Valor Inicial (R$)",
                min_value=0.0,
                value=1000.0,
            )
            monthly = st.number_input(
                "Contribuição Mensal (R$)",
                min_value=0.0,
                value=500.0,
            )

        with col2:
            annual_return = st.slider(
                "Retorno Anual (%)",
                min_value=0.0,
                max_value=30.0,
                value=10.0,
            )
            years = st.number_input(
                "Período (anos)",
                min_value=1,
                max_value=50,
                value=10,
            )

        if st.button("▶️ Simular Investimento"):
            df = ScenarioSimulator.simulate_investment(
                initial,
                monthly,
                annual_return,
                years,
            )

            # Resumo
            final_balance = df["Balance"].iloc[-1]
            total_contributed = df["Total_Contributed"].iloc[-1]
            gains = df["Gains"].iloc[-1]

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Saldo Final", f"R$ {final_balance:,.2f}")
            with col2:
                st.metric("Total Investido", f"R$ {total_contributed:,.2f}")
            with col3:
                st.metric("Ganhos", f"R$ {gains:,.2f}")

            # Gráfico
            st.line_chart(
                df[["Year", "Balance", "Total_Contributed"]]
                .groupby("Year")
                .tail(1)
                .set_index("Year")
            )

            st.dataframe(df, use_container_width=True)

    @staticmethod
    def _render_loan_simulator():
        """Simulador de empréstimos."""
        col1, col2 = st.columns(2)

        with col1:
            principal = st.number_input(
                "Valor do Empréstimo (R$)",
                min_value=100.0,
                value=10000.0,
            )
            annual_rate = st.slider(
                "Taxa de Juros Anual (%)",
                min_value=0.0,
                max_value=50.0,
                value=10.0,
            )

        with col2:
            months = st.number_input(
                "Período (meses)",
                min_value=1,
                max_value=360,
                value=12,
            )

        if st.button("▶️ Simular Empréstimo"):
            df = ScenarioSimulator.simulate_loan(principal, annual_rate, months)

            # Resumo
            monthly_payment = df["Payment"].iloc[0]
            total_paid = df["Payment"].sum()
            total_interest = df["Interest"].sum()

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Parcela Mensal", f"R$ {monthly_payment:,.2f}")
            with col2:
                st.metric("Total a Pagar", f"R$ {total_paid:,.2f}")
            with col3:
                st.metric("Juros Totais", f"R$ {total_interest:,.2f}")

            # Gráfico
            st.line_chart(df.set_index("Month")[["Balance", "Payment"]])

            st.dataframe(df, use_container_width=True)

    @staticmethod
    def _render_comparative_analysis():
        """Compara múltiplos cenários de investimento."""
        st.write("Simule múltiplos cenários e compare resultados")

        col1, col2 = st.columns(2)

        with col1:
            initial = st.number_input(
                "Valor Inicial (R$)", min_value=0.0, value=5000.0
            )
            monthly = st.number_input(
                "Contribuição Mensal (R$)",
                min_value=0.0,
                value=500.0,
            )
            years = st.number_input("Período (anos)", min_value=1, value=10)

        with col2:
            st.write("**Cenários de Retorno:**")
            scenarios = {
                "Conservador": st.checkbox("Conservador (6% a.a.)", value=True),
                "Moderado": st.checkbox("Moderado (10% a.a.)", value=True),
                "Agressivo": st.checkbox("Agressivo (15% a.a.)", value=True),
            }

        if st.button("▶️ Comparar Cenários"):
            results = {}

            if scenarios["Conservador"]:
                results["Conservador"] = ScenarioSimulator.simulate_investment(
                    initial, monthly, 6, years
                )
            if scenarios["Moderado"]:
                results["Moderado"] = ScenarioSimulator.simulate_investment(
                    initial, monthly, 10, years
                )
            if scenarios["Agressivo"]:
                results["Agressivo"] = ScenarioSimulator.simulate_investment(
                    initial, monthly, 15, years
                )

            # Comparar finais
            comparison = pd.DataFrame(
                {
                    name: [df["Balance"].iloc[-1], df["Gains"].iloc[-1]]
                    for name, df in results.items()
                },
                index=["Saldo Final", "Ganhos"],
            )

            st.dataframe(comparison.T, use_container_width=True)

            # Gráfico comparativo
            chart_data = pd.concat(
                {
                    name: df.set_index("Year")["Balance"].groupby(level=0).tail(1)
                    for name, df in results.items()
                },
                axis=1,
            )
            st.line_chart(chart_data)


def render_catalog_page():
    """Página completa de catálogo e simulador."""
    st.title("💼 Produtos Financeiros e Simulador")

    tab1, tab2 = st.tabs(["📋 Catálogo", "🎯 Simulador"])

    with tab1:
        ProductCatalog.render_catalog()

    with tab2:
        ScenarioSimulator.render_simulator()
