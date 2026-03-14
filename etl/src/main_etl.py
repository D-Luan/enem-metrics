import time
from pipelines.desempenho_por_renda.extract import extrair_dados as extrair_renda
from pipelines.desempenho_por_renda.transform import transformar_dados as transformar_renda
from pipelines.desempenho_por_renda.load import carregar_dados as carregar_renda

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
        print(f"Erro ao executar o pipeline: {e}")

if __name__ == "__main__":
    executar_pipeline_renda()