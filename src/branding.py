"""
Módulo de Branding MestreGrana
Cores, tipografia e componentes visuais da marca
"""

import streamlit as st

# Paleta de Cores Oficial
COLORS = {
    "primary": "#00CB63",      # Verde Primário (logo, destaque)
    "dark": "#042540",         # Azul Escuro (background)
    "black": "#1F1F1F",        # Preto (texto principal)
    "gray": "#8B7280",         # Cinza (texto secundário)
    "white": "#FFFFFF",        # Branco (contraste)
}

# Taglines
TAGLINE = "MEDE. PLANEJA. MULTIPLICA."
TAGLINE_FULL = {
    "mede": "Acompanhe seus números com clareza e precisão.",
    "planeja": "Manage seu futuro e tome decisões inteligentes.",
    "multiplica": "Transforme controle em crescimento e conquistas."
}

# Tipografia
FONT_PRIMARY = "Poppins"


def apply_custom_theme():
    """Aplica tema customizado com cores da marca ao Streamlit"""
    custom_css = f"""
    <style>
    :root {{
        --primary-color: {COLORS['primary']};
        --dark-color: {COLORS['dark']};
        --black-color: {COLORS['black']};
        --gray-color: {COLORS['gray']};
        --white-color: {COLORS['white']};
    }}
    
    * {{
        font-family: '{FONT_PRIMARY}', sans-serif;
    }}
    
    body {{
        background-color: {COLORS['dark']};
        color: {COLORS['black']};
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {COLORS['dark']};
        border-right: 2px solid {COLORS['primary']};
    }}
    
    /* Botões */
    .stButton > button {{
        background-color: {COLORS['primary']};
        color: {COLORS['white']};
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        background-color: #00B555;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 203, 99, 0.3);
    }}
    
    /* Abas (Tabs) */
    .stTabs [data-baseweb="tab-list"] button {{
        color: {COLORS['gray']};
        border-bottom: 2px solid transparent;
        transition: all 0.3s ease;
    }}
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
        color: {COLORS['primary']};
        border-bottom: 3px solid {COLORS['primary']};
    }}
    
    /* Cards / Containers */
    .stContainer {{
        background-color: {COLORS['white']};
        border-left: 4px solid {COLORS['primary']};
        border-radius: 8px;
        padding: 16px;
    }}
    
    /* Títulos */
    h1, h2, h3, h4, h5, h6 {{
        color: {COLORS['black']};
        font-weight: 700;
    }}
    
    h1 {{
        border-bottom: 3px solid {COLORS['primary']};
        padding-bottom: 10px;
    }}
    
    /* Métricas */
    [data-testid="metric-container"] {{
        background-color: rgba(0, 203, 99, 0.05);
        border-left: 4px solid {COLORS['primary']};
        border-radius: 6px;
        padding: 12px;
    }}
    
    /* Inputs */
    input, textarea, select {{
        border: 2px solid {COLORS['gray']};
        border-radius: 6px;
        padding: 8px 12px;
    }}
    
    input:focus, textarea:focus, select:focus {{
        border-color: {COLORS['primary']};
        box-shadow: 0 0 0 3px rgba(0, 203, 99, 0.1);
    }}
    
    /* Links */
    a {{
        color: {COLORS['primary']};
        text-decoration: none;
        font-weight: 500;
    }}
    
    a:hover {{
        text-decoration: underline;
        color: #00B555;
    }}
    
    /* Dividers */
    hr {{
        border-color: {COLORS['primary']};
        opacity: 0.3;
    }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


def render_header():
    """Renderiza o header/branding no topo da página"""
    header_html = f"""
    <div style="background: linear-gradient(135deg, {COLORS['dark']} 0%, {COLORS['primary']} 100%); 
                padding: 24px 16px; border-radius: 8px; margin-bottom: 20px; 
                text-align: center; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);">
        <h1 style="color: {COLORS['white']}; margin: 0; font-size: 32px; font-weight: 700;">
            <span style="color: {COLORS['primary']};">MG</span>
            <span style="margin-left: 8px;">MestreGrana</span>
        </h1>
        <p style="color: {COLORS['white']}; margin: 8px 0 0 0; font-size: 14px; 
                  font-weight: 500; letter-spacing: 1px; opacity: 0.9;">
            {TAGLINE}
        </p>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def render_feature_card(title, description, icon="💡"):
    """Renderiza um card de feature com branding"""
    card_html = f"""
    <div style="background-color: {COLORS['white']}; 
                border-left: 4px solid {COLORS['primary']}; 
                border-radius: 8px; padding: 16px; 
                margin-bottom: 12px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <span style="font-size: 24px; margin-right: 12px;">{icon}</span>
            <h3 style="color: {COLORS['primary']}; margin: 0; font-size: 18px; font-weight: 600;">
                {title}
            </h3>
        </div>
        <p style="color: {COLORS['gray']}; margin: 0; font-size: 14px;">
            {description}
        </p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def render_stats_card(label, value, change=None, icon="📊"):
    """Renderiza um card de estatísticas com branding"""
    change_color = COLORS['primary'] if (change and float(str(change).replace('%', '')) > 0) else COLORS['gray']
    change_html = f"<span style='color: {change_color}; font-weight: 600;'>{change}</span>" if change else ""
    
    card_html = f"""
    <div style="background: linear-gradient(135deg, rgba(0, 203, 99, 0.1) 0%, rgba(4, 37, 64, 0.1) 100%);
                border: 2px solid {COLORS['primary']}; border-radius: 8px; 
                padding: 16px; text-align: center;">
        <div style="font-size: 24px; margin-bottom: 8px;">{icon}</div>
        <div style="font-size: 24px; font-weight: 700; color: {COLORS['primary']}; margin-bottom: 4px;">
            {value}
        </div>
        <div style="font-size: 12px; color: {COLORS['gray']}; font-weight: 500;">
            {label}
        </div>
        {change_html if change_html else ""}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def render_section_divider(title=""):
    """Renderiza um divisor de seção com branding"""
    divider_html = f"""
    <div style="margin: 24px 0; border-top: 3px solid {COLORS['primary']}; 
                padding-top: 12px;">
        {f"<p style='color: {COLORS['primary']}; font-weight: 600; font-size: 14px; margin: 0;'>{title}</p>" if title else ""}
    </div>
    """
    st.markdown(divider_html, unsafe_allow_html=True)


def get_color(name: str):
    """Retorna uma cor da paleta pelo nome"""
    return COLORS.get(name.lower(), COLORS['primary'])
