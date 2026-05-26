# 🚀 Setup Rápido - MestreGrana

## ⚡ 3 Passos para Colocar Tudo em Ordem

### Passo 1️⃣: Copiar `.env.example` para `.env`

```bash
# Windows PowerShell
Copy-Item ".env.example" ".env"

# Linux/Mac
cp .env.example .env
```

### Passo 2️⃣: Preencher suas credenciais

Abra `.env` e preencha:

```bash
# ===== 🤖 APIs DE IA =====
GROQ_API_KEY=gsk_sua_chave_groq
GEMINI_API_KEY=sua_chave_gemini
OPENAI_API_KEY=sk_sua_chave_openai

# ===== 🗄️ NEON DATABASE =====
DATABASE_URL=postgresql://seu_usuario:sua_senha@seu_host/seu_db?sslmode=require

# ===== 🍃 MONGODB ATLAS (opcional) =====
# MONGODB_ATLAS_URI=mongodb+srv://user:password@cluster...
```

### Passo 3️⃣: Validar tudo

```bash
python validate_all.py
```

Esperado:
```
🟢 LLM (Groq/Gemini/OpenAI): Configurado
🟢 Neon Database: Conectado - PostgreSQL 17.x
🟢 MongoDB Atlas: Conectado (ou não configurado)

✅ TUDO PRONTO! Execute: streamlit run src/streamlit.py
```

---

## 🔗 Obter Credenciais

### 🤖 Groq (Grátis)
1. Acesse: https://console.groq.com
2. Sign Up com GitHub/email
3. Copie sua `GROQ_API_KEY`

### 🎨 Google Gemini (Grátis)
1. Acesse: https://makersuite.google.com/app/apikey
2. Clique em "Create API Key"
3. Copie a chave

### 🚀 OpenAI (Pago)
1. Acesse: https://platform.openai.com/api-keys
2. Login/Sign Up
3. Crie nova chave e copie

### 🗄️ Neon Database (Grátis, 3 projetos)
1. Acesse: https://neon.tech
2. Sign Up
3. Criar novo projeto
4. Copiar **CONNECTION STRING** completa:
   ```
   postgresql://user:password@ep-xxx.us-east-1.neon.tech/db?sslmode=require
   ```

### 🍃 MongoDB Atlas (Grátis, 5GB)
1. Acesse: https://www.mongodb.com/cloud/atlas
2. Sign Up
3. Criar cluster
4. Obter **Connection String**:
   ```
   mongodb+srv://user:password@cluster.mongodb.net/?retryWrites=true&w=majority
   ```

---

## ✅ Checklist

- [ ] Copiei `.env.example` para `.env`
- [ ] Preenchí `GROQ_API_KEY`
- [ ] Preenchí `GEMINI_API_KEY`
- [ ] Preenchí `OPENAI_API_KEY` (ou deixei em branco)
- [ ] Preenchí `DATABASE_URL` (Neon)
- [ ] Preenchí `MONGODB_ATLAS_URI` (opcional)
- [ ] Executei `python validate_all.py`
- [ ] Tudo mostrou ✅

---

## ▶️ Executar a App

Após validar com sucesso:

```bash
streamlit run src/streamlit.py
```

Esperado na sidebar:
```
Status Atlas: 🟢 Online
Status Neon: 🟢 Online
Status LLM: 🟢 Online
```

---

## 🆘 Troubleshooting

### ❌ "DatabaseError: could not translate host name"
- Verifique se `DATABASE_URL` está correto
- Verifique conexão à internet
- Teste em: https://neon.tech/console

### ❌ "Connection refused"
- Neon pode estar hibernado (free tier)
- Acesse https://neon.tech/console e ative o projeto

### ❌ "Invalid API key"
- Copie exatamente a chave (sem espaços)
- Gere uma nova chave se necessário

---

## 📧 Dúvidas?

Consulte a documentação técnica em `docs/` ou abra uma issue no GitHub.

---

**Última atualização:** 17 de maio de 2026
