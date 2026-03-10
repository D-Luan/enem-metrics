import polars as pl

def extrair_dados():
    caminho_arquivo = "./etl/data/MICRODADOS_ENEM_2023.csv"

    df_extraido = pl.read_csv(
        caminho_arquivo,
        separator=";",
        encoding="latin1",
        columns=[
            "NU_INSCRICAO",
            "TP_PRESENCA_CN",
            "TP_PRESENCA_CH",
            "TP_PRESENCA_LC",
            "TP_PRESENCA_MT",
            "NU_NOTA_CN",
            "NU_NOTA_CH",
            "NU_NOTA_LC",
            "NU_NOTA_MT",
            "NU_NOTA_REDACAO",
            "Q006"
        ]
    )

    return df_extraido

if __name__ == "__main__":
    df_extraido = extrair_dados()

    print("Extração concluída com sucesso!")
    print(df_extraido.head())