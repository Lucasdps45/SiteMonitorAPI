CREATE TABLE targets (
    id        SERIAL PRIMARY KEY,
    url       TEXT NOT NULL,
    itervalo  INTEGER NOT NULL DEFAULT 60,
    ativo     BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE checks (
    id          SERIAL PRIMARY KEY,
    target_id   INTEGER NOT NULL REFERENCES targets(id) ON DELETE CASCADE,
    status_code INTEGER,
    latencia_ms INTEGER,
    is_up       BOOLEAN NOT NULL,
    checado_em  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE incidents (
    id          SERIAL PRIMARY KEY,
    target_id   INTEGER NOT NULL REFERENCES targets(id) ON DELETE CASCADE,
    inicio      TIMESTAMP NOT NULL,
    fim         TIMESTAMP,
    duracao_seg INTEGER
);