from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from psycopg_pool import AsyncConnectionPool
from psycopg import AsyncConnection
from config import get_postgres_uri
from src import database
from src.api.routes_metricas import router as metricas_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando as conexões com o banco de dados...")

    database.pool = AsyncConnectionPool(conninfo=get_postgres_uri(), open=False)
    await database.pool.open()

    yield

    print("Fechando as conexões do banco de dados...")
    if database.pool:
        await database.pool.close()

app = FastAPI(
    title="API ENEM Metrics",
    description="Sistema OLAP para análise de microdados do ENEM",
    version="1.0.0",   
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(metricas_router)

@app.get("/health")
async def health_check(db: AsyncConnection = Depends(database.get_db)):
    try:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT 1")
            resultado = await cursor.fetchone()

        return {"status": "ok", "banco_conectado": True, "teste_query": resultado[0]}
    except Exception as e:
        return {"status": "erro", "detalhe": str(e)}