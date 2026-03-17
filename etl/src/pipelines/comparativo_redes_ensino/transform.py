import polars as pl
from pipelines.comparativo_redes_ensino.extract import extrair_dados

def limpar_dados(df: pl.LazyFrame) -> pl.LazyFrame:
    df_limpo = df.drop_nulls([
        "TP_DEPENDENCIA_ADM_ESC",
        "NU_NOTA_CN",
        "NU_NOTA_CH",
        "NU_NOTA_LC",
        "NU_NOTA_MT",
        "NU_NOTA_REDACAO"
    ])

    return df_limpo

def filtrar_e_padronizar_escolas(df: pl.LazyFrame) -> pl.LazyFrame:
    df_padronizado = (
        df.filter(
            pl.col("TP_DEPENDENCIA_ADM_ESC").is_in([1, 2, 4])
        )
        .with_columns(
            pl.col("TP_DEPENDENCIA_ADM_ESC")
            .cast(pl.String)
            .replace({
                1: "Federal",
                2: "Estadual",
                4: "Privada"
            })
        )
    )

    return df_padronizado

def agregar_desempenho(df: pl.LazyFrame) -> pl.LazyFrame:
    df_agregado = df.group_by(["SG_UF_PROVA", "TP_DEPENDENCIA_ADM_ESC"]).agg([
        pl.col("NU_NOTA_MT").mean().round(2),
        pl.col("NU_NOTA_CN").mean().round(2),
        pl.col("NU_NOTA_CH").mean().round(2),
        pl.col("NU_NOTA_LC").mean().round(2),
        pl.col("NU_NOTA_REDACAO").mean().round(2),
        pl.len().cast(pl.Int32).alias("total_alunos")
    ])

    return df_agregado

def transformar_dados(df: pl.LazyFrame) -> pl.LazyFrame:
    df_limpo = limpar_dados(df)
    df_padronizado = filtrar_e_padronizar_escolas(df_limpo)
    df_agregado = agregar_desempenho(df_padronizado)

    df_final = df_agregado.rename({
        "SG_UF_PROVA": "uf",
        "TP_DEPENDENCIA_ADM_ESC": "tipo_escola",
        "NU_NOTA_MT": "media_matematica",
        "NU_NOTA_CN": "media_natureza",
        "NU_NOTA_CH": "media_humanas",
        "NU_NOTA_LC": "media_linguagens",
        "NU_NOTA_REDACAO": "media_redacao"
    })

    return df_final

if __name__ == "__main__":
    df_extraido = extrair_dados()
    df_final = transformar_dados(df_extraido)

    print("Dados transformados com sucesso!")
    print(df_final.head(5).collect())