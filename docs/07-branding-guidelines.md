# 📱 Guia de Branding MestreGrana

## Identidade Visual

MestreGrana é uma aplicação de educação financeira que visa capacitar usuários a **medir, planejar e multiplicar** seus recursos financeiros. A identidade visual reflete modernidade, confiança e crescimento.

---

## Paleta de Cores

| Cor | Código Hex | Uso |
|-----|-----------|-----|
| 🟢 Verde Primário | `#00CB63` | Logo, CTAs, destaque, elementos interativos |
| 🔵 Azul Escuro | `#042540` | Background, sidebar, elementos secundários |
| ⚫ Preto | `#1F1F1F` | Texto principal, headings |
| ⚪ Cinza | `#8B7280` | Texto secundário, desativado |
| ⚪ Branco | `#FFFFFF` | Fundo, contraste, cards |

### Aplicação de Cores

- **CTA Primário (Botões):** Verde `#00CB63`
- **Hover (Botões):** Verde Escuro `#00B555`
- **Background Principal:** Azul Escuro `#042540`
- **Cards/Containers:** Branco `#FFFFFF` com borda verde esquerda
- **Destaques:** Verde primário
- **Texto:** Preto para ênfase, Cinza para secundário

---

## Tipografia

### Fonte Primária: **Poppins**

- **Regular (400):** Corpo de texto, descrições
- **Medium (500):** Labels, subtítulos
- **SemiBold (600):** Destaques, cards
- **Bold (700):** Headings, títulos principais

### Hierarquia de Tamanhos

| Elemento | Tamanho | Peso | Uso |
|----------|--------|------|-----|
| H1 | 32px | 700 | Títulos de página (Header) |
| H2 | 28px | 700 | Títulos de seção |
| H3 | 20px | 600 | Subtítulos |
| Body | 14px | 400 | Corpo de texto |
| Small | 12px | 500 | Rótulos, metatexto |

---

## Logo e Marca

### Logo Padrão
- **Símbolo:** MG com seta de tendência
- **Cores:** Verde primário com variações
- **Tamanho mínimo:** 48x48px

### Tagline Oficial
**"MEDE. PLANEJA. MULTIPLICA."**

### Significados dos Pilares

| Pilar | Descrição |
|-------|-----------|
| **MEDE** | Acompanhe seus números com clareza e precisão |
| **PLANEJA** | Manage seu futuro e tome decisões inteligentes |
| **MULTIPLICA** | Transforme controle em crescimento e conquistas |

---

## Componentes de UI

### Botões

```
Estilo: Retângulo com bordas suavizadas (border-radius: 6px)
Cor: Verde #00CB63
Texto: Branco, bold
Hover: Verde escuro #00B555, com sombra e elevação
```

### Cards

```
Estilo: Borda esquerda verde (4px)
Border-radius: 8px
Sombra: Suave (0 2px 8px rgba(0, 0, 0, 0.1))
Background: Branco
```

### Abas (Tabs)

```
Ativo: Texto verde, borda inferior verde (3px)
Inativo: Texto cinza, borda inferior transparente
Transição: Suave (0.3s)
```

### Dividers

```
Cor: Verde com 30% de opacidade
Espessura: 1px
Margem: 24px acima e abaixo
```

### Métricas/KPIs

```
Background: Verde com 5% de opacidade
Borda esquerda: Verde (4px)
Border-radius: 6px
Padding: 12px
Destaque: Número em verde bold
```

---

## Ícones e Emojis

A aplicação usa ícones em emoji para melhor usabilidade:

| Ícone | Contexto |
|-------|----------|
| 💬 | Assistente/Chat |
| 📊 | Dashboard/Análise |
| 📋 | Auditoria |
| 📈 | Relatórios/Crescimento |
| 💼 | Produtos/Simulador |
| 💸 | MestreGrana (favicon) |
| 🟢 | Status Online |
| 🔴 | Status Offline |
| ⚙️ | Conformidade/Configurações |

---

## Aplicação Streamlit

### Configuração Inicial

```python
from branding import apply_custom_theme, render_header

st.set_page_config(page_title="MestreGrana", page_icon="💸", layout="wide")

# Aplicar tema customizado
apply_custom_theme()

# Renderizar header
render_header()
```

### Componentes Disponíveis

#### Header
```python
from branding import render_header
render_header()  # Renderiza MG MestreGrana com tagline
```

#### Feature Card
```python
from branding import render_feature_card
render_feature_card(
    title="Minha Feature",
    description="Descrição da feature",
    icon="📊"
)
```

#### Stats Card
```python
from branding import render_stats_card
render_stats_card(
    label="Saldo Atual",
    value="R$ 1.250,00",
    change="+5.2%",
    icon="💰"
)
```

#### Section Divider
```python
from branding import render_section_divider
render_section_divider("Nova Seção")
```

### CSS Customizado

O tema customizado aplica automaticamente:

- **Cores primárias** em todos os componentes Streamlit
- **Espaçamento e bordas** consistentes
- **Efeitos hover** suaves
- **Tipografia Poppins** em toda a interface
- **Gradientes** em seções principais

---

## Acessibilidade

- ✅ Contraste WCAG AA+ entre texto e fundo
- ✅ Cores não são único indicador de status
- ✅ Fonte legível em todos os tamanhos
- ✅ Espaçamento adequado entre elementos

---

## Diretrizes Gerais

1. **Consistência:** Use sempre as cores definidas
2. **Hierarquia:** Respeite a tipografia proposta
3. **Espaçamento:** 8px base (8, 16, 24, 32...)
4. **Ícones:** Use emojis padronizados do projeto
5. **Responsividade:** Teste em múltiplos tamanhos

---

## Documentação de Cor

### Verde Primário #00CB63

- **RGB:** 0, 203, 99
- **HSL:** 151°, 100%, 40%
- **Uso:** CTAs, destaque, logo
- **Acessibilidade:** Alto contraste com branco e escuro

### Azul Escuro #042540

- **RGB:** 4, 37, 64
- **HSL:** 206°, 88%, 13%
- **Uso:** Background, sidebar
- **Acessibilidade:** Excelente para texto branco

---

## Links e Recursos

- **Tipografia:** [Poppins no Google Fonts](https://fonts.google.com/specimen/Poppins)
- **Módulo:** `src/branding.py`
- **Documentação Técnica:** Veja comentários no código

---

*Última atualização: 17 de maio de 2026*
*Versão: 1.0*
