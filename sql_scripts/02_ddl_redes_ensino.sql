DROP TABLE IF EXISTS mart_comparativo_redes_ensino;

CREATE TABLE mart_comparativo_redes_ensino (
    uf VARCHAR(2),
    tipo_escola VARCHAR(50),
    media_matematica DOUBLE PRECISION,
    media_natureza DOUBLE PRECISION,
    media_humanas DOUBLE PRECISION,
    media_linguagens DOUBLE PRECISION,
    media_redacao DOUBLE PRECISION,
    total_alunos INT,
    PRIMARY KEY (uf, tipo_escola)
);