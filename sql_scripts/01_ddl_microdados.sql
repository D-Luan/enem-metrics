DROP TABLE IF EXISTS microdados_enem_tratado;

CREATE TABLE microdados_enem_tratado(
    id_estudante BIGINT PRIMARY KEY,
    nota_media NUMERIC,
    renda_categoria VARCHAR(50)
);