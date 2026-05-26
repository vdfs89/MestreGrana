# Termo de Uso e Disclaimer - MestreGrana

## 1. Aviso Legal e Limitações

O **MestreGrana** é um **assistente educacional de IA** para apoio em organização financeira e educação sobre IRPF. **Não é um serviço de consultoria contábil ou tributária profissional**.

### ⚠️ Limitações Críticas

- **Não substitui contador ou auditor**: Qualquer informação gerada deve ser validada com profissional certificado antes de ser usada em declarações à Receita Federal.
- **Sem responsabilidade legal**: Você é responsável por validar os dados e decisões tomadas com base nas sugestões do MestreGrana.
- **Dados fictícios**: O app utiliza dados mockados para demonstração. Seu histórico real é sensível e deve ser protegido.
- **Sem garantia de precisão**: Modelos de IA podem cometer erros ou alucinar dados. Sempre confirme informações críticas.

## 2. Conformidade com LGPD (Lei Geral de Proteção de Dados)

### 2.1 Coleta e Uso de Dados

O MestreGrana coleta os seguintes dados pessoais:

- **Nome e e-mail** (via formulário de login)
- **Endereço IP** (para auditoria)
- **Histórico de transações e conversa** (armazenado em banco de dados)
- **Informações financeiras** (renda, patrimônio, metas)

### 2.2 Base Legal de Tratamento

O processamento ocorre com base em:
- **Consentimento do usuário** (ao usar o app)
- **Interesse legítimo** (melhorar o serviço)

### 2.3 Direitos do Usuário

Você tem direito a:
- ✅ **Acessar** seus dados armazenados
- ✅ **Corrigir** informações incorretas
- ✅ **Excluir** sua conta e histórico (direito ao esquecimento)
- ✅ **Portar** seus dados para outro serviço
- ✅ **Revogar** consentimento a qualquer tempo

Para exercer direitos LGPD, entre em contato via issues do repositório GitHub.

### 2.4 Retenção de Dados

- **Dados de transação**: Mantidos enquanto a conta estiver ativa
- **Logs de acesso**: Retidos por 90 dias para segurança
- **Após exclusão**: Dados são removidos em até 30 dias

## 2.5 Política de Cookies e Consentimento

### O que são Cookies

Cookies são pequenos arquivos de texto armazenados no seu navegador para:

- **✅ Necessários** (obrigatório): Manter sua sessão, lembrar login, funcionalidades básicas do app
- **📊 Analytics** (opcional): Entender como você usa o app, melhorar experiência, corrigir bugs
- **⚙️ Preferências** (opcional): Lembrar suas configurações, tema escuro, atalhos personalizados

### Consentimento LGPD

Na primeira acesso, você verá um banner solicitando seu consentimento:

| Cookie | Obrigatório | Dados Coletados | Provedor |
|--------|-----------|-----------------|----------|
| Necessários | ✅ Sim | Session ID, Auth Token | MestreGrana |
| Analytics | ❌ Não | Páginas visitadas, cliques, erros | Google Analytics, Groq, OpenAI |
| Preferências | ❌ Não | Tema, idioma, histórico de busca | MestreGrana |

### Dados Coletados com Analytics (se consentir)

Se autorizar analytics, coletamos:
- Páginas visitadas e tempo de uso
- Botões clicados, funcionalidades utilizadas
- Erros encontrados (para correção)
- Navegador, SO, resolução (não identifica você individualmente)
- Prompts/queries de chatbot (para melhorar precisão das respostas)

**Estes dados são anonimizados, encriptados em trânsito (TLS) e nunca vendidos a terceiros.**

### Revogação de Consentimento

A qualquer momento, você pode:
1. **Limpar cookies**: Abra F12 → Application → Cookies → Delete all
2. **Revogar consentimento**: Acesse novamente para modificar preferências
3. **Solicitar exclusão**: Crie uma issue em `github.com/vdfs89/MestreGrana` com assunto "LGPD: Revogar Consentimento"

### Cookies de Terceiros

Utilizamos cookies de:
- **Google Analytics**: Análise anônima de uso
- **Groq/OpenAI**: Logging de queries para melhorar modelos (sem dados sensíveis)

Estes terceiros têm suas próprias políticas de privacidade que você pode consultar.

## 3. Conformidade Tributária

### 3.1 O que o MestreGrana NÃO Faz

❌ Não preenche a Declaração de Ajuste Anual do IRPF  
❌ Não calcula imposto a pagar com precisão legal  
❌ Não valida se você é obrigado a declarar  
❌ Não consulta dados da RFB (Receita Federal)  

### 3.2 O que Você Deve Fazer

1. **Consulte um contador** antes de declarar
2. **Valide dados** contra recibos e documentos
3. **Recolha documentos fiscais** (notas, comprovantes)
4. **Avise seu contador** sobre deduções identificadas
5. **Mantenha registros** por 5 anos (prazo de guarda de livros)

### 3.3 Responsabilidade sobre Erros Tributários

- O MestreGrana é apenas um assistente educacional
- Erros em declaração são responsabilidade do declarante
- A Receita Federal pode multar ou processar por informações falsas ou omissão
- Consulte sempre um profissional certificado

## 4. Segurança e Práticas de Proteção

### 4.1 Medidas Implementadas Pelo App

O MestreGrana implementa múltiplas camadas de segurança:

**Validação de Entrada**
- ✅ Validação de e-mail, CPF, telefone, valores monetários
- ✅ Detecção de padrões de SQL injection
- ✅ Sanitização de strings (remoção de caracteres perigosos)
- ✅ Limite de comprimento de entrada (máx 1000 caracteres)

**Proteção do Banco de Dados**
- ✅ Prepared statements (SQL parametrizado - bloqueia 100% SQL injection)
- ✅ Conexões TLS/SSL obrigatórias (Neon padrão)
- ✅ Auditoria automática (tabela `audit_log` registra todas as mudanças)
- ✅ Sem senhas hardcoded no código

**Proteção de Secrets**
- ✅ Variáveis de ambiente seguras (`.env` local, `st.secrets` produção)
- ✅ `.env` nunca commitado (protegido por `.gitignore`)
- ✅ Chaves API rotacionadas automaticamente
- ✅ Acesso restrito via controle de identidade

**Criptografia**
- ✅ HTTPS/TLS obrigatório em transmissão
- ✅ Conexão PostgreSQL com SSL
- ✅ Dados sensíveis hashados quando necessário
- ✅ Cookies encriptados em sessão

**Conformidade**
- ✅ Consentimento explícito de cookies/dados (LGPD)
- ✅ Política de retenção de dados (90 dias logs, 30 dias pós-exclusão)
- ✅ Direito ao esquecimento implementado
- ✅ Auditoria rastreável de acessos (IP, timestamp, mudanças)

Veja documentação técnica completa em [docs/06-data-security.md](06-data-security.md).

### 4.2 O Que NÃO Fazemos

- ❌ **Não armazenamos senhas de terceiros** (bancos, corretoras)
- ❌ **Não integramos com APIs de banco** sem verificação de segurança
- ❌ **Não vendemos seus dados** a terceiros
- ❌ **Não coletamos dados não consentidos**
- ❌ **Não desabilitamos HTTPS** em produção
- ❌ **Não compartilhamos dados** com marketers/publicidade

### 4.3 Responsabilidades do Usuário

Você é responsável por:
- 🔐 Manter seu `.env` seguro (não compartilhar)
- 🔐 Usar senha forte no Neon, MongoDB Atlas, Streamlit Cloud
- 🔐 Revogar tokens/chaves API se comprometidos
- 🔐 Não compartilhar dados financeiros em chat público
- 🔐 Fazer logout ao terminar sessão
- 🔐 Usar conexão segura (Wi-Fi confiável ou VPN)

### 4.4 Reporte de Vulnerabilidades (Responsável)

Se encontrar uma vulnerabilidade de segurança:

1. **NÃO publique** em issues públicas
2. **Envie para**: `contato@mestregrana.app` ou crie uma issue privada no GitHub
3. **Incluindo**:
   - Tipo de vulnerabilidade (SQL injection, XSS, CSRF, etc)
   - Passos detalhados para reproduzir
   - Impacto estimado
   - Sugestões de correção (opcional)
4. **SLA**: Responderemos em até 24 horas, corrigiremos em até 48 horas

## 5. Isenção de Responsabilidade

**VOCÊ UTILIZA O MESTREGRANA POR SUA CONTA E RISCO.**

Nem o desenvolvedor nem os provedores de IA (Groq, Google, OpenAI) são responsáveis por:
- Perda ou vazamento de dados
- Erros nas recomendações
- Multas ou penalidades tributárias resultantes do uso
- Mal funcionamento ou indisponibilidade do serviço
- Danos diretos, indiretos ou consequentes

## 6. Modificações dos Termos

Estes termos podem ser modificados a qualquer momento. Alterações importantes serão comunicadas no repositório GitHub. Continuar usando o app após mudanças equivale a aceitar os novos termos.

**Última atualização**: 17 de maio de 2026

---

## 7. Contato e Suporte

Para dúvidas sobre:
- **LGPD e privacidade**: Abra uma issue no GitHub
- **Sugestões de uso**: Veja docs/ no repositório
- **Bugs ou problemas**: Issues do repositório vdfs89/MestreGrana

---

**Ao usar o MestreGrana, você concorda com todos os termos acima.**
