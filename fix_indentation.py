"""Script para indentar o código do assistente dentro do else: block"""

# Ler o arquivo
with open("src/streamlit.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Encontrar a linha com "else:" que adicionamos (marcada com comentário de página padrão)
else_line_idx = None
for i, line in enumerate(lines):
    if "# --- Página padrão: Assistente IA ---" in line:
        else_line_idx = i
        break

if else_line_idx is None:
    print("❌ Não encontrou o comentário de página padrão")
    exit(1)

print(f"✓ Encontrou página padrão na linha {else_line_idx + 1}")

# Indentar todas as linhas após esse comentário
new_lines = lines[:else_line_idx + 1]  # Mantém até o comentário

for i in range(else_line_idx + 1, len(lines)):
    line = lines[i]
    # Não indenta linhas vazias
    if line.strip():  # Se não é vazia
        new_lines.append("    " + line)
    else:
        new_lines.append(line)

# Salvar de volta
with open("src/streamlit.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("✅ Indentação corrigida!")
print(f"   Total de linhas: {len(new_lines)}")
