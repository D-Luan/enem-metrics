from typing import AsyncGenerator
from psycopg import AsyncConnection
from psycopg_pool import AsyncConnectionPool

pool: AsyncConnectionPool | None = None

async def get_db() -> AsyncGenerator[AsyncConnection, None]:
    if pool is None:
        raise RuntimeError("Pool de conexões do banco de dados não foi inicializado.")
    
    async with pool.connection() as conn:
        yield conn
