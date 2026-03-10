import polars as pl
from polars.testing import assert_frame_equal
from etl.transform import filtrar_dados, limpar_dados, calcular_nota_media, categorizar_renda, transformar_dados

def test_filtrar_dados_deve_manter_apenas_alunos_presentes_nos_4_dias():
    df_entrada = pl.DataFrame({
        "NU_INSCRICAO": [1, 2, 3],
        "TP_PRESENCA_CN": [1, 1, 1],
        "TP_PRESENCA_CH": [0, 1, 1],
        "TP_PRESENCA_LC": [1, 1, 1],
        "TP_PRESENCA_MT": [1, 0, 1]
    })

    df_esperado = pl.DataFrame({
        "NU_INSCRICAO": [3],
        "TP_PRESENCA_CN": [1],
        "TP_PRESENCA_CH": [1],
        "TP_PRESENCA_LC": [1],
        "TP_PRESENCA_MT": [1]
    })

    df_resultado = filtrar_dados(df_entrada)
    assert_frame_equal(df_resultado, df_esperado)

def test_limpar_dados_deve_tratar_renda_nula_e_remover_notas_nulas():
    df_entrada = pl.DataFrame({
        "NU_INSCRICAO": [1, 2, 3],
        "Q006": ["A", None, "C"],
        "NU_NOTA_CN": [600.0, 500.0, None],
        "NU_NOTA_CH": [650.0, 500.0, 600.0],
        "NU_NOTA_LC": [700.0, 500.0, 600.0],
        "NU_NOTA_MT": [800.0, 500.0, 600.0],
        "NU_NOTA_REDACAO": [900.0, 500.0, 600.0]
    })

    df_esperado = pl.DataFrame({
        "NU_INSCRICAO": [1, 2],
        "Q006": ["A", "Não Informado"],
        "NU_NOTA_CN": [600.0, 500.0],
        "NU_NOTA_CH": [650.0, 500.0],
        "NU_NOTA_LC": [700.0, 500.0],
        "NU_NOTA_MT": [800.0, 500.0],
        "NU_NOTA_REDACAO": [900.0, 500.0]
    })

    df_resultado = limpar_dados(df_entrada)
    assert_frame_equal(df_resultado, df_esperado)

def test_calcular_nota_media_deve_somar_e_dividir_por_cinco_com_arredondamento():
    df_entrada = pl.DataFrame({
        "NU_INSCRICAO": [1, 2],
        "NU_NOTA_CN": [600.0, 500.5],
        "NU_NOTA_CH": [600.0, 600.0],
        "NU_NOTA_LC": [600.0, 550.0],
        "NU_NOTA_MT": [600.0, 700.0],
        "NU_NOTA_REDACAO": [600.0, 800.0]
    })

    df_esperado = pl.DataFrame({
        "NU_INSCRICAO": [1, 2],
        "NU_NOTA_CN": [600.0, 500.5],
        "NU_NOTA_CH": [600.0, 600.0],
        "NU_NOTA_LC": [600.0, 550.0],
        "NU_NOTA_MT": [600.0, 700.0],
        "NU_NOTA_REDACAO": [600.0, 800.0],
        "nota_media": [600.0, 630.1]
    })

    df_resultado = calcular_nota_media(df_entrada)
    assert_frame_equal(df_resultado, df_esperado)

def test_categorizar_renda_deve_mapear_letras_para_categorias_corretas():
    df_entrada = pl.DataFrame({
        "NU_INSCRICAO": [1, 2, 3, 4],
        "Q006": ["C", "G", "P", "Não Informado"]
    })

    df_esperado = pl.DataFrame({
        "NU_INSCRICAO": [1, 2, 3, 4],
        "Q006": ["C", "G", "P", "Não Informado"],
        "renda_categoria": ["Renda Baixa", "Renda Média", "Renda Alta", "Não Informado"]
    })

    df_resultado = categorizar_renda(df_entrada)
    assert_frame_equal(df_resultado, df_esperado)

def test_transformar_dados_deve_executar_pipeline_completo_e_retornar_schema_correto():
    df_entrada = pl.DataFrame({
        "NU_INSCRICAO": [100],
        "TP_PRESENCA_CN": [1], 
        "TP_PRESENCA_CH": [1], 
        "TP_PRESENCA_LC": [1], 
        "TP_PRESENCA_MT": [1],
        "NU_NOTA_CN": [500.0], 
        "NU_NOTA_CH": [500.0], 
        "NU_NOTA_LC": [500.0], 
        "NU_NOTA_MT": [500.0], 
        "NU_NOTA_REDACAO": [500.0],
        "Q006": ["C"]
    })

    df_esperado = pl.DataFrame({
        "id_estudante": [100],
        "nota_media": [500.0],
        "renda_categoria": ["Renda Baixa"]
    })

    df_resultado = transformar_dados(df_entrada)
    assert_frame_equal(df_resultado, df_esperado)