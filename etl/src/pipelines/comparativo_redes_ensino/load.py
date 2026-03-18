import polars as pl
from utils.config import get_postgres_uri, conexao_postgres

def carregar_dados(df: pl.LazyFrame) -> pl.LazyFrame:
    uri = get_postgres_uri()

    with conexao_postgres(uri) as conn:
        with conn.cursor() as cur:
            print("Limpando dados da tabela com o TRUNCATE...")
            cur.execute("TRUNCATE TABLE mart_comparativo_redes_ensino;")
        conn.commit()

    df_coletado = df.collect()

    print("Inserindo dados na tabela...")
    df_coletado.write_database(
        table_name="mart_comparativo_redes_ensino",
        connection=uri,
        engine="adbc",
        if_table_exists="append"
    )

    print(f"Carga finalizada com sucesso! {df_coletado.height} linhas inseridas.")