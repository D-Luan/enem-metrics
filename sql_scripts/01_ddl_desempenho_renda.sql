DROP TABLE IF EXISTS mart_desempenho_por_renda;

CREATE TABLE mart_desempenho_por_renda(
    id_estudante BIGINT PRIMARY KEY,
    nota_media DOUBLE PRECISION,
    renda_categoria VARCHAR(50)
);