"""Interactive table components using Streamlit and Pandas."""

try:
    import streamlit as st
except Exception:
    from _stubs import st

import pandas as pd


def render_transactions_table(df, title="Transações"):
    """Render transactions table with filtering and sorting."""
    if df is None or df.empty:
        st.warning(f"Nenhuma {title.lower()} disponível")
        return

    st.subheader(title)
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        if "tipo" in df.columns:
            filtro_tipo = st.selectbox(
                "Filtrar por tipo",
                ["Todos"] + sorted(df["tipo"].unique().tolist()),
                key=f"filtro_tipo_{title}"
            )
            if filtro_tipo != "Todos":
                df = df[df["tipo"] == filtro_tipo]
    
    with col2:
        if "categoria" in df.columns:
            filtro_categoria = st.selectbox(
                "Filtrar por categoria",
                ["Todos"] + sorted(df["categoria"].unique().tolist()),
                key=f"filtro_categoria_{title}"
            )
            if filtro_categoria != "Todos":
                df = df[df["categoria"] == filtro_categoria]
    
    # Sorting
    if "data" in df.columns:
        sort_desc = st.checkbox("Ordenar por data (decrescente)", key=f"sort_{title}")
        df = df.sort_values("data", ascending=not sort_desc)
    
    # Display
    st.dataframe(df, use_container_width=True, height=400)
    
    # Summary
    if "valor" in df.columns:
        total = df["valor"].sum()
        st.metric(f"Total {title.lower()}", f"R$ {total:,.2f}")


def render_products_table(df, title="Produtos"):
    """Render products table with filtering."""
    if df is None or (isinstance(df, pd.DataFrame) and df.empty):
        st.warning(f"Nenhum {title.lower()} disponível")
        return

    st.subheader(title)
    
    # If list of dicts, convert to DataFrame
    if isinstance(df, list):
        df = pd.DataFrame(df)
    
    # Filters
    if "tipo" in df.columns:
        filtro_tipo = st.multiselect(
            "Filtrar por tipo",
            df["tipo"].unique().tolist(),
            default=df["tipo"].unique().tolist(),
            key=f"filtro_tipo_{title}"
        )
        df = df[df["tipo"].isin(filtro_tipo)]
    
    # Display
    st.dataframe(df, use_container_width=True, height=400)


def render_metrics_grid(metrics_dict, cols=4):
    """Render metrics in a grid layout.
    
    Args:
        metrics_dict: dict with {label: value}
        cols: number of columns (default 4)
    """
    if not metrics_dict:
        return
    
    col_list = st.columns(cols)
    for idx, (label, value) in enumerate(metrics_dict.items()):
        col_idx = idx % cols
        with col_list[col_idx]:
            st.metric(label, value)


def render_kpi_cards(kpi_data):
    """Render KPI cards with color coding.
    
    Args:
        kpi_data: list of {"title": "", "value": "", "delta": "", "color": ""}
    """
    if not kpi_data:
        return
    
    cols = st.columns(len(kpi_data))
    for col, kpi in zip(cols, kpi_data):
        with col:
            st.metric(
                kpi["title"],
                kpi["value"],
                delta=kpi.get("delta"),
            )
