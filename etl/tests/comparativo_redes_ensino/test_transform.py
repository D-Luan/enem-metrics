import polars as pl
from polars.testing import assert_frame_equal
from pipelines.comparativo_redes_ensino.transform import limpar_dados, filtrar_e_padronizar_escolas, agregar_desempenho, transformar_dados

def test_limpar_dados_deve_tratar_escolas_e_notas_nulas():
    df_entrada = pl.DataFrame({
        "TP_DEPENDENCIA_ADM_ESC": [None, 2, 4], 
        "NU_NOTA_CN": [650.0, 810.0, 720.0], 
        "NU_NOTA_CH": [700.0, 620.0, 500.0], 
        "NU_NOTA_LC": [450.0, 800.0, None], 
        "NU_NOTA_MT": [600.0, 580.0, 720.0], 
        "NU_NOTA_REDACAO": [300.0, 700.0, 920.0]
    }).lazy()

    df_esperado = pl.DataFrame({
        "TP_DEPENDENCIA_ADM_ESC": [2], 
        "NU_NOTA_CN": [810.0], 
        "NU_NOTA_CH": [620.0], 
        "NU_NOTA_LC": [800.0], 
        "NU_NOTA_MT": [580.0], 
        "NU_NOTA_REDACAO": [700.0]
    }).lazy()

    df_resultado = limpar_dados(df_entrada)
    assert_frame_equal(df_resultado.collect(), df_esperado.collect())

def test_filtrar_e_padronizar_dados_deve_manter_apenas_escolas_especificas():
    df_entrada = pl.DataFrame({ 
        "TP_DEPENDENCIA_ADM_ESC": [1, 2, 2, 1, 3, 4, 4, 3]
    }).lazy()

    df_esperado = pl.DataFrame({
        "TP_DEPENDENCIA_ADM_ESC": ["Federal", "Estadual", "Estadual", "Federal", "Privada", "Privada"]
    }).lazy()

    df_resultado = filtrar_e_padronizar_escolas(df_entrada)
    assert_frame_equal(df_resultado.collect(), df_esperado.collect())

def test_agregar_desempenho_deve_calcular_media_das_notas_e_quantidade_de_alunos():
    df_entrada = pl.DataFrame({
        "SG_UF_PROVA": ["PE", "PE", "PE"], 
        "TP_DEPENDENCIA_ADM_ESC": ["Federal", "Estadual", "Federal"], 
        "NU_NOTA_MT": [550.0, 800.0, 650.0], 
        "NU_NOTA_CN": [750.0, 420.0, 700.0], 
        "NU_NOTA_CH": [630.0, 500.0, 600.0], 
        "NU_NOTA_LC": [650.0, 500.0, 450.0], 
        "NU_NOTA_REDACAO": [600.0, 810.0, 450.0]
    }).lazy()

    df_esperado = pl.DataFrame({
        "SG_UF_PROVA": ["PE", "PE"], 
        "TP_DEPENDENCIA_ADM_ESC": ["Federal", "Estadual"], 
        "NU_NOTA_MT": [600.0, 800.0], 
        "NU_NOTA_CN": [725.0, 420.0], 
        "NU_NOTA_CH": [615.0, 500.0], 
        "NU_NOTA_LC": [550.0, 500.0], 
        "NU_NOTA_REDACAO": [525.0, 810.0],
        "total_alunos": pl.Series([2, 1], dtype=pl.Int32)
    }).lazy()

    df_resultado = agregar_desempenho(df_entrada)
    assert_frame_equal(df_resultado.collect(), df_esperado.collect(), check_row_order=False)

def test_transformar_dados_deve_executar_pipeline_completo_e_retornar_schema_correto():
    df_entrada = pl.DataFrame({
        "SG_UF_PROVA": ["PE", "SP", "RJ"], 
        "TP_DEPENDENCIA_ADM_ESC": [1, 2, 4], 
        "NU_NOTA_MT": [740.0, 650.0, 450.0], 
        "NU_NOTA_CN": [550.0, 680.0, 500.0], 
        "NU_NOTA_CH": [500.0, 520.0, 400.0], 
        "NU_NOTA_LC": [620.0, 340.0, 740.0], 
        "NU_NOTA_REDACAO": [800.0, 600.0, 400.0]
    }).lazy()

    df_esperado = pl.DataFrame({
        "uf": ["PE", "SP", "RJ"], 
        "tipo_escola": ["Federal", "Estadual", "Privada"], 
        "media_matematica": [740.0, 650.0, 450.0], 
        "media_natureza": [550.0, 680.0, 500.0], 
        "media_humanas": [500.0, 520.0, 400.0], 
        "media_linguagens": [620.0, 340.0, 740.0], 
        "media_redacao": [800.0, 600.0, 400.0], 
        "total_alunos": pl.Series([1, 1, 1], dtype=pl.Int32)
    }).lazy()

    df_resultado = transformar_dados(df_entrada)
    assert_frame_equal(df_resultado.collect(), df_esperado.collect(), check_row_order=False)