# Checklist de Segurança - MestreGrana

## ✅ Pré-Deploy (Antes de Colocar em Produção)

### Código
- [ ] Todas as queries usam prepared statements (`%s`)
- [ ] Nenhuma concatenação de SQL (`f"SELECT ... {var}"` ❌)
- [ ] Inputs validados com `DataSecurity.validate_*()`
- [ ] Strings sanitizadas com `DataSecurity.sanitize_string()`
- [ ] Detecção de SQL injection em inputs críticos

### Secrets e Credenciais
- [ ] `.env` NUNCA foi commitado (verificar: `git log --all --full-history -- .env`)
- [ ] Todas as chaves em st.secrets (Streamlit Cloud) ou variáveis de ambiente
- [ ] Nenhuma chave API hardcoded no código
- [ ] `.gitignore` contém `.env`, `*.pem`, `credentials.json`
- [ ] Permissões de `.env` restritas: `chmod 600 .env` (Linux/Mac)

### Banco de Dados
- [ ] CONNECTION_STRING usa `?sslmode=require` (TLS obrigatório)
- [ ] Usuário BD não é admin (least privilege)
- [ ] Backup criptografado configurado (Neon console)
- [ ] Tabela `audit_log` testada
- [ ] Tabela `user_consents` funcional

### Autenticação e LGPD
- [ ] Banner de consentimento de cookies renderizando
- [ ] Termo de Uso visível ([TERMO_DE_USO.md](TERMO_DE_USO.md))
- [ ] `CookieConsent.render_consent_banner()` no topo de streamlit.py
- [ ] Consentimento sendo salvo no banco
- [ ] Direito ao esquecimento implementado

### Logs e Auditoria
- [ ] Logs não contêm senhas, tokens ou dados sensíveis
- [ ] Auditoria de mudanças registrada em `audit_log`
- [ ] IP do usuário capturado (para segurança)
- [ ] Timestamps em UTC (evitar timezone issues)

### Dependências
- [ ] `pip-audit` executado - zero vulnerabilidades críticas
- [ ] `pip list --outdated` - dependências atualizadas
- [ ] Não há `requirements.txt` com versões indefinidas (`==1.2.3`, não `>=1.0`)

### Teste de Segurança
- [ ] Form de teste: valores inválidos rejeitados
- [ ] Form de teste: SQL injection detectado/bloqueado
- [ ] Conexão BD com SSL funcionando
- [ ] Health check Neon OK: `python src/validate_neon.py`

### Documentação
- [ ] [TERMO_DE_USO.md](TERMO_DE_USO.md) completo e atualizado
- [ ] [06-data-security.md](06-data-security.md) linkizado
- [ ] [05-cookies-consent.md](05-cookies-consent.md) linkizado
- [ ] README menciona conformidade LGPD
- [ ] Reporte de vulnerabilidades explicado

---

## 🔄 Monitoramento Pós-Deploy

### Diário
- [ ] Revisar `audit_log` em busca de atividades suspeitas
- [ ] Verificar status do Neon (console) - sem erros críticos
- [ ] Revisar logs de erro (Streamlit Cloud ou servidor)

### Semanal
- [ ] Verificar permissões de usuários BD
- [ ] Revisar backups (status OK?)
- [ ] Teste manual: form com inputs maliciosos

### Mensal
- [ ] `pip-audit` - verificar novas vulnerabilidades
- [ ] Rotacionar chaves API antigas
- [ ] Revisar política de retenção de dados (respeitar LGPD)
- [ ] Teste de recuperação de backup

### Trimestral
- [ ] Auditoria de segurança completa
- [ ] Penetration testing (contratar especialista)
- [ ] Revisar e atualizar [TERMO_DE_USO.md](TERMO_DE_USO.md)
- [ ] Treinar developers em OWASP Top 10

---

## 🚨 Resposta a Incidentes

### Se houver Vazamento de Dados

1. **PARAR APP IMEDIATAMENTE** (Streamlit Cloud → Stop)
2. **Revogar chaves comprometidas** (Neon console, Groq/OpenAI dashboards)
3. **Notificar usuários** (email/notificação app)
4. **Investigar**: logs, audit_log, backups
5. **Corrigir**: patches de segurança
6. **Deploy + Testes**: validar correção
7. **Relatar**: à Receita Federal se dados fiscal-related
8. **Comunicação**: transparência sobre o que aconteceu

### Se houver Vulnerabilidade Descoberta

1. **Documentar**: tipo, severidade, reprodução
2. **Criar branch**: `fix/security-{CVE}`
3. **Corrigir**: implementar patch
4. **Testar**: validar correção
5. **Deploy**: prioritário
6. **Agradecer**: researcher que reportou (se divulgação responsável)

---

## 📊 Matriz de Risco

| Ameaça | Probabilidade | Impacto | Mitigação |
|--------|---|--------|-----------|
| SQL Injection | Baixa | CRÍTICO | Prepared statements, sanitização |
| Roubo de Credenciais | Média | CRÍTICO | Variáveis de ambiente, HTTPS |
| XSS (Cross-Site Scripting) | Baixa | Alto | Streamlit já escapa HTML |
| CSRF | Baixa | Médio | Streamlit session tokens |
| Brute Force Login | Baixa | Médio | Rate limiting (a implementar) |
| DDoS | Baixa | Médio | Cloudflare/WAF (se produção) |
| Vazamento LGPD | Médio | CRÍTICO | Criptografia, consentimento, auditoria |
| Erro de Dev | Alta | Variável | Code review, CI/CD testing |

---

## 🛠️ Ferramentas de Segurança

### Instaladas/Configuradas

```bash
# Verificar dependências
pip-audit                      # Vulnerabilidades em packages
bandit -r src/                 # Problemas de segurança no código
pip show -f cryptography       # Versão de criptografia

# Testar validação
python -c "
from src.data_security import DataSecurity
assert DataSecurity.detect_sql_injection(\"'; DROP TABLE--\")
print('✅ SQL Injection detection working')
"
```

### Recomendadas (Próximo)

```bash
# OWASP ZAP (teste de penetração)
docker run -t owasp/zap2docker-stable zap-baseline.py

# Talisman (headers de segurança)
pip install flask-talisman

# Safety (complemento de pip-audit)
pip install safety
safety check
```

---

## 📚 Documentação Relacionada

- [docs/TERMO_DE_USO.md](TERMO_DE_USO.md) - Termos e política de segurança
- [docs/06-data-security.md](06-data-security.md) - Guia técnico de segurança
- [docs/04-neon-integration.md](04-neon-integration.md) - Segurança da BD
- [docs/05-cookies-consent.md](05-cookies-consent.md) - LGPD compliance
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Referência de vulnerabilidades

---

**Arquivo**: `docs/07-security-checklist.md`  
**Última revisão**: 17 de maio de 2026  
**Revisor**: DevSecOps Lead
