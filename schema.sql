PRAGMA foreign_keys = ON;

-- =====================================
-- Tabela de usuários
-- =====================================
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cargo TEXT,
    centro_custo TEXT,
    departamento TEXT,
    termo_assinado TEXT CHECK (termo_assinado IN ('S','N')) NOT NULL
);

-- =====================================
-- Tabela de equipamentos
-- =====================================
CREATE TABLE equipamentos (
    patrimonio TEXT PRIMARY KEY,
    tipo TEXT,
    marca TEXT,
    modelo TEXT,
    numero_serie TEXT,
    sistema_operacional TEXT,
    memoria TEXT,
    ano_compra INTEGER,

    status_maquina TEXT,

    usuario_atual_id INTEGER,

    observacao TEXT,

    ultima_manutencao_preventiva TEXT,
    manutencao_preventiva_programada TEXT,

    FOREIGN KEY (usuario_atual_id)
        REFERENCES usuarios(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

-- =====================================
-- Tabela de movimentações
-- =====================================
CREATE TABLE movimentacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    patrimonio TEXT NOT NULL,

    usuario_anterior_id INTEGER,
    usuario_novo_id INTEGER,

    tipo_movimentacao TEXT NOT NULL,
    data_movimentacao TEXT NOT NULL,
    observacao TEXT,

    FOREIGN KEY (patrimonio)
        REFERENCES equipamentos(patrimonio)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    FOREIGN KEY (usuario_anterior_id)
        REFERENCES usuarios(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    FOREIGN KEY (usuario_novo_id)
        REFERENCES usuarios(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);