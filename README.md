# EnemMetrics

## Status do Projeto
**Em Desenvolvimento (Prova de Conceito)**

Este projeto utiliza a abordagem "Tracer Bullet" para validar a arquitetura e o fluxo de dados antes de processar a base completa. O foco atual é a funcionalidade de comparação de notas por renda.

## Funcionalidade Atual
- **Comparação de Notas por Renda**: Geração de dados mockados simulando a distribuição de notas do ENEM para diferentes faixas de renda.
- **API Backend**: Endpoint funcional que retorna dados prontos para consumo por gráficos no frontend.

## Tecnologias
- Python 3.x
- FastAPI
- Uvicorn

## Como Executar

1. **Instale as dependências**:
   ```bash
   pip install "fastapi[standard]"
   ```

2. **Execute o servidor**:
   ```bash
   fastapi dev main.py
   ```

3. **Acesse a documentação interativa (OpenAPI)**:
   - URL: `http://127.0.0.1:8000/docs`

## Endpoints Disponíveis

GET `/api/comparacao/nota-renda`

Retorna um JSON com a distribuição percentual de notas por faixa de renda.

**Exemplo de Resposta:**
```json
{
  "labels": ["500-599", "600-699", "700-799", "800-899", "900-999"],
  "datasets": [
    {
      "label": "Renda Alta",
      "data": [0, 25.05, 25.61, 24.54, 24.8]
    },
    {
      "label": "Renda Média",
      "data": [24.75, 25.74, 25.71, 23.8, 0]
    },
    {
      "label": "Renda Baixa",
      "data": [32.14, 33.3, 34.57, 0, 0]
    }
  ]
}
```

## Próximos Passos
- Criar interface frontend para exibição do gráfico.
- Substituir dados mockados pela leitura real do arquivo CSV.
- Implementar novos filtros de análise (ex: região, escola pública/privada).