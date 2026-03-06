from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from psycopg_pool import AsyncConnectionPool
from psycopg import AsyncConnection
from config import get_postgres_uri
from src import database

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando as conexões com o banco de dados...")

    database.pool = AsyncConnectionPool(conninfo=get_postgres_uri())

    yield

    print("Fechando as conexões do banco de dados...")
    if database.pool:
        await database.pool.close()

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health_check(db: AsyncConnection = Depends(database.get_db)):
    try:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT 1")
            resultado = await cursor.fetchone()

        return {"status": "ok", "banco_conectado": True, "teste_query": resultado[0]}
    except Exception as e:
        return {"status": "erro", "detalhe": str(e)}