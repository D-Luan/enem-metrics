import os
import polars as pl

def extrair_dados():
    caminho_arquivo = os.getenv("DATA_PATH", "./etl/data/MICRODADOS_ENEM_2023.csv")

    df_extraido = pl.read_csv(
        caminho_arquivo,
        separator=";",
        encoding="latin1",
        null_values=["", "NA"],
        columns=[
            "SG_UF_PROVA",
            "TP_DEPENDENCIA_ADM_ESC",
            "NU_NOTA_MT",
            "NU_NOTA_CN",
            "NU_NOTA_CH",
            "NU_NOTA_LC",
            "NU_NOTA_REDACAO",
            "NU_INSCRICAO"
        ]
    ).lazy()

    return df_extraido

if __name__ == "__main__":
    df_extraido = extrair_dados()

    print("Dados extraídos com sucesso!")
    print(df_extraido.head().collect())