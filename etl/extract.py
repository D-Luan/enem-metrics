import polars as pl
from transform import transformar_dados

def extrair_dados():
    caminho_arquivo = "./data/MICRODADOS_ENEM_2023.csv"

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
    df = extrair_dados()
    df_transformado = transformar_dados(df)

    print("Extração concluída com sucesso!")
    print(df_transformado.head())