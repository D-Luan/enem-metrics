import polars as pl
from utils.config import get_postgres_uri, conexao_postgres

def carregar_dados(df: pl.DataFrame):
    uri = get_postgres_uri()

    with conexao_postgres(uri) as conn:
        with conn.cursor() as cur:
            print("Limpando dados da tabela com o TRUNCATE...")
            cur.execute("TRUNCATE TABLE mart_desempenho_por_renda;")
        conn.commit()
        
    print("Inserindo novos dados a tabela...")
    df.write_database(
        table_name="mart_desempenho_por_renda",
        connection=uri,
        engine="adbc",
        if_table_exists="append"
    )

    print(f"Carga finalizada com sucesso! {df.height} linhas inseridas.")
   
