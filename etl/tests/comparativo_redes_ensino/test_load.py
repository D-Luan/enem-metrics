import os
import pytest
import polars as pl
import adbc_driver_postgresql.dbapi as dbapi
from dotenv import load_dotenv
from pipelines.comparativo_redes_ensino.load import carregar_dados
from utils.config import get_postgres_uri, conexao_postgres

load_dotenv()

@pytest.fixture
def setup_banco_teste(monkeypatch):
    load_dotenv(".env.local", override=True)

    db_password = os.getenv("DB_PASSWORD", "postgres")

    monkeypatch.setenv("DB_USER", "postgres")
    monkeypatch.setenv("DB_PASSWORD", db_password)
    monkeypatch.setenv("DB_NAME", "metricas_teste")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")

    uri = get_postgres_uri()

    with conexao_postgres(uri) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS mart_comparativo_redes_ensino (
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
            """)
        conn.commit()

    yield uri

    with conexao_postgres(uri) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS mart_comparativo_redes_ensino;")
        conn.commit()

def test_carregar_dados_deve_inserir_dataframe_no_postgres(setup_banco_teste):
    df_mock = pl.DataFrame({
        "uf": ["PE", "SP", "RJ"], 
        "tipo_escola": ["Federal", "Estadual", "Privada"], 
        "media_matematica": [740.0, 650.0, 450.0], 
        "media_natureza": [550.0, 680.0, 500.0], 
        "media_humanas": [500.0, 520.0, 400.0], 
        "media_linguagens": [620.0, 340.0, 740.0], 
        "media_redacao": [800.0, 600.0, 400.0], 
        "total_alunos": pl.Series([1, 1, 1], dtype=pl.Int32)
    }).lazy()

    carregar_dados(df_mock)

    with conexao_postgres(setup_banco_teste) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM mart_comparativo_redes_ensino ORDER BY uf;")
            resultados = cur.fetchall()

    assert len(resultados) == 3
    assert resultados[0][0] == "PE"
    assert resultados[0][1] == "Federal"