DROP TABLE IF EXISTS servicos_tecnicos;
DROP TABLE IF EXISTS ordens;
DROP TABLE IF EXISTS equipamentos;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    cargo TEXT NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_usuarios_nome ON usuarios(nome);
CREATE INDEX idx_usuarios_email ON usuarios(email);

CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    telefone TEXT NOT NULL,
    endereco TEXT NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_clientes_nome ON clientes(nome);
CREATE INDEX idx_clientes_telefone ON clientes(telefone);

CREATE TABLE equipamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    marca TEXT NOT NULL,
    modelo TEXT NOT NULL,
    serie TEXT,
    estado_equipamento TEXT NOT NULL,
    defeito_relatado TEXT NOT NULL,
    codigo_barras TEXT UNIQUE,
    foto1 TEXT,
    foto2 TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
);

CREATE INDEX idx_equipamentos_cliente ON equipamentos(cliente_id);
CREATE INDEX idx_equipamentos_serie ON equipamentos(serie);
CREATE INDEX idx_equipamentos_codigo ON equipamentos(codigo_barras);

CREATE TABLE ordens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipamento_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    declaracao TEXT,
    relatorio_pecas TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    visivel INTEGER DEFAULT 1,
    FOREIGN KEY (equipamento_id) REFERENCES equipamentos (id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
);

CREATE INDEX idx_ordens_equipamento ON ordens(equipamento_id);
CREATE INDEX idx_ordens_usuario ON ordens(usuario_id);
CREATE INDEX idx_ordens_status ON ordens(status);
CREATE INDEX idx_ordens_data ON ordens(data_criacao);

CREATE TABLE IF NOT EXISTS servicos_tecnicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ordem_id INTEGER NOT NULL,
    diagnostico TEXT NOT NULL,
    descricao_servico TEXT NOT NULL,
    valor_mao_obra REAL NOT NULL,
    servico_realizado TEXT NOT NULL,
    produtos TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ordem_id) REFERENCES ordens (id)
);

CREATE INDEX idx_servicos_ordem ON servicos_tecnicos(ordem_id);
