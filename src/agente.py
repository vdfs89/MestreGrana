import pandas as pd
import json
from groq import Groq
import google.generativeai as genai
from openai import OpenAI

class FinanceForge:
    def __init__(self, keys):
        self.keys = keys
        self.client_groq = Groq(api_key=keys["GROQ"])
        genai.configure(api_key=keys["GEMINI"])
        self.client_openai = OpenAI(api_key=keys["OPENAI"])

    def carregar_contexto_rag(self):
        try:
            perfil = json.load(open("data/perfil_investidor.json", "r", encoding='utf-8'))
            produtos = json.load(open("data/produtos_financeiros.json", "r", encoding='utf-8'))
            transacoes = pd.read_csv("data/transacoes.csv")
            historico = pd.read_csv("data/historico_atendimento.csv")
            saldo = transacoes[transacoes['tipo']=='entrada']['valor'].sum() - transacoes[transacoes['tipo']=='saida']['valor'].sum()
            resumo = f"""
            DADOS DO CLIENTE: {perfil['nome']}, {perfil['idade']} anos, {perfil['profissao']}.
            PERFIL: {perfil['perfil_investidor']}. OBJETIVO: {perfil['objetivo_principal']}.
            SALDO ATUAL: R$ {saldo:.2f}.
            HISTÓRICO RECENTE: {historico['resumo'].iloc[-1]}
            PRODUTOS DISPONÍVEIS: {str(produtos)[:500]}...
            """
            return resumo
        except Exception as e:
            return f"Erro ao carregar base de conhecimento: {e}"

    def responder(self, mensagens_chat):
        contexto_real = self.carregar_contexto_rag()
        system_msg = {
            "role": "system", 
            "content": f"Você é o FinanceForge. Use este contexto real para responder: {contexto_real}. Seja proativo e cite valores específicos dos arquivos CSV/JSON."
        }
        prompt_completo = [system_msg] + mensagens_chat

        # Failover: Groq → Gemini → OpenAI
        try:
            resp = self.client_groq.chat.completions.create(
                model="llama-3.3-70b-versatile", messages=prompt_completo
            )
            return resp.choices[0].message.content, "Groq (Llama 3.3)"
        except:
            pass
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            resp = model.generate_content(f"{system_msg['content']}\n\nUsuário: {mensagens_chat[-1]['content']}")
            return resp.text, "Google Gemini"
        except:
            return "Sistemas sobrecarregados. Tente novamente.", "Offline"
