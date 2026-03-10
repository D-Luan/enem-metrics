import pytest
import polars as pl
import adbc_driver_postgresql.dbapi as dbapi
from etl.load import carregar_dados
from etl.config import get_postgres_uri

@pytest.fixture
def setup_banco_teste(monkeypatch):
    monkeypatch.setenv("DB_USER", "postgres")
    monkeypatch.setenv("DB_PASSWORD", "postgres")
    monkeypatch.setenv("DB_NAME", "enem_teste")
    monkeypatch.setenv("DB_HOST", "127.0.0.1")
    monkeypatch.setenv("DB_PORT", "5432")

    uri = get_postgres_uri()
    
    conn = dbapi.connect(uri)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS microdados_enem_tratado (
                id_estudante BIGINT,
                nota_media DOUBLE PRECISION,
                renda_categoria TEXT
            );
        """)
    conn.commit()
    conn.close()
    
    yield uri 
    
    conn = dbapi.connect(uri)
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS microdados_enem_tratado;")
    conn.commit()
    conn.close()

def test_carregar_dados_deve_inserir_dataframe_no_postgres(setup_banco_teste):
    df_mock = pl.DataFrame({
        "id_estudante": [101, 102],
        "nota_media": [650.5, 720.0],
        "renda_categoria": ["Renda Baixa", "Renda Alta"]
    })

    carregar_dados(df_mock)

    conn = dbapi.connect(setup_banco_teste)
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM microdados_enem_tratado ORDER BY id_estudante;")
        resultados = cur.fetchall()
    conn.close()

    assert len(resultados) == 2
    assert resultados[0][0] == 101
    assert resultados[0][1] == 650.5