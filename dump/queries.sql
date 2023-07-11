CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TABLE IF NOT EXISTS vacancies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(256) NOT NULL,
    company_name VARCHAR(256) NOT NULL,
    salary INTEGER NOT NULL DEFAULT 0,
    link VARCHAR(1024) NOT NULL,
    create_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_company_name ON vacancies (company_name);
