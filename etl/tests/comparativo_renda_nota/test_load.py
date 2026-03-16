import pytest
import polars as pl
import adbc_driver_postgresql.dbapi as dbapi
from pipelines.desempenho_por_renda.load import carregar_dados
from utils.config import get_postgres_uri, conexao_postgres

@pytest.fixture
def setup_banco_teste(monkeypatch):
    monkeypatch.setenv("DB_USER", "postgres")
    monkeypatch.setenv("DB_PASSWORD", "postgres")
    monkeypatch.setenv("DB_NAME", "enem_teste")
    monkeypatch.setenv("DB_HOST", "127.0.0.1")
    monkeypatch.setenv("DB_PORT", "5432")

    uri = get_postgres_uri()
    
    with conexao_postgres(uri) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS mart_desempenho_por_renda (
                    id_estudante BIGINT,
                    nota_media DOUBLE PRECISION,
                    renda_categoria TEXT
                );
            """)
        conn.commit()
    
    yield uri 
    
    with conexao_postgres(uri) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS mart_desempenho_por_renda;")
        conn.commit()

def test_carregar_dados_deve_inserir_dataframe_no_postgres(setup_banco_teste):
    df_mock = pl.DataFrame({
        "id_estudante": [101, 102],
        "nota_media": [650.5, 720.0],
        "renda_categoria": ["Renda Baixa", "Renda Alta"]
    })

    carregar_dados(df_mock)

    with conexao_postgres(setup_banco_teste) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM mart_desempenho_por_renda ORDER BY id_estudante;")
            resultados = cur.fetchall()

    assert len(resultados) == 2
    assert resultados[0][0] == 101
    assert resultados[0][1] == 650.5