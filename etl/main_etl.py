import time
from etl.extract import extrair_dados
from etl.transform import transformar_dados
from etl.load import carregar_dados

def executar_pipeline():
    print("Executando a pipeline ETL...")
    inicio = time.time()
    
    try:
        print("Extraindo dados...")
        df_extraido = extrair_dados()

        print("Transformando dados...")
        df_transformado = transformar_dados(df_extraido)

        print("Carregando dados...")
        carregar_dados(df_transformado)

        fim = time.time()
        print(f"Pipeline ETL executado com sucesso! Finalizado em {fim - inicio:.2f} segundos.")
    except Exception as e:
        print(f"Erro ao executar o pipeline: {e}")

if __name__ == "__main__":
    executar_pipeline()