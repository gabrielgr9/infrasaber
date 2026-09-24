-- Init foi utilizado para caso a aplicação não suba automaticamente o banco, o mesmo irá subir com os códigos abaixo.

CREATE SCHEMA IF NOT EXISTS app;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS trusted;
CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.pontos_wifi_por_bairro (
    id SERIAL PRIMARY KEY,
    bairro VARCHAR(255),
    regiao VARCHAR(255),
    total_pontos INTEGER,
    total_ativos INTEGER,
    total_manutencao INTEGER,
    total_inativos INTEGER
);

CREATE TABLE IF NOT EXISTS trusted.pontos_wifi_prefeitura (
    id_ponto_externo VARCHAR(255) PRIMARY KEY,
    nome_local VARCHAR(255),
    tipo VARCHAR(50),
    endereco TEXT,
    bairro VARCHAR(255),
    subprefeitura VARCHAR(255),
    regiao VARCHAR(255),
    latitude NUMERIC(10, 8),
    longitude NUMERIC(11, 8),
    status VARCHAR(50),
    horario_funcionamento VARCHAR(255),
    descricao TEXT,
    link TEXT,
    cleaned_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS staging.pontos_wifi_prefeitura (
    id_ponto_externo VARCHAR(255) PRIMARY KEY,
    nome_local VARCHAR(255),
    tipo VARCHAR(50),
    endereco TEXT,
    bairro VARCHAR(255),
    subprefeitura VARCHAR(255),
    regiao VARCHAR(255),
    latitude NUMERIC(10, 8),
    longitude NUMERIC(11, 8),
    status VARCHAR(50),
    horario_funcionamento VARCHAR(255),
    descricao TEXT,
    link TEXT,
    ingested_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);