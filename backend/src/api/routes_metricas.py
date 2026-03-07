from fastapi import APIRouter, Depends, HTTPException
from psycopg import AsyncConnection
from src.database import get_db
from src.repositories.metricas_repo import obter_comparacao_renda
from src.schemas.metricas import RespostaComparacaoRenda

router = APIRouter(prefix="/api/metricas", tags=["Métricas Análises"])

@router.get("/renda", response_model=RespostaComparacaoRenda)
async def comparacao_renda_nota(db: AsyncConnection = Depends(get_db)):
    try:
        dados_agrupados = await obter_comparacao_renda(db)
        return {"dados": dados_agrupados}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar métricas: {str(e)}")