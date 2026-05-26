-- Schema PostgreSQL otimizado para NeonDB
-- Executa com segurança usando IF NOT EXISTS

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_tax_deductible BOOLEAN DEFAULT FALSE
);

ALTER TABLE categories
ADD COLUMN IF NOT EXISTS is_tax_deductible BOOLEAN DEFAULT FALSE;

CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    type VARCHAR(3) NOT NULL CHECK (type IN ('REC', 'DES')),
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS budgets (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    month_year VARCHAR(7) NOT NULL,
    budget_limit NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS debts (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(id) ON DELETE CASCADE,
    debt_type VARCHAR(100) NOT NULL,
    total_amount NUMERIC(10, 2) NOT NULL,
    monthly_installment NUMERIC(10, 2) NOT NULL,
    interest_rate NUMERIC(5, 2) NOT NULL,
    is_late BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_insights (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(id) ON DELETE CASCADE,
    insight_text TEXT NOT NULL,
    relevance_score INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Conformidade Tributária (IRPF)
CREATE TABLE IF NOT EXISTS tax_compliance (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(id) ON DELETE CASCADE,
    cpf VARCHAR(11),
    income_type VARCHAR(50), -- salário, PJ, freela, MEI, etc
    fiscal_year INTEGER,
    total_income NUMERIC(14, 2),
    deductible_expenses NUMERIC(14, 2),
    estimated_tax_liability NUMERIC(14, 2),
    validation_status VARCHAR(20), -- draft, pending_review, validated
    last_reviewed_by VARCHAR(255), -- contador responsável
    last_reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Auditoria e Rastreabilidade
CREATE TABLE IF NOT EXISTS audit_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    operation VARCHAR(10) NOT NULL, -- INSERT, UPDATE, DELETE
    record_id INTEGER,
    changed_by VARCHAR(255),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    old_values JSONB,
    new_values JSONB,
    ip_address VARCHAR(45)
);

-- Documentação de Suporte (Notas Fiscais, Recibos, etc)
CREATE TABLE IF NOT EXISTS supporting_documents (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(id) ON DELETE CASCADE,
    transaction_id INTEGER REFERENCES transactions(id) ON DELETE SET NULL,
    document_type VARCHAR(50), -- invoice, receipt, bank_statement, etc
    document_url TEXT,
    file_hash VARCHAR(64), -- SHA-256 para integridade
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_verified BOOLEAN DEFAULT FALSE
);

-- Consentimento de Cookies e Dados (LGPD)
CREATE TABLE IF NOT EXISTS user_consents (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(id) ON DELETE CASCADE,
    consent_type VARCHAR(50), -- cookies_analytics, marketing_email, data_processing, etc
    consent_data JSONB, -- {'necessary': true, 'analytics': true, 'preferences': false, 'timestamp': '2026-05-17T...', 'version': '1.0'}
    consented_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    revoked_at TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    UNIQUE(user_id, consent_type, consented_at)
);

-- Índices úteis para consultas frequentes
CREATE INDEX IF NOT EXISTS idx_transactions_user_date ON transactions(user_id, transaction_date DESC);
CREATE INDEX IF NOT EXISTS idx_transactions_category ON transactions(category_id);
CREATE INDEX IF NOT EXISTS idx_budgets_user_month ON budgets(user_id, month_year);
CREATE INDEX IF NOT EXISTS idx_debts_user ON debts(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_insights_user_date ON ai_insights(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_tax_compliance_user_year ON tax_compliance(user_id, fiscal_year DESC);
CREATE INDEX IF NOT EXISTS idx_audit_log_table_date ON audit_log(table_name, changed_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_log_user ON audit_log(changed_by);
CREATE INDEX IF NOT EXISTS idx_supporting_docs_transaction ON supporting_documents(transaction_id);
CREATE INDEX IF NOT EXISTS idx_user_consents_user_type ON user_consents(user_id, consent_type);
CREATE INDEX IF NOT EXISTS idx_user_consents_timestamp ON user_consents(consented_at DESC);
