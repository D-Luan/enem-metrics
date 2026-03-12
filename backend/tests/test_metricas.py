import os
import pytest
import psycopg
from fastapi.testclient import TestClient
from src.config import get_postgres_uri
from src.main import app

TEST_DB_URL = get_postgres_uri()

@pytest.fixture(scope='module', autouse=True)
def setup_banco_teste():
    with psycopg.connect(TEST_DB_URL, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS microdados_enem_tratado (
                    id_estudante BIGINT PRIMARY KEY,
                    nota_media DOUBLE PRECISION,
                    renda_categoria VARCHAR(50)
                )
            """)

            cur.execute("TRUNCATE TABLE microdados_enem_tratado;")

            cur.execute("INSERT INTO microdados_enem_tratado VALUES (1, 500.0, 'Renda Baixa')")
            cur.execute("INSERT INTO microdados_enem_tratado VALUES (2, 750.0, 'Renda Alta')")
            cur.execute("INSERT INTO microdados_enem_tratado VALUES (3, 650.0, 'Renda Média')")
            cur.execute("INSERT INTO microdados_enem_tratado VALUES (4, 450.0, 'Renda Baixa')")

    yield

def test_get_health_deve_retornar_status_200_e_banco_conectado_true():
    with TestClient(app) as client:
        resposta = client.get("/health")
        assert resposta.status_code == 200
        assert resposta.json()["banco_conectado"] is True

def test_get_metricas_renda_deve_retornar_agrupamento_matematico_correto_dos_microdados_mockados():
    with TestClient(app) as client:
        resposta = client.get("/metricas/renda")
        assert resposta.status_code == 200

        dados = resposta.json()["dados"]
        assert len(dados) > 0

        faixa_nota = next(item for item in dados if item["faixa_nota"] == "0-599")
        assert faixa_nota["qtd_renda_baixa"] == 2
        assert faixa_nota["pct_renda_baixa"] == 100.0