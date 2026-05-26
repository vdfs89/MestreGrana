#!/usr/bin/env python3
"""
Script de Validação Completa - MestreGrana
Valida todas as configurações: LLM, Neon, Atlas
"""

import os
import sys
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

print("\n" + "=" * 70)
print("🔍 VALIDAÇÃO COMPLETA - MestreGrana")
print("=" * 70 + "\n")

# ===== 1. Verificar variáveis de ambiente =====
print("1️⃣  Verificando Variáveis de Ambiente...")
print("-" * 70)

env_vars = {
    "GROQ_API_KEY": "🤖 Groq LLM",
    "GEMINI_API_KEY": "🎨 Google Gemini",
    "OPENAI_API_KEY": "🚀 OpenAI",
    "DATABASE_URL": "🗄️ Neon Database",
    "MONGODB_ATLAS_URI": "🍃 MongoDB Atlas",
}

found_vars = {}
missing_vars = {}

for var, label in env_vars.items():
    value = os.environ.get(var)
    if value:
        # Esconde parte da chave por segurança
        masked = value[:20] + "..." if len(value) > 20 else value
        print(f"   ✅ {label}: {masked}")
        found_vars[var] = value
    else:
        print(f"   ❌ {label}: NÃO CONFIGURADO")
        missing_vars[var] = label

print(f"\n   Resumo: {len(found_vars)}/5 variáveis encontradas")

# ===== 2. Testar LLM APIs =====
print("\n2️⃣  Testando APIs de IA...")
print("-" * 70)

# Groq
if "GROQ_API_KEY" in found_vars:
    try:
        from groq import Groq
        client = Groq(api_key=found_vars["GROQ_API_KEY"])
        # Test simple call
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=10
        )
        print("   ✅ Groq: Funcionando")
    except Exception as e:
        print(f"   ❌ Groq: Erro - {str(e)[:60]}")
else:
    print("   ⚪ Groq: Não configurado")

# Gemini
if "GEMINI_API_KEY" in found_vars:
    try:
        import google.generativeai as genai
        genai.configure(api_key=found_vars["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content("ping", stream=False)
        print("   ✅ Gemini: Funcionando")
    except Exception as e:
        print(f"   ❌ Gemini: Erro - {str(e)[:60]}")
else:
    print("   ⚪ Gemini: Não configurado")

# OpenAI
if "OPENAI_API_KEY" in found_vars:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=found_vars["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=10
        )
        print("   ✅ OpenAI: Funcionando")
    except Exception as e:
        print(f"   ❌ OpenAI: Erro - {str(e)[:60]}")
else:
    print("   ⚪ OpenAI: Não configurado")

# ===== 3. Testar Neon =====
print("\n3️⃣  Testando Neon Database...")
print("-" * 70)

if "DATABASE_URL" in found_vars:
    try:
        import psycopg2
        from psycopg2 import pool
        
        # Create pool
        connection_pool = pool.SimpleConnectionPool(
            2, 10, found_vars["DATABASE_URL"], sslmode="require"
        )
        
        # Test connection
        conn = connection_pool.getconn()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        cur.close()
        connection_pool.putconn(conn)
        connection_pool.closeall()
        
        pg_version = version.split(",")[0]
        print(f"   ✅ Neon: Conectado - {pg_version}")
    except ImportError:
        print("   ❌ Neon: Falta psycopg2-binary (pip install psycopg2-binary)")
    except Exception as e:
        print(f"   ❌ Neon: Erro - {str(e)[:60]}")
else:
    print("   ⚪ Neon: Não configurado")
    print("      👉 Execute: https://neon.tech")

# ===== 4. Testar MongoDB Atlas =====
print("\n4️⃣  Testando MongoDB Atlas...")
print("-" * 70)

if "MONGODB_ATLAS_URI" in found_vars:
    try:
        from pymongo import MongoClient
        
        client = MongoClient(
            found_vars["MONGODB_ATLAS_URI"],
            tls=True,
            serverSelectionTimeoutMS=5000
        )
        client.admin.command("ping")
        print("   ✅ MongoDB: Conectado")
        client.close()
    except ImportError:
        print("   ❌ MongoDB: Falta pymongo (pip install pymongo)")
    except Exception as e:
        print(f"   ❌ MongoDB: Erro - {str(e)[:60]}")
else:
    print("   ⚪ MongoDB: Não configurado (opcional)")
    print("      👉 Execute: https://www.mongodb.com/cloud/atlas")

# ===== 5. Resumo Final =====
print("\n5️⃣  Resumo Final")
print("-" * 70)

status_summary = {
    "🤖 LLM (Groq/Gemini/OpenAI)": "GROQ_API_KEY" in found_vars,
    "🗄️ Neon Database": "DATABASE_URL" in found_vars,
    "🍃 MongoDB Atlas": "MONGODB_ATLAS_URI" in found_vars,
}

all_ok = True
for service, is_configured in status_summary.items():
    symbol = "🟢" if is_configured else "🔴"
    status = "Configurado" if is_configured else "Não configurado"
    print(f"   {symbol} {service}: {status}")
    if not is_configured and "Não" in status:
        all_ok = False

print("\n" + "=" * 70)
if all_ok:
    print("✅ TUDO PRONTO! Execute: streamlit run src/streamlit.py")
else:
    print("⚠️  FALTAM CONFIGURAÇÕES")
    print("\n📝 Próximos passos:")
    print("   1. Copie .env.example para .env")
    print("   2. Preencha suas chaves de API")
    print("   3. Execute novamente este script")
    print("   4. Execute: streamlit run src/streamlit.py")

print("=" * 70 + "\n")
