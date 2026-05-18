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
    """Renderiza o header/branding profissional com pilares"""
    header_html = f"""
    <div style="background: linear-gradient(135deg, {COLORS['dark']} 0%, rgba(4, 37, 64, 0.8) 100%); 
                padding: 32px 24px; border-radius: 12px; margin-bottom: 28px; 
                box-shadow: 0 8px 24px rgba(0, 203, 99, 0.15); border-top: 4px solid {COLORS['primary']};">
        
        <!-- Título e Tagline -->
        <div style="text-align: center; margin-bottom: 28px;">
            <h1 style="color: {COLORS['white']}; margin: 0 0 8px 0; font-size: 36px; font-weight: 700;">
                <span style="color: {COLORS['primary']};">MG</span>
                <span style="margin-left: 12px;">MestreGrana</span>
            </h1>
            <p style="color: {COLORS['white']}; margin: 0 0 8px 0; font-size: 14px; 
                      font-weight: 500; letter-spacing: 1px; opacity: 0.95;">
                {TAGLINE}
            </p>
            <p style="color: rgba(255, 255, 255, 0.85); margin: 0; font-size: 13px; 
                      max-width: 500px; margin-left: auto; margin-right: auto; line-height: 1.5;">
                Seu aliado inteligente para medir, planejar e multiplicar suas finanças.
            </p>
        </div>
        
        <!-- 4 Pilares -->
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-top: 24px;">
            <!-- Pilar 1: MEDE -->
            <div style="background: rgba(0, 203, 99, 0.1); border-radius: 8px; padding: 16px; 
                        text-align: center; border-left: 4px solid {COLORS['primary']};">
                <div style="font-size: 28px; margin-bottom: 8px;">🎯</div>
                <p style="color: {COLORS['primary']}; margin: 0 0 4px 0; font-weight: 600; font-size: 13px;">
                    MEDE
                </p>
                <p style="color: rgba(255, 255, 255, 0.75); margin: 0; font-size: 11px; line-height: 1.4;">
                    Acompanhe seus números com clareza
                </p>
            </div>
            
            <!-- Pilar 2: PLANEJA -->
            <div style="background: rgba(0, 203, 99, 0.1); border-radius: 8px; padding: 16px; 
                        text-align: center; border-left: 4px solid {COLORS['primary']};">
                <div style="font-size: 28px; margin-bottom: 8px;">📊</div>
                <p style="color: {COLORS['primary']}; margin: 0 0 4px 0; font-weight: 600; font-size: 13px;">
                    PLANEJA
                </p>
                <p style="color: rgba(255, 255, 255, 0.75); margin: 0; font-size: 11px; line-height: 1.4;">
                    Tome decisões inteligentes
                </p>
            </div>
            
            <!-- Pilar 3: MULTIPLICA -->
            <div style="background: rgba(0, 203, 99, 0.1); border-radius: 8px; padding: 16px; 
                        text-align: center; border-left: 4px solid {COLORS['primary']};">
                <div style="font-size: 28px; margin-bottom: 8px;">📈</div>
                <p style="color: {COLORS['primary']}; margin: 0 0 4px 0; font-weight: 600; font-size: 13px;">
                    MULTIPLICA
                </p>
                <p style="color: rgba(255, 255, 255, 0.75); margin: 0; font-size: 11px; line-height: 1.4;">
                    Transforme em crescimento
                </p>
            </div>
            
            <!-- Pilar 4: CONFIANÇA -->
            <div style="background: rgba(0, 203, 99, 0.1); border-radius: 8px; padding: 16px; 
                        text-align: center; border-left: 4px solid {COLORS['primary']};">
                <div style="font-size: 28px; margin-bottom: 8px;">🔐</div>
                <p style="color: {COLORS['primary']}; margin: 0 0 4px 0; font-weight: 600; font-size: 13px;">
                    CONFIANÇA
                </p>
                <p style="color: rgba(255, 255, 255, 0.75); margin: 0; font-size: 11px; line-height: 1.4;">
                    Segurança & Transparência
                </p>
            </div>
        </div>
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


def render_footer():
    """Renderiza o footer com badges de tecnologia"""
    footer_html = f"""
    <div style="background: {COLORS['dark']}; border-top: 2px solid {COLORS['primary']}; 
                padding: 20px 24px; margin-top: 40px; border-radius: 8px;">
        <div style="display: flex; justify-content: center; align-items: center; gap: 32px; flex-wrap: wrap;">
            <!-- Código Aberto -->
            <div style="text-align: center;">
                <div style="font-size: 24px; margin-bottom: 6px;">💻</div>
                <p style="color: {COLORS['white']}; margin: 0; font-size: 12px; font-weight: 500;">
                    Código Aberto
                </p>
            </div>
            
            <!-- Python -->
            <div style="text-align: center;">
                <div style="font-size: 24px; margin-bottom: 6px;">🐍</div>
                <p style="color: {COLORS['white']}; margin: 0; font-size: 12px; font-weight: 500;">
                    Python
                </p>
            </div>
            
            <!-- Streamlit -->
            <div style="text-align: center;">
                <div style="font-size: 24px; margin-bottom: 6px;">⚡</div>
                <p style="color: {COLORS['white']}; margin: 0; font-size: 12px; font-weight: 500;">
                    Streamlit
                </p>
            </div>
            
            <!-- Seguro e Transparente -->
            <div style="text-align: center;">
                <div style="font-size: 24px; margin-bottom: 6px;">🛡️</div>
                <p style="color: {COLORS['white']}; margin: 0; font-size: 12px; font-weight: 500;">
                    Seguro & Transparente
                </p>
            </div>
            
            <!-- Dados que geram valor -->
            <div style="text-align: center;">
                <div style="font-size: 24px; margin-bottom: 6px;">💎</div>
                <p style="color: {COLORS['white']}; margin: 0; font-size: 12px; font-weight: 500;">
                    Dados que geram valor
                </p>
            </div>
        </div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)
