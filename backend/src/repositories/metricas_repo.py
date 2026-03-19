from psycopg import AsyncConnection

async def obter_comparacao_renda(conn: AsyncConnection) -> list[dict]:
    query = """
        WITH faixas AS (
            SELECT renda_categoria,
                CASE
                    -- Labels com faixa de nota para o gráfico
                    WHEN nota_media < 600 THEN '0-599'
                    WHEN nota_media < 700 THEN '600-699'
                    WHEN nota_media < 800 THEN '700-799'
                    WHEN nota_media < 900 THEN '800-899'
                    ELSE '900-1000'
                END AS faixa_nota
            FROM mart_desempenho_por_renda
        ),
        agrupamento AS (
            SELECT faixa_nota,
                -- Conta quantas notas de cada renda existem em cada faixa
                COUNT(*) FILTER (WHERE renda_categoria = 'Renda Baixa') AS qtd_renda_baixa,
                COUNT(*) FILTER (WHERE renda_categoria = 'Renda Média') AS qtd_renda_media,
                COUNT(*) FILTER (WHERE renda_categoria = 'Renda Alta') AS qtd_renda_alta,
                COUNT(*) AS total_notas
            FROM faixas
            GROUP BY faixa_nota
        )

        SELECT
            faixa_nota,
            qtd_renda_baixa,
            qtd_renda_media,
            qtd_renda_alta,
            total_notas,
            -- Calcula a porcentagem de cada renda
            ROUND((qtd_renda_baixa * 100.0 / NULLIF(total_notas, 0)), 1) AS pct_renda_baixa,
            ROUND((qtd_renda_media * 100.0 / NULLIF(total_notas, 0)), 1) AS pct_renda_media,
            ROUND((qtd_renda_alta * 100.0 / NULLIF(total_notas, 0)), 1) AS pct_renda_alta
        FROM agrupamento
        ORDER BY faixa_nota;
    """

    async with conn.cursor() as cur:
        await cur.execute(query)

        colunas = [desc.name for desc in cur.description]
        linhas = await cur.fetchall()

        resultado = [dict(zip(colunas, linha)) for linha in linhas]
        return resultado