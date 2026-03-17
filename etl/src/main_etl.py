import time
import argparse
from pipelines.desempenho_por_renda.extract import extrair_dados as extrair_renda
from pipelines.desempenho_por_renda.transform import transformar_dados as transformar_renda
from pipelines.desempenho_por_renda.load import carregar_dados as carregar_renda
from pipelines.comparativo_redes_ensino.extract import extrair_dados as extrair_redes
from pipelines.comparativo_redes_ensino.transform import transformar_dados as transformar_redes
from pipelines.comparativo_redes_ensino.load import carregar_dados as carregar_redes

def executar_pipeline_renda():
    print("Executando a pipeline de Desempenho por Renda...")
    inicio = time.time()
    
    try:
        print("Extraindo dados...")
        df_extraido = extrair_renda()

        print("Transformando dados...")
        df_transformado = transformar_renda(df_extraido)

        print("Carregando dados...")
        carregar_renda(df_transformado)

        fim = time.time()
        print(f"Pipeline do Desempenho por Renda executado com sucesso! Finalizado em {fim - inicio:.2f} segundos.")
    except Exception as e:
        print(f"Erro ao executar a pipeline de Desempenho por Renda: {e}")

def executar_pipeline_redes_ensino():
    print("Executando a pipeline de Desempenho por Redes de Ensino...")
    inicio = time.time()

    try:
        print("Extraindo dados...")
        df_extraido = extrair_redes()

        print("Transformando dados...")
        df_transformado = transformar_redes(df_extraido)

        print("Carregando dados...")
        carregar_redes(df_transformado)

        fim = time.time()
        print(f"Pipeline de Desempenho por Redes de Ensino executado com sucesso! Finalizado em {fim - inicio:.2f} segundos.")
    except Exception as e:
        print(f"Erro ao executar a pipeline de Desempenho por Redes de Ensino: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Orquestrador do ETL EnemMetrics")
    parser.add_argument(
        "--pipeline",
        type=str,
        required=True,
        choices=["renda", "redes_ensino", "todas"],
        help="Qual pipeline você deseja executar?"
    )
    
    args = parser.parse_args()

    match args.pipeline:
        case "renda":
            executar_pipeline_renda()
        case "redes_ensino":
            executar_pipeline_redes_ensino()
        case "todas":
            executar_pipeline_renda()
            print("\n" + "="*60)
            executar_pipeline_redes_ensino()

    print("\nProcesso ETL concluído!")