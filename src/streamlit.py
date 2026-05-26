"""
Compatibilidade de entrada para a plataforma de deploy.
Este arquivo existe para manter o mesmo módulo principal esperado pela plataforma
(antes era `src/streamlit.py`). Ele simplesmente importa e executa o `app.py`.
"""

from app import *
