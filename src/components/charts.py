import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def plot_saldo_evolution(historico_df):
    """Plot evolution of account balance over time."""
    if historico_df is None or historico_df.empty or "data" not in historico_df.columns:
        return None
    
    if "saldo" not in historico_df.columns:
        return None
    
    fig = px.line(
        historico_df,
        x="data",
        y="saldo",
        markers=True,
        title="Evolução do Saldo",
        labels={"data": "Data", "saldo": "Saldo (R$)"},
    )
    fig.update_traces(line=dict(color="#4F8A10", width=2))
    fig.update_layout(hovermode="x unified")
    return fig


def plot_gastos_categoria(transacoes_df):
    """Plot spending by category."""
    if transacoes_df is None or transacoes_df.empty:
        return None
    
    if "tipo" not in transacoes_df.columns or "categoria" not in transacoes_df.columns:
        return None
    
    gastos = transacoes_df[transacoes_df["tipo"] == "saida"]
    if gastos.empty:
        return None
    
    gastos_categoria = gastos.groupby("categoria")["valor"].sum().sort_values()
    
    fig = px.barh(
        x=gastos_categoria.values,
        y=gastos_categoria.index,
        title="Gastos por Categoria",
        labels={"x": "Valor (R$)", "y": "Categoria"},
    )
    fig.update_traces(marker=dict(color="#FFB347"))
    fig.update_layout(hovermode="y unified")
    return fig


def plot_receitas_vs_despesas(transacoes_df):
    """Plot income vs expenses over time."""
    if transacoes_df is None or transacoes_df.empty:
        return None
    
    if "data" not in transacoes_df.columns or "tipo" not in transacoes_df.columns:
        return None
    
    receitas = transacoes_df[transacoes_df["tipo"] == "entrada"].groupby("data")["valor"].sum()
    despesas = transacoes_df[transacoes_df["tipo"] == "saida"].groupby("data")["valor"].sum()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=receitas.index, y=receitas.values, name="Receitas", mode="lines+markers"))
    fig.add_trace(go.Scatter(x=despesas.index, y=despesas.values, name="Despesas", mode="lines+markers"))
    
    fig.update_layout(
        title="Receitas vs Despesas",
        xaxis_title="Data",
        yaxis_title="Valor (R$)",
        hovermode="x unified",
    )
    return fig
