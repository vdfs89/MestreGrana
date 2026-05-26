"""Card and KPI display components."""

try:
    import streamlit as st
except Exception:
    from _stubs import st

import plotly.graph_objects as go


def render_stat_card(title, value, subtitle="", icon="📊", color="#4F8A10"):
    """Render a single stat card.
    
    Args:
        title: str - Card title
        value: str - Main value
        subtitle: str - Subtitle/description
        icon: str - Emoji icon
        color: str - Hex color
    """
    st.metric(title, value, delta=subtitle)


def render_info_card(title, content, icon="ℹ️"):
    """Render an info card with styled container.
    
    Args:
        title: str - Card title
        content: str - Card content
        icon: str - Emoji icon
    """
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        st.markdown(f"### {icon}")
    with col2:
        st.markdown(f"**{title}**")
        st.markdown(content)


def render_kpi_section(kpi_data):
    """Render KPI section with multiple cards.
    
    Args:
        kpi_data: list - List of dicts with {title, value, delta, icon}
    """
    cols = st.columns(len(kpi_data))
    for col, kpi in zip(cols, kpi_data):
        with col:
            with st.container(border=True):
                st.metric(
                    label=kpi["title"],
                    value=kpi["value"],
                    delta=kpi.get("delta"),
                )


def render_progress_card(title, progress, max_value=100):
    """Render progress card.
    
    Args:
        title: str - Card title
        progress: float - Current progress
        max_value: float - Max value
    """
    percentage = (progress / max_value) * 100
    st.metric(f"{title} ({percentage:.1f}%)", progress, max_value=max_value)


def render_chart_card(title, fig, key=None):
    """Render card with chart.
    
    Args:
        title: str - Card title
        fig: plotly Figure - Chart figure
        key: str - Unique key
    """
    with st.container(border=True):
        st.markdown(f"### {title}")
        st.plotly_chart(fig, use_container_width=True, key=key)


def render_data_card(title, data_dict, icon="📋"):
    """Render data card with key-value pairs.
    
    Args:
        title: str - Card title
        data_dict: dict - Data to display
        icon: str - Emoji icon
    """
    with st.container(border=True):
        st.markdown(f"### {icon} {title}")
        for key, value in data_dict.items():
            st.markdown(f"**{key}:** {value}")


def render_status_indicator(status, message=""):
    """Render status indicator with color.
    
    Args:
        status: str - 'success', 'error', 'warning', 'pending'
        message: str - Status message
    """
    status_icons = {
        "success": "🟢",
        "error": "🔴",
        "warning": "🟡",
        "pending": "⚪",
    }
    
    icon = status_icons.get(status, "⚪")
    st.markdown(f"{icon} {message}")


def render_feature_card(title, description, icon="✨", url=None):
    """Render feature card.
    
    Args:
        title: str - Feature title
        description: str - Feature description
        icon: str - Emoji icon
        url: str - Optional link URL
    """
    with st.container(border=True):
        st.markdown(f"## {icon} {title}")
        st.markdown(description)
        if url:
            st.markdown(f"[Saiba mais →]({url})")


def render_testimonial_card(author, text, rating=5):
    """Render testimonial card.
    
    Args:
        author: str - Testimonial author
        text: str - Testimonial text
        rating: int - Rating (1-5)
    """
    stars = "⭐" * rating + "☆" * (5 - rating)
    with st.container(border=True):
        st.markdown(f"_\"{text}\"_")
        st.markdown(f"**{author}** {stars}")
