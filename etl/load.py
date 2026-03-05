import polars as pl
import adbc_driver_postgresql.dbapi as dbapi
from config import get_postgres_uri

def carregar_dados(df: pl.DataFrame):
    uri = get_postgres_uri()

    try:
        conn = dbapi.connect(uri)

        with conn.cursor() as cur:
            print("Limpando dados da tabela com o TRUNCATE...")
            cur.execute("TRUNCATE TABLE microdados_enem_tratado;")

        conn.commit()
        conn.close()

        print("Inserindo novos dados a tabela...")
        df.write_database(
            table_name="microdados_enem_tratado",
            connection=uri,
            engine="adbc",
            if_table_exists="append"
        )

        print(f"Carga finalizada com sucesso! {df.height} linhas inseridas.")
    except Exception as e:
        print(f"Erro ao carregar dados no banco: {e}")
        raise e

