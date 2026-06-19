"""
Exemplo de uso: MestreGrana AI & Datasets
Como carregar dados locais (perfil, transações) e consultar o mentor de IA.
"""

import sys
from pathlib import Path

# Adiciona o diretório src/ e root ao caminho de busca do Python
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from services.data_service import load_perfil, load_transacoes
from core.llm_client import call_llm_with_fallback

def main():
    print("=" * 60)
    print("🤖 Exemplo de Uso - MestreGrana AI & Dados Locais")
    print("=" * 60)
    
    # 1. Carregar dados reais simulados
    print("\n1️⃣  Carregando dados financeiros locais...")
    perfil = load_perfil()
    transacoes = load_transacoes()
    
    if not perfil:
        print("❌ Perfil do investidor não encontrado. Verifique data/perfil_investidor.json.")
        return
        
    print(f"   ✅ Perfil carregado: {perfil.get('nome')} ({perfil.get('perfil_investidor')})")
    print(f"   ✅ Total de transações carregadas: {len(transacoes)}")
    
    # 2. Montar pergunta
    pergunta = "Com base no meu objetivo de construir reserva de emergência e no meu perfil, o que eu devo priorizar?"
    print(f"\n2️⃣  Pergunta simulada:")
    print(f"   \"{pergunta}\"")
    
    # 3. Montar prompt do sistema
    transacoes_str = transacoes.to_string() if not transacoes.empty else "Nenhuma transação registrada."
    prompt = f"""Você é o MestreGrana, um mentor financeiro experiente.
Oriente o usuário com base nos seguintes dados reais:
Nome: {perfil.get('nome')}
Idade: {perfil.get('idade')}
Renda Mensal: R$ {perfil.get('renda_mensal', 0):,.2f}
Perfil: {perfil.get('perfil_investidor')}
Objetivo: {perfil.get('objetivo_principal')}
Reserva de Emergência Atual: R$ {perfil.get('reserva_emergencia_atual', 0):,.2f}

Transações recentes:
{transacoes_str}

Pergunta: {pergunta}
Resposta:"""
    
    # 4. Chamar LLM com fallback automático
    print("\n3️⃣  Consultando IA MestreGrana (com failover automático)...")
    resposta = call_llm_with_fallback(prompt)
    
    if resposta:
        print("\n4️⃣  Resposta do Mentor MestreGrana:")
        print("-" * 60)
        print(resposta)
        print("-" * 60)
    else:
        print("❌ Erro: Não foi possível obter resposta dos LLMs disponíveis.")

if __name__ == "__main__":
    main()
