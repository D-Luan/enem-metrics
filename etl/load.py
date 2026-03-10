import polars as pl
import adbc_driver_postgresql.dbapi as dbapi
from etl.config import get_postgres_uri, conexao_postgres

def carregar_dados(df: pl.DataFrame):
    uri = get_postgres_uri()

    with conexao_postgres(uri) as conn:
        with conn.cursor() as cur:
            print("Limpando dados da tabela com o TRUNCATE...")
            cur.execute("TRUNCATE TABLE microdados_enem_tratado;")
        conn.commit()
        
    print("Inserindo novos dados a tabela...")
    df.write_database(
        table_name="microdados_enem_tratado",
        connection=uri,
        engine="adbc",
        if_table_exists="append"
    )

    print(f"Carga finalizada com sucesso! {df.height} linhas inseridas.")
   
