import polars as pl
from etl.load import carregar_dados

def filtrar_dados(df: pl.DataFrame):
    df_filtrado = df.filter(
        pl.all_horizontal(
            pl.col(
                "TP_PRESENCA_CN", 
                "TP_PRESENCA_CH", 
                "TP_PRESENCA_LC", 
                "TP_PRESENCA_MT"
            ) == 1
        )
    )

    return df_filtrado

def limpar_dados(df: pl.DataFrame):
    df_limpo = (
        df.with_columns(
            pl.col("Q006").fill_null("Não Informado")
        )
        .drop_nulls(subset=[
            "NU_NOTA_CN",
            "NU_NOTA_CH", 
            "NU_NOTA_LC", 
            "NU_NOTA_MT", 
            "NU_NOTA_REDACAO"
        ])
    )

    return df_limpo

def calcular_nota_media(df: pl.DataFrame):
    df_com_media = df.with_columns(
        (
            pl.sum_horizontal(
                "NU_NOTA_CN",
                "NU_NOTA_CH", 
                "NU_NOTA_LC", 
                "NU_NOTA_MT", 
                "NU_NOTA_REDACAO"
            ) / 5
        )
        .round(1)
        .alias("nota_media")
    )

    return df_com_media

def categorizar_renda(df: pl.DataFrame):
    df_categorizado = df.with_columns(
        pl.when(pl.col("Q006").is_in(["A", "B", "C", "D"])).then(pl.lit("Renda Baixa"))
        .when(pl.col("Q006").is_in(["E", "F", "G", "H", "I", "J", "K"])).then(pl.lit("Renda Média"))
        .when(pl.col("Q006").is_in(["L", "M", "N", "O", "P", "Q"])).then(pl.lit("Renda Alta"))
        .otherwise(pl.lit("Q006"))
        .alias("renda_categoria")
    )

    return df_categorizado

def transformar_dados(df: pl.DataFrame):
    df_filtrado = filtrar_dados(df)
    df_limpo = limpar_dados(df_filtrado)
    df_calculado = calcular_nota_media(df_limpo)
    df_categorizado = categorizar_renda(df_calculado)

    df_final = (
        df_categorizado
        .rename({"NU_INSCRICAO": "id_estudante"})
        .select(["id_estudante", "nota_media", "renda_categoria"])
    )

    return df_final
    

if __name__ == "__main__":
    df_mock = pl.DataFrame({
        "NU_INSCRICAO": [123, 456],
        "NU_NOTA_CN": [600.0, 500.0],
        "NU_NOTA_CH": [650.0, 500.0],
        "NU_NOTA_LC": [700.0, 500.0],
        "NU_NOTA_MT": [800.0, 500.0],
        "NU_NOTA_REDACAO": [900.0, 500.0],
        "TP_PRESENCA_CN": [1, 1], 
        "TP_PRESENCA_CH": [1, 1], 
        "TP_PRESENCA_LC": [1, 1], 
        "TP_PRESENCA_MT": [1, 1],
        "Q006": ["C", "G"]
    })

    df_transformado = transformar_dados(df_mock)
    carregar_dados(df_transformado)

    print(df_transformado)